(() => {
  'use strict';
  const root = document.querySelector('#time-budget');
  if (!root) return;
  const inputs = ['available', 'overhead', 'per-post'].map(id => root.querySelector('#' + id));
  const result = root.querySelector('[data-sim-result]');
  const update = () => {
    if (inputs.some(input => input.value.trim() === '' || !input.validity.valid)) {
      result.textContent = '시간을 빠짐없이 올바른 분 단위로 입력하세요.';
      return;
    }
    const [available, overhead, perPost] = inputs.map(input => Number(input.value));
    const count = Math.floor(Math.max(0, available - overhead) / perPost);
    result.textContent = `${count}편 · ${count ? '준비·점검을 뺀 시간 안에 연습할 분량입니다.' : '준비·점검 시간을 확보하거나 첫 제작 범위를 줄이세요.'}`;
  };
  inputs.forEach(input => input.addEventListener('input', update));
  root.querySelector('[data-zero]').addEventListener('click', () => {
    inputs[0].value = '0';
    update();
  });
  update();
})();
