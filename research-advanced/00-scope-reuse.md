# A1 조사 범위와 기존 근거 재사용

2026년 10월 조사 기준 · 컷오프/접근일 2026-10-26. 이 폴더는 심화편 구현·집필에 넘기는 조사 기록이다. 서비스 가입·결제·실계정 로그인·게시·감사 신청은 하지 않았다.

## 조사 결정

| 기존 근거·코드 | 재사용한 내용 | 이번에 채울 공백 |
|---|---|---|
| `research/graph-api-publishing.md`, `r2-api-limits.md` | 로그인별 계정·권한, JPEG, 컨테이너 상태, 50/100 상충 | Unified 권장과 학습 경로 구분, 현행 resumable 지원 범위, 오류·인사이트 |
| `research/practice-instagram.md` | 앱 역할·토큰 생성기·공개 URL·개발 모드의 확인 공백 | 생성 화면과 Standard Access 예외의 관계, 업로드 대안 |
| `research/ai-production.md`, `ai-models-pricing.md` | 제작 단계·한국어/권리 판단, 공급자별 모델과 가격 | 구조화 출력·종료 API·강제 지출 한도, 편당 계산 |
| `research/nocode-pipelines.md`, `scheduling-automation-tools.md` | 승인 템플릿·커넥터와 API 자체 요건 구분 | 현행 요금·노드 기능·스케줄 영속 상태·한국 사례 |
| `research-shorts/13-api-quota-audit.md`, `14-oauth-setup.md` | 2026 granular quota, 비공개 잠금 상충, Testing 7일 | 공식 본문 재대조, 감사 양식, 상태 필드·Analytics |
| `research-shorts/01-specs-feed.md`, `05-ai-disclosure.md`, `11-upload-desktop.md`, `15-analytics.md` | Shorts 분류·AI 공개·업로드와 분석의 차이 | API 지표 이름·지연·썸네일 제약 |
| `starter-kit/publish.py` | Instagram Login·v26.0·URL 방식·컨테이너→폴링→발행·AI 필드·기본 드라이런·승인 | 현행 한도 조회·갱신·지속 상태/재개는 후속 설계; 기존 코드 수정 안 함 |
| `shorts-kit/upload.py` | 로컬 OAuth·재개 업로드·256KiB 배수·308 Range·세션/파일 해시·기본 private·합성 공개 필드 | 매일 운영의 토큰 수명·일정·분석과 비용; 기존 코드 수정 안 함 |

기존 조사에 이미 답이 있는 기초 질문을 Hermes에 반복하지 않았다. 상충·중요 변경은 기존 결론을 입력으로 주고 **차이 확인**을 요청했다. 이전 기록은 이전 기록으로 인용하고, 새 A번호는 이번 확인 수준을 독립적으로 기록한다.

## 근거와 편집 제안의 구분

- A###: 외부 출처. [SOURCES](SOURCES.md)에 기관·날짜·확인 수준을 둔다.
- ADV-###: 검증 가능한 주장. [사실표](FACT-SHEET.md)에 장과 판정을 연결한다.
- 추천 조합·승인 해시·재시도 정책·예산 가정은 **편집/설계 제안**이다. 외부 서비스가 제공하는 기능처럼 쓰지 않는다.
- 공식 본문을 수신해도 소개·탐색 메뉴뿐이면 본문 검증으로 세지 않는다. 실패 URL은 출처표에 남긴다.
- 날짜가 없는 문서에 접근일을 갱신일로 대입하지 않는다. 최신 문서의 과거 변경 항목도 시행일과 구별한다.

## 파일 소유

이번 작업은 `research-advanced/`, `docs/results/phase-A1*.md`와 명시된 산출물 `docs/learner-questions-advanced.md`만 작성한다. 마지막 파일은 사용자 산출물 목록의 명시적 예외로 취급한다. 공통 상태·설계서·사이트·기존 조사·키트는 수정하지 않는다. 설계 조정안은 결과 문서에 둔다.
