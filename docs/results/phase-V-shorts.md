# Phase V-shorts — ShortsBook 시각자료 보강 결과

2026-10-26. [계획](phase-V-shorts-plan.md), `docs/STYLE-GUIDE.md` 6.1·6.2를 적용했다. 페이지별 최소 개수는 폐기하고, 이미 있는 표·폴더 트리·인터랙션으로 충분한 곳에는 새 그림을 넣지 않았다. 사이트 구현·로컬 검증 완료이며 Claude Code 검수 전이다.

## 구현

- 영상 제작에 필요한 샷 크기, 자막 가림·위치, 음성·음악 트랙, 공통 시간축, 비율·해상도, 편집 영역, 출력 설정·완성 파일 대조를 보강했다.
- 중단본의 추가 figure 213개를 검토해 **7개 유지·개선, 키프레임 2개를 1개 비교로 통합, 204개 제거**했다. 기존 figure 11개를 유지하고 새 도식 11개를 추가했다. 최종 30개는 검토 결과 집계이며 목표 개수가 아니다.
- 공통 부품은 `site-shorts/assets/figures.css`, `figure-components.svg`, [사용 안내](../../site-shorts/assets/FIGURES.md)에 모았다. 그림의 번호와 밖의 설명을 연결하고, 2칸 비교는 좁은 화면에서 같은 크기로 위아래 배치한다. 차트 항목명·금액은 다른 줄에 두어 겹침을 없앴다.
- 기존 실습 6 시간축과 실습 8 업로드 순서의 작은 글씨를 모바일에서 읽을 수 있게 다시 배치했다. 업로드 순서 SVG도 `<use>`로 문서의 라이트·다크 색을 따른다.
- 서비스 화면·로고를 복제하지 않았다. 자막 가림은 설명용으로 표시하고 공식 고정 안전 여백으로 제시하지 않았다. 숫자는 기존 본문의 계산·각주·기준월을 공유한다.
- AI 이미지를 새로 생성하지 않았다. 기존 기준/관찰 그림과 중단본의 새싹/마무리 키프레임을 사용한다. 키프레임에는 `AI 생성 예시`, 실제 프롬프트, 참조 이미지와 정지 그림임을 표시했다. 크레딧·생성 기록을 실제 사용 파일에 맞췄다.

## 유지한 그림

이하 경로는 `site-shorts/` 기준이다. ID는 검토·앵커용이며 본문에 작업 단계나 내부 번호를 노출하지 않는다.

| 페이지 | 그림 | 처리 |
|---|---|---|
| `index.html` | 기존 제작 표지·키트 MP4 | 그대로 유지 |
| `chapters/01-map.html` | `v-fig-4` 프로젝트 → MP4 → 업로드 | 중단본 유지 |
| `chapters/02-revenue.html` | `v-fig-8` 내 배정액과 45% | 중단본 유지, 금액·항목 분리 |
| `chapters/06-scenes.html` | 기존 AI 기준/관찰 그림 | 그대로 유지 |
| `chapters/07-editing.html` | `v-fig-63` 발화·자막 끝 맞추기 | 중단본 유지, 막대 안 겹친 글자 제거 |
| `chapters/09-export.html` | 기존 원본/압축 비교 캔버스 | 그대로 유지 |
| `chapters/12-analytics.html` | `v-fig-99` 전체 표본과 계속 시청 | 중단본 유지, 비율의 분모 표시 |
| `practice/05-scenes.html` | 기존 종이 로봇 AI 예시·프롬프트 | 그대로 유지 |
| `practice/06-edit.html` | `practice-timeline` 기존 장면·음성·자막 도식 | 내용·제목 보존, 모바일 배치·테마 개선 |
| `practice/08-publish.html` | `upload-overview` 기존 업로드 6단계 | 순서·내용 보존, 세로 배치·테마 개선 |
| `prompts.html` | 기존 AI 기준/관찰 그림 | 그대로 유지 |
| `ai-models.html` | `v-fig-203/204/205` 결제/배분액·생성 크레딧·시도별 API 비용 | 중단본 유지, 값·항목 분리 및 캡션 근거 |

## 추가·통합한 그림

| 페이지 | ID | 그림이 보여 주는 내용 |
|---|---|---|
| `chapters/05-audio.html` | `audio-tracks` | 말만·음악만·함께 듣기에서 남는 소리 |
| `chapters/06-scenes.html` | `shot-sizes` | 같은 케이블 장면의 전체/가까운 구도 |
| `chapters/06-scenes.html` | `keyframe-comparison` | 이전 `v-fig-189/188`의 새싹 가까운 샷과 마무리 샷 통합 |
| `chapters/08-captions.html` | `caption-placement` | 긴 아래 자막이 가리는 예와 옮기고 줄인 예 |
| `chapters/08-captions.html` | `subtitle-files` | SRT 수정과 MP4 재출력의 다른 경로 |
| `chapters/09-export.html` | `aspect-resolution` | 같은 9:16, 다른 가로·세로 점 수 |
| `chapters/10-templates.html` | `template-layers` | 자막 모양·출력 설정은 남기고 장면·이야기는 교체 |
| `practice/05-scenes.html` | `paper-shot-sizes` | 종이 분류의 전체/손끝 촬영 구도 |
| `practice/06-edit.html` | `editor-regions` | 파일 목록·세로 미리보기·타임라인의 관계와 번호 |
| `practice/07-export.html` | `export-settings` | 9:16·1080p·MP4 선택 → 실제 파일 정보 확인 |
| `practice/08-publish.html` | `published-result` | 같은 영상의 제목·공개·Shorts·주소·재생 확인 |
| `practice/09-api.html` | `api-sequence` | 인증 파일 → 검수·승인 → 드라이런 → 본인이 선택하는 실제 전송 |

## 제거한 그림과 파일

- 이론 15장에 의무로 들어간 인물 삽화와 크레딧의 기준 시트를 모두 제거했다. 대화를 읽는 데 장면 삽화가 필요하지 않았다.
- 각 장의 축 제목·실습 단계·성공 문장을 같은 상자와 화살표에 옮긴 그림, 글만 들어 있는 좋은/나쁜 비교, 안내·용어집·출처·샘플 페이지의 의무 지도는 제거했다.
- 기존 표·계산기·곡선·타임라인을 그대로 반복한 계산 그림, 메뉴를 상자 세 칸에 되풀이한 위치 그림을 제거했다. 구도·자막·편집·출력은 위의 내용별 도식으로 다시 그렸다.
- 키프레임의 도구 지도·실습·프롬프트 부록 중복본은 없애고 이론 7장의 비교와 실제 프롬프트에 모았다. 이미지 자체는 삭제하지 않았다.
- 사용하지 않는 새 파일 **228개(인물 WebP 16개, SVG 사본/틀 212개, 1,558,693바이트)**를 삭제했다. `assets/img/characters/`와 `assets/img/fig/`는 남기지 않았다. 기존 추적 이미지·영상은 보존했고 두 키프레임만 새 자산으로 남았다.

페이지별 **제거한 모든 그림의 ID·캡션, 통합한 2개 그림, 삭제한 모든 파일의 경로·크기**는 [전체 검토 목록](phase-V-shorts/figure-audit.json)에 기록했다. 제거한 그림의 재생성용 프롬프트는 배포 자산에서 제거했다.

## 검증

| 검사 | 실제 결과 |
|---|---|
| `style_lint.py` | 36파일 통과, 금지어·내부 용어·상자 밖 단서 0 |
| `check_site.py --site site-shorts` | 오류 0, 이론 15장·원본 도구 31개·실습 43키·퀴즈 45문항 |
| Chromium 화면 | 전체 HTML 36페이지 × 1280/375/360px × 라이트/다크 = 216회 렌더, 총 1,446개 확인 통과 |
| 가로 넘침·그림 경계 | 접힌 설명을 펼친 상태 포함 오류 0 |
| 새/개선 SVG 글자 | 실제 변환 후 최소 16.54px, SVG 경계 이탈 0 |
| 이미지·오류 | figure 이미지 로드 성공, 콘솔·페이지·내부 HTTP 오류 0 |
| 기존 인터랙션 | 이론 전체 퀴즈 Space 정답, 실습 자막 시간 방향키, 원본 도구 31개 임베드 확인 |
| 본문·조작 보존 | 기준 커밋 `41a8234879a58f6e3d603c114568c0f02c38c930`과 306항목 대조 통과. 크레딧 외 그림 밖 본문·구조, script·입력·버튼·기존 앵커, 원본 JS/CSS 보존 |
| 대표 화면 직접 검토 | 샷 비교·자막 가림·편집 영역·음량·시간축·해상도·키프레임·출력·업로드 순서의 글자와 라이트/다크 확인 |

검사기 `scripts/check_site.py`는 다른 담당자의 변경본을 실행했으며 이 작업에서는 수정하지 않았다. 문체 검사는 시각자료 작업의 어휘·단서 회귀 검사이며, 새 축약 비율 기준선을 만들지 않았다.

[브라우저 결과](phase-V-shorts/browser-check.json) · [정적 결과](phase-V-shorts/check-site.json) · [문체 결과](phase-V-shorts/style-lint.json) · [보존 결과](phase-V-shorts/preservation-check.json) · [재현 명령](phase-V-shorts/commands.md). 스크린샷 41장은 [검증 폴더](phase-V-shorts/)에 있다. 대표: [1280px 라이트 샷 비교](phase-V-shorts/shot-sizes-1280-light.png), [360px 다크 편집 영역](phase-V-shorts/editor-regions-360-dark.png).

## 범위와 남은 확인

다른 책·키트·조사·문체 기준·공유 상태 문서는 수정하지 않았다. 이번 결과 기록을 통합 담당자가 `PROJECT_STATE.md`·서가 진행표에 반영하면 된다. commit/push·배포·실계정 로그인/게시·결제는 하지 않았다. 로컬 Chromium 검증이며 실제 휴대폰·서비스 화면에서의 최종 확인과 Claude Code 검수가 남아 있다.

`scripts/notify.py`로 완료 요약과 대표 스크린샷 2장을 디스코드에 전송했다(HTTP 200).
