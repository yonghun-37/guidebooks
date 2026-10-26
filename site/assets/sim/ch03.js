(() => {
  'use strict';
  ReelsSim.mount('#concept-figure', (el, report) => {
    const details = ["지급자: 브랜드·판매자·구매자·의뢰인·독자·플랫폼 중 누가 돈을 내는지 적습니다.", "대가: 게시·인정 구매·상품·납품·구독·기능별 보상 중 계약이 정한 것을 적습니다.", "장부: 같은 기간의 실제 현금 수입·환불·비용·운영 시간을 기록합니다. 예상 화면 금액과 중복 합산하지 않습니다."];
    ReelsSim.buttonGroup(el.querySelector('[data-concept-buttons]'), step => {
      el.querySelectorAll('[data-node]').forEach(node => { node.dataset.active = String(node.dataset.node === step); });
      report(details[Number(step)]);
    });
  });
  ReelsSim.mount('#ledger-sim', (el, report) => {
    const keys = ['brand', 'affiliate', 'product', 'service', 'reader', 'platform', 'cost', 'refund', 'hours'];
    const inputs = keys.map(key => el.querySelector('#' + key));
    const won = value => new Intl.NumberFormat('ko-KR', { maximumFractionDigits: 0 }).format(value) + '원';
    const update = () => {
      if (inputs.some(input => input.value.trim() === '' || !input.validity.valid)) {
        report('계산을 멈췄습니다. 빈칸은 미확인 값입니다. 금액은 0~10억 원의 정수, 시간은 0~744시간의 0.5시간 단위로 입력하세요. 빈칸을 자동으로 0으로 바꾸지 않습니다.'); return;
      }
      const values = inputs.map(input => Number(input.value));
      const income = values.slice(0, 6).reduce((a, b) => a + b, 0);
      const balance = income - values[6] - values[7];
      const hours = values[8];
      const hourly = hours > 0 ? `시간당 현금 잔액 약 ${won(balance / hours)}.` : '시간이 0이라 시간당 값은 계산할 수 없습니다. 운영 시간 누락 여부를 확인하세요.';
      report(`현금 수입 ${won(income)} − 비용 ${won(values[6])} − 환불 ${won(values[7])} = 현금 잔액 ${won(balance)}. ${balance < 0 ? '현금이 부족한 상태입니다. ' : ''}운영 ${hours}시간. ${hourly} 세금 등은 제외한 연습 장부이며 수익 예측이 아닙니다.`);
    };
    inputs.forEach(input => input.addEventListener('input', update));
    el.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const values = {zero: [0,0,0,0,0,0,0,0,0], example: [120000,20000,0,0,0,0,40000,10000,10], break: [0,0,0,0,0,0,50000,0,0]}[button.dataset.preset];
      inputs.forEach((input, i) => { input.value = values[i]; }); update();
    }));
    update();
  });
})();
