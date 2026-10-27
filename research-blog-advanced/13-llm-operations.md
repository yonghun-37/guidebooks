# LLM 가격 변경과 예약 운영 재사용

2026-10-27 · 한국 · 2026년 10월 조사 기준. 신규 과금·가입·실계정 게시를 실행하지 않았다.

**무료 mock로 끝낸 다음 실제 API를 고를 때 현재 가격·모델 종료·지출 한도를 확인한다.**

## 원응답과 재사용

기존 근거 재사용 범위: [00-scope-reuse.md](00-scope-reuse.md). 원응답 전문은 외부 RUN에만 보관한다.

| 원응답 경로 | SHA256 |
|---|---|
| `/home/yonghun/project/hermes-research/output/blog-advanced-research-20261027/raw/16-llm-delta.md` | `713aa41c4ad7c0e6350687f5f5e0dff7aee5bb47b421d807a11c473e9969ac8b` |

## 핵심 사실·수치·한국 가용성

| 모델·조건 | 입력/출력 $/100만토큰 | 가정: 입력3000·출력1000토큰/편·30편 |
|---|---|---|
| gpt-6-luna Standard short, 캐시 없음 | 0.10 / 0.50 | 0.0008달러/편·0.024달러/월 |
| gpt-6.1-sol 같은 조건 | 2.00 / 10.00 | 0.016달러/편·0.48달러/월 |
| Gemini3.5Flash-Lite 표준 | 0.30 / 2.50 | 0.0034달러/편·0.102달러/월 |

계산은 (입력토큰×입력단가+출력토큰×출력단가)/1000000이다. 이는 텍스트 토큰의 가상 계산이며 재시도·사고/도구토큰·이미지·세금·환전·최소 충전·구독료를 제외한다. ChatGPT 구독을 API 크레딧으로 취급하지 않는다. [BX071](SOURCES.md#bx071) [BX075](SOURCES.md#bx075)

Structured Outputs는 Responses text.format의 json_schema/strict다. Gemini/Anthropic의 함수명과 옵션은 기존 research-advanced/generation-apis.md를 재사용하고 서로 동일한 JSON 필드라고 설명하지 않는다. 요청 형식이 맞아도 임상/정책 사실은 별도 대조한다. experience는 빈칸으로 받고 사람이 직접 채운다.

OpenAI 현재 강제 월한도는 Project settings→Limits→Spend→Edit spend limit→Monthly spend limit→Enforce a hard limit→Save다. Spend alerts만으로 차단된다고 쓰지 않는다. AI Studio는 Spend의 Monthly spend cap에서 확인한다. 키트도 호출 전에 예상 최대비용을 예약하고 실패·재시도 비용을 포함한다. 공급자 한도의 전파/정산 지연으로 초과 가능성이 남는다. [BX073](SOURCES.md#bx073) [BX076](SOURCES.md#bx076)

OpenAI2026-10-14 종료 공지에서 구 GPT-4계열 종료/대체를 현재 선택 모델 종료와 혼동하지 않았다. 가격표의 gpt-6-luna/gpt-6.1-sol 등재를 재확인했고 새 종료로 교체할 근거는 찾지 못했다. Gemini 종료표도 다시 대조했다. [BX074](SOURCES.md#bx074)

cron/Windows 작업 스케줄러/알림/Actions 설정은 기존 심화 조사 재사용이다. 개인 노트북이 꺼지면 로컬 작업은 실행되지 않는다. Actions는 기본 브랜치·UTC 스케줄·지연/누락·임시 runner·중복 실행을 고려한다. SQLite/승인 대장을 공개 artifact로 내보내지 않는다. WP-Cron은 방문 기반이라 예약 등록 성공과 실제 공개를 따로 기록한다. [BX080](SOURCES.md#bx080) [BX127](SOURCES.md#bx127)

## 불확실·상충과 권장 결론

문서상 지원·규정 확인과 특정 계정/제품/거래의 성공을 구별한다. 실제 계정 조건·제품 모델·계약이 정해지면 같은 공식 원문에서 확인일과 적용 범위를 갱신한다.

## 교과서·키트 반영

A1·A4·A11: doctor/start/check의 한국어 오류가 버전·폴더·포트·시간대·mock/live를 구별하도록 제안한다. 예약에 승인 우회 기능을 넣지 않는다.

## 연결 사실

[BXF-086](FACT-SHEET.md#bxf-086) · [BXF-087](FACT-SHEET.md#bxf-087) · [BXF-088](FACT-SHEET.md#bxf-088) · [BXF-089](FACT-SHEET.md#bxf-089) · [BXF-090](FACT-SHEET.md#bxf-090) · [BXF-091](FACT-SHEET.md#bxf-091) · [BXF-092](FACT-SHEET.md#bxf-092)
