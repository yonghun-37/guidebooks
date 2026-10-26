"""Actions용 private/ 전체를 암호화해 별도 비공개 R2 객체에 보존한다."""
import argparse
import io
from pathlib import Path
import sqlite3
import sys
import tempfile
import uuid
import json
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import ROOT, cli, secrets
from state import Store
from transport import https_url

MAX_ARCHIVE = 256 * 1024 * 1024  # 키트 기본 상한. 무한 누적 대신 운영자가 보관 정책을 정한다.

def client(values):
    try:
        import boto3
        endpoint=values['STATE_ENDPOINT'];https_url(endpoint)
        from urllib.parse import urlsplit
        if not urlsplit(endpoint).hostname.endswith('.r2.cloudflarestorage.com'): raise ValueError('상태 저장소는 R2 비공개 계정 엔드포인트를 사용하세요.')
        return boto3.client('s3',endpoint_url=endpoint,region_name='auto',aws_access_key_id=values['STATE_ACCESS_KEY_ID'],aws_secret_access_key=values['STATE_SECRET_ACCESS_KEY'])
    except (ImportError,KeyError): raise ValueError('상태 저장소 Secrets·requirements-live.txt를 확인하세요.') from None

def sync(direction, private=None, *, values=None, s3=None):
    values=values if values is not None else secrets();private=Path(private or ROOT/'private').resolve()
    try:
        from cryptography.fernet import Fernet, InvalidToken
        cipher=Fernet(values['STATE_ENCRYPTION_KEY'].encode());bucket=values['STATE_BUCKET']
    except (ImportError,ValueError,KeyError): raise ValueError('STATE_ENCRYPTION_KEY(Fernet 키)·STATE_BUCKET을 설정하세요.') from None
    s3=s3 or client(values);key=values.get('STATE_OBJECT_KEY','auto-kit-state.enc')
    lease_path = private / '.state-lease.json'
    lease_key = key + '.lease'
    def acquire():
        nonce = uuid.uuid4().hex
        try:
            s3.put_object(Bucket=bucket,Key=lease_key,Body=nonce.encode(),IfNoneMatch='*',ContentType='text/plain')
        except Exception:
            raise ValueError('외부 상태에 미완료 실행 표식이 있습니다. 이전 상태 보존/복구를 확인할 때까지 실행하지 않습니다.') from None
        return nonce
    if direction=='push':
        if not (private/'state/state.sqlite').exists(): raise ValueError('보존할 상태 DB가 없습니다. 새 빈 상태로 덮어쓰지 않습니다.')
        from common import read_json,save_json
        if lease_path.exists():
            nonce = read_json(lease_path)['nonce']
            try:
                actual = s3.get_object(Bucket=bucket,Key=lease_key)['Body'].read(1024).decode()
                if actual != nonce: raise ValueError()
            except Exception:
                raise ValueError('외부 상태 lease가 현재 실행과 다릅니다. 덮어쓰지 않습니다.') from None
        else:
            nonce = acquire(); save_json(lease_path, {'nonce':nonce})
        store=Store(private/'state')
        with store.lock(), tempfile.TemporaryDirectory() as temporary:
            backup=Path(temporary)/'state.sqlite'
            connection=sqlite3.connect(backup)
            store.db.backup(connection);connection.close()
            buffer=io.BytesIO()
            with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as archive:
                for path in sorted(private.rglob('*')):
                    if path.is_symlink(): raise ValueError('private/에는 심볼릭 링크를 두지 마세요.')
                    if not path.is_file() or path.name in ('state.sqlite-wal','state.sqlite-shm','runner.lock','.state-lease.json'): continue
                    archive.write(backup if path.name=='state.sqlite' else path,path.relative_to(private).as_posix())
            store.db.close()
            if buffer.tell()>MAX_ARCHIVE: raise ValueError('상태 묶음이 256MiB를 넘었습니다. 보존 정책을 정하고 백업하세요.')
            data=cipher.encrypt(buffer.getvalue())
            try: s3.put_object(Bucket=bucket,Key=key,Body=data,ContentType='application/octet-stream')
            except Exception: raise ValueError('외부 상태 보존 실패. 다음 실행을 중단하고 현재 runner/로컬 상태를 복구하세요.') from None
            try: s3.delete_object(Bucket=bucket,Key=lease_key)
            except Exception: raise ValueError('상태는 보존했으나 lease 해제 실패. 다음 실행 전에 객체·lease를 확인하세요.') from None
            lease_path.unlink()
    elif direction=='pull':
        if private.exists() and any(p.is_file() for p in private.rglob('*')):
            raise ValueError('기존 private/가 있어 복원을 중단했습니다. 새 폴더에서 복원하세요.')
        nonce = acquire()
        try:
            response=s3.get_object(Bucket=bucket,Key=key)
            data=response['Body'].read(MAX_ARCHIVE*2+1)
            if len(data)>MAX_ARCHIVE*2: raise ValueError()
            raw=cipher.decrypt(data)
            archive=zipfile.ZipFile(io.BytesIO(raw))
        except Exception: raise ValueError('외부 상태를 복원하지 못했습니다. 빈 DB로 실행하지 않습니다. 처음 1회 로컬 push 또는 키·객체를 확인하세요.') from None
        if sum(info.file_size for info in archive.infolist())>MAX_ARCHIVE: raise ValueError('상태 복원 용량 상한 초과')
        if 'state/state.sqlite' not in archive.namelist(): raise ValueError('복원 묶음에 상태 DB가 없습니다.')
        for info in archive.infolist():
            target=(private/info.filename).resolve()
            if not target.is_relative_to(private) or info.filename.startswith('/') or '\\' in info.filename or (info.external_attr>>16)&0o170000==0o120000:
                raise ValueError('상태 묶음에 허용되지 않은 경로가 있습니다.')
        for info in archive.infolist():
            target=private/info.filename
            if info.is_dir(): target.mkdir(parents=True,exist_ok=True);continue
            target.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
            target.write_bytes(archive.read(info));target.chmod(0o600)
        # 승인 대상은 상대경로·파일 bytes이므로 이동해도 승인 내용은 같다.
        relocate(private)
        from common import save_json
        save_json(lease_path, {'nonce':nonce})
    else: raise ValueError('push/pull 중 하나를 고르세요.')

def relocate(private):
    """출력 폴더만 새 private/로 옮긴다. 설정·승인·요청 내용은 바꾸지 않는다."""
    store=Store(private/'state')
    for run in store.runs():
        from pathlib import PureWindowsPath
        old = PureWindowsPath(run['output']) if PureWindowsPath(run['output']).drive else Path(run['output'])
        new = private / 'state' / run['id']
        if not new.is_dir():
            raise ValueError('복원한 실행 폴더가 없습니다. 자동 발행하지 않았습니다.')
        run['output'] = str(new)
        path_type = PureWindowsPath if isinstance(old,PureWindowsPath) else Path
        run['files'] = [str(new / Path(*path_type(file).relative_to(old).parts)) for file in run['files']]
        if run.get('insights', {}).get('csv'):
            run['insights']['csv'] = str(new / 'insights.csv')
        store.save(run)
        from common import save_json
        save_json(new / 'run.json',run)
    store.db.close()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('direction',choices=['push','pull']);p.add_argument('--live',action='store_true')
    a=p.parse_args()
    if not a.live: raise ValueError('외부 상태 전송에는 --live를 명시하세요.')
    sync(a.direction);print('암호화 상태 '+a.direction+' 완료. 인증 값은 출력하지 않습니다.')

if __name__=='__main__':cli(main)
