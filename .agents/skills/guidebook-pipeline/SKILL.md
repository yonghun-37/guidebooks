---
name: guidebook-pipeline
description: Use when starting or continuing a guidebook (new book like ShortsBook, or a new phase of ReelsBook) — phase order, file ownership in parallel work, site/kit/deploy conventions, and the known pitfalls of this environment.
metadata:
  version: '1.0.0'
---
# 교과서 제작 파이프라인

역할: **Claude Code = 설계·검수·커밋·배포·사용자 보고**, **Codex = 실행(조사 지휘·집필·구현·검증)**, **Hermes = 웹 자료조사**. 진행 보고는 `python3 scripts/notify.py "메시지" [첨부...]`(디스코드, 한국어, 5줄 이내).

## 단계 순서 (ReelsBook에서 검증된 순서)

| 단계 | 내용 | 산출물 |
|---|---|---|
| 설계 | 목표·성공 기준(학습자 손에 남는 결과물), 이론편/실습편 목차, 인물, 시뮬레이터 후보 | docs/DESIGN*.md, docs/PLAN.md |
| **학습자 질문 먼저** | 장마다 초보자 질문 5개. 조사·집필의 출발점 | docs/learner-questions.md |
| 조사 | Hermes 질의(guidebook-research) + Codex 직접 확인 | research/* |
| 참고 분석 | 참고 교과서를 REA로 분석 | docs/reference-analysis*.md |
| 뼈대 | 공통 CSS/JS, 장 템플릿 v2, 표지, 1장 | site/ |
| 키트 | 무료·오프라인으로 끝까지 되는 예제, 실제 게시 경로는 기본 드라이런 | starter-kit/ |
| **샘플 1장 → 사용자 선택** | 문체·구성 2~3안을 한 장으로 만들어 사용자에게 고르게 한다. **전 장 집필 전에** 한다 | site/drafts/ |
| 이론편 집필 | 병렬(장 묶음별) | site/chapters/ |
| 실습편 | "오늘 기준 절차" 재조사 → 실습 0~N, E2E 체크리스트 | site/practice/ |
| 통합 | 장 데이터·실험실·용어집·출처 | |
| 독립 검수 | 별도 Codex가 초보자 역할로 따라 하기 + 채점표 | docs/results/phase-*-findings.md |
| 수정·게이트 | style_lint, check_site, 브라우저 검사 | |

ReelsBook에서는 "샘플 → 선택"을 늦게 해서 14장을 다시 썼다. 새 책은 반드시 집필 전에 한다.

## 병렬 작업 규칙

- 각 작업자는 **담당 파일만** 수정한다. 공통 파일(book.js, book.css, common.js, glossary, credits, index)은 통합 단계에서 한 작업자만 고친다. 필요한 변경은 `docs/results/phase-<x>-requests.md`에 diff로 남긴다.
- 새 용어는 `docs/results/phase-<x>-glossary.md`에 표로 남긴다.
- research/SOURCES.md·FACT-SHEET.md는 한 번에 한 조사 작업자만 수정한다.
- 결과는 `docs/results/phase-<x>.md`(+스크린샷 폴더), 상태는 docs/PROJECT_STATE.md(통합 작업자만).

## 이 환경의 알려진 함정

| 함정 | 대처 |
|---|---|
| Codex 샌드박스는 `.git`에 쓸 수 없다 | Codex는 commit하지 않는다. Claude가 검수 후 commit·push |
| `--dangerously-bypass-approvals-and-sandbox`는 자동 모드에서 거부된다 | `codex --search exec -s workspace-write -c sandbox_workspace_write.network_access=true --add-dir <Hermes RUN>` (scripts/codex_phase.sh) |
| `--search`를 `exec` 뒤에 쓰면 오류 | 최상위 옵션: `codex --search exec ...` |
| REA MCP가 비대화 실행에서 "requires approval" 로 거부 | `-c 'mcp_servers.rea.default_tools_approval_mode="approve"'` (codex_phase.sh에 포함) |
| Hermes 검색이 프록시 차단으로 403인데 exit 0 | 원응답에서 403을 세고 Codex 검색·직접 열람으로 보완 (2026-10-26 사용자가 해제) |
| 대기 스크립트의 `pgrep -f "<이름>"`이 자기 자신과 일치해 영원히 대기 | 실행 중인 PID를 구해 `while kill -0 <PID>` |
| 앱 도움말 페이지는 JS 렌더링이라 본문 추출이 안 됨 | 메뉴 이름은 "보통 이런 이름" + 표준 확인 문구 + 공식 링크, 사용자 실계정으로 확인 목록 갱신 |
| 근거 규칙만 강조하면 원고가 단서투성이가 된다 | STYLE-GUIDE의 문체 규칙과 함께 지시 |
| 구조·각주·렌더링 통과를 품질 통과로 착각 | 본문을 학습자 질문 기준으로 읽고 채점 |
| 새 책의 Hermes 출력 폴더가 Codex 샌드박스 쓰기 범위 밖 | 실행 전 `mkdir -p <RUN>/{queries,raw}` 후 `HERMES_RUN=<RUN> scripts/codex_phase.sh ...` |
| Codex 속도 | 사용자 지시(2026-10-26): 모든 Codex 실행에 `-c 'service_tier="fast"'` (codex_phase.sh에 포함, 전역 config에도 설정됨) |
| 공개 저장소 | 토큰·.env·Hermes 원응답 전문 금지. 키트 .env는 gitignore |

## 사이트·배포 규약

- 저장소 github.com/yonghun-37/guidebooks(공개, main). Pages(Actions): `shelf/` → `/`, `site/` → `/reels/`, 키트 샘플 → `/progress/samples/`. 새 책은 `site-<book>/` → `/<book>/`처럼 워크플로에 한 줄 추가.
- 사이트는 빌드 없는 정적 HTML/CSS/바닐라 JS, 상대 링크만, 외부 스크립트는 버전 고정 CDN.
- 진행 현황 페이지 `shelf/progress/index.html`의 단계 상태를 단계 종료 때 갱신한다.
- 실제 계정 로그인·게시는 작업자가 하지 않는다. 사용자가 로컬 .env에 토큰을 넣고 요청할 때만 live 검증.
