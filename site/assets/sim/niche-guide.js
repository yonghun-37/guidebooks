(() => {
  'use strict';
  const root = document.querySelector('#niche-sim');
  if (!root) return;
  const inputs = [...root.querySelectorAll('[data-plan]')];
  const update = () => {
    const count = inputs.filter(input => input.checked).length;
    const next = ['독자와 반복 질문부터 적으세요.', '비어 있는 기획 항목을 채우세요.', '비어 있는 기획 항목을 채우세요.', '샘플을 보여 주고 구매 의향을 물어보세요.'][count];
    root.querySelector('[data-sim-result]').textContent = `${count}개 · ${next}`;
  };
  inputs.forEach(input => input.addEventListener('change', update));
  for (const [selector, checked] of [['[data-zero]', false], ['[data-all]', true]]) {
    root.querySelector(selector).addEventListener('click', () => {
      inputs.forEach(input => { input.checked = checked; });
      update();
    });
  }
  update();
})();
