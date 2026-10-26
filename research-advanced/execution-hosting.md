# 예약 실행·공개 미디어 호스팅·ffmpeg

- Hermes 원응답: `/home/yonghun/project/hermes-research/output/advanced-research-20261026/raw/08-execution-hosting.md` · SHA256 `9d884fce93dc02e62c5b0d339ef79935f4e3d5b78571b48b514c6530752b356d` · exit 0.
- 실행·실패 구분: [provenance.json](provenance.json). 핵심 주장은 Codex 직접 열람/기존 근거와 대조했다.

2026년 10월 조사 기준. 호스팅 기본 지식은 기존 `research/practice-instagram.md`를 재사용한다. 설치·배포·결제·URL 게시를 실행하지 않았다.

## 실행 방식 추천

**첫 구현은 로컬+승인 파일로 완주한다. PC 상시 가동이 어려우면 GitHub Actions로 옮기되 상태와 승인은 실행 밖에 보관한다.** n8n은 여러 서비스·승인 UI를 눈으로 연결하려는 독자에게 선택지다. 이는 초보 운영 부담을 줄이는 편집 제안이다.

| 방식 | 잘 맞는 경우 | 비용·운영 제약 |
|---|---|---|
| 로컬 Windows/macOS | 설치·실패 복구를 배우는 첫 실습 | 기존 PC·전기/인터넷 필요. 꺼짐·절전·작업 디렉터리·권한 확인 |
| GitHub Actions | 매일 짧은 생성/업로드·수동 시작도 필요 | cron 지연·누락 가능. 작업 파일·SQLite는 다음 runner에 저절로 남지 않음 |
| n8n 셀프 호스팅 | 지속 실행·승인 웹훅·외부 서비스가 많음 | Community 소프트웨어 무료와 서버 무료는 다름. 백업·업데이트·HTTPS·자격증명 관리 필요 |
| n8n Cloud/Make/Zapier | 서버 관리 대신 구독을 선택 | 노코드 사용량과 LLM/렌더·호스팅 사용료 별도 |

## GitHub Actions

- `schedule`은 최소5분 간격이며 default branch의 워크플로/최신 커밋으로 실행한다.
- 현행 문서는 **`timezone` IANA 문자열 지원**을 명시한다. 생략하면 UTC. 예: 매일 한국시각09:17은 `cron: '17 9 * * *'`, `timezone: Asia/Seoul`; UTC 방식은 `'17 0 * * *'`다. ‘UTC만 가능’은 구형 설명이다.
- 정각 등 고부하 때 지연·일부 큐 누락이 가능하다. 공개 저장소는60일 활동이 없으면 예약 비활성화될 수 있다. 정확한 분 단위 게시 시각을 보장하는 실행기로 설명하지 않는다. [A044](SOURCES.md#a044)
- 표준 GitHub 호스팅 runner는 공개 저장소에서 무료. 비공개 GitHub Free는 월2,000분·artifact500MB 포함이다. 큰 runner는 공개여도 유료이며 저장/캐시·공유 계정 사용량을 확인한다. 예: 하루10분×30일=300분은 해당 가정의 실행 시간이지 모든 생성 작업의 보장 시간은 아니다. [A045](SOURCES.md#a045)
- 저장 위치: Repository Settings → Secrets and variables → Actions → New repository secret. workflow는 `${{ secrets.NAME }}`를 환경변수로 넘긴다. 공개 저장소에 `.env`/OAuth token JSON/세션 URI를 커밋하지 않는다. fork PR에 secret이 전달된다고 기대하지 않는다. OIDC를 지원하는 클라우드라면 장기 서비스 키를 줄이는 방식을 검토한다. [A046](SOURCES.md#a046)

**운영 설계 제안:** `concurrency`로 동일 계정 겹침을 막고 상태 저장소/완료 ID를 먼저 읽는다. artifact는 private 원본·토큰 저장소나 영구 데이터베이스로 쓰지 않는다. approval 대기로 runner를 계속 켜 두지 말고 생성 작업 종료 → 승인 기록 → 별도 `workflow_dispatch` 발행 작업으로 나눈다. 생성한 파일·승인 해시·상태를 어디에 보관하고 누가 읽는지 A2에서 명시해야 한다.

## Windows 작업 스케줄러·macOS launchd

| OS | 준비/설정 개요 | 성공 확인 |
|---|---|---|
| Windows | Task Scheduler 작업 만들기 → 매일 트리거 → 프로그램에 가상환경 Python 절대경로 → 인수에 `pipeline.py` 절대경로 → 시작 위치에 프로젝트 경로. `schtasks /Create /SC DAILY /ST HH:MM`은 공식 CLI 선택지 | 수동 Run 결과·Last Run Result·로그·실행 사용자 확인. 깨우기/로그온 관계는 사용자 환경에서 선택 |
| macOS | `~/Library/LaunchAgents/`의 본인 plist에 `ProgramArguments` 절대경로, `StartCalendarInterval` Hour/Minute, `WorkingDirectory`, stdout/stderr 경로 설정. 현재 OS의 `launchctl` 등록 방법 확인 | 수동 실행·launchctl 상태·로그 확인. LaunchAgent 로그인 세션과 시스템 daemon 구별 |

[A051](SOURCES.md#a051) [A052](SOURCES.md#a052). Apple 자료는 archived 개발 문서이므로 현대 macOS 실습 명령을 그대로 검증했다고 쓰지 않는다. 절전·전원 꺼짐의 누락 처리·깨우기 동작은 실제 기기에서 시험한다. 토큰을 스케줄러 인수나 plist에 직접 넣지 않는다. cron을 쓰는 Linux도 PATH·cwd·timezone·중복 실행을 명시한다.

## Instagram용 공개 URL 선택

| 후보 | 무료 범위·조건 | 적합성/주의 |
|---|---|---|
| GitHub Pages | Free 공개 저장소 지원. 사이트1GB·월대역폭100GB soft·기본10 builds/시간 soft | 작은 **공개 교육용 JPEG** 예제. 상업 거래/SaaS용 무료 호스팅으로 쓰지 말라는 제한; 상용 대량 미디어 CDN으로 권장하지 않음. 공개 원본·이력 노출 주의 [A047](SOURCES.md#a047) |
| Cloudflare R2 Standard | 월10GB-month, ClassA100만·B1000만, 인터넷 egress 무료. 초과$0.015/GB-month·A$4.50/백만·B$0.36/백만 | 운영 객체 저장 후보. R2 subscription/checkout 필요, ‘카드 없이 영구 무료’ 보장 금지. r2.dev는 개발용·rate limit; 운영은 custom domain 권장, 도메인 비용 별도 [A048](SOURCES.md#a048)[A049](SOURCES.md#a049)[A099](SOURCES.md#a099) |
| Google Cloud Storage | Free Tier 미국 `us-east1/us-west1/us-central1` 합산5GB-month·A5천·B5만·북미발 egress100GB(중국/호주 제외) | **서울 리전은 이 무료 저장 범위가 아님**. 결제계정/프로젝트·조직 public-access prevention·버킷 공개 정책 확인. 초과 과금 [A050](SOURCES.md#a050) |
| Facebook Login 영상 직접 업로드 | resumable binary 경로면 영상 공개 URL 불필요 | 로그인·권한 경로 변경 비용. 이미지·커버 URL까지 해결되는 것은 아님 [A006](SOURCES.md#a006)[A142](SOURCES.md#a142) |

R2 무료량은 Standard에만 적용한다. GCS egress를 과거1GB 값으로 쓰지 않는다. R2/GCS 무료량은 정액 지출 상한이 아니며 Cloud budget은 자동 과금 중지가 아니다. R2의 공개 가격/시작 문서에서 사용자 지정 강제 월상한을 확인하지 못했으므로 저장기간·최대파일크기·요청수를 앱에서 제한하고 Billing 사용량/알림 제공 범위를 사용자 확인 항목으로 둔다. [A031](SOURCES.md#a031) [A132](SOURCES.md#a132)

**추천:** 첫 카드 샘플은 별도 교육용 Pages의 비민감 JPEG. 매일 운영은 사용자가 과금 조건을 확인한 R2 Standard와 기존 도메인 또는 GCS를 선택한다. 신규 도메인 구매를 필수로 만들지 않는다. r2.dev는 시험용임을 표시한다. 로그인 없이 파일 본문을 GET해 읽히는지, `Content-Type`·용량·리디렉션·만료를 확인하고 Meta 처리 완료까지 지우지 않는다. 승인 전 공개하면 안 되는 소재는 교육용 공개 경로에 올리지 않는다.

## ffmpeg 배포·렌더

공식 ffmpeg는 소스를 배포하고 Windows/macOS 빌드 제공자 링크를 안내한다. 운영체제 패키지 관리자/공식 연결 빌드를 고르고 `ffmpeg -version`, `ffprobe`와 필요한 필터/코덱을 확인한다. 임의 다운로드 사이트의 실행 파일을 키트에 재배포하지 않는다. [A053](SOURCES.md#a053)

기본 LGPL과 `--enable-gpl` 등으로 바뀌는 빌드 조건을 구분한다. 바이너리를 동봉하면 해당 빌드의 라이선스·소스 제공 등 의무를 검토한다. 가장 단순한 키트 배포는 **사용자가 설치한 ffmpeg를 호출**하는 방식이다. 폰트 파일의 배포 권리도 별도다. [A054](SOURCES.md#a054)

렌더 설계 제안: H.264/AAC MP4·`+faststart`, 한글 폰트의 명시 경로, 화면 밖 자막 검사·ffprobe 규격 검증. 자막 필터 `libass`·코덱은 빌드에 따라 달라 존재를 확인한다. 로컬 무료 설치와 렌더 시간/전기는 구분한다. A1/A4/A5/A6/A7에 반영한다.
