(() => {
  'use strict';
  const revenue = document.querySelector('#revenue-form');
  const cost = document.querySelector('#cost-form');
  if (!revenue || !cost) return;
  const revenueResult = document.querySelector('[data-revenue-result]');
  const costResult = document.querySelector('[data-cost-result]');
  const money = new Intl.NumberFormat('ko-KR', { maximumFractionDigits: 2 });
  document.querySelectorAll('[data-calc-action], [data-zero-revenue], [data-zero-cost], [data-save-plan]').forEach(el => { el.hidden = false; });
  revenue.elements.rate.max = '100';
  function values(form) {
    const data = {};
    for (const input of form.querySelectorAll('input')) {
      input.setCustomValidity('');
      if (input.value === '' || !Number.isFinite(input.valueAsNumber)) {
        input.setCustomValidity('모르는 값은 확인한 뒤 입력하세요. 수입·지출이 없으면 0을 넣으세요.');
      }
      data[input.name] = input.valueAsNumber;
    }
    return form.reportValidity() ? data : null;
  }
  revenue.addEventListener('submit', event => {
    event.preventDefault();
    const v = values(revenue);
    if (!v) return;
    const total = v.pv / 1000 * v.rpm + v.orders * v.basket * v.rate / 100 + v.sponsor;
    revenueResult.textContent = Number.isFinite(total)
      ? `${money.format(total)}원 · 입력한 월의 세 수입 합계예요. 비용·세금·지급 지연 전이며 실입금과 다를 수 있어요.`
      : '입력값이 너무 커 계산할 수 없어요. 단위와 자릿수를 확인하세요.';
  });
  cost.addEventListener('submit', event => {
    event.preventDefault();
    const v = values(cost);
    if (!v) return;
    const usd = (v.intokens * v.inprice + v.outtokens * v.outprice) / 1000000 * v.calls;
    const total = v.hosting + v.domain / 12 + usd * v.fx;
    costResult.textContent = Number.isFinite(total)
      ? `${money.format(total)}원/월 · 입력한 호스팅·도메인 갱신비·텍스트 토큰의 월환산이에요. 별도 지출은 따로 더하세요.`
      : '입력값이 너무 커 계산할 수 없어요. 단위와 자릿수를 확인하세요.';
  });
  for (const [form, result] of [[revenue, revenueResult], [cost, costResult]]) {
    form.addEventListener('input', event => {
      event.target.setCustomValidity?.('');
      result.textContent = '입력값이 바뀌었어요. 계산 버튼을 다시 누르세요.';
    });
  }
  function zero(form, result, text) {
    form.querySelectorAll('input').forEach(input => {
      input.value = input.name === 'fx' ? '1' : '0';
      input.setCustomValidity('');
    });
    form.requestSubmit();
    result.textContent += text;
  }
  document.querySelector('[data-zero-revenue]').addEventListener('click', () => zero(revenue, revenueResult, ' 수입 0의 가정이에요.'));
  document.querySelector('[data-zero-cost]').addEventListener('click', () => zero(cost, costResult, ' mock 비용 0의 가정이며, 달러 비용 0에 곱하는 환율은 1로 놓았어요.'));
  document.querySelector('[data-save-plan]').addEventListener('click', () => {
    const lines = ['운영계획', '글 유형과 사람 승인: ', '다음 검토 시간과 끝낼 단계: ', '', '내 숫자 · 가정과 실제 견적을 구별해 채우세요.'];
    for (const form of [revenue, cost]) {
      form.querySelectorAll('input').forEach(input => {
        lines.push(`${input.parentElement.firstChild.textContent.trim()}: ${input.value || '모름'}`);
      });
    }
    lines.push('', revenueResult.textContent, costResult.textContent, '별도 지출·견적 날짜: ', '입력값은 기대 수익을 보장하지 않아요.');
    const url = URL.createObjectURL(new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = '운영계획.txt';
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    document.querySelector('[data-plan-save]').textContent = '받은 운영계획.txt에서 승인·검토 시간과 별도 지출 칸을 채우세요.';
  });
})();
