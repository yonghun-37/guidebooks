# A5v-insta · 심화편 시각자료 보강 계획

범위: `site/advanced/`와 그 아래 전용 자산. 요청에 명시된 이 계획표·결과·검증 증거만 `docs/results/phase-A5v-insta*`에 남긴다. 공통 자산·키트·연구·다른 책·현재 상태 문서는 수정하지 않는다. 기존 A3/A4 기록을 재사용하는 시각자료 보강이며 별도 ADR은 필요하지 않다.

기준: STYLE-GUIDE 6절, DESIGN-advanced 1.2절, A3/A4 결과, 심화편 11페이지와 auto-kit README·SVG·코드·mock 출력. 기존 그림을 모두 누락으로 취급하지 않고, 필요한 연결·실물·판정 근거가 부족한 부분을 보완한다. 숫자는 연구 가정·키트 기본값·실제 mock 출력·편집 제안을 구분한다.

| 장 | 그림 / 현재 공백 | 보여 줄 결론 | 데이터 근거 |
|---|---|---|---|
| A0 | 전체 시스템 지도 교체: 기존 직렬 흐름에 실행기·상태·공급자·알림 연결 부족 | 실행기가 상태를 읽고 제작·호스팅·관문·게시·분석을 잇고, 사람은 알림에서 개입한다 | pipeline.py, state.py, ops/, hosting/, DESIGN 1.2; 각 노드 해당 장 링크 |
| A1 | 상태도 보완: 대기·승인/예약 경로, 재시도와 결과 불명 구별 | 제작 실패는 같은 ID 재개, 검사 실패는 수정 후 새 실행, 발행 불명은 조회한다 | pipeline.py resume/tick/reconcile, publish/instagram.py |
| A1 | 실제 폴더 트리 교체: 실행 폴더만 있던 구조 확장 | 입력 설정·실행 기록·공개 미디어를 구분해서 찾는다 | auto-kit 실제 파일 트리·mock 실행 폴더 |
| A2 | 번호가 있는 API 키 발급 위치 + 설정 핵심 키 주석 | 키는 비공개 .env, 동작·상한은 config.json에서 정한다 | README, config.example.json, research-advanced/generation-apis.md·SOURCES A025/A081 |
| A2 | 지출 상한 계층 그림 교체 | 출력/재시도 제한→실행 최대비 예약→일/월 상한→공급자 강제 상한이 함께 필요하다 | providers/adapters.py, budget 기본 일 $1·월 $10·max_attempts=2·max_output_tokens=2000; costs.md A030/A031/A081/A115 |
| A3 | 입력→실제 JSON 일부→스키마/내용 검사 교체 | 구조화 출력은 모양 검사와 원문 검사를 따로 통과해야 한다 | content.schema.json, samples/insta/draft.json, gates.inspect_text |
| A3 | 편당·월 비용 비교 차트 신설 | 코드 카드 대비 이미지·영상 옵션의 증가분을 먼저 계산한다 | costs.md·cost-model.json, A025/A028/A037; 30편·3000/1000토큰 가정; 고품질 목표안은 배경 1장 재사용 가정 |
| A4 | 기존 실물 카드 갱신 + 릴스 실제 프레임 추가 | 같은 문안이 JPEG 카드와 자막이 있는 MP4로 렌더된다 | 깨끗한 임시 복사본 mock carousel/reel 실행, 실제 JPEG·short.mp4 추출; WebP 각 400KB 이하 |
| A5 | 콘솔 위치 그림 보완: 계정 연결→권한→토큰 번호 | 본인 계정 역할·게시/분석 권한·토큰을 같은 로그인 경로에서 준비한다 | instagram-auth.md A083/A111/A110, 콘솔 캡처 없이 직접 그린 틀 |
| A5 | 기존 시퀀스 보완 + 계정 한도/운영 상한 게이지 | 컨테이너 ID와 게시 ID를 구별하고 더 낮은 남은 한도를 따른다 | instagram-publishing.md A006/A007/A008; 가상 usage=1, 레퍼런스 total=50, 로컬 기본=1 |
| A6 | 관문 흐름 보완: 검사별 실패 사유 + 실제 gates.json | 어떤 검사에서 멈췄는지 passed와 reasons로 확인한다 | gates/__init__.py, 새 mock gates.json, 민감 단어 추가 테스트의 실제 예외 |
| A6 | 운영 모드 전환 그림: 표 대체 | 통과율·미해결 예외·거부/오류를 보고 사람이 모드를 바꾼다 | 기존 A0/A6 편집 제안: 최근 10편 9편, 다음 10편 전부; 플랫폼 보장값·자동 승격 기능 아님 |
| A7 | 하루 타임라인 교체: 분 단위 예와 대기 분기 | 시작 시각과 공개 시각은 다르며 승인/예외에서는 멈춘다 | schedule/install.py, pipeline.tick, review.hours=2; 09:17은 운영 예시, 15분 tick 기본값 |
| A7 | 실행 보고·대시보드·승인/예외 알림 신설: 기존 단일 가상 알림 대체 | 비용·관문·예외·다음 행동을 실제 보고에서 찾는다 | 새 mock dashboard.html·daily-report.json·notification.json, ops/report.py·notifications.py; 전송 없이 로컬 재현 |
| A8 | 개선 고리 보완 + 지표→점수 계산 예 | missing은 보류하고 준비된 views를 분류 점수에 반영한다 | topics/__init__.py, sources.performance_weight=0.25, 실제 mock views=12; log(1+12) 계산, 가상 후보 비교 |
| A9 | 위험별 차단 장치 지도 교체 | 각 위험의 차단 위치와 자동으로 판단하지 못하는 일을 함께 확인한다 | gates/, hosting/, state_sync.py, tokens.py; policy-safety.md A068/A075/A154 |
| E2E | 새 그림 없음 | 진행 체크에는 기존 시스템·관문·운영 그림 링크를 활용한다 | 기존 E2E 구조 유지 |

검증: style_lint, check_site(site), 11페이지 × 1280/375/360px × 라이트/다크. SVG 텍스트 경계·최소 표시 크기·노드 링크 키보드·이미지·콘솔·내부 HTTP·figure 캡션/접근성·각주를 확인한다. 대표 2장과 장별 증거를 저장하고 완료 시 지정 notify.py로 보고한다. 실계정 로그인·유료 API·게시·commit/push는 실행하지 않는다.

실행 상태: 위 표의 보강을 완료했다. A0의 중복 운영 표와 A6의 전환 표를 그림/링크로 정리했고, 기존 E2E에도 그림 링크와 모바일 글자 크기를 반영했다. 검증·실물 출력의 한계·후속 항목은 [결과](phase-A5v-insta.md)에 기록했다.
