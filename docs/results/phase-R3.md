# Phase R3. AI 제작 도구와 제작 과정 집중 조사

기준/접근일: **2026-10-26**. 담당: Codex(조사·정리), Hermes(공식 웹 조사). 두 책 공통, **Claude Code 검수 대기**. 이 단계는 문헌 조사이며 실제 앱/계정에서의 제작·결제·게시 검증이 아니다.

## 완료한 내용과 산출물

- [공통 조사](../../research/ai-production.md): 작업별 실명 서비스·무료/유료·한국어/한국·상업권/표시 비교, 처음 가입할 AI 추천, 책별 무료/월1~3만 원 조합, 인스타4종·쇼츠3종 레시피, 입력/출력/도구/학습시간/비용, 프롬프트P1~P5, 품질 기준·상충·후속 확인 위치.
- [인스타 출처](../../research/SOURCES.md) S300~S399, [인스타 사실표](../../research/FACT-SHEET.md) AIP-001~068 추가.
- [쇼츠 출처](../../research-shorts/SOURCES.md) Y300~Y399, [쇼츠 사실표](../../research-shorts/FACT-SHEET.md) YT-AIP-001~068 추가. 공통 원문은 동일 끝번호로 대응한다.
- [직접 확인 메타데이터](phase-R3-verification.json): URL·기관·날짜·확인 범위·수집상태·해시. 본문 전문/로그인 자료는 포함하지 않는다.

**추천:** 처음 가입할 AI는 ChatGPT Free. 첫 완성 편집기는 인스타카드 Canva Free(한국어 우선 대안 MiriCanvas), 쇼츠 Clipchamp Free. 월 예산은 미리캔버스Pro14900원+타입캐스트Basic9900원=표시가24800원 조합을 두 책에서 함께 쓴다. 기업/공공/에이전시는 타입캐스트Basic 대상과 구별한다. 최종 청구액/과금 인원은 확인 대상이다.

## 중요한 변경과 판단

1. Sora는 웹/앱04-26·API09-24 종료 안내를 확인했다. 가이드는 아카이브로만 사용한다. CLOVA X/Cue: 종료 안내도 확인해 신규 실습에서 제외한다.
2. Flow 일50 무료 안내와 시작 도움말의 유료구독 요건이 상충한다. 한국 무료 생성 당일 완성을 기본 조합으로 약속하지 않는다. 현재 Gemini 앱 영상 모델은 Omni이며 Veo의Flow/API경로와 구별한다.
3. Midjourney V8.2의 Edit Model을 V7의 --oref와 구별한다. Ideogram 타이포 강점을 한글 완벽 렌더링으로 확대하지 않는다.
4. Vrew의 현행 공용 크레딧과 구형 기능별 한도를 분리했다. CapCut 무료 자막/한국Pro가격은 미확인으로 남기고 무료 출력이 명확한 Clipchamp를 제공한다.
5. Pika Free는 무워터마크지만 월지급0·상업권없음이다. Starter상업권은 공식 판본차이가 있어 보류한다. Runway 무료125는 최초 지급이다. Kling/Hailuo/Luma 최고 모델 사양을 앱 무료사양으로 전용하지 않는다.
6. Suno의 현재 상업권에는 허용 다운로드 조건이 있다. 무료곡의 나중 유료다운로드 소급범위는 상충으로 남긴다. Udio의 다운로드 중단을 확인해 파일전달 경로에서 제외한다.
7. Instagram의 현실적 영상/음성 신고와 정지이미지 자동 라벨을 구별했다. 현행 Instagram 상세도움말은 Hermes근거이며 Codex본문확인은 못 했다. YouTube현행공개/예외/C2PA자동라벨은 직접 읽었다.

## 수행 범위와 환경 준수

AGENTS.md·pipeline/research Skill·DESIGN12절·DESIGN-shorts와 지정6개 기존노트를 읽고 R3지시를 적용했다. OpenAI부분에는 openai-docs Skill과 공식 문서를 사용했다. 과거 PLAN의 일반질의상한/기존RUN보다 사용자의 이번 **RUN·총30회·최대4개** 지시를 우선했다.

site/, site-shorts/, starter-kit/, shorts-kit/, 설계서·배포·서가는 수정하지 않았다. PROJECT_STATE/진행페이지는 pipeline의 통합작업자 소유 규칙에 따라 이 결과로 갱신하도록 남겼다. 다른 작업자의 기존 변경/동시커밋을 되돌리지 않았다. Codex는 commit/push를 실행하지 않았다. 유료 API·결제·로그인·실계정 게시·컨테이너 기동/재시작/설정 변경을 하지 않았다. Hermes저장소는 허용된RUN의질의·원응답/메트릭만 썼다.

## Hermes 실행과 품질 판정

실행 **12/30회**, 재시도0회, 실제 최대동시4개, 각 `-s guidebook-research --max-turns 40 --provider openai-codex -t web`. 모든 프로세스 exit0이지만 이것만으로 성공 판정하지 않았다.

질의별 원응답을 읽고 오류 고지·근거 URL·핵심 수치의 본문/검색 구별을 확인했다. **근거 없이 끝난 전면 실패0/12(0%)**, 부분 접근/추출·미확인 항목12/12(100%)다. 부분제약을 없는 것으로 치지 않고 Codex 웹 검색·직접 HTTP로 보완했다. 아래 `403/timeout/blocked/검색실패`는 **대소문자 무시 문자열 출현 횟수**이며 실제 오류 건수가 아니다. “403은 없었다”도1회로 세므로 이를 실패율로 나누지 않는다. 실제 명시403 오류로 실패한 질의는 보고되지 않았고,03질의는30초시간초과를 고지했다.

시각은 **UTC**다(한국시각은+9시간). 바이트는 원응답 파일의 실제 크기다.

| 질의 | 시작 UTC | 종료 UTC | exit | 바이트 | 403/timeout/blocked/검색실패 언급 | URL수 | 판정·보완 |
|---|---|---|---|---|---|---|---|
| 01-research-llm | 04:28:45 | 04:33:40 | 0 | 25,327 | 1/0/0/0 | 32 | 부분 보완: Cue HTTP/접근 오류, 공식 공지는 Codex HTTP 추가 확인 |
| 02-image-generators | 04:28:45 | 04:31:40 | 0 | 27,434 | 2/0/0/0 | 43 | 부분 보완: 접힌 가격/참조 메뉴 누락, 공식 Markdown/JSON 대조 |
| 03-design-korea | 04:28:45 | 04:34:36 | 0 | 33,258 | 1/0/0/0 | 36 | 부분 보완: HTTP 오류·30초 시간초과, Miri 일반가격/Adobe한국가격 Codex 확보 |
| 04-editors | 04:28:45 | 04:32:44 | 0 | 18,799 | 1/0/0/0 | 26 | 부분 보완: 한국 CapCut 가격·Vrew 월결제 미확인; Vrew크레딧 Codex 공지확인 |
| 05-veo-sora | 04:31:40 | 04:35:48 | 0 | 26,139 | 1/0/0/0 | 46 | 부분 보완: 종료/약관 일부URL 실패, Sora종료·Flow공식상충 Codex 확인 |
| 06-other-video | 04:32:44 | 04:36:50 | 0 | 29,363 | 1/0/0/0 | 45 | 부분 보완: 약관/한국스토어/무료모델 불완전, 미확인·상충 분리 |
| 07-korean-voices | 04:33:40 | 04:37:15 | 0 | 24,755 | 1/0/0/0 | 36 | 부분 보완: 일부공식본문 누락, Typecast/Eleven/Clova/Vrew원문 대조 |
| 08-music-rights | 04:34:36 | 04:38:30 | 0 | 23,116 | 1/0/0/0 | 27 | 부분 보완: 일부YouTubeURL오류, Suno약관/다운로드·Udio변경 직접확인 |
| 09-workflow-cards | 04:35:48 | 04:38:39 | 0 | 19,800 | 1/0/0/0 | 14 | 부분 보완: 한국어도움말/다운로드누락, 영어Bulk·Miri가이드로 보완 |
| 10-workflow-shorts | 04:36:50 | 04:40:05 | 0 | 20,869 | 1/0/0/0 | 20 | 부분 보완: 일부UI검색 결과없음, 한국Vrew/해외Clipchamp 직접대조 |
| 11-prompt-guides | 04:37:15 | 04:40:52 | 0 | 25,237 | 1/0/0/0 | 25 | 부분 보완: 추정/구형URL실패, 현행Runway/MJ·Sora아카이브 직접대조 |
| 12-platform-labels | 04:38:30 | 04:42:26 | 0 | 22,087 | 1/0/0/0 | 19 | 부분 보완: Instagram현행도움말은셸, Hermes+Meta정책과YouTube본문 대조 |

원응답 경로: `/home/yonghun/project/hermes-research/output/ai-production-research-20261026/raw/<질의>.md`. 질의 파일은 같은RUN의`queries/<질의>.txt`다. 원응답은 수정하지 않았다.

| 원응답 파일 | SHA256 |
|---|---|
| `01-research-llm.md` | `66776ab6705be23c68bc491c9f826b9ce1f9870b7c24fc17e3e5d614d43fd071` |
| `02-image-generators.md` | `5b5776d07dbb5e6b51d482effa741e9d44df29e872fe73e1db4e5c4db5ea1398` |
| `03-design-korea.md` | `c8ed67155a1a0d4213bd1476e582845e178569c65bad77e8de605bbadb06f74e` |
| `04-editors.md` | `7794ae52bbf0e373155e8e6c9146c71232927d2a9832ed97aab6f0fdd52d8bcf` |
| `05-veo-sora.md` | `bf6ee234bdd18c7367ffb90012b9aed7fbf36823b43d77443ab1d928fb13d8f4` |
| `06-other-video.md` | `036da003f158ffde91215a02bfd8015df37d20cb701c08ee102f510720ef0577` |
| `07-korean-voices.md` | `7c1fa558767d3102d5edaae2ff799d1942f634be738b10d0fc59b937bbc946f3` |
| `08-music-rights.md` | `d68ca11e5b76ca4259e96da106dfb2a0a4d17f7731522085df825edc5ae2a37b` |
| `09-workflow-cards.md` | `467db81cd066c52f6c81080d9146cd945672c4978f6e93246a0fe4d92afe118e` |
| `10-workflow-shorts.md` | `683699b86c649c95ebe24e2e2e2576f808f42eb16470faaa170c76f6860768e3` |
| `11-prompt-guides.md` | `a885bc0f7f44fcf1e5e048c7aabe235250bf62ffb95a4d5b07447c62010a617d` |
| `12-platform-labels.md` | `b15748f4a275f2ce7935ec700e6e0f0af25384f39414d1505250d9bfeff87293` |

## Codex 공식 출처 직접 확인

신규등록100개 중 **94개는 적힌 범위의 본문을 웹 또는HTTP로 직접 확인**했다. 확인은 페이지 전체 사실의 보증이 아니다. 예: Gemini구독페이지 본문은 읽었지만 Pro금액은 빈값이므로 그 숫자는Hermes로 표시한다. Kling/Hailuo일부/Instagram현행도움말은HTTP200도 셸이라 직접확인으로 세지 않는다. 원문별 수준은 출처표와JSON을 따른다.

최소12개 요구를 충족하는 핵심 직접 확인 예시는 다음과 같다.

| 공식 원문 | 확인한 핵심 |
|---|---|
| [S300](../../research/SOURCES.md#s300) / [Y300](../../research-shorts/SOURCES.md#y300) | 무료도구별한도 |
| [S301](../../research/SOURCES.md#s301) / [Y301](../../research-shorts/SOURCES.md#y301) | Plus20/API별도 |
| [S302](../../research/SOURCES.md#s302) / [Y302](../../research-shorts/SOURCES.md#y302) | 웹검색/출처열기 |
| [S307](../../research/SOURCES.md#s307) / [Y307](../../research-shorts/SOURCES.md#y307) | Miri파일형식/다운로드 |
| [S310](../../research/SOURCES.md#s310) / [Y310](../../research-shorts/SOURCES.md#y310) | Cue종료공지 |
| [S312](../../research/SOURCES.md#s312) / [Y312](../../research-shorts/SOURCES.md#y312) | MJ가격/상업기업조건 |
| [S314](../../research/SOURCES.md#s314) / [Y314](../../research-shorts/SOURCES.md#y314) | 망고대량제작 |
| [S319](../../research/SOURCES.md#s319) / [Y319](../../research-shorts/SOURCES.md#y319) | Canva유료Bulk/CSV |
| [S322](../../research/SOURCES.md#s322) / [Y322](../../research-shorts/SOURCES.md#y322) | Miri월14900/연160800 |
| [S328](../../research/SOURCES.md#s328) / [Y328](../../research-shorts/SOURCES.md#y328) | CapCut음악플랫폼제한 |
| [S334](../../research/SOURCES.md#s334) / [Y334](../../research-shorts/SOURCES.md#y334) | 무료1080p/무워터마크 |
| [S336](../../research/SOURCES.md#s336) / [Y336](../../research-shorts/SOURCES.md#y336) | 타입캐스트최초무료/Basic |
| [S339](../../research/SOURCES.md#s339) / [Y339](../../research-shorts/SOURCES.md#y339) | Eleven무료상업불가 |
| [S342](../../research/SOURCES.md#s342) / [Y342](../../research-shorts/SOURCES.md#y342) | Flow가입/표시 |
| [S343](../../research/SOURCES.md#s343) / [Y343](../../research-shorts/SOURCES.md#y343) | Flow50/모델별비용 |
| [S346](../../research/SOURCES.md#s346) / [Y346](../../research-shorts/SOURCES.md#y346) | Sora종료 |
| [S348](../../research/SOURCES.md#s348) / [Y348](../../research-shorts/SOURCES.md#y348) | Runway상업권 |
| [S359](../../research/SOURCES.md#s359) / [Y359](../../research-shorts/SOURCES.md#y359) | Udio다운로드중단 |
| [S363](../../research/SOURCES.md#s363) / [Y363](../../research-shorts/SOURCES.md#y363) | YouTubeAI공개/C2PA |
| [S384](../../research/SOURCES.md#s384) / [Y384](../../research-shorts/SOURCES.md#y384) | Gen4.5사양 |
| [S387](../../research/SOURCES.md#s387) / [Y387](../../research-shorts/SOURCES.md#y387) | Suno현행다운로드상업조건 |
| [S388](../../research/SOURCES.md#s388) / [Y388](../../research-shorts/SOURCES.md#y388) | Vrew공용크레딧 |
| [S399](../../research/SOURCES.md#s399) / [Y399](../../research-shorts/SOURCES.md#y399) | Adobe한국VAT포함가격 |

## 검증 결과

- 문서 정합성 검사 통과: 출처 S/Y300~399 각각100개·사실 AIP/YT-AIP 각각68개 고유성, 모든 신규 로컬 링크/출처 앵커, 표 열수, 원응답12개 바이트/SHA256, 실제 최대동시4개, 학습시간7종 합계·월예산24800원·크레딧120/160 산술을 확인했다. 최종 실행1381개 세부 검사 통과(반복 링크 항목 포함). 이는 앱 기능 테스트 개수가 아니다.
- 기존 출처/사실표4개는 원래 바이트 접두부 해시가 그대로다. 신규 내용을 덧붙였고 기존 사실·다른 작업자 내용을 덮어쓰지 않았다.
- `git diff --check` 통과. 이번 작업은 연구문서만 수정해 사이트/키트 회귀 테스트는 실행하지 않았다. 로그인·이미지/영상/음성 생성·결제·게시 성공을 테스트했다고 주장하지 않는다.
- 원응답 전문·토큰·개인 환경 파일은 추가하지 않았다. 저장소에는 조사 요약·공식 URL/날짜·확인 범위·해시만 보존한다.

## 남은 확인·집필 인계

- 한국 계정의 실제 무료량·한국어 음질/자막/한글 생성·기기별 UI·결제·다운로드/게시 실증은 미실행이다. 학습자에게 확인할 화면과 무료 대안을 함께 남겼다.
- 레시피 시간은 편집자가 배정한 학습예산, 프롬프트는 공식문서대조 예시다. 생성성공·평균제작시간·품질순위로 표시하지 않는다. 실제 AI예시 산출·생성물/프롬프트 공개는 후속 집필 단계다.
- 최신 Instagram도움말·Kling멤버십·Hailuo일부·Vrew월결제·Canva/CapCut한국가격·Suno소급권리·Luma신구모델 범위는 명시한 확인수준/상충을 유지한다.
- 사이트/키트 원고 반영, 공유PROJECT_STATE/진행페이지 갱신, Claude Code 검수·commit은 해당 작업자가 맡는다. R3 조사자료가 있다는 이유로 실습·배포까지 완료로 표시하지 않는다.
- 완료보고: `python3 scripts/notify.py`로 한국어5줄과 공통 조사 노트를 첨부해 디스코드 전송 완료(HTTP200). 처음엔 ChatGPT Free·카드 Canva·쇼츠 Clipchamp 추천을 보고했다.
