# ReelsBook 실행 계획

작성: 2026-10-26, Claude Code. 설계는 docs/DESIGN.md를 따른다. Codex는 지시받은 Phase만 수행하고, 끝나면 docs/results/phase-N.md 작성 → docs/PROJECT_STATE.md 갱신 → `git commit` → `python3 scripts/notify.py`로 보고한다.

## Hermes 호출법

Hermes는 이미 실행 중인 컨테이너 `hermes-research-hermes-1`이다(provider `openai-codex`, 웹 도구 사용 가능). 컨테이너가 없으면 멈추고 보고한다(직접 기동하지 않는다).

```bash
RUN=/home/yonghun/project/hermes-research/output/ai-insta-research-20261026
# 1) 질의 파일을 $RUN/queries/<topic>.txt 에 쓴다
# 2) 실행(질의 하나당 1회, 원응답 보존):
cd /home/yonghun/project/hermes-research && timeout 900 docker compose exec -T --user 1000:1000 -e HOME=/opt/data hermes \
  /opt/hermes/.venv/bin/hermes chat --query-file /output/ai-insta-research-20261026/queries/<topic>.txt \
  -Q --provider openai-codex -t web --max-turns 30 > $RUN/raw/<topic>.md 2>&1
```

- 질의는 최대 4개까지 병렬로 실행한다. 전체 질의 수는 16회 이하로 한다(재시도 포함). 실패한 질의는 1회만 재시도한다.
- 모든 질의에 다음 요구를 포함한다: 한국어로 답할 것, 주장마다 출처 URL과 출처의 게시·갱신일을 붙일 것, 공식 문서(Meta/Instagram 도움말·개발자 문서, 법령·정부기관)를 우선할 것, 확인하지 못한 것은 "미확인"으로 표시할 것, 한국에서의 가용성을 구분할 것, 2026년 10월 기준 최신 정보를 우선할 것.
- 원응답(raw)은 수정하지 않는다. Codex의 정리본은 ai-insta/research/에 따로 쓴다.

## Phase 1. 자료조사 (Hermes)

질의 주제(한 주제 = 한 질의, 필요하면 나누거나 합친다):

1. `algorithm-formats`: 인스타그램 추천 시스템 공식 설명, 릴스/캐러셀 사양(길이, 비율, 해상도, 장수), 오리지널 콘텐츠·재게시 정책, 2025~2026 변화.
2. `monetization-meta`: Meta/인스타그램 크리에이터 수익화 기능 전체와 자격 요건, 한국 가용 여부.
3. `monetization-other`: 브랜디드 콘텐츠·협찬 단가 범위, 제휴 마케팅(쿠팡 파트너스 등 한국 프로그램 포함) 조건, 자체 상품·뉴스레터 등 외부 수익 경로, 뉴스/정보 요약 계정의 실제 수익 모델 사례.
4. `graph-api-publishing`: Instagram Graph API(Content Publishing) 요건, 계정 유형, 권한, 게시 한도, 릴스·캐러셀 업로드 절차, 앱 검수, 토큰 수명, 2026년 변경 사항. Instagram API with Instagram Login 경로 포함.
5. `scheduling-automation-tools`: Meta Business Suite 예약, n8n/Make/Zapier/Buffer/Later 등 예약·자동화 도구 비교(무료 범위, 가격, 인스타 지원 기능).
6. `ai-text-image-tools`: 카드 문안·대본용 LLM과 이미지 생성 도구, 무료 경로, 상업적 이용 라이선스.
7. `ai-video-voice-tools`: TTS(한국어 품질, 무료·오픈소스 포함), 자동 자막(Whisper 계열), 영상 자동 편집(FFmpeg, MoviePy, Remotion, CapCut 등), 템플릿 기반 카드 렌더링(HTML→이미지, Canva 대량 생성), 라이선스.
8. `ai-labeling-policy`: Meta AI 생성 콘텐츠 라벨 정책, AI 대량 생성 계정의 도달·제재 위험, 한국 AI 기본법 등 표시 의무 동향(시행일 포함).
9. `korea-copyright-news`: 뉴스 기사·사진 인용과 저작권법(공정 이용, 출처 표시), 뉴스 요약 콘텐츠의 법적 위험, 초상권·퍼블리시티권, 실제 분쟁 사례.
10. `korea-ads-tax`: 공정위 추천·보증 심사지침(경제적 이해관계 표시), 인스타 유료 파트너십 라벨, 부업 SNS 수익의 세금(사업자등록 필요 시점, 업종코드, 종합소득세) 기초.
11. `growth-benchmarks`: 릴스/캐러셀 참여율·도달 벤치마크, 게시 빈도와 성장의 공개 데이터, 뉴스카드형 계정의 성장 사례, 니치 선택 기준.
12. `risks-failures`: 자동화 계정의 실패 사례, 스팸·계정 제한 사유, 커뮤니티 가이드라인 주요 위반, 회복 방법.

산출물:

- `research/<topic>.md`: 주제별 정리 노트. 구조는 "핵심 사실(출처 각주) / 수치 표 / 한국 가용성 / 불확실·상충 / 교과서 반영 포인트(장 번호)". 원응답 경로와 SHA256을 머리에 적는다.
- `research/SOURCES.md`: 전체 출처 목록(번호, 제목, URL, 기관, 게시·갱신일, 접근일, 신뢰도 등급 A 공식/B 언론·업계/C 개인·블로그).
- `research/FACT-SHEET.md`: 교과서에서 쓸 핵심 사실·수치 목록(사실 ID, 문장, 출처 번호, 반영 장).
- Codex는 원응답의 핵심 공식 출처 5개 이상을 직접 열어 확인하고 일치 여부를 FACT-SHEET에 표시한다(확인함/불일치/열 수 없음).
- 조사 결과에 따라 DESIGN.md 5절 목차 조정이 필요하면 제안을 docs/results/phase-1.md에 적는다(설계서 자체는 Claude Code가 고친다).

## Phase 2. 참고 사이트 분석 (REA)

- Codex에 연결된 REA MCP(`rea`)를 사용해 https://art.euiyun.com/color/ 의 표지와 장 페이지 2~3개, 실험실, 용어집을 분석한다. REA를 쓸 수 없으면 이유를 기록하고 curl·브라우저 자동화로 대체한다.
- 파악할 것: 정보 구조(URL 체계, 내비게이션, 장 사이 이동), 장 내부 블록 마크업 패턴, 시뮬레이터 구현 방식(SVG/Canvas, 상태, 입력 장치), 퀴즈 방식, 반응형·다크 모드·인쇄 처리, 타이포그래피·여백 체계, 성능(파일 크기, 의존성).
- 산출물: `docs/reference-analysis.md`(패턴 목록과 ReelsBook 적용 방안, 따라 하지 않을 점). 원 사이트 코드·문장·이미지는 저장소에 복사하지 않는다(분석용 임시 파일은 저장소 밖 임시 디렉터리에 둔다).

## Phase 3. 뼈대와 디자인 시스템, 1장

- `site/` 구조, `book.css`, `book.js`(장 데이터, 내비, 진행 체크, 퀴즈 엔진, 복사 버튼, 다크 모드), 시뮬레이터 공통 모듈, 장 템플릿(`docs/chapter-template.html`).
- 표지(index.html)와 1장 완성, 1장 시뮬레이터 1개 동작.
- 산출물 스크린샷(데스크톱·모바일)을 `docs/results/phase-3/`에 저장한다. 이 단계 후 Claude Code가 검수한다.

## Phase 4. 스타터 키트

- DESIGN.md 6절대로 구현. 오프라인 모드 전체 실행 성공, `samples/` 생성, `starter-kit/README.md`(초보자용 설치 안내: Windows/macOS/Linux).
- 2부·3부 원고가 이 키트를 참조하므로 원고보다 먼저 만든다.

## Phase 5. 원고와 시뮬레이터 (2~16장, 부록)

- 5a: 2~8장. 5b: 9~14장. 5c: 15장 실험실, 16장 용어집, 출처·크레딧, 업데이트 기록.
- 모든 사실 주장은 FACT-SHEET의 사실 ID에 연결하고 페이지 각주로 SOURCES 항목을 단다.
- 작업실 노트의 명령은 실제로 실행해 확인한 것만 쓴다.

## Phase 6. 품질 게이트와 독립 검토

- DESIGN.md 8절의 게이트를 자동 검사 스크립트(`scripts/check_site.py`)와 스크린샷으로 확인한다.
- 별도 Codex 세션이 초보자 역할로 1→14장을 따라가며 막힘 목록을 만든다. 수정 후 재검사한다.
- 결과를 docs/results/phase-6.md에 기록한다.

## Phase 1b. 확장 자료조사 (Hermes, 사용자 요청 2026-10-26)

사용자가 "자료조사가 가장 중요하니 폭넓게 수집"을 요청했다. Phase 1 결과의 공백을 메우고 범위를 넓힌다. 질의 한도는 Phase 1과 별도로 **최대 28회**(재시도 포함), `--max-turns 40`.

추가 주제:

13. `korea-cases`: 한국의 카드뉴스·정보 요약형 인스타 계정과 미디어 스타트업 사례(성장 경로, 수익 모델, 운영 방식). 공개 인터뷰·기사 근거.
14. `global-faceless-ai`: 해외 얼굴 없는(faceless) AI 자동화 계정 사례, 공개된 수익 사례, 과장 광고·고가 강의 사기 패턴 경고.
15. `cross-platform`: 같은 콘텐츠의 유튜브 쇼츠·틱톡·스레드·네이버 클립 재활용, 플랫폼별 한국 수익화 조건 비교.
16. `korea-creator-economy`: 한국 인플루언서 마케팅 시장 규모, 체험단·협찬 매칭 플랫폼, 팔로워 구간별 단가 공개 자료.
17. `content-craft`: 카드뉴스 디자인·카피 원칙, 릴스 첫 3초 훅, 자막, 게시 시간, 해시태그 효용에 대한 공식·데이터 근거.
18. `music-assets-licensing`: 비즈니스 계정 음원 제한, 무료·상업용 음원·이미지·폰트 소스와 라이선스(공공누리 유형 포함).
19. `news-sources`: 뉴스 소재 소스(RSS, 네이버 뉴스 검색 API, 정부 보도자료·공공데이터), 이용약관과 재사용 조건.
20. `ai-tools-pricing`: 2026년 10월 기준 주요 AI 도구 가격·무료 한도 비교(LLM, 이미지, 한국어 TTS, 자동 자막·편집: 예 Vrew, 타입캐스트, CapCut, ElevenLabs 등). 한국어 품질 평가.
21. `nocode-pipelines`: n8n/Make/Zapier로 인스타 자동화한 실제 템플릿·사례, 흔한 실패 지점, 비용.
22. `account-setup-security`: 계정 개설, 프로페셔널 계정 전환, 2단계 인증, Meta 인증 구독, 새 계정 운영에 대한 공식 안내와 속설 검증.
23. `analytics-metrics`: 인사이트 지표 정의와 최근 변경(조회수 통합 등), 공유(보내기)·저장의 중요도에 대한 공식 발언.
24. `misinformation-ethics`: 뉴스 요약 계정의 오보·허위정보 위험, 팩트체크 절차, 정정·삭제 요구 대응, 관련 플랫폼 정책.
25. `learning-resources`: 공식 학습 자료(Instagram 크리에이터 센터, Meta Blueprint 등), 신뢰할 만한 강의·책·커뮤니티, 피해야 할 유형.
26. `gap-fill`: Phase 1의 FACT-SHEET에서 "미확인/추가 조사 필요"로 남은 항목 재조사(필요하면 여러 질의로 나눈다).

산출물: Phase 1 산출물 형식으로 research/<topic>.md를 추가하고 SOURCES.md·FACT-SHEET.md를 확장한다. 그리고 **research/BRIEFING.md**(사용자용 종합 브리핑, 한국어)를 쓴다: ① 한 쪽 요약 ② 주제별 핵심 발견 ③ 초보자가 반드시 알아야 할 10가지 ④ 현실적 기대치(수익·시간) ⑤ 위험과 금지 사항 ⑥ 추천 도구 조합(무료/저비용/유료) ⑦ 여전히 불확실한 것 ⑧ 교과서 목차 조정 제안. 모든 주장에 출처 번호를 단다.
