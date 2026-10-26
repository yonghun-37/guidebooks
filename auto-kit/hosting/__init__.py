"""미디어 파일만 공개한다. 원본·설정·인증·DB는 업로드하지 않는다."""
import base64
from pathlib import Path
import re
import shutil
from urllib.parse import quote, urlsplit
from common import secrets, digest
from transport import HTTP, https_url

def host(files, config, identifier, output, *, live=False, http=None, s3=None):
    settings = config['hosting']
    if not files or any(Path(f).suffix.lower() not in ('.jpg', '.jpeg', '.mp4') for f in files):
        raise ValueError('호스팅은 게시용 JPEG/MP4만 받습니다.')
    if sum(Path(f).stat().st_size for f in files) > settings['max_bytes_per_run']:
        raise ValueError('호스팅 실행별 용량 상한을 넘었습니다.')
    base = settings['base_url'].rstrip('/')
    https_url(base)
    if urlsplit(base).query:
        raise ValueError('공개 기본 URL에는 쿼리를 넣지 마세요.')
    names = [f'{identifier}/{i:02d}-{Path(f).name}' for i, f in enumerate(files)]
    urls = [base + '/' + quote(name, safe='/') for name in names]
    if not live:
        destination = Path(output) / 'public'
        for file, name in zip(files, names):
            path = destination / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(file, path)
        return {'adapter': 'local', 'urls': urls, 'network_calls': 0}
    if urlsplit(base).hostname.endswith('.invalid') or settings['adapter'] == 'local':
        raise ValueError('실제 호스팅 어댑터와 공개 HTTPS 기본 URL을 설정하세요.')
    http, values = http or HTTP(), secrets()
    if settings['adapter'] == 'pages':
        repository = settings['pages_repository']
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
            raise ValueError('별도 교육용 Pages 저장소 owner/name을 설정하세요.')
        token = values.get('PAGES_TOKEN')
        if not token: raise ValueError('PAGES_TOKEN이 없습니다.')
        headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json'}
        for file, name in zip(files, names):
            url = f'https://api.github.com/repos/{repository}/contents/{quote(name, safe="/")}'
            response = http.request('GET', url, headers=headers, params={'ref': settings['pages_branch']})
            body = {'message': '교육용 미디어 추가', 'branch': settings['pages_branch'], 'content': base64.b64encode(Path(file).read_bytes()).decode()}
            if response.status_code == 200:
                body['sha'] = response.json()['sha']
            elif response.status_code != 404:
                raise ValueError('Pages 미디어 브랜치·저장소 접근을 확인하세요.')
            http.json('PUT', url, headers=headers, json=body)
    elif settings['adapter'] == 'r2':
        endpoint = settings['r2_endpoint']
        https_url(endpoint)
        if not urlsplit(endpoint).hostname.endswith('.r2.cloudflarestorage.com'):
            raise ValueError('R2 계정 S3 엔드포인트를 설정하세요.')
        if s3 is None:
            try:
                import boto3
                s3 = boto3.client('s3', endpoint_url=endpoint, region_name='auto', aws_access_key_id=values['R2_ACCESS_KEY_ID'], aws_secret_access_key=values['R2_SECRET_ACCESS_KEY'])
            except (ImportError, KeyError):
                raise ValueError('R2 키·requirements-live.txt를 확인하세요.') from None
        for file, name in zip(files, names):
            try:
                s3.upload_file(str(file), settings['r2_bucket'], name, ExtraArgs={'ContentType': 'video/mp4' if Path(file).suffix == '.mp4' else 'image/jpeg'})
            except Exception:
                raise ValueError('R2 업로드 확인 실패. 같은 객체 키로 재개하세요.') from None
    else:
        raise ValueError('hosting.adapter는 local/pages/r2 중 하나여야 합니다.')
    # 인증 없이 실제 바이트를 확인한다. 배포 대기 중이면 host 단계에서 멈춘다.
    for file, url in zip(files, urls):
        response = http.request('GET', url)
        expected = 'video/mp4' if Path(file).suffix == '.mp4' else 'image/jpeg'
        import hashlib
        if response.status_code != 200 or not response.headers.get('Content-Type', '').startswith(expected) or hashlib.sha256(response.content).hexdigest() != digest(file):
            raise ValueError('공개 URL의 파일·MIME·배포를 확인하지 못했습니다. 배포 후 resume 하세요.')
    return {'adapter': settings['adapter'], 'urls': urls}
