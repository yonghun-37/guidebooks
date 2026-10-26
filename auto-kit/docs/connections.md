# 자격을 만들고 실제 출력까지 연결하기

2026년 10월 조사 기준. 아래 실제 서비스 단계는 **사용자가 자기 계정으로 수행**해요. 무료 연습에는 필요 없어요. 키를 화면 공유·Git·채팅에 넣지 마세요. 화면 위치 그림은 [인스타 게시](../../site/advanced/05-publish.html#hosting-pages), [쇼츠 자격](../../site-shorts/advanced/02-credentials.html#google-tts), [운영 알림](../../site-shorts/advanced/07-operations.html#alerts)에 있어요.

## 무료 교육용 Instagram 파일: GitHub Pages

1. [GitHub](https://github.com/) 계정을 만들고 본인 별도 **public** 저장소(예: `learning-media`)를 만들어요. README를 함께 만들어 초기 브랜치를 준비해요. 이곳에는 공개해도 되는 미디어만 올려요. 키트·private·토큰·DB를 복사하지 않아요.
2. 저장소 브랜치 메뉴에서 `media` 브랜치를 만들어요. `media`에 `index.html`을 추가해 간단한 안내문을 저장해요. Settings → Pages → Source에서 **Deploy from a branch**, Branch `media`, 폴더 `/(root)` → Save를 눌러요. 표시되는 `https://본인아이디.github.io/learning-media/`를 열어 안내문을 확인해요.
3. 우측 사용자 설정 Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token에서 소유자·만료일을 정해요. Only select repositories로 이 저장소만 선택하고 Repository permissions의 **Contents: Read and write**를 허용해요. 키 문자열은 본인 로컬 `.env`의 `PAGES_TOKEN=` 뒤에 넣어요. 만료 전 교체하세요.
4. `config.json`의 `hosting` 객체를 아래처럼 바꿔요. OWNER·저장소 이름은 본인 값이에요. `media`는 브랜치 이름이며 공개 URL에 붙이지 않아요.

```json
{
  "adapter": "pages",
  "base_url": "https://OWNER.github.io/learning-media",
  "pages_repository": "OWNER/learning-media",
  "pages_branch": "media",
  "r2_bucket": "",
  "r2_endpoint": "",
  "max_bytes_per_run": 25000000
}
```

```bash
python doctor.py --config config.json --live --flow insta
```

이렇게 보이면 성공: 호스팅 필수 설정·키의 누락 오류가 없어요. doctor는 여기서 업로드·키 유효성·배포 성공을 검증하지 않아요. 다른 `[error]`는 LLM·Instagram 인증 안내에 따라 해결해요.

5. README 5절의 본인 소스·실제 생성·승인제 `run --live`를 실행해요. 키트가 JPEG/MP4만 미디어 브랜치에 올려요. 배포 중이라 `공개 URL의 파일·MIME·배포를 확인하지 못했습니다`면 Pages 배포 완료 후 **같은 ID로 resume**해요. 생성 결과는 다시 만들지 않아요.
6. `private/state/RUN_ID/run.json`의 `hosting.urls`에서 첫 URL을 복사해 로그아웃 창에서 열어요. 미리보기 페이지가 아닌 JPEG/MP4 자체가 보여야 해요. 키트는 인증 없는 GET·MIME·SHA256 일치 후에만 host 단계를 완료해요. 그다음 관문·승인·게시 순서예요. 공개 전에 이미 호스팅되므로 공개 불가 자료는 넣지 마세요.

Pages는 작은 교육용 선택지예요. 상업 호스팅 제한과 저장/전송/build 한도가 있어 사업용 CDN으로 계속 쓰는 구성은 별도 확인하세요. 운영 대안 R2는 결제 활성화 뒤 공개 **미디어 bucket**을 만들고 공개 도메인을 연결해요. R2 → Account Details → API Tokens → Manage에서 해당 bucket Object Read & Write 권한만 골라 Access Key ID/Secret과 S3 endpoint를 받아요. `hosting.adapter=r2`, `r2_bucket=버킷이름`, `r2_endpoint=https://계정ID.r2.cloudflarestorage.com`, `base_url=공개도메인`으로 설정하고 `.env`에 `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`를 넣어요. endpoint는 비공개 API용이며 공개 URL이 아니에요. `requirements-live.txt` 설치 후 같은 doctor·URL 확인 순서를 써요. 무료량·초과 청구·도메인 비용을 확인하고 private 상태용 bucket과 분리해요. r2.dev는 개발용이에요. [공식 근거](../../research-advanced/a6-connections.md)

## Google Cloud 음성 키

1. [Cloud Console](https://console.cloud.google.com/)에 본인 계정으로 들어가 프로젝트를 만들어요. Billing에서 결제 계정을 연결해요. 무료량을 쓰더라도 연결이 필요해요.
2. APIs & Services → Library → **Cloud Text-to-Speech API** → Enable을 눌러요.
3. 같은 프로젝트 Credentials → Create credentials → API key를 만들어요. standard 키를 쓰고 API restrictions에서 Cloud Text-to-Speech API만 허용해요. 고정 서버 IP가 있으면 IP 제한도 적용해요. 서버 Python 호출에 웹사이트 referrer 제한을 걸지 않아요.
4. 키 문자열을 `.env`의 `GOOGLE_TTS_API_KEY=` 뒤에 넣어요. YouTube OAuth JSON·Gemini AI Studio 키와 달라요. config는 `providers.tts: "google"`, `models.tts: "ko-KR-Wavenet-A"`, `media.recording: null`로 정해요. 본인 프로젝트에 제공되는 ko-KR 음성을 고르세요.
5. `python doctor.py --config config.json --live --flow shorts`로 키 존재 등 빠진 설정을 확인해요. [본문의 짧은 WAV 시험](../../site-shorts/advanced/03-generation.html#tts-test)으로 발음·파일을 확인한 뒤 전체 실행을 해요. 짧은 시험은 업로드 없이 TTS만 호출하지만 파이프라인 비용 예약 밖이므로 Cloud 사용량도 확인해요.

Cloud 예산 알림은 자동 중지가 아니에요. 무료량·초과 단가·API quota를 확인하고 무인 운영 전 비용 통제를 준비하세요. 같은 녹음을 매일 새 대본에 붙이면 내용이 달라져요. 본인 녹음 대안은 대본마다 새로 필요해요. [발급·인증 근거](../../research-advanced/a6-connections.md)

## 무료 모델로 매일 가능한가

**한국어 글 생성은 소규모 무료 등급으로 시도할 수 있어요. 매일 성공·전체 청구 0원은 보장하지 않아요.** 예를 들어 `providers.llm: "gemini"`, `models.gemini: "gemini-3.5-flash-lite"`를 고르고 [가격표](https://ai.google.dev/gemini-api/docs/pricing)의 Free Tier와 [한도 문서의 active rate limits 링크](https://ai.google.dev/gemini-api/docs/rate-limits)를 열어요. 본인 프로젝트의 RPM·TPM·RPD 안에 생성·대조·재시도까지 들어가야 해요. 한도를 소진하면 기다리거나 예산을 정한 유료 모델로 바꿔요. 한국어 원문 한 편을 먼저 생성해 숫자·줄바꿈을 검수하세요.

한국의 unpaid 입력·응답은 제품 개선과 사람 검토에 쓰일 수 있어 개인정보·기밀은 넣지 않아요. 카드 템플릿·로컬 렌더에는 API 청구가 없어요. 쇼츠는 별도 TTS 무료량·결제 조건을 확인해요. 이미지·영상 생성 API는 무료라고 전제하지 않아요. 키트는 무료 잔량을 모르므로 **유료 단가로 보수적으로 비용 예약**해요.

무료 LLM만 고르면, 결제 미연결 프로젝트라 유료 청구가 불가능한지 AI Studio와 Cloud Billing에서 직접 확인한 경우에만 `provider_hard_cap_confirmed: true`를 기록해요. 유료 프로젝트에는 강제 상한을 따로 확인해요. 이 확인으로 결제가 연결된 TTS까지 초과 차단된다고 생각하면 안 돼요. [무료량·데이터 조건 근거](../../research-advanced/a6-connections.md)

## Discord 알림 → 선택 Telegram 승인

**Discord는 운영자가 알림을 읽는 곳이고 승인 버튼 수신기는 아니에요.** 본인 서버를 만든 뒤 Server Settings → Integrations → Webhooks → New Webhook에서 수신 채널을 골라요. Copy Webhook URL로 받은 값을 `.env`의 `DISCORD_WEBHOOK_URL=`에 넣어요.

시험은 아래처럼 게시 없이 알림 함수만 호출해요. 네트워크를 쓰므로 본인이 자격을 넣은 뒤 실행하세요.

```bash
python -c "from pathlib import Path; from common import ROOT; from ops.notifications import notify; p=ROOT/'private/notify-test'; p.mkdir(parents=True,exist_ok=True); notify({'id':'test','flow':'insta','status':'설정 시험','output':str(p),'files':[]},'알림 연결 시험',live=True)"
```

이렇게 보이면 성공: 지정 채널에 `알림 연결 시험`이 와요. 로컬 `private/notify-test/notification.json`도 확인하세요. 실제 매일 알림은 실행기가 live로 보냅니다. 운영자는 예외 알림의 ID·이유를 읽고 해당 미리보기/원문을 확인해요.

휴대폰 승인을 원하면 Telegram에서 공식 BotFather의 `/newbot`으로 봇을 만들고 토큰을 `.env`의 `TELEGRAM_BOT_TOKEN`에 넣어요. 그 봇과 **개인 채팅**을 시작하고 메시지를 하나 보내요. [본문 ID 조회 명령](../../site-shorts/advanced/07-operations.html#alerts)으로 `message.from.id`를 `TELEGRAM_ALLOWED_USER`, `message.chat.id`를 `TELEGRAM_CHAT_ID`에 넣어요. 봇 username은 숫자 ID가 아니에요.

운영자는 봇에 대기 알림이 오면 미리보기를 읽고 버튼을 눌러요. 컴퓨터 쪽 운영자는 **그때** `python pipeline.py telegram --live`를 켜 두어야 해요. 이 명령은 최대 25초 1회만 읽고 끝나요. 상시 수신은 본문 PowerShell/Bash 반복 루프를 켜고, 창·PC를 유지해요. OS 예약은 tick만 호출하며 수신기를 자동 등록하지 않아요. getUpdates 수신기는 1개만 운영하고 webhook과 함께 쓰지 않아요. 승인은 기록만 하며 다음 tick 또는 동일 ID `resume --live`가 발행해요. [발급 근거·수신 동작](../../research-advanced/a6-connections.md)

앱이 업데이트되면 버튼 이름이나 위치가 조금 다를 수 있어요. 최신 화면에서 비슷한 이름을 찾고 못 찾겠으면 각 절의 공식 도움말을 확인하세요.
