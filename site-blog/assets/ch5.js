(() => {
  'use strict';
  const reasons = {
    broad:'검색수는 가장 크지만 “지원금” 전체를 설명할 자료는 부족합니다. 대상과 신청 단계로 좁혀 내가 확인한 안내에 맞는 질문을 먼저 고르세요.',
    specific:'첫 글에 맞는 선택입니다. 검색수보다 확인한 대상·서류·신청 경로로 답할 수 있다는 점이 이유입니다. 공식 제도명을 확인해 제목과 본문을 완성하세요.',
    thin:'문서 수와 광고 경쟁도는 낮지만 지급 일정 자료가 없습니다. 숫자가 작다는 이유로 지급일을 만들지 말고 해당 제도의 공식 안내부터 확인하세요.'
  };
  document.querySelectorAll('input[name="keyword"]').forEach(input => input.addEventListener('change', () => {
    document.getElementById('keyword-result').textContent = '1개 선택';
    document.getElementById('keyword-reason').textContent = reasons[input.value];
  }));
})();
