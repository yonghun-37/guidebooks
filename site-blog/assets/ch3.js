(() => {
  'use strict';
  const task = document.getElementById('tool-task');
  const suggestions = {
    draft:'ChatGPT Free 새 대화에 내 공식 자료·메모를 넣고 제목·개요·근거표를 받으세요.',
    proof:'ChatGPT의 같은 대화에 검수한 원고를 넣고 수정 전·후·이유 표를 받으세요.',
    image:'미리캔버스 Free에서 무료 템플릿에 내 사진과 제목을 넣고 저장하세요.',
    keyword:'네이버 데이터랩 검색어트렌드에 후보와 같은 기간·기기 조건을 넣고 상대지수를 기록하세요.',
    analytics:'Google Search Console의 검색 실적에서 같은 기간의 노출·클릭·검색어를 확인하세요. 네이버 블로그는 플랫폼 통계를 봅니다.'
  };
  const render = () => {document.getElementById('tool-choice').textContent = suggestions[task.value];};
  task.addEventListener('change', render); render();
})();
