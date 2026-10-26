(() => {
  'use strict';
  const root = document.querySelector('#ledger-sim');
  if (!root) return;
  const sales = root.querySelector('#sales');
  const result = root.querySelector('[data-sim-result]');
  const update = () => {
    if (sales.value.trim() === '' || !sales.validity.valid) {
      result.textContent = '인정 구매 건수를 올바른 정수로 입력하세요.';
      return;
    }
    const amount = 50000 * Number(sales.value) * 0.03;
    result.textContent = `${amount.toLocaleString('ko-KR')}원 · ${amount ? '취소 없는 인정 구매의 수수료이며 세금 등을 빼기 전입니다.' : '인정 구매가 없으면 판매 수수료도 생기지 않습니다.'}`;
  };
  sales.addEventListener('input', update);
  root.querySelector('[data-zero]').addEventListener('click', () => {
    sales.value = '0';
    update();
  });
  update();
})();
