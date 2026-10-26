/* AIa 전용: 선택 도우미, 복사, 모델 검색과 공개 가정 비용 계산. */
(() => {
 'use strict';
 const $ = id => document.getElementById(id);
 const money = value => new Intl.NumberFormat('ko-KR',{maximumFractionDigits:2}).format(value);
 if ($('tool-content')) {
  const update = () => {
   const content=$('tool-content').value,paid=$('tool-budget').value==='paid',ko=$('tool-korean').value==='yes';
   let combo,price,reason;
   if(paid&&content==='video'){
    price='월 29,000원';combo='ChatGPT Free → Google AI Pro의 Flow → Clipchamp Free + 본인 녹음';
    reason='생성 장면에 예산을 집중합니다. 미리캔버스·타입캐스트 구독 대신 고르는 교체안입니다.';
   }else if(paid&&content==='cards'){
    price='월 14,900원';combo='ChatGPT Free → 미리캔버스 Pro';
    reason='카드에는 음성 구독이 필요하지 않습니다. 한국어 템플릿과 소재에만 예산을 씁니다. 해설도 함께 만들 때 타입캐스트 Basic을 더하면 월 24,800원입니다.';
   }else if(paid){
    price='월 24,800원';combo='ChatGPT Free → 미리캔버스 Pro → 타입캐스트 Basic → Clipchamp Free';
    reason='디자인과 해설 음성에 함께 쓰는 조합입니다. 카드만 만들면 타입캐스트를 빼고 월 14,900원으로 시작합니다.';
   }else{
    price='추가 구독료 0원';combo='ChatGPT Free → Canva Free → Clipchamp Free + 본인 소재·녹음';
    reason=content==='video'?'무료 생성 영상의 당일 완성은 보장하지 않습니다. 먼저 직접 촬영한 장면으로 완성하고, Flow는 접근·잔여량이 있을 때만 시험합니다.':'글은 무료 채팅, 장면은 본인 사진·도형, 소리는 본인 녹음으로 끝까지 만듭니다.';
   }
   $('tool-price').textContent=price;$('tool-combo').textContent=combo;
   $('tool-reason').textContent=reason+' '+(ko?'한국어가 필요하므로 제목은 편집기에서 입력하고, 날짜·단위가 들어간 문장으로 자막과 목소리를 시험하세요.':'영어 지시문도 사용할 수 있습니다. 내보낼 언어의 글자·발음과 소재 이용 조건은 그대로 확인하세요.');
   $('tool-next').href={cards:'../practice/04-cards.html',motion:'../practice/05-reel.html',explain:'../practice/05-reel.html',video:'08-reels.html#generated'}[content];
  };
  ['tool-content','tool-budget','tool-korean'].forEach(id=>$(id).addEventListener('change',update));
  document.querySelector('[data-tool-preset]').addEventListener('click',()=>{$('tool-content').value='video';$('tool-budget').value='free';$('tool-korean').value='yes';update()});
  update();
 }
 document.querySelectorAll('[data-prompt]').forEach(root=>{
  const input=root.querySelector('textarea'),status=root.querySelector('[data-copy-status]');
  root.querySelector('[data-copy-prompt]').addEventListener('click',async()=>{
   try{await navigator.clipboard.writeText(input.value);status.textContent='복사했습니다. 대괄호를 내 자료로 바꿔 붙여 넣으세요.'}
   catch{input.focus();input.select();status.textContent='문장을 선택했습니다. Ctrl+C 또는 ⌘C로 복사하세요.'}
  });
 });
 if($('model-search')){
  const rows=[...document.querySelectorAll('[data-model-row]')];
  const index=rows.map(row=>({row,text:row.textContent.normalize('NFKC').toLocaleLowerCase('ko-KR')}));
  const filter=()=>{
   const query=$('model-search').value.normalize('NFKC').trim().toLocaleLowerCase('ko-KR'),cat=$('model-category').value;
   let count=0;index.forEach(({row,text})=>{row.hidden=!(cat==='all'||row.dataset.category===cat)||!text.includes(query);if(!row.hidden)count++});
   document.querySelectorAll('[data-model-section]').forEach(section=>{section.hidden=![...section.querySelectorAll('[data-model-row]')].some(r=>!r.hidden)});
   $('model-count').textContent=`${rows.length}개 중 ${count}개 표시`;$('model-empty').hidden=count!==0;
  };
  $('model-search').addEventListener('input',filter);$('model-category').addEventListener('change',filter);
  $('model-reset').addEventListener('click',()=>{$('model-search').value='';$('model-category').value='all';filter();$('model-search').focus()});filter();
 }
 if($('cost-content')){
  const update=()=>{
   const content=$('cost-content').value,combo=$('cost-combo').value,attempts=Number($('cost-attempts').value);
   let value=0,formula='',cash='',note='',label='편당 사용분';
   if(combo==='free'){
    if(content==='video'){
     formula=`4클립 × ${attempts}회 × 12크레딧 = ${48*attempts}크레딧. Flow Omni 720p·8초 기준.`;
     note=`일 무료량 50크레딧${attempts>1?'을 넘습니다. 이월되지 않으므로 여러 날로 나눠도 접근·성공이 보장되지는 않습니다.':' 안에 들어갑니다. 무료 영상 접근과 한 번에 채택할 결과가 나오는 조건입니다.'} 막히면 직접 촬영 장면을 사용하세요.`;
    }else{formula='무료 채팅 + 본인 사진·도형 + 본인 녹음 + 무료 편집 = 0원.';note='유료 소재·음성은 제외합니다. 무료 AI 한도에 닿으면 확인한 문안을 직접 다듬으세요.'}
    cash='새 구독료 0원 · 기기·인터넷·작업 시간은 제외합니다.';
   }else{
    let usd=0,allocation=0;
    if(content==='cards'||content==='explain'){
     usd=(combo==='low'?0.0707:0.8975)*attempts;
     formula=combo==='low'?`(문안 $0.0007 + 이미지 5장 × $0.014) × ${attempts}회`:`(문안 $0.07 + 이미지 출력 5장 × $0.165 + 입력 $0.0025) × ${attempts}회`;
     if(content==='explain'){
      if(combo==='low'){usd+=0.0046*attempts;formula+=` + TTS $0.0046 × ${attempts}회`}
      else{allocation=82.5;formula+=' + 타입캐스트 9,900원 × 0.5분 ÷ 60분';label='편당 배분액'}
     }
    }else{
     usd=(combo==='low'?2.0567:12.87)*attempts;
     formula=combo==='low'?`(문안 $0.0007 + Runway Gen-4 Turbo 4클립 × 10초 × $0.05 + 시작 이미지 4장 × $0.014) × ${attempts}회`:`(문안 $0.07 + Runway Dev의 Veo 3.1 음성 4클립 × 8초 × $0.40) × ${attempts}회`;
    }
    value=usd*1350+allocation;formula+=` = $${new Intl.NumberFormat('en-US',{maximumFractionDigits:6}).format(usd)} × 1,350원${allocation?' + 82.5원':''} = 약 ${money(value)}원.`;
    cash=allocation?`타입캐스트 신규 월 구독 9,900원 + API 사용분 약 ${money(usd*1350)}원 = 약 ${money(9900+usd*1350)}원. API 최소 충전액·세금·수수료는 추가 확인하세요.`:'구독료는 포함하지 않았습니다. 실제 API 첫 결제는 최소 충전액·세금·수수료 때문에 위 사용분보다 클 수 있습니다.';
    note=content==='video'&&combo==='low'?'최종 32초지만 생성은 40초가 청구됩니다. 무음 모델이므로 본인 녹음을 넣습니다.':content==='explain'&&combo==='high'?'재시도는 문안·이미지만 반복하며, 확정한 음성은 다시 다운로드하지 않는 가정입니다. Basic은 개인 크리에이터용입니다.':'입력 토큰·장수·해상도가 바뀌면 비용도 바뀝니다. 높은 비용 설정은 품질 순위나 성공률을 뜻하지 않습니다.';
   }
   $('cost-result').dataset.value=String(value);
   $('cost-result').textContent=combo==='free'&&content==='video'?(attempts>1?`당일 무료량 초과 · ${48*attempts}크레딧`:'추가 지출 0원 · 무료 접근·채택 조건부'):`${label} 약 ${money(value)}원`;
   $('cost-formula').textContent=formula;$('cost-cash').textContent=cash;$('cost-note').textContent=note;
  };
  ['cost-content','cost-combo','cost-attempts'].forEach(id=>$(id).addEventListener('change',update));
  document.querySelector('[data-cost-reset]').addEventListener('click',()=>{$('cost-content').value='cards';$('cost-combo').value='low';$('cost-attempts').value='1';update()});update();
 }
})();
