# 일일 생성 예약 — OS 명령 근거

확인일: 2026-10-26. Phase 6b에서 Codex가 공식 명령 문서와 Linux man-pages/POSIX 설명을 직접 대조했다. 키트는 명령 문자열만 생성한다. 실제 OS 등록·Windows/macOS 실행·다음 날 실제 실행은 수행하지 않았다.

- [S268](SOURCES.md#s268): Microsoft `schtasks /create` 문서의 `/SC DAILY`, `/ST HH:MM`, `/TN`, `/TR`을 사용한다. 작업 이름은 ReelsBookDaily이며 기존 작업을 강제로 바꾸는 `/F`는 넣지 않는다. Python 경로·스크립트 경로·인자를 인용하고 제어 문자와 cmd 환경 확장/메타 문자가 있는 경로는 거절한다. `/Query /TN … /V /FO LIST`, `/Run /TN …`, `/Delete /TN …` 안내를 함께 출력한다. 이 명령은 cmd.exe용이며 PowerShell에서는 먼저 cmd.exe로 들어가도록 설명한다.
- [S269](SOURCES.md#s269): crontab은 분·시·일·월·요일 다섯 칸 뒤 실행할 명령을 둔다. 매일 09:00은 `0 9 * * *`이다. 명령부의 `%`는 셸 인용 안에 있어도 cron이 먼저 처리하므로 `\%`로 이스케이프한다. 셸 인자는 `shlex.join()`으로 인용한다.
- [S270](SOURCES.md#s270): `crontab -e`에서 해당 한 줄을 추가·삭제하고 `crontab -l`로 확인한다. 전체 예약을 지우는 `crontab -r`은 안내하지 않는다. 다른 작업의 줄은 보존한다.

키트의 로컬 시각·날짜별 폴더·중복 거절·오프라인 고정·검수 대기 종료는 외부 정책이 아닌 직접 구현한 동작이다. 컴퓨터가 꺼져 있거나 잠자기 상태일 때의 예약 실행은 보장하지 않는다. macOS cron의 실제 권한 설정, Windows 작업의 로그인/배터리 조건은 독자 기기에서 확인해야 한다. 명령의 단위 검증은 `starter-kit/tests/test_daily_schedule.py`에 보존한다.

공식 원문:

- https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create
- https://man7.org/linux/man-pages/man5/crontab.5.html
- https://man7.org/linux/man-pages/man1/crontab.1p.html
