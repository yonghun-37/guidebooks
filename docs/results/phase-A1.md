# Phase A1 결과 — API 완전 자동화 심화편 자료조사

2026-10-26 · Codex. 조사 산출물 작성·정적 검증 완료. Claude 설계 검수 대기. **계정/유료 API/실제 게시를 검증한 결과가 아니다.**

## 완료한 범위

- AGENTS·pipeline/research 스킬·STYLE-GUIDE·DESIGN-advanced·DESIGN12절·PLAN의 A단계와 기존 API/비용/업로드 조사·두 publish 모듈을 읽고 재사용표를 작성했다.
- `research-advanced/`에 주제 노트10개, 재사용표, BRIEFING, SOURCES137항목, FACT-SHEET84사실, 비용 계산 JSON, 출처 직접확인/원응답 해시 기록을 작성했다.
- 명시된 산출물 예외인 `docs/learner-questions-advanced.md`에 A0~A9 각각5문항, 총50개를 실제 개발자 포럼 문제와 연결했다. 직접 인용/빈도조사가 아닌 편집 질문으로 표시했다.
- 기존 research/·research-shorts/·research-blog/·site*/·*-kit/·설계서·PROJECT_STATE는 수정하지 않았다. 통합 작업자 소유의 상태/사이트는 건드리지 않았다. commit/push하지 않았다.

시작 시 Git에는 다른 작업자의 `docs/learner-questions-blog.md`, `docs/prompts/phase-A2.md`·A3·A4가 untracked였다. 이들을 읽거나 수정하지 않았다. 진행 중 다른 작업자의 변경도 회수/되돌리지 않았다.

## 중요한 결론

1. Meta 신규 통합 권장은 Unified Login. 기존 Instagram Login 본인 학습과 구분한다. Standard Access 검수 면제 표와 앱 생성의 live data 검수 문구는 적용 범위 공백을 남긴다.
2. 인스타100/50 한도와 limit 예제 필드 상충은 유지한다. 계정조회·하루1건 실습·방어적50이하 제안이며 허용 보장 숫자가 아니다.
3. Instagram Login resumable 지원으로 확대하지 않는다. Audio API는 존재하며 Facebook/Unified의Reels 지원, Instagram Login 미지원이다.
4. YouTube 현행은 insert1unit·기본100회/일 전용버킷. 비공개 잠금은 현행 API/도움말 상충. OAuth 검증·API 감사·quota 증설을 분리한다.
5. 현재 PC Studio Shorts 사용자 썸네일과API50MB를 반영한다. 오래된 ‘Shorts프레임만’·‘API2MB’를 반복하지 않는다.
6. OpenAI hard spend limit·Gemini project cap/Prepay를 확인했다. Cloud budget alert는자동정지아님. 이미지 Standard/Batch 혼동을 피하도록 주 비용표를 현행Gemini단가로 통일했다.
7. Imagen4·GeminiVeoPreview·GPTImage1 종료와OpenAISpeechAPI종료예정을 신규실습 설계에 반영해야 한다. 전체Veo/Google영상종료라는 뜻이 아니다.
8. 가상월생성비: 플랫폼별매일1편, 무료음성소진후 저비용합계$0.12·고품질목표합계$8.5875. 추가생성20%허용시$10.305. 사용량/제외비·구독최소청구를 공개했다.

근거·조건은 [BRIEFING](../../research-advanced/BRIEFING.md)과 각 주제 노트, [사실표](../../research-advanced/FACT-SHEET.md)를 따른다.

## Hermes 실행·질의 품질표

- RUN: `/home/yonghun/project/hermes-research/output/advanced-research-20261026`.
- `-Q --provider openai-codex -t web -s guidebook-research --max-turns 40`, 질의당 timeout900초.
- **총14회/상한28회, 최대동시3회.** 최초12회+실패11/12각1회재시도. 더 재시도하거나 런타임/모델/설정을 변경하지 않았다.
- exit0 **11/14**, 공급자오류 **3/14(21.4%)**. 12개주제중Hermes정상결과11개; 사례 주제는 Codex가 직접 보완했다. exit0도 부분추출/검색누락을 인정하므로 완전 성공으로 세지 않는다.
- **빈 원응답(0bytes)0/14.** 오류3개는 각각438bytes이며 조사본문/URL이 없다. 공급자 스트림이 첫 이벤트 뒤12초간 SSE를 보내지 못한 오류다.
- 403 **문자열11회**, Hermes가 실제403을 관측했다고 보고한 응답 **0회**. 각각 ‘403없음/상태코드미제공’ 문맥이었다. `403` 단순검색11을 차단11로 오기하지 않는다.
- `실패표시`는 timeout/blocked/검색실패/접근실패 단어의 기계적수이며 실제차단/도구호출실패건수와 다르다. 추출하위요청의 빈본문 총수는 요약답변만으로 정확히 복원할 수 없어 미집계다.
- URL수도 원응답의 고유URL문자열수이며 직접검증출처수와 다르다. 시간은KST·모두2026-10-26.

| 질의 | 시작 | 종료 | exit | bytes | 403문자열/실제보고 | 실패표시 | URL문자열 | 품질·보완 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 01-instagram-auth | 17:21:18 | 17:25:21 | 0 | 28,847 | 1 / 0 | 0 | 31 | 빈본문/검색0건 인정; Unified·본인학습 분리 |
| 02-instagram-media | 17:21:18 | 17:25:17 | 0 | 19,592 | 1 / 0 | 0 | 18 | 빈참조/생략 인정; Audio API·FB resumable 수정 |
| 03-youtube-quota-audit | 17:21:18 | 17:24:51 | 0 | 16,919 | 1 / 0 | 0 | 15 | 추가추출 timeout; quota/잠금 상충 유지 |
| 04-youtube-fields-analytics | 17:24:51 | 17:30:08 | 0 | 29,595 | 1 / 0 | 0 | 37 | 제목/목차 누락; Codex status/metrics 본문 보완 |
| 05-llm-structured-budgets | 17:25:17 | 17:28:50 | 0 | 26,423 | 1 / 0 | 1 | 43 | 2 URL network/빈본문; hardcap 직접대조 |
| 06-image-video-api | 17:25:21 | 17:30:04 | 0 | 24,740 | 1 / 0 | 0 | 38 | 일부 HTTP/빈본문·모델 셸; 종료/가격 직접대조 |
| 07-tts-korean | 17:28:50 | 17:32:54 | 0 | 22,554 | 1 / 0 | 0 | 38 | 일부 network/생략; 한국어/가격·종료 확인 |
| 08-execution-hosting | 17:30:04 | 17:35:10 | 0 | 30,010 | 1 / 0 | 0 | 38 | 공식문서 부분추출; timezone/GCS무료량 대조 |
| 09-nocode-korea | 17:30:08 | 17:34:32 | 0 | 21,243 | 1 / 0 | 0 | 31 | 동적가격/월결제 일부미확인; 현재표 대조 |
| 10-approval-security | 17:32:54 | 17:37:58 | 0 | 27,386 | 1 / 0 | 4 | 25 | 일부 빈본문/접근실패; 공식수신/서명 보완 |
| 11-platform-policy | 17:34:32 | 17:34:50 | 1 | 438 | 0 / 0 | 0 | 0 | 공급자 SSE 무응답, 조사본문 없음 |
| 12-pipelines-failures | 17:34:50 | 17:35:07 | 1 | 438 | 0 / 0 | 0 | 0 | 공급자 SSE 무응답, 조사본문 없음 |
| 11-platform-policy-retry | 17:37:36 | 17:41:41 | 0 | 21,270 | 1 / 0 | 0 | 24 | 부분본문/발췌 구분; 정책/실제제재 대조 |
| 12-pipelines-failures-retry | 17:37:36 | 17:37:58 | 1 | 438 | 0 / 0 | 0 | 0 | 1회재시도도 SSE실패; Codex 공개원문 직접보완 |

원질의·원응답 전문은 RUN에만 둔다. 저장소의 [provenance.json](../../research-advanced/provenance.json)에 경로·SHA256·실행상태를 기록하고, 주제 노트 머리에도 관련 원응답 경로·해시를 연결했다.

## Codex 직접 확인·재사용

- 직접 GET **161개URL**, HTTP200 **146개**, 오류 **15개**. 실제403은Make옛경로 **1개(A059)**이고 정상경로A131로 보완했다. HTTP상태와 본문확인을 분리했다.
- HTTP200 중 **제목/메뉴만11개**, 미래효력정책1개(A148,11/12효력)는 현행판정에서 제외했다. 현재 Anthropic API지역은A152로 대체했다.
- 출처표에서 **127개를 직접 관련본문 확인/채택**으로 기록했다. 공식API/정책·가격·공급자문서, 원저장소·LICENSE, 개발자포럼·한국사례를 구별한다. 커뮤니티/기여자 성공 주장·매출은 정책/수익 증거로 쓰지 않았다.
- 직접검증은 본문관련절 열람이다. 실제콘솔클릭·API호출·한국카드승인·계정상태의검증이 아니다. 날짜미표기/기존날짜재현불가도 남겼다.
- 기존조사재사용·추가공백은 [00-scope-reuse](../../research-advanced/00-scope-reuse.md), URL상태/본문해시는 [verification.json](../../research-advanced/verification.json)에 있다. HTTP원문은 공개저장소에 복사하지 않았다.

## DESIGN-advanced.md 조정 제안 — Claude가 반영

설계서는 수정하지 않았다. 아래는 조사에 따른 제안이며A2구현을 미리 한 것이 아니다.

1. A0/A5에 로그인 3종 비교를 넣는다. 새 서비스에는 Unified를 권장하고, 본인 계정 키트는 Instagram Login을 사용한다. 호스트·scope·토큰을 섞지 않는다.
2. `hosting/`은 Instagram Login 기본 경로에 필요하다. 영상 직접 업로드는 Facebook 경로의 선택 실습으로 둔다. Pages는 교육용 공개 샘플, r2.dev는 개발용으로 한정하고 R2 운영 도메인·GCS 무료 리전 조건을 설명한다.
3. 공급자는 mock+LLM 1개+TTS 1개부터 구현한다. 모델별 어댑터를 모두 만드는 것보다 필요한 입출력을 먼저 맞춘다. 종료된 Imagen/Veo Preview와 종료 예정 Speech API를 새 기본값으로 고정하지 않는다.
4. 비용 상한과 알림을 분리한다. 공급자 hard cap, 실행별 예상 최대비 예약, 실제 usage 기록, 최대 재시도를 설계한다. Anthropic Default Workspace의 상한 제한과 Cloud budget이 자동 중지가 아니라는 점을 설명한다.
5. 승인 기본은 로컬 파일이다. 모바일 대안은 Telegram polling, Discord는 알림부터 시작한다. incoming webhook만으로 승인 callback이 완성된다고 설명하지 않는다. 파일·문안·계정·표시·예약 시각을 승인에 묶는다.
6. GitHub Actions의 상태 저장 위치를 A2에서 결정한다. SQLite/JSON을 runner 작업 폴더에만 두면 재시작·중복 방지를 충족하지 못한다. 승인을 기다리며 runner를 오래 유지하지 않는다.
7. 업로드에는 결과 불명 상태, 기존 ID 조회, 동일 세션 재개를 둔다. 발행 응답 유실을 새 발행으로 해결하지 않는다. API 일일 한도와 채널 제한을 별도로 기록한다.
8. AI·협찬·음악을 로그인별 기능 표로 나눈다. Audio API를 Facebook/Unified 릴스의 선택 기능으로 설명한다. 한국 카탈로그와 Unified의 페이지 준비 조건은 확인 항목으로 둔다.
9. 분석은 지원 metric·단위·날짜·missing을 명시한다. Instagram 최대 48시간 지연과 YouTube의 마지막 준비 날짜에 맞춰 수집한다. Studio와 즉시 같은 숫자를 성공 기준으로 삼지 않는다.
10. E2E 게이트를 mock 완주, 문서상 요건, 사용자 실계정 검증으로 나눈다. 본인 개발 모드의 게시 가시성·YouTube 잠금·한국 결제·음성 품질은 사용자 실행으로 확인한다. 감사 소요·정시 실행·수익화를 보장하지 않는다.

## 검증과 남은 확인

완료 전 검증 스킬(`superpowers:verification-before-completion`)에 따라 실제 검증 출력을 확인했다. Python 정적 검사에서 다음 항목이 통과했다.

| 검사 | 결과 |
|---|---|
| A번호·앵커·로컬 문서 링크 | 오류 0개 |
| 질문·장 수 | A0~A9 각각 5개, 총 50개 |
| 사실 ID | 84개, 중복 없음 |
| 원질의·원응답 SHA256 | 14쌍 일치 |
| 편당/월 비용 산식·두 문서의 표 | 4개 시나리오 일치 |
| Hermes 상한·병렬 수 | 14≤28, 최대 3 |
| 자격증명 패턴 검사 | 검출 0개 |
| 기존 research/·research-shorts/·두 게시 모듈 | 작업 종료 시 Git diff 없음 |

첫 정적 검사에서는 아직 작성 전인 본 결과 문서로 향하는 링크 1개를 찾았다. 결과 문서를 작성한 뒤 재검사해 해결했다. 진행 중 다른 작업자가 바꾼 사이트·검사 스크립트·별도 결과 문서는 그대로 보존했다.

남은 확인: Instagram 50/100 및 config 실응답, Standard/live data 문구 범위·Creator Story·Unified Audio 요건, YouTube 미검증 잠금과 감사 처리 기간, 한국 UI·카드·모델 접근·TTS 발음, 일부 공급자의 강제 상한·알림 위치, 실제 분석 조합·일정 동작이다. 원고에서는 ‘확인할 점’으로 모으고 사용자가 확인할 위치를 제공한다.

코드 테스트·유료 생성·실업로드·배포는 범위 밖이라 실행하지 않았다. 공통 프로젝트 상태는 통합 작업자가 갱신한다. 이 조사 결과를 A2 구현 완료나 A3/A4 집필 완료로 표시하지 않는다.

## 완료 알림

사용자가 지정한 `python3 scripts/notify.py "✅ [심화편 조사 완료] ..." research-advanced/BRIEFING.md`를 실행했다. **HTTP 200 전송 성공**, BRIEFING 첨부 완료. 메시지는 5줄이며 산출물과 남은 확인 사항을 포함했다. 토큰은 출력하거나 문서에 넣지 않았다.
