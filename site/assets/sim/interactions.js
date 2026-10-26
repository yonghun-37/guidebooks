/* 원본 교육 도구. 이론·실습·실험실이 같은 상태 전이와 DOM 렌더링을 사용한다. */
(() => {
  'use strict';
  const one = (root, selector) => root.querySelector(selector);
  const all = (root, selector) => [...root.querySelectorAll(selector)];
  const put = (root, selector, text) => { one(root, selector).textContent = text; };
  const pressed = (root, selector, value) => all(root, selector).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.choice === value)));
  const numberField = (key, title, value, min = 0, max = 1000000, step = 1) => `<label>${title}<input data-value="${key}" type="number" min="${min}" max="${max}" step="${step}" value="${value}" required></label>`;
  const valid = inputs => inputs.map(input => {
    const ok = input.value.trim() !== '' && input.validity.valid;
    input.setAttribute('aria-invalid', String(!ok)); return ok;
  }).every(Boolean);
  const report = (root, value, sentence) => put(root, '[data-sim-result]', `${value} · ${sentence}`);
  const selectPreset = (root, preset) => all(root, '[data-preset]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.preset === preset)));
  const buttons = entries => entries.map(([key, title]) => `<button type="button" data-choice="${key}" aria-pressed="false">${title}</button>`).join('');
  const routeData = {
    sponsor: { title: '협찬', payer: '브랜드', action: '약속한 콘텐츠 제작', condition: '제작 범위·지급 조건 합의', anchor: 'sponsor', labels: ['제작비(원)', '완료 건수'], values: [200000, 1, 100, 30000, 0] },
    affiliate: { title: '제휴', payer: '제휴 판매처', action: '독자가 링크에서 구매', condition: '취소·제외를 뺀 인정 구매', anchor: 'affiliate-route', labels: ['상품 가격(원)', '인정 구매 건수'], values: [50000, 20, 3, 0, 0] },
    own: { title: '내 상품', payer: '구매자', action: '자료·서비스 전달', condition: '판매·환불 조건 확인', anchor: 'own-product', labels: ['판매 가격(원)', '판매 건수'], values: [5000, 10, 100, 10000, 0] },
    platform: { title: '플랫폼', payer: '플랫폼', action: '기능별 조건 확인', condition: '조회만으로 수입을 만들지 않음', anchor: 'meta-status', labels: ['확인한 수입(원)', '사용하지 않는 값'], values: [0, 1, 100, 0, 0] }
  };
  function revenue(root, body) {
    let route = 'affiliate';
    const memory = Object.fromEntries(Object.entries(routeData).map(([key, data]) => [key, { values: [...data.values], mode: 'bonus' }]));
    body.innerHTML = `<div class="tool-row" data-routes aria-label="돈의 경로">${buttons(Object.entries(routeData).map(([key, d]) => [key, d.title]))}</div><ol class="tool-flow" data-flow></ol><div data-route-fields></div><p data-formula class="decision-note"></p><div class="tool-row"><button type="button" data-reset>기본값</button><button type="button" data-zero>거래 없는 예</button><a data-condition href="#affiliate-route">이 경로의 조건 읽기</a></div>`;
    const draw = () => {
      const data = routeData[route], state = memory[route], v = state.values;
      pressed(body, '[data-routes] button', route);
      one(body, '[data-flow]').innerHTML = [ ['돈을 보내는 쪽', data.payer], ['독자·내가 하는 일', data.action], ['받는 조건', data.condition] ].map(([a,b]) => `<li><small>${a}</small>${b}</li>`).join('');
      const fields = one(body, '[data-route-fields]');
      fields.innerHTML = `${route === 'platform' ? '<label>연습할 기능<select data-mode><option value="bonus">초대·활성화 없는 보너스</option><option value="confirmed">내가 확인한 기능 수입</option></select></label>' : ''}<div class="tool-fields">${numberField('0', data.labels[0], v[0])}${route !== 'platform' ? numberField('1', data.labels[1], v[1], 0, 10000) : ''}</div><details><summary>요율·비용·환불 바꾸기</summary><div class="tool-fields">${route === 'affiliate' ? numberField('2', '가정 요율(%)', v[2], 0, 100, 0.1) : ''}${numberField('3', '비용(원)', v[3])}${numberField('4', '환불·공제(원)', v[4])}</div></details>`;
      if (route === 'platform') {
        one(fields, '[data-mode]').value = state.mode;
        one(fields, '[data-value="0"]').disabled = state.mode === 'bonus';
        one(fields, '[data-mode]').addEventListener('change', event => { state.mode = event.target.value; draw(); });
      }
      one(body, '[data-condition]').href = `#${data.anchor}`;
      all(fields, 'input').forEach(input => input.addEventListener('input', () => { v[Number(input.dataset.value)] = input.value; update(); }));
      update();
    };
    const update = () => {
      const state = memory[route], v = state.values.map(Number);
      if (!valid(all(body, 'input:not(:disabled)'))) { ReelsSim.moneyBars(root, null); report(root, '—', '빈칸·범위를 확인해 입력하세요.'); return; }
      const gross = route === 'platform' ? (state.mode === 'bonus' ? 0 : v[0]) : v[0] * v[1] * v[2] / 100;
      const net = Math.round(gross - v[3] - v[4]);
      ReelsSim.moneyBars(root, {income: gross, cost: v[3] + v[4], balance: net});
      const formula = route === 'platform' ? `${state.mode === 'bonus' ? '초대·활성화 없음 = 0' : v[0].toLocaleString('ko-KR')}` : `${v[0].toLocaleString('ko-KR')} × ${v[1]}${route === 'affiliate' ? ` × ${v[2]}%` : ''}`;
      put(body, '[data-formula]', `가상 계산: ${formula} − 비용 ${v[3]} − 환불·공제 ${v[4]}`);
      report(root, `${net.toLocaleString('ko-KR')}원`, route === 'platform' && state.mode === 'bonus' ? '초대·활성화가 없으면 조회만으로 보너스가 생기지 않습니다.' : `${routeData[route].title} 수입에서 입력한 비용·환불을 뺀 가상 금액이며 세금은 포함하지 않았습니다.`);
    };
    all(body, '[data-routes] button').forEach(b => b.addEventListener('click', () => { route = b.dataset.choice; draw(); }));
    one(body, '[data-reset]').addEventListener('click', () => { memory[route] = { values: [...routeData[route].values], mode: 'bonus' }; draw(); });
    one(body, '[data-zero]').addEventListener('click', () => { memory[route].values[route === 'platform' ? 0 : 1] = 0; draw(); });
    draw();
  }

  const cardDefault = { title: '청년 지원금, 신청 전 3가지', body: '대상·기간·서류를 확인하세요.\n자동 지급은 아니에요.', source: '예시 문안 · 지원 신청 체크', size: 44, padding: 90, palette: 'cream' };
  function cards(root, body) {
    let before = {...cardDefault}, comparing = false, small = false;
    body.innerHTML = `<div class="card-editor"><div><label>제목<input data-title maxlength="100"></label><label>본문<textarea data-copy rows="4" maxlength="1600"></textarea></label></div><div><div data-after class="card-stage" aria-label="수정 후 카드 미리보기"><div class="card-sheet"><div class="card-copy card-head"></div><div class="card-copy card-text"></div><div class="card-copy card-source"></div></div></div><p data-clip class="clip-label"></p></div></div><div class="tool-row"><button type="button" data-preset="overflow" aria-pressed="false">넘치는 예</button><button type="button" data-preset="default" aria-pressed="true">기본값</button><button type="button" data-small aria-pressed="false">작게 보기</button></div><details><summary>크기·여백·출처·수정 전후</summary><div class="tool-fields">${numberField('size', '원본 글자 크기(px)', 44, 24, 90)}${numberField('padding', '원본 여백(px)', 90, 30, 180)}</div><label>글자 크기 슬라이더<input data-size-range type="range" min="24" max="90" value="44" aria-label="원본 글자 크기 슬라이더"></label><label>출처<input data-source maxlength="240"></label><label>색 조합<select data-palette><option value="cream">밝은 바탕·짙은 글자</option><option value="navy">짙은 바탕·밝은 글자</option></select></label><div class="tool-row"><button type="button" data-freeze>현재 모습을 수정 전으로 고정</button><button type="button" data-compare aria-pressed="false">수정 전후 보기</button></div><div data-before-panel hidden><p>고정한 수정 전 · 같은 문안을 고쳐 비교하세요.</p><div data-before class="card-stage"><div class="card-sheet"><div class="card-copy card-head"></div><div class="card-copy card-text"></div><div class="card-copy card-source"></div></div></div></div></details>`;
    const fields = { title: one(body,'[data-title]'), body: one(body,'[data-copy]'), source: one(body,'[data-source]'), size: one(body,'[data-value="size"]'), padding: one(body,'[data-value="padding"]'), palette: one(body,'[data-palette]') };
    const state = () => Object.fromEntries(Object.entries(fields).map(([key,input]) => [key,input.value]));
    const paint = (stage, data) => {
      const sheet = one(stage, '.card-sheet');
      sheet.style.transform = `scale(${stage.clientWidth / 240})`;
      sheet.style.padding = `${Number(data.padding)/4.5}px`;
      sheet.style.fontSize = `${Number(data.size)/4.5}px`;
      sheet.style.background = data.palette === 'navy' ? '#172b35' : '#fff8e9';
      sheet.style.color = data.palette === 'navy' ? '#fff8e9' : '#172b35';
      for (const [selector,key] of [['.card-head','title'],['.card-text','body'],['.card-source','source']]) put(sheet, selector, data[key]);
      one(sheet,'.card-head').style.fontSize = `${Number(data.size)*1.2/4.5}px`;
      one(sheet,'.card-source').style.fontSize = `${Math.max(24, Number(data.size)*0.65)/4.5}px`;
      return all(sheet,'.card-copy').reduce((sum, element) => {
        const lines = Math.max(0, Math.ceil((element.scrollHeight-element.clientHeight-1) / parseFloat(getComputedStyle(element).lineHeight)));
        element.classList.toggle('is-clipped',lines>0);
        return sum+lines;
      },0);
    };
    const update = () => {
      if (!valid([fields.size, fields.padding])) { report(root,'—','글자 크기와 여백의 입력 범위를 확인하세요.'); return; }
      const data = state(), clipped = paint(one(body,'[data-after]'),data);
      if(comparing) paint(one(body,'[data-before]'),before);
      put(body,'[data-clip]',clipped ? '잘림 있음 · 입력란에서 전체 문장을 읽으세요.' : '제목·본문·출처 표시');
      one(body,'[data-size-range]').value = data.size;
      report(root, `${clipped}줄 넘침`, clipped ? '잘린 곳의 문장을 줄이거나 글자 크기·여백을 조정하세요.' : !data.title.trim() || !data.body.trim() || !data.source.trim() ? '비어 있는 제목·본문·출처를 채우고 다시 읽어 보세요.' : '휴대폰 크기에서 제목부터 출처까지 직접 읽어 보세요.');
    };
    const load = data => { Object.entries(fields).forEach(([key,input]) => { input.value = data[key]; }); update(); };
    Object.values(fields).forEach(input => input.addEventListener('input', () => { selectPreset(body,''); update(); }));
    one(body,'[data-size-range]').addEventListener('input', event => { fields.size.value = event.target.value; selectPreset(body,''); update(); });
    all(body,'[data-preset]').forEach(b => b.addEventListener('click', () => { const data={...cardDefault}; if(b.dataset.preset==='overflow') data.body = '신청 전에는 대상과 기간을 확인하고, 제출 서류와 제외 조건을 공고에서 찾아보세요.\n'.repeat(10); before = {...data}; load(data); selectPreset(body,b.dataset.preset); }));
    one(body,'[data-freeze]').addEventListener('click', () => { if(valid([fields.size,fields.padding])) { before=state(); update(); report(root,'1개 고정','현재 카드가 수정 전으로 고정되었으니 문안을 고쳐 비교하세요.'); } });
    one(body,'[data-compare]').addEventListener('click',event => { comparing=!comparing; event.currentTarget.setAttribute('aria-pressed',String(comparing)); one(body,'[data-before-panel]').hidden=!comparing; update(); });
    one(body,'[data-small]').addEventListener('click',event => { small=!small; event.currentTarget.setAttribute('aria-pressed',String(small)); all(body,'.card-stage').forEach(stage=>stage.classList.toggle('is-small',small)); update(); });
    new ResizeObserver(update).observe(one(body,'[data-after]'));
    document.fonts?.ready.then(update);
    load(cardDefault);
  }

  const reelDefault = () => ['청년 지원금, 신청 전 3가지', '신청 대상을 확인하세요.', '신청 기간도 살펴보세요.', '제출 서류를 챙기세요.', '자동 지급 아님을 확인하세요.'].map((text,i)=>({text,start:i*4,end:(i+1)*4}));
  function reels(root, body) {
    const total = 20, fps = 24;
    let captions = reelDefault(), boundaries = [0,4,8,12,16,20], selected = 0, t = 0, playing = false, looping = false, raf = 0, previous = 0, lastPaint = 0;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    body.innerHTML = `<div class="reel-preview"><div class="reel-screen" aria-label="무음 영상 미리보기"><strong data-scene-name></strong><p data-subtitle></p><small>무음 연습</small></div><div><p><output data-clock aria-live="off"></output></p><p data-play-state role="status" aria-live="polite" aria-atomic="true">정지 상태입니다.</p><div class="tool-row"><button type="button" data-play aria-pressed="false">재생</button><button type="button" data-stop>처음</button><button type="button" data-loop aria-pressed="false" aria-label="선택 자막 구간 반복">반복</button></div></div></div><div class="timeline" aria-label="가상 20초 시간표"><div class="track" data-scenes><span class="track-label">장면</span></div><div class="track" data-captions><span class="track-label">자막</span></div><div class="track"><span class="track-label">음성</span><span class="voice-clip">무음 · 녹음 파일 없음</span></div><div class="playhead" aria-hidden="true"></div></div><label>재생 위치<input data-seek type="range" min="0" max="480" step="1" value="0" aria-label="재생 위치(프레임)"></label><div class="tool-row"><button type="button" data-frame="-1">이전 프레임</button><button type="button" data-frame="1">다음 프레임</button></div><label>선택 자막<textarea data-caption rows="2" maxlength="400"></textarea></label><details><summary>시간 숫자·장면 길이 편집</summary><div class="tool-fields">${numberField('start','자막 시작(초)',0,0,20,0.1)}${numberField('end','자막 끝(초)',4,0,20,0.1)}</div><div class="tool-row"><button type="button" data-apply>자막 시간 적용</button><button type="button" data-shift="-0.1">자막 −0.1초</button><button type="button" data-shift="0.1">자막 +0.1초</button></div><div class="tool-fields">${numberField('scene-end','선택 장면 끝(초)',4,0,20,0.1)}${numberField('position','재생 위치(초)',0,0,20,0.001)}</div><div class="tool-row"><button type="button" data-scene-apply>장면 시간 적용</button><button type="button" data-position-apply>위치로 이동</button></div></details><div class="tool-row"><button type="button" data-preset="fast" aria-pressed="false">빠른 자막 예</button><button type="button" data-repair>문장만 짧게 복구</button><button type="button" data-preset="default" aria-pressed="true">기본값</button></div>`;
    // 모든 사용자 문자열은 textContent/value로 넣는다.
    one(body,'.reel-screen').setAttribute('aria-label','무음 영상 미리보기');
    const announce = text => put(body,'[data-play-state]',text);
    const timeFields = [one(body,'[data-value="start"]'),one(body,'[data-value="end"]')];
    const renderClock = () => {
      const scene = t >= total ? 4 : boundaries.findIndex((start,i)=>i<5 && start<=t && t<boundaries[i+1]);
      const caption = captions.find(c=>c.start<=t && t<c.end);
      put(body,'[data-scene-name]',`장면 ${scene+1}`);
      put(body,'[data-subtitle]',caption?.text || '표시 중인 자막 없음');
      put(body,'[data-clock]',`${t.toFixed(2)} / ${total.toFixed(2)}초`);
      one(body,'.playhead').style.left = `${t/total*100}%`;
      one(body,'[data-seek]').value = Math.round(t*fps);
      one(body,'[data-seek]').setAttribute('aria-valuetext',`${t.toFixed(2)}초, 장면 ${scene+1}`);
      one(body,'[data-value="position"]').value = t.toFixed(3);
      all(body,'[data-scenes] button').forEach((b,i)=>b.setAttribute('aria-current',i===scene?'true':'false'));
    };
    const result = () => {
      const c=captions[selected], duration=c.end-c.start;
      const gap = (selected===0 ? c.start>0 : c.start>captions[selected-1].end) || (selected===4 ? c.end<total : c.end<captions[selected+1].start);
      report(root, `${duration.toFixed(1)}초`, `${gap?'자막 사이에 빈 구간이 있으니 ':''}선택 문장을 직접 읽고 짧으면 문장을 줄이거나 시간을 늘리세요.`);
    };
    const pause = (message='현재 프레임에 정지했습니다.') => { playing=false; cancelAnimationFrame(raf); one(body,'[data-play]').setAttribute('aria-pressed','false'); put(body,'[data-play]','재생'); announce(message); };
    const seek = (value,message) => { pause(message); t=Math.min(total,Math.max(0,Math.round(value*fps)/fps)); renderClock(); announce(`${t.toFixed(2)}초에 정지했습니다.`); };
    const editSelection = () => {
      one(body,'[data-caption]').value=captions[selected].text;
      timeFields[0].value=captions[selected].start.toFixed(1); timeFields[1].value=captions[selected].end.toFixed(1);
      one(body,'[data-value="scene-end"]').value=boundaries[selected+1];
      one(body,'[data-value="scene-end"]').disabled=selected===4;
      all(body,'[data-captions] button, [data-scenes] button').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.index)===selected)));
      timeFields.forEach(input=>input.setAttribute('aria-invalid','false'));
      result();
    };
    const tracks = () => {
      for (const [selector,segments] of [['[data-scenes]',boundaries.slice(0,5).map((start,i)=>({start,end:boundaries[i+1]}))],['[data-captions]',captions]]) {
        const track=one(body,selector); all(track,'button').forEach(b=>b.remove());
        segments.forEach((clip,i)=>{
          const b=document.createElement('button'); b.type='button'; b.className='clip'; b.textContent=String(i+1); b.dataset.index=i;
          b.style.left=`${clip.start/total*100}%`; b.style.width=`${(clip.end-clip.start)/total*100}%`;
          b.setAttribute('aria-label',`${selector.includes('scenes')?'장면':'자막'} ${i+1}, ${clip.start.toFixed(1)}초부터 ${clip.end.toFixed(1)}초${selector.includes('captions')?`, ${captions[i].text}`:''}`);
          b.addEventListener('click',()=>{ selected=i; seek(clip.start); editSelection(); announce(`${i+1}번째 구간을 선택해 시작에 정지했습니다.`); }); track.append(b);
        });
      }
      editSelection(); renderClock();
    };
    const tick = stamp => {
      if(!playing) return;
      t+=(stamp-previous)/1000; previous=stamp;
      const c=captions[selected];
      if(looping && t>=c.end) t=c.start+(t-c.start)%(c.end-c.start);
      if(t>=total){t=total; pause('끝까지 재생해 정지했습니다.');}
      if(!reduced.matches || stamp-lastPaint>=250 || !playing){renderClock();lastPaint=stamp;}
      if(playing) raf=requestAnimationFrame(tick);
    };
    one(body,'[data-play]').addEventListener('click',()=>{
      if(playing){pause();return;}
      const c=captions[selected]; if(looping && (t<c.start || t>=c.end)) t=c.start; else if(t>=total)t=0;
      playing=true; previous=performance.now(); lastPaint=0; one(body,'[data-play]').setAttribute('aria-pressed','true'); put(body,'[data-play]','프레임 정지'); announce(looping?'선택 자막 구간을 반복 재생합니다.':'무음으로 재생합니다.'); raf=requestAnimationFrame(tick);
    });
    one(body,'[data-stop]').addEventListener('click',()=>seek(0));
    one(body,'[data-seek]').addEventListener('input',event=>seek(Number(event.target.value)/fps));
    one(body,'[data-loop]').addEventListener('click',event=>{looping=!looping;event.currentTarget.setAttribute('aria-pressed',String(looping)); if(looping){t=captions[selected].start;renderClock();} announce(looping?'선택 자막 구간 반복을 켰습니다.':'구간 반복을 껐습니다.');});
    all(body,'[data-frame]').forEach(b=>b.addEventListener('click',()=>seek(t+Number(b.dataset.frame)/fps)));
    one(body,'[data-caption]').addEventListener('input',event=>{captions[selected].text=event.target.value; selectPreset(body,''); renderClock();result(); const b=one(body,`[data-captions] [data-index="${selected}"]`); b.setAttribute('aria-label',`자막 ${selected+1}, ${event.target.value}`);});
    const applyTimes = (start,end) => {
      pause();
      const overlap=captions.some((c,i)=>i!==selected && start<c.end && end>c.start);
      if(!valid(timeFields) || end<=start || overlap){ timeFields.forEach(input=>input.setAttribute('aria-invalid','true')); report(root,'—','시작은 끝보다 앞서고 다른 자막과 겹치지 않아야 합니다.'); return; }
      captions[selected].start=start;captions[selected].end=end;t=start;selectPreset(body,'');tracks();announce('자막 시간을 적용해 시작에 정지했습니다.');
    };
    one(body,'[data-apply]').addEventListener('click',()=>applyTimes(Number(timeFields[0].value),Number(timeFields[1].value)));
    all(body,'[data-shift]').forEach(b=>b.addEventListener('click',()=>{const c=captions[selected],delta=Number(b.dataset.shift);timeFields[0].value=(c.start+delta).toFixed(1);timeFields[1].value=(c.end+delta).toFixed(1);applyTimes(Number(timeFields[0].value),Number(timeFields[1].value));}));
    one(body,'[data-scene-apply]').addEventListener('click',()=>{const input=one(body,'[data-value="scene-end"]'),end=Number(input.value);pause();if(selected===4 || !valid([input]) || end<=boundaries[selected] || end>=boundaries[selected+2]){input.setAttribute('aria-invalid','true');report(root,'—','장면 끝은 양옆 장면의 바깥 경계 사이에 입력하세요.');return;}boundaries[selected+1]=end;tracks();announce('장면 경계만 바꿨습니다. 자막 시간은 따로 확인하세요.');});
    one(body,'[data-position-apply]').addEventListener('click',()=>{const input=one(body,'[data-value="position"]');if(valid([input]))seek(Number(input.value));else report(root,'—','영상 안의 재생 위치를 입력하세요.');});
    all(body,'[data-preset]').forEach(b=>b.addEventListener('click',()=>{pause();captions=reelDefault();boundaries=[0,4,8,12,16,20];selected=0;t=0;looping=false;one(body,'[data-loop]').setAttribute('aria-pressed','false');if(b.dataset.preset==='fast'){captions[0].text='청년 지원금을 신청하려면 대상과 신청 기간, 제출 서류와 제외 조건, 심사 절차까지 공고에서 모두 확인해야 합니다.';captions[0].end=1;}selectPreset(body,b.dataset.preset);tracks();announce('가상 예제로 돌아와 첫 장면에 정지했습니다.');}));
    one(body,'[data-repair]').addEventListener('click',()=>{pause();captions[selected].text='신청 대상을 확인하세요.';t=captions[selected].start;selectPreset(body,'');tracks();announce('같은 장면과 시간을 두고 문장만 줄였습니다. 다시 재생하세요.');});
    document.addEventListener('visibilitychange',()=>{if(document.hidden && playing)pause('탭을 떠나 재생을 멈췄습니다. 돌아와 재생을 눌러 주세요.');});
    window.addEventListener('pagehide',()=>pause());
    tracks();
  }

  function publishing(root, body) {
    let step=0, scenario='normal', resolved=false, timer=0, automatic=false;
    const names=['파일 준비','공개 주소','생성 요청','처리 확인','게시 요청','결과 확인'];
    const normal=[['승인한 파일 준비','검수한 파일과 현재 승인을 확인합니다.'],['공개 주소 접근 가능','외부에서 읽을 수 있는 미디어 주소를 확인합니다.'],['생성 요청 성공 · 가상 ID 수신','요청이 받아들여졌으며 아직 게시되지 않았습니다.'],['처리 완료 · FINISHED','준비 상자가 완료됐으니 게시 요청으로 진행합니다.'],['게시 요청 응답 수신 · 가상 게시물 ID','실제 게시물과 주소를 확인해야 완료입니다.'],['게시물·주소 확인 완료','가상 결과를 확인했으며 실제 계정에는 게시하지 않았습니다.']];
    body.innerHTML=`<label>가상 상황<select data-scenario><option value="normal">정상 진행</option><option value="url">주소 접근 불가</option><option value="delay">처리 지연</option><option value="unknown">게시 응답 끊김</option></select></label><ol class="tool-flow step-flow">${names.map(name=>`<li>${name}</li>`).join('')}</ol><div class="state-panel"><strong data-state></strong><p data-action></p></div><div class="tool-row"><button type="button" data-prev>이전</button><button type="button" data-next>다음</button><button type="button" data-auto aria-pressed="false">자동 진행</button><button type="button" data-reset>처음으로</button></div><div class="tool-row" data-recovery hidden><button type="button" data-resolve></button><button type="button" data-retry>바로 다시 게시</button></div><details><summary>가상 요청·응답 기록</summary><ol class="tool-log" data-log></ol><p>이전 버튼은 가상 화면을 되돌립니다. 실제 요청을 취소하지 않습니다.</p></details>`;
    const blocked = () => !resolved && ((scenario==='url' && step===1)||(scenario==='delay' && step===3)||(scenario==='unknown' && step===4));
    const status = (index, history=false) => {
      if((!resolved || history) && scenario==='url' && index===1)return ['주소 접근 실패','공개 범위와 주소를 고친 뒤 다시 확인합니다.'];
      if((!resolved || history) && scenario==='delay' && index===3)return ['처리 중 · IN_PROGRESS','게시 요청을 멈추고 준비 상자의 처리 상태를 다시 확인합니다.'];
      if((!resolved || history) && scenario==='unknown' && index===4)return ['게시 응답 끊김 · 완료 여부 모름','게시됐을 수 있으니 프로필과 원격 상태부터 확인합니다.'];
      return normal[index];
    };
    const halt=()=>{clearTimeout(timer);automatic=false;one(body,'[data-auto]').setAttribute('aria-pressed','false');put(body,'[data-auto]','자동 진행');};
    const draw=()=>{
      const [state,action]=status(step), failed=blocked();
      all(body,'.step-flow li').forEach((li,i)=>{if(i===step)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current');});
      put(body,'[data-state]',state);put(body,'[data-action]',action);
      one(body,'[data-prev]').disabled=step===0;one(body,'[data-next]').disabled=step===5 || failed;
      one(body,'[data-recovery]').hidden=!failed;
      put(body,'[data-resolve]',scenario==='url'?'공개 주소 고쳐서 확인':scenario==='delay'?'처리 상태 다시 확인':'프로필·원격 상태 확인');
      one(body,'[data-retry]').hidden=scenario!=='unknown';
      const log=one(body,'[data-log]');log.replaceChildren();
      for(let i=0;i<=step;i++){const li=document.createElement('li');li.textContent=`${names[i]} — ${status(i,true).join(' · ')}`;log.append(li);}
      if(resolved){const li=document.createElement('li');li.textContent=scenario==='unknown'?'원격 확인 — 가상 게시물을 찾았습니다. 중복 요청을 보내지 않았습니다.':scenario==='delay'?'상태 재확인 — 가상 처리 완료를 확인했습니다.':'주소 수정 — 가상 접근 가능을 확인했습니다.';log.append(li);}
      report(root,step===5?'1건 확인':'0건 확인',step===5?'가상 게시물의 주소까지 확인했으니 실제 게시에서는 내 프로필도 확인하세요.':action);
      if(failed || step===5)halt();
    };
    const advance=()=>{if(step<5 && !blocked())step++;draw();};
    const autoTick=()=>{if(!automatic)return;advance();if(automatic)timer=setTimeout(autoTick,1800);};
    one(body,'[data-scenario]').addEventListener('change',event=>{halt();scenario=event.target.value;step=0;resolved=false;draw();});
    one(body,'[data-next]').addEventListener('click',()=>{halt();advance();});
    one(body,'[data-prev]').addEventListener('click',()=>{halt();step=Math.max(0,step-1);draw();});
    one(body,'[data-reset]').addEventListener('click',()=>{halt();step=0;resolved=false;draw();});
    one(body,'[data-auto]').addEventListener('click',()=>{if(automatic){halt();return;}if(blocked()||step===5){draw();return;}automatic=true;one(body,'[data-auto]').setAttribute('aria-pressed','true');put(body,'[data-auto]','자동 정지');timer=setTimeout(autoTick,1800);});
    one(body,'[data-resolve]').addEventListener('click',()=>{resolved=true;if(scenario==='unknown')step=5;draw();});
    one(body,'[data-retry]').addEventListener('click',()=>report(root,'0건 재시도','중복 게시를 막으려면 프로필과 원격 상태를 먼저 확인하세요.'));
    document.addEventListener('visibilitychange',()=>{if(document.hidden)halt();});window.addEventListener('pagehide',halt);
    draw();
  }

  const cases = {
    mixed: { title:'신청 체크·사진·제휴 링크 카드', description:'신청 체크 카드에 기사 사진, “누구나 자동 지급” 문구와 제휴 링크가 있습니다.', issues:['rights','facts','labels'], clues:{rights:'기사 사진의 이용 허락 자료가 없습니다. 출처 링크만 있습니다.',facts:'예시 원문은 “대상·기간·서류 확인, 자동 지급 아님”입니다. 카드에는 조건이 빠졌습니다.',ad:'가상 제휴 관계가 있지만 관계 문구와 표시가 빠졌습니다.',ai:'글쓰기 보조만 썼고 사실적인 사람·음성 합성은 없습니다.',security:'가상 작업 파일에 토큰·개인정보가 없습니다.'} },
    voice: { title:'AI 진행자·신청 관리 앱 릴스', description:'가상 진행자가 제공받은 신청 관리 앱을 써 봤다고 말하고 작업 화면이 보입니다.',issues:['facts','labels','security'],clues:{rights:'가상 계약 메모에 이미지·음성의 광고 게시 이용 허락이 있습니다.',facts:'가상 진행자는 앱을 사용하지 않았습니다. 체험담의 근거가 없습니다.',ad:'가상 앱 업체에서 이용권을 제공했지만 관계 문구가 빠졌습니다.',ai:'사실적인 AI 합성 진행자·음성이지만 AI 표시가 없습니다.',security:'가상 화면에 비밀 키 자리 표시자가 노출됐습니다. 실제 값은 없습니다.'} }
  };
  function safety(root, body) {
    let caseId='mixed', seen=new Set(), fixed=new Set(), decisions={}, prediction='evidence';
    const groups={rights:'권리',facts:'사실',labels:'표시',security:'보안'};
    const needed={rights:['rights'],facts:['facts'],labels:['ad','ai'],security:['security']};
    body.innerHTML=`<label>가상 사례<select data-case>${Object.entries(cases).map(([id,c])=>`<option value="${id}">${c.title}</option>`).join('')}</select></label><p data-case-description></p><details><summary>내 예상 고르기</summary><div class="tool-row" data-prediction>${buttons([['publish','지금 게시'],['fix','고쳐서 게시'],['evidence','근거부터 확인']])}</div></details><p>먼저 증거를 열고, 아래에서 판단하세요.</p><div class="tool-row" data-evidence>${buttons([['facts','원출처'],['rights','이미지·음성 허락'],['ad','광고 관계'],['ai','AI 사용'],['security','보안']])}</div><p class="state-panel" data-clue role="status" aria-live="polite" aria-atomic="true">아직 증거를 열지 않았습니다.</p><div data-decisions>${Object.entries(groups).map(([key,title])=>`<label class="decision-row">${title}<select data-decision="${key}" aria-label="${title} 판단" disabled><option value="hold">보류 · 증거 먼저</option><option value="fix">수정 필요</option><option value="clear">근거 확인 완료</option></select></label>`).join('')}</div><details><summary>문제 고치기·확인한 증거 다시 보기</summary><div class="tool-row" data-fixes>${Object.entries({rights:'소재 교체',facts:'원문대로 수정',labels:'표시 보완',security:'비밀값 제거'}).map(([key,label])=>`<button type="button" data-fix="${key}" disabled>${label}</button>`).join('')}</div><ul class="evidence-log" data-evidence-log></ul><p data-changes class="decision-note"></p></details>`;
    const available=key=>needed[key].every(id=>seen.has(id));
    const update=(message='')=>{
      const c=cases[caseId];
      Object.keys(groups).forEach(key=>{one(body,`[data-decision="${key}"]`).disabled=!available(key);one(body,`[data-fix="${key}"]`).disabled=!available(key);});
      all(body,'[data-evidence] button').forEach(b=>b.setAttribute('aria-pressed',String(seen.has(b.dataset.choice))));
      pressed(body,'[data-prediction] button',prediction);
      const remaining=Object.keys(groups).filter(key=>decisions[key]!=='clear');
      report(root,`${remaining.length}개 남음`,message || (remaining.length?`${remaining.map(key=>groups[key]).join('·')}의 증거와 수정 내용을 확인하세요.`:'가상 사례의 판단을 마쳤으니 실습에서 내 자료의 근거를 따로 확인하세요.'));
      const log=one(body,'[data-evidence-log]');log.replaceChildren();
      seen.forEach(id=>{const li=document.createElement('li');li.textContent=c.clues[id];log.append(li);});
      const changes={rights:'허락 자료가 없는 사진을 직접 그린 도식으로 교체했습니다.',facts:caseId==='mixed'?'원문대로 “대상·기간·서류 확인, 자동 지급 아님”으로 고쳤습니다.':'실제로 쓰지 않은 앱의 체험담을 지웠습니다.',labels:caseId==='mixed'?'제휴 수수료 관계 문구를 첫 화면에 넣고 필요한 표시를 확인했습니다.':'앱 이용권 제공 관계·가상 진행자 설명을 넣고 협찬·AI 표시를 확인했습니다.',security:'작업 화면의 비밀 키 자리 표시자를 지웠습니다.'};
      put(body,'[data-changes]',fixed.size?[...fixed].map(key=>changes[key]).join(' '):'수정한 항목이 없습니다.');
    };
    const reset=()=>{seen=new Set();fixed=new Set();decisions={};prediction='evidence';all(body,'[data-decision]').forEach(select=>select.value='hold');put(body,'[data-case-description]',cases[caseId].description);put(body,'[data-clue]','아직 증거를 열지 않았습니다.');update();};
    all(body,'[data-evidence] button').forEach(b=>b.addEventListener('click',()=>{const clue=b.dataset.choice;seen.add(clue);put(body,'[data-clue]',cases[caseId].clues[clue]);update(`${b.textContent} 증거를 열었으니 단서를 읽고 해당 항목을 판단하세요.`);}));
    all(body,'[data-prediction] button').forEach(b=>b.addEventListener('click',()=>{prediction=b.dataset.choice;update('예상을 기록했으니 증거를 열어 판단을 확인하세요.');}));
    all(body,'[data-decision]').forEach(select=>select.addEventListener('change',()=>{
      const key=select.dataset.decision, problematic=cases[caseId].issues.includes(key);
      if(select.value==='clear' && problematic && !fixed.has(key)){select.value=decisions[key]||'hold';update(`${groups[key]}의 문제가 남아 있으니 증거를 다시 보고 먼저 고치세요.`);return;}
      decisions[key]=select.value;update();
    }));
    all(body,'[data-fix]').forEach(b=>b.addEventListener('click',()=>{const key=b.dataset.fix;fixed.add(key);decisions[key]='fix';one(body,`[data-decision="${key}"]`).value='fix';update(`${groups[key]}의 가상 수정을 반영했으니 근거 확인 완료를 선택하세요.`);}));
    one(body,'[data-case]').addEventListener('change',event=>{caseId=event.target.value;reset();});
    reset();
  }

  const mount = { revenue, cards, reels, publishing, safety };
  all(document,'[data-interaction]').forEach(root=>{
    const body=one(root,'[data-tool-body]');
    root.setAttribute('role','region');
    const status=one(root,'[data-sim-result]');status.setAttribute('aria-live','polite');status.setAttribute('aria-atomic','true');
    mount[root.dataset.interaction](root,body);
    if (['cards','reels'].includes(root.dataset.interaction)) body.insertBefore(status, one(body,'details'));
    if (root.dataset.interaction === 'safety') {
      body.insertBefore(status, one(body,'[data-decisions]'));
      body.append(one(body,'details'));
    }
    const preset = new URLSearchParams(location.search).get('toolPreset');
    if (root.dataset.interaction === 'cards' || root.dataset.interaction === 'reels') one(body, `[data-preset="${preset === 'overflow' ? 'overflow' : preset === 'fast' ? 'fast' : 'default'}"]`)?.click();
    if (root.dataset.interaction === 'revenue' && ['platform','affiliate'].includes(preset)) one(body, `[data-choice="${preset}"]`).click();
    if (root.dataset.interaction === 'publishing' && preset === 'unknown') {
      one(body,'[data-scenario]').value='unknown';
      one(body,'[data-scenario]').dispatchEvent(new Event('change'));
    }
  });
})();
