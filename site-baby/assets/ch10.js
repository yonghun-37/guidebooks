/* 10장 전용: 2026 금액을 고정한 월령별 비교. 미래 연도 정책 예측 아님.
   N036 N037 N095 N105. 공용 단면 계산기·공용 이벤트는 변경하지 않는다. */
(function(root){
 'use strict';
 const AS_OF='2026-10-27', regions=Object.freeze({capital:100000,other:105000,preferred:110000,special:120000});
 function parseDate(value){
  if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(value))throw new Error('출생일을 정확히 입력하세요.');
  const d=new Date(value+'T00:00:00Z');
  if(!Number.isFinite(+d)||d.toISOString().slice(0,10)!==value)throw new Error('실제 달력에 있는 출생일을 입력하세요.');
  return d;
 }
 function addMonths(date,months){
  const y=date.getUTCFullYear(),m=date.getUTCMonth()+months;
  const last=new Date(Date.UTC(y,m+1,0)).getUTCDate();
  return new Date(Date.UTC(y,m,Math.min(date.getUTCDate(),last))).toISOString().slice(0,10);
 }
 function calculate({birth,order,transition,region,payment="unknown"}){
  const date=parseDate(birth),now=parseDate(AS_OF);
  if(date>now)throw new Error('조사일 뒤 출생은 계산하지 않습니다. 출생 후 현행 안내를 확인하세요.');
  let age=(now.getUTCFullYear()-date.getUTCFullYear())*12+now.getUTCMonth()-date.getUTCMonth();
  if(now.getUTCDate()<date.getUTCDate())age--;
  if(age>=24)throw new Error('조사일 기준 0~23개월 출생일을 입력하세요.');
  if(!['first','later'].includes(order)||!['unknown',...Object.keys(regions)].includes(region)||(transition!==null&&(!Number.isInteger(transition)||transition<0||transition>23)))throw new Error('출생순위·전환 월령·지역 선택을 확인하세요.');
  if(!['unknown','cash','voucher'].includes(payment))throw new Error('아동수당 지급 수단을 확인하세요.');
  const child=region==='unknown'?null:regions[region];
  const rows=Array.from({length:24},(_,month)=>{
   const daycare=transition!==null&&month>=transition,base=month<12?1000000:500000;
   const childcare=daycare?(month<12?584000:515000):0,parent=Math.max(0,base-childcare);
   return Object.freeze({month,date:addMonths(date,month),daycare,parent,child,childcare,payment,monthly:child===null||payment==='unknown'?null:parent+(payment==='cash'?child:0)});
  });
  return Object.freeze({asOf:AS_OF,age,rows:Object.freeze(rows),firstMeeting:order==='first'?2000000:3000000,localVoucherPossible:['preferred','special'].includes(region)});
 }
 const api=Object.freeze({calculate,AS_OF});
 if(typeof module!=='undefined'&&module.exports){module.exports=api;return;}
 root.BabyChapter10=api;
 const form=document.querySelector('#ch10-form');if(!form)return;
 const result=document.querySelector('#benefits-result'),table=document.querySelector('#ch10-months'),vouchers=document.querySelector('#ch10-vouchers');
 const won=n=>n===0?'0원':(n/10000).toLocaleString('ko-KR',{maximumFractionDigits:1})+'만 원';
 const ref=id=>`<sup class="footnote-ref"><a href="${window.BabyBook.url('credits.html')}#${id.toLowerCase()}">[${id}]</a></sup>`;
 function render(){
  try{
   const transition=form.elements.transition.value==='none'?null:Number(form.elements.transition.value);
   const r=calculate({birth:form.elements.birth.value,order:form.elements.order.value,transition,region:form.elements.region.value,payment:form.elements.payment.value}),current=r.rows[r.age];
   result.textContent=`조사일 기준 ${r.age}개월 · 월 현금 ${current.monthly===null?'합계 확인 필요':won(current.monthly)}. 아래 24개 행은 2026 금액 비교이며 실제 지급 내역·미래 정책 예측이 아닙니다.`;
   vouchers.innerHTML=`<p><strong>1회 바우처 · 첫만남이용권 ${won(r.firstMeeting)}</strong>${ref('N036')}</p><p>보육료 바우처는 아래 표에서 별도 표시하며 현금에 더하지 않습니다.${ref('N037')}</p>${r.localVoucherPossible?`<p>해당 지역의 상품권 추가 1만 원은 제외했습니다. 기본 아동수당도 상품권일 수 있어요. 시행 여부·지급 방식을 주민센터에 확인하세요.${ref('N095')}${ref('N105')}</p>`:''}`;
   table.innerHTML=`<p id="ch10-table-help">표를 좌우·위아래로 움직여 볼 수 있습니다. 날짜는 월령 시작 참고일이며 입금일·실제 서비스 전환일이 아닙니다. 지역 모름은 아동수당·합계를 확인 필요로 남깁니다.${ref('N037')}${ref('N095')}</p><div class="table-wrap" role="region" aria-label="출생부터 23개월 월별 비교표" aria-describedby="ch10-table-help" tabindex="0"><table><caption>0~23개월 현금·아동수당 비교 · 2026 금액 고정 비교</caption><thead><tr><th scope="col">월령·시작 참고일</th><th scope="col">돌봄</th><th scope="col">부모급여 현금</th><th scope="col">아동수당 · 지급 수단</th><th scope="col">월 현금 합계</th><th scope="col">보육료 바우처</th></tr></thead><tbody>${r.rows.map(row=>`<tr${row.month===transition?' class="transition-row"':''}><th scope="row">${row.month}개월<br>${row.date}${row.month===transition?'<br>어린이집 전환':''}</th><td>${row.daycare?'어린이집':'가정양육'}</td><td>${won(row.parent)}</td><td>${row.child===null?'10만 원 이상, 지역 확인 필요':won(row.child)+' · '+(row.payment==='cash'?'현금':row.payment==='voucher'?'지역상품권':'현금/지역상품권 확인 필요')}</td><td>${row.monthly===null?'확인 필요':won(row.monthly)}</td><td>${won(row.childcare)}</td></tr>`).join('')}</tbody></table></div>`;
  }catch(error){result.textContent=error.message;table.replaceChildren();vouchers.replaceChildren();}
 }
 form.addEventListener('submit',e=>{e.preventDefault();render();});form.addEventListener('input',render);form.addEventListener('change',render);
 document.querySelector('[data-benefit-preset]').addEventListener('click',()=>{form.elements.birth.value='2025-10-27';form.elements.transition.value='12';form.elements.order.value='first';form.elements.region.value='unknown';form.elements.payment.value='unknown';render();});
 render();
})(typeof window!=='undefined'?window:globalThis);
