/* 공통 외곽: 네이티브 입력을 쓰고, 결과를 항상 텍스트로 출력한다. */
(() => {
  'use strict';
  const savedIds = new Set(['ledger-sim', 'niche-sim', 'planner-sim']);
  const memory = new Map();
  const key = id => `reelsbook:sim:${id}`;
  const readState = id => {
    try {
      const value = JSON.parse(localStorage.getItem(key(id)) || 'null');
      return value?.version === 1 && value.values && typeof value.values === 'object' && !Array.isArray(value.values) && Object.values(value.values).every(item => typeof item === 'string') && typeof value.result === 'string' && typeof value.valid === 'boolean' ? value : null;
    } catch { return memory.get(id) || null; }
  };
  const clearState = () => {
    let stored = true;
    savedIds.forEach(id => { memory.delete(id); try { localStorage.removeItem(key(id)); } catch { stored = false; } });
    return stored;
  };
  window.ReelsSim = Object.freeze({
    readState, clearState,
    mount(selector, render) {
      const element = document.querySelector(selector);
      if (!element) return;
      element.setAttribute('role', 'region');
      const result = element.querySelector('[data-sim-result]');
      if (result) { result.setAttribute('role', 'status'); result.setAttribute('aria-live', 'polite'); result.setAttribute('aria-atomic', 'true'); }
      const id = element.id;
      const inputs = [...element.querySelectorAll('input[id], select[id], textarea[id]')];
      const saved = savedIds.has(id) ? readState(id) : null;
      if (saved) inputs.forEach(input => {
        const value = saved.values[input.id];
        if (typeof value === 'string') input.value = value;
      });
      render(element, text => { if (result) result.textContent = text; });
      if (savedIds.has(id)) {
        const notice = document.createElement('p'); notice.className = 'sim-assumptions'; notice.dataset.inputSaveStatus = ''; notice.setAttribute('role', 'status');
        notice.textContent = saved ? '저장한 입력을 복원했습니다. 이 브라우저에서만 이어 씁니다.' : '초기 예시값입니다. 입력을 바꾸면 이 브라우저에 저장해 15장 한 달 시나리오에서 이어 씁니다.';
        element.append(notice);
        const save = () => {
          const values = Object.fromEntries(inputs.map(input => [input.id, input.value]));
          const state = {version:1, values, result:result?.textContent || '', valid:inputs.every(input => input.value.trim() !== '' && input.validity.valid), updatedAt:new Date().toISOString()};
          memory.set(id, state);
          let stored = true;
          try { localStorage.setItem(key(id), JSON.stringify(state)); } catch { stored = false; }
          notice.textContent = stored ? '입력을 이 브라우저에 저장했습니다. 15장 한 달 시나리오에서 확인·삭제할 수 있습니다.' : '저장할 수 없는 환경입니다. 현재 화면의 계산은 계속 동작하며 페이지를 떠나면 입력이 이어지지 않습니다.';
          // 같은 출처의 실험실 프레임에 변경을 알린다. 파일 열기 제한은 직접 장 링크로 안내한다.
          try { if (window.parent !== window) window.parent.dispatchEvent(new Event('reelsbook:inputs')); } catch { /* 출처가 다르면 알림 생략 */ }
        };
        element.addEventListener('input', save);
        element.addEventListener('change', save);
        element.addEventListener('click', event => { if (event.target.closest('[data-preset]')) save(); });
      }
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
