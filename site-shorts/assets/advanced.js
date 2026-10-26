/* 심화편 도구: 네트워크 호출 없음. 비용 입력은 저장하지 않는다. */
(() => {
 'use strict';
 const byId = id => document.getElementById(id);
 const calculator = byId('calculator');
 if (calculator) {
  const names = ['count','llm','tts','images','video','retry','cap'];
  const fields = Object.fromEntries(names.map(name => [name, byId(`cost-${name}`)]));
  const result = byId('cost-result'), detail = byId('cost-detail'), chart = byId('cost-chart'), breakdown = byId('cost-breakdown');
  const render = () => {
   if (Object.values(fields).some(input => input.value.trim() === '' || !input.validity.valid || !Number.isFinite(Number(input.value)))) {
    result.textContent = '계산할 수 없어요 · 모든 칸에 허용 범위의 숫자를 넣으세요.'; detail.textContent = ''; if (breakdown) breakdown.textContent = ''; chart.hidden = true; chart.style.display = 'none'; return;
   }
   const value = Object.fromEntries(names.map(name => [name, Number(fields[name].value)]));
   const pieces = [value.llm, value.tts, value.images * .03375, value.video * .05];
   const per = pieces.reduce((a,b) => a+b,0), base = per * value.count, total = base * (1 + value.retry / 100);
   result.textContent = `월 $${total.toFixed(5)} · ${total > value.cap ? '내 월 상한을 초과해요. 편수·장면·재생성을 줄이세요.' : '내 월 상한 안이에요. 고정비와 실제 usage도 더 확인하세요.'}`;
   detail.textContent = `편당 $${per.toFixed(5)} × ${value.count}편 = $${base.toFixed(5)} + 추가 생성 허용 ${value.retry}%. 월 상한 $${value.cap.toFixed(2)}.`;
   chart.hidden = false; chart.style.display = ''; chart.replaceChildren();
   const ns = 'http://www.w3.org/2000/svg';
   const add = (tag,attrs,text) => { const el=document.createElementNS(ns,tag); Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,String(v))); if(text)el.textContent=text;chart.append(el); };
   const monthly = pieces.map(n=>n*value.count), max=Math.max(.00001,...monthly);
   const labels=['LLM','TTS','이미지','영상'];
   if (breakdown) breakdown.textContent = '월 항목별 비용: '+labels.map((s,i)=>`${s} $${monthly[i].toFixed(5)}`).join(' · ');
   add('title',{},'가상 월 생성비: '+labels.map((s,i)=>`${s} $${monthly[i].toFixed(5)}`).join(', '));
   monthly.forEach((n,i)=>{add('text',{x:0,y:20+i*42},`${labels[i]} $${n.toFixed(5)}`);add('rect',{x:135,y:7+i*42,width:n/max*220,height:18,rx:3});});
  };
  calculator.addEventListener('input',render); calculator.addEventListener('change',render);
  calculator.querySelectorAll('[data-cost-preset]').forEach(button=>button.addEventListener('click',()=>{
   const type=button.dataset.costPreset;
   const values = type==='image' ? [30,.016,.018,6,0,20,10] : type==='extreme' ? [300,.016,.018,6,60,100,10] : [30,.0008,.0024,0,0,20,10];
   names.forEach((name,i)=>{fields[name].value=String(values[i]);});render();
  }));render();
 }
 const gate=byId('gate-lab');
 if(gate){const render=()=>{const test=byId('gate-case').value, mode=byId('gate-mode').value;
  byId('gate-result').textContent=test!=='pass'?`예외 대기열 · ${test} 검사 실패라 게시하지 않아요. 원인을 고친 뒤 새 검수로 돌아가세요.`:mode==='auto'?'자동 게시 · 명시한 공개 범위로 업로드해요. private면 비공개예요.':mode==='post_review'?'예약 · 공개 전 거부할 수 있어요. 취소 완료 응답을 확인하세요.':'승인 대기 · 검사를 통과해도 현재 모드는 직접 승인이 필요해요.';
 };gate.addEventListener('change',render);render();}
 const runner=byId('runner-choice');
 if(runner){const render=()=>{byId('runner-result').textContent=byId('runner-pc').value==='yes'?'로컬 · 현재 PC에서 mock 예약부터 확인하세요.':byId('runner-state').value==='yes'?'GitHub Actions · 단일 실행과 상태 pull·push를 유지하고 mock부터 돌리세요.':'이전 준비 · 외부 상태 복구·단일 실행을 시험하기 전에는 로컬을 유지하세요.';};runner.addEventListener('change',render);render();}
 // 다른 페이지에서 확인한 키도 보존한다. 기존 실습편 진행 키와 분리한다.
 const key='shortsbook:advanced:v1',checks=[...document.querySelectorAll('[data-advanced-check]')];
 let saved={},stored=true;
 const read=()=>{saved={};try{const data=JSON.parse(localStorage.getItem(key)||'{}');if(data&&typeof data==='object'&&!Array.isArray(data))for(const [name,value] of Object.entries(data))if(/^(A\d+|requirements|live):[\w-]+$/.test(name)&&value===true)saved[name]=true;}catch{stored=false;}};
 const status=()=>{document.querySelectorAll('[data-advanced-progress]').forEach(el=>{el.textContent=`${checks.filter(input=>input.checked).length}/${checks.length} 확인 · ${stored?'이 브라우저에만 저장해요.':'저장할 수 없어요. 현재 페이지에서만 확인하고 개인 메모에 남기세요.'}`;});};
 const restore=()=>{checks.forEach(input=>{input.checked=saved[input.dataset.advancedCheck]===true;});status();};
 const save=()=>{try{localStorage.setItem(key,JSON.stringify(saved));stored=true;}catch{stored=false;}status();};
 read();restore();
 checks.forEach(input=>input.addEventListener('change',()=>{if(input.checked)saved[input.dataset.advancedCheck]=true;else delete saved[input.dataset.advancedCheck];save();}));
 document.querySelectorAll('[data-advanced-reset]').forEach(button=>button.addEventListener('click',()=>{saved={};checks.forEach(input=>{input.checked=false;});save();}));
 window.addEventListener('storage',event=>{if(event.key===key){read();restore();}});
})();
