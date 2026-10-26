# 신청 체크 카드와 15초 릴스 — 실제 생성 샘플

가상 계정 **출근길 3분 생활 뉴스**의 “청년 지원금, 신청 전 확인할 3가지”입니다. 특정 제도·금액·신청일을 만들지 않고 **대상·기간·서류**를 확인하는 형식을 보여 줍니다. 직접 작성한 **예시 문안이며 실제 제도 안내가 아닙니다.** 카드·캡션·영상에 표시를 유지하고 실제 뉴스처럼 게시하지 마세요. 동봉 자료의 `synthetic: true`는 live 게시를 차단합니다.

- `news.json`: 동봉 RSS에서 읽은 예시 문안 3개(대상·기간·서류).
- `copy.json`: 같은 내용을 다듬은 표지·본문 3장·마무리 1장. 실제 입력 JSON입니다.
- `card-01.png`~`card-05.png`: 1080×1350. 마지막 카드에 직접 작성 예시 문안과 원문 자리표시자를 표시했습니다.
- `reel.mp4`: 같은 카드 5장으로 만든 1080×1920, 24fps, **15초**, H.264/AAC. 무음·화면 자막, 느린 확대·이동·페이드가 있습니다.
- `subtitles.srt`: 0~3 / 3~6 / 6~9 / 9~12 / 12~15초 자막.
- `commute-card.webp`: 표지의 **AI 생성 예시** 배경. [실제 생성 프롬프트](../../site/assets/img/ai-examples/README.md)를 공개했습니다. 실제 도시·기관의 사진이 아닙니다.

공공기관의 실제 공고를 전재하지 않았습니다. `example.invalid`는 원문 링크를 넣을 자리이며 열리는 신청 페이지가 아닙니다. 실제 자료로 바꿀 때는 개별 공고의 이용 표식·대상·기간·예외를 확인하고 기관·작성연도·제목·표시된 작성자·원문 URL을 카드와 캡션에 남기세요. [공공누리 근거](../../research/music-assets-licensing.md), [공식 출처 표기 안내](https://goe.go.kr/goe/cm/cntnts/cntntsView.do?cntntsId=1046&mi=10092)를 함께 읽으세요.

## 다시 만드는 순서

2026-10-26 Ubuntu 22.04 x86_64 / Python 3.11.15 / FFmpeg 7.0.2에서, 설치·실행 기록이 없는 임시 키트 복사본으로 실행했습니다. 먼저 [README](../README.md)에 따라 설치하고 **starter-kit 폴더**에서 실행하세요. Windows의 `python`은 `.venv\Scripts\python.exe`로 바꿉니다. 같은 출력 폴더가 있으면 새 이름을 쓰세요.

```bash
python run_pipeline.py --offline --output output/first-post
```

기본 결과는 20초입니다. 문안을 다듬은 이 폴더의 `copy.json`을 `output/first-post/copy.json`으로 복사해 덮어쓰세요. 배경 경로 `samples/commute-card.webp`는 키트 폴더를 기준으로 읽습니다. 다음으로 `output/first-post/config.json`을 편집합니다.

1. `reel.duration`을 `15`로 바꿉니다.
2. `theme`을 `"ink"`로 바꿉니다.
3. `colors`를 `{"background": "#F0F2F5", "foreground": "#182B4A", "accent": "#3459BE"}`로 바꿉니다.
4. 폰트·피드·asset_root 경로는 내 컴퓨터에서 처음 생성된 값을 그대로 둡니다.

```bash
python write_copy.py output/first-post/news.json --validate --output output/first-post/copy.json
python run_pipeline.py render output/first-post
```

성공하면 `구조 검증 OK: … (사실 확인은 사람이 해야 합니다)`와 `검수 대기: …/REVIEW.md`가 나옵니다. 이 작업에서도 검수 대기에서 멈췄고 실제 게시하지 않았습니다. `cards/*.png`, `reel.mp4`, `subtitles.srt`, `copy.json`, `news.json`을 이 폴더와 사이트의 샘플 폴더로 복사했습니다. JPG·검수표·승인 파일·개인 설정은 동봉하지 않습니다.

샘플 전체는 약 **1.8MB**, 10MB 이하입니다. 테스트는 규격·디코딩·모션·3초 지점 장면 전환·무음·합성 게시 차단을 확인합니다. 모션을 붙여도 플랫폼 수익화가 보장되지는 않습니다. 내 해설·시연과 포맷 정책을 함께 검토하세요.

코드·직접 작성 예시 문안·샘플의 프로젝트 고지는 [MIT](../LICENSE), 폰트 소프트웨어는 [OFL](../assets/fonts/OFL.txt)입니다. AI 배경의 제작 방식·프롬프트는 위 링크에 공개했습니다. 실제 뉴스·사진·음원은 각각 이용 조건을 확인하세요.
