/* 장 전용 도구. 입력은 브라우저 안에서만 계산하며 저장·외부 호출하지 않는다. */
(() => {
  'use strict';
  ReelsSim.mount('#chapter-figure', (element, report) => {
    ReelsSim.buttonGroup(element.querySelector('[data-figure-buttons]'), key => {
      report(element.querySelector(`[data-figure-note="${key}"]`).textContent);
    });
  });

  ReelsSim.mount('#publishing-sim', (element, report) => {
    const bundles = element.querySelector('#publish-bundles');
    const recent = element.querySelector('#publish-recent');
    const limit = element.querySelector('#publish-limit');
    const time = element.querySelector('#publish-time');
    const calendar = element.querySelector('[data-calendar]');
    const update = () => {
      if ([bundles, recent, time].some(input => !input.value || !input.checkValidity())) {
        calendar.textContent = '예약 후보를 확인할 수 없습니다.';
        report('묶음 수·직전 발행 건수·시각을 유효한 값으로 입력하세요.'); return;
      }
      const date = new Date(time.value + '+09:00');
      if (!Number.isFinite(date.getTime())) { calendar.textContent = ''; report('예약 시각을 다시 입력하세요.'); return; }
      const count = Number(bundles.value), issued = Number(recent.value), planned = count * 2;
      calendar.textContent = `예약 후보: ${time.value.replace('T', ' ')} KST (UTC+09:00) / ${date.toISOString().replace('T', ' ').replace('.000Z', ' UTC')}\n캐러셀 ${count}건 + 릴스 ${count}건 = 발행 ${planned}건. 시스템에는 등록하지 않았습니다.`;
      const limits = limit.value === 'unknown' ? [50, 100] : [Number(limit.value)];
      const rows = limits.map(value => {
        const total = issued + planned, remaining = value - total;
        return `${value}건 가정: 합계 ${total}건, ${remaining < 0 ? `가정 한도 ${-remaining}건 초과 → 예약안 보류` : `가정 잔여 ${remaining}건 → 다른 요건도 별도 확인`}.`;
      });
      report((planned === 0 ? '새 발행 계획은 0건입니다.\n' : '') + rows.join('\n') + '\n실효 한도 미확인. 이 계산은 게시 허가나 계정 안전 판정이 아닙니다.');
    };
    element.querySelectorAll('input, select').forEach(input => input.addEventListener('input', update));
    element.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      bundles.value = button.dataset.preset === 'break' ? 80 : 2;
      recent.value = button.dataset.preset === 'break' ? 40 : 0;
      limit.value = 'unknown'; time.value = '2026-10-27T21:00'; update();
    }));
    update();
  });

})();
