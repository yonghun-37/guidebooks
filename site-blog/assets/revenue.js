/* 가상 입력으로만 계산한다. 외부 요청·환율 변환·실적 저장은 하지 않는다. */
(() => {
  'use strict';
  const tool = document.getElementById('revenue-tool');
  if (!tool) return;
  const field = name => document.getElementById(`calc-${name}`);
  const ads = document.getElementById('ads-fields');
  const affiliate = document.getElementById('affiliate-fields');
  const result = field('result'), interpretation = field('interpretation'), formula = field('formula');
  const fmt = value => new Intl.NumberFormat('ko-KR', {maximumFractionDigits: 6}).format(value);
  const money = value => field('currency').value === 'USD' ? `US$${value.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2})}` : `${Math.round(value).toLocaleString('ko-KR')}원`;
  const value = name => Number(field(name).value);
  function render() {
    const isAds = field('mode').value === 'ads';
    ads.hidden = ads.disabled = !isAds;
    affiliate.hidden = affiliate.disabled = isAds;
    field('pages-label').textContent = field('base').value === 'uv' ? '페이지/일별 UV · 가상' : '페이지/방문 · 가상';
    const names = ['visitors','days', ...(isAds ? ['pages','rpm'] : ['click','conversion','price','rate','cancel'])];
    const invalid = names.find(name => field(name).value.trim() === '' || !field(name).validity.valid || !Number.isFinite(value(name)));
    if (invalid) {
      result.textContent = '입력 확인';
      interpretation.textContent = `${field(invalid).closest('label').textContent.trim()} 칸의 범위와 값을 확인하세요.`;
      formula.textContent = '빈 값·음수·범위를 벗어난 비율은 계산하지 않습니다.';
      return;
    }
    let amount;
    if (isAds) {
      const pv = value('visitors') * value('days') * value('pages');
      amount = field('approved').value === 'no' ? 0 : pv / 1000 * value('rpm');
      formula.textContent = field('approved').value === 'no' ? '미승인·미게재 → 해당 광고 수입 0' : `${fmt(value('visitors'))} × ${fmt(value('days'))} × ${fmt(value('pages'))} = ${fmt(pv)} PV; ${fmt(pv)} ÷ 1,000 × ${money(value('rpm'))} = ${money(amount)}`;
      interpretation.textContent = '가상 조건의 기간 광고 예상 수입입니다. 입금액이 아닙니다.';
    } else {
      const orders = value('visitors') * value('days') * value('click') / 100 * value('conversion') / 100;
      const remaining = orders * (1 - value('cancel') / 100);
      amount = remaining * value('price') * value('rate') / 100;
      formula.textContent = `${fmt(value('visitors'))} × ${fmt(value('days'))} × ${fmt(value('click'))}% × ${fmt(value('conversion'))}% = ${fmt(orders)}건; 취소 반영 ${fmt(remaining)}건 × ${money(value('price'))} × ${fmt(value('rate'))}% = ${money(amount)}`;
      interpretation.textContent = '가상 구매·취소 조건의 제휴 수입입니다. 최종승인·입금은 따로 확인하세요.';
    }
    if (!Number.isFinite(amount)) {
      result.textContent = '입력 확인';
      interpretation.textContent = '계산 범위를 넘었습니다. 입력값을 줄여 주세요.';
      formula.textContent = '';
    } else result.textContent = money(amount);
  }
  const set = values => Object.entries(values).forEach(([name, value]) => { field(name).value = value; });
  const reference = () => set({mode:'ads',currency:'USD',base:'uv',visitors:1000,days:30,pages:1,rpm:0.99,approved:'yes'});
  const affiliateExample = () => set({mode:'affiliate',currency:'KRW',base:'visits',visitors:1000,days:30,click:2,conversion:1,price:50000,rate:3,cancel:0});
  field('mode').addEventListener('change', () => { if (field('mode').value === 'affiliate') affiliateExample(); else reference(); render(); });
  field('currency').addEventListener('change', () => { field(field('mode').value === 'ads' ? 'rpm' : 'price').value = ''; render(); });
  tool.addEventListener('input', render);
  tool.addEventListener('change', render);
  tool.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
    if (button.dataset.preset === 'affiliate') affiliateExample();
    else {
      reference();
      if (button.dataset.preset === 'zero') set({currency:'KRW',approved:'no',rpm:0});
    }
    render();
  }));
  render();
})();
