# 한국어 음성·자막·영상·카드 렌더링과 라이선스

작성: 2026-10-26, Codex 정리. **2026년 10월 조사 기준**(컷오프: 2026-10-26). Hermes 원응답과 별개인 편집본이다.

- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/ai-video-voice-tools.md`
- SHA256: `2b79ba695521b1277ef62ee595be048831b698811e6f0f1132a01f30a7e44ed6`
- 원응답: `/home/yonghun/project/hermes-research/output/ai-insta-research-20261026/raw/ai-video-voice-supplement.md`
- SHA256: `ce56d5d36d9efbb26c8902cd8637067e4f7ed64b1d9ba7734387f83711e3784b`

## 핵심 사실(출처 각주)

- **VIDEO-01 · 확인함**: eSpeak NG의 개발 언어 문서에는 ko/Korean이 있으며 COPYING은 GPLv3 본문이다. 배포판별 언어·실제 한국어 품질·출력 음성의 별도 권리 조건은 이번 실행에서 검증하지 않았다. [^S082] [^S083]
- **VIDEO-02 · 확인함**: MMS-TTS-KOR 공식 모델 카드는 한국어 체크포인트와 CC-BY-NC-4.0를 명시한다. 비상업 조건이 있는 모델을 상업용 무료 한국어 TTS 기본 경로로 소개하면 안 된다. [^S084]
- **VIDEO-03 · 확인함**: XTTS-v2 모델 카드는 한국어와 Coqui Public Model License를 표시한다. 엔진 코드 라이선스, 모델 운영, 상업 결과물, 참조 음성·화자 동의는 별개이며 CPML 전문·상업 이용 경로는 미확인이다. [^S085]
- **VIDEO-04 · 미확인/추가 조사 필요**: Piper는 개별 음성 MODEL_CARD의 라이선스 확인이 필요하다는 공식 검색 발췌가 있다. 한국어 공식 배포 음성 및 해당 음성의 상업 이용은 확인하지 못했다. 엔진의 구버전과 현행 계열도 구분해야 한다. [^S086] [^S087]
- **VIDEO-05 · 확인함**: Whisper 공식 README는 코드와 모델 가중치 모두 MIT로 공개한다고 명시한다. Whisper는 음성 인식·자막 단계 도구이며 TTS가 아니다. 한국어 오류율이나 완전 오프라인 처리는 실행 검증하지 않았다. [^S088]
- **VIDEO-06 · 확인함**: faster-whisper 코드와 MoviePy는 확인한 파일에서 MIT, Playwright는 Apache-2.0, Pillow는 MIT-CMU로 표시된다. 추가 모델·의존성·브라우저·폰트·이미지·음원의 이용 권리는 별도다. [^S089] [^S091] [^S093] [^S094]
- **VIDEO-07 · 확인함**: FFmpeg 공식 안내는 기본 LGPL2.1 이상, 선택적 GPL 구성 사용 시 GPL 적용을 설명한다. 도구를 실행해 영상을 만드는 것과 라이브러리·바이너리를 제품에 포함·재배포하는 조건을 구분해야 한다. [^S090]
- **VIDEO-08 · Hermes 근거**: Playwright는 페이지·특정 요소 스크린샷을 제공한다. Noto Sans KR의 OFL은 폰트와 제작 문서의 조건을 구분한다. 모든 폰트·템플릿이 같은 권리라는 근거가 되지 않는다. [^S092] [^S095]
- **VIDEO-09 · 미확인/추가 조사 필요**: Remotion 무료/회사 조건, CapCut 소재·음원, Canva 대량 생성 플랜·API·소재 권리는 기준일 적용 전문을 충분히 확보하지 못했다. 유료 플랜 결제를 상업용 소재 전체 허락으로 설명하면 안 된다. [^S096] [^S097] [^S098] [^S099] [^S100]
- **VIDEO-10 · 미확인/추가 조사 필요**: Google Cloud TTS·Azure Speech의 한국 계정 무료량·대상 음성·결제수단·초과 과금은 확인되지 않았다. OS 내장 음성과 오픈 모델의 존재만으로 상업 배포 권리까지 확인된 것은 아니다. [^S101] [^S102] [^S085]

## 수치 표

| 항목 | 값·적용 범위 | 판정·출처 |
| --- | --- | --- |
| 제작 크기·길이 | 카드1080×1350·릴스1080×1920·15~30초 | DESIGN.md의 실습 목표, 플랫폼 유일 규격 아님 |
| eSpeak NG / MMS / XTTS | GPLv3 코드 / CC-BY-NC-4.0 모델 / CPML 모델 | 한국어 지원과 상업 출력 조건을 분리 [^S083] [^S084] [^S085] |
| Whisper·faster-whisper | 코드+원본 가중치 MIT / 실행기 코드 MIT | 추가/변환 모델별 조건 별도 [^S088] [^S089] |
| 렌더링 코드 | MoviePy MIT / Playwright Apache-2.0 / Pillow MIT-CMU | 권리·실행 범위 구분 [^S091] [^S093] [^S094] |
| 클라우드 무료 문자량·한국어 정확도 | 미확인 | 0원·무제한·품질 순위 미제시 [^S101] [^S102] |
| Remotion·Canva 한도 | 무료 인원·회사 가격·대량 행수 미확인 | 판본/출처 상충으로 숫자 미채택 [^S097] [^S099] |

## 한국 가용성

- 한국어 문서/언어 항목과 한국에서의 설치·무료 티어·상업 계약·리전 제공을 별개로 확인한다. 실제 로컬 설치·합성·자막·MP4 생성은 수행하지 않았다.
- 상업용 한국어 TTS 기본 경로의 출력 권리를 끝까지 확인하지 못했다. 직접 녹음·무음 대안은 실습 설계 제안으로 남기며 TTS 권리 확인 완료로 표시하지 않는다.

## 불확실·상충

- 초기·보충 Hermes는 프록시403과 본문 잘림으로 핵심 라이선스 확인에 실패했다. 확인함은 Codex가 직접 읽은 파일 범위다.
- eSpeak 출력 음성 약관, Piper 한국어 음성, XTTS CPML 전문·계약·화자 동의, OS 음성 상업 배포, 클라우드 한국 무료량은 남아 있다.
- Canva Bulk Create의300행/150열과다른경로60열 검색표현이 혼재하며 API 대상 플랜 변경일도 미확인이다. 확정 한도로 쓰지 않는다. [^S099]
- 코드·가중치·학습 데이터·입력 자산·출력물·화자 권리를 한 라이선스 이름으로 일괄 승인하지 않는다.

## 교과서 반영 포인트(장 번호)

- 7~8장: HTML/CSS→Playwright 캡처 또는 Pillow 카드를 FFmpeg 영상 후보와 연결하되 실제 실행은 후속 Phase에서 검증한다.
- 8장: 본인 녹음·무음 경로를 먼저 검토하고 라이선스가 검증된 음성만 선택 실습에 추가하는 방향을 설계자에게 제안한다.
- 8장: 자막의 인명·수치·부정·무음 구간·타임스탬프와 휴대폰 가독성을 사람 검수 항목으로 둔다.
- 7~12장: 자산별 공식 URL·버전·라이선스·상업/광고/재배포 허락을 기록하는 장부를 제안한다.

[^S082]: [eSpeak NG Languages](https://raw.githubusercontent.com/espeak-ng/espeak-ng/master/docs/languages.md) · eSpeak NG · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Codex raw 본문의 ko/Korean 행·배포판 언어 확인 지침 확인; 설치판 실제 동작 미검증. 전체 메타데이터: [SOURCES.md](SOURCES.md#s082).

[^S083]: [eSpeak NG COPYING](https://raw.githubusercontent.com/espeak-ng/espeak-ng/master/COPYING) · eSpeak NG · 게시·갱신: 파일 갱신일 미상; GPLv3 본문 버전2007-06-29 · 접근: 2026-10-26 · A · Codex raw GPLv3 본문 확인; 엔진 배포 조건이며 음성/참조자료 권리 일괄 승인 아님. 전체 메타데이터: [SOURCES.md](SOURCES.md#s083).

[^S084]: [MMS Korean TTS Model Card](https://huggingface.co/facebook/mms-tts-kor/raw/main/README.md) · Meta / Facebook 공식 모델 저장소 · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Codex raw 본문에서 한국어 체크포인트·CC-BY-NC-4.0 확인; 상업 기본 경로에서 제외. 전체 메타데이터: [SOURCES.md](SOURCES.md#s084).

[^S085]: [XTTS-v2 Model Card](https://huggingface.co/coqui/XTTS-v2/raw/main/README.md) · Coqui 공식 모델 저장소 · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Codex raw 본문 Korean 및 CPML 표시 확인; CPML 전문·상업 계약·화자 동의 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s085).

[^S086]: [Piper VOICES](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md) · OHF-Voice / Piper · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 발췌만; 개별 MODEL_CARD 필요, 한국어 공식 음성·현행 엔진 전문 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s086).

[^S087]: [Piper CHANGELOG](https://github.com/OHF-Voice/piper1-gpl/blob/main/CHANGELOG.md) · OHF-Voice / Piper · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 발췌의 GPLv3 전환 표시만; 정확한 릴리스 경계 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s087).

[^S088]: [Whisper README License](https://raw.githubusercontent.com/openai/whisper/main/README.md) · OpenAI / Whisper · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Codex README 끝 License 절에서 코드·가중치 모두 MIT 확인; 한국어 정확도·네트워크 차단 실증 없음. 전체 메타데이터: [SOURCES.md](SOURCES.md#s088).

[^S089]: [faster-whisper LICENSE](https://raw.githubusercontent.com/SYSTRAN/faster-whisper/master/LICENSE) · SYSTRAN / faster-whisper · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Codex raw MIT 라이선스 확인; 변환/추가 모델과 의존성의 권리는 별도. 전체 메타데이터: [SOURCES.md](SOURCES.md#s089).

[^S091]: [MoviePy LICENCE.txt](https://raw.githubusercontent.com/Zulko/moviepy/master/LICENCE.txt) · MoviePy / Zulko · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Codex MIT 원문 확인; FFmpeg·외부자산 권리와 실제 편집 API는 별도. 전체 메타데이터: [SOURCES.md](SOURCES.md#s091).

[^S093]: [Playwright LICENSE](https://raw.githubusercontent.com/microsoft/playwright/main/LICENSE) · Microsoft / Playwright · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Codex Apache-2.0 라이선스 원문 확인; 브라우저·폰트·이미지 권리는 별도. 전체 메타데이터: [SOURCES.md](SOURCES.md#s093).

[^S094]: [Pillow LICENSE](https://raw.githubusercontent.com/python-pillow/Pillow/main/LICENSE) · Pillow 프로젝트 · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Codex MIT-CMU 라이선스 및 저작권/고지 유지 조건 원문 확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s094).

[^S090]: [FFmpeg License and Legal Considerations](https://www.ffmpeg.org/legal.html) · FFmpeg · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Codex 본문 LGPL2.1+·선택 GPL·libx264 등 확인; 사용할 바이너리·한국 codec 특허 조건은 별도. 전체 메타데이터: [SOURCES.md](SOURCES.md#s090).

[^S092]: [Screenshots | Playwright](https://playwright.dev/docs/screenshots) · Microsoft / Playwright · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes page/locator screenshot 원문 확인; 로컬 렌더링 실증 없음. 전체 메타데이터: [SOURCES.md](SOURCES.md#s092).

[^S095]: [Noto Sans KR OFL.txt](https://github.com/google/fonts/blob/main/ofl/notosanskr/OFL.txt) · Google Fonts / Adobe · 게시·갱신: 파일 갱신일 미상; SIL OFL1.1 본문2007-02-26 · 접근: 2026-10-26 · A · Hermes 라이선스 원문 일부; 실제 배포 폰트 파일과 대응 확인 필요. 전체 메타데이터: [SOURCES.md](SOURCES.md#s095).

[^S096]: [Remotion License FAQ](https://www.remotion.dev/docs/license/faq) · Remotion · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색만; 무료/회사 조건의 기준일 판본 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s096).

[^S097]: [Remotion Terms](https://www.remotion.dev/docs/terms) · Remotion · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색의 v5.0 표기·시행일 미확인; 무료 인원·가격 숫자 채택 보류. 전체 메타데이터: [SOURCES.md](SOURCES.md#s097).

[^S098]: [CapCut 소재 라이선스 약관(확인 대상)](https://www.capcut.com/clause/material-license-agreement) · CapCut · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 원문 접근 실패; 소재·음원 상업/광고/지역 조건 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s098).

[^S099]: [Create designs in bulk](https://www.canva.com/help/bulk-create/) · Canva · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 검색 발췌; 대상 플랜·데스크톱 조건, 무료·한국 가용성 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s099).

[^S100]: [Canva Content License Agreement(확인 대상)](https://www.canva.com/policies/content-license-agreement/) · Canva · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 원문 접근 실패; 무료/Pro소재·템플릿 재판매·음원 권리 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s100).

[^S101]: [Google Cloud TTS Pricing(확인 대상)](https://cloud.google.com/text-to-speech/pricing) · Google Cloud · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 원문 접근 실패; 무료 문자량·대상 음성·한국 결제 조건 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s101).

[^S102]: [Azure Speech Pricing(확인 대상)](https://azure.microsoft.com/ko-kr/pricing/details/cognitive-services/speech-services/) · Microsoft Azure · 게시·갱신: 날짜 미상 · 접근: 2026-10-26 · A · Hermes 원문 접근 실패; F0 무료 범위·한국어 음성·지역 조건 미확인. 전체 메타데이터: [SOURCES.md](SOURCES.md#s102).
