# B5 — BlogBook 실습편과 전체 체크리스트

2026-10-26. **집필·로컬 검증 완료, Claude Code 검수·공통 목차 통합 대기.** 기존 결과 문서 관례를 Level 2 구현 기록으로 재사용했다. 실계정 가입·이미지 서비스의 사용자 계정 조작·발행·심사·API live·커밋·배포를 수행한 기록이 아니다.

## 범위와 완료한 결과

- [x] 실습 **0~6·8~10 및 E2E**를 실제 HTML로 집필했다. `site-blog/practice/00-start.html`에서 시작해 본문 끝의 직접 링크로 0→10→E2E를 따라간다.
- [x] 승인된 실습 7은 원고 준비·다음 검색 실습·이전/다음 연결만 바꿨다. 본문·인물·발행 단계·컴포넌트는 유지했다.
- [x] 실습 전용 `assets/practice-workbook.css|js`와 AI 배경 `practice/images/support-background.webp`를 추가했다. 지정된 공통 JS/CSS·표지·용어집·출처·실험실·부록·키트는 수정하지 않았다.
- [x] ChatGPT Free를 기본으로, Gemini·Claude 대안, 네이버 데이터랩·검색광고 키워드 도구·Google Trends, 미리캔버스·Canva, Search Console의 입력 위치·결과 보관·다음 서비스로 넘기기를 안내했다.
- [x] 수아의 ‘퇴근 후 생활 정보’에서 **지원 제도 신청 방법 / 한 달 쓴 생활 가전 후기 / 당일치기 여행**을 이어 썼다. 자료가 없는 경험·수치·정책은 만들지 않고, 실제 글은 본인 자료로 작성하도록 했다.
- [x] 장마다 결과물·시간·따라 하기·성공 기준·문제 해결·FAQ 5개·자동화/무료 대안을 넣었다. E2E는 전체 경로·동일한 체크 15키·총 시간·공개 URL·다음 확인일을 모았다.

## 실습별 구현

| 실습 | 구현과 독자에게 남는 것 |
|---|---|
| 0 | 세 글 유형·필요 자료·무료 조합·플랫폼 선택. Windows/macOS/휴대폰 자료 보관. 제작 90/60분과 전체 준비·발행 시간 구분 |
| 1 | 네이버/티스토리 탭, 주소·이름 구분, 같은 블로그의 비공개 연습 글, 2단계 인증·복구 확인, 비밀번호·인증번호 공유 금지 |
| 2 | 무료 AI 가입·대화 입력·복사·파일 저장, 이미지 도구 준비, 한도 대응, 개인정보 제거, Python 설치 생략 가능 |
| 3 | AI 후보 → 무료 추세 → 계정이 있으면 월간검색수. PC/모바일·지수·표시 없음 구분, 실제 조회 조건과 선택 이유 메모 |
| 4 | 세 유형의 입력 틀·근거표 → 개요 → 초안 → 원문 대조 → 내 경험 → 교정. 복사용 요청문과 같은 크기 수정 전후 비교 |
| 5 | 직접 사진·무료 템플릿·선택 AI 삽화, 실제 생성 배경과 요청문, 제목은 텍스트로 추가, PNG/JPG 보관·대체 설명·권리/AI 역할 메모 |
| 6 | AI의 제한된 교정 → 공식 편집기, 플랫폼별 제목·본문·소제목·사진·링크·태그. 제휴 표시 위치·줄바꿈·모바일·개인정보 점검 |
| 7 | 승인 본문의 앞뒤 연결만 수정. 전체 공개·모바일·URL 기록은 기존 구현 사용 |
| 8 | 네이버 별도 등록 불필요, 외부 사이트 소유확인·URL 접두사·head 태그·티스토리 플러그인·실제 피드·URL 검사. 실패·대기·다음 확인일 |
| 9 | 애드포스트·애드센스·쿠팡/쇼핑커넥트의 신청·검수·정산 구분. 조건 미달/거절도 사유·수정·다음 확인일 기록. 종료된 AdFit 신규 경로 제외 |
| 10 | 첫 7일 지표표와 수동 경로, 선택 Python·샘플 점검·변환·사람 승인·Blogger 드라이런·daily/resume. API 인증 비교·중복 방지 |
| E2E | 0→10 직접 이동, 전체 체크·주소 연동, 정보/후기 130분·경험 100분의 발행 계획과 선택 작업 합산. 실측 시간·대기는 분리 |

시각자료는 플랫폼 분기·작업 위치·초안 전후·이미지 구성·글 구조·검색/신청 상태·키트 파일 흐름에 사용했다. SVG는 직접 그렸고, 실제 서비스 UI·로고를 복제하지 않았다. 소형 화면에서는 비교 카드를 세로로 쌓고 CSS 변수로 두 테마를 지원한다. 주의는 필요한 절의 ‘확인할 점’에 모았다.

## 상태·저장·파일 소유

- 기존 `practice.js`의 `blogbook:practice:v1`에 체크·공개 URL을 저장한다. E2E의 15개 키가 개별 실습과 일치한다. 자동화 생략 시 수동 경로 선택을 기록할 수 있다.
- 추가 작업 메모는 `blogbook:worknotes:v1`에 보관한다. 복사 버튼·저장 차단 안내·수동 복사 대안·메모 별도 삭제를 제공한다. 네트워크 전송은 없다.
- 본문·명시적 이전/다음은 실제 파일을 가리킨다. **공통 book.js의 준비중 상태는 그대로라 사이드바·전체 목차는 통합이 필요하다.** 이를 숨기는 우회 코드는 넣지 않았다.
- [공통 요청 diff](phase-B5-requests.md)에 목차 상태·시간·표지 정적 링크·상태 문서·추가 출처 통합을 남겼다. [용어 후보](phase-B5-glossary.md)에 첫 설명 위치와 정의를 남겼다.
- PROJECT_STATE와 서가 상태는 통합 작업자 소유이므로 수정하지 않았다. B4a/b/c·auto-kit 등 동시에 존재한 다른 작업의 파일은 편집하지 않았다.

## 깨끗한 blog-kit 실제 실행

[실행 원문](phase-B5/kit-run.json). `/tmp/blogbook-b5-ptvym2ws/blog-kit`에 `.venv`·output·.env·auth를 제외하고 새로 복사했다. Linux Python **3.10.12**의 새 가상환경을 사용했고 외부 실행 패키지·API 키를 설치/사용하지 않았다.

실제로 실행한 순서와 본문 성공 문구:

1. `brief.py` → `프롬프트 생성 완료:`와 `brief.md` 경로.
2. `check.py samples/article.md --strict` → **`확인할 항목: 0개`**, **`제목: 27자 / 본문: 1369자(공백 포함)`**.
3. `render.py` → `HTML 생성 완료:`와 `검수 대기:`. 이미지가 복사된 preview.html·editor.html·REVIEW.md를 생성했다.
4. 샘플의 가상 경험을 실제 게시하지 않는 연습으로 검수표를 확인하고 `review.py --approve` → `사람 승인 기록 완료. publish.py는 기본 드라이런입니다.`.
5. `publish.py --platform blogger` → `mode: dry-run`, `state: draft`, endpoint의 **`isDraft=true`**, `authorization: <REDACTED>`와 dry-run.json. 전송하지 않았다.
6. WordPress 드라이런 → `status: draft`; 네이버·티스토리 → `편집기에 붙여 넣기:` 안내.
7. `daily.py --date 2026-10-26` → `작성 대기:`; 같은 날짜 `--resume` → HTML 생성·`검수 대기:`. 자동 작성·승인·발행으로 설명하지 않았다.

실습 10 명령과 발췌 출력은 위 실행에 맞췄다. Windows 명령은 README에 맞춘 안내이며 실기기 실행 성공으로 표시하지 않는다. 키트 코드를 수정하지 않아 pytest를 새로 수행하지 않았고, 이 검증을 키트 전체 회귀 테스트로 소개하지 않는다.

## 실행한 검증

- [담당 원고 문체 검사](phase-B5/style-lint.json): **신규/재집필 11 HTML 모두 통과**, 금지어·내부 용어·단서 반복 0. 신규 실습이라 이론편 축약 비율은 적용하지 않았다.
- [사이트 전체 문체 검사](phase-B5/style-lint-site.json): 검사 시점 **33 HTML 통과**. 동시 작업 이론편의 품질 검수를 대신하는 판정은 아니다.
- [정적 검사](phase-B5/check-site.json): `check_site --site site-blog` **오류 0**, 서가 포함 35 HTML·참조 1,548개·실습 진행 키 15개. B번호 각주는 모두 등록된 출처이고 각주 앵커·그림 제목/캡션·이미지 설명을 검사했다.
- `node --check site-blog/assets/practice-workbook.js` 및 담당 tracked 변경의 `git diff --check` 통과.
- [브라우저 재현 코드](phase-B5/verify-browser.mjs)·[결과 JSON](phase-B5/browser-check.json): **12 실습 페이지 × 1280/375/360px × 라이트/다크**, **1,397개 확인**, 내부 링크 **291개**, 가로 넘침·콘솔·페이지·내부 HTTP 오류 **0**.
- 탭 전환·패널 표시·End/Home/좌우 화살표, 목차 Enter/Escape, FAQ Enter, 체크 Space, 프롬프트 Enter 복사, 개별 실습↔E2E 체크/주소 복원·삭제, 메모 복원·별도 삭제를 확인했다.
- JS 없는 원고·플랫폼 안내·명령 읽기, 저장 차단 시 입력·체크 유지와 안내, 클립보드 차단 시 수동 선택 대안, AI 이미지 실제 로딩을 확인했다.
- 초기 검사에서 AI 이미지의 원본 폭으로 생긴 넘침을 발견해 실습 전용 이미지 max-width로 수정했다. 수정 후 전체 브라우저 검사를 통과했다.

재현: 저장소 루트에서 `python3 -m http.server 8627 --bind 127.0.0.1`, 다른 터미널에서 `node docs/results/phase-B5/verify-browser.mjs`. 기존 환경의 Playwright/Chromium 경로를 사용한다.

스크린샷은 [phase-B5/](phase-B5/)에 **86장**이다. 대표 화면:

- [시작 375 라이트](phase-B5/00-start-375-light.png)
- [키워드 360 다크](phase-B5/03-keywords-trend-360-dark.png)
- [초안 비교 1280 라이트](phase-B5/04-draft-compare-1280-light.png) · [360 다크](phase-B5/04-draft-compare-360-dark.png)
- [이미지 배치 비교 1280 라이트](phase-B5/05-images-compare-1280-light.png) · [AI 배경 1280 라이트](phase-B5/05-images-ai-image-1280-light.png)
- [글 구조 360 다크](phase-B5/06-editor-disclosure-360-dark.png) · [Blogger 드라이런 360 다크](phase-B5/10-automation-dry-run-360-dark.png)

대표 화면을 실제 이미지로 열어 글자·여백·구조·테마·삽화·표시 위치를 점검했다. 외부 서비스의 계정 화면이나 Windows/macOS·실제 휴대폰 성공을 의미하지 않는다.

## AI 이미지 제작 기록

자산: [support-background.webp](../../site-blog/practice/images/support-background.webp), **1672×941, 24,866 bytes**. 내장 `image_gen` 도구로 생성했다. API 키·CLI·결제를 사용하지 않았다. 생성 PNG를 Chromium canvas로 **형식만 WebP로 변환**했으며 내용은 편집하지 않았다. 본문에는 AI 생성 예시·한국어 요청문·배경을 저장해 디자인 도구로 넘기는 방법이 있다.

실제 생성 요청문:

> Use case: illustration-story. Asset type: Korean beginner blogging textbook, example thumbnail BACKGROUND to teach a learner how to add a separate text layer. Primary request: a clean flat editorial illustration of a blank paper checklist and a closed plain folder on a desk. Muted purple and cream palette. Landscape composition, subjects on right half and generous clean empty space on left for a future heading. No writing anywhere: no text, letters, numbers, logos, brands, people, money, fake official seals, application forms, interface, or watermark. This is a conceptual illustration for an article on checking official support-program notices before applying, never a documentary photo or evidence of an actual application. Opaque cream background.

## 남은 확인

1. Claude Code의 내용 검수와 [공통 요청](phase-B5-requests.md) 적용: 목차·표지·출처·용어집·PROJECT_STATE·서가를 통합한다. 공통 목차에 ‘준비중’이 남는 것은 현재 소유 규칙에 따른 통합 잔여 작업이다.
2. 추가로 직접 확인한 보안·대화 조작 안내 세 건은 요청 문서에 URL·실제 확인 범위를 보존했다. 본문에는 직접 공식 링크로 제공하며 등록 전 B번호를 만들어 쓰지 않았다.
3. 외부 서비스의 현재 로그인 후 세부 배치·모바일 제약·소유확인·광고 신청/정산·실제 게시, Windows/macOS 설치·예약·실계정 OAuth는 실행하지 않았다. 변경되는 메뉴는 공식 도움말과 현재 화면을 확인하도록 안내했다.
4. 공개 저장소의 최종 blog-kit ZIP/README와 통합 배포 확인, 커밋·push·배포는 후속 작업이다. 본 작업에서는 하지 않았다.

완료 알림: `scripts/notify.py`로 대표 이미지 배치 비교 화면을 첨부해 디스코드 전송 **HTTP 200**을 확인했다. 메시지는 한국어 5줄로 정리했다.
