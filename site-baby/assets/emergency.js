/* 장·실습·인쇄물의 동일한 데이터 렌더러. 응급 판정을 계산하지 않는다. */
(() => {
  'use strict';
  const rows = window.BabyEmergency;
  const source = id => `<sup class="footnote-ref"><a href="${window.BabyBook.url('credits.html')}#${id.toLowerCase()}">[${id}]</a></sup>`;
  const item = row => `<p class="emergency-message" data-emergency-id="${row.id}">${row.text}${row.sources.map(source).join('')}</p>`;
  document.querySelectorAll('[data-emergency]').forEach(host => {
    if (host.hasAttribute('data-emergency-full')) {
      host.className = 'emergency-grid';
      host.innerHTML = `<section class="emergency-tier call"><h3><b>①</b> 119</h3>${rows.filter(row => row.tier === 'call').map(item).join('')}</section><section class="emergency-tier urgent"><h3><b>②</b> 즉시 진료</h3>${rows.filter(row => row.tier === 'urgent').map(item).join('')}</section><section class="emergency-tier ask"><h3><b>③</b> 오늘 소아과에 묻기</h3><p>목록에 없는 변화도 걱정되면 오늘 소아과에 연락하세요. 증상이 겹치면 위의 긴급한 행동부터 따르세요.${source('N001')}</p><p class="small">안전 여부를 판정하는 표가 아닙니다.</p></section>`;
    } else {
      const selected = host.dataset.emergency.split(',');
      host.className = 'emergency-inline';
      host.innerHTML = rows.filter(row => selected.includes(row.id)).map(row => `<p class="emergency-label">${row.tier === 'call' ? '119' : '즉시 진료'}</p>${item(row)}`).join('');
    }
  });
})();
