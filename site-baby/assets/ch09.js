/* 9장 전용 참고 날짜 계산. 저장·외부 전송 없음. */
(function () {
  'use strict';
  const routes = ['unknown', 'single', 'six'];
  const pad = value => String(value).padStart(2, '0');
  const format = date => `${date.getUTCFullYear()}-${pad(date.getUTCMonth() + 1)}-${pad(date.getUTCDate())}`;
  function parse(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error('출생일을 확인하세요.');
    const date = new Date(`${value}T00:00:00Z`);
    if (!Number.isFinite(date.getTime()) || format(date) !== value) throw new Error('실제 달력에 있는 출생일을 입력하세요.');
    return date;
  }
  const days = (date, amount) => new Date(date.getTime() + amount * 86400000);
  function months(date, amount) {
    const target = new Date(date.getTime());
    target.setUTCDate(1);
    target.setUTCMonth(target.getUTCMonth() + amount);
    const last = new Date(target.getTime());
    last.setUTCMonth(last.getUTCMonth() + 1, 0);
    target.setUTCDate(Math.min(date.getUTCDate(), last.getUTCDate()));
    return target;
  }
  function calendar(value, route, today) {
    const birth = parse(value);
    if (!routes.includes(route)) throw new Error('B형간염 경로를 다시 선택하세요.');
    if (today && birth > parse(today)) throw new Error('예정일 대신 실제 출생일을 입력하세요.');
    const range = (start, end) => `${format(start)} ~ ${format(end)}`;
    const rows = [
      [format(birth), '출생 B형간염 기록·산모 검사 결과 확인'],
      [range(birth, days(birth, 28)), 'BCG 피내 · 출생 후 4주 이내 표준 시기'],
      [range(days(birth, 14), days(birth, 35)), '1차 영유아검진 · 공단의 대상 시작·종료일 우선'],
      [format(months(birth, 1)), route === 'single' ? '단독 경로: 1개월 B형간염 접종 확인' : route === 'six' ? '6가 경로: 1개월 B형간염 생략 · 2개월 예약 확인' : '경로 모름: 기관에 단독·6가 여부 확인 · 1개월 접종을 임의로 정하지 않기'],
      [format(months(birth, 2)), route === 'six' ? '2개월: 6가(DTaP·IPV·Hib·B형간염) + 폐렴구균 + 로타 확인' : '2개월: DTaP·IPV·Hib·폐렴구균·로타 · 경로·포함 성분 확인'],
      [format(days(birth, 104)), '로타 첫 접종 마지막 가능 일령: 14주 6일 · 이 날까지 기다리지 않기'],
      [format(months(birth, 4)), route === 'six' ? '4개월: 6가 + 폐렴구균 + 로타 다음 회차 확인' : '4개월: DTaP·IPV·Hib·폐렴구균·로타 다음 회차 확인'],
      [range(months(birth, 4), days(months(birth, 7), -1)), '2차 영유아검진 · 4~6개월 참고 기간 · 공단 대상조회 우선'],
      [format(months(birth, 8)), '로타 전 과정: 8개월 0일 이내 · 종류별 회차와 간격은 기관 확인']
    ];
    return rows;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { calendar, months, days, parse, format };
    return;
  }
  const form = document.querySelector('[data-calendar-form]');
  if (!form) return;
  const status = document.querySelector('[data-calendar-status]');
  const result = document.querySelector('[data-calendar-result]');
  const body = document.querySelector('[data-calendar-rows]');
  const localToday = () => {
    const now = new Date();
    return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  };
  form.elements.birth.max = localToday();
  const clear = () => { body.replaceChildren(); result.hidden = true; };
  form.addEventListener('input', () => {
    clear();
    status.textContent = '조건이 바뀌었습니다. 참고 달력을 다시 만드세요.';
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    clear();
    try {
      const rows = calendar(form.elements.birth.value, form.elements.route.value, localToday());
      for (const [date, action] of rows) {
        const tr = document.createElement('tr');
        const th = document.createElement('th');
        const td = document.createElement('td');
        th.scope = 'row'; th.textContent = date; td.textContent = action;
        tr.append(th, td); body.append(tr);
      }
      result.hidden = false;
      status.textContent = `${rows.length}개 · 참고 날짜이며 실제 일정은 접종기관 확인이 필요합니다.`;
    } catch (error) { status.textContent = error.message; }
  });
  form.addEventListener('reset', () => {
    clear();
    status.textContent = '출생일과 경로를 선택하세요.';
  });
})();
