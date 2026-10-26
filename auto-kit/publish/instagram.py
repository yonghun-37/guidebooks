"""Instagram Login: limit → create → poll → publish. POST는 자동 재전송하지 않는다."""
import re
import time
from pathlib import Path
from common import read_json, save_json, hashed
from transport import Deferred, Uncertain, RemoteError, read_retry

def request_plan(urls, target, *, account='<IG_USER_ID>', version='v26.0'):
    base = f'https://graph.instagram.com/{version}'
    steps = [{'method': 'GET', 'url': f'{base}/{account}/content_publishing_limit', 'params': {'fields': 'quota_usage,config'}}]
    def create(name, params):
        steps.extend([{'method': 'POST', 'url': f'{base}/{account}/media', 'data': params, 'save_as': name}, {'method': 'GET', 'url': base + '/{' + name + '}', 'params': {'fields': 'status_code'}, 'until': 'FINISHED'}])
    ai = str(target['is_ai_generated']).lower()
    if target.get('format') == 'reel':
        create('PARENT', {'media_type': 'REELS', 'video_url': urls[0], 'caption': target['caption'], 'is_ai_generated': ai})
    elif len(urls) == 1:
        create('PARENT', {'image_url': urls[0], 'caption': target['caption'], 'is_ai_generated': ai})
    else:
        for i, url in enumerate(urls):
            create(f'CHILD_{i}', {'image_url': url, 'is_carousel_item': 'true'})
        create('PARENT', {'media_type': 'CAROUSEL', 'children': ','.join('{CHILD_' + str(i) + '}' for i in range(len(urls))), 'caption': target['caption'], 'is_ai_generated': ai})
    steps.append({'method': 'POST', 'url': f'{base}/{account}/media_publish', 'data': {'creation_id': '{PARENT}'}})
    return {'mode': 'dry-run', 'login': 'Instagram Login', 'network_calls': 0, 'authorization': 'Bearer <REDACTED>', 'requests': steps}

class Instagram:
    def __init__(self, http, *, token, account, version='v26.0', safety_limit=50, sleep=time.sleep):
        if not str(account).isdigit() or not re.fullmatch(r'v\d+\.\d+', version):
            raise ValueError('Instagram 계정 ID·API 버전을 확인하세요.')
        self.http, self.account, self.sleep = http, str(account), sleep
        self.headers = {'Authorization': 'Bearer ' + token}
        self.base = f'https://graph.instagram.com/{version}'
        self.safety_limit = safety_limit

    def limit(self):
        try:
            raw = read_retry(self.http, f'{self.base}/{self.account}/content_publishing_limit', params={'fields': 'quota_usage,config'}, headers=self.headers, sleep=self.sleep)['data'][0]
            used, total = raw['quota_usage'], raw['config']['quota_total']
            if type(used) is not int or type(total) is not int or total <= 0 or used < 0:
                raise KeyError()
        except (ValueError, KeyError, IndexError, TypeError):
            raise Deferred('Instagram 한도를 확인하지 못해 발행을 연기합니다. 임의 100을 적용하지 않습니다.') from None
        if used >= min(total, self.safety_limit):
            raise Deferred('Instagram 계정/키트 게시 한도에 도달해 발행을 연기합니다.')
        return {'usage': used, 'total': total, 'duration': raw['config'].get('quota_duration')}

    def poll(self, identifier):
        for attempt in range(8):
            result = read_retry(self.http, f'{self.base}/{identifier}', params={'fields': 'status_code'}, headers=self.headers, sleep=self.sleep)
            status = result.get('status_code')
            if status == 'FINISHED': return status
            if status == 'PUBLISHED': return status
            if status in ('ERROR', 'EXPIRED'):
                raise ValueError('Instagram 컨테이너 처리 실패/만료. 공개 URL·규격·기존 게시 여부를 확인하세요.')
            if status != 'IN_PROGRESS':
                raise ValueError('Instagram 컨테이너 상태를 확인할 수 없습니다.')
            self.sleep(min(2 ** attempt, 30))
        raise Deferred('Instagram 미디어가 처리 중입니다. 같은 컨테이너로 나중에 재개합니다.')

    def publish(self, urls, target, journal):
        journal = Path(journal)
        identity = hashed({'urls': urls, 'target': target, 'account': self.account})
        state = read_json(journal) if journal.exists() else {'identity': identity, 'containers': {}, 'attempted': []}
        if state['identity'] != identity:
            raise ValueError('게시 문안/대상/URL이 바뀌었습니다. 기존 시도 기록으로 발행할 수 없습니다.')
        if state.get('result'):
            return state['result']
        if state.get('publishing'):
            status = self.poll(state['containers']['PARENT'])
            raise Uncertain(f'기존 컨테이너 상태 {status}. 발행 요청을 반복하지 않습니다. 게시 ID를 확인해 reconcile 하세요.')
        self.limit()
        plan = request_plan(urls, target, account=self.account, version=self.base.rsplit('/', 1)[1])
        def substitute(text):
            for name, identifier in state['containers'].items():
                text = text.replace('{' + name + '}', identifier)
            return text
        for step in plan['requests']:
            name = step.get('save_as')
            if name:
                if name in state['containers']:
                    continue
                if name in state['attempted']:
                    raise Uncertain('컨테이너 생성 결과 불명. 새 컨테이너 없이 계정 상태를 확인하세요.')
                state['attempted'].append(name); save_json(journal, state)
                try:
                    result = self.http.json('POST', step['url'], data={k: substitute(v) for k,v in step['data'].items()}, headers=self.headers)
                except RemoteError as error:
                    if error.status and error.status < 500:
                        # 명백한 오류 응답은 접수 불명이 아니다. 단, 재시도는 별도 실행에서 한다.
                        state['attempted'].remove(name); save_json(journal, state)
                        if error.status == 429 or error.subcode == 2207042:
                            raise Deferred('Instagram 한도/요청 제한으로 연기합니다.') from None
                        raise
                    raise Uncertain('컨테이너 생성 응답 유실. 새 요청 없이 확인하세요.') from None
                identifier = str(result.get('id', ''))
                if not identifier.isdigit():
                    raise Uncertain('유효한 컨테이너 ID를 받지 못했습니다. 새 요청 없이 확인하세요.')
                state['containers'][name] = identifier; save_json(journal, state)
            elif step['method'] == 'GET' and 'until' in step:
                if self.poll(substitute(step['url']).rsplit('/', 1)[1]) == 'PUBLISHED':
                    raise Uncertain('이미 발행된 컨테이너입니다. 기존 게시 ID를 확인하세요.')
            elif step['method'] == 'POST':
                self.limit()
                state['publishing'] = True; save_json(journal, state)
                try:
                    result = self.http.json('POST', step['url'], data={'creation_id': state['containers']['PARENT']}, headers=self.headers)
                except RemoteError:
                    raise Uncertain('발행 결과 불명. 기존 컨테이너 조회만 허용하며 자동 재게시하지 않습니다.') from None
                identifier = str(result.get('id', ''))
                if not identifier.isdigit():
                    raise Uncertain('발행 ID가 없습니다. 기존 컨테이너·계정 게시물을 확인하세요.')
                state['result'] = {'id': identifier, 'container_id': state['containers']['PARENT']}
                save_json(journal, state)
        return state['result']
