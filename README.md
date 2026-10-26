# Guidebooks

처음부터 차근차근 따라 하는 실습형 웹 교과서 모음입니다. GitHub Pages로 배포합니다.

| 책 | 경로 | 소스 |
|---|---|---|
| ReelsBook: AI 인스타 릴스·뉴스카드 자동화와 수익화 입문 | `/reels/` | `site/`, 따라 하기 예제 `starter-kit/` |
| ShortsBook: 영상 제작에 집중한 유튜브 쇼츠 입문 | `/shorts/` | `site-shorts/`, 따라 하기 예제 `shorts-kit/` |

- `shelf/`: 서가 첫 화면(`/`)
- `site/`: ReelsBook 정적 사이트(빌드 도구 없음)
- `starter-kit/`: 교과서 실습용 Python 예제
- `site-shorts/`, `shorts-kit/`: 쇼츠 교과서와 오프라인 제작 예제
- `research/`: 조사 노트와 출처
- `docs/`: 설계·계획·단계별 결과
- 배포: `main`에 push하면 `.github/workflows/pages.yml`이 `shelf/` + `site/`(→ `reels/`) + `site-shorts/`(→ `shorts/`)를 Pages에 올립니다. 현재 작성·검증 상태는 [프로젝트 현황](docs/PROJECT_STATE.md)과 [진행 페이지](shelf/progress/index.html)를 참고하세요.
