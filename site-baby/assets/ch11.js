/* 11장 전용 가족 일정 배치. 건강·수면량·우울 점수 판정 없음. 저장·통신 없음. */
(function(root){
 'use strict';
 function time(value){
  if(typeof value!=='string'||!/^\d{2}:\d{2}$/.test(value))throw new Error('네 칸의 시간을 모두 입력하세요.');
  const [h,m]=value.split(':').map(Number);
  if(h>23||m>59)throw new Error('실제 시각을 입력하세요.');
  const t=h*60+m;if(t>=1080)return t;if(t<=720)return t+1440;
  throw new Error('오늘 18시부터 다음 날 12시 사이로 입력하세요.');
 }
 function plan({aStart,aEnd,bStart,bEnd}){
  const a=[time(aStart),time(aEnd)],b=[time(bStart),time(bEnd)];
  if(a[1]<=a[0]||b[1]<=b[0])throw new Error('끝 시각을 시작 뒤로 정하세요. 같은 시각은 하루 종일로 계산하지 않습니다.');
  const overlap=[Math.max(a[0],b[0]),Math.min(a[1],b[1])],split=Math.floor((overlap[0]+overlap[1])/2);
  const points=[...new Set([...a,...b,...(overlap[0]<overlap[1]?[split]:[])])].sort((x,y)=>x-y),segments=[];
  for(let i=0;i<points.length-1;i++){
   const start=points[i],end=points[i+1],mid=(start+end)/2,A=mid>=a[0]&&mid<a[1],B=mid>=b[0]&&mid<b[1];
   const owner=A&&B?(mid<split?'A':'B'):A?'A':B?'B':'help';
   const previous=segments[segments.length-1];if(previous&&previous.owner===owner)previous.end=end;else segments.push({start,end,owner});
  }
  const longest=owner=>Math.max(0,...segments.filter(s=>s.owner===owner).map(s=>s.end-s.start));
  return {aRest:longest('B'),bRest:longest('A'),segments};
 }
 const api=Object.freeze({plan});if(typeof module!=='undefined'&&module.exports){module.exports=api;return;}
 root.BabyChapter11=api;
 const form=document.querySelector('#ch11-form');if(!form)return;
 const result=document.querySelector('#ch11-result'),svg=document.querySelector('#ch11-timeline'),list=document.querySelector('#ch11-plan');
 const clock=t=>`${t>=1440?'다음 날 ':''}${String(Math.floor(t/60)%24).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
 const duration=n=>`${Math.floor(n/60)}시간${n%60?' '+(n%60)+'분':''}`;
 function render(){try{
  const p=plan(Object.fromEntries(new FormData(form))),min=Math.min(p.aRest,p.bRest);
  result.textContent=`두 사람 중 짧은 쪽의 가장 긴 휴식 예정: ${duration(min)}. 실제 수유·회복 일정에 맞춰 고치세요. 의학적 목표 시간이 아닙니다.`;
  // Same timeline scale for availability and plan. Outside the chosen span is not counted as rest.
  const x=t=>52+(t-1080)/1080*250;
  let parts='<title>두 사람의 수면 예정 구간과 돌봄 공백</title><g fill="none" stroke="currentColor"><path d="M52 42H302M52 100H302M52 158H302M52 216H302"/></g><g><text x="50" y="25">18시</text><text x="126" y="25">0시</text><text x="210" y="25">6시</text><text x="265" y="25">12시</text><text x="2" y="76">A 수면</text><text x="2" y="133">B 수면</text><text x="2" y="192">도움</text></g>';
  p.segments.forEach(s=>{const y=s.owner==='B'?55:s.owner==='A'?113:171;parts+=`<rect x="${x(s.start)}" y="${y}" width="${x(s.end)-x(s.start)}" height="28" style="fill:var(--soft);stroke:var(--accent);stroke-width:2;${s.owner==='A'?'stroke-dasharray:5 3':s.owner==='help'?'stroke-dasharray:2 3':''}"/>`;});
  parts+='<text x="15" y="247">상대가 맡는 동안 휴식 예정 · 빈 구간 별도 계획</text>';svg.innerHTML=parts;
  list.innerHTML=`<p>A의 가장 긴 휴식 예정: <strong>${duration(p.aRest)}</strong> / B: <strong>${duration(p.bRest)}</strong></p><ul>${p.segments.map(s=>`<li>${clock(s.start)}~${clock(s.end)}: ${s.owner==='help'?'도움 필요 · 다른 어른·지원자에게 요청':s.owner+'가 아기를 맡고 '+(s.owner==='A'?'B':'A')+'는 휴식 예정'}</li>`).join('')}</ul><p>선택한 시간 바깥은 계획에 넣지 않았습니다. 교대가 없는 시간은 돌봄자를 따로 정합니다. 수유로 깬 시간은 휴식에서 빼고 실제 교대표를 조정하세요.</p>`;
 }catch(error){result.textContent=error.message;list.replaceChildren();svg.innerHTML='<title>시간 입력 확인 필요</title>';}}
 form.addEventListener('submit',e=>{e.preventDefault();render();});form.addEventListener('input',render);form.addEventListener('change',render);
 document.querySelector('#ch11-preset').addEventListener('click',()=>{for(const [key,value] of Object.entries({aStart:'18:00',aEnd:'20:00',bStart:'06:00',bEnd:'08:00'}))form.elements[key].value=value;render();});render();
})(typeof window!=='undefined'?window:globalThis);
