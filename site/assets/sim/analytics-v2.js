/* 11장 전용: 같은 관찰 조건의 저장·공유 비율만 계산한다. */
(() => {
  'use strict';
  ReelsSim.mount('#analytics-sim', (element, report) => {
    const inputs = [...element.querySelectorAll('input')];
    const update = () => {
      if (inputs.some(input => input.value.trim() === '' || !input.checkValidity())) {
        report('— · 비어 있거나 잘못된 값을 확인하고 다시 입력하세요.');
        return;
      }
      const [reach, saved, shares] = inputs.map(input => Number(input.value));
      if (reach === 0) {
        report('— · 도달이 없어 비율을 계산할 수 없으니 측정 상태를 확인하세요.');
        return;
      }
      const ratio = (saved + shares) / reach * 100;
      report(`${Number(ratio.toFixed(2))}% · 같은 조건의 다른 게시물과 이 비율을 비교하세요.`);
    };
    element.addEventListener('input', update);
    element.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const values = button.dataset.preset === 'break' ? [0, 0, 0] : [400, 16, 4];
      inputs.forEach((input, index) => { input.value = values[index]; });
      update();
    }));
    update();
  });
})();
