/* 심화편 전용 계산·진행 기록. 외부 요청과 비밀 입력은 없다. */
(() => {
  'use strict';
  const calculator = document.querySelector('#cost-calculator');
  if (calculator) {
    const fields = ['count','input','output','images','allowance','cap'].map(name => calculator.querySelector(`#cost-${name}`));
    const provider = calculator.querySelector('#cost-provider');
    const rates = { luna:[0.1,0.5], gemini:[0.3,2.5], haiku:[0.1,0.5], sol:[2,10] };
    const result = calculator.querySelector('#monthly-cost');
    const bar = calculator.querySelector('[data-cost-bar]');
    const caption = calculator.querySelector('[data-cost-caption]');
    const render = () => {
      const valid = fields.every(input => input.value.trim() !== '' && input.validity.valid && Number.isFinite(input.valueAsNumber));
      if (!valid || !rates[provider.value]) {
        result.textContent = '입력 범위를 확인하세요. 편수·토큰·이미지는 0 이상의 정수, 상한은 0 이상이에요.';
        bar.style.width = '0%'; bar.classList.remove('over');
        caption.textContent = '입력을 확인하면 상한과 비교해요.';
        bar.parentElement.setAttribute('aria-label', '입력 오류로 비용 비교를 표시하지 않음');
        return;
      }
      const [count, input, output, images, allowance, cap] = fields.map(field => field.valueAsNumber);
      const [inputRate, outputRate] = rates[provider.value];
      const monthly = count * ((input*inputRate+output*outputRate)/1e6+images*0.03375) * (1+allowance/100);
      const over = monthly > cap;
      result.textContent = `$${monthly.toFixed(5)}/월 · ${over ? '상한을 넘어요. 편수·이미지·추가 생성을 줄이세요.' : '가정한 생성비가 상한 안에 있어요.'}`;
      const proportion = cap > 0 ? monthly/cap*100 : (monthly > 0 ? 100 : 0);
      bar.style.width = `${Math.min(100,proportion)}%`;
      bar.classList.toggle('over',over);
      caption.textContent = `예상 $${monthly.toFixed(5)} / 상한 $${cap.toFixed(2)} · ${cap > 0 ? proportion.toFixed(1)+'%' : '상한 0'}. 이 화면은 과금을 중지하지 않아요.`;
      bar.parentElement.setAttribute('aria-label', caption.textContent);
    };
    calculator.addEventListener('input', render);
    calculator.addEventListener('change', render);
    calculator.querySelector('[data-cost-extreme]').addEventListener('click', () => { fields[0].value='3000'; fields[3].value='5'; render(); });
    calculator.querySelector('[data-cost-reset]').addEventListener('click', () => { fields.forEach((field,i) => {field.value=[30,3000,1000,0,0,1][i];}); provider.value='luna'; render(); });
    render();
  }
  const key = 'reelsbook:advanced:v1';
  const allowed = new Set([...Array.from({length:10},(_,i)=>`a${i}`),'account','budget','public','live-post','live-next','live-metrics']);
  const inputs = [...document.querySelectorAll('[data-advanced-check]')];
  if (!inputs.length) return;
  let state = {}, available = true;
  const read = () => {
    state = {};
    try {
      const value = JSON.parse(localStorage.getItem(key) || 'null');
      if (value?.version === 1 && value.checks && typeof value.checks === 'object' && !Array.isArray(value.checks)) {
        state = Object.fromEntries(Object.entries(value.checks).filter(([name,value])=>allowed.has(name) && value===true));
      }
    } catch { /* 손상/차단된 저장소에서도 현재 화면의 체크는 유지한다. */ }
  };
  const announce = () => {
    const count = Object.keys(state).length;
    document.querySelectorAll('[data-advanced-status]').forEach(node => {
      node.textContent = `${count}/${allowed.size} 확인 · ` + (available ? '이 브라우저에만 저장해요. 키트 실행 기록과는 따로예요.' : '저장할 수 없어요. 현재 화면에서 체크한 뒤 이동 전에 개인 메모를 남기세요.');
    });
    document.querySelectorAll('[data-advanced-progress]').forEach(node => {node.max=allowed.size;node.value=count;});
  };
  const restore = () => {inputs.forEach(input=>{input.checked=state[input.dataset.advancedCheck]===true;});announce();};
  const save = () => {
    try {localStorage.setItem(key,JSON.stringify({version:1,checks:state}));available=true;}
    catch {available=false;}
    announce();
  };
  read(); restore(); save();
  inputs.forEach(input=>input.addEventListener('change',()=>{
    if (input.checked) state[input.dataset.advancedCheck]=true;
    else delete state[input.dataset.advancedCheck];
    inputs.filter(other=>other.dataset.advancedCheck===input.dataset.advancedCheck).forEach(other=>{other.checked=input.checked;});
    save();
  }));
  document.querySelectorAll('[data-advanced-reset]').forEach(button=>button.addEventListener('click',()=>{state={};save();restore();}));
  window.addEventListener('storage',event=>{if(event.key===key){read();restore();}});
})();
