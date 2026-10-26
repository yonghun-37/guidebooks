"use strict";
const format = n => n.toLocaleString('ko-KR');
const axis = document.querySelector('#axis-picker');
if(axis){
 const form=document.querySelector('#axis-inputs'), result=document.querySelector('#axis-result');
 const label=(id,title,value,step=1,max=1000000000)=>`<label>${title}<input id="${id}" type="number" min="0" max="${max}" step="${step}" value="${value}" required></label>`;
 const run=()=>{
  if(axis.value==='views'){result.innerHTML='<strong>보너스 초대 없는 새 계정의 조회수 보상</strong><span class="draft-big">0원</span><p>조회수를 돈으로 바꾸는 일반 요금표가 없습니다. 협찬·구매가 생긴 경우는 다른 축에서 계산하세요.</p>';return;}
  const inputs=[...form.querySelectorAll('input')];
  if(inputs.some(i=>!i.validity.valid||!i.value.trim())){result.textContent='빈칸을 채우고 표시된 범위 안의 숫자를 넣어 주세요.';return;}
  const [price,count,rate]=inputs.map(i=>Number(i.value));
  const total=axis.value==='affiliate'?price*count*rate/100:price*count;
  result.innerHTML=`<strong>이 입력으로 계산한 ${axis.value==='affiliate'?'제휴 수수료':'받을 돈'}</strong><span class="draft-big">${format(Math.round(total))}원</span><p>${format(price)}원 × ${format(count)}${axis.value==='affiliate'?'건 × '+rate+'%':'건'} = ${format(Math.round(total))}원</p><p class="draft-small">가상 계산 · 취소 없는 거래 · 비용·수수료·세금 전. 실제 계약·구매가 있어야 생기는 금액입니다.</p>`;
 };
 const render=()=>{form.innerHTML=axis.value==='views'?'<p>초대나 별도 보상 계약이 없는 한국 새 계정을 가정합니다.</p>':label('calc-price',axis.value==='affiliate'?'인정 구매 1건 금액 (원)':'한 건 가격 (원)',axis.value==='brand'?200000:axis.value==='affiliate'?50000:10000)+label('calc-count','한 달 성사 건수',axis.value==='brand'?1:axis.value==='affiliate'?20:10,1,1000000)+(axis.value==='affiliate'?label('calc-rate','적용 수수료율 (%) · 공개 가이드 기본 3%',3,0.1,100):'');run();};
 axis.addEventListener('change',render);form.addEventListener('input',run);render();
}
const picker=document.querySelector('#question-picker');
if(picker){const show=()=>{const card=document.getElementById(picker.value);const dest=document.querySelector('#question-result');dest.replaceChildren();const h=document.createElement('h3');h.textContent=card.querySelector('h3').textContent;const p=card.querySelector('.draft-answer').cloneNode(true);const a=document.createElement('a');a.href='#'+picker.value;a.textContent='이 답의 숫자·할 일 읽기 →';dest.append(h,p,a);};picker.addEventListener('change',show);show();}
const slider=document.querySelector('#stage-slider');
if(slider){const show=()=>{const card=document.querySelectorAll('.draft-stage')[Number(slider.value)];document.querySelector('#stage-label').textContent=card.dataset.followers+'명';const result=document.querySelector('#stage-result');result.replaceChildren();const h=document.createElement('h3');h.textContent=card.querySelector('h3').textContent;result.append(h,card.querySelector('.stage-math').cloneNode(true),card.querySelector('.draft-action').cloneNode(true));};slider.addEventListener('input',show);show();}
for(const box of document.querySelectorAll('[data-draft-check]')){const key='reelsbook:phase8s:'+document.body.dataset.variant+':'+box.dataset.draftCheck;try{box.checked=localStorage.getItem(key)==='1';}catch{}box.addEventListener('change',()=>{try{localStorage.setItem(key,box.checked?'1':'0');}catch{const status=document.querySelector('#save-status');if(status)status.textContent='저장할 수 없는 환경입니다. 메모는 따로 보관하세요.';}});}
