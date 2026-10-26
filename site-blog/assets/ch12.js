(() => { 'use strict';
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
 const id=button.dataset.copy, node=document.getElementById(id), status=document.querySelector(`[data-copy-status="${id}"]`);
 const value=node.value ?? node.textContent;
 try {await navigator.clipboard.writeText(value);status.textContent='복사했습니다. 내 메모와 출처를 채워 넣으세요.';}
 catch {status.textContent='자동 복사를 사용할 수 없습니다. 아래 글을 선택해 복사하세요.'; if(node.select){node.focus();node.select();}else{const range=document.createRange();range.selectNodeContents(node);const selection=getSelection();selection.removeAllRanges();selection.addRange(range);}}
}));
const $=id=>document.getElementById(id);
const text={product:'업체로부터 제품을 무료로 제공받아 직접 사용한 뒤 작성했습니다.',both:'업체로부터 제품과 원고료를 제공받아 작성했습니다.',affiliate:'이 글에는 제휴 링크가 포함되어 있으며, 구매가 발생하면 수수료를 받습니다.'};
const update=()=>{
 const place=document.querySelector('input[name="place"]:checked').value,relation=$('disclosure-relation').value,sentence=text[relation],ok=['first','title'].includes(place);
 $('disclosure-value').textContent=ok?'위치 적절':'수정';
 $('disclosure-meaning').textContent=ok?'선택한 위치에서 실제 관계와 충분한 크기·대비·접힘 여부를 확인하세요.':'글 끝·댓글·더보기 뒤에만 두지 말고 제목 또는 본문 첫 부분으로 옮기세요.';
 $('preview-title').textContent=place==='title'?sentence+' 한 달 써 본 생활 가전 후기':'한 달 써 본 생활 가전 후기';
 $('preview-disclosure').hidden=place!=='first';$('preview-disclosure').textContent=sentence;
 $('preview-end').hidden=!['end','hidden'].includes(place);$('preview-end').textContent=(place==='hidden'?'댓글·더보기 뒤: ':'글 끝: ')+sentence;
};
$('disclosure-form').addEventListener('submit',e=>{e.preventDefault();update();});
$('disclosure-form').addEventListener('change',update);
$('disclosure-extreme').addEventListener('click',()=>{$('place-hidden').checked=true;update();});
update();
})();