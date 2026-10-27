/* 생성된 전체 용어에서 검색한다. 입력은 저장하지 않는다. */
(() => {
  'use strict';
  const input = document.querySelector('#term-search');
  const entries = [...document.querySelectorAll('[data-glossary-entry]')];
  const render = () => {
    const query = input.value.trim().toLocaleLowerCase();
    entries.forEach(entry => { entry.hidden = !entry.dataset.search.toLocaleLowerCase().includes(query); });
    document.querySelector('#term-count').textContent = `${entries.filter(entry => !entry.hidden).length}/${entries.length}개 용어`;
  };
  input.addEventListener('input', render);
  // 직접 앵커로 열 때도 해당 항목을 먼저 보여 준다.
  window.addEventListener('hashchange', () => { input.value = ''; render(); });
  render();
})();
