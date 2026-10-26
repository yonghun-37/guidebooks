/* 14장 전용: 검수 시간을 남긴 30일 제작 시간 예산을 계산한다. */
(() => {
  'use strict';
  ReelsSim.mount('#planner-sim', (element, report) => {
    const start = element.querySelector('#plan-start');
    const minutes = element.querySelector('#plan-minutes');
    const days = element.querySelector('#plan-days');
    const update = () => {
      if ([start, minutes, days].some(input => input.value.trim() === '' || !input.checkValidity())) {
        report('— · 첫날 날짜와 확보 시간·활동일을 확인하세요.');
        return;
      }
      const active = Number(days.value);
      let activeDays = 0;
      for (let day = 0; day < 30; day++) if (day % 7 < active) activeDays++;
      const budget = activeDays * Math.max(Number(minutes.value) - 10, 0);
      report(`${budget.toLocaleString('ko-KR')}분 · ${budget === 0 ? '제작 시간이 없으니 활동일·기간·작업 범위를 조정하세요.' : '이 시간 안에 미완료 작업을 나누고 모자란 일은 다음 기간으로 옮기세요.'}`);
    };
    element.addEventListener('input', update);
    element.addEventListener('change', update);
    element.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      start.value = '2026-10-27';
      minutes.value = button.dataset.preset === 'break' ? 0 : 30;
      days.value = '5';
      update();
    }));
    update();
  });
})();
