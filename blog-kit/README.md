# 수아의 첫 블로그 글 만들기

**본인 자료 → 복사용 프롬프트 → 사람 작성 → 초안 검사 → HTML → 사람 승인 → 발행 요청 미리보기**를 만들어요. Python 3.10 이상이면 추가 프로그램·계정·API 키 없이 오프라인으로 끝낼 수 있어요. 실행용 패키지 설치는 없어요. AI 서비스에 붙여 넣기는 선택이며, 인터넷이 없으면 같은 순서로 직접 쓰세요.

가상 블로그 **‘퇴근 후 생활 정보’**의 대표 소재는 ‘청년 직장인 지원 제도, 신청 전에 어디부터 볼까’예요. 실제 제도·지원금·신청 자격을 지어내지 않고 공식 공고를 확인하는 글이에요. [샘플 글](samples/article.md)과 [완성 미리보기](samples/rendered/preview.html)를 먼저 열어 보세요. 수아의 경험은 가상 편집 연습이며 본인의 체험담으로 게시하면 안 돼요.

## 1. 폴더와 Python 준비

터미널은 명령을 글자로 입력하는 창이에요. Windows는 시작 메뉴에서 PowerShell을, macOS는 Spotlight에서 터미널을 여세요. 화면은 기기·버전마다 조금 달라요.

| 하는 일 | Windows PowerShell | macOS / Linux | 이렇게 보이면 성공 |
|---|---|---|---|
| Python 확인 | `py -3 --version` | `python3 --version` | `Python 3.10` 이상 |
| 키트 폴더로 이동 | `cd "C:\blog"` | `cd "/Users/내이름/Downloads/guidebooks-main/blog-kit"` | 실제 압축을 푼 경로로 바꾸고 다음 줄에 오류가 없어요 |
| 폴더 확인 | `dir` | `ls` | `brief.py`, `daily.py`, `samples`가 보여요 |
| 가상환경 만들기 | `py -3 -m venv .venv` | `python3 -m venv .venv` | 폴더 안에 `.venv`가 생겨요 |
| 사용할 Python 확인 | `.venv\Scripts\python.exe --version` | `.venv/bin/python --version` | `Python 3.10` 이상이 보여요 |

가상환경은 이 폴더에만 프로그램을 담는 상자예요. **아래 모든 `python`은 Windows에서 `.venv\Scripts\python.exe`, macOS/Linux에서 `.venv/bin/python`으로 바꿔 실행하세요.** 활성화나 PowerShell 보안 설정 변경은 필요 없어요. Python이 없다면 [공식 다운로드](https://www.python.org/downloads/)에서 준비하세요. 키트는 시스템 패키지를 설치하지 않아요. Windows 예약 실습을 할 때는 `C:\blog`처럼 짧은 폴더를 권해요.

## 2. 먼저 샘플로 끝까지 연습하기

코드 블록의 명령만 복사해 Enter를 누르세요. 아래 경로는 모두 `blog-kit` 폴더 기준이에요. 각 명령은 AI·블로그 서버에 접속하지 않아요.

```bash
python brief.py --keyword "청년 직장인 지원 제도 신청 전 확인할 것" --type 정보 --platform naver --output output/practice/brief.md
```

**이렇게 보이면 성공:** `프롬프트 생성 완료:` 뒤에 `brief.md` 경로가 보여요. 파일을 메모장으로 열면 검색 의도·질문 → 개요 → 초안 → 사실 확인 요청 → 제목 3안 → 요약·FAQ → 썸네일 프롬프트가 있어요. ‘후기’는 실제 사용 메모·제공 관계를, ‘경험’은 본인의 상황·행동·결과를 넣어요. `--notes materials.md`를 추가하면 직접 준비한 로컬 메모도 각 프롬프트에 들어가요. 개인정보를 먼저 빼세요.

```bash
python check.py samples/article.md --output output/practice/report.md --strict
```

**이렇게 보이면 성공:** `확인할 항목: 0개`, `제목: 27자 / 본문: 1369자`가 보여요. 샘플에 자동 점검 수정 후보가 없다는 뜻이에요. 실제 사실·경험·권리의 확인은 사람이 해요.

```bash
python render.py samples/article.md --output output/practice/article
```

**이렇게 보이면 성공:** `HTML 생성 완료:`와 `검수 대기:`가 보여요. `output/practice/article/preview.html`을 더블 클릭하면 모바일 폭의 글과 순서도가 열려요. 이미지 파일도 출력 폴더의 `assets/`로 복사돼요.

| 파일 | 무엇에 쓰나요? |
|---|---|
| `draft.md` | 출력 폴더에 복사된 초안. 이후 수정할 본문 |
| `editor.html` | HTML 모드를 지원하는 편집기에 넣을 본문 조각 |
| `preview.html` | 브라우저에서 읽고 복사할 미리보기 |
| `report.md` | 자동 점검 결과 |
| `REVIEW.md` | 사람이 확인할 검수표·출처/경험/권리/AI 사용/관계/공개 URL 메모 |
| `render.json`, `config.snapshot.json` | 변환 파일의 변경 감지·설정 기록 |

`REVIEW.md`를 열어 다섯 항목을 읽고 직접 확인한 뒤 `[ ]`를 `[x]`로 바꿔 저장하세요. 이 연습의 ‘경험’ 확인은 **가상 글임을 이해하고 실제 게시에 쓰지 않는 것**이에요.

```bash
python review.py output/practice/article --approve
```

**이렇게 보이면 성공:** `사람 승인 기록 완료.`가 보이고 `APPROVED.json`이 생겨요. 확인 표시가 빠지면 오류로 멈춰요.

```bash
python publish.py output/practice/article --platform blogger
```

**이렇게 보이면 성공:** `"mode": "dry-run"`, `"state": "draft"`, `isDraft=true`, `"authorization": "<REDACTED>"`가 보여요. `dry-run.json`에도 요청 내용이 저장돼요. 서버 전송은 없고 `.env`나 인증 파일도 읽지 않아요. `<BLOG_ID>`는 사용자가 넣을 자리예요.

```bash
python publish.py output/practice/article --platform wordpress
```

**이렇게 보이면 성공:** 요청 본문에 `"status": "draft"`가 보여요. `https://example.invalid`는 실제로 접속하지 않는 예시 주소예요. WordPress 드라이런도 오프라인이에요.

## 3. 내 글을 매일 이어 쓰기

다음은 고정 연습 날짜예요. 내 작업은 `--date`를 빼면 컴퓨터의 오늘 날짜로 만들어요.

```bash
python daily.py --date 2026-10-26
```

**이렇게 보이면 성공:** `작성 대기:`와 `output/daily/2026-10-26/draft.md`가 보여요. `brief.md`, `materials.md`, `daily-config.json`도 생겨요. 같은 날짜를 다시 만들면 기존 파일을 보호하며 멈춰요.

`materials.md`에 공식 출처·실제 경험·이미지 권리·AI 사용 범위·제공 관계를 적으세요. `brief.md`를 보며 직접 쓰거나, 사용할 수 있는 AI 서비스에 한 단계씩 넣고 답변을 검수하세요. 최종 본문은 `draft.md`에 저장해요. HTML을 붙이는 파일이 아니라 `# 제목`, `## 소제목` 형태의 Markdown 파일이에요.

```bash
python daily.py --date 2026-10-26 --resume
```

**이렇게 보이면 성공:** 같은 날짜 폴더에 `editor.html`, `preview.html`, `report.md`, `REVIEW.md`가 생기고 `검수 대기:`에서 멈춰요. `--resume`은 AI 호출·승인·발행을 하지 않아요. 실제 제휴 링크가 있다면 `--affiliate`를 함께 넣으세요.

리포트를 읽고 수정할 때는 이 폴더의 `draft.md`를 고친 뒤 같은 `--resume` 명령을 다시 실행하세요. **재변환은 이전 승인과 검수 체크를 지워요.** 다시 미리보기를 열고 검수표를 채운 뒤 `review.py 폴더 --approve`와 `publish.py 폴더`를 차례로 실행하세요. 승인 이후 초안·HTML·리포트·이미지·검수표가 달라져도 전송을 멈춰요.

키워드·유형·플랫폼·점검 기본값을 바꾸려면 `config.example.json`을 같은 폴더의 `config.json`으로 복사하고 편집하세요. JSON은 이름과 문자열을 큰따옴표로 감싸는 설정 형식이에요. 쉼표를 유지하세요. 새 일일 작업은 변경한 설정을 쓰고 기존 작업은 생성 당시 `daily-config.json`을 써요.

| Windows | macOS / Linux | 이렇게 보이면 성공 |
|---|---|---|
| `Copy-Item config.example.json config.json` | `cp config.example.json config.json` | `config.json`이 생겨요 |

## 4. 점검 결과를 읽는 법

제목·본문은 **공백 포함 문자 수**로 세고, 이미지 주소·링크 주소는 글자 수에서 빼요. 제목·본문 길이, 소제목 개수, 반복 문장 최소 길이, 상투 표현과 제휴 링크 탐지 목록은 모두 **키트 기본값(바꿀 수 있음)**이에요. 검색 순위나 광고 승인에 필요한 숫자가 아니에요. `config.example.json`의 `rules`와 `rule_basis`를 보세요.

- 제목 하나, 소제목 단계, 본문 길이, `![내용 설명](이미지)`의 대체 텍스트를 점검해요.
- 제휴 링크가 보이면 **본문 첫 문단**의 수수료·제공 관계를 확인해요. 알려지지 않은 짧은 링크는 놓칠 수 있고 `naver.me` 같은 링크는 오탐할 수 있어요. 실제 관계를 직접 판단하고 `--affiliate`로 알려 주세요. 무료 제품·원고료처럼 링크 없는 관계도 사람이 확인해요.
- 숫자 문장과 **같은 줄**에 `[출처: 원문URL | 확인일 | 해당 근거]` 또는 `[내 기록: 관찰일 | 실제 관찰 내용]`을 적어요. 메모의 존재를 검사하며 URL 진위·숫자 정확성은 대조하지 않아요. 여러 문장이 한 줄에 있으면 해당 줄의 모든 숫자가 메모로 설명되는지 사람이 확인하세요.
- 같은 문장·상투 표현을 알려 주고, `## 내 경험` 아래에 내용이 있는지 확인해요. 문단의 존재와 실제 경험인지는 달라요. 정보 글에서는 공고를 찾아본 실제 과정도 적을 수 있어요.

광고 표시의 근거는 [조사 노트](../research-blog/08-policy-copyright.md)와 [공정위 추천·보증 심사지침](https://www.law.go.kr/LSW/admRulInfoR.do?admRulSeq=2100000280130&chrClsCd=010201)이에요. **2026년 10월 조사 기준**, 지침은 제목 또는 첫 부분을 허용하며 키트는 본문 첫 문단을 기본으로 정했어요. 두 곳에 모두 적어야 한다는 뜻이 아니에요. 실제 프로그램의 안내 문구와 관계에 맞춰 분명하게 표시하세요.

`check.py`는 수정 후보가 있어도 기본 종료 코드가 0이에요. 위 연습처럼 `--strict`를 넣으면 수정 후보가 있을 때 코드 2로 끝나요. 파일/설정 오류는 코드 1이에요. 사람 승인은 자동 검사 개수와 관계없이 모든 리포트 항목을 검토해야 해요.

## 5. 편집기에 옮기고 직접 발행하기

```bash
python publish.py output/practice/article --platform naver
```

**이렇게 보이면 성공:** `편집기에 붙여 넣기:` 안내가 보여요. 티스토리는 `--platform tistory`로 바꾸면 같은 안내가 나와요.

네이버·티스토리는 [공식 글쓰기 API가 종료](../research-blog/07-api-automation.md)되어 이 키트에서 API 발행을 하지 않아요. `preview.html`을 브라우저에서 열고 글을 선택해 편집기에 복사하세요. 편집기가 HTML 모드를 지원하면 `editor.html`의 내용도 쓸 수 있어요. 제목은 제목 칸에 따로 넣고 본문 제목이 중복되면 지우세요. **로컬 이미지는 편집기에서 직접 다시 올리고**, 소제목·대체 텍스트·링크·광고 문구를 확인하세요. 복사만으로 플랫폼 서식·사진 전송이 완성되지는 않아요.

내 실제 자료로 쓴 글을 직접 발행한 뒤 공개 주소와 공개 상태를 `materials.md` 또는 `REVIEW.md`의 메모에 적으세요. 검수표를 고쳤다면 이후 API 연습 전에 다시 승인해야 해요. 가상 샘플은 발행하지 마세요.

## 6. 선택: API로 내 초안 저장하기

**API도 기본은 드라이런이며, `--live`를 붙여야 네트워크 쓰기가 생겨요.** 키트는 초안 저장만 제공해요. 실제 공개는 관리 화면에서 내용을 확인한 뒤 직접 하세요. [API 조사 노트](../research-blog/07-api-automation.md), [Blogger insert](https://developers.google.com/blogger/docs/3.0/reference/posts/insert), [WordPress 글 API](https://developer.wordpress.org/rest-api/reference/posts/)를 참고하세요.

먼저 본인 자료로 새 글을 만들고 변환·검수·승인을 끝내세요. **가상 연습용 표시가 있는 동봉 샘플의 live 실행은 차단해요.** API는 로컬 사진 업로드를 하지 않으므로 사진은 권리·호스팅을 확인한 HTTPS 주소로 바꾸고 재변환·재승인하세요. 편집기에서 사진을 올리는 수동 경로를 써도 돼요.

| 대상 | 사용자가 직접 준비할 것 |
|---|---|
| Blogger(기본) | 본인 Google Cloud 프로젝트에서 Blogger API 활성화, OAuth 동의·테스트 사용자/클라이언트 설정, 본인 동의로 발급한 `https://www.googleapis.com/auth/blogger` 범위의 액세스 토큰, 쓰기 권한이 있는 블로그의 숫자 ID |
| 설치형 WordPress(심화) | 본인이 관리하는 HTTPS 사이트, 글 작성 권한, 사용자 프로필에서 만든 도구 전용 **애플리케이션 비밀번호** |
| WordPress.com | 별도 OAuth API 방식. 이 키트의 설치형 Basic 인증 연결로 사용하지 않아요 |

Blogger 토큰은 API key와 달라요. [공식 시작 안내](https://developers.google.com/blogger/docs/3.0/getting_started)의 인증 절차를 따르세요. 이 키트는 OAuth 토큰 발급·갱신을 자동화하지 않아요. WordPress는 [애플리케이션 비밀번호 안내](https://developer.wordpress.org/advanced-administration/security/application-passwords/)에서 본인 프로필의 기능 사용 가능 여부를 확인하세요. 주 로그인 비밀번호를 넣지 마세요.

| Windows | macOS / Linux | 이렇게 보이면 성공 |
|---|---|---|
| `Copy-Item .env.example .env` | `cp .env.example .env` | `.env` 파일이 생겨요 |

`.env`는 인증용 비밀값을 보관하는 로컬 텍스트 파일이에요. 필요한 플랫폼 항목만 직접 채우세요. Blogger는 `BLOGGER_BLOG_ID`와 `BLOGGER_ACCESS_TOKEN`, WordPress는 `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`를 사용해요. 토큰을 명령줄·초안·설정 JSON에 적지 마세요. JSON 인증 파일이 있다면 `auth/`에 보관하고 `BLOGGER_TOKEN_FILE=auth/token.json`을 쓰세요. `access_token` 또는 `token` 필드만 사용해요. live에는 직접 준비한 `.env` 파일이 있어야 해요. 환경변수가 `.env`보다 우선하고, 파일을 지정하면 파일 토큰이 우선해요. `.env`는 셸 명령으로 실행하지 않아요.

다음의 `output/my-article`은 **본인 글을 변환·승인한 실제 폴더**로 바꾸세요. 둘 중 본인의 플랫폼 하나만 실행하세요.

```bash
python publish.py output/my-article --platform blogger --live
```

**이렇게 보이면 성공:** `초안 저장 완료.`가 보여요. `LIVE_ATTEMPT.json`의 글 ID로 Blogger 관리 화면에서 초안과 중복 여부를 확인하세요.

```bash
python publish.py output/my-article --platform wordpress --live
```

**이렇게 보이면 성공:** 같은 완료 문구와 글 ID가 생겨요. WordPress 관리 화면에서 초안인지 확인하세요.

응답 오류·시간 초과가 나면 `LIVE_ATTEMPT.json`을 유지하며 같은 폴더에서 재전송하지 않아요. 이미 저장됐을 수 있으니 관리 화면부터 확인하세요. 기록을 지워 반복 실행하지 마세요. 401은 인증·토큰 만료, 403은 권한·API 설정·호스팅 제한을 확인하세요. 리다이렉트는 따라가지 않으므로 `WP_URL`에 최종 HTTPS 주소를 넣으세요. 응답 전문·토큰은 출력·로그에 남기지 않아요. `.env`, `auth/`, 토큰 파일과 실제 `output/`은 `.gitignore`로 제외돼요. 실제 live 실행·토큰 발급은 이번 키트 검증에 포함하지 않았어요.

## 7. 매일 정해진 시각에 준비하기

```bash
python schedule_setup.py --os windows --time 20:30
```

**이렇게 보이면 성공:** `안내만 생성했습니다.`와 `BlogBookDaily`의 등록·확인·수동 실행·삭제 명령이 나와요. Windows 명령은 PowerShell에서 `cmd.exe`로 명령 프롬프트를 연 뒤 안내대로 실행하세요.

```bash
python schedule_setup.py --os macos --time 20:30
```

**이렇게 보이면 성공:** `안내만 생성했습니다.`와 `30 20 * * *`로 시작하는 cron 한 줄이 나와요. Linux는 `--os linux`를 써요. cron은 정한 시각에 명령을 실행하는 예약 도구예요.

**예약 등록은 안내에 나온 명령을 사용자가 직접 실행해요.** 도우미가 OS 설정을 바꾸지 않아요. 컴퓨터의 현지 시각을 쓰며 컴퓨터가 켜져 있어야 해요. 잠자기·전원 꺼짐·권한 때문에 건너뛸 수 있으므로 로그를 확인하세요. Windows 명령이 길다는 오류가 나면 키트를 짧은 경로로 옮기세요. 안내의 261자 제한은 보수적인 키트 기본값이에요. 예약이 실행되면 날짜별 프롬프트와 초안 틀만 만들어요. **작성 → `--resume` → 리포트·미리보기 → 사람 승인 → 드라이런/선택 live**는 사람이 이어 가요. 승인·발행은 예약에 넣지 않아요.

## 8. 개발자 테스트와 지원하는 문법

실행에는 외부 패키지가 없어요. 테스트할 때만 pytest가 필요해요. 이미 설치되어 있다면 다음을 실행하세요.

```bash
python -m pytest
```

**이렇게 보이면 성공:** 테스트가 모두 `passed`로 끝나요. pytest가 없으면 가상환경에서 `python -m pip install -r requirements-dev.txt`로 준비할 수 있어요. **이 설치만 인터넷이 필요**하며 정상 설치 후 `Successfully installed` 또는 `Requirement already satisfied`가 보여요. 테스트는 실제 네트워크를 차단하고 발행 응답을 모킹해요. 모킹은 실제 서버 대신 가짜 응답을 넣는 검증이에요.

지원 문법은 `#`~`######` 제목, 문단, 평면 글머리/번호 목록, `>` 인용, 단순 파이프 표, 삼중 백틱 코드, `**굵게**`, 백틱 인라인 코드, `[글자](주소)`, `![설명](이미지)`예요. 목록 중첩·각주·복잡한 표·공백/괄호가 포함된 주소·원시 HTML은 지원하지 않아요. 원시 HTML은 글자로 표시하고, 위험한 주소 방식은 거절해요. HTTPS 링크·이미지도 자동 다운로드하거나 사실 확인하지 않아요. 복사한 후 플랫폼 편집기에서 사진·서식·대체 텍스트를 마지막으로 확인하세요.

검증 환경은 Linux / Python 3.10, 오프라인 실행·모킹이에요. Windows/macOS 실기기 예약 등록과 실제 계정 발행은 사용자가 별도로 확인해야 해요.
