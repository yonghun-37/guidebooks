import base64
import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from common import load_config, read_json, now
from providers import Provider, SCHEMA
from providers.adapters import Adapters
from state import Store, BudgetExceeded
from transport import HTTP, RemoteError, Deferred, Uncertain
from publish.youtube import publish, resumable
from publish.instagram import Instagram

@pytest.mark.parametrize('provider',['openai','gemini','anthropic'])
def test_actual_llm_adapter_payload_and_usage(provider):
    draft=Provider.mock_draft({'title':'책','text':'책을 읽어요.','entities':[]},'insta')
    answer=json.dumps(draft,ensure_ascii=False)
    bodies={
      'openai':{'output':[{'content':[{'type':'output_text','text':answer}]}],'usage':{'input_tokens':3,'output_tokens':4}},
      'gemini':{'candidates':[{'content':{'parts':[{'text':answer}]}}],'usageMetadata':{'promptTokenCount':3,'candidatesTokenCount':4,'thoughtsTokenCount':2,'totalTokenCount':9}},
      'anthropic':{'content':[{'type':'text','text':answer}],'usage':{'input_tokens':3,'output_tokens':4}}}
    calls=[]
    class H:
        def json(self,*args,**kw):calls.append((args,kw));return bodies[provider]
    values={name:'hidden' for name in ['OPENAI_API_KEY','GEMINI_API_KEY','ANTHROPIC_API_KEY']}
    result=Adapters(H(),values).llm(provider,load_config()['models'][provider],{'source':{'text':'원문'}},SCHEMA,100)
    assert result['value']==draft
    assert result['usage']['output_tokens']==(6 if provider=='gemini' else 4)
    assert calls[0][1]['headers']

def test_media_adapters_no_real_network(tmp_path):
    class H:
        def json(self,method,url,**kw):
            if 'texttospeech' in url:return {'audioContent':base64.b64encode(b'WAVE').decode()}
            return {'candidates':[{'content':{'parts':[{'inlineData':{'data':base64.b64encode(b'PNG').decode()}}]}}], 'usageMetadata':{'totalTokenCount':1200}}
    a=Adapters(H(),{'GOOGLE_TTS_API_KEY':'hidden','GEMINI_API_KEY':'hidden'})
    a.media('tts','voice',{'path':str(tmp_path/'a.wav'),'text':'안녕'})
    result=a.media('image','model',{'path':str(tmp_path/'a.png'),'text':'일러스트'})
    assert (tmp_path/'a.wav').read_bytes()==b'WAVE'
    assert result['usage']['billing_unknown']

def test_video_job_poll_and_resume_same_task(tmp_path):
    calls=[];image=tmp_path/'in.png';image.write_bytes(b'PNG')
    class H:
        def json(self,method,url,**kw):
            calls.append((method,url))
            if method=='POST':return {'id':'task1'}
            return {'status':'SUCCEEDED','output':['https://example.org/clip.mp4']}
        def request(self,*a,**kw):return SimpleNamespace(status_code=200,content=b'MP4')
    a=Adapters(H(),{'RUNWAY_API_KEY':'hidden'},sleep=lambda _:None)
    payload={'path':str(tmp_path/'out.mp4'),'image':str(image),'text':'움직임','seconds':5}
    a.media('video','gen4_turbo',payload);a.media('video','gen4_turbo',payload)
    assert len([c for c in calls if c[0]=='POST'])==1

def test_cost_limit_prevents_adapter_call(tmp_path):
    cfg=load_config();cfg['providers']['llm']='openai';cfg['budget']['daily_usd']=.000001
    calls=[]
    p=Provider(cfg,Store(tmp_path),'r',invoke=lambda *a:calls.append(a))
    with pytest.raises(BudgetExceeded):p.draft({'title':'책','text':'원문','entities':[]},'insta')
    assert calls==[]

def test_http_does_not_follow_auth_redirect():
    captured=[]
    class Session:
        def request(self,*a,**kw):captured.append(kw);return SimpleNamespace(status_code=302,json=lambda:{})
    with pytest.raises(RemoteError):HTTP(Session()).json('GET','https://example.org',headers={'Authorization':'hidden'})
    assert captured[0]['allow_redirects'] is False

def test_youtube_lost_put_queries_same_session(tmp_path):
    (tmp_path/'short.mp4').write_bytes(b'VIDEO')
    calls=[]
    class R:
        def __init__(self,status,data=None,headers=None):self.status_code=status;self.data=data or {};self.headers=headers or {}
        def json(self):return self.data
    responses=[R(200,headers={'Location':'https://www.googleapis.com/upload/youtube/v3/videos?upload_id=x'}),OSError('lost'),R(201,{'id':'same_video'})]
    class Session:
        def request(self,method,url,**kw):
            calls.append((method,kw));r=responses.pop(0)
            if isinstance(r,Exception):raise r
            return r
    result=resumable(tmp_path,{'status':{}},Session(),sleep=lambda _:None)
    assert result['id']=='same_video'
    assert calls[-1][1]['headers']['Content-Range']=='bytes */5'
    assert len([c for c in calls if c[0]=='POST'])==1

def test_youtube_unknown_start_never_restarts(tmp_path):
    (tmp_path/'short.mp4').write_bytes(b'VIDEO')
    calls=[]
    class Session:
        def request(self,*a,**kw):calls.append(a);raise OSError('lost')
    with pytest.raises(ValueError):resumable(tmp_path,{'status':{}},Session(),sleep=lambda _:None)
    with pytest.raises(Uncertain):resumable(tmp_path,{'status':{}},Session(),sleep=lambda _:None)
    assert len(calls)==1

def test_youtube_quota_is_deferred_not_unknown(tmp_path):
    (tmp_path/'short.mp4').write_bytes(b'VIDEO')
    class Session:
        def request(self,*a,**kw):return SimpleNamespace(status_code=403,json=lambda:{'error':{'errors':[{'reason':'quotaExceeded'}]}})
    with pytest.raises(Deferred):publish(tmp_path,{'status':{}},Session())
    assert not (tmp_path/'upload-session.json').exists()
