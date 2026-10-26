(() => { 'use strict';
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
 const id=button.dataset.copy, node=document.getElementById(id), status=document.querySelector(`[data-copy-status="${id}"]`);
 const value=node.value ?? node.textContent;
 try {await navigator.clipboard.writeText(value);status.textContent='복사했습니다. 내 메모와 출처를 채워 넣으세요.';}
 catch {status.textContent='자동 복사를 사용할 수 없습니다. 아래 글을 선택해 복사하세요.'; if(node.select){node.focus();node.select();}else{const range=document.createRange();range.selectNodeContents(node);const selection=getSelection();selection.removeAllRanges();selection.addRange(range);}}
}));
const data={info:['공식 공고','대상·기간·신청 절차의 원문을 먼저 모읍니다.'],review:['사용 메모','직접 쓴 환경·장단점·제공 관계와 사진을 먼저 모읍니다.'],travel:['동선·사진','실제 이동 순서·놓친 점·내 사진을 먼저 모읍니다.']};
const select=document.getElementById('template-kind');
select.addEventListener('change',()=>{const [a,b]=data[select.value];document.getElementById('template-value').textContent=a;document.getElementById('template-meaning').textContent=b;});
})();