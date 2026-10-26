/* 14장 전용: 검수 시간을 남긴 30일 제작 시간 예산을 계산한다. */
(() => {
  'use strict';
  ReelsSim.mount('#planner-sim', (element, report) => {
    const start = element.querySelector('#plan-start');
    const minutes = element.querySelector('#plan-minutes');
    const days = element.querySelector('#plan-days');
    const calendar = element.querySelector('[data-plan-calendar]');
    const copy = element.querySelector('[data-plan-text]');
    const weeks = element.querySelector('[data-plan-weeks]');
    const phases = ['생활 뉴스 독자·권리 메모 → 신청 체크 문안', '신청 체크 카드·영상 제작 → 사람 검수', '앱 첫 게시 → 게시 기록 확인', '반응·수입·비용 기록 → 다음 계획'];
    const update = () => {
      if ([start, minutes, days].some(input => input.value.trim() === '' || !input.checkValidity())) {
        calendar.hidden = true; weeks.replaceChildren(); copy.value = '';
        report('— · 첫날 날짜와 확보 시간·활동일을 확인하세요.');
        return;
      }
      const active = Number(days.value);
      let activeDays = 0;
      for (let day = 0; day < 30; day++) if (day % 7 < active) activeDays++;
      calendar.hidden = false;
      const first = new Date(start.value + 'T12:00:00');
      const dateAt = day => {
        const date = new Date(first);
        date.setDate(date.getDate() + day);
        return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
      };
      const lines = ['날짜 | 할 일 | 완료·보류 | 실제 시간'];
      const rows = Array.from({length:30}, (_,day) => {
        const date = dateAt(day);
        const task = day % 7 < active ? phases[Math.min(3, Math.floor(day/7))] : '쉬는 날 · 밀린 일은 다음 활동일로';
        lines.push(`${date} | ${task} | □ |     분`);
        return `<tr><th scope="row">${date}</th><td>${task}</td><td><input type="checkbox" aria-label="${date} 완료"></td></tr>`;
      });
      calendar.innerHTML = `<table><caption>가상 30일 초안 · 첫날 기준 7일 중 앞 ${active}일 활동</caption><thead><tr><th scope="col">날짜</th><th scope="col">할 일</th><th scope="col">완료</th></tr></thead><tbody>${rows.join('')}</tbody></table>`;
      weeks.innerHTML = [6,13,20,27,29].map(day => `<li data-weekly-check>${dateAt(day)} 점검: 완료 __ / 보류 이유 __ / 실제 시간·비용 __ / 다음 활동일 __ / 계속·축소·중단 __</li>`).join('');
      lines.push('', ...[6,13,20,27,29].map(day => `${dateAt(day)} 점검 | 완료·보류 이유 __ | 실제 시간·비용 __ | 다음 활동일 __ | 계속·축소·중단 __`));
      copy.value = lines.join('\n');
      const budget = activeDays * Math.max(Number(minutes.value) - 10, 0);
      report(`${budget.toLocaleString('ko-KR')}분 · ${budget === 0 ? '제작 시간이 없으니 활동일·기간·작업 범위를 조정하세요.' : '이 시간 안에 미완료 작업을 나누고 모자란 일은 다음 기간으로 옮기세요.'}`);
    };
    const change = event => { if ([start, minutes, days].includes(event.target)) update(); };
    element.addEventListener('input', change);
    element.addEventListener('change', change);
    element.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      start.value = '2026-10-27';
      minutes.value = button.dataset.preset === 'break' ? 0 : 30;
      days.value = '5';
      update();
    }));
    update();
  });
})();
