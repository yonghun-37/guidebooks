# Phase 7r 결과 — 실습편 오늘 기준 절차 재조사

작성: 2026-10-26, Codex. **2026년 10월 조사 기준**, 컷오프 2026-10-26. 설계는 DESIGN 10절, 범위는 PLAN Phase 7r이다.

## 완료 범위와 판정

**요청된 조사 실행·정리·직접 확인 기록을 작성했다. 앱의 전체 클릭 절차 근거 확보는 일부 미완료다.** 실제 계정 로그인·게시·유료 API·결제는 수행하지 않았으며 `site/`·`starter-kit/`을 수정하지 않았다. commit·push를 시도하지 않았다.

- [x] AGENTS·DESIGN 10절·PLAN Hermes 호출법/Phase7·지정 기존 조사와 실제 키트 계약을 읽고 범위를 확인했다.
- [x] 초기6회+보충2회, 합계8회/상한8회로 Hermes 질의·원응답을 외부 RUN에 보존했다. 개별 주제 보충은1회씩이며 최대동시4회·각 `--max-turns 40`이다.
- [x] 공식 문서 최소6개 요구를 넘어 **22개 문서의 관련 본문**을 Codex가 직접 읽고 확인 범위를 기록했다.
- [x] 실습1~10 대응 절차 노트·S174~S195 출처22개·PRAC-01~26 사실/공백을 추가하고 기존 출처7개의 재확인 범위를 보존했다.
- [x] 문서 정합성·실행 예산·해시·동시 실행 상한 등 20개 검사를 실행해 20/20 통과했다. 상세 결과는 아래 검증 기록을 따른다.
- [ ] 앱의 현행 한국 메뉴·AI/협찬 토글·예약·인사이트 클릭 순서의 공식 본문 확보. 미확인 탐색표로 인계했다.
- [ ] 개발 모드 게시물의 일반 독자 공개와 한국 계정 실게시 검증. 이번 단계의 실계정 금지 범위이며 조건부7v에서만 검증한다.

Level2 조사 기록이며 기존 `research/`와 `docs/results/` 관례를 재사용했다. 새 specs/ADR·구현·스케줄러를 추가하지 않았다.

## 조사 실행과 근거 품질

컨테이너 `hermes-research-hermes-1`가 실행 중임을 확인하고 PLAN의 기존 CLI만 사용했다. Hermes 저장소 코드·config·runtime·Skill·Prefect·DB·네트워크를 수정하지 않았다.

| 질의 | 대응 항목 | 결과 |
| --- | --- | --- |
| practice-account | 프로페셔널 전환·2FA·복구 연락처/백업코드 | exit0, 중계403, 근거 확보 실패 |
| practice-app-publish | 앱 캐러셀/릴스·AI/협찬 라벨·혼합 캐러셀 | exit0, 중계403, 근거 확보 실패 |
| practice-transfer-hosting | PC→휴대폰·무료 공개 URL 후보/제한 | exit0, 중계403, 근거 확보 실패 |
| practice-api-setup-token | 앱 생성·역할·검수/모드·토큰 | exit0, 중계403, 근거 확보 실패 |
| practice-api-media-version | 최신버전·image_url·rupload·캐러셀·API 라벨 | exit0, 중계403, 근거 확보 실패 |
| practice-schedule-insights | 앱/Business Suite 예약·24시간/7일 지표 | exit0, 중계403, 근거 확보 실패 |
| practice-app-publish-supplement | 정확한 공식 URL로 앱 절차 보충1회 | exit0, 같은 중계403, 근거 확보 실패 |
| practice-api-setup-token-supplement | 검수/모드 문서 대조·토큰 수명 보충1회 | exit0, 같은 중계403, 근거 확보 실패 |

8회 모두 `search.parallel.ai` 연결에서403을 보고했다. 도구 중계의 실패를 Meta 원서버 차단이나 한국 미지원으로 해석하지 않았다. 질의에 준 값·URL을 원문 확인으로 재사용하지 않았다. Codex가 별도 `urllib`/web로 공식 문서를 읽은 결과는 Hermes 성공으로 집계하지 않는다. HTTP200이어도 빈 본문·제목·소개만 있으면 본문 확인으로 세지 않았다.

원질의는 `$RUN/queries/practice-*.txt`, 원응답은 `$RUN/raw/practice-*.md`에 있다. RUN은 `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026`이다. 원응답은 수정하지 않았고 전문을 공개 저장소에 복사하지 않았다. 실행시각·exit·바이트·SHA256은 [provenance](../../research/provenance-phase-7r.json)에 있다.

## 직접 확인한 핵심과 상충

- **버전:** 공식 버전표와v26 변경이력에서 최신Graph API **v26.0, 2026-07-29 출시**를 확인했다. [S174](../../research/SOURCES.md#s174), [S175](../../research/SOURCES.md#s175)
- **검수/개발 모드:** 본인 소유·관리계정 Standard Access 검수 면제와 역할 사용자 테스트 권한을 읽었다. 공통 App Modes의 비역할 사용자 비노출·앱 생성 Step10의 live data 검수 문장도 함께 읽었다. 문서 조합상 검수 없는 본인계정 게시 테스트는 가능하다고 해석하지만 일반 공개까지 보장하지 않는다. [S031](../../research/SOURCES.md#s031), [S176](../../research/SOURCES.md#s176), [S178](../../research/SOURCES.md#s178), [S179](../../research/SOURCES.md#s179)
- **토큰:** 대시보드 Generate token은60일 장기, OAuth는1시간 단기다. 장기토큰은 발급24시간 이후·만료 전에 갱신하며 만료 후 갱신 불가다. [S177](../../research/SOURCES.md#s177), [S030](../../research/SOURCES.md#s030)
- **이미지/영상 업로드:** 이미지에는 공개 `image_url`이 필요하다. 동영상 resumable은 Facebook Login for Business 구현 앱의 `rupload.facebook.com` 경로로 문서화되어 있고 릴스·캐러셀 동영상 예제가 있다. Instagram Login의 rupload나 이미지 바이너리 지원 근거는 없다. 버전 없는/있는 rupload 예제 경로 혼재도 기록했다. [S001](../../research/SOURCES.md#s001), [S004](../../research/SOURCES.md#s004)
- **혼합 캐러셀:** API20개 혼합·VIDEO 자식과REELS의 차이를 본문에서 확인했다. 앱20개 혼합은 메타데이터/기존 Hermes 수준이다. 과거API10개 발췌와100/50한도 상충을 감추지 않았다.
- **호스팅/파일 전송:** GitHub Pages·raw/업로드·정책과 Cloudflare R2 무료량/checkout/개발용URL 제한, Apple AirDrop·Google Drive/iPhone·Android USB 절차를 읽었다. 무료 URL이 Meta 수신을 보장하거나 상시 운영 호스팅을 포괄 허용하는 것은 아니다.
- **라벨/날짜:** API AI는2026-06-22, 유료파트너십은2026-04-22 변경이력 구획이다. AI는 두 로그인, 유료파트너십은Facebook Login이다. 앱의 AI/파트너십 토글 위치는 미확인으로 남겼다.
- **후보 URL 오인 방지:** `225190788256708`은IGTV 소개, `566810106808145`는Meta Account 2FA 제목을 반환해 Instagram 릴스/인증앱 절차 근거에서 제외했다. S066 메타3분과 과거20분, 예약30일/75일 단편, S039의 모바일 제목과 데스크톱 안내 혼동도 기록했다.

## 산출물과 검증

- [practice-instagram.md](../../research/practice-instagram.md): 실습1~10별 번호 절차·입력/기대 결과·출처·확인 수준·화면 차이 대처·오류. 로컬 키트 계약/편집 제안/미확인 앱 경로를 구분했다.
- [SOURCES.md](../../research/SOURCES.md): 신규22개(S174~S195), 전체195개. 신규16개+기존6개, 합계22개의 관련 본문 직접 확인. 나머지는 메타데이터/미확인 후보이며 전체195개가 확인 완료라는 뜻은 아니다.
- [FACT-SHEET.md](../../research/FACT-SHEET.md): PRAC-01~26 신규 사실/공백.
- [verification-phase-7r.json](../../research/verification-phase-7r.json): 출처별 읽은 범위·날짜·응답 해시·제한. HTML/텍스트 원문은 `/tmp` 캐시로만 두고 공개 저장소에 넣지 않았다.
- [provenance-phase-7r.json](../../research/provenance-phase-7r.json):8회 실행·질의/원응답 해시·예산/품질.
- [validation-phase-7r.json](../../research/validation-phase-7r.json): 문서 정합성·출처/사실ID·링크·질의 수/원응답 해시·최대동시 실행 검사. 앱/API/기기 통합 테스트의 성공 기록이 아니다.
- [PROJECT_STATE.md](../PROJECT_STATE.md): 동시 작업자의 최신 Phase5d·사이트/키트 상태를 보존하고7r 조사·남은 공백만 좁게 추가했다.

키트·사이트 코드가 바뀌지 않았으므로 해당 테스트를 재실행하지 않았다. 실제 로그인·API 요청·휴대폰 전송·예약·게시·OS별 키트 실행은 검증하지 않았다. 이 조사 결과를 앱 완주·일반 공개 성공으로 보고하지 않는다.

## 인계·보고

7w는 확인된 API/전송 절차와 미확인 앱 탐색표를 구분해 사용해야 한다. 미확인 앱 메뉴를 확정 버튼 이름·화면 설명으로 바꾸지 않는다. 후속 계정 제공 시7v에서 게시 성공·일반 공개·라벨·예약/지표를 확인할 수 있지만 이번7r에서 수행하지 않았다. commit은 Claude Code 검수 범위다.

요청된 `python3 scripts/notify.py`로 한국어 5줄 완료·산출물·남은 문제를 전송했다. **HTTP 200**을 확인했다. 메시지 ID는 `1564084573883859039`이며 토큰은 출력하거나 문서에 저장하지 않았다.
