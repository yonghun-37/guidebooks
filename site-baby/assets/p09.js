/* 실습9 전용. 네트워크 없이 브라우저 저장·CSV 내보내기만 한다. */
(() => {
  'use strict';
  const key='babybook:care-log:v1', form=document.querySelector('#record-form'), status=document.querySelector('#record-status');
  const list=document.querySelector('#record-list'), summary=document.querySelector('#today-summary');
  const labels={breast:'모유',formula:'분유','sleep-start':'잠 시작','sleep-end':'잠 끝',wet:'소변 기저귀',stool:'대변 기저귀',both:'소변+대변'};
  let records=[];
  const localStamp=date=>`${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}T${String(date.getHours()).padStart(2,'0')}:${String(date.getMinutes()).padStart(2,'0')}`;
  const valid=row=>row&&typeof row==='object'&&typeof row.id==='string'&&Object.hasOwn(labels,row.kind)&&typeof row.at==='string'&&/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(row.at)&&Number.isFinite(new Date(row.at).getTime())&&typeof row.note==='string'&&row.note.length<=160&&(row.amount===null||(row.kind==='formula'&&Number.isInteger(row.amount)&&row.amount>=0&&row.amount<=3000));
  try{
    const raw=localStorage.getItem(key), saved=JSON.parse(raw||'[]');
    if(!Array.isArray(saved)||!saved.every(valid))throw new Error('invalid');
    records=saved;status.textContent='이 브라우저에만 저장해요. 다른 기기·탭과 자동으로 합쳐지지 않아요.';
  }catch{status.textContent='저장값을 읽을 수 없어요. 현재 화면에서 새로 기록할 수 있지만, 떠나기 전 CSV를 내려받거나 종이에 옮겨 주세요.';}
  function save(message){
    try{localStorage.setItem(key,JSON.stringify(records));status.textContent=message+' 이 브라우저에 저장했어요.';}
    catch{status.textContent='저장할 수 없어요. 현재 화면의 기록은 남아 있어요. 떠나기 전 CSV를 내려받거나 종이에 옮겨 주세요.';}
  }
  function render(){
    const today=localStamp(new Date()).slice(0,10), todays=records.filter(r=>r.at.slice(0,10)===today);
    const count=k=>todays.filter(r=>k.includes(r.kind)).length;
    summary.textContent=`오늘 ${today} · 수유 ${count(['breast','formula'])}회 (모유 ${count(['breast'])} · 분유 ${count(['formula'])}) · 잠 시작 ${count(['sleep-start'])}회 / 끝 ${count(['sleep-end'])}회 · 소변 ${count(['wet','both'])}회 · 대변 ${count(['stool','both'])}회. 입력한 기록의 요약이며 충분히 먹음·안전을 판정하지 않아요.`;
    list.replaceChildren();
    [...records].sort((a,b)=>b.at.localeCompare(a.at)).forEach(row=>{
      const li=document.createElement('li'),button=document.createElement('button');
      li.append(document.createTextNode(`${row.at.replace('T',' ')} · ${labels[row.kind]}${row.amount===null?'':' · 실제 먹은 '+row.amount+' mL'}${row.note?' · '+row.note:''}`));
      button.type='button';button.textContent='삭제';button.setAttribute('aria-label',row.at.replace('T',' ')+' '+labels[row.kind]+' 기록 삭제');
      button.addEventListener('click',()=>{records=records.filter(r=>r.id!==row.id);save('해당 기록을 지웠어요.');render();});li.append(button);list.append(li);
    });
    if(!records.length){const li=document.createElement('li');li.textContent='아직 남긴 기록이 없어요.';list.append(li);}
  }
  form.elements.at.value=localStamp(new Date());
  form.addEventListener('invalid',event=>{status.textContent=event.target.name==='amount'?'분유량은 0 이상의 정수로 적어요. 이번 입력은 저장하지 않았어요. 모르면 빈칸으로 남겨요.':'입력한 시각과 내용을 확인해 주세요. 이번 입력은 저장하지 않았어요.';},true);
  form.addEventListener('input',()=>{status.textContent='입력 중이에요. 기록할 종류 버튼을 눌러야 저장돼요.';});
  form.addEventListener('submit',event=>{
    event.preventDefault();const kind=event.submitter?.value;
    if(!Object.hasOwn(labels,kind)){status.textContent='기록할 종류 버튼을 눌러 주세요.';return;}
    const at=form.elements.at.value,date=new Date(at);
    if(!Number.isFinite(date.getTime())||localStamp(date)!==at||date>new Date()){status.textContent='실제로 돌본 시각을 입력하세요. 미래 시각은 기록하지 않아요.';return;}
    const amount=kind==='formula'&&form.elements.amount.value!==''?Number(form.elements.amount.value):null;
    if(amount!==null&&(!Number.isInteger(amount)||amount<0||amount>3000)){status.textContent='실제 먹은 분유량을 확인하세요. 모르면 빈칸으로 남겨요.';return;}
    records.push({id:crypto.randomUUID(),kind,at,note:form.elements.note.value.slice(0,160),amount});
    save('기록했어요.');render();form.elements.note.value='';form.elements.amount.value='';form.elements.at.value=localStamp(new Date());
  });
  // Quote all cells, preserve newlines, and neutralize spreadsheet formula prefixes.
  const cell=value=>'"'+String(value??'').replace(/^[\s]*[=+@-]/,match=>"'"+match).replace(/"/g,'""')+'"';
  document.querySelector('#download-csv').addEventListener('click',()=>{
    if(!records.length){status.textContent='내려받을 기록이 없어요. 먼저 실제 돌봄을 기록해 주세요.';return;}
    const rows=[['시각','종류','실제 분유량(mL)','관찰'],...[...records].sort((a,b)=>a.at.localeCompare(b.at)).map(r=>[r.at,labels[r.kind],r.amount,r.note])];
    const blob=new Blob(['\uFEFF'+rows.map(row=>row.map(cell).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=url;a.download='babybook-care-log.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status.textContent='CSV 내려받기를 시작했어요. 개인 기기에서 파일을 확인해 주세요.';
  });
  const confirm=document.querySelector('#clear-confirm'),clear=document.querySelector('#clear-records');
  clear.addEventListener('click',()=>{confirm.hidden=false;document.querySelector('#cancel-clear').focus();});
  document.querySelector('#cancel-clear').addEventListener('click',()=>{confirm.hidden=true;clear.focus();});
  document.querySelector('#confirm-clear').addEventListener('click',()=>{
    records=[];render();confirm.hidden=true;
    try{localStorage.removeItem(key);status.textContent='이 브라우저의 수유·수면·기저귀 기록을 모두 지웠어요.';}
    catch{status.textContent='현재 화면은 비웠지만 저장값을 지울 수 없어요. 브라우저 설정의 사이트 데이터에서 지워 주세요.';}
    clear.focus();
  });
  render();
})();
