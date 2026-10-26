"""사용자가 로컬 브라우저에서 본인 채널의 업로드 권한을 허용할 때만 실행한다."""
import argparse
import json
from pathlib import Path

from common import ROOT, cli, read_json
from upload import SCOPE, private_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-secret", type=Path, default=ROOT / "private" / "client_secret.json")
    parser.add_argument("--token", type=Path, default=ROOT / "private" / "token.json")
    args = parser.parse_args()
    if args.token.exists():
        raise ValueError("토큰 파일이 이미 있습니다. 재인증이 필요하면 기존 파일을 안전한 곳으로 옮기세요.")
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        raise ValueError("python -m pip install -r requirements-live.txt를 먼저 실행하세요.") from None
    client = read_json(args.client_secret).get("installed", {})
    if client.get("auth_uri") != "https://accounts.google.com/o/oauth2/auth" or client.get("token_uri") != "https://oauth2.googleapis.com/token":
        raise ValueError("Google에서 받은 데스크톱 앱 인증 파일을 사용하세요.")
    try:
        flow = InstalledAppFlow.from_client_secrets_file(str(args.client_secret), scopes=[SCOPE])
        credentials = flow.run_local_server(port=0, authorization_prompt_message="브라우저에서 본인 계정·채널·업로드 권한을 확인하세요.", success_message="인증 파일을 저장합니다. 이 창을 닫고 터미널로 돌아가세요.")
        private_json(args.token, json.loads(credentials.to_json()))
    except Exception:
        raise ValueError("인증에 실패했습니다. API 활성화·테스트 사용자·본인 채널을 확인하세요. [Y041] [Y042]") from None
    print("OAuth 토큰 저장 완료. 파일을 공유하거나 Git에 넣지 마세요. 업로드는 실행하지 않았습니다.")


if __name__ == "__main__":
    cli(main)
