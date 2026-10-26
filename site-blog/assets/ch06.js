/* 문장 종류의 시각적 비교. 사용자의 원고나 사실을 자동 판정하지 않는다. */
(() => {
  'use strict';
  const tool = document.querySelector('#draft-tool');
  if (!tool) return;
  const inputs = [...tool.querySelectorAll('[data-highlight]')];
  const render = () => {
    inputs.forEach(input => tool.querySelectorAll(`[data-kind="${input.dataset.highlight}"]`).forEach(mark => mark.classList.toggle('highlight-off', !input.checked)));
    tool.querySelector('[data-draft-result]').textContent = `${inputs.filter(input => input.checked).length}가지 강조가 켜져 있습니다. 내 원고도 사실·경험·표현 순서로 고쳐 보세요.`;
  };
  inputs.forEach(input => input.addEventListener('change', render));
  tool.querySelector('#draft-off').addEventListener('click', () => { inputs.forEach(input => { input.checked = false; }); render(); });
  render();
})();
