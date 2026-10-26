# ShortsBook 시각자료 부품

기준은 `docs/STYLE-GUIDE.md` 6절이다. 그림 개수 목표는 없다. 새 그림을 만들기 전에 기존 도구·표가 같은 내용을 이미 보여 주는지 확인한다.

- `figures.css`: `book-figure`와 결론 캡션, `v-compare`/`v-panel`의 같은 크기 비교, `v-steps` 단계 띠, `v-svg`와 차트·파형·선·번호 스타일이다. 680px 이하에서는 비교를 위아래로 배치해 글자를 줄이지 않는다.
- `figure-components.svg`: `screen-frame`은 서비스와 무관한 화면 틀, `number-circle`은 번호 배경이다. `egg-rice`는 간장 계란밥의 전체·가까운 샷, `money-card`는 대표 해설의 네 칸 메모다.
- `upload-flow.svg#upload-flow`: 실습 8의 업로드 순서다. `<img>` 대신 제목이 있는 바깥 SVG에서 `<use>`로 불러와 문서의 테마 색을 물려받는다.
- `--fig-main/alt/warn/good/bad/grid`와 본문의 `--surface/ink/soft/muted`를 쓴다. 외부 심벌에도 같은 변수가 전달된다. 새 색이 필요하면 라이트·다크 값을 함께 정한다.

```html
<figure class="book-figure" id="설명할-내용">
  <svg class="v-svg" viewBox="0 0 300 240" role="img"
       aria-label="번호 1은 파일 목록, 번호 2는 결과 미리보기">
    <title>작업 영역의 관계</title>
    <use href="../assets/figure-components.svg#screen-frame"
         width="300" height="240"/>
    <!-- 번호 원 위의 글자와 해당 작업 영역은 본문에 맞춰 직접 추가한다. -->
  </svg>
  <figcaption>그림이 보여 주는 결론 한 문장과 필요한 출처 각주.</figcaption>
</figure>
```

`v-svg`의 본문 글자는 19, 보조 글자는 18을 기본으로 한다. viewBox를 크게 잡고 통째로 축소하지 않는다. 실제 360px 화면에서 변환 후 글자 크기와 경계를 검사한다. 차트는 같은 단위끼리 영점에서 그리고, 값과 항목명을 다른 줄에 두어 긴 숫자가 겹치지 않게 한다. 숫자는 본문의 근거·가상 계산을 공유하고 캡션에 기준월·각주를 단다.

화면 그림은 정확한 서비스 배치로 안내하지 않는다. 번호와 밖의 설명을 연결한다. AI 래스터는 실제 프롬프트·참조와 `AI 생성 예시`를 함께 공개한다. 두 추가 키프레임의 기록은 `img/visual-provenance.json`, 기존 기준 이미지 기록은 `img/ai-examples/y4ai-prompts.json`이다.
