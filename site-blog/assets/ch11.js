(() => { 'use strict';
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
 const id=button.dataset.copy, node=document.getElementById(id), status=document.querySelector(`[data-copy-status="${id}"]`);
 const value=node.value ?? node.textContent;
 try {await navigator.clipboard.writeText(value);status.textContent='복사했습니다. 내 메모와 출처를 채워 넣으세요.';}
 catch {status.textContent='자동 복사를 사용할 수 없습니다. 아래 글을 선택해 복사하세요.'; if(node.select){node.focus();node.select();}else{const range=document.createRange();range.selectNodeContents(node);const selection=getSelection();selection.removeAllRanges();selection.addRange(range);}}
}));
const $=id=>document.getElementById(id), form=$('analytics-form');
const n=value=>new Intl.NumberFormat('ko-KR',{maximumFractionDigits:2}).format(value);
const result=(value,meaning,formula='')=>{$('analytics-value').textContent=value;$('analytics-meaning').textContent=meaning;$('analytics-formula').textContent=formula;};
const update=()=>{
 const ctr=$('metric').value==='ctr',names=ctr?['impressions','clicks']:['pv','income'];
 const values={};let bad=false;
 for(const suffix of ['before','after'])for(const name of names){const input=$(name+'-'+suffix);const value=Number(input.value);const valid=input.value.trim()!==''&&Number.isFinite(value)&&value>=0&&input.validity.valid;input.setAttribute('aria-invalid',String(!valid));if(!valid)bad=true;values[name+'-'+suffix]=value;}
 if(bad){result('입력 확인','빈칸은 미집계로 남기고, 음수·잘못된 값은 고친 뒤 계산하세요.');return;}
 const den=suffix=>values[names[0]+'-'+suffix],num=suffix=>values[names[1]+'-'+suffix];
 if(ctr&&['before','after'].some(s=>num(s)>den(s))){result('입력 확인','검색 클릭은 같은 보고서의 노출을 넘을 수 없습니다. 기간·필터를 확인하세요.');return;}
 if(['before','after'].some(s=>den(s)===0)){result('계산 보류','분모가 0인 기간은 계산하지 않습니다. 미집계·광고 게재 상태를 확인하세요.');return;}
 const before=num('before')/den('before')*(ctr?100:1000),after=num('after')/den('after')*(ctr?100:1000);
 if(!Number.isFinite(before)||!Number.isFinite(after)){result('입력 확인','값이 너무 큽니다. 보고서의 숫자와 단위를 다시 확인하세요.');return;}
 let meaning;
 if(ctr){const fit=$('query-fit').value;meaning=fit==='unknown'?'검색어·페이지·기기별 보고서를 먼저 열고 비교할 질문을 고르세요.':fit==='mismatch'?'새 검색어의 비중과 제목의 약속을 비교하고, 질문에 맞는 첫 답변을 고치세요.':after<before?'같은 검색어·기기의 노출과 제목·순위 변화를 함께 확인하세요.':'해결한 질문과 유입 검색어를 기록하고 같은 조건으로 다시 비교하세요.';}
 else meaning=after<before?'페이지 RPM이 내려갔습니다. 예상 수입 합계·유입 구성·광고 게재 상태를 함께 확인하세요.':'페이지 RPM과 예상 수입 합계를 따로 기록하고 확정·입금 상태를 확인하세요.';
 result(n(after)+(ctr?'%':'원'),meaning,`앞 기간 ${n(before)}${ctr?'%':'원'} → 뒤 기간 ${n(after)}${ctr?'%':'원'} / 뒤 기간: ${n(num('after'))} ÷ ${n(den('after'))} × ${ctr?100:1000} = ${n(after)}${ctr?'%':'원'}`);
};
form.addEventListener('submit',e=>{e.preventDefault();update();});
const sync=()=>{const ctr=$('metric').value==='ctr';$('query-fit').disabled=!ctr;$('query-fit').parentElement.hidden=!ctr;for(const name of ['impressions','clicks','pv','income'])for(const suffix of ['before','after']){const input=$(name+'-'+suffix);input.disabled=ctr?!['impressions','clicks'].includes(name):!['pv','income'].includes(name);input.parentElement.hidden=input.disabled;input.removeAttribute('aria-invalid');}update();};
$('metric').addEventListener('change',sync);
$('analytics-default').addEventListener('click',()=>{const data={impressions:[1000,2000],clicks:[50,40],pv:[1000,2000],income:[1000,1000]};for(const [name,values]of Object.entries(data))['before','after'].forEach((s,i)=>$(name+'-'+s).value=values[i]);$('query-fit').value='mismatch';sync();});
$('analytics-zero').addEventListener('click',()=>{for(const name of ['impressions','clicks','pv','income'])for(const suffix of ['before','after'])$(name+'-'+suffix).value='0';update();});
$('analytics-missing').addEventListener('click',()=>{for(const input of form.querySelectorAll('input'))input.value='';result('미집계','숫자가 아직 없으므로 계산하지 않습니다. 집계 후 같은 기간의 값으로 채우세요.');});
sync();
})();