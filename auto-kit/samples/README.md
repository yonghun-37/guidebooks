# 키 없이 만든 실행 결과

하린의 가상 계정 「출근길 3분 생활 뉴스」는 **청년 지원금, 신청 전 확인할 3가지** 카드 5장을 만들어요. 도윤의 가상 채널 「자취생 10분 생존법」은 **월급날 10분, 돈을 네 칸으로 나누기** 36초 영상을 만들어요. 직접 작성한 예시 문안·도형·설명용 신호음을 사용해요. 외부 호출과 생성비는 0이에요.

- [인스타 카드 미리보기](insta/preview.html) · [요청 계획](insta/request-plan.json) · [관문](insta/gates.json)
- [쇼츠 재생](shorts/preview.html) · [MP4](shorts/short.mp4) · [자막](shorts/subtitles.srt)
- [대시보드](dashboard.html) · [인스타 지표 CSV](insta/insights.csv) · [쇼츠 지표 CSV](shorts/insights.csv)

실제 제도명·금액·마감일을 넣지 않았어요. 네 칸은 월세·생활비·비상금·목표이며 10분은 메모 활동 시간이에요. 원문·계정·지표는 실제 사례가 아니에요. `example.invalid`는 실제 출처를 채울 자리예요. 쇼츠의 신호음은 낭독이 아니에요. SQLite·토큰·세션 파일은 공개 샘플에 넣지 않아요. PNG는 편집/확인용, API 전송용 카드는 JPEG예요. `missing`은 데이터가 없는 상태이며 숫자 0과 달라요.

원문: [직접 입력](../sources/sample.json) · [생활 뉴스 RSS](../sources/insta-feed.xml) · [네 칸 메모 RSS](../sources/shorts-feed.xml).

Python 3.11 이상에서 재생성: `python examples/build_samples.py`. 이렇게 보이면 성공: `mock 샘플 생성 완료`, 전체 10MB 이하·외부 호출 0.
