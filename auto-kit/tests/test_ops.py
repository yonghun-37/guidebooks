from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace
import pytest
from common import load_config, now, read_json, save_json
from state import Store, BudgetExceeded, Busy
from ops.tokens import instagram_token
from ops.notifications import notify, poll
from insights import collect
from providers.adapters import llm_request, Adapters
from pipeline import Pipeline

def test_token_refresh_redacted_and_24h(tmp_path):
    cfg = load_config(); path = tmp_path / 'token.json'; cfg['ops']['instagram_token_file'] = str(path)
    save_json(path, {'access_token': 'old-secret', 'issued_at': (now()-timedelta(days=55)).isoformat(), 'expires_at': (now()+timedelta(days=5)).isoformat()})
    class HTTP:
        def json(self, *a, **kw): return {'access_token': 'new-secret', 'expires_in': 5184000}
    assert instagram_token(cfg, refresh=True, http=HTTP())['access_token'] == 'new-secret'
    assert read_json(path)['access_token'] == 'new-secret'
    assert path.stat().st_mode & 0o777 == 0o600

def test_two_connections_cannot_overreserve(tmp_path):
    a, b = Store(tmp_path), Store(tmp_path)
    a.reserve('a','llm',.06,daily=.1,monthly=.1)
    with pytest.raises(BudgetExceeded): b.reserve('b','llm',.06,daily=.1,monthly=.1)
    with a.lock():
        with pytest.raises(Busy):
            with b.lock(): pass

def test_llm_request_shapes():
    cfg = load_config()
    for name, key in [('openai','text'),('gemini','generationConfig'),('anthropic','output_config')]:
        url, env, body = llm_request(name, cfg['models'][name], 'prompt', {'type':'object'}, 100)
        assert key in body and url.startswith('https://') and env.endswith('_API_KEY')

def test_analytics_missing_zero_and_youtube_dates(tmp_path):
    store = Store(tmp_path)
    run = {'id':'r', 'flow':'shorts', 'output':str(tmp_path), 'result':{'id':'vid'}, 'config':load_config()}
    class Response:
        status_code = 200
        def json(self): return {'columnHeaders':[{'name':'day'},{'name':'views'},{'name':'engagedViews'},{'name':'estimatedMinutesWatched'}], 'rows':[['2026-10-24',0,0,2.5]]}
    class Session:
        def request(self,*a,**kw): return Response()
    collect(store,run,live=True,session=Session(), start='2026-10-24',end='2026-10-26')
    text=(tmp_path/'insights.csv').read_text(encoding='utf-8-sig')
    assert '2026-10-24' in text and 'available' in text and '2.5,분' in text
    collect(store,run,live=False)
    assert 'missing' in (tmp_path/'insights.csv').read_text(encoding='utf-8-sig')

def test_telegram_allowed_user_and_replay(tmp_path):
    cfg=load_config(); p=Pipeline(cfg,tmp_path)
    run=p.run('insta')
    update={'update_id':10,'callback_query':{'id':'cb','from':{'id':7},'message':{'chat':{'id':8}},'data':f'a:{run["id"]}:{run["binding"][:12]}'}}
    class HTTP:
        def json(self, method, url, **kw): return {'result':[update]} if url.endswith('getUpdates') else {'ok':True}
    values={'TELEGRAM_BOT_TOKEN':'secret','TELEGRAM_ALLOWED_USER':'999','TELEGRAM_CHAT_ID':'8'}
    poll(p,http=HTTP(),values=values)
    assert not p.store.get(run['id']).get('approval')
    assert p.store.kv('telegram_offset')==11
    # 동일 update_id는 허용 사용자를 바꿔도 다시 처리하지 않는다.
    values['TELEGRAM_ALLOWED_USER']='7'
    poll(p,http=HTTP(),values=values)
    assert not p.store.get(run['id']).get('approval')
    update['update_id']=11
    poll(p,http=HTTP(),values=values)
    assert p.store.get(run['id'])['approval']['actor']=='telegram:7'

def test_notifications_attach_preview_and_hide_credentials(tmp_path):
    cfg=load_config(); p=Pipeline(cfg,tmp_path); run=p.run('insta')
    calls=[]
    class HTTP:
        def request(self,*a,**kw): calls.append(kw); return SimpleNamespace(status_code=204)
    notify(run,'승인 대기',live=True,http=HTTP(),values={'DISCORD_WEBHOOK_URL':'https://discord.com/api/webhooks/id/secret'})
    assert 'files' in calls[0]
    assert 'secret' not in (Path(run['output'])/'notification.json').read_text()

def test_dryrun_blocks_all_network_and_cost_queue(tmp_path, monkeypatch):
    cfg=load_config(); cfg['mode']='auto'
    p=Pipeline(cfg,tmp_path)
    def fail(*a,**k): raise BudgetExceeded('budget')
    monkeypatch.setattr(p.store,'reserve',fail)
    run=p.run('insta')
    assert run['status']=='exception' and not run['gates']['cost']['passed']
    assert read_json(Path(run['output'])/'notification.json')['event']=='비용 중단'
