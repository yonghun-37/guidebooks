너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, docs/results/phase-A5v-insta.md, auto-kit/(rendering/, config.example.json, pipeline.py, tests/)를 읽어라.
이번 작업은 **Phase A2c. auto-kit 채널명 하드코딩 수정** 이다. 담당: auto-kit/와 site/advanced/04-render.html의 렌더 결과 이미지(그 그림 파일과 캡션)만. site-shorts/·site-blog/는 다른 작업자가 수정 중 — 건드리지 마라. commit하지 마라.
문제: auto-kit/rendering/short_base.py가 "자취생 10분 생존법", "도윤의 연습", "도윤의 쇼츠 작업실", "서진: …"을 하드코딩해서, insta 흐름의 모션 릴스 프레임에도 쇼츠 채널명이 찍힌다.
1. 채널/계정 이름·발화자 등 표시 문구를 흐름별 config(예: `flows.insta.account_name = "출근길 3분 생활 뉴스"`, `flows.shorts.channel_name = "자취생 10분 생존법"`)에서 읽게 하고, 렌더러·미리보기 HTML에서 하드코딩을 제거한다. 다른 하드코딩된 인물·채널 문구도 grep으로 찾아 같은 방식으로 정리한다.
2. 테스트: insta 흐름 렌더 결과(프레임 텍스트 또는 렌더 입력)에 쇼츠 채널명이 없고 계정명이 들어가는지 검사하는 테스트 추가. pytest 전체 통과(Python 3.11).
3. mock insta 흐름을 다시 실행해 site/advanced/04-render.html의 릴스 프레임 이미지를 교체하고, "채널명이 남아 있으므로 … 바꾸세요" 같은 임시 경고 문구를 삭제한다. check_site(--site site) 통과.
4. docs/results/phase-A2.md 끝에 "A2c 수정" 절 추가, `python3 scripts/notify.py "✅ [A2c 완료] auto-kit 채널명 설정화 ..."`.
