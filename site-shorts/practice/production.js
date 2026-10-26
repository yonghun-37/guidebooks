/* 실습편의 유형 선택과 가상 자막 시간 연습. 계정·네트워크 작업 없음. */
(() => {
 'use strict';
 const choice=document.querySelector('.route-choice');
 if(choice) {
  const messages={film:'60분 · 폰 촬영·녹음과 AI 자동 자막으로 만들어요. 준비·업로드 시간은 더하세요.',explain:'65분 · 녹음/TTS와 스톡·AI 이미지로 설명해요. 준비·업로드 시간은 더하세요.',generate:'80분 + 생성 대기 · 기준 이미지와 짧은 샷을 연결해요. 무료 접근·크레딧을 먼저 확인하세요.'};
  const render=()=>{document.querySelector('[data-route-result]').textContent=messages[choice.querySelector(':checked').value];};
  choice.addEventListener('change',render);choice.addEventListener('practice-restored',render);render();
 }
 const lab=document.querySelector('[data-caption-lab]');
 if(!lab)return;
 const head=lab.querySelector('#playhead'),end=lab.querySelector('#caption-end'),play=lab.querySelector('[data-caption-play]'),loop=lab.querySelector('[data-caption-loop]');
 let running=false,previous=0,frame;
 const render=()=>{
  const time=Number(head.value),stop=Number(end.value),delta=stop-6;
  lab.querySelector('[data-caption-preview]').style.visibility=time<=stop?'visible':'hidden';
  lab.querySelector('[data-caption-result]').textContent=`${Math.abs(delta).toFixed(1)}초 ${delta<0?'일찍 끝나요. 말이 끝나는 6초까지 늘려 보세요.':delta>0?'늦게 끝나요. 다음 문장과 겹치지 않는지 보세요.':'차이예요. 가상 발화와 자막의 끝이 맞아요.'}`;
  head.setAttribute('aria-valuetext',`${time.toFixed(1)}초`);end.setAttribute('aria-valuetext',`${stop.toFixed(1)}초`);
 };
 const pause=()=>{running=false;cancelAnimationFrame(frame);play.textContent='재생';previous=0;};
 const tick=now=>{
  if(!running)return;
  const dt=previous?(now-previous)/1000:0;previous=now;
  let time=Number(head.value)+dt;
  if(loop.checked&&time>=6)time%=6;
  else if(time>=12){time=12;pause();}
  head.value=String(time);render();if(running)frame=requestAnimationFrame(tick);
 };
 play.addEventListener('click',()=>{if(running){pause();return;}if(Number(head.value)>=12)head.value='0';running=true;play.textContent='일시 정지';frame=requestAnimationFrame(tick);});
 // Fine enough increments to preserve frame stepping even though the labelled slider is rounded for reading.
 head.step='0.001';
 [head,end].forEach(input=>input.addEventListener('input',()=>{pause();render();}));
 lab.querySelector('[data-caption-frame]').addEventListener('click',()=>{pause();head.value=String(Math.min(12,Number(head.value)+1/30));render();});
 lab.querySelector('[data-caption-fix]').addEventListener('click',()=>{pause();end.value='6';render();});
 lab.querySelector('[data-caption-bad]').addEventListener('click',()=>{pause();end.value='1';head.value='3';render();});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
 render();
})();
