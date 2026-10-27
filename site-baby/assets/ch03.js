/* 3장 잠자리 점검. 미선택 항목의 개선 목록만 보여 준다. */
(() => {
  'use strict';
  const host = document.querySelector('#sleep-check'), result = document.querySelector('#sleep-result');
  if (!host || !result) return;
  const render = () => {
    const missing = [...host.querySelectorAll('input[type=checkbox]')].filter(input => !input.checked);
    result.replaceChildren();
    const title = document.createElement('p');
    title.textContent = `지금 고칠 것 ${missing.length}개 · 다음 잠 전에 아래 목록부터 고칩니다.`;
    result.append(title);
    if (missing.length) {
      const list = document.createElement('ul');
      missing.forEach(input => { const li = document.createElement('li'); li.textContent = input.value; list.append(li); });
      result.append(list);
    }
    const note = document.createElement('p');
    note.textContent = '모두 체크해도 안전을 보장하지 않습니다. 매 잠마다 등을 대고, 잠자리를 비우고, 뒤집으려는 움직임을 확인하세요.';
    result.append(note);
  };
  host.addEventListener('change', render); render();
})();
