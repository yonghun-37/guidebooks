/* 13장 전용: 사용자가 정한 목표·비용·가격으로 거래 수를 역산한다. */
(() => {
  'use strict';
  ReelsSim.mount('#roadmap-sim', (element, report) => {
    const inputs = [...element.querySelectorAll('input')];
    const update = () => {
      if (inputs.some(input => input.value.trim() === '' || !input.checkValidity())) {
        ReelsSim.moneyBars(element, null);
        report('— · 목표·비용·제안 가격을 유효하게 입력하세요.');
        return;
      }
      const [goal, cost, price] = inputs.map(input => Number(input.value));
      if (price === 0) {
        ReelsSim.moneyBars(element, null);
        report('— · 제안 가격을 정한 뒤 필요한 거래 수를 계산하세요.');
        return;
      }
      const count = Math.ceil((goal + cost) / price);
      ReelsSim.moneyBars(element, {income: count * price, cost, balance: count * price - cost});
      report(`${count.toLocaleString('ko-KR')}건 · 그만큼 제작·수정할 시간이 있는지 먼저 확인하세요.`);
    };
    element.addEventListener('input', update);
    element.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const values = button.dataset.preset === 'break' ? [0, 0, 0] : [300000, 100000, 100000];
      inputs.forEach((input, index) => { input.value = values[index]; });
      update();
    }));
    update();
  });
})();
