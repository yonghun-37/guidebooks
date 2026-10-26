"""단계별 상태·재개·승인·게시. 기본은 키 없는 드라이런."""
import argparse
import copy
from datetime import timedelta
from pathlib import Path
import uuid
from common import ROOT, cli, load_config, kit_path, save_json, read_json, now, local_now, timestamp, hashed, secrets
from state import Store, BudgetExceeded
from providers import Provider
from topics import select_topic
from rendering.media import render
from gates import inspect_text, inspect_media, content_text, verdict
from approve import binding, approve as record_approval, require_approval
from hosting import host
from transport import HTTP, Deferred, Uncertain, RemoteError
from publish import instagram, youtube
from ops.tokens import instagram_token, google_session
from ops.notifications import notify
from ops.report import report
from insights import collect

class Pipeline:
    def __init__(self, config=None, state=None):
        self.config = copy.deepcopy(config or load_config())
        self.store = Store(state or ROOT / 'private/state')
        self.render, self.select = render, select_topic

    def _credentials(self, config, flow):
        try:
            if flow == 'insta':
                token = instagram_token(config, refresh=True)
                return token['access_token']
            session = google_session(config)
            path=kit_path(config['ops']['google_token_file'])
            granted=read_json(path).get('granted_at')
            if secrets().get('GOOGLE_OAUTH_MODE','testing')=='testing' and (not granted or (now()-timestamp(granted)).days>=6):
                self._ops_notice(flow,'OAuth Testing 7일 만료 확인·Production 요건 확인 후 재동의',config)
            return session
        except ValueError:
            self._ops_notice(flow,'토큰 만료/인증 실패·doctor와 본인 계정 재인증 확인',config)
            raise

    def _ops_notice(self, flow, event, config):
        key='ops_notice:'+(flow or 'all')+':'+('일일 보고' if event.startswith('일일 보고') else event)+':'+local_now().date().isoformat()
        if self.store.kv(key):return
        output=self.store.root/'ops';output.mkdir(exist_ok=True)
        try:
            notify({'id':'ops','flow':flow,'status':'운영 점검','output':str(output),'files':[]},event,live=True)
            self.store.kv(key,True)
        except (ValueError,OSError):self.store.event('ops','notification','delivery_failed')

    def run(self, flow, provider=None, live=False):
        if flow not in ('insta', 'shorts'):
            raise ValueError('flow는 insta 또는 shorts여야 합니다.')
        config = copy.deepcopy(self.config)
        if provider:
            if provider == 'mock':
                config['providers'] = {**config['providers'], 'llm': 'mock', 'tts': 'mock', 'image': 'mock', 'video': 'mock'}
            else:
                config['providers']['llm'] = provider
        if live:
            if config['providers']['llm'] == 'mock':
                raise ValueError('mock 콘텐츠는 --live로 게시하지 않습니다. 사용자 원문·실제 공급자를 설정하세요.')
            if not config['budget']['provider_hard_cap_confirmed']:
                raise ValueError('공급자 강제 지출 상한을 직접 확인하고 provider_hard_cap_confirmed=true로 설정하세요.')
            if flow == 'shorts' and not config['media']['recording'] and config['providers']['tts'] == 'mock':
                raise ValueError('live 쇼츠에는 본인 녹음 또는 실제 TTS 공급자가 필요합니다.')
            if (config['media']['image_api'] and config['providers']['image'] == 'mock') or (config['media']['video_api'] and config['providers']['video'] == 'mock'):
                raise ValueError('live 생성 미디어에는 실제 공급자를 설정하세요.')
            credentials = self._credentials(config, flow)
        elif config['providers']['llm'] != 'mock':
            raise ValueError('기본 드라이런은 mock만 호출합니다. 실제 생성은 사용자 키와 --live가 필요합니다.')
        identifier = uuid.uuid4().hex[:12]
        output = self.store.root / identifier
        output.mkdir(mode=0o700)
        target = copy.deepcopy(config['instagram' if flow == 'insta' else 'youtube'])
        if live and flow == 'shorts':
            actual_channel = youtube.channel_id(credentials)
            if target['account'] not in ('MINE', actual_channel):
                raise ValueError('설정한 YouTube 채널과 현재 OAuth 채널이 다릅니다.')
            target['account'] = actual_channel
        if live and flow == 'insta' and not str(target['account']).isdigit():
            target['account'] = secrets().get('IG_USER_ID', '')
            if not target['account'].isdigit():
                raise ValueError('Instagram 숫자 account 또는 .env의 IG_USER_ID가 필요합니다.')
        run = {'id': identifier, 'flow': flow, 'live': live, 'status': 'running', 'config': config, 'target': target, 'steps': [], 'output': str(output), 'created_at': now().isoformat(), 'files': []}
        if config['mode'] == 'post_review':
            publish_at = (now() + timedelta(hours=config['review']['hours'])).isoformat()
            if config['review']['hours'] <= 0:
                raise ValueError('사후 확인 시간은 0보다 커야 합니다.')
            if flow == 'shorts':
                target['privacyStatus'], target['publishAt'] = 'private', publish_at
            run['publish_at'] = publish_at
        elif flow == 'shorts' and target.get('publishAt'):
            run['publish_at'] = target['publishAt']
        save_json(output / 'config.json', config)
        self.store.save(run)
        return self.resume(identifier, live=live)

    def _save(self, run, step=None):
        if step and step not in run['steps']:
            run['steps'].append(step)
            self.store.event(run['id'], step, 'done')
        self.store.save(run)
        save_json(Path(run['output']) / 'run.json', run)

    def _notice(self, run, event):
        # 알림 실패가 이미 성공한 게시를 실패로 뒤집지 않게 한다.
        try:
            notify(run, event, live=run['live'])
        except (ValueError, OSError):
            self.store.event(run['id'], 'notification', 'delivery_failed')

    def resume(self, identifier, live=False):
        with self.store.lock():
            run = self.store.get(identifier)
            if live != run['live']:
                raise ValueError('드라이런과 live 실행을 서로 전환할 수 없습니다. 별도 실행으로 생성·검수하세요.')
            if run['status'] in ('done', 'dry_run', 'rejected'):
                return run
            if run.get('defer_until') and timestamp(run['defer_until']) > now():
                return run
            if run['status'] == 'exception':
                return run  # 관문 실패는 approve로 우회할 수 없다. 수정 후 새 실행.
            cfg = run['config']; output = Path(run['output'])
            provider = Provider(cfg, self.store, run['id'], mock=not live)
            step = 'topic'
            try:
                if 'topic' not in run['steps']:
                    run['source'] = self.select(cfg, self.store, run['flow'], live=live)
                    run['source_hash'] = run['source']['source_hash']
                    if live and (run['source'].get('synthetic', False) or not run['source'].get('rights_reviewed')):
                        raise ValueError('가상 소스 또는 권리 미확인 소스는 live 생성·게시할 수 없습니다.')
                    save_json(output / 'source.json', run['source']); self._save(run, step)
                step = 'budget'
                if step not in run['steps']:
                    run['budget_reservation']=provider.reserve_run(run['source'],run['flow']);self._save(run,step)
                step = 'draft'
                if step not in run['steps']:
                    run['draft'] = provider.draft(run['source'], run['flow'])
                    target = run['target']; target['caption'] = run['draft']['caption'] + ('\n원문: ' + run['source']['url'] if run['source'].get('url') else '')
                    # YouTube metadata도 원문 링크가 포함된 문안을 사용한다.
                    save_json(output / 'draft.json', run['draft']); self._save(run, step)
                step = 'render'
                if step not in run['steps']:
                    run['files'] = list(map(str, self.render(run['draft'], cfg, output, run['flow'], provider)))
                    self._save(run, step)
                step = 'host'
                if step not in run['steps']:
                    run['hosting'] = host(run['files'], cfg, run['id'], output, live=live) if run['flow'] == 'insta' else {'adapter': 'not-required', 'urls': []}
                    self._save(run, step)
                step = 'gates'
                if step not in run['steps']:
                    recent = [content_text(r['draft']) for r in self.store.runs() if r['id'] != run['id'] and r['flow'] == run['flow'] and r['status'] in ('done','dry_run','scheduled','uncertain') and 'draft' in r][:cfg['gates']['recent_posts']]
                    run['gates'] = inspect_text(run['draft'], run['source'], recent, cfg['gates'])
                    run['gates'].update(inspect_media(run['files'], run['flow'], cfg['gates'], run['target']))
                    if cfg['providers']['llm_check']:
                        check = provider.check(run['source'], run['draft'])
                        run['gates']['llm_check'] = verdict([] if check['passed'] else [check['reason']])
                    self.store.finish_budget(run['id'])
                    spend = self.store.spend()
                    run['gates']['cost'] = verdict(['비용 상한 도달'] if spend['day'] >= cfg['budget']['daily_usd'] or spend['month'] >= cfg['budget']['monthly_usd'] else [], **spend)
                    run['generation_cost'] = sum((c['actual'] if c['actual'] is not None else c['reserved']) / 1e6 for c in self.store.calls() if c['run_id'] == run['id'])
                    run['gate_passed'] = all(r['passed'] for r in run['gates'].values())
                    save_json(output / 'gates.json', run['gates'])
                    run['binding'] = binding(run)
                    self._save(run, step)
                if not run['gate_passed']:
                    run['status'] = 'exception'; self._save(run); self._notice(run, '품질 관문 예외'); return run
                step = 'review'
                if binding(run) != run['binding']:
                    raise ValueError('관문 이후 파일·문안·대상이 바뀌었습니다. 새 실행으로 검수하세요.')
                if cfg['mode'] == 'approval' and not run.get('approval'):
                    run['status'] = 'waiting_approval'; self._save(run); self._notice(run, '승인 대기'); return run
                if 'publish' not in run['steps']:
                    if run.get('approval') and timestamp(run['approval']['expires_at']) <= now():
                        run.pop('approval'); run['status'] = 'waiting_approval'; self._save(run); self._notice(run, '승인 만료·재승인 대기'); return run
                    require_approval(run)
                if cfg['mode'] == 'post_review' and run['flow'] == 'insta' and timestamp(run['publish_at']) > now():
                    run['status'] = 'scheduled'; self._save(run); self._notice(run, '공개 전 거부 가능'); return run
                step = 'publish'
                if step not in run['steps']:
                    # 텍스트 해시를 사용하므로 배경만 바꿔 같은 문안을 다시 올릴 수 없다.
                    run['content_hash'] = hashed(content_text(run['draft']))
                    try:
                        self.store.claim(run, run['content_hash'])
                    except ValueError:
                        run['status'] = 'exception'; run['gates']['duplicate'] = verdict(['같은 콘텐츠의 게시 시도 기록이 있습니다.']); self._save(run); return run
                    self._save(run)
                    if run['flow'] == 'insta':
                        plan = instagram.request_plan(run['hosting']['urls'], run['target'], account=run['target']['account'], version=cfg['instagram']['api_version'])
                    else:
                        body = youtube.metadata({**run['draft'], 'caption': run['target']['caption']}, run['target'], resuming=(output / 'upload-session.json').exists())
                        plan = youtube.request_plan(run['files'][0], body)
                    save_json(output / 'request-plan.json', plan)
                    if live:
                        credentials = self._credentials(cfg, run['flow'])
                        if run['flow'] == 'insta':
                            api = instagram.Instagram(HTTP(), token=credentials, account=run['target']['account'], version=cfg['instagram']['api_version'], safety_limit=cfg['instagram']['safety_daily_posts'])
                            run['quota'] = api.limit()
                            self._save(run)
                            run['result'] = api.publish(run['hosting']['urls'], run['target'], output / 'instagram-journal.json')
                        else:
                            if youtube.channel_id(credentials) != run['target']['account']:
                                raise ValueError('승인한 YouTube 채널과 현재 OAuth 채널이 다릅니다. 업로드하지 않았습니다.')
                            # Cloud Console 할당량은 공개 API로 조회되지 않는다. 확인한 로컬 cap과 API 거절을 함께 사용.
                            quota_config=run.get('quota_override',cfg['youtube'])
                            confirmed = quota_config.get('quota_confirmed_at')
                            if not confirmed or (now() - timestamp(confirmed)).days > 30:
                                raise Deferred('YouTube Cloud Console의 업로드 버킷을 확인하고 quota_confirmed_at을 기록하세요.')
                            from zoneinfo import ZoneInfo
                            day = now().astimezone(ZoneInfo('America/Los_Angeles')).date().isoformat()
                            key = 'youtube_insert:' + day
                            used = self.store.kv(key) or 0
                            existing = (output / 'upload-session.json').exists()
                            if not existing:
                                if used >= quota_config['quota_daily_insert']:
                                    raise Deferred('키트 YouTube 일일 업로드 상한에 도달했습니다.')
                                self.store.kv(key, used + 1)
                            run['quota'] = {'local_usage': used + int(not existing), 'local_limit': quota_config['quota_daily_insert'], 'period_day':day, 'timezone':'America/Los_Angeles', 'verified': confirmed}
                            self._save(run)
                            run['result'] = youtube.publish(output, body, credentials)
                    else:
                        run['result'] = {'id': 'dry-' + run['id'], 'mode': 'dry-run'}
                    self._save(run, step)
                step = 'insights'
                if step not in run['steps']:
                    # 방금 게시한 지표가 미준비여도 게시 성공 기록을 보존한다.
                    try:
                        run['insights'] = collect(self.store, run, live=live)
                    except (ValueError, OSError):
                        run['insights'] = {'pending': True, 'note': '분석 권한·준비 날짜 확인 후 insights.py로 재조회'}
                    self._save(run, step)
                run['status'] = 'scheduled' if run.get('publish_at') and timestamp(run['publish_at']) > now() else ('done' if live else 'dry_run')
                run.pop('defer_until', None); self._save(run); self._notice(run, '실행 보고')
            except BudgetExceeded:
                run['status'] = 'exception'; run.setdefault('gates', {})['cost'] = verdict(['일/월 비용 상한. 추가 호출을 중단했습니다.']); self._save(run); self._notice(run, '비용 중단')
            except Deferred as error:
                run['status'] = 'deferred'; run['defer_until'] = (now() + timedelta(minutes=cfg['ops']['defer_minutes'])).isoformat(); run['reason'] = str(error); self._save(run); self._notice(run, '자동 연기')
            except Uncertain as error:
                run['status'] = 'uncertain'; run['reason'] = str(error); self._save(run); self._notice(run, '게시 결과 확인 필요')
            except (ValueError, OSError) as error:
                run['status'] = 'exception' if step == 'review' else 'failed'
                run['failed_step'] = step
                run['reason'] = str(error) if isinstance(error, ValueError) else '파일 처리 실패. 경로·권한을 확인하세요.'
                self.store.event(run['id'], step, run['status']); self._save(run); self._notice(run, '단계 중단')
            except Exception:
                run['status'] = 'failed'; run['failed_step'] = step; run['reason'] = '단계 응답/파일 형식 오류. 인증 값 보호를 위해 예외 전문은 기록하지 않습니다.'
                self.store.event(run['id'], step, 'failed'); self._save(run); self._notice(run, '단계 중단')
            finally:
                report(self.store, cfg)
            return run

    def approve(self, identifier, actor='local'):
        with self.store.lock():
            run = self.store.get(identifier)
            record_approval(run, actor)
            self._save(run)
            return run

    def reject(self, identifier):
        with self.store.lock():
            run = self.store.get(identifier)
            if run['status'] == 'rejected': return run
            if run['status'] not in ('waiting_approval', 'scheduled', 'deferred', 'failed', 'exception'):
                raise ValueError('현재 상태에서는 거부할 수 없습니다. 기존 게시 여부를 확인하세요.')
            if run.get('publish_at') and timestamp(run['publish_at']) <= now():
                raise ValueError('예약 시각이 지났습니다. 공개 상태를 먼저 확인하세요.')
            if 'publish' in run['steps']:
                if run['flow'] != 'shorts' or not run.get('publish_at'):
                    raise ValueError('이미 게시된 실행은 로컬 거부로 취소할 수 없습니다.')
                if run['live']:
                    credentials = self._credentials(run['config'], 'shorts')
                    if youtube.channel_id(credentials) != run['target']['account']:
                        raise ValueError('승인한 채널과 현재 OAuth 채널이 달라 예약 취소를 중단했습니다.')
                    youtube.cancel(run['result']['id'], credentials)
            run['status'] = 'rejected'; self._save(run); self._notice(run, '거부 완료')
            self.store.finish_budget(run['id'])
            report(self.store, run['config'])
            return run

    def reconcile(self, identifier, media_id):
        """결과 불명 Instagram에 사용자가 확인한 ID를 조회·결합한다. 새 발행 없음."""
        with self.store.lock():
            run = self.store.get(identifier)
            if run['flow'] != 'insta' or run['status'] != 'uncertain' or not run['live'] or not media_id.isdigit():
                raise ValueError('결과 불명 Instagram live 실행과 기존 게시 ID가 필요합니다.')
            token = self._credentials(run['config'], 'insta')
            cfg = run['config']['instagram']; base = f"https://graph.instagram.com/{cfg['api_version']}"
            api = HTTP(); headers = {'Authorization': 'Bearer ' + token}
            existing = api.json('GET', base + '/' + run['target']['account'] + '/media', params={'fields': 'id,caption', 'limit': 100}, headers=headers)
            matches = [m for m in existing.get('data', []) if m.get('id') == media_id and m.get('caption') == run['target']['caption']]
            if len(matches) != 1:
                raise ValueError('현재 계정의 최근 게시물 ID·문안이 일치하지 않습니다. 새 발행 없이 확인하세요.')
            run['result'] = {'id': media_id, 'reconciled': True}; self._save(run, 'publish'); run['status'] = 'running'; self._save(run)
        return self.resume(identifier, live=True)

    def refresh_ops(self, identifier):
        """발행 내용·승인은 그대로 두고 Console에서 재확인한 quota 기록만 갱신."""
        with self.store.lock():
            run=self.store.get(identifier)
            if run['flow']!='shorts' or 'publish' in run['steps']:
                raise ValueError('업로드 전 쇼츠 실행의 할당량 기록만 갱신할 수 있습니다.')
            quota=self.config['youtube'];confirmed=timestamp(quota.get('quota_confirmed_at'))
            if not 0 <= (now()-confirmed).total_seconds() < 30*86400 or type(quota['quota_daily_insert']) is not int or quota['quota_daily_insert']<=0:
                raise ValueError('최근 30일 이내 Console 확인 시각과 양수 일일 insert cap을 설정하세요.')
            run['quota_override']={key:quota[key] for key in ('quota_confirmed_at','quota_daily_insert')}
            run.pop('defer_until',None);self._save(run)
            return run

    def tick(self, *, flow=None, provider=None, live=False, daily_at=None):
        import re
        if daily_at and not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', daily_at):
            raise ValueError('--daily-at은 HH:MM 형식이어야 합니다.')
        results = []
        local_day = local_now().date().isoformat()
        for run in self.store.runs():
            if run['live'] != live or (flow and run['flow'] != flow): continue
            # 지표 지연을 고려해 완료 후에도 최근 게시물을 매일 다시 수집한다.
            if live and 'publish' in run['steps'] and run['status'] in ('done','scheduled') and (now()-timestamp(run['created_at'])).days <= run['config']['ops'].get('analytics_lookback_days',7):
                key = f'insights:{local_day}:{run["id"]}'
                if not self.store.kv(key):
                    try:
                        # UTC 자정 경계의 플랫폼 보고일 누락을 막기 위해 시작일에 하루 여유.
                        start_day=(timestamp(run['created_at'])-timedelta(days=1)).date().isoformat()
                        run['insights'] = collect(self.store,run,live=True,start=start_day,end=now().date().isoformat())
                        self._save(run); self.store.kv(key,True)
                    except (ValueError,OSError):
                        self.store.event(run['id'],'insights','pending')
            if run['status'] in ('running','deferred','failed','scheduled') or (run['status'] == 'waiting_approval' and run.get('approval')):
                results.append(self.resume(run['id'], live=live))
        ready = not daily_at or local_now().strftime('%H:%M') >= daily_at
        if flow and ready:
            key = f'daily:{local_day}:{flow}:{live}'
            acquired = self.store.db.execute('INSERT OR IGNORE INTO kv VALUES(?,?)',(key,'"starting"')).rowcount
            if acquired:
                result = self.run(flow, provider=provider, live=live)
                self.store.kv(key, result['id']); results.append(result)
        summary=report(self.store, self.config)
        if live:
            self._ops_notice(flow or 'all',f"일일 보고 · 실행 {summary['runs']}개 · 예외 {len(summary['exceptions'])}개 · 당일 생성비 ${summary['spend']['day']:.6f}",self.config)
        return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('run','resume','approve','reject','status','tick','report','telegram','reconcile','refresh-ops'):
        p = sub.add_parser(name)
        p.add_argument('--state', default='private/state'); p.add_argument('--config'); p.add_argument('--live', action='store_true')
        if name in ('run','tick'): p.add_argument('--flow', choices=['insta','shorts'], required=name == 'run'); p.add_argument('--provider', choices=['mock','openai','gemini','anthropic']); p.add_argument('--mode', choices=['auto','post_review','approval'])
        if name == 'tick': p.add_argument('--daily-at', help='OS 현지 HH:MM 이후에만 하루 새 생성. 재개는 항상 실행')
        if name in ('resume','approve','reject','reconcile','refresh-ops'): p.add_argument('id')
        if name == 'reconcile': p.add_argument('--media-id', required=True)
    args = parser.parse_args()
    config = load_config(kit_path(args.config) if args.config else None)
    if getattr(args, 'mode', None): config['mode'] = args.mode
    pipeline = Pipeline(config, kit_path(args.state))
    if args.command == 'run': result = pipeline.run(args.flow, args.provider, args.live)
    elif args.command == 'resume': result = pipeline.resume(args.id, args.live)
    elif args.command == 'approve': result = pipeline.approve(args.id)
    elif args.command == 'reject':
        run = pipeline.store.get(args.id)
        if run['live'] and 'publish' in run['steps'] and not args.live:
            raise ValueError('실제 예약 영상 취소에는 reject ID --live를 사용하세요.')
        result = pipeline.reject(args.id)
    elif args.command == 'reconcile':
        if not args.live: raise ValueError('기존 ID 조회에는 --live를 명시하세요.')
        result = pipeline.reconcile(args.id, args.media_id)
    elif args.command == 'refresh-ops': result = pipeline.refresh_ops(args.id)
    elif args.command == 'tick': result = pipeline.tick(flow=args.flow, provider=args.provider, live=args.live, daily_at=args.daily_at)
    elif args.command == 'report': result = report(pipeline.store, config)
    elif args.command == 'telegram':
        if not args.live: raise ValueError('Telegram polling은 --live를 명시하세요.')
        from ops.notifications import poll
        result = poll(pipeline)
    else:
        result = [{'id': r['id'], 'flow': r['flow'], 'status': r['status'], 'reason': r.get('reason')} for r in pipeline.store.runs()]
    import json
    if isinstance(result, dict) and 'status' in result:
        print(f"{result['id']} · {result['flow']} · {result['status']}")
        if result.get('reason'): print(result['reason'])
        print('미리보기: ' + result['output'] + '/preview.html')
        if result['status'] in ('failed','exception','uncertain'): raise SystemExit(2)
    else:
        print(json.dumps(result if not isinstance(result, list) else [{k: r[k] for k in ('id','flow','status','reason') if k in r} for r in result], ensure_ascii=False, indent=2))

if __name__ == '__main__': cli(main)
