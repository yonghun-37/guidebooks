너는 ai-insta 프로젝트의 작업자(Codex)다. AGENTS.md, .agents/skills/guidebook-pipeline·guidebook-writing, docs/STYLE-GUIDE.md, **docs/DESIGN-blog.md 8절**, research-blog/(BRIEFING·FACT-SHEET·ai-production-blog, 자동화·API·정책 노트), docs/results/phase-B2.md, 그리고 참고 구현 starter-kit/·shorts-kit/(README, daily.py, schedule_setup.py, publish.py/upload.py, tests)를 읽어라.
이번 작업은 **Phase B3k. blog-kit** 이다. `blog-kit/` 폴더만 만든다(site-blog/는 다른 작업자가 동시에 만든다 — 건드리지 마라. starter-kit/, shorts-kit/, site/, site-shorts/ 수정 금지). commit하지 마라. 시스템 패키지 설치 금지.

- Python 3.10+, 표준 라이브러리 우선(필요 시 requirements.txt 최소), 무료·오프라인으로 끝까지.
- `brief.py`: 키워드·글 유형(정보/후기/경험)·플랫폼 → AI 서비스에 붙여 넣을 프롬프트 묶음 md(research-blog/ai-production-blog.md의 프롬프트 공식 기반: 검색 의도·질문 목록, 개요, 초안, 사실 확인 요청, 제목 3안, 요약·FAQ, 썸네일 이미지 프롬프트).
- `check.py`: 초안 md 검사 → 사람이 읽는 리포트. 제목 길이, 소제목 구조, 글자 수, 이미지 대체 텍스트, 제휴 링크가 있으면 대가성 문구가 본문 첫머리에 있는지(공정위 지침 근거), 숫자가 있는 문장의 출처 메모, 반복 문장·AI 상투 표현, "내 경험" 문단 유무. 기준값은 근거가 있으면 근거, 없으면 "키트 기본값(바꿀 수 있음)"으로 config에 둔다.
- `render.py`: md → 편집기에 붙여 넣을 HTML + 미리보기 HTML(모바일 폭).
- `publish.py`: B2 결론에서 API 발행이 실제로 가능한 플랫폼만(예: Blogger API v3, WordPress REST + 애플리케이션 비밀번호). **기본 드라이런**(요청 내용 출력), `--live`는 사용자가 .env/인증 파일을 직접 넣었을 때만, 토큰은 출력·로그 금지, .env는 .gitignore. 기본 공개 상태는 초안/비공개. 네이버·티스토리처럼 API가 없으면 "편집기에 붙여 넣기" 경로 안내만.
- daily.py/schedule_setup.py: 매일 정해진 시간에 brief→(사람 작성)→check→render까지, 발행은 사람 승인 후(starter-kit 방식 재사용).
- samples/에 가상 주제 샘플 글 1편과 출력물, pytest(오프라인 전체·검사 규칙·렌더·드라이런·모킹 발행), 초보자용 README(Windows/macOS, 명령마다 "이렇게 보이면 성공").
- 결과 docs/results/phase-B3k.md, `python3 scripts/notify.py "✅ [blog-kit 완료] ..."`.
- **예시**: docs/STYLE-GUIDE.md 7절 — 실제로 사람들이 보고 읽을 만한 소재로 예시를 정해 장을 관통시킨다(설명용 인위적 소재 금지, 실존 브랜드·지어낸 성과 숫자 금지). 인스타·쇼츠 편의 새 예시(출근길 3분 생활 뉴스 / 자취생 10분 생존법)와 어울리게 한다.
