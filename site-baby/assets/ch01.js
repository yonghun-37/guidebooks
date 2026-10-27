/* 1장 전용. 날짜는 UTC 달력으로 계산하고 법정/기관 경계를 확정하지 않는다. */
(function () {
  'use strict';
  const iso = date => date.toISOString().slice(0, 10);
  function calendar(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value) || Number(value.slice(0, 4)) < 1900 || Number(value.slice(0, 4)) > 2100) throw new Error('실제 출생일을 올바르게 입력하세요.');
    const birth = new Date(value + 'T00:00:00Z');
    if (Number.isNaN(birth.getTime()) || iso(birth) !== value) throw new Error('달력에 있는 실제 출생일을 입력하세요.');
    const days = count => { const d = new Date(birth); d.setUTCDate(d.getUTCDate() + count); return iso(d); };
    const month = new Date(Date.UTC(birth.getUTCFullYear(), birth.getUTCMonth() + 1, 1));
    const last = new Date(Date.UTC(month.getUTCFullYear(), month.getUTCMonth() + 1, 0)).getUTCDate();
    month.setUTCDate(Math.min(last, birth.getUTCDate()));
    return { month: iso(month), clamped: birth.getUTCDate() > last, benefit: days(59), screenStart: days(14), screenEnd: days(35), rota: days(14 * 7 + 6) };
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { calendar };
  if (typeof document === 'undefined') return;
  const form = document.querySelector('#deadline-form'), result = document.querySelector('#deadline-result');
  if (!form || !result) return;
  const ref = n => `<sup class="footnote-ref"><a href="${['N037', 'N044'].includes(n) ? '../credits.html#' : '#'}${n.toLowerCase()}">[${n}]</a></sup>`;
  const date = value => `<time datetime="${value}">${value.replaceAll('-', '.')}</time>`;
  form.addEventListener('input', () => { result.textContent = '출생일을 바꿨습니다. 기한 달력 보기를 다시 누르세요.'; });
  form.addEventListener('submit', event => {
    event.preventDefault();
    try {
      const value = form.elements.birth.value;
      const today = new Date(), localToday = [today.getFullYear(), String(today.getMonth() + 1).padStart(2, '0'), String(today.getDate()).padStart(2, '0')].join('-');
      if (value > localToday) throw new Error('예정일 대신 이미 태어난 아기의 실제 출생일을 입력하세요.');
      const r = calendar(value);
      result.innerHTML = `<p><strong>챙길 기한 4개</strong> · 참고 날짜를 기관 조회와 대조하세요.</p><ul><li>출생신고: 출생 후 1개월 이내. 달력상 한 달 무렵 ${date(r.month)}${r.clamped ? ' · 다음 달에 같은 날짜가 없어 말일을 참고 표시했습니다.' : ''} <strong>법정기한·휴일 처리는 기관 조회로 확인</strong>.${ref('N044')}</li><li>부모급여: 출생일 포함 60일째 ${date(r.benefit)}. 출생월 소급 신청의 참고 끝날짜입니다. <strong>접수일·예외는 기관 조회로 확인</strong>.${ref('N037')}</li><li>첫 검진: 출생일에서 14~35일 뒤 ${date(r.screenStart)}~${date(r.screenEnd)}. <strong>실제 시작·종료일은 건강보험공단 대상조회로 확인</strong>.${ref('N031')}</li><li>로타 첫 접종: 14주 6일에 해당하는 ${date(r.rota)}까지가 상한입니다. 표준 시작인 2개월에 미리 상담하세요. <strong>접종 가능일은 기관 조회로 확인</strong>.${ref('N027')}</li></ul><p>생후 일수는 출생일에 일수를 더하고, 부모급여 60일은 출생일을 포함해 계산했습니다. 1개월을 30일로 바꾸지 않았습니다. 미래 일정은 예약 전 해당 연도 안내도 확인하세요.</p>`;
    } catch (error) { result.textContent = error.message; }
  });
})();
