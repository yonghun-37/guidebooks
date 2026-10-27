/* 4장 순서 안내. 정상/안전/산통 판정을 내리지 않는다. */
(() => {
  'use strict';
  const steps = [...document.querySelectorAll('#crying-steps li')], result = document.querySelector('#crying-result');
  const next = document.querySelector('#crying-next'), reset = document.querySelector('#crying-reset');
  if (!steps.length || !result || !next || !reset) return;
  let index = 0;
  const render = () => {
    steps.forEach((step, n) => { if (n === index) step.setAttribute('aria-current', 'step'); else step.removeAttribute('aria-current'); });
    result.textContent = `지금 확인 ${index + 1}/${steps.length} · ${steps[index].textContent} 계속되면 연락. 급한 신호가 보이면 즉시 공통 응급 안내를 따릅니다.`;
    next.disabled = index === steps.length - 1;
  };
  next.addEventListener('click', () => { index = Math.min(index + 1, steps.length - 1); render(); });
  reset.addEventListener('click', () => { index = 0; render(); });
  render();
})();
