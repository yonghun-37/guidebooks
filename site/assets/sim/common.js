/* 공통 외곽: 네이티브 입력을 쓰고, 결과를 항상 텍스트로 출력한다. */
(() => {
  'use strict';
  window.ReelsSim = Object.freeze({
    mount(selector, render) {
      const element = document.querySelector(selector);
      if (!element) return;
      element.setAttribute('role', 'region');
      const result = element.querySelector('[data-sim-result]');
      if (result) { result.setAttribute('role', 'status'); result.setAttribute('aria-live', 'polite'); result.setAttribute('aria-atomic', 'true'); }
      render(element, text => { if (result) result.textContent = text; });
    },
    buttonGroup(group, select) {
      const buttons = [...group.querySelectorAll('button')];
      const activate = button => {
        buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        select(button.dataset.step, button);
      };
      buttons.forEach((button, index) => {
        button.addEventListener('click', () => activate(button));
        button.addEventListener('keydown', event => {
          let next;
          if (['ArrowRight', 'ArrowDown'].includes(event.key)) next = (index + 1) % buttons.length;
          if (['ArrowLeft', 'ArrowUp'].includes(event.key)) next = (index + buttons.length - 1) % buttons.length;
          if (event.key === 'Home') next = 0;
          if (event.key === 'End') next = buttons.length - 1;
          if (next !== undefined) { event.preventDefault(); buttons[next].focus(); activate(buttons[next]); }
        });
      });
      if (buttons[0]) activate(buttons[0]);
    }
  });
})();
