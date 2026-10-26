# auto-kit A2 구현 계획·진행

**목표:** 키 없이 두 흐름을 완주하고 사용자 인증을 추가하면 같은 상태·관문·승인 절차로 실제 API에 연결한다.
**설계:** [확정 설계](../../docs/DESIGN-advanced.md) 3·6절. Python 3.11+, SQLite, Pillow, pip ffmpeg, requests, JSON Schema. 다른 키트에서 필요한 코드만 복사한다.

## 범위와 결정

- 파일 소유: `auto-kit/`와 명시적으로 요청된 `docs/results/phase-A2.md`만. 공통 상태 갱신은 통합 작업자에게 넘긴다. commit·시스템 설치·실계정/유료 API 호출 없음.
- 기존 확정 설계와 사용자 실행 지시를 구현 승인으로 사용한다. 별도 설계·선택 대기 없이 직접 구현한다.
- 비용은 UTC 일/월, 모든 시도 전에 원자적 최대비 예약. 결과 불명 비용은 예약 유지. 원문/파일/설정은 실행별 동결, 승인 후 바뀌면 중단.
- Instagram은 예약 API를 가정하지 않고 로컬 지연 발행. YouTube는 private+publishAt. 거부는 공개 전만 가능하며 이미 게시된 Instagram을 자동 삭제하지 않는다.
- 운영 상태/세션/토큰은 private 디렉터리. Actions는 암호화된 외부 객체 저장소로 전체 상태를 복원/보존하고 runner를 승인 대기로 붙잡지 않는다.

## 작업

- [x] 1. `common.py`, `state.py`, `providers/`: 스키마·비용·공급자·mock. 비용 동시예약/일월 상한, 실행 최대비 예약/호출 정산, 스키마 재시도·usage 검증.
- [x] 2. `topics/`, `rendering/`, `gates/`: RSS/성과, 카드/ffmpeg, 검사. 실제 로컬 MP4·LUFS와 텍스트 관문 검증.
- [x] 3. `publish/`, `hosting/`, `ops/tokens.py`: Instagram 컨테이너/한도, YouTube 재개, R2/Pages, 토큰. 모킹 308/유실/폴링/오류/인증 경계 검증.
- [x] 4. `pipeline.py`, `approve/`, `ops/`: 상태·승인·거부·재개·중복·알림·분석. 두 흐름 mock 및 모든 외부 경계를 바꾼 live 코드 조립 테스트.
- [x] 5. `schedule/`, `examples/`, `doctor.py`, README·SVG·samples. 깨끗한 복사본 명령·링크·브라우저 검사, 독립 검토 수정 완료. 결과/실제 알림 여부는 저장소 결과 문서 참조.

## 검토 초점

승인 후 내용/대상 변경, 성공 응답 유실 후 중복 발행, 비용 재시도/동시 실행, quota 조회 실패와 0 구분, 드라이런 네트워크·토큰 유출을 회귀 테스트로 고정한다. 자동 관문은 사실/저작권 전체 검증기가 아니며 한국어 이름 추출 누락 가능성을 README에 명시한다.

## 최종 구현 결정

- YouTube 실제 채널 ID를 조회해 승인에 결합한다. readonly를 요청하고, 예약 취소에는 force-ssl도 필요하다.
- 새 생성 날짜는 OS 현지 날짜, 비용은 UTC, YouTube insert 카운터는 Pacific 날짜를 사용한다. 하루 생성 키는 원자적으로 선점한다.
- 외부 상태는 Fernet 암호화 ZIP과 원자적 conditional lease. 보존 실패 후 다음 실행을 닫고, Windows/POSIX 실행 경로를 복원할 수 있게 파일 상대경로로 승인한다.
- 업로드 직후 미준비 지표를 놓치지 않도록 tick이 최근 완료 게시물을 매일 재수집한다.
- RSS의 권리 확인은 기본 보류이며 feed 객체에서 사용자가 명시할 수 있다. 진행 중 영상 작업의 비용 예약은 같은 ticket을 재사용한다.
- 실계정·유료 생성·OS 실제 등록은 수행하지 않는다. 통합 상태 문서는 다른 작업자 소유이므로 갱신 요청만 결과에 남긴다.

## A2b 검수 수정

- [x] 생활 뉴스·네 칸 메모 원문/로컬 RSS를 흐름별로 선택하고 mock 장면·공개 샘플·도식을 같은 예시로 연결한다. 예시 문안 표시와 synthetic live 차단을 유지한다.
- [x] 최소 Python 3.11·doctor·OS 설치 명령을 통일한다.
- [x] 깨끗한 Python 3.11 복사본에서 README 명령·전체 pytest·새 미디어와 도식을 검증했다. 결과는 기존 phase-A2.md의 A2b 절에 기록한다.

## A6 독립 검토 수정 계획

입력: [발견 16건](../../docs/results/phase-A5r-findings.md)·[채점표](../../docs/results/phase-A5r-scorecard.md). 기존 구조를 유지하는 Level 2 수정이다. 새 의존성·배포 변경 없이 현재 문서와 코드를 맞춘다. commit·유료 키·실계정 사용은 하지 않는다.

- [x] F03/F04: `read_json`을 쓰는 실행별 결과 조회 CLI와 회귀 테스트. 두 흐름이 같은 상태에 있어도 ID·flow를 확인하고 UTF-8로 읽는다.
- [x] F05/F07: 실제 폰트 실패→복구 회귀, 시작 기준 사후 확인 시각 테스트. 성공 전진 시 현재 오류만 지우고 실패 이력은 이벤트에 보존한다.
- [x] F09: `python -m ops.tokens import-instagram --config config.json`으로 재발급한 환경 자격을 명시적으로 private 파일에 적용. 유효성·파일 권한·값 미출력 검증.
- [x] F10: 보유 소재 개수(2~5)를 요청 장면 수에 반영하고 해당 수의 스키마로 검증·재시도. mock도 같은 수로 문안을 묶어 렌더 수와 일치. 요청 불일치가 렌더/유료 미디어 호출 전에 차단되는지 검증.
- [x] F01/F02/F06/F08/F11/F13: README에 발급→설정 대응, 예외 종결, 수신 운영, 공통 전환 기준과 비용 예약 설명. doctor에 공개 호스팅 필수 필드 점검 추가.
- [x] F14: 사람이 편집한 카드·한국어 낭독 쇼츠와 재현/권리 안내를 일반 mock 샘플과 구분해 동봉.
- [x] F01~F16: 두 책 및 질문표 동기화. 공식 출처 직접 확인으로 추가 근거 보존.
- [x] Python 3.11 새 venv·깨끗한 복사본 README·pytest, 문체/정적 검사, 22페이지 3폭×2테마·콘솔·키보드·미디어 확인 후 A6 결과·현재 상태 기록.

파일 소유: 주 작업자=키트 구현/README·연구·질문표·통합 결과, 인스타 작업자=`site/advanced`와 전용 assets, 쇼츠 작업자=`site-shorts/advanced`와 전용 assets, 견본 작업자=`samples/editorial`·생성 스크립트·전용 견본 assets. 공통 파일은 수정하지 않는다.
