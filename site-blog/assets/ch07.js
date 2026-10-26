(() => {
  'use strict';
  const input = document.querySelector('#thumb-title');
  if (!input) return;
  const render = () => {
    const title = input.value.trim();
    document.querySelector('#thumb-output').textContent = title || '제목을 입력하세요';
    document.querySelector('#thumb-result').textContent = title ? `제목 ${Array.from(title).length}자입니다. 작은 화면에서 사물과 겹치거나 읽기 어려운 부분을 줄이세요.` : '제목을 입력하면 배경 위에 표시됩니다.';
  };
  input.addEventListener('input', render);
  document.querySelector('#thumb-reset').addEventListener('click', () => { input.value = '지원 제도 신청 전 확인'; render(); });
  render();
})();
