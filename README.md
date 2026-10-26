# Guidebooks

처음부터 차근차근 따라 하는 실습형 웹 교과서 모음입니다. GitHub Pages로 배포합니다.

| 책 | 경로 | 소스 |
|---|---|---|
| ReelsBook: AI 인스타 릴스·뉴스카드 자동화와 수익화 입문 | `/reels/` | `site/`, 따라 하기 예제 `starter-kit/` |

- `shelf/`: 서가 첫 화면(`/`)
- `site/`: ReelsBook 정적 사이트(빌드 도구 없음)
- `starter-kit/`: 교과서 실습용 Python 예제
- `research/`: 조사 노트와 출처
- `docs/`: 설계·계획·단계별 결과
- 배포: `main`에 push하면 `.github/workflows/pages.yml`이 `shelf/` + `site/`(→ `reels/`)를 Pages에 올립니다.
