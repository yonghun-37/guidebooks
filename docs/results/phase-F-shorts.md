# ShortsBook 검토 반영과 최종 게이트

2026-10-26 · 작업자 Codex · 검토 기준: [독립 검토](phase-R-shorts-findings.md), STYLE-GUIDE 5절, DESIGN 12절.

**차단 1건·혼란 6건·사소 2건, 총 9건을 모두 수정했다. 요청된 정적·문체·브라우저·키트 게이트를 통과했다.** 외부 서비스 실계정 제작·게시 성공을 뜻하지 않는다.

수정 범위는 `site-shorts/`와 이 결과 문서다. `shorts-kit/`은 검증 결과 코드 수정이 필요하지 않았다. 기존 README 변경, 다른 작업자의 `site/`·검토 산출물을 보존했다. 공용 스크립트·프로젝트 상태·서가·연구 원장은 수정하지 않았다. commit/push하지 않았다.

## 최종 게이트

| 게이트 | 결과 | 실제 확인 범위 |
|---|---|---|
| `check_site(site-shorts)` | 통과 | HTML 38개, 내부 참조 3,461개, 이론 15장, 원본 도구 31개, 퀴즈 45문항, 실습/E2E 43키. 오류 0 |
| `style_lint` | 통과 | 본문·부록 HTML 35개, 금지어·내부 용어·대상 단서 표현 0 |
| 1280/375/360px | 통과 | 현행 본문·부록 33페이지 × 3너비 × 라이트/다크. 접힌 내용 펼침·목차 열림 포함, 가로 넘침 0 |
| 다크 모드 | 통과 | 같은 33페이지, 임베드 도구 테마 전달, 추가된 AI 음성 분기와 모바일 본문 확인 |
| 콘솔·페이지·내부 HTTP | 통과 | 브라우저 검사에서 오류 0 |
| 키보드·상호작용 | 통과 | 목차 Enter/Escape, 퀴즈 45문항 Space·초기화, 원본 도구 31개/3너비 초점·슬라이더, OS 탭 End, 복사·검색·진행/주소 복원·삭제, JS 없는 읽기·저장 차단. 전체 검사 **3,554개 확인**, 내부 링크 956개 |
| 수정 항목 집중 검사 | 통과 | **69개 확인**. 네 샷 복사문·파일 연결, 두 페이지의 AI 표시/음성 분기·초기화, 비용 토큰 링크·API 상세 키보드, 유형 저장/복원/전체 삭제·저장 차단 등 |
| `shorts-kit` pytest | 통과 | 깨끗한 임시 복사본, Linux Python 3.10.12, 새 도구 가상환경에서 **38 passed in 8.63s** |
| 키트 README 실행 | 통과 | 오프라인 생성·프롬프트 파일 생성·미검수 승인 거부·재출력·가상 자료 승인·기본 드라이런·일일 생성·Windows/macOS 예약 명령 안내. 드라이런 `network_calls: 0`, `privacyStatus: private` |
| 키트 실제 MP4 | 통과 | 새 출력 파일을 Chromium에서 재생. 1080×1920·36초, 자막·자체 도형 미리보기 확인. 동봉 가상 예의 무음 영상 |
| 변경 형식 | 통과 | 변경한 사이트·키트 범위 `git diff --check`, 수정 JS 구문 검사 |
| 과거 대비 이론 분량 70% | 비교 불가 | ShortsBook 개편 전 기준선이 없다. 다른 책의 기준선이나 현행본으로 기준선을 만들지 않았다. 이 항목의 통과를 주장하지 않는다 |

브라우저는 Chrome for Testing 149.0.7827.55와 Playwright를 사용했다. 33페이지는 표지·이론 15장·실습 0~10/E2E·실험실·용어집·프롬프트·모델 비용·출처이며, 준비 중 페이지와 샘플 미리보기는 이 페이지 수와 구분했다. 샘플은 별도 재생 확인했다.

## 항목별 해결

| 항목 | 수정 내용 | 재확인 |
|---|---|---|
| **SB-R-01 차단** | [실습 6 모바일 프로젝트](../../site-shorts/practice/06-edit.html#mobile-project)에 장면 가져오기 → 기기 녹음/직접 음성 해설 → [분할·삭제·배치](../../site-shorts/practice/06-edit.html#mobile-cut) → [원본·음성·음악 볼륨](../../site-shorts/practice/06-edit.html#mobile-volume)을 추가했다. 기존 자막 절과 [실습 7 품질 선택·기기 저장](../../site-shorts/practice/07-export.html#mobile-export)으로 연결했다. 입력 파일·완료 확인·파일을 찾지 못할 때 직접 녹음하는 대안도 안내한다 | 추가 앵커·메뉴·파일 안내, 360px 본문·다크 화면, 내부 링크 확인. 메뉴가 달라질 수 있는 부분은 후보명·공식 도움말 제공. 앱 실기기 실행은 미검증 |
| **SB-R-02 혼란** | [실습 2 시험 MP4](../../site-shorts/practice/02-setup.html#test-export)에 사진 가져오기·타임라인·1080p 내보내기·`test.mp4` 재생을 PC/폰 각각 적었다. 프로젝트 저장과 MP4 저장을 직답으로 구분했다 | 성공 기준도 편집기 밖 MP4 재생으로 통일. 실습 6~7 상세 앵커 확인 |
| **SB-R-03 혼란** | [실습 3](../../site-shorts/practice/03-script.html#prompt)에 유형 직접 입력을 넣고 생성형은 [로봇 네 샷](../../site-shorts/prompts.html#story-example)으로 연결했다. 네 샷의 읽을 말·장면·자막·`shot-01.mp4`~`shot-04.mp4`를 공통 예로 제공했다. 실습 4는 예문 대신 내 `script.txt`를 읽도록 명시, 실습 5는 같은 네 샷·파일명·4×2×20=160크레딧으로 수정했다 | 실제 복사문에 네 해설 모두 포함. 실습 4의 공통 대본 링크, 실습 5 네 파일·샷 02 고개 동작·비용 계산 확인. 낭독 시간은 독자가 재서 장면 길이를 조절 |
| **SB-R-04 혼란** | [비용식](../../site-shorts/ai-models.html#cost-types)의 토큰을 새 [AI 사용량 토큰](../../site-shorts/glossary.html#ai-token) 항목으로 연결했다. 인증 토큰은 별도 제목·API 실습 역링크로 구분했다 | 비용식에 인증 토큰 링크 0, 키보드로 사용량 정의 이동 확인. 용어집 49개 |
| **SB-R-05 혼란** | [이론 업로드](../../site-shorts/chapters/11-upload.html#upload-tool)·[실습 8](../../site-shorts/practice/08-publish.html#upload-tool)에 비현실적 삽화·TTS 선택과 음성 조건 질문을 추가했다. 본인 음성, 타인 복제, 실제 발언처럼 들리는 합성, 일반 TTS, 모름을 구분한다. 여러 사용이 섞이면 공개 필요 항목을 우선 고르게 했다. 이론 메타데이터 도구도 미결정 음성을 남은 항목으로 센다 | 두 페이지 모두 삽화+본인 음성의 아니요, 타인 복제/오인 합성의 예, 일반 TTS의 확인 보류·공식 예시 안내, AI 음악의 예, 숨긴 질문 비활성·초기화 확인. 일반 TTS를 일괄 면제하지 않음 |
| **SB-R-06 혼란** | [이론 7 FAQ 4](../../site-shorts/chapters/06-scenes.html#faq-4)를 Flow 한국 제공·18세·무료 접근 확인·일 50/네 샷 80크레딧·무료 대안 순으로 직답했다. [계정 FAQ 5](../../site-shorts/practice/01-account.html#faq-5)는 채널 생성·요구되는 기능 인증·수입 활동의 등록 확인을 지금/요구될 때/수입 활동 때 표로 분리했다 | FAQ 첫 문장·구체 예·다음 행동, 실습 생성 표로의 링크 확인. 기존 연구 근거를 유지하고 채널·세무 공식 안내도 재열람 |
| **SB-R-07 혼란** | [모델·비용 부록](../../site-shorts/ai-models.html#bundles)의 본문 빈값·본문 대조·URL 셸·초 연결 등 조사 메모를 제거했다. 불확실한 값은 요금표/결제창·모델 카드·플랜 약관·파일 표시 도움말의 어떤 항목을 볼지로 바꿨다. 구독표와 모델 6분류에 확인할 점을 모으고 API 비용 상세 83개를 접었다. 원문 대조가 끝나지 않은 검색 단가도 확정 가격으로 남기지 않았다 | 모델 271개·구독 24개 유지, 해당 조사 메모와 `확인 필요` 반복 0. Veo 검색 6행·초기화 271행, 분류/API 상세 Enter 조작 확인. `/count`는 `/초`로 자동 환산하지 말도록 안내. 모든 가격의 새 전수 검증을 주장하지 않음 |
| **SB-R-08 사소** | 협찬 문장의 일반 명사 서비스 링크를 빼고 [AI 도구 지도](../../site-shorts/chapters/02b-ai-tools.html#question)의 ‘AI 서비스’에 연결했다. 용어집 제목·역링크도 맞췄다 | 수익 장 일반 서비스 링크 0, 도구 지도 문맥 링크 1 |
| **SB-R-09 사소** | 기존 실습 저장 키 안에 선택한 유형을 저장·복원한다. 다른 페이지를 거쳐도 보존하고, 실습 전체 기록 삭제 시 유형과 설명도 기본값으로 되돌린다 | 생성형 선택·체크 후 새로고침, 다른 실습 왕복, E2E 전체 삭제, 저장 차단 상태의 현재 선택·안내 확인 |

**미수정 검토 항목은 없다.** R-01은 본문 안내의 차단 해소이며 Create 실계정의 성공 검증은 아니다. R-05의 일반 TTS는 근거 없이 예/아니요를 자동 확정하는 대신, 실제 음성과 공식 기준을 대조하도록 안내한다.

## 추가로 대조한 공식 자료

기존 연구의 Y342/Y343/Y382(Flow), Y043/Y057(채널/세무), Y013/Y363(AI 공개)을 유지했다. 모바일 절차 보완은 2026-10-26 아래 공식 본문과 대조했으며 새 숫자·유료 한도를 만들지 않았다. 연구 원장은 다른 작업자의 범위이므로 수정하지 않았고, 새 모바일 절차의 근거는 이 기록과 실습의 직접 링크에 남겼다.

- [Create 프로젝트 만들기](https://support.google.com/youtube/answer/13521789): 갤러리·다른 앱 파일·가져오기.
- [Create 오디오 추가·편집](https://support.google.com/youtube/answer/13521394?hl=ko): 사운드의 기기 파일 탭, 직접 음성 해설, 오디오 분할·볼륨·페이드·삭제·영상보다 긴 오디오 제한. 별도 녹음 파일이 목록에 안 보일 때 직접 녹음하는 대안은 이 절차를 사용한다.
- [Create 저장·내보내기](https://support.google.com/youtube/answer/13521602): 더보기 → 내보내기 → 품질 선택 → 내보내기. 1080p 메뉴 노출 자체는 기기에서 확인하도록 안내한다.
- [AI 사용 공개](https://support.google.com/youtube/answer/14328491?hl=ko): 비현실적 생성과 사실적 합성·AI 음악·본인 음성 복제 예시. 로봇 삽화의 분기는 이 기준을 가상 예에 적용한 판단이다.
- [채널 만들기](https://support.google.com/youtube/answer/1646861?hl=ko), [국세청 1인 미디어 세무 안내](https://t.nts.go.kr/nts/cm/cntnts/cntntsView.do?cntntsId=7802&mi=2480): 채널 개설 절차와 수입 활동의 세무 확인을 분리한다.

## 실행 기록과 제약

저장소 루트에서 실행:

```bash
python3 scripts/check_site.py --site site-shorts --output /tmp/shorts-final-check-site.json
python3 scripts/style_lint.py site-shorts/chapters/*.html site-shorts/practice/*.html site-shorts/{index,prompts,ai-models,glossary,lab,credits}.html --output /tmp/shorts-final-style-lint.json
git diff --check -- site-shorts shorts-kit
```

브라우저는 `python3 -m http.server 8876 --bind 127.0.0.1 --directory /home/yonghun/project/ai-insta`로 제공했다. 기존 [Y5 브라우저 검사](phase-Y5/verify-browser.mjs)의 서버·출력 경로와 용어 수(48→49)를 바꿔 재실행했다. 추가 69개 시나리오와 스크린샷은 `/tmp/shorts-final-gate/`, JSON 정적 결과는 위 명령의 `/tmp/` 경로다. 임시 증거 파일은 저장소에 추가하지 않았고, 항목별 결과는 이 문서에 보존했다.

키트는 `/tmp/shorts-final-kit-khi34xgi/shorts-kit`에 개인 설정·입출력·인증·기존 가상환경을 제외하고 복사했다. `/tmp/shorts-final-tools` 가상환경에 `requirements-dev.txt`를 설치하고 복사본에서 `python -m pytest -q`와 README 명령을 실행했다. 가상 예의 명시적 판단값·검수 체크는 드라이런 회귀 시험용이며 실제 게시 승인이 아니다.

남은 제약:

- Windows/macOS·휴대폰 실기기, ChatGPT/Vrew/Flow/Runway/Clipchamp/Create 실계정 제작, 실제 로그인·결제·공개 게시·OAuth/live 호출·OS 예약 등록은 실행하지 않았다. 유료 API·새 결제를 사용하지 않았다.
- 이론 분량 70%의 과거 기준선 비교는 불가하다. 현재 문체 자동 검사는 그 비교와 구분한다.
- 공용 `scripts/build_appendices_shorts.py`는 기존 `토큰→auth-token`, `서비스→service` 자동 연결·48개 용어 정의로 용어집을 생성한다. 요청한 파일 소유 범위에 따라 이 생성기는 변경하지 않았다. 향후 부록을 재생성할 때는 통합 담당자가 R-04/R-08의 문맥별 연결과 새 `ai-token` 정의를 생성기에 반영해야 한다. 이번 게이트는 현재 사이트 파일 기준이다.
- 공용 `docs/PROJECT_STATE.md`와 서가 진행표의 통합 반영·Claude Code 검수·커밋·배포는 이 작업 범위 밖이다.

## 완료 알림

`python3 scripts/notify.py "✅ [ShortsBook 최종 수정 완료] ..."`로 한국어 4줄을 전송했다. HTTP 200, 메시지 ID `1564163157130485782`를 확인했다. 토큰은 출력·기록하지 않았다.
