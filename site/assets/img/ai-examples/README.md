# AI 생성 예시와 실제 생성 지시문

2026-10-26 내장 이미지 생성 도구로 새로 제작했다. 외부 API 키·결제를 사용하지 않았다. 실제 도시·교통기관·정책 현장의 사진이 아니다. 홈페이지·교과서의 AI 생성 예시 고지는 플랫폼의 AI 공개 설정과 구분한다.

| 파일 | 용도 | 크기 | 바이트 |
|---|---|---|---|
| commute-card.webp | 신청 체크 카드 배경 | 960×1200 | 132242 |
| commute-reel.webp | 같은 주제의 릴스 시작 프레임 | 720×1280 | 61940 |

원본 PNG를 WebP로 변환·축소했다. 두 번째는 9:16으로 크롭했다. 아래는 내장 도구에 전달한 실제 지시문이다. 본문의 한국어 프롬프트는 같은 구도를 따라 만들기 위한 축약 지시문이다.

## 카드 배경

```text
Use case: photorealistic-natural. Create one portrait editorial background photograph for a Korean commuter life-news information card, 4:5 composition. An anonymous modern city bus stop and glass office buildings in soft early morning light, no recognizable landmarks, no people, no signs, no text, no logos, no brands. Restrained deep navy, slate blue, cream and a warm sunrise accent. Keep the upper half visually quiet and light so headline text can be added separately; detailed city scenery in the lower half. Premium realistic editorial photography, calm and credible, never a dramatic news event. This is an AI illustrative background, not documentary evidence.
```

## 릴스 기준 장면

```text
Use case: photorealistic-natural. Asset type: portrait 9:16 opening frame for a commuter life-news explainer reel called 'three things to check before applying for youth support'. A fictional anonymous modern city at sunrise, seen through a clean train window from an empty seat. In lower foreground an unbranded dark blue commuter bag, beyond the window midrise office buildings and an abstract bus stop with no signs. Upper third quiet pale morning sky, middle buildings leave clear negative space for separately added captions. Credible premium editorial photography with natural soft warm light, navy/slate/cream palette. No identifiable people, faces, brands, logos, text, numbers, recognizable real landmarks or official emblems. No evidence-of-an-event appearance. The scene will be animated later with just passing morning light; do not render text.
```

카드 배경 사본은 starter-kit/samples/commute-card.webp에도 동봉한다. 교과서의 예시 문안과 배경은 특정 기관의 정책 홍보물·승인 자료가 아니다. 생성 영상 프롬프트는 제작 연습용이며, 이 작업에서 외부 영상 생성 서비스를 실행하지 않았다.
