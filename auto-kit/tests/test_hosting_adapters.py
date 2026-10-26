from types import SimpleNamespace
import pytest
from common import load_config
import hosting

@pytest.mark.parametrize('adapter',['pages','r2'])
def test_mocked_hosting_upload_then_public_byte_verification(tmp_path,monkeypatch,adapter):
    media=tmp_path/'card.jpg';media.write_bytes(b'JPEG-FIXTURE')
    cfg=load_config();cfg['hosting'].update({'adapter':adapter,'base_url':'https://media.example.org','pages_repository':'learner/education','pages_branch':'media','r2_endpoint':'https://account.r2.cloudflarestorage.com','r2_bucket':'public-media'})
    monkeypatch.setattr(hosting,'secrets',lambda:{'PAGES_TOKEN':'PRIVATE_HOST_TOKEN_SENTINEL'})
    calls=[]
    class H:
        def request(self,method,url,**kwargs):
            calls.append((method,url,kwargs))
            if 'api.github.com' in url:return SimpleNamespace(status_code=404)
            assert not kwargs.get('headers')
            return SimpleNamespace(status_code=200,headers={'Content-Type':'image/jpeg'},content=media.read_bytes())
        def json(self,method,url,**kwargs):calls.append((method,url,kwargs));return {'content':{'sha':'sha'}}
    class S3:
        def upload_file(self,*args,**kwargs):calls.append(('S3',args,kwargs))
    result=hosting.host([media],cfg,'r',tmp_path,live=True,http=H(),s3=S3())
    assert result['urls']==['https://media.example.org/r/00-card.jpg']
    if adapter=='pages':assert any(c[0]=='PUT' and c[2]['json']['branch']=='media' for c in calls)
    else:assert calls[0][2]['ExtraArgs']['ContentType']=='image/jpeg'

def test_hosting_wrong_public_content_stops(tmp_path,monkeypatch):
    media=tmp_path/'card.jpg';media.write_bytes(b'JPEG')
    cfg=load_config();cfg['hosting'].update({'adapter':'r2','base_url':'https://media.example.org','r2_endpoint':'https://account.r2.cloudflarestorage.com','r2_bucket':'public'})
    class S3:
        def upload_file(self,*a,**k):pass
    class H:
        def request(self,*a,**k):return SimpleNamespace(status_code=200,headers={'Content-Type':'text/html'},content=b'login page')
    with pytest.raises(ValueError,match='공개 URL'):hosting.host([media],cfg,'r',tmp_path,live=True,http=H(),s3=S3())
