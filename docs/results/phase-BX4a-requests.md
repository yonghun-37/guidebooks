# BX4a 통합·키트 요청

2026-10-28. 담당 장과 전용 자산만 수정했다. A1은 동일 명령 탭 7개를 공통 블록으로 합쳤다. 공통 파일·다른 장·키트·research·PROJECT_STATE는 수정하지 않았다.

| 대상 | 요청 | 근거·지금 본문의 처리 |
|---|---|---|
| `site-blog/assets/book.js`·표지 | `00-start`, `02-wordpress`, `03-topics`, `04-drafts`, `05-gates`, `06-publish`를 완성 상태로 표시 | 각 body에 `data-manuscript="complete"`. 본문은 완성, 공통 목차 상태는 통합 담당자 소유다. |
| 출처 검사·credits | 심화편의 `research-blog-advanced/SOURCES.md`를 site-blog 출처 등록부에 포함하고 실제 각주 텍스트를 검사 | 원본 검사 154건 모두 미등록 출처. 임시 합산 등록부 검사에서는 다른 담당 장의 `#L107`을 출처로 읽는 오류 1건만 남았다. `BS074` 같은 URL 쿼리도 출처로 세지 않도록 BX3 요청을 함께 처리할 것. [원본](phase-BX4a/check-site.json)·[임시 합산](phase-BX4a/check-site-combined-registry.json). |
| 용어집·도구 목록 | [새 용어 후보](phase-BX4a-glossary.md), A0 `#income`·`#cost`, A5 `#tool`을 통합 | A0 계산기와 A5 고정 샘플 판정 도구는 전용 JS/CSS만 사용하며 외부 전송·저장 없음. |
| A6 상태 출력 | `output/status.json`에 예약 날짜·공개 URL을 넣을지 검토하고, 추가한다면 expected와 본문을 함께 갱신 | 현재 실제 파일은 `post_count`, `posts[].id/status`만 제공한다. 날짜/URL은 SQLite의 posts 기록에 있다. 본문은 이 차이를 정확히 안내하고 기본 성공을 **mock 예약**으로 제한했다. 키트 변경은 없음. |
| A6 공개 재조회 명령 | A6에서도 mock 공개 재조회를 본문 기본 단계로 삼으려면 `status --sample info --advance-days 2`를 commands/expected에 공식 추가 | 현재 A6 commands는 고정 시계의 future 재조회까지만 있다. 해당 추가 명령은 본문에 임의 삽입하지 않았다. 공개 재조회 연습은 이미 commands에 있는 A9로 연결했다. 실제 서버는 예약 시각 뒤 publish와 URL을 확인하도록 안내한다. |
| A4 실제 API·프롬프트 | 실제 CLI 전환과 프롬프트 파일을 과정 산출물에 포함하려면 별도 구현·검증·명령/expected 갱신 필요 | 현재 `draft` CLI는 고정 mock 샘플을 사용한다. `providers/openai_adapter.py`는 주입 transport용이며 CLI와 연결되지 않았다. `model` 설정만 바꾸면 유료 호출이 된다고 쓰지 않았다. 설계 목차의 프롬프트 파일이 실제 생성된다고 주장하지 않는다. |
| A9 동일 명령 탭 | 공통 파일 소유와 별도로 A9 담당자가 동일 Windows/unix 명령을 공통 블록으로 합칠 것 | A1은 BX4a에서 7개를 합쳤고 OS가 다른 가상환경·복사 명령 탭만 남겼다. A9는 수정하지 않았다. |
| 상태 문서·서가 | BX4a 완료 범위와 미실행 경로를 통합 반영 | 결과 [phase-BX4a.md](phase-BX4a.md). Windows/macOS 실기기·이번 Docker·실호스팅·유료 호출은 미실행이다. |

정책 근거 추가 요청은 없다. A3의 자료 자체 기준일·수정일은 개인 출처 메모에 기록하도록 했고, 현재 스키마의 `as_of`/`checked_on`과 구별했다. 현재 키트에 없는 사후 확인 모드는 구현된 것처럼 설명하지 않았다.
