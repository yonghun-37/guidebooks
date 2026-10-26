# 키 없이 만든 실행 결과

가상 소식·도형 카드·설명용 신호음으로 만든 작은 샘플이에요. 외부 호출과 생성비는 0이에요.

- [인스타 카드 미리보기](insta/preview.html) · [요청 계획](insta/request-plan.json) · [관문](insta/gates.json)
- [쇼츠 재생](shorts/preview.html) · [MP4](shorts/short.mp4) · [자막](shorts/subtitles.srt)
- [대시보드](dashboard.html) · [인스타 지표 CSV](insta/insights.csv) · [쇼츠 지표 CSV](shorts/insights.csv)

원문·계정·지표는 실제 사례가 아니에요. SQLite·토큰·세션 파일은 공개 샘플에 넣지 않아요. PNG는 편집/확인용, API 전송용 카드는 JPEG예요. `missing`은 데이터가 없는 상태이며 숫자 0과 달라요.

재생성: `python examples/build_samples.py`. 이렇게 보이면 성공: `mock 샘플 생성 완료`, 전체 10MB 이하·외부 호출 0.
