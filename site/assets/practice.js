/* 실습의 OS 탭과 모든 페이지가 공유하는 진행 기록. 비밀 값·네트워크 없음. */
(() => {
  'use strict';
  document.querySelectorAll('[data-os-tabs]').forEach(group => {
    const list = group.querySelector('[data-tab-list]');
    const tabs = [...group.querySelectorAll('[data-os-tab]')];
    const panels = [...group.querySelectorAll('[data-os-panel]')];
    list.setAttribute('role', 'tablist');
    const activate = (tab, focus = false) => {
      tabs.forEach(item => {
        item.setAttribute('aria-selected', String(item === tab));
        item.tabIndex = item === tab ? 0 : -1;
      });
      panels.forEach(panel => { panel.hidden = panel.dataset.osPanel !== tab.dataset.osTab; });
      if (focus) tab.focus();
    };
    panels.forEach(panel => { panel.setAttribute('role', 'tabpanel'); panel.tabIndex = 0; });
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); activate(tabs[next], true); }
      });
    });
    activate(tabs[0]);
  });

  const checks = [...document.querySelectorAll('[data-practice-check]')];
  const fields = [...document.querySelectorAll('[data-practice-field]')];
  const key = 'reelsbook:practice:v1';
  let state = { checks: {}, fields: {} }, available = true;
  const read = () => {
    try {
      const parsed = JSON.parse(localStorage.getItem(key) || '{}');
      if (parsed && parsed.version === 1 && parsed.checks && typeof parsed.checks === 'object' && !Array.isArray(parsed.checks)) {
        state.checks = Object.fromEntries(Object.entries(parsed.checks).filter(([name, value]) => /^\d+:\w[\w-]*$/.test(name) && value === true));
        state.fields = parsed.fields && typeof parsed.fields['posted-url'] === 'string' ? { 'posted-url': parsed.fields['posted-url'].slice(0, 500) } : {};
      }
    } catch { /* 손상된 기록은 비워서 읽고 현재 페이지 조작을 유지한다. */ }
  };
  read();
  const announce = () => {
    const completed = checks.filter(input => input.checked).length;
    document.querySelectorAll('[data-practice-status]').forEach(node => {
      node.textContent = available ? `${completed}/${checks.length} 단계 확인 · 이 브라우저에만 저장됨` : `${completed}/${checks.length} 단계 확인 · 저장할 수 없습니다. 현재 페이지에서는 계속 사용하고, 이동 전 개인 메모로 남기세요.`;
    });
    document.querySelectorAll('[data-practice-progress]').forEach(node => { node.max = checks.length; node.value = completed; });
  };
  const save = () => {
    try { localStorage.setItem(key, JSON.stringify({ version: 1, ...state })); available = true; }
    catch { available = false; }
    announce();
  };
  const restore = () => {
    checks.forEach(input => { input.checked = state.checks[input.dataset.practiceCheck] === true; });
    fields.forEach(input => { input.value = state.fields[input.dataset.practiceField] || ''; });
    announce();
  };
  restore();
  // 처음부터 저장이 차단되면 조작 전에 알린다.
  save();
  checks.forEach(input => input.addEventListener('change', () => {
    if (input.checked) state.checks[input.dataset.practiceCheck] = true;
    else delete state.checks[input.dataset.practiceCheck];
    checks.filter(other => other.dataset.practiceCheck === input.dataset.practiceCheck).forEach(other => { other.checked = input.checked; });
    save();
  }));
  fields.forEach(input => input.addEventListener('input', () => {
    state.fields[input.dataset.practiceField] = input.value.slice(0, 500);
    save();
    document.querySelectorAll('[data-practice-field-status]').forEach(node => {
      node.textContent = available ? '주소를 기록했습니다. 실제 게시 확인은 본인이 해 주세요.' : '저장할 수 없습니다. 개인 메모에 주소를 복사해 주세요.';
    });
  }));
  document.querySelectorAll('[data-practice-reset]').forEach(button => button.addEventListener('click', () => {
    state = { checks: {}, fields: {} };
    save(); restore();
  }));
  window.addEventListener('storage', event => { if (event.key === key) { state = { checks: {}, fields: {} }; read(); restore(); } });
})();
