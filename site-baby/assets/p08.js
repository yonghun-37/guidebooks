/* 실습 8 전용: 표준 시기 참고표. 접종·진료를 판정하지 않는다. */
(() => {
  'use strict';
  const form=document.querySelector('#schedule-form'), target=document.querySelector('#schedule-result');
  const parse=value=>{
    if(!/^\d{4}-\d{2}-\d{2}$/.test(value))throw new Error('생년월일을 입력하세요.');
    const [y,m,d]=value.split('-').map(Number), date=new Date(Date.UTC(y,m-1,d));
    if(y<1900||date.getUTCFullYear()!==y||date.getUTCMonth()!==m-1||date.getUTCDate()!==d)throw new Error('올바른 생년월일을 입력하세요.');
    const now=new Date(), today=new Date(Date.UTC(now.getFullYear(),now.getMonth(),now.getDate()));
    if(date>today)throw new Error('출생 후 실제 생년월일을 넣어 주세요. 출산 전에는 아래 전화 대본부터 준비해요.');
    return date;
  };
  const stamp=date=>date.toISOString().slice(0,10);
  const days=(date,n)=>new Date(date.getTime()+n*86400000);
  const months=(date,n)=>{
    const y=date.getUTCFullYear(),m=date.getUTCMonth()+n,d=date.getUTCDate();
    const end=new Date(Date.UTC(y,m+1,0)).getUTCDate();
    return new Date(Date.UTC(y,m,Math.min(d,end)));
  };
  function render(event){
    event?.preventDefault(); target.replaceChildren();
    try{
      const birth=parse(form.elements.birth.value), route=form.elements.route.value;
      const rows=[['1차 검진 참고 기간',`${stamp(days(birth,14))} ~ ${stamp(days(birth,35))} · 공단 대상조회와 대조`,['N031']],['BCG 피내 · 4주 이내',`${stamp(days(birth,28))}까지의 표준 시기 · 기관과 대조`,['N027']]];
      if(route==='single')rows.push(['B형간염 단독 · 1개월',stamp(months(birth,1))+' 무렵 · 선행 기록 확인',['N027']],['B형간염 단독 · 6개월',stamp(months(birth,6))+' 무렵 · 다음 일정',['N027']]);
      else if(route==='six')rows.push(['6가 혼합 경로','1개월 B형간염 생략 여부를 병원에 확인 · 2·4·6개월 표준 시기',['N027']]);
      else rows.push(['B형간염 경로 확인',route==='individual'?'산모 검사·미숙아·기접종 기록을 알려 담당 기관의 개별 계획을 받아요.':'아직 경로를 정하지 않았어요. 1개월 접종을 자동으로 예약하지 말고 담당 기관에 물어보세요.',['N027']]);
      rows.push(['2개월 접종 참고일',stamp(months(birth,2))+' 무렵 · 성분·종류·간격은 기관 확인',['N027']],['로타 첫 접종 상한 · 14주 6일',stamp(days(birth,104))+' · 상한까지 기다리지 말고 2개월부터 예약',['N027']],['다음 4개월 접종 참고일',stamp(months(birth,4))+' 무렵',['N027']],['2차 검진 · 4~6개월',stamp(months(birth,4))+' 무렵부터 · 정확한 종료일은 공단 대상조회',['N032']]);
      if(route==='six')rows.push(['6가 혼합 · 6개월 참고일',stamp(months(birth,6))+' 무렵',['N027']]);
      const intro=document.createElement('p');intro.textContent='표준 시기 참고표예요. 예약 확정·개인 접종 계획이 아니에요. 달력 월의 같은 날짜가 없으면 말일을 참고일로 표시해요. 실제 시작·종료일과 선행 접종 간격은 기관에서 확인하세요.';target.append(intro);
      const ul=document.createElement('ul');
      for(const [label,value,refs] of rows){
        const li=document.createElement('li'), strong=document.createElement('strong');strong.textContent=label+': ';li.append(strong,document.createTextNode(value));
        refs.forEach(id=>{const sup=document.createElement('sup'),a=document.createElement('a');a.href='../credits.html#'+id.toLowerCase();a.textContent='['+id+']';sup.className='footnote-ref';sup.append(a);li.append(sup);});ul.append(li);
      }target.append(ul);
    }catch(error){target.textContent=error.message;}
  }
  form.addEventListener('submit',render);
  const host=document.querySelector('#booking-record'), fields=[...host.querySelectorAll('input,select')], status=document.querySelector('#booking-status'),key='babybook:booking:v1';
  try{
    const saved=JSON.parse(localStorage.getItem(key)||'{}');
    if(saved&&typeof saved==='object'&&!Array.isArray(saved))fields.forEach(field=>{if(typeof saved[field.name]==='string')field.value=saved[field.name].slice(0,180);});
  }catch{status.textContent='저장값을 읽을 수 없어요. 예약 내용은 종이나 개인 메모에 남겨 주세요.';}
  fields.forEach(field=>field.addEventListener('input',()=>{
    try{localStorage.setItem(key,JSON.stringify(Object.fromEntries(fields.map(f=>[f.name,f.value]))));status.textContent='예약 기록을 이 브라우저에 저장했어요. 실제 예약은 병원 통화로 확인하세요.';}
    catch{status.textContent='저장할 수 없어요. 현재 예약 기록을 인쇄하거나 종이에 옮겨 주세요.';}
  }));
  document.querySelector('#booking-clear').addEventListener('click',()=>{
    try{localStorage.removeItem(key);fields.forEach(field=>{field.value=field.tagName==='SELECT'?field.options[0].value:'';});status.textContent='예약 기록을 지웠어요.';}
    catch{status.textContent='저장값을 지울 수 없어요. 브라우저 설정의 사이트 데이터에서 지워 주세요.';}
  });
})();
