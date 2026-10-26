/* 장 전용 도구. 입력은 브라우저 안에서만 계산하며 저장·외부 호출하지 않는다. */
(() => {
  'use strict';
  ReelsSim.mount('#chapter-figure', (element, report) => {
    ReelsSim.buttonGroup(element.querySelector('[data-figure-buttons]'), key => {
      report(element.querySelector(`[data-figure-note="${key}"]`).textContent);
    });
  });

  ReelsSim.mount('#roadmap-sim', (element, report) => {
    const money = value => value.toLocaleString('ko-KR', {maximumFractionDigits: 0}) + '원';
    const update = () => {
      const rows = ['a', 'b'].map(side => {
        const inputs = ['income', 'cost', 'refund', 'hours'].map(key => element.querySelector(`#ledger-${side}-${key}`));
        if (inputs.some(input => input.value === '' || !input.checkValidity())) return `${side.toUpperCase()}: 미기록 또는 입력 범위 오류. 같은 기간의 모든 칸을 확인하세요.`;
        const [income, cost, refund, hours] = inputs.map(input => Number(input.value));
        const balance = income - cost - refund;
        return `${side.toUpperCase()}: 입금 ${money(income)} − 비용 ${money(cost)} − 환불 ${money(refund)} = 세전 현금 잔액 ${money(balance)}.\n운영 ${hours}시간. ${hours > 0 ? '시간당 잔액 약 ' + money(balance / hours) : '시간 0으로 시간당 계산 보류'}.`;
      });
      report(rows.join('\n\n') + '\n팔로워·미지급 계약액·세무상 순이익을 계산한 값이 아닙니다.');
    };
    element.querySelectorAll('input').forEach(input => input.addEventListener('input', update));
    element.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const mode = button.dataset.preset;
      const values = mode === 'normal' ? [[100000, 30000, 10000, 10], [160000, 80000, 20000, 20]] : mode === 'break' ? [[0, 50000, 0, 10], [0, 100000, 10000, 0]] : [[0,0,0,0],[0,0,0,0]];
      ['a','b'].forEach((side, index) => ['income','cost','refund','hours'].forEach((key, i) => { element.querySelector(`#ledger-${side}-${key}`).value = values[index][i]; })); update();
    }));
    update();
  });

})();
