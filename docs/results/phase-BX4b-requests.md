# BX4b 통합 요청

담당 장·전용 자산만 수정했다. 공통·다른 장·키트·research·PROJECT_STATE·서가는 수정하지 않았다.

| 대상 | 요청 | 근거·확인 방법 |
|---|---|---|
| scripts/check_site.py 출처 등록 | site-blog 심화 장에서 research-blog-advanced/SOURCES.md의 BX 출처도 검사하도록 등록 범위를 추가 | BX3부터 미등록 BX 출처 오류가 남아 있다. 원본 검사 결과는 phase-BX4b/check-site.json. |
| scripts/check_site.py 인용 추출 | URL 문자열의 BS074·L107을 본문 출처로 세지 않도록 인용 텍스트/각주만 추출 | A9 개인정보보호위원회 공식 URL의 bbsId=BS074 값과 A11 GitHub 코드 줄 링크의 #L107 값이다. 둘 다 출처 ID가 아니다. 기존 BX3 요청 재확인. |
| site-blog/assets/book.js | 07-ads, 08-affiliate, 10-analytics, 11-operations, 12-policy, e2e의 상태를 완성으로 변경 | 각 본문 body data-manuscript=complete. 공통 파일 소유자는 BX5. |
| 표지·용어집·출처·실험실 | 새 여섯 장과 A8 표시 위치 도구·E2E 기록을 목차/부록에 통합 | 새 용어 후보는 phase-BX4b-glossary.md. 실제 인용 출처는 각 장 source-notes. |
| docs/PROJECT_STATE.md·서가 | BX4b 집필·검증 결과와 실제 미실행 경로를 통합 시 반영 | 병렬 작업 중 공통 상태 문서는 수정하지 않음. phase-BX4b.md의 검증 결과 참조. |
| A1·A9 샘플 | 동일한 명령의 Windows/unix 탭을 공통 명령 블록 하나로 통합 | 이번 담당 여섯 장은 공통 블록만 사용. A1·A9는 승인된 샘플을 보존. |

키트 차이와 장별 추가 요청은 아래에 통합했다.

## 현재 키트와 설계 기대의 차이

아래 항목은 본문에서 사실대로 구별했고 기본 완주를 막지 않는다. 이 단계에서는 키트·expected를 고치지 않았다. 향후 변경을 선택할 때 시작 ZIP/expected/체크포인트를 함께 검토한다.

| 대상 | 실제 구현과 본문 대응 |
|---|---|
| A8 프로그램 문구 | links.csv의 program은 쿠팡(모의)이지만 기본 원고 commercial_relations에 program이 없어 일반 관계 문구가 나온다. 쿠팡 의무 문구 분기를 별도로 시연하려면 샘플·시작 상태·expected를 함께 조정해야 한다. 본문은 실제 문구와 실사용 문구를 분리했다. |
| A10 실수집·재점수 | report는 고정 모의 지표/6점이며 GA4/GSC는 전송 함수 주입형 어댑터다. OAuth·토큰 갱신·정기 실수집·글감 자동 재점수는 구현 완료로 표시하지 않는다. |
| A11 예약 대상 | 생성되는 OS 예시와 Actions 예시의 run --sample은 가상 승인을 포함한다. 실제 글 승인 작업으로 등록하지 않도록 본문에 쓰고 report 예약 연습으로 바꾸게 했다. 후속 생성기 개선 시 안전한 기본 작업을 검토한다. |
| A11 영속 상태·알림 | runner 밖 비공개 상태 보존과 라이브 알림 전송 구성은 선택 운영 과제다. 파일 생성만으로 예약 등록·알림 수신·상태 동기화가 완료됐다고 쓰지 않는다. |
| A12 점검 기록 | audit는 고정 빈 제목 여섯 개를 생성한다. 확인자·근거·보류 이유 저장은 키트 밖 개인 메모로 안내했다. 원본 체크칸 수정 시 학습용 바이트 검사가 실패한다. |

## 검증 수집기

공통 명령의 `data-run="common"`을 수집해야 한다. `docs/results/phase-BX4b/verify-commands.py`는 이 블록을 포함해 commands.md·성공 stdout·실제 코드 발췌를 대조한다. 새 심화편은 기존 Reels 기준선에 없으므로 분량 비교 baseline을 임의 추가하거나 기존 값을 바꾸지 않았다.
