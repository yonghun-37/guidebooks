"""live 조립 경로도 인증·호스팅·게시·분석 경계를 모두 대체한다."""
from pathlib import Path
from types import SimpleNamespace
import pytest
import pipeline as module
from pipeline import Pipeline
from common import load_config, hashed, now
from providers import Provider

@pytest.mark.parametrize('flow',['insta','shorts'])
def test_live_orchestration_all_external_mocked(tmp_path,monkeypatch,flow):
    cfg=load_config();cfg['mode']='auto';cfg['providers']['llm']='openai';cfg['budget']['provider_hard_cap_confirmed']=True
    cfg['instagram']['account']='123';cfg['youtube']['quota_confirmed_at']=now().isoformat()
    p=Pipeline(cfg,tmp_path)
    source={'title':'책 이야기','text':'책을 함께 읽어요.','entities':[],'rights_reviewed':True,'synthetic':False,'url':'https://example.org/source','source_hash':hashed('책을 함께 읽어요.')}
    p.select=lambda *a,**kw:source
    monkeypatch.setattr(Provider,'draft',lambda *a:Provider.mock_draft(source,flow))
    monkeypatch.setattr(module,'host',lambda *a,**kw:{'adapter':'r2','urls':['https://example.org/a.jpg','https://example.org/b.jpg']})
    monkeypatch.setattr(module,'collect',lambda *a,**kw:{'mocked':True})
    calls=[]
    class Session:
        def request(self,method,url,**kw):
            calls.append((method,url,kw))
            if '/channels' in url:return SimpleNamespace(status_code=200,json=lambda:{'items':[{'id':'channelA'}]})
            if method=='POST':return SimpleNamespace(status_code=200,headers={'Location':'https://www.googleapis.com/upload/youtube/v3/videos?upload_id=fake'})
            return SimpleNamespace(status_code=201,headers={},json=lambda:{'id':'video123'})
    p._credentials=lambda *a:'AUTH_SENTINEL_DO_NOT_PERSIST_123' if flow=='insta' else Session()
    class H:
        def json(self,method,url,**kw):
            calls.append((method,url,kw))
            if 'content_publishing_limit' in url:return {'data':[{'quota_usage':0,'config':{'quota_total':10}}]}
            if method=='GET':return {'status_code':'FINISHED'}
            return {'id':str(len(calls))}
    monkeypatch.setattr(module,'HTTP',H)
    monkeypatch.setattr(p,'_notice',lambda *a:None)
    if flow=='shorts':
        # 사용자 녹음 경로를 로컬 신호음으로 대체. 어떤 TTS API도 호출하지 않는다.
        recording=tmp_path/'recording.wav'
        Provider(cfg,p.store,'fixture',mock=True).media('tts','음성',recording)
        p.config['media']['recording']=str(recording)
    result=p.run(flow,live=True)
    assert result['status']=='done',result.get('reason')
    assert 'publish' in result['steps'] and calls
    assert 'AUTH_SENTINEL_DO_NOT_PERSIST_123' not in (Path(result['output'])/'run.json').read_text()
