"""키·토큰·ffmpeg·한도·비용 설정을 한국어로 안내한다. 기본 오프라인."""
import argparse
from datetime import timedelta
import shutil
import subprocess
import imageio_ffmpeg
from common import ROOT, cli, kit_path, load_config, secrets, read_json, timestamp, now

def diagnose(config, values=None, live=False, flow=None):
    values = values if values is not None else secrets()
    results = []
    def add(level, message): results.append({'level':level,'message':message})
    if not kit_path(config['media']['font']).is_file(): add('error','한글 폰트 파일이 없습니다. media.font 경로를 확인하세요.')
    try:
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-version'],check=True,capture_output=True)
        add('ok','pip ffmpeg 실행 가능. 시스템 패키지 설치가 필요 없습니다.')
    except (OSError,RuntimeError,subprocess.CalledProcessError):
        add('error','pip ffmpeg가 없습니다. requirements.txt를 바이너리로 다시 설치하세요.')
    add('ok' if shutil.which('ffprobe') else 'info','ffprobe JSON 사용' if shutil.which('ffprobe') else 'ffprobe 없음: 동봉하지 않고 pip ffmpeg 규격 parser로 검사합니다.')
    if config['budget']['daily_usd'] <= 0 or config['budget']['monthly_usd'] <= 0:
        add('error','일/월 비용 상한을 0보다 크게 설정하세요.')
    else:
        add('ok',f"일 ${config['budget']['daily_usd']}, 월 ${config['budget']['monthly_usd']} 상한. UTC 기준, 재시도·예약 비용 포함.")
    if not live:
        add('ok','mock 준비 완료. 키·토큰 없이 두 흐름을 실행할 수 있습니다.')
        return results
    if config['providers']['llm']=='mock': add('error','실제 LLM 공급자를 설정하세요. providers.llm: openai/gemini/anthropic')
    required={'openai':'OPENAI_API_KEY','gemini':'GEMINI_API_KEY','anthropic':'ANTHROPIC_API_KEY'}
    key=required.get(config['providers']['llm'])
    if key and not values.get(key): add('error',key+' 누락. .env에 직접 넣으세요.')
    if not config['budget']['provider_hard_cap_confirmed']: add('error','공급자 강제 지출 상한 확인 후 provider_hard_cap_confirmed=true. Cloud budget 알림은 자동 중지가 아닙니다.')
    if config['media']['image_api'] and not values.get('GEMINI_API_KEY'): add('error','이미지 API GEMINI_API_KEY가 없습니다.')
    if config['media']['video_api'] and not values.get('RUNWAY_API_KEY'): add('error','영상 API RUNWAY_API_KEY가 없습니다.')
    if flow in (None,'shorts'):
        if not config['media']['recording'] and config['providers']['tts']=='mock': add('error','쇼츠에는 본인 녹음 또는 Google TTS 공급자를 설정하세요.')
        if config['providers']['tts']!='mock' and not values.get('GOOGLE_TTS_API_KEY'): add('error','GOOGLE_TTS_API_KEY가 없습니다.')
        path=kit_path(config['ops']['google_token_file'])
        client=kit_path(config['ops']['google_client_file'])
        if not path.exists() or not client.exists(): add('error','사용자 OAuth 인증 파일이 없습니다. python oauth_setup.py를 실행하세요.')
        else:
            try:
                token=read_json(path)
                if not token.get('refresh_token'): add('error','Google refresh token이 없습니다. 재동의하세요.')
                if values.get('GOOGLE_OAUTH_MODE','testing')=='testing':
                    granted=token.get('granted_at')
                    if not granted: add('warning','OAuth Testing: 동의 시각이 없어 7일 만료를 계산할 수 없습니다.')
                    elif timestamp(granted)+timedelta(days=7) <= now()+timedelta(days=1): add('warning','OAuth Testing 7일 만료가 임박/경과했습니다. Production 요건 확인 후 재동의하세요.')
                if 'https://www.googleapis.com/auth/youtube.readonly' not in token.get('scopes',[]): add('error','실제 대상 채널 확인에 youtube.readonly 권한이 필요합니다. 재동의하세요.')
                if (config['mode']=='post_review' or config['youtube'].get('publishAt')) and 'https://www.googleapis.com/auth/youtube.force-ssl' not in token.get('scopes',[]): add('error','예약 취소에는 youtube.force-ssl 권한이 필요합니다. oauth_setup.py --post-review로 재동의하세요.')
            except (ValueError,TypeError): add('error','Google 토큰 JSON 형식·시각을 확인하세요.')
        if not config['youtube']['quota_confirmed_at']: add('error','Cloud Console의 실제 insert 버킷을 확인해 youtube.quota_confirmed_at을 UTC 시각으로 기록하세요.')
        add('info','YouTube 로컬 일일 cap과 API quota 거절을 함께 검사합니다. API 업로드 한도·채널 한도는 별개입니다.')
    if flow in (None,'insta'):
        token_path=kit_path(config['ops']['instagram_token_file'])
        token=read_json(token_path) if token_path.exists() else {'access_token':values.get('IG_ACCESS_TOKEN'),'issued_at':values.get('IG_TOKEN_ISSUED_AT'),'expires_at':values.get('IG_TOKEN_EXPIRES_AT')}
        if not all(token.get(k) for k in ('access_token','issued_at','expires_at')): add('error','Instagram 토큰·발급 시각·만료 시각이 필요합니다. .env.example을 참고하세요.')
        else:
            try:
                left=timestamp(token['expires_at'])-now()
                if left.total_seconds()<=0: add('error','Instagram 토큰 만료. 재인증하세요.')
                elif left.days<config['ops']['token_warning_days']: add('warning','Instagram 토큰 만료 임박. 다음 live 실행에서 조건이 맞으면 갱신합니다.')
            except ValueError: add('error','Instagram 발급·만료 시각에 UTC 오프셋을 넣으세요.')
        if config['hosting']['adapter']=='local': add('error','실제 공개 URL 호스팅 pages 또는 r2를 설정하세요.')
        add('info','Instagram 한도는 발행 직전 content_publishing_limit로 읽습니다. 조회 실패 시 연기합니다.')
    return results

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config');p.add_argument('--live',action='store_true');p.add_argument('--flow',choices=['insta','shorts']);p.add_argument('--check-remote',action='store_true')
    args=p.parse_args();cfg=load_config(kit_path(args.config) if args.config else None)
    results=diagnose(cfg,live=args.live,flow=args.flow)
    for row in results: print(f"[{row['level']}] {row['message']}")
    if args.check_remote:
        if not args.live or args.flow!='insta': raise ValueError('--check-remote는 --live --flow insta와 함께 사용하세요. 게시하지 않고 계정/한도만 조회합니다.')
        from ops.tokens import instagram_token
        from publish.instagram import Instagram
        from transport import HTTP
        token=instagram_token(cfg,refresh=True)['access_token'];account=cfg['instagram']['account']
        if not str(account).isdigit(): account=secrets().get('IG_USER_ID','')
        quota=Instagram(HTTP(),token=token,account=account).limit()
        print(f"[ok] 한도 조회: 사용 {quota['usage']} / 계정 총량 {quota['total']}")
    if any(r['level']=='error' for r in results): raise SystemExit(1)

if __name__=='__main__': cli(main)
