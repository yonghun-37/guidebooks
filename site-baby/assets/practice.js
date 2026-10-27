/* 실습의 OS 탭과 모든 페이지가 공유하는 진행 기록. 비밀 값·네트워크 없음. */
(() => {
  'use strict';
  document.querySelectorAll('[data-os-tabs]').forEach(group => {
    const list = group.querySelector('[data-tab-list]');
    const tabs = [...group.querySelectorAll('[data-os-tab]')].filter(node => node.closest('[data-os-tabs]') === group);
    const panels = [...group.querySelectorAll('[data-os-panel]')].filter(node => node.closest('[data-os-tabs]') === group);
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

})();
