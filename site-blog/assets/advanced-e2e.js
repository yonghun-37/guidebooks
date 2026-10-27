/* 이 진행표의 체크·메모만 브라우저에 저장한다. 서버 검사·전송은 없다. */
(() => {
  'use strict';
  const checks = [...document.querySelectorAll('[data-e2e-check]')];
  if (!checks.length) return;
  const notes = [...document.querySelectorAll('[data-e2e-note]')];
  const key = 'blogbook:advanced:e2e:v1';
  const status = document.querySelector('[data-e2e-save]');
  const count = document.querySelector('[data-e2e-count]');
  function render() {
    count.textContent = `체크한 항목: ${checks.filter(item => item.checked).length}개. 이 표는 서버 상태를 자동 확인하지 않아요.`;
  }
  try {
    const saved = JSON.parse(localStorage.getItem(key) || 'null');
    if (saved && typeof saved === 'object') {
      checks.forEach(item => { item.checked = saved.checks?.[item.dataset.e2eCheck] === true; });
      notes.forEach(item => {
        const value = saved.notes?.[item.dataset.e2eNote];
        if (typeof value === 'string') item.value = value.slice(0, 1200);
      });
    }
    status.textContent = '이 브라우저에서 기록을 이어 써요. 다른 기기에는 옮겨지지 않아요.';
  } catch {
    status.textContent = '저장 기록을 읽을 수 없어요. 현재 화면에서 작성하고 전체 내용을 개인 메모로 옮겨 보관하세요.';
  }
  function save() {
    render();
    try {
      localStorage.setItem(key, JSON.stringify({
        checks: Object.fromEntries(checks.map(item => [item.dataset.e2eCheck, item.checked])),
        notes: Object.fromEntries(notes.map(item => [item.dataset.e2eNote, item.value.slice(0, 1200)]))
      }));
      status.textContent = '이 브라우저에 저장했어요. 다른 기기에는 옮겨지지 않아요.';
    } catch {
      status.textContent = '저장할 수 없어요. 현재 화면에서 작성하고 전체 내용을 개인 메모로 옮겨 보관하세요.';
    }
  }
  checks.forEach(item => item.addEventListener('change', save));
  notes.forEach(item => item.addEventListener('input', save));
  document.querySelector('[data-e2e-reset]').addEventListener('click', () => {
    checks.forEach(item => { item.checked = false; });
    notes.forEach(item => { item.value = ''; });
    render();
    try {
      localStorage.removeItem(key);
      status.textContent = '이 진행표의 체크·메모를 지웠어요.';
    } catch {
      status.textContent = '화면의 기록은 지웠지만 저장소에 접근할 수 없어요. 브라우저 사이트 데이터에서도 지워 주세요.';
    }
  });
  render();
})();
