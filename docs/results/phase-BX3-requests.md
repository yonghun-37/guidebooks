# BX3 통합·키트 후속 요청

이번 작업은 사이트 심화편과 허용된 연결 파일만 바꿨다. 키트·research·검사기·PROJECT_STATE·서가는 수정하지 않았다.

## 통합 담당자: 출처 검사기 등록

`python3 scripts/check_site.py --site site-blog`는 `research-blog/SOURCES.md`만 읽는다. 새 장의 BX 출처 21종을 미등록으로 판정한다. 또 출처 URL의 `bbsId=BS074`도 사실 ID로 읽어 총 22건을 보고한다.

- `site-blog/advanced/`의 각주는 `research-blog-advanced/SOURCES.md`를 함께 조회하도록 검사기를 확장해 달라.
- 출처 번호 검사는 각주·출처 앵커를 대상으로 하고 외부 URL의 쿼리는 출처 ID로 세지 않는 것이 좋다.
- 기존 검사기는 수정하지 않았다. 임시 루트에서 두 출처 목록만 합쳐 동일 검사 함수를 실행하면 오류 0이다. [원본 결과](phase-BX3/check-site.json), [임시 합산 결과](phase-BX3/check-site-combined-registry.json).
- 실제 배포 전 이 등록 변경 후 원본 명령의 exit 0을 다시 확인해야 한다.

## 키트 담당자: A1 맛보기와 expected의 범위

`course/commands.md`의 A1 명령은 `doctor`, `status --mock`뿐이다. 사용자 요구의 `blog.py run --sample`을 실행하면 A1 expected에 없는 초안·보고서가 추가되므로 직후 `check A1`은 실패한다.

- 본문은 기본 A1을 먼저 check → 맛보기 → 날짜 변경 → reset/start → 기본 A1 재실행/check로 구성했다.
- 기본 A1·A9의 “이렇게 보이면 성공”은 expected stdout 그대로다. `start/check/reset`, 맛보기 등 expected에 없는 보조 실행은 별도 “실행 결과”로 표시하고 실제 stdout과 대조했다.
- 후속 키트에서 맛보기용 별도 expected·체크포인트를 제공하면 안내가 단순해진다. 기존 A1 expected를 임의로 고치지는 않았다.

## 키트 담당자: 운영 기록·진단의 차이

1. `doctor`는 고정 8767 포트의 빈자리 검사이고 실제 mock 서버는 임시 포트를 쓴다. 본문에서 둘을 구분했다. 고정 포트가 사용 중이어도 mock 자체는 작동할 수 있으므로 진단 문구·검사 정책을 검토해 달라.
2. 협찬 `tax.csv`에는 반납·비용 전용 열이 없다. 본문은 현금·현물·가액 근거·원천징수·실입금·증빙을 CSV에서 확인하고, 반납·비용은 개인 메모에 따로 적도록 안내했다. SQLite 이력에는 관련 기록이 있다. 후속 단계에서 내보내기 열 확장을 검토해 달라.
3. `course.py start/reset`은 output/private뿐 아니라 config.toml도 삭제한다. .env는 보존한다. 본문 양쪽에 실제 범위를 명시하고 운영 폴더에서 쓰지 않게 했다.

## 다음 단계의 문서·배포

- A0·A2~A8·A10~A12·E2E는 준비 중이다. 장 데이터와 각 자리 페이지의 `data-manuscript`를 본문 완성 때 함께 갱신한다.
- PROJECT_STATE, 서가 진행 현황, 배포·키트 ZIP 제공은 통합 담당자 소유다. 이번 범위에서는 바꾸지 않았다.
- Windows PowerShell/macOS 실기기, 이번 단계의 Docker·실호스팅 연결·실세금신고·실제 광고주 회신은 수행하지 않았다. Docker 선행 실행 근거는 phase-BX3k.md에 있다.
