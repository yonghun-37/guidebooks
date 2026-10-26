# Phase 4 결과 — 오프라인 스타터 키트

## 범위·요구사항·완료 상태

`docs/DESIGN.md` 6절과 `docs/PLAN.md` Phase 4에 따라 `starter-kit/`을 새로 구현했다. API 키·외부 AI 서비스 없이 합성 RSS 수집부터 문안 후보, 카드, 릴스, 검수 대기, 승인, 드라이런까지 완료하는 것이 이번 단계의 목표다. 기존 Phase 기록 구조를 재사용하며 별도 명세·ADR 구조는 추가하지 않았다.

- [x] 합성임을 표시한 로컬 RSS와 오프라인 규칙 기반 문안
- [x] 카드 PNG 1080×1350 및 API용 JPEG 생성
- [x] 한국어 오픈 폰트·자막·무음 AAC를 포함한 1080×1920 릴스
- [x] REVIEW.md 검수 대기 → approve → 드라이런, 승인 대상 변경 감지
- [x] 실제 생성한 samples/ 미디어와 용량 제한 확인
- [x] 초보자용 Windows/macOS/Linux 설치·실행·오류 안내
- [x] pytest 및 실제 CLI 실행 검증

## 구성과 구현 전략

| 파일 | 구현 |
|---|---|
| `starter-kit/config.example.yaml` | 계정명·색·폰트·RSS·오프라인 문안·무음·실습 길이·AI 표시 선택 |
| `fetch_news.py` | 기본 로컬 RSS 2.0. 명시적 `--online`일 때만 RSS URL 요청. 최대 3개 항목의 제목·링크·짧은 요약·게시일 저장, 본문 페이지 요청 없음 |
| `write_copy.py` | 원문에 없는 사실을 추가하지 않는 후보 추출과 직접 편집용 JSON. API·모델 호출 없음 |
| `render_cards.py` | Pillow 대체 렌더러. 1080×1350 PNG와 게시용 JPEG, 출처·합성 표시, 한국어 줄바꿈과 글자 영역 초과 오류 |
| `make_reel.py` | 정지 카드·별도 자막 영역·무음 AAC → H.264/yuv420p MP4. 기본 24fps·20초, 설정 허용 범위 15~30초. SRT도 저장 |
| `review.py` | 검수 대상 manifest, 다섯 항목 확인을 요구하는 REVIEW.md, 승인 시점·SHA256 저장. 승인 전 게시 및 승인 후 파일 변경 차단 |
| `run_pipeline.py` | 생성 후 검수 대기에서 정상 종료. `render`는 승인 무효화 후 재제작, `approve`는 승인 기록 후 항상 드라이런 |
| `publish.py` | Instagram Login 요청 계획. 캐러셀 자식 생성·상태 확인 → 부모 생성·상태 확인·게시, 이어 릴스 생성·상태 확인·게시. 기본 네트워크 호출 없음 |

기본 실행은 `output/<컴퓨터의 날짜>/`에 생성한다. 기존 폴더는 덮어쓰지 않으며 `--output`으로 새 실행 이름을 지정한다. 설정은 경로와 함께 스냅샷으로 저장한다. 문안을 고치면 `copy.json` 편집 → `render` → 새 검수표 확인 → `approve` 순서다. 재렌더링 실패 때도 이전 승인을 허용하지 않는다.

live는 `--live`와 환경변수 토큰·계정 ID·API 버전 및 공개 HTTPS 미디어 URL을 모두 요구한다. 합성 샘플은 live에서 거부한다. 요청 인증은 헤더로만 전달하고 토큰·오류 응답 전문을 출력하지 않는다. live 시도 기록을 배타적으로 생성해 같은 폴더의 반복 실행을 막고, 컨테이너 상태를 제한된 횟수만 조회한다. 중간 실패의 자동 재게시·복구는 구현하지 않았다. **이번 작업에서는 live·실제 로그인·게시를 실행하지 않았다.**

## 선택 근거와 라이선스

정책·API 설명은 **2026년 10월 조사 기준**이다. `research/FACT-SHEET.md`, `ai-text-image-tools.md`, `ai-video-voice-tools.md`, `graph-api-publishing.md`를 근거로 다음을 선택했다.

- 연구 노트 AI-01·07의 기본 경로에 맞춰 규칙 기반 후보+사람 편집을 채택했다. 외부 LLM 연결은 이 최소 예제에 포함하지 않았다.
- DESIGN이 허용한 대체 렌더러인 Pillow(MIT-CMU, VIDEO-06)를 채택해 브라우저·브라우저 설치 의존성을 없앴다.
- 상업용 한국어 TTS 출력 권리가 미확인인 VIDEO-01~04·10에 따라 무음+자막을 기본 경로로 구현했다. TTS·Whisper·모델 다운로드는 하지 않았다.
- Noto Sans KR 원본 가변 TTF와 SIL OFL 1.1 전문을 동봉했다. Google Fonts의 고정 리비전 원본과 TTF·OFL의 바이트 일치를 확인했고, 출처·SHA256을 `assets/fonts/README.md`에 기록했다. 실행 중 폰트 다운로드가 없다.
- `imageio-ffmpeg` wrapper는 BSD-2-Clause이고 FFmpeg 자체 조건은 별도다. 설치된 7.0.2 바이너리의 `--enable-gpl --enable-version3 --enable-libx264`를 실제 확인했다. 실행 파일은 가상환경에만 있으며 저장소 배포 자산에 포함하지 않는다(VIDEO-07/S090).
- PyYAML(MIT), imageio-ffmpeg(BSD-2-Clause), pytest(MIT)는 설치 패키지의 라이선스 메타데이터·LICENSE와 공식 저장소를 추가 확인했다. 원래 research 노트에 없던 실행 의존성 확인 근거는 키트 README에 구분하여 링크했다. research 파일은 수정하지 않았다.
- 직접 작성한 코드·합성 데이터·샘플에는 키트 범위의 MIT LICENSE를 추가했다. 폰트와 설치 의존성에는 각자의 조건이 적용된다.

API-06에 따라 학습용 PNG를 게시 요청에 그대로 넣지 않고 JPEG를 생성했다. API-08의 생성→상태→게시 순서를 드라이런에 반영했다. API-12의 AI 자기공개 값은 사용자가 검수하는 문안에 보존하며 캐러셀 부모와 릴스에 반영한다. API-13의 별도 광고/파트너십 게시 매개변수는 지원하지 않는다. 계정별 게시 한도를 확정 수치로 하드코딩하지 않았다.

## 설치 환경과 실제 검증

환경: Ubuntu 22.04 x86_64. 시스템 `python3`는 **3.10.12**여서 기존에 설치된 **Python 3.11.15**로 `starter-kit/.venv`를 만들었다. 의존성·캐시는 `starter-kit/.venv`, `starter-kit/.cache`에만 설치·저장했다.

`command -v ffmpeg`, `ffprobe`, `espeak-ng`는 모두 실행 파일을 찾지 못했다. 시스템 패키지 설치는 시도하지 않았다. pip의 `imageio-ffmpeg==0.6.0` 동봉 바이너리 **FFmpeg 7.0.2**로 제작·디코딩했다. ffprobe 없이 실제 MP4를 읽고 전체 프레임 디코딩을 검사했다.

고정한 실행 의존성: Pillow 13.0.0, PyYAML 6.0.3, imageio-ffmpeg 0.6.0. 개발 의존성: pytest 9.1.1.

저장소 루트에서 실행한 최종 테스트:

```bash
starter-kit/.venv/bin/python -m pytest -q -c starter-kit/pytest.ini --basetemp=starter-kit/.cache/pytest-final
```

**16 passed in 2.53s.**

| 검증 | 실제 결과 |
|---|---|
| 네트워크 차단 전체 실행 | socket 연결·게시 urlopen을 차단한 상태에서 소재→문안→PNG/JPEG→MP4→검수 대기→테스트용 체크 처리→승인→드라이런 통과 |
| 검수 전/후 차단 | 승인 없음·체크 누락 거부. 문안·PNG·MP4·검수표·manifest 변경 각각 거부. 재렌더링 실패 시 승인 폐기 확인 |
| 카드 | PNG 4장 각각 1080×1350, JPEG도 같은 크기·실제 JPEG 확인 |
| 실제 영상 | MP4 디코딩: 1080×1920, 24fps, 20.0초, 480프레임, H.264/yuv420p, AAC. 첫 프레임 RGB 크기와 전체 프레임 수 확인 |
| 자막 | 영상 내 자막 이미지 시각 확인, SRT 첫/마지막 시간 0~5초·15~20초 확인 |
| 드라이런 | 14개 요청 단계, 공식 호스트, JPEG/MP4 URL, 생성·상태·발행 순서, caption·children·creation_id·AI 표시 값 확인 |
| 토큰이 환경에 있는 기본 실행 | 네트워크 미호출, 테스트용 토큰 문자열이 출력에 없음을 확인 |
| 입력·실패 | 오프라인 원격 피드 거부, 잘못된/빈/DTD 피드 거부, 지원하지 않는 음성 설정·길이 거부, 기존 결과 덮어쓰기 거부 |
| FFmpeg 대안 | 시스템 실행 파일이 없을 때 .venv 내부 pip 바이너리 선택 확인 |
| 동봉 samples | PNG 4장과 MP4의 실제 규격 및 폴더 전체 10MB 이하 확인 |

추가로 `run_pipeline.py --offline`, `render`, `approve`, 독립 `publish.py`를 실제 CLI로 실행했다. 검수표 체크는 재현 검증용으로 처리했으며 실제 사람의 게시 승인을 받은 것으로 표현하지 않는다. approve·publish의 JSON 출력이 서로 같음을 확인했다. README의 fetch→write_copy→render_cards→make_reel 단계별 명령도 실행해 MP4까지 성공했다. Python 컴파일 검사, 로컬 문서 링크 검사와 `git diff --check`도 통과했다.

카드·영상 프레임을 시각 확인하는 과정에서 가변 폰트 기본값이 Thin인 점을 발견해 Weight 500으로 바꾸고 단어 단위 줄바꿈을 적용했다. 최종 테스트·샘플은 수정된 렌더러 기준이다.

## 산출물과 인계

- [초보자 안내](../../starter-kit/README.md): 터미널·Python 확인, OS별 pip 설치, 가상환경 안 uv 대체 경로, 첫 실행, 검수·문안 편집, 단계별 실행, 오류 표, 도구 선택·라이선스.
- [samples](../../starter-kit/samples/README.md): 카드 PNG 4장, 20초 MP4, SRT, 합성 피드·문안 JSON. 미디어·JSON·자막 합계 **500,433바이트**, 안내문을 포함해도 10MB 미만. 샘플 생성 명령도 기록했다.
- [폰트 출처](../../starter-kit/assets/fonts/README.md), [OFL 전문](../../starter-kit/assets/fonts/OFL.txt), [키트 코드 라이선스](../../starter-kit/LICENSE).
- `starter-kit/.gitignore`는 환경·캐시·생성 결과·개인 설정을 제외한다. 토큰·개인 환경 파일·Hermes 원응답은 추가하지 않았다.

남은 검증 범위는 Windows/macOS 실제 실행, 실제 RSS 제공자별 이용 허락·자료 검수, 실제 계정의 API 권한·공개 호스팅·게시다. 실제 LLM/TTS 연결, 예약 실행, live 실패의 자동 복구는 이 최소 예제에 포함하지 않는다. 향후 작업으로 승인받았다는 의미는 아니다.

사용자의 병행 작업 경계에 따라 `site/`, `research/`, `docs/PROJECT_STATE.md`는 수정하지 않았다. 기존 `docs/prompts/phase-4.md` 변경도 보존했다. commit·push는 시도하지 않았다. Claude Code가 검수 후 커밋한다.

`python3 scripts/notify.py`로 한국어 5줄 보고와 `starter-kit/samples/card-01.png` 첨부를 전송했고 **HTTP 200** 응답을 확인했다.
