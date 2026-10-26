/* 공통 외곽: 네이티브 입력을 쓰고, 결과를 항상 텍스트로 출력한다. */
(() => {
  'use strict';
  // 카드는 네이티브 앵커, FAQ는 details/summary라 JS 없이도 쓸 수 있다.
  // 절 이동 뒤 키보드 초점도 옮기고, FAQ 내부로 직접 온 링크는 펼친다.
  const fragmentTarget = hash => {
    try { return document.getElementById(decodeURIComponent(hash.slice(1))); }
    catch { return null; }
  };
  const openFaq = target => {
    for (let node = target; node; node = node.parentElement) {
      if (node.matches('.chapter-faq details')) node.open = true;
    }
  };
  const revealFragment = () => {
    const target = fragmentTarget(location.hash);
    if (target) openFaq(target);
  };
  document.querySelectorAll('[data-axis-nav] a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', event => {
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const target = fragmentTarget(anchor.hash);
      if (!target) return;
      openFaq(target);
      if (!target.hasAttribute('tabindex')) {
        target.tabIndex = -1;
        target.addEventListener('blur', () => target.removeAttribute('tabindex'), { once: true });
      }
      target.focus({ preventScroll: true });
      // URL·뒤로 가기·스크롤은 앵커의 기본 동작에 맡긴다.
    });
  });
  window.addEventListener('hashchange', revealFragment);
  revealFragment();
  let printClosedFaqs = [];
  window.addEventListener('beforeprint', () => {
    printClosedFaqs = [...document.querySelectorAll('.chapter-faq details:not([open])')];
    printClosedFaqs.forEach(details => { details.open = true; });
  });
  window.addEventListener('afterprint', () => {
    printClosedFaqs.forEach(details => { details.open = false; });
    printClosedFaqs = [];
  });
  const savedIds = new Set();
  const memory = new Map();
  const key = id => `shortsbook:sim:${id}`;
  const readState = id => {
    try {
      const value = JSON.parse(localStorage.getItem(key(id)) || 'null');
      return [1, 2].includes(value?.version) && value.values && typeof value.values === 'object' && !Array.isArray(value.values) && Object.values(value.values).every(item => typeof item === 'string') && typeof value.result === 'string' && typeof value.valid === 'boolean' ? value : null;
    } catch { return memory.get(id) || null; }
  };
  const clearState = () => {
    let stored = true;
    savedIds.forEach(id => { memory.delete(id); try { localStorage.removeItem(key(id)); } catch { stored = false; } });
    return stored;
  };
  window.ShortsSim = Object.freeze({
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
          const state = {version:2, values, result:result?.textContent || '', valid:inputs.every(input => input.value.trim() !== '' && input.validity.valid), updatedAt:new Date().toISOString()};
          memory.set(id, state);
          let stored = true;
          try { localStorage.setItem(key(id), JSON.stringify(state)); } catch { stored = false; }
          notice.textContent = stored ? '입력을 이 브라우저에 저장했습니다. 15장 한 달 시나리오에서 확인·삭제할 수 있습니다.' : '저장할 수 없는 환경입니다. 현재 화면의 계산은 계속 동작하며 페이지를 떠나면 입력이 이어지지 않습니다.';
          // 같은 출처의 실험실 프레임에 변경을 알린다. 파일 열기 제한은 직접 장 링크로 안내한다.
          try { if (window.parent !== window) window.parent.dispatchEvent(new Event('shortsbook:inputs')); } catch { /* 출처가 다르면 알림 생략 */ }
        };
        element.addEventListener('input', save);
        element.addEventListener('change', save);
        element.addEventListener('click', event => { if (event.target.closest('[data-preset]')) save(); });
        // 입력을 이어 쓰되 저장된 결과는 현재 계산으로 갱신한다.
        if (saved) save();
      }
    },
    moneyBars(element, values) {
      let svg = element.querySelector('[data-money-bars]');
      if (!svg) {
        svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('data-money-bars', '');
        svg.setAttribute('viewBox', '0 0 360 180');
        svg.setAttribute('role', 'img');
        svg.classList.add('money-bars');
        element.querySelector('[data-sim-result]').before(svg);
      }
      svg.hidden = !values;
      svg.style.display = values ? '' : 'none';
      if (!values) return;
      const rows = [['income', '수입'], ['cost', '비용'], ['balance', '잔액']];
      const won = value => `${Math.round(value).toLocaleString('ko-KR')}원`;
      svg.setAttribute('aria-label', rows.map(([key, name]) => `${name} ${won(values[key])}`).join(', '));
      svg.replaceChildren();
      const node = (tag, attrs, text) => {
        const child = document.createElementNS(svg.namespaceURI, tag);
        Object.entries(attrs).forEach(([key, value]) => child.setAttribute(key, value));
        if (text) child.textContent = text;
        svg.append(child);
      };
      const max = Math.max(1, ...Object.values(values).map(Math.abs));
      node('line', {x1: 180, x2: 180, y1: 24, y2: 168, class: 'money-zero'});
      rows.forEach(([key, name], index) => {
        const y = 18 + index * 54, value = values[key], width = Math.abs(value) / max * 170;
        node('text', {x: 8, y}, `${name} ${won(value)}`);
        node('rect', {x: value < 0 ? 180 - width : 180, y: y + 8, width, height: 16,
          class: `money-${key}${value < 0 ? ' money-negative' : ''}`, 'data-bar': key});
      });
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
