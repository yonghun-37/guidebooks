"""공통 draft/media/check 인터페이스, 스키마 검증, 호출별 비용 장부."""
import json
from pathlib import Path
import math
from jsonschema import Draft202012Validator, ValidationError
from common import ROOT, read_json, canonical, hashed, save_json, digest
from transport import RemoteError
from .adapters import Adapters

SCHEMA = read_json(ROOT / 'providers/content.schema.json')
CHECK_SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['passed', 'reason'], 'properties': {'passed': {'type': 'boolean'}, 'reason': {'type': 'string'}}}

class Provider:
    def __init__(self, config, store, run_id, *, mock=False, invoke=None, adapters=None):
        self.config, self.store, self.run_id = config, store, run_id
        self.mock, self.invoke, self.adapters = mock, invoke, adapters or Adapters()
        self.prices = read_json(ROOT / 'providers/prices.json')

    @staticmethod
    def mock_draft(source, flow):
        # 동봉 원문은 첫 줄이 훅, 다음 줄이 '항목: 설명'이다. 새 사실을 덧붙이지 않는다.
        lines = [line.strip() for line in source['text'].splitlines() if line.strip()]
        title = source['title'][:40]
        scenes = [{'title': title, 'text': lines[0][:150], 'duration': 3 if flow == 'insta' else 6}]
        for line in lines[1:5]:
            heading, separator, body = line.partition(':')
            scenes.append({'title': heading[:40] if separator else title,
                           'text': (body.strip() if separator else line)[:150],
                           'duration': 3 if flow == 'insta' else 7.5})
        if len(scenes) == 1:
            scenes.append({'title': '원문에서 다시 확인', 'text': lines[0][:150], 'duration': 3})
        text = '\n'.join(lines)
        return {'title': title, 'caption': text[:2000], 'narration': text[:4000],
                'entities': source.get('entities', []), 'scenes': scenes}

    def reserve_run(self, source, flow):
        """장면 최대 5개·대본 최대 4000자·모든 재시도를 포함한 실행 견적."""
        existing=self.store.db.execute("SELECT id,reserved FROM calls WHERE run_id=? AND kind='run:maximum'",(self.run_id,)).fetchone()
        if existing:return {'ticket':existing['id'],'maximum_usd':existing['reserved']/1e6,'includes_retries':True}
        if self.mock: maximum=0
        else:
            cfg=self.config;attempts=cfg['budget']['max_attempts'];tokens=cfg['budget']['max_output_tokens']
            name=cfg['providers']['llm'];model=cfg['models'].get(name)
            rate=self.prices['llm'][model]
            input_max=len((canonical({'source':source,'flow':flow})+canonical(SCHEMA)).encode())+3000
            maximum=attempts*(input_max*rate['input_million']+tokens*rate['output_million'])/1e6
            if cfg['providers']['llm_check']:
                model=cfg['models'].get('check_llm',model);rate=self.prices['llm'][model]
                maximum+=attempts*((input_max+30000)*rate['input_million']+tokens*rate['output_million'])/1e6
            if cfg['media']['image_api'] or cfg['media']['video_api']:
                maximum+=0 if cfg['providers']['image']=='mock' else 5*.1
            if cfg['media']['video_api']:
                maximum+=0 if cfg['providers']['video']=='mock' else 5*5*self.prices['video'][cfg['models']['video']]['second_usd']
            if (flow=='shorts' or cfg['media']['motion_reel'] or cfg['instagram']['format']=='reel') and not cfg['media']['recording']:
                maximum+=0 if cfg['providers']['tts']=='mock' else 4000*self.prices['tts'][cfg['models']['tts']]['character_million']/1e6
        ticket=self.store.reserve(self.run_id,'run:maximum',maximum,daily=self.config['budget']['daily_usd'],monthly=self.config['budget']['monthly_usd'])
        return {'ticket':ticket,'maximum_usd':maximum,'includes_retries':True}

    def _call(self, kind, payload, schema=None):
        group = 'llm' if kind in ('llm', 'check') else kind
        provider = 'mock' if self.mock else self.config['providers'][group]
        model = self.config['models'].get(provider) if group == 'llm' else self.config['models'][group]
        if kind == 'check' and provider != 'mock':
            provider = self.config['providers'].get('check_llm', provider)
            model = self.config['models'].get('check_llm', self.config['models'].get(provider))
        max_tokens = self.config['budget']['max_output_tokens']
        if provider == 'mock':
            rate, estimate = {}, 0
        else:
            rate = self.prices[group].get(model)
            if not rate:
                raise ValueError('모델 가격표가 없습니다. 조사 날짜·단가를 설정한 뒤 호출하세요.')
            # UTF-8 bytes는 토큰 수보다 보수적인 입력 상한. 지시문 여유 포함.
            input_max = len((canonical(payload) + canonical(schema)).encode()) + 3000
            if group == 'llm':
                estimate = (input_max * rate['input_million'] + max_tokens * rate['output_million']) / 1e6
            elif group == 'tts':
                estimate = len(payload['text']) * rate['character_million'] / 1e6
            elif group == 'image':
                estimate = max(.1, rate['unit_usd'] + input_max * rate['input_million'] / 1e6)
            else:
                estimate = payload['seconds'] * rate['second_usd']
        attempts = self.config['budget']['max_attempts'] if group == 'llm' else 1
        for attempt in range(attempts):
            cost_path=Path(payload['path']).with_suffix('.cost.json') if group=='video' else None
            identity=hashed({'kind':kind,'model':model,'text':payload.get('text'),'seconds':payload.get('seconds'),'image':digest(payload['image']) if payload.get('image') else None})
            if cost_path and cost_path.exists():
                record=read_json(cost_path)
                if record['identity']!=identity:raise ValueError('영상 생성 비용/작업 대상이 바뀌었습니다.')
                ticket=record['ticket']
            else:
                ticket = self.store.reserve(self.run_id, kind + ':' + provider, estimate, daily=self.config['budget']['daily_usd'], monthly=self.config['budget']['monthly_usd'])
                if cost_path:save_json(cost_path,{'identity':identity,'ticket':ticket})
            try:
                if provider == 'mock':
                    result = {'value': ({'passed': True, 'reason': 'mock 원문 대조'} if kind == 'check' else self.mock_draft(payload['source'], payload['flow'])), 'usage': {'mock': True}}
                elif self.invoke:
                    result = self.invoke(kind, payload, model)
                elif group == 'llm':
                    result = self.adapters.llm(provider, model, payload, schema, max_tokens)
                else:
                    result = self.adapters.media(kind, model, payload)
            except RemoteError as error:
                # 실패/응답 유실도 과금됐을 수 있다. 예약을 환불하지 않는다.
                if error.status not in (0, 429, 500, 502, 503, 504) or attempt + 1 == attempts:
                    raise
                self.adapters.sleep(2 ** attempt)
                continue
            usage = result.get('usage')
            if provider == 'mock':
                actual = 0
            elif not usage or usage.get('billing_unknown'):
                actual = estimate
            elif group == 'llm' and (not all(k in usage and type(usage[k]) is int and usage[k] >= 0 for k in ('input_tokens', 'output_tokens'))):
                actual = estimate
            elif group == 'llm':
                actual = (usage.get('input_tokens', 0) * rate['input_million'] + usage.get('output_tokens', 0) * rate['output_million']) / 1e6
            elif group == 'tts':
                actual = usage['characters'] * rate['character_million'] / 1e6
            elif group == 'video':
                actual = usage['seconds'] * rate['second_usd']
            else:
                actual = estimate
            self.store.settle(ticket, actual, usage or {'missing_usage': True})
            value = result['value']
            if schema:
                try:
                    Draft202012Validator(schema).validate(value)
                except ValidationError:
                    if attempt + 1 == attempts:
                        raise ValueError('JSON 스키마 검증 실패. 재시도 예산을 소진했습니다.') from None
                    continue
            return value
        raise ValueError('공급자 재시도 횟수를 확인하세요.')

    def draft(self, source, flow):
        if len(source['text']) > self.config['budget']['max_source_chars']:
            raise ValueError('원문 길이 상한을 넘었습니다. 소스를 줄이세요.')
        return self._call('llm', {'source': source, 'flow': flow}, SCHEMA)

    def check(self, source, draft):
        return self._call('check', {'mode': 'check', 'source': source, 'draft': draft}, CHECK_SCHEMA)

    def media(self, kind, text, path, **kwargs):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if self.mock or self.config['providers'][kind] == 'mock':
            ticket = self.store.reserve(self.run_id, kind + ':mock', 0, daily=self.config['budget']['daily_usd'], monthly=self.config['budget']['monthly_usd'])
            if kind == 'image':
                from PIL import Image, ImageDraw
                im = Image.new('RGB', (720, 1280), '#173b42')
                ImageDraw.Draw(im).ellipse((100, 200, 650, 750), fill='#d4a95d')
                im.save(path)
            elif kind == 'tts':
                # 가상 연습 음성: 말이 아닌 사인파. 실제 TTS 품질을 주장하지 않는다.
                import wave, struct
                with wave.open(str(path), 'wb') as f:
                    f.setnchannels(1); f.setsampwidth(2); f.setframerate(24000)
                    f.writeframes(b''.join(struct.pack('<h', int(3000 * math.sin(2 * math.pi * 220 * n / 24000))) for n in range(round(24000 * kwargs.get('seconds', 6)))))
            else:
                from rendering.media import ffmpeg
                ffmpeg(['-loop', '1', '-i', kwargs['image'], '-t', str(kwargs.get('seconds', 5)), '-vf', 'scale=720:1280', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-threads', '2', str(path)])
            self.store.settle(ticket, 0, {'mock': True})
            return str(path)
        return self._call(kind, {'text': text, 'path': str(path), **kwargs})
