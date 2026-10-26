# 프로젝트 현황

갱신: 2026-10-26. **2026년 10월 조사 기준**, 컷오프2026-10-26.

## 프로젝트 개요

AI로 Instagram 릴스·뉴스카드를 만들고 검수·게시·수익 구조를 배우는 한국어 입문 교과서와 스타터 키트다. 범위·설계는 [DESIGN.md](DESIGN.md), [PLAN.md](PLAN.md)를 따른다.

## 현재 산출물

- Phase1 연구 기록은 Git e22bd23에 존재한다. [12개 주제 사실표](../research/FACT-SHEET.md), [Phase1 결과](results/phase-1.md), 원응답16회 기록을 보존했다. 과거 결과 문서의 당시 커밋 실패는 역사 기록이며 현재 커밋 유무와 구분한다.
- **Phase1b 확장 조사·브리핑·정합성 검증·첨부 보고 완료, 검수/커밋 대기:** [브리핑](../research/BRIEFING.md), [결과](results/phase-1b.md), [공백 해결표](../research/gap-fill.md). 주제13~26의14개 노트·73개 사실/공백을 추가했다.
- [출처 목록](../research/SOURCES.md)은 신규56개를 더해 총173개다. 신규 공식45개 출처의 관련 본문을 Codex가 직접 읽었다. 전체 출처가 모두 현행·한국 적용 검증을 마친 것은 아니다.
- Hermes는 초기14회+좁은 보충14회=28회/최대동시4개/--max-turns40. 모두exit0이나27회는 웹중계403으로 근거 확보 실패, 가격1회만 일부 공식본문을 얻었다. [실행/품질 manifest](../research/provenance-phase-1b.json), [직접 확인](../research/verification-phase-1b.json), [정합성 검사](../research/validation-phase-1b.json)를 구분한다. 문서 정합성40개 검사가 통과했고 Phase1 원응답·질의 해시도 유지됐다.5줄 한국어 요약과 브리핑 첨부의 Discord 보고는 HTTP200으로 완료했다.
- 다른 작업자의 Phase4 기본 키트(3005fa0)·Phase4b 확장(b6e0155) 커밋이 저장소에 있다. 해당 결과는 [Phase4](results/phase-4.md)·[Phase4b](results/phase-4b.md)를 따른다. 참고 분석·사이트·스타터 키트는 다른 작업자의 범위다. 이번에는 관련 코드/결과를 변경하거나 다시 검증하지 않았다. 단계별 현황은 해당 결과 문서를 따른다.

## 조사에서 확인한 핵심

- 국내 정보 미디어의 독자·편집·광고 경로와 해외 AI 스튜디오·가상인물·교육 사업을 구분했다. 회사 매출·다채널 독자·최고월 수입은 개인 Instagram 자동수익의 증거가 아니다.
- YouTube 초기후원/광고 자격·한국 지원, TikTok한국1만/일한약관5만 상충, NAVER 신규 API HUB와 기사 권리의 차이를 기록했다.
- 타입캐스트 플랜·ElevenLabs 무료 비상업/유료 조건·Google 한국어 음성/무료량/초과과금, CapCut 음악 반출 제한·Canva 소재 조건을 보완했다.
- W3C 대비/자막·Buffer 관찰연구·정부 산업원조사를 확인했다. 한국 초보 뉴스계정의 성장 기간·단가·전환율을 보장하지 않는다.
- Meta API100/50 충돌·JPEG 요건·세 로그인 경로·AI/광고 표시 분리와 기존 공정위2026-06-01 지침 근거를 유지했다. API views의 도입/폐기·광고/교차게시 합산 범위를 재확인했다.

## 남은 공백·제약

- 한국 Gifts/구독의 현행 개설·구매·지급, 보너스/광고·Live배지, 예약/음원/표시·커넥터 전체 지원과 실계정 동작.
- API 실효 한도·Unified 온보딩, TikTok 현행 약관 적용, 클립/이관공지 전문 대조.
- 쿠팡 현행 정책/요율/정산·국외 제휴/세무, 개별 TTS 화자/입출력·폰트/소재 권리·일부 한국 가격/무료량, 한국어 품질 실측.
- AI profile한국·AI기본법시행령/가이드첨부/계도후속, 최신AI요약분쟁·개별기사/RSS/사진/개인정보, 스팸/항소·해킹복구 절차.
- Hermes원응답은 외부RUN에 보존하며 공개 저장소에 전문·개인환경·토큰을 넣지 않는다. 유료키/결제·실계정 로그인/게시·Hermes환경수정·push는 하지 않았다.

## Git·다음 확인

.git가 읽기 전용이라 Phase1b의 요청 커밋은 불가하다. git add/commit을 시도하거나 우회하지 않았다. Claude Code가 연구의 확인 수준·브리핑·목차 제안을 검수하고, 쓰기가 가능한 환경에서 Phase1b 소유22개 파일만 `Phase 1b: extended research and briefing`으로 커밋해야 한다. docs/reference-analysis.md·docs/results/phase-2.md와 동시 작업의 starter-kit/·Phase4b 파일은 포함하지 않는다. 후속 집필/구현은 해당 Phase 지시에 따른다.
