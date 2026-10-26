from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath
import io
from types import SimpleNamespace
import pytest
from cryptography.fernet import Fernet
import pipeline as module
from pipeline import Pipeline
from common import load_config, now, hashed
from ops.state_sync import sync,relocate
from providers import Provider
from state import Store, BudgetExceeded
from topics import select_topic

def test_same_local_date_across_utc_midnight_creates_once(tmp_path,monkeypatch):
    p=Pipeline(load_config(),tmp_path);calls=[]
    monkeypatch.setattr(module,'local_now',lambda:datetime(2026,10,26,0,tzinfo=timezone.utc))
    p.run=lambda *a,**kw:(calls.append('run') or {'id':'r'})
    p.tick(flow='insta',daily_at='00:00')
    monkeypatch.setattr(module,'now',lambda:datetime(2026,10,26,1,tzinfo=timezone.utc))
    p.tick(flow='insta',daily_at='00:00')
    assert len(calls)==1

def test_windows_paths_relocate_without_changing_approval(tmp_path):
    private=tmp_path/'private';p=Pipeline(load_config(),private/'state');r=p.run('insta');p.approve(r['id'])
    r=p.store.get(r['id']);old=Path(r['output']);win=PureWindowsPath('C:/book/auto-kit/private/state')/r['id']
    r['files']=[str(win/Path(f).relative_to(old)) for f in r['files']];r['output']=str(win);p.store.save(r)
    relocate(private)
    assert p.resume(r['id'])['status']=='dry_run'

def test_remote_push_failure_leaves_lease_and_blocks_next_pull(tmp_path):
    private=tmp_path/'private';p=Pipeline(load_config(),private/'state');p.run('insta')
    class S3:
        def __init__(self):self.objects={}
        def put_object(self,**kw):
            if kw['Key'].endswith('.lease'):
                if kw['Key'] in self.objects:raise ValueError('existing lease')
                self.objects[kw['Key']]=kw['Body'];return
            raise OSError('storage failed')
        def get_object(self,**kw):return {'Body':io.BytesIO(self.objects[kw['Key']])}
    s3=S3();v={'STATE_ENCRYPTION_KEY':Fernet.generate_key().decode(),'STATE_BUCKET':'private'}
    with pytest.raises(ValueError):sync('push',private,values=v,s3=s3)
    assert 'auto-kit-state.enc.lease' in s3.objects
    with pytest.raises(ValueError,match='미완료'):sync('pull',tmp_path/'next/private',values=v,s3=s3)

def test_done_live_metrics_recollected_by_tick(tmp_path,monkeypatch):
    cfg=load_config();cfg['mode']='auto';p=Pipeline(cfg,tmp_path);r=p.run('insta')
    r['live']=True;r['status']='done';p.store.save(r);calls=[]
    monkeypatch.setattr(module,'collect',lambda *a,**kw:(calls.append(kw) or {'refreshed':True}))
    p.tick(live=True)
    p.tick(live=True)
    assert len(calls)==1 and calls[0]['live']
    assert p.store.get(r['id'])['insights']['refreshed']

def test_run_envelope_is_not_double_charged(tmp_path):
    s=Store(tmp_path)
    envelope=s.reserve('r','run:maximum',.08,daily=.1,monthly=.1)
    ticket=s.reserve('r','llm',.06,daily=.1,monthly=.1)
    assert s.spend()['total']==pytest.approx(.08)
    s.settle(ticket,.02,{'input_tokens':3,'output_tokens':3})
    assert s.spend()['total']==pytest.approx(.08)
    s.finish_budget('r')
    assert s.spend()['total']==pytest.approx(.02)

def test_rss_explicit_rights_confirmation(tmp_path):
    path=tmp_path/'feed.xml';path.write_text('<rss><channel><item><title>소식</title><description>책 소식</description></item></channel></rss>')
    cfg=load_config();cfg['sources']['files']=[];cfg['sources']['rss']=[{'url':str(path),'rights_reviewed':True,'category':'독서'}]
    source=select_topic(cfg,Store(tmp_path/'state'),'insta')
    assert source['rights_reviewed'] is True

def test_live_upload_channel_swap_is_blocked(tmp_path,monkeypatch):
    cfg=load_config();cfg['mode']='approval';cfg['providers']['llm']='openai';cfg['budget']['provider_hard_cap_confirmed']=True;cfg['media']['recording']=str(tmp_path/'recording.wav')
    p=Pipeline(cfg,tmp_path);source={'title':'책','text':'책 이야기','entities':[],'rights_reviewed':True,'synthetic':False,'source_hash':hashed('책 이야기')}
    p.select=lambda *a,**kw:source
    monkeypatch.setattr(Provider,'draft',lambda *a:Provider.mock_draft(source,'shorts'))
    Provider(cfg,p.store,'fixture',mock=True).media('tts','음성',tmp_path/'recording.wav')
    channel=['channelA'];calls=[]
    class Session:
        def request(self,method,url,**kw):
            calls.append((method,url))
            assert method=='GET' and url.endswith('/channels')
            return SimpleNamespace(status_code=200,json=lambda:{'items':[{'id':channel[0]}]})
    p._credentials=lambda *a:Session();monkeypatch.setattr(p,'_notice',lambda *a:None)
    r=p.run('shorts',live=True);assert r['status']=='waiting_approval'
    assert r['target']['account']=='channelA'
    p.approve(r['id']);channel[0]='channelB'
    result=p.resume(r['id'],live=True)
    assert result['status']=='failed' and 'publish' not in result['steps']
    assert '채널' in result['reason']

def test_resuming_video_reuses_cost_ticket(tmp_path):
    cfg=load_config();cfg['providers']['video']='runway';s=Store(tmp_path/'state');attempts=[]
    image=tmp_path/'image.png';image.write_bytes(b'owned-image')
    def invoke(kind,payload,model):
        attempts.append(kind)
        if len(attempts)==1:raise ValueError('작업 폴링 대기')
        Path(payload['path']).write_bytes(b'MP4')
        return {'value':payload['path'],'usage':{'seconds':5}}
    p=Provider(cfg,s,'r',invoke=invoke)
    with pytest.raises(ValueError):p.media('video','장면',tmp_path/'clip.mp4',image=str(image),seconds=5)
    assert s.spend()['pending']==pytest.approx(.25)
    p.media('video','장면',tmp_path/'clip.mp4',image=str(image),seconds=5)
    assert len(s.calls())==1 and s.spend()['total']==pytest.approx(.25)

def test_reserved_publish_at_requires_cancel_scope(tmp_path):
    from common import save_json
    from ops.tokens import google_session,UPLOAD_SCOPE,CHANNEL_SCOPE
    cfg=load_config();cfg['mode']='approval';cfg['youtube']['publishAt']='2099-01-01T00:00:00Z'
    client=tmp_path/'client.json';token=tmp_path/'token.json'
    cfg['ops']['google_client_file']=str(client);cfg['ops']['google_token_file']=str(token)
    save_json(client,{'installed':{'client_id':'id','client_secret':'secret'}})
    save_json(token,{'client_id':'id','client_secret':'secret','token_uri':'https://oauth2.googleapis.com/token','scopes':[UPLOAD_SCOPE,CHANNEL_SCOPE]})
    with pytest.raises(ValueError,match='scope'):google_session(cfg)
