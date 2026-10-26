"""shorts-kit/oauth_setup.py를 복사·확장. 본인이 로컬에서만 실행한다."""
import argparse
import json
from common import cli, kit_path, load_config, read_json, save_json, now
from ops.tokens import UPLOAD_SCOPE, ANALYTICS_SCOPE, CHANNEL_SCOPE

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config');parser.add_argument('--analytics',action='store_true');parser.add_argument('--post-review',action='store_true')
    args=parser.parse_args();cfg=load_config(kit_path(args.config) if args.config else None)
    client=kit_path(cfg['ops']['google_client_file']);token=kit_path(cfg['ops']['google_token_file'])
    if token.exists(): raise ValueError('토큰 파일이 이미 있습니다. 재동의하려면 기존 파일을 비공개 백업한 뒤 옮기세요.')
    settings=read_json(client).get('installed',{})
    if settings.get('auth_uri')!='https://accounts.google.com/o/oauth2/auth' or settings.get('token_uri')!='https://oauth2.googleapis.com/token': raise ValueError('Google Desktop app 인증 파일을 사용하세요.')
    scopes=[UPLOAD_SCOPE, CHANNEL_SCOPE]
    if args.analytics: scopes.append(ANALYTICS_SCOPE)
    if args.post_review or cfg['mode']=='post_review' or cfg['youtube'].get('publishAt'): scopes.append('https://www.googleapis.com/auth/youtube.force-ssl')
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow=InstalledAppFlow.from_client_secrets_file(str(client),scopes=scopes)
        credential=flow.run_local_server(port=0,authorization_prompt_message='본인 브라우저에서 채널·권한을 확인하세요.',success_message='인증 완료. 터미널로 돌아가세요.')
        value=json.loads(credential.to_json());value['granted_at']=now().isoformat();save_json(token,value)
    except ImportError: raise ValueError('requirements-live.txt를 먼저 설치하세요.') from None
    except Exception: raise ValueError('OAuth 동의 실패. API 활성화·본인 테스트 사용자·채널을 확인하세요.') from None
    print('OAuth 토큰 저장 완료. 값은 출력하지 않습니다.')

if __name__=='__main__': cli(main)
