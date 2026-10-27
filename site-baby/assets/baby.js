/* 기관 연락처와 신청 상태만 저장. 원문 서류·개인 식별정보·네트워크 요청 없음. */
(() => {
  'use strict';
  const storage={
    read(key) {try {const value=JSON.parse(localStorage.getItem('babybook:'+key)||'{}');return value&&typeof value==='object'&&!Array.isArray(value)?value:{};}catch{return {}; }},
    write(key,value) {try {localStorage.setItem('babybook:'+key,JSON.stringify(value));return true;}catch{return false;}},
    remove(key) {try {localStorage.removeItem('babybook:'+key);return true;}catch{return false;}}
  };
  const contacts=[['emergency','응급 연락','119'],['pediatric','담당 소아과 · 이름 / 전화',''],['er','가까운 응급실 · 전화 / 소아 진료 여부',''],['night','야간·휴일 진료기관 · 이름 / 전화','']];
  const fields=[...document.querySelectorAll('[data-contact-fields]')];
  const saved=storage.read('contacts:v1');
  fields.forEach((host,index)=>{
    host.className='contact-fields';host.replaceChildren();
    contacts.forEach(([key,label,initial])=>{
      const wrapper=document.createElement('label');wrapper.textContent=label;
      const input=document.createElement('input');input.type='text';input.maxLength=140;input.dataset.contact=key;input.id=`contact-${index}-${key}`;
      input.value=key==='emergency'?initial:typeof saved[key]==='string'?saved[key].slice(0,140):'';
      input.readOnly=key==='emergency';
      const print=document.createElement('span');print.className='print-field';print.textContent=input.value||'________________________________________________';
      wrapper.append(input,print);host.append(wrapper);
      input.addEventListener('input',()=>{
        print.textContent=input.value||'________________________________________________';
        const values=Object.fromEntries([...host.querySelectorAll('input[data-contact]')].filter(field=>!field.readOnly).map(field=>[field.dataset.contact,field.value]));
        const success=storage.write('contacts:v1',values);
        document.querySelectorAll('[data-contact-status]').forEach(node=>node.textContent=success?'기관 연락처를 이 브라우저에 저장했습니다.':'저장할 수 없습니다. 이동 전 종이에 옮기거나 현재 페이지를 인쇄하세요.');
      });
    });
  });
  document.querySelectorAll('[data-contact-status]').forEach(node=>node.textContent='입력은 이 브라우저의 저장소에만 남습니다. 공용 기기에서는 사용 후 지우세요.');
  document.querySelectorAll('[data-contact-clear]').forEach(button=>button.addEventListener('click',()=>{
    const success=storage.remove('contacts:v1');
    fields.forEach(host=>host.querySelectorAll('input:not([readonly])').forEach(input=>{input.value='';input.nextElementSibling.textContent='________________________________________________';}));
    document.querySelectorAll('[data-contact-status]').forEach(node=>node.textContent=success?'저장한 연락처를 지웠습니다.':'저장소 접근이 막혀 저장값을 지울 수 없습니다. 브라우저 설정에서 사이트 데이터를 지우세요.');
  }));
  const record=document.querySelector('[data-completion-record]');
  if(record){
    const state=storage.read('applications:v1'), inputs=[...record.querySelectorAll('[data-record]')];
    const status=document.querySelector('[data-record-status]');
    inputs.forEach(input=>{
      const value=state[input.dataset.record];
      if(typeof value==='string') input.value=value.slice(0,100);
      const print=input.nextElementSibling;
      const sync=()=>{if(print?.classList.contains('print-field'))print.textContent=input.value||'________________';}; sync();
      input.addEventListener('input',()=>{sync();status.textContent=storage.write('applications:v1',Object.fromEntries(inputs.map(field=>[field.dataset.record,field.value])))?'신청 항목·상태·확인일을 이 브라우저에 저장했어요.':'저장할 수 없어요. 이동 전 종이나 개인 메모에 남기세요.';});
    });
    document.querySelector('[data-record-clear]').addEventListener('click',()=>{
      const success=storage.remove('applications:v1');inputs.forEach(input=>{input.value='';input.dispatchEvent(new Event('change'));if(input.nextElementSibling)input.nextElementSibling.textContent='________________';});
      status.textContent=success?'이 브라우저의 신청 기록을 지웠어요.':'저장값을 지울 수 없어요. 브라우저 설정에서 사이트 데이터를 지우세요.';
    });
  }
  document.querySelectorAll('[data-print]').forEach(button=>button.addEventListener('click',()=>window.print()));
})();
