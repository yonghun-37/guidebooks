(() => {
  'use strict';
  const search = document.querySelector('#term-search');
  const category = document.querySelector('#term-category');
  const entries = [...document.querySelectorAll('[data-glossary-entry]')];
  const normalize = text => text.normalize('NFKC').toLocaleLowerCase('ko').trim();
  const update = () => {
    const query = normalize(search.value);
    entries.forEach(entry => { entry.hidden = !(normalize(entry.dataset.search).includes(query) && (!category.value || category.value === entry.dataset.category)); });
    const count = entries.filter(entry => !entry.hidden).length;
    document.querySelector('#term-count').textContent = `${entries.length}개 용어 중 ${count}개 · 가나다순 (영문 약어는 한국어 발음 순서)${count ? '' : ' · 검색 결과가 없습니다.'}`;
  };
  const revealAnchor = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    if (target?.matches('[data-glossary-entry]')) {search.value = ''; category.value = ''; update(); target.scrollIntoView();}
  };
  search.addEventListener('input', update); category.addEventListener('change', update);
  window.addEventListener('hashchange', revealAnchor); update(); revealAnchor();
})();
