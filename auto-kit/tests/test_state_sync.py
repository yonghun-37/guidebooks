import io
from pathlib import Path
from cryptography.fernet import Fernet
from common import load_config
from pipeline import Pipeline
from ops.state_sync import sync
from approve import require_approval

def test_encrypted_restore_preserves_approval_on_new_root(tmp_path):
    original=tmp_path/'one/private'; destination=tmp_path/'two/private'
    p=Pipeline(load_config(),original/'state');r=p.run('insta');p.approve(r['id'])
    class S3:
        def __init__(self): self.objects={}
        def put_object(self,**kw):
            if kw.get('IfNoneMatch') and kw['Key'] in self.objects:raise ValueError('busy')
            self.objects[kw['Key']]=kw['Body']
            if not kw['Key'].endswith('.lease'):self.data=kw['Body']
        def get_object(self,**kw): return {'Body':io.BytesIO(self.objects[kw['Key']])}
        def delete_object(self,**kw): self.objects.pop(kw['Key'],None)
    s3=S3();values={'STATE_ENCRYPTION_KEY':Fernet.generate_key().decode(),'STATE_BUCKET':'private'}
    sync('push',original,values=values,s3=s3)
    assert '가상'.encode() not in s3.data
    sync('pull',destination,values=values,s3=s3)
    restored=Pipeline(load_config(),destination/'state')
    run=restored.store.get(r['id'])
    require_approval(run)
    assert restored.resume(r['id'])['status']=='dry_run'
