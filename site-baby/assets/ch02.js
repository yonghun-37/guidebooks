/* 2장 관찰 목록. 섭취량·건강 상태를 계산하지 않으며 저장하지 않는다. */
(() => {
  'use strict';
  const host = document.querySelector('#feeding-check'), result = document.querySelector('#feeding-result');
  if (!host || !result) return;
  const render = () => {
    const checks = [...host.querySelectorAll('input[type=checkbox]')], missing = checks.filter(input => !input.checked);
    result.replaceChildren();
    const title = document.createElement('p');
    title.textContent = `확인한 항목 ${checks.length - missing.length}개 · 관찰을 모아 상담할 질문을 정리합니다.`;
    result.append(title);
    if (missing.length) {
      const list = document.createElement('ul');
      missing.forEach(input => { const li = document.createElement('li'); li.textContent = input.value + ' 확인 방법을 소아과·수유 상담에 묻기'; list.append(li); });
      result.append(list);
    }
    const note = document.createElement('p');
    note.textContent = '모두 확인해도 충분히 먹었다는 판정은 아닙니다. 먹기·소변·활력이 달라지면 아래 공통 안내를 따릅니다.';
    result.append(note);
  };
  host.addEventListener('change', render); render();
})();
