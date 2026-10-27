# 운영 예시

`backup()`은 SQLite 논리 SQL 덤프와 mock WordPress 파일, 설정을 고정 ZIP에 담습니다. `.env`와 비밀값은 백업하지 않습니다. `restore()`는 ZIP 경로와 DB를 먼저 확인하고 교체가 실패하면 기존 상태를 복원합니다. SQL 덤프를 사용해 Python 버전이 다른 환경에서도 같은 내용을 바이트 단위로 비교하기 쉽게 했습니다.

`generate_schedule()`은 cron, macOS launchd, Windows 작업 스케줄러의 예시만 파일로 만듭니다. `<KIT>`을 실제 절대 경로로 바꾸고 운영체제에서 직접 등록하세요. `notify()`는 기본적으로 드라이런이며 실전송은 명시적 live, 허용 HTTPS 주소, 주입한 전송 함수가 모두 필요합니다. 응답 없음은 승인으로 취급하지 않습니다.

## 선택: 로컬 WordPress

`ops/`에서 직접 만든 `.env`에 `DB_PASSWORD`와 `DB_ROOT_PASSWORD`를 설정하고 `docker compose up -d`를 실행하세요. 브라우저에서 `http://127.0.0.1:8877`로 로컬 설치를 완료하고 사용자 프로필의 애플리케이션 비밀번호를 만들어 키트의 로컬 비밀 설정에 넣습니다. 로컬 컨테이너에서만 `WP_ENVIRONMENT_TYPE=local`을 사용합니다. 실제 운영에서는 HTTPS와 서버 접근 통제를 사용하세요. 실계정 연결은 사용자가 직접 설정합니다.

예제 ZIP은 mock 상태용입니다. 실제 WordPress는 DB 덤프와 `wp-content/uploads`를 함께 백업하고 별도 테스트 환경에 복구하여 글과 미디어를 확인하세요. 애플리케이션 비밀번호는 WordPress 사용자 프로필에서 폐기 후 새로 발급하고 로컬 `.env`만 교체합니다. 알림 키와 DB 비밀번호도 해당 서비스에서 교체하고 백업·로그에 남기지 마세요.

실습 종료 시 `docker compose down`으로 컨테이너를 멈춥니다. `docker compose down -v`는 DB와 WordPress 볼륨을 삭제하므로 데이터가 더 이상 필요 없거나 복구 가능한 백업이 있을 때만 실행하세요.

키트 루트의 `config.toml`에 `wordpress.mode="local"`, `url="http://127.0.0.1:8877"`을 설정합니다. 루트 `.env`에 `WP_USERNAME`과 `WP_APP_PASSWORD`를 넣습니다(Compose용 DB 비밀은 `ops/.env`). 아래 명령의 `--live`는 이 로컬 컨테이너 연결에만 사용하세요.

```text
python blog.py draft --sample info
python blog.py publish --sample info --prepare --live
python blog.py gate --sample info --approve 서윤
python blog.py publish --sample info --live
python blog.py status --sample info --live
```

샘플의 PNG는 WordPress 기본 업로드 형식입니다. SVG 원본도 함께 제공하며 추가 플러그인 없이 SVG를 업로드하지 않습니다. `python samples/make_images.py`로 PNG·가짜 EXIF JPEG를 다시 만들 수 있습니다.

승인에는 최종 원고·로컬 사진 바이트·서버 분류/미디어·협찬 계약과 광고주 확인 자료를 묶습니다. 발행 전 서버 원문과 미디어 원본 바이트를 재조회합니다. 불일치는 승인을 취소하고 예약 글을 초안으로 회수합니다. 회수가 확인되지 않으면 보류 상태로 남으므로 서버 관리자 화면을 직접 확인하세요. 별도 CDN이나 자동 이미지 변환을 연결하려면 원본 해시 비교 경로부터 확인해야 합니다.

이미 승인한 협찬 글을 고치면 작성으로 돌아갑니다. 가상 사례의 새 광고주 확인은 `python blog.py sponsor review`로 기록하고 다시 `gate --sample sponsor --approve 서윤`을 실행합니다. 실제 광고주 회신은 이 명령으로 만들지 않습니다.
