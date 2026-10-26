# 공개 파이프라인 사례·운영 실패

- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/12-pipelines-failures.md` · SHA256 `73f3f6aac81a54422cd180b49c8e3729ce46dffd72bec390454d569eb40ec4af` · exit 1.
- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/12-pipelines-failures-retry.md` · SHA256 `75930c8cddf7bbdb004da4d577cb09818050070e189ee0f2f4182c0577ac8dcb` · exit 1.
- 실행·실패 구분: [provenance.json](provenance.json). 핵심 주장은 Codex 직접 열람/기존 근거와 대조했다.

2026년 10월 조사 기준. 공개 README·템플릿·개발자 포럼을 읽은 분석이며 설치·실계정 게시·비용 벤치마크는 하지 않았다. 저장소의 별 수·제목 속 수익 표현·README 광고를 성공 증거로 쓰지 않는다.

## 재사용할 구조

| 공개 사례 | 입력→출력 구조 | 비용·운영에서 배울 점 |
|---|---|---|
| `gyoridavid/short-video-maker` | 텍스트/검색어 → Kokoro TTS → Whisper 자막 → Pexels 배경 → Remotion 조립 → MP4를 REST/MCP로 제공 | 생성형 영상 없이 조립하는 대안. README는 최소 메모리·동시실행/캐시 축소로 OOM 완화를 설명. GPU/서버·소재 API·의존 라이선스는 별도. **YouTube 업로더 전체가 아님** [A074](SOURCES.md#a074)[A096](SOURCES.md#a096) |
| `harry0703/MoneyPrinterTurbo` | 주제→LLM 대본→TTS·소재/생성 샷→자막·배경음→세로 영상; WebUI/API/CLI | 여러 모델/판매자의 키·과금 경로가 늘어남. README 광고/제휴 가격은 공식 API 정가로 채택하지 않음. ‘영상 생성 완료’와 승인·예약·발행 성공을 분리 [A095](SOURCES.md#a095)[A097](SOURCES.md#a097) |
| n8n ‘human-approved Instagram posts with Gemini, Telegram, and Instagram’ | 입력→Gemini 초안/이미지→Telegram 승인→Meta 게시 | 사람 검수 지점과 reject 분기를 배움. 기여자 카탈로그 설명이며 토큰·공개파일·유료 모델은 사용자 재설정. 월비용/실행 성공 미검증 [A072](SOURCES.md#a072) |
| n8n 포럼 ‘Automate Instagram carousels using n8n, apitemplate and Blotato’ | 폼 문안→API 템플릿 이미지→Sheets URL목록→Gmail 미리보기 승인→Blotato 게시 | 렌더·호스팅·승인·발행을 분리. **대본 AI 사용 안 함**이라고 작성자가 명시. 외부 서비스 구독료 전체를 무료로 추정하지 않음 [A118](SOURCES.md#a118) |
| GPTers 부동산 영상 사례 | Sheets·사진/음악→폴더 필터→병합→Shotstack | 같은 번호의 블로그/영상 폴더 혼동을 분리. 게시/수익 완료 사례로 과장하지 않음 [A093](SOURCES.md#a093) |

저장소 자체 LICENSE는 별도로 확인한다(A156·A157). 코드 라이선스가 Pexels 소재·음성 모델·Remotion·폰트·생성 API의 모든 권리를 대신하지 않는다. 학습 키트에 전체 프로젝트/의존성을 복사하지 않고 필요한 구조만 새로 구현하는 것이 이번 설계 제안이다.

## 실제 질문에서 나온 실패

| 관측/질문 | 실제 근거 | 권장 처리와 과장하지 않을 점 |
|---|---|---|
| 며칠 후 YouTube 인증 실패 | n8n autopilot 채널 질문: 초기 동작 뒤 인증 문제 [A117](SOURCES.md#a117) | Google Testing7일 조건 대조, Production/검증 예외 확인 후 재동의. 포럼 답변을 공식 검증 면제 보장으로 쓰지 않음 [A018](SOURCES.md#a018) |
| Instagram `media is not ready` 뒤403 download/robots 오류 | 2025-12-31~2026-01 스레드 [A116](SOURCES.md#a116) | 고정60초 sleep 하나로 해결했다고 쓰지 않음. `status_code` 폴링·외부 파일 GET·호스트 접근 차단 확인 [A009](SOURCES.md#a009) |
| 유효한 JSON인데 모델/노드 바꾸면 실패 | 2025-02 포럼의 Gemini/OpenAI schema 차이 [A126](SOURCES.md#a126) | 공급자 지원 부분집합·SDK/노드 버전·실제 원응답 분리, 파싱 실패를 무시하고 게시하지 않음 [A026](SOURCES.md#a026)[A029](SOURCES.md#a029) |
| Instagram stories 생성에서 parser/URL 오류 | n8n 사용자 워크플로 질문 [A127](SOURCES.md#a127) | 텍스트·이미지 URL·최종 미디어 파일 단계별 검증. screenshot 속 토큰을 로그로 복사하지 않음 |
| 정각을 피해도 cron 수시간 지연 | 2026-10-04 GitHub Community 질문 [A119](SOURCES.md#a119) | 개별 사용자 관측이며 평균 지연 통계 아님. 공식 schedule 지연/드롭 조건과 연결; 정확한 정시 실행을 보장하지 않음 [A044](SOURCES.md#a044) |
| community node·webhook 때문에 예상 밖 셀프호스팅 | GPTers 사용자 보고 [A094](SOURCES.md#a094) | 과거 당시 환경 제약과 현재 노드 지원을 구별. 처음에는 간단한 로컬 경로부터 |
| nested metrics를 표로 정리하기 어려움 | n8n Instagram Insights 질문 [A153](SOURCES.md#a153) | 미디어 ID·metric·기간·값·단위·조회시각을 행으로 정규화. 오래된 plays/impressions 이름을 현재 지원표로 업데이트 [A109](SOURCES.md#a109)[A110](SOURCES.md#a110) |

## 운영 설계에서 별도로 막을 실패

다음은 발생률을 측정한 사건이 아니라 공식 프로토콜·기존 코드로부터 도출한 회귀 위험이다.

- 생성 API 재시도마다 새 이미지·음성·영상 과금 → 결과 ID/파일 재사용, 요청 전 비용 예약, 최대시도 제한.
- 승인 후 파일/캡션 변경 → 승인 대상 해시와 계정·라벨을 다시 검증.
- 업로드 성공 직후 응답 유실 → 기존 세션/컨테이너/게시물 조회, 새 업로드/발행 금지 우선.
- Instagram 공개 URL이 먼저 만료/삭제 → 다운로드·처리 완료까지 유지, 이후 보존 정책 적용.
- runner가 끝나며 SQLite·세션·승인 파일 소실 → 다음 실행이 읽을 영속 상태 저장 위치 명시.
- ffmpeg에서 한글 자막 네모/필터 누락 → 폰트 권리/경로와 `libass`/코덱 지원 확인, ffprobe+실제 미리보기 검수.
- 분석 API가 빈 데이터 반환 → 0과 missing을 구분하고 재수집, 계정/미디어별 지원 metric 확인.

## 구현자에게 넘길 최소 상태 흐름(제안)

`draft → generated → rendered → awaiting_approval → approved → uploading → published → measured`를 기본으로, `rejected`, `failed`, `unknown_publish_result`를 분리한다. 승인 없는 상태에서 publish로 건너뛰지 않는다. content hash·모델/버전·비용·토큰 만료일·컨테이너/세션/게시 ID·실패단계를 남기되 토큰 값은 저장하지 않는다. 실제 명칭과 JSON/SQLite 선택은 A2에서 정하고 이 조사에서 구현 완료로 표시하지 않는다. A1/A4/A6/A8/A9에 반영한다.
