# Phase E-insta — ReelsBook 예시 전면 교체

2026-10-26 완료. 기준은 `docs/STYLE-GUIDE.md` 7절 예시 원칙과 6절 시각자료다. [교체 전 전수 목록](phase-E-insta-before.md), [검증·스크린샷](phase-E-insta/), [재현 명령](phase-E-insta/commands.md)을 함께 보관한다.

## 최종 예시와 선택 이유

가상 계정은 **출근길 3분 생활 뉴스**, 대표 콘텐츠는 **청년 지원금, 신청 전 확인할 3가지**다. 대상·기간·서류 확인이라는 독자 질문을 기획 → 원문 대조 → 카드 5장 → 15초 모션 → 30초 해설 → AI 도시 배경 → 검수·게시 → 저장·공유 해석으로 연결했다.

“다음 달부터 바뀌는 제도”는 시행일·현행 요건을 확정해야 하는 제목이다. 기존 research에는 공공자료의 일반 이용 조건은 있지만 특정 지원 공고의 현행 요건과 개별 이용 표식을 확정한 근거가 없다. 사용자가 허용한 대안에 따라 **직접 작성한 예시 문안**으로 형식을 보여 주었다. 실제 제도명·금액·마감일을 만들지 않았고, 특정 공공기관이 작성·승인한 카드처럼 표시하지 않았다. 실제 게시에는 독자가 확인한 원문으로 교체하도록 안내한다.

공공누리 관련 근거는 기존 `research/music-assets-licensing.md`의 ASSET-03, `research/news-sources.md`의 NEWS-05, `research/FACT-SHEET.md`, `research/SOURCES.md`의 S128이다. [경기도교육청 공식 안내](https://goe.go.kr/goe/cm/cntnts/cntntsView.do?cntntsId=1046&mi=10092)를 직접 다시 열어 제1유형의 출처 표시·상업 이용·변경 허용과 기관·작성연도·표시된 작성자·URL을 포함하는 출처 작성 항목을 확인했다. 본문·README에는 이를 S128 각주와 공식 링크로 연결했다. 실제 공고·첨부 사진은 이번 샘플에 전재하지 않았다. `example.invalid`는 원문을 채울 자리라고 명시했다.

## 변경한 내용

- `site/index.html`, 이론·실습, `prompts.html`, `ai-models.html`, `lab.html`, JS 기본 문안·검수 사례·달력 데이터를 같은 생활 뉴스 주제로 연결했다. 좋은/나쁜 요약·카드 비교와 퀴즈 해설도 대상·기간·서류와 “자동 지급 아님”으로 맞췄다.
- 기획 시트의 계정 이름·소개와 실제 앱 입력 예, 원자료·카드 문안·낭독문·캡션 프롬프트를 일치시켰다. 30초 해설의 낭독문에는 확인 순서와 저장할 이유를 넣었다. 실제 30초 음성 파일이나 외부 서비스 생성 영상을 제작한 것으로 서술하지 않는다.
- 이미지·영상 프롬프트는 종이 캐릭터 대신 출근길 도시·열차 창밖 장면으로 바꿨다. 같은 참조 이미지에서 빛 변화·느린 전진·하늘로 기울이기를 각각 독립 클립으로 생성하는 연습이다. 기존 모델·크레딧·가격·출력 수 계산은 유지했다.
- 기존 수익 산수·정책·모델 표·출처 링크·입력 조건·진행 키·퀴즈 정답 플래그를 보존했다. 20초 시간 편집 시뮬레이터와 키트 기본 설정도 유지한다. 대표 샘플·서비스 실습의 15초 목표와 구별해 표기했다.
- 키트는 `fixtures/sample-feed.xml`, `config.example.yaml`의 계정명, `prompts/`, 문안 생성·카드 렌더러의 **문자열 상수만** 바꿨다. 승인·게시·보안·수집·영상·음성 로직은 변경하지 않았다. 샘플 전환 시점 검사는 15초÷5장면인 3초로 조정했다.

## AI 이미지와 실제 샘플

내장 이미지 생성 도구로 새 이미지 2장을 만들었다. 유료 API 키·외부 과금을 사용하지 않았다. 두 이미지 모두 직접 열어 사람·브랜드·텍스트·실제 명소가 없고 자막 여백이 있는지 확인했다.

| 파일 | 용도 | 규격·크기 |
|---|---|---|
| `site/assets/img/ai-examples/commute-card.webp` | 카드 배경·샘플 표지 | 960×1200, 132,242바이트 |
| `site/assets/img/ai-examples/commute-reel.webp` | 같은 주제의 릴스 시작 프레임 | 720×1280, 61,940바이트 |

각각 400KB 이하이며 figure·의미 있는 alt·AI 생성 예시 캡션·프롬프트·lazy/치수를 제공한다. 실제 생성 도구에 넣은 전체 지시문은 [이미지 제작 기록](../../site/assets/img/ai-examples/README.md)에 있다. 쓰이지 않는 `library-evening.webp`를 삭제하고 크레딧을 갱신했다. 카드 배경은 키트 `samples/commute-card.webp`에도 동봉했다.

[키트 샘플 README](../../starter-kit/samples/README.md)의 절차대로 깨끗한 임시 복사본에서 기본 생성 → 문안 편집·15초/색 설정 → 구조 검증 → 재생성을 실행했다. `news.json`, `copy.json`, PNG 5장, MP4, SRT를 키트와 사이트 사본에 함께 반영했다. 실제 영상은 **1080×1920·24fps·360프레임·15초·H.264/AAC·무음**이다. 전체 키트 샘플은 약 1.8MB다. 카드·캡션에 직접 작성 예시임을 표시하고 AI 배경 고지·플래그를 유지했다. `synthetic: true`와 live 차단은 그대로다. 산출물은 검수 대기에서 멈췄다.

## 검증 결과

| 검사 | 결과 |
|---|---|
| style_lint | 기존 고정 기준선 25파일 + 기타 8파일 통과. 금지어·내부 용어 0, 이론 분량 조건 통과 |
| check_site(site) | 40 HTML(서가 포함), 내부 참조 3,436, 도구 31, 진행 키 43, 퀴즈 57. 오류 0 |
| Chromium 전체 검사 | ReelsBook 38 HTML × 1280/375/360px × 라이트/다크, 1,188항목 통과. 가로 넘침·콘솔·페이지·로컬 HTTP 오류 0 |
| 실제 조작 | 6개 화면 조건에서 카드 기본/넘침/작게 보기, 자막 복구·프레임 이동, 검수 증거·수정·판정 91항목 통과 |
| 내용 보존 | 149항목 통과. 기존 앵커·각주·공식 링크·입력/저장·정답 플래그·모델 표·계산·게시 차단 로직 유지 |
| 키트 pytest | **116 passed in 25.58s**. 네트워크 차단·모킹, 실제 미디어 디코딩·모션·무음·합성 live 거부 포함 |
| 남은 인위적 예시 | `site/`, `starter-kit/` 검색 0건. 설치·캐시·기존 실행 출력은 제외 |
| Git 공백 검사 | 요청 범위 `git diff --check` 통과 |

스크린샷 90장을 저장했다. 대표 화면: [360px 카드 비교](phase-E-insta/site-chapters-07-cards-visual-card-compare-360-light.png), [다크 요약 비교](phase-E-insta/site-chapters-06-writing-visual-summary-compare-1280-dark.png), [375px 다크 AI 장면](phase-E-insta/site-chapters-08-reels-figure-375-dark.png). 실제 PNG 3종(표지·본문·마무리)과 대표 브라우저 이미지를 직접 열어 확인했다.

기계 판독 결과는 `check-site.json`, `style-baseline.json`, `style-other.json`, `browser-check.json`, `interaction-check.json`, `content-preservation.json`, `sample-audit.json`, `pytest.txt`에 있다. 시작 시점 파일 해시·구 예시 위치 목록도 함께 남겼다.

## 범위와 남은 확인

수정은 `site/`, `starter-kit/`, 사용자가 지정한 `docs/results/phase-E-insta*`로 제한했다. PROJECT_STATE·설계·스타일 가이드·research·생성 스크립트·서가·쇼츠는 수정하지 않았다. 다른 작업자가 변경 중인 파일도 보존했다. 새 ADR·중복 기능 문서는 만들지 않았다. commit/push하지 않았다.

남은 일은 Claude Code의 최종 검수·커밋·배포다. 실제 지원 공고를 공개 콘텐츠로 만들 때의 최신 요건·개별 이용 표식 확인과 실제 계정 앱 조작은 사용자 단계로 남는다. 실제 로그인·게시·결제·OS 실기기 검증은 수행하지 않았다.

요청한 디스코드 완료 알림을 새 카드 표지 PNG와 함께 전송했다. `scripts/notify.py` 응답 HTTP 200을 확인했다.
