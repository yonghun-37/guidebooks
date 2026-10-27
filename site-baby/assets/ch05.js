(() => { 'use strict';
 document.querySelectorAll('[data-prep]').forEach(tool => {
  const inputs=[...tool.querySelectorAll('input[type="checkbox"]')], result=tool.querySelector('[data-prep-result]');
  const update=()=>{ result.textContent=`${inputs.filter(input=>input.checked).length}개 · 메모한 항목 수입니다. 아기 상태를 판정하지 않습니다.`; };
  inputs.forEach(input=>input.addEventListener('change',update));update();
 });
})();
