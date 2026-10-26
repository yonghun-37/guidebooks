# 승인 알림·버튼·토큰 유출 대응

- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/10-approval-security.md` · SHA256 `3bec0a18b6f9fa6404959420c8cc7a6e039f326e7596bea17b7134ba10849f52` · exit 0.
- 실행·실패 구분: [provenance.json](provenance.json). 핵심 주장은 Codex 직접 열람/기존 근거와 대조했다.

2026년 10월 조사 기준. 아래 승인 상태/해시는 후속 구현을 위한 **설계 제안**이다. 봇 생성·메시지 발송·외부 승인 서버 배포를 하지 않았다.

## 추천

**첫 실습은 로컬 승인 파일, 휴대폰 승인은 Telegram bot+long polling을 선택한다.** 이미 디스코드를 쓰면 incoming webhook 알림과 로컬 승인 명령을 결합한다. ‘웹훅 주소 하나면 안전한 승인 버튼까지 끝’이라고 가르치지 않는다.

| 방법 | 알림 | 승인 응답 | 별도 실행기 |
|---|---|---|---|
| 로컬 `approve.json`/명령 | 터미널·미리보기 파일 | 본인 명령으로 승인 기록 | 로컬 파이프라인 |
| Discord incoming webhook | HTTPS POST로 채널 메시지 | 웹훅 자체는 클릭 승인을 수신하지 않음; 링크는 외부 승인 화면으로 이동 | 링크 수신 서버 또는 별도 로컬 명령 |
| Discord app/bot | 메시지+interactive component | `custom_id` 버튼 interaction | Gateway 상시 연결 또는 public HTTP endpoint |
| Telegram bot | `sendMessage`+inline keyboard | `callback_query` 수신·`answerCallbackQuery` | `getUpdates` long polling 또는 HTTPS webhook |

Discord webhook은 일반 알림에 봇 계정을 요구하지 않는다. Link button은 URL을 열지만 앱에 interaction을 보내지 않는다. `custom_id` 버튼은 interaction을 받아 서버가 승인 상태를 바꿔야 한다. [A066](SOURCES.md#a066) [A144](SOURCES.md#a144)

## Discord 버튼

1. 앱이 만든 메시지에 승인/거절 `custom_id`를 담는다.
2. Gateway 또는 HTTP interactions 중 한 수신 경로를 선택한다.
3. HTTP는 공개키로 `X-Signature-Ed25519`와 timestamp+**원본 요청 바디** 서명을 검증한다. 잘못된 서명은401로 거절한다.
4. 3초 안에 초기 응답/지연 응답 ACK를 하고 실제 작업을 이어간다. interaction token의 후속응답 유효15분은 ‘콘텐츠 승인 만료일’이 아니다.
5. 누른 사용자 ID와 허용 채널/권한을 검증한 뒤 대상 콘텐츠를 승인한다. 게시 작업은 별도 실행한다. [A065](SOURCES.md#a065) [A145](SOURCES.md#a145)

일반 봇/웹훅 API에 승인당 요금표는 확인되지 않았다. 서비스 rate limit은 따르고 응답429/Retry-After를 처리한다. 서버/실행 비용은 별도다. 링크의 GET 방문만으로 게시하면 보안 검사기·미리보기 로봇이 승인할 위험이 있으므로 **GET은 미리보기, 명시적 인증된 POST/명령만 승인**하도록 설계한다.

## Telegram 버튼

`InlineKeyboardMarkup` 버튼에 짧은 `callback_data`를 넣는다(1~64bytes). 업데이트의 사용자/채팅·callback ID를 확인하고 `answerCallbackQuery`로 처리 사실을 응답한다. `getUpdates`의 offset을 저장해 이미 처리한 업데이트를 다시 소비하지 않는다. webhook과 polling은 동시에 쓰지 않는다. webhook을 쓰면 HTTPS와 `secret_token` 헤더 검증을 적용한다. [A067](SOURCES.md#a067)

일반 소규모 봇 알림/응답은 무료 사용 범위이며 유료 대량 broadcast/Stars와 분리한다. 자신의 하루1~2건 승인에 paid broadcast를 켤 이유가 없다. 일반 방송 rate limit과 유료 증설 조건은 [FAQ A143](SOURCES.md#a143)에 있다. `getUpdates`는 public ingress가 없어 로컬 입문에 단순하지만, 대기 프로세스가 켜져 있어야 한다.

## 승인 데이터 설계

다음은 제공 서비스의 필수 스키마가 아닌 최소 설계안이다.

- 승인 대상: 콘텐츠 ID, 최종파일 SHA256, caption/metadata SHA256, **계정·플랫폼·공개범위·AI 표시·예약 시각**, 생성 견적/사용비.
- 승인 기록: 승인자 ID, 승인시각, 만료시각, 단일사용 요청 ID, 결정(approve/reject).
- 검증: 파일/문안/대상 계정/표시/시각이 바뀌면 이전 승인을 무효화한다. 거절·만료·중복 클릭은 발행하지 않는다.
- 미리보기: 이미지 순서·영상/소리·사실·권리·AI/협찬 표시를 검수한다. 승인 메시지에 키·토큰·private 세션 URL을 넣지 않는다.
- 운영: 생성 성공과 승인 성공·게시 성공을 각각 기록한다. 승인 대기 중 네트워크/runner를 무한 유지하지 않는다.

GitHub Actions에서는 파일/상태를 외부에 남긴 뒤 생성 job을 끝내고, 인증된 수동 dispatch로 승인된 해시만 발행하는 방식을 권장한다. Discord 링크에 GitHub token을 넣어 dispatch를 호출하지 않는다. approval HTTP 서비스가 이미 있으면 서명/인증·허용 사용자·재전송 방지를 구현한 뒤 연결한다. A1에서는 구현하지 않았다.

## 유출 때 바로 할 일

1. 파이프라인/예약을 멈추고 **노출된 자격증명을 폐기·재발급**한다. 파일 삭제만 하지 않는다.
2. Meta는 계정의 연결 앱/앱 대시보드에서 권한·토큰을 무효화하고 필요하면 앱 시크릿을 재설정한다. Google은 계정 연결 OAuth 권한을 취소하고 재동의하며 서비스/API 키는 삭제·회전한다.
3. LLM/TTS/저장소 키, Discord webhook URL, Telegram bot token도 각각 revoke/rotate한다. Telegram은 BotFather, Discord는 webhook 삭제/재생성 및 bot token reset 경로를 사용자 콘솔에서 확인한다.
4. 공급자 usage·청구·계정 게시 이력·권한을 점검하고 Secrets/.env를 새 값으로 바꾼다. 로그에 새 비밀이 다시 나오지 않도록 한다.
5. Git에 올라간 비밀은 이력·fork·clone·artifact에 남을 수 있다. **폐기 후** 민감 이력 정리를 검토하고 공동 작업자와 조정한다. 이번 조사에서 Git 이력은 수정하지 않는다. [A075](SOURCES.md#a075) [A107](SOURCES.md#a107) [A108](SOURCES.md#a108) [A068](SOURCES.md#a068)

Meta 데이터 보안 조항은 토큰·앱 시크릿 보호와 보안 사고 대응을 요구한다. 필요한 신고는 해당 약관·대시보드 절차로 확인하며 모든 사고의 통일 기한을 만들어 쓰지 않는다. Google 인증 설정 파일은 Desktop public client라는 특성과 별개로 계정 refresh token·세션 URI와 함께 공개하지 않는다. A2/A6/A9에 반영한다.
