# 심화편 학습자 질문 A0~A9

2026-10-26 · A6에서 관문/운영 질문 대응 갱신. 두 책 공통 질문이며 게시·분석 예시는 플랫폼별로 나눈다. 실제 포럼의 **문제를 참고해 새로 쓴 질문**이다. 인용문·설문 빈도 순위가 아니다. 포럼 답변을 정책·가격 근거로 쓰지 않고 공식 출처와 대조한다. A### 전체 메타데이터는 [조사 출처](../research-advanced/SOURCES.md)에 있다.

## A0. 전체 그림

질문 출발점: [Autopilot YouTube 인증 문제 A117](https://community.n8n.io/t/need-help-with-final-step-of-my-autopilot-youtube-channel/295406), [한국 사용자 호스팅 경험 A094](https://www.gpters.org/nocode/post/journey-self-hosting-automate-EkBOTxGYh8N0Dg5).

1. 완전 자동화라면서 제가 승인해야 하는 곳은 어디인가요?
2. 매일 인스타 카드1편과 쇼츠1편이면 각각 한 달에 얼마인가요?
3. ChatGPT 유료 구독이 있는데 API 비용도 따로 내야 하나요?
4. 제 컴퓨터를 꺼도 돌아가나요? 무료 서버가 꼭 필요한가요?
5. API 게시가 막혀도 손으로 먼저 게시할 수 있나요?

답변 근거: BRIEFING·costs·execution-hosting·youtube-api.

## A1. 파이프라인 설계

질문 출발점: [승인형 캐러셀 파이프라인 A118](https://community.n8n.io/t/automate-instagram-carousels-using-n8n-apitemplate-and-blotato/204294), [Instagram 처리/다운로드 실패 A116](https://community.n8n.io/t/instagram-automation-gives-a-bad-request-with-a-400-error-with-valid-api/243518).

1. 주제·대본·이미지·승인·게시 결과를 어떤 파일로 나누나요?
2. 음성까지 만든 뒤 실패하면 처음부터 돈을 내고 다시 만들어야 하나요?
3. 업로드 직후 인터넷이 끊겼을 때 중복 게시를 어떻게 막나요?
4. 승인한 뒤 문안이나 대상 계정을 바꾸면 다시 승인해야 하나요?
5. 다음 날 실행할 때 어제의 작업 상태는 어디에서 읽나요?

답변 근거: cases-operations·approval-security·youtube-api·instagram-publishing.

## A2. 키·토큰·비용

질문 출발점: [며칠 뒤 인증 만료 A117](https://community.n8n.io/t/need-help-with-final-step-of-my-autopilot-youtube-channel/295406), [서비스 연결/운영 경험 A094](https://www.gpters.org/nocode/post/journey-self-hosting-automate-EkBOTxGYh8N0Dg5). 지출·유출 질문은 이 문제를 장기 운영 조건으로 확장한 편집 질문이다.

1. API 키·access token·refresh token은 무엇이 다른가요?
2. YouTube 자동화가 일주일마다 끊기는데 매번 로그인해야 하나요?
3. 인스타 토큰60일이 지나기 전에 어떻게 갱신하나요?
4. 예산 알림만 켜면 월2만원에서 자동으로 멈추나요?
5. 키를 GitHub에 올렸다면 파일만 지우면 되나요?

답변 근거: generation-apis·instagram-auth·youtube-api·approval-security.

## A3. 생성 API

질문 출발점: [Gemini/OpenAI JSON schema 차이 A126](https://community.n8n.io/t/gemini-2-0-how-to-pass-structured-output/81379), [이미지 URL·parser 실패 A127](https://community.n8n.io/t/im-having-issues-with-ai-agent-structured-output-parser-and-download-image-nodes-in-my-n8n-workflow-for-generating-instagram-stories-errors-like-invalid-url-and-parsing-failures/156194).

1. JSON으로 달라고 했는데 설명문이 섞이면 어떻게 하나요?
2. 같은 JSON 스키마를 OpenAI·Gemini·Claude에 그대로 보내도 되나요?
3. 무료 모델만으로 매일 운영할 수 있고 한국어도 되나요?
4. 음성은 글자당, 영상은 초당, 이미지와 LLM은 어떻게 계산하나요?
5. 예제의 Imagen·Veo·TTS 모델이 사라지면 무엇으로 바꾸나요?

답변 근거: generation-apis·costs·FACT-SHEET의 종료/가격 항목.

## A4. 렌더링

질문 출발점: [카드 템플릿 렌더/승인 A118](https://community.n8n.io/t/automate-instagram-carousels-using-n8n-apitemplate-and-blotato/204294), [사진·음악·문안 병합의 한국 사례 A093](https://www.gpters.org/nocode/post/QympbRkXRXlD6J6). 폰트·규격 질문은 조립 단계의 실패 위험을 확장했다.

1. 생성 이미지에 한글을 직접 그리지 않고 카드 문안을 넣을 수 있나요?
2. 이미지6장과 음성으로 세로 쇼츠를 만드는 데 영상 생성 API가 꼭 필요한가요?
3. ffmpeg는 어디에서 설치하고 한글 자막이 네모로 나오면 무엇을 확인하나요?
4. 렌더 완료 파일의 비율·길이·코덱을 어떻게 확인하나요?
5. 무료 폰트·소재·음원을 키트에 넣어 함께 배포해도 되나요?

답변 근거: execution-hosting·instagram-publishing·youtube-api·cases-operations.

## A5. 게시 API

질문 출발점: [Instagram API 게시 실패 A116](https://community.n8n.io/t/instagram-automation-gives-a-bad-request-with-a-400-error-with-valid-api/243518), [YouTube OAuth 운영 A117](https://community.n8n.io/t/need-help-with-final-step-of-my-autopilot-youtube-channel/295406).

1. 인스타는 비즈니스/크리에이터 중 무엇을 골라야 하고 Facebook 페이지도 필요한가요?
2. 본인 계정 하나에만 올려도 앱 검수·사업자 인증을 받아야 하나요?
3. 제 PC의 이미지·영상 파일을 바로 올릴 수 있나요, 공개 URL이 필요한가요?
4. 인스타100건/50건, 유튜브1,600/100/1unit 중 지금 어느 숫자로 계산하나요?
5. YouTube 공개로 요청했는데 비공개로 잠기면 설정 변경만 하면 되나요?

답변 근거: instagram-auth·instagram-publishing·youtube-api.

## A6. 자동 품질 관문과 예외 대기열

질문 출발점: [승인형 캐러셀 A118](https://community.n8n.io/t/automate-instagram-carousels-using-n8n-apitemplate-and-blotato/204294). A5r에서 직접 재현한 예외·오탐·종결 문제를 반영했다. 같은 검사기를 쓰되 각 책의 제작물에 맞춰 질문을 나눈다.

| 순서 | 인스타 질문 | 쇼츠 질문 |
|---|---|---|
| 1 | 어떤 검사를 모두 통과해야 하나요? | 사실 검사는 무엇을 보나요? |
| 2 | 원문과 숫자가 같으면 사실도 맞나요? | 중복은 파일 이름으로 보나요? |
| 3 | 정상 문안인데 검토 단어로 멈추면요? | 실패를 승인으로 넘길 수 있나요? |
| 4 | 예외를 approve로 통과시켜도 되나요? | 알림에는 무엇을 넣나요? |
| 5 | 고친 예외를 0건으로 만들고 언제 전자동으로 가나요? | 언제 전자동으로 가나요? |

답변 근거: 각 책 A6 FAQ와 실제 예외 실습. 인스타 #build/#exception-lab, 쇼츠 #checks/#exceptions/#exception-lab/#threshold. 두 책 모두 미게시 예외를 고친 새 실행으로 재검사하고 옛 ID를 reject해 기록을 보존한다. 원격 결과 불명은 조회/대조로 해결한다.

## A7. 스케줄링과 운영

질문 출발점: [2026-10 GitHub cron 지연 A119](https://github.com/orgs/community/discussions/209507), [국내 n8n 셀프호스팅 A094](https://www.gpters.org/nocode/post/journey-self-hosting-automate-EkBOTxGYh8N0Dg5).

운영의 핵심 질문(두 책 A7 본문과 화면 도식으로 답한다):

1. 매일 오전 9시로 설정했는데 늦으면 어디를 확인하나요? 절전 중에도 돌아가나요?
2. Discord 웹훅과 Telegram 봇 자격은 어디서 만들고 .env 어디에 넣나요?
3. 누가 언제 알림을 읽고 승인 버튼을 누르며, 수신 명령은 누가 켜 두나요?
4. 승인하지 않은 작업·이미 게시한 작업·실패한 작업을 다음 tick이 어떻게 처리하나요?
5. 내 컴퓨터 대신 클라우드에서 실행할 때 상태와 비밀을 어떻게 보존하나요?

노코드는 A7 안의 선택 상자와 FAQ에서 별도로 답한다. 다음 기존 FAQ 5개를 유지한다: 처음 고를 실행기, 무료 셀프호스팅의 서버/API 비용, Instagram 전용 노드 대안, credits/tasks와 편수 차이, AI 표시 필드가 없을 때 HTTP 요청. 운영 질문을 A6 관문 질문으로 채점하지 않는다.

답변 근거: execution-hosting·approval-security·nocode·cases-operations·[발급 보완](../research-advanced/a6-connections.md).

## A8. 분석

질문 출발점: [Instagram Insights JSON 정리 A153](https://community.n8n.io/t/organize-instagram-insights/16081). 오래된 스레드는 문제 유형만 참고하고 지표 이름은 현행 공식 문서로 갱신한다.

1. 게시 성공 응답만 있으면 조회수도 바로 알 수 있나요?
2. 인스타 views·reach·saved·shares를 어떤 API로 가져오나요?
3. 어제 게시한 글의 분석 값이 비었는데0으로 저장해도 되나요?
4. YouTube views와 engagedViews, 평균시청시간은 무엇이 다른가요?
5. 업로드 토큰으로 수익까지 볼 수 있고 Studio와 숫자도 같나요?

답변 근거: instagram-publishing·youtube-api·cases-operations.

## A9. 정책·안전

질문 출발점: [승인 구조 A118](https://community.n8n.io/t/automate-instagram-carousels-using-n8n-apitemplate-and-blotato/204294), [실제 유료 생성 파이프라인 A093](https://www.gpters.org/nocode/post/QympbRkXRXlD6J6). 아래는 이 운영 문제에 정책·권리 질문을 연결한 편집 질문이며 커뮤니티의 직접 발언을 옮긴 것이 아니다.

1. 공식 API로 게시하면 스팸·반복 콘텐츠 제재를 받지 않나요?
2. 같은 템플릿에 AI 대본·음성만 바꾸면 수익화가 가능한가요?
3. AI로 대본만 쓴 것과 실제같은 영상·음성을 만든 것의 표시는 어떻게 다른가요?
4. API 게시·AI 표시 때문에 도달이 낮아진다는 공식 근거가 있나요?
5. 무료 음원·협찬 표시·AI 표시를 API가 알아서 처리해 주나요?

답변 근거: policy-safety·instagram-publishing·approval-security.
