# n8n·Make·Zapier와 한국 사용자 사례

- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/09-nocode-korea.md` · SHA256 `4876bd153a8e00d6d76b7023c1307f8f859473381bce22073f96a7208f78c2d4` · exit 0.
- 실행·실패 구분: [provenance.json](provenance.json). 핵심 주장은 Codex 직접 열람/기존 근거와 대조했다.

2026년 10월 조사 기준. 기존 `research/nocode-pipelines.md`의 승인형 템플릿과 기능 범위를 재사용한다. 계정 연결·결제·템플릿 실행은 하지 않았다.

## 가격·무료 분량

| 도구 | 무료 | 유료 표시(기본 선택량) | 단위·주요 함정 |
|---|---|---|---|
| n8n Community | 내부 사업/개인 자동화 소프트웨어 사용료0 | 서버·저장/백업·관리 비용 별도 | cloud execution 상한을 Community에 적용하지 않음; 무제한 유료 호스팅 재판매 허용 아님 |
| n8n Cloud | 체험과 상시 무료를 구분 | Starter €20/월 환산·2,500executions, Pro€50·10,000, **연결제**. 월결제·한국 통화 재확인 | 전체 workflow 실행 단위. 외부 API·서버 생성비는 별도 |
| Make | $0·월1,000credits, 예약 최소15분 | 10k credits 선택: Core$9·Pro$16·Teams$29/월 표시, 할인/연결제 선택 상태 | 모듈 액션·polling·일부 AI 가변credits. 무료 파일5MB·실행5분 제한은 영상에 중요 |
| Zapier | $0·월100tasks, two-step Zaps | Professional 750tasks: 연결제 시작$19.99/월. 월결제값은 선택 화면 재확인(보충 Hermes는$29.99 확인) | 성공 액션task·유료 앱·다단계·webhook 조건 확인. pay-per-task 켜면 초과 과금 |

[A055](SOURCES.md#a055) [A120](SOURCES.md#a120) [A131](SOURCES.md#a131) [A062](SOURCES.md#a062). 공식 가격표 일부는 동적 토글·통화가 다르게 반환된다. €/$를 같은 가격으로 합치지 않는다. 연간 합계를 월 청구액처럼 쓰지 않는다. n8n 라이선스는 source-available/Sustainable Use License이며 OSI 무제한 오픈소스와 구별한다.

가상 계산: 30편×6개 성공 액션=180tasks면 Zapier Free100을 초과한다. Make에서도180credits만 보지 말고 polling·자식이미지 반복·생성 대기·오류 재시도를 더한다. 매15분 polling이 매번1credit을 쓴다고 가정하면 하루96×30일=2,880이므로 콘텐츠가 없어도1,000을 초과한다. 정확한 모듈별 차감은 현재 usage에서 확인한다.

## 게시·생성 노드

| 도구 | Instagram | YouTube | OpenAI |
|---|---|---|---|
| n8n | 공식 기본 Instagram 전용 게시 노드는 확인하지 못함. **HTTP Request**로 로그인별 API 호출; Facebook Graph API 노드는 facebook 호스트 기본 | 공식 YouTube 노드 `Upload a video` 지원 | 공식 노드에 Responses/Chat·이미지·음성 등. 노드/모델 버전 일치 확인 |
| Make | 공식 `Instagram for Business (Facebook login)`: 비즈니스+연결페이지·관리권한. 사진·릴스·캐러셀 모듈. 별도 Instagram Login 네이티브 앱은 공개 근거 미확인 | 공식 Upload a Video | 공식 OpenAI 연동; 미노출 최신 필드는 HTTP 호출 검토 |
| Zapier | 공식 Instagram for Business의 사진·동영상 게시 액션을 현재 목록에서 확인. 캐러셀은 현재 액션 지원표/입력 확인 전 확정 금지 | Upload Video | 공식 연동 존재; 최신 모델·schema 옵션과 사용료 확인 |

[A056](SOURCES.md#a056) [A057](SOURCES.md#a057) [A058](SOURCES.md#a058) [A060](SOURCES.md#a060) [A061](SOURCES.md#a061) [A063](SOURCES.md#a063) [A064](SOURCES.md#a064). API 자체가 Creator를 지원한다고 Make 특정 Facebook 커넥터도 Creator를 받는다고 확대하지 않는다. 커뮤니티 Instagram 노드의 존재와 공식 기본 노드는 다르다.

컨테이너 상태 폴링·AI 라벨·협찬/음원·insights는 네이티브 모듈의 현재 입력에서 개별 확인한다. `is_ai_generated`/`containsSyntheticMedia`가 안 보이면 기본 모듈이 자동으로 처리한다고 가정하지 않는다. HTTP Request를 쓰거나 사용자가 플랫폼 UI에서 마무리해야 한다. 자동화 도구가 Meta/YouTube의 검수·할당량을 없애지 않는다.

## 추천 흐름

편집 제안: n8n `Schedule Trigger → 입력 → LLM 구조화 초안 → 렌더 서비스/로컬 worker → 공개 URL(인스타) → 승인 → 게시 생성/상태/발행 → 결과 ID → 분석/실패 알림`.

첫 실습은 제공된 [human-approved Instagram 템플릿 A072](SOURCES.md#a072)의 **승인 구조**를 참고한다. 기여자 템플릿은 본인 계정에서 재설정해야 하며 그대로 가져오면 안전하게 운영된다는 보장이 없다. Instagram Login이면 Facebook Graph API 노드 호스트를 그대로 쓰지 말고 HTTP Request의 호스트·scope·token을 맞춘다. 렌더 worker의 인증·동시실행·파일 정리도 별도다.

## 한국 사용자 공개 사례

| 원문 | 구조·배울 점 | 검증 한계 |
|---|---|---|
| GPTers ‘N8N으로 부동산 매물 소개 릴스와 유튜브 자동화 하기’ | Google Sheets·사진/음악 폴더→필터/병합→Shotstack. 같은 매물번호로 잘못된 사진 폴더를 고르는 문제를 필터로 분리 | 작성자 실험 보고, 게시 성공·비용·매출 미검증. 본문도 테스트 중이라고 설명 [A093](SOURCES.md#a093) |
| GPTers ‘유튜브 영상 요약 자동화를 하려다 셀프 호스팅까지’ | Telegram 입력→요약→응답. API 연결·community node 노출·webhook 구성에서 막혀 실행 방식 변경 | YouTube **업로드** 사례가 아닌 수집/요약 사례. 개인 보고를 현재 n8n 전체 기능 제약으로 일반화 금지 [A094](SOURCES.md#a094) |

두 문서는 상대 날짜만 있어 절대 게시일을 확정하지 않는다. 한국 독자가 공개 공유한 운영 경험의 근거이며 공급자 보장·수익 사례가 아니다. API 가격·정책 주장은 공식 문서에서 따로 확인한다. A0/A1/A6/A7에 반영한다.
