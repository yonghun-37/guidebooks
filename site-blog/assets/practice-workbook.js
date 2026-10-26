/* 실습 전용 복사·작업 메모. 외부 통신과 인증 정보 없음. */
(() => {
  'use strict';
  const statuses = [...document.querySelectorAll('[data-work-status]')];
  const say = message => statuses.forEach(node => { node.textContent = message; });
  document.querySelectorAll('[data-copy-target]').forEach(button => {
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      if (!target) return;
      try {
        await navigator.clipboard.writeText(target.textContent);
        say('복사했어요. 내 자료로 바꿔서 사용하세요.');
        button.textContent = '복사했어요';
        setTimeout(() => { button.textContent = '복사'; }, 1800);
      } catch {
        const range = document.createRange(); range.selectNodeContents(target);
        const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
        target.focus(); say('문장을 선택했어요. Ctrl+C 또는 ⌘+C, 휴대폰은 선택 메뉴의 복사로 가져가세요.');
      }
    });
  });
  const key = 'blogbook:worknotes:v1';
  const fields = [...document.querySelectorAll('[data-worknote]')];
  let notes = {}, available = true;
  try {
    const parsed = JSON.parse(localStorage.getItem(key) || '{}');
    if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) {
      notes = Object.fromEntries(Object.entries(parsed).filter(([name,value]) => /^[a-z][a-z0-9-]*$/.test(name) && typeof value === 'string').map(([name,value]) => [name,value.slice(0,12000)]));
    }
    localStorage.setItem(key,JSON.stringify(notes));
  } catch { available = false; }
  const status = () => say(available ? '메모를 이 브라우저에 저장했어요. 중요한 내용은 개인 파일에도 보관하세요.' : '메모를 저장할 수 없어요. 이동 전에 개인 메모 앱이나 파일로 복사하세요.');
  if (!available && fields.length) status();
  fields.forEach(field => {
    field.maxLength = 12000; field.value = notes[field.dataset.worknote] || '';
    field.addEventListener('input', () => {
      notes[field.dataset.worknote] = field.value;
      try { localStorage.setItem(key,JSON.stringify(notes)); available = true; }
      catch { available = false; }
      status();
    });
  });
  document.querySelectorAll('[data-work-clear]').forEach(button => button.addEventListener('click', () => {
    notes = {};
    try { localStorage.removeItem(key); available = true; } catch { available = false; }
    fields.forEach(field => { field.value = ''; });
    say(available ? '이 브라우저의 실습 작업 메모를 지웠어요.' : '현재 화면의 메모는 지웠어요. 브라우저 저장소 접근은 차단돼 있어요.');
  }));
})();
