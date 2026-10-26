/* 이론 11~15장의 가상 제작 연습. 네트워크·계정 조작·저장은 하지 않는다. */
(() => {
  'use strict';
  const page = document.querySelector('.operations-chapter');
  if (!page) return;
  const $ = (root, selector) => root.querySelector(selector);
  const report = (root, number, message) => {
    const output = $(root, '[data-ops-result]');
    const strong = document.createElement('strong'); strong.textContent = number;
    output.replaceChildren(strong, document.createTextNode(message));
  };
  const listen = (root, render) => { root.addEventListener('input', render); root.addEventListener('change', render); };

  const pipeline = $(page, '#pipeline-tool');
  if (pipeline) {
    const steps = ['대본', '녹음', '자막', '편집', '검수', '출력'];
    const expected = ['이번 편 대본', '녹음 원본과 연결 경로', '자막 파일과 녹음', '장면 원본과 시간축', '소리·자막·화면·권리 대조', '검수한 완성 파일'];
    const failure = $(pipeline, '#pipe-failure');
    const next = $(pipeline, '[data-pipe-next]');
    let index = 0, stopped = false;
    const failures = {voice: 1, captions: 2, clip: 3, sync: 4, all: 1};
    const fixes = {
      voice: '녹음 파일이 없습니다. 파일명·이동한 폴더를 확인하고 다시 연결하세요.',
      captions: '자막 파일이 없습니다. 저장한 자막을 불러오거나 녹음에 맞춰 다시 만드세요.',
      clip: '장면 원본이 없습니다. 원본 위치를 찾아 다시 연결하고 빈 화면을 확인하세요.',
      sync: '말은 “비상금”, 자막은 “비상근”입니다. 자막 내용을 고친 뒤 해당 구간을 다시 재생하세요.',
      all: '녹음·자막·장면 파일이 모두 없습니다. 우선 녹음부터 복구하고 이후 단계도 다시 점검하세요.'
    };
    const render = () => {
      const list = $(pipeline, '[data-pipe-steps]');
      list.replaceChildren(...steps.map((name, i) => {
        const li = document.createElement('li'), label = document.createElement('strong'), state = document.createElement('span');
        const status = stopped && i === index ? '실패 · 여기부터 수정' : i < index ? '확인됨' : i === index ? '다음 확인' : '대기';
        label.textContent = `${i + 1}. ${name}`; state.textContent = status; li.append(label, state);
        if (i === index) li.setAttribute('aria-current', 'step');
        if (stopped && i === index) li.dataset.state = 'failed';
        return li;
      }));
      next.disabled = stopped || index === steps.length;
      if (stopped) {
        $(pipeline, '[data-pipe-evidence]').textContent = `기대한 입력: ${expected[index]} / 발견: ${fixes[failure.value]}`;
        report(pipeline, `${index + 1}단계에서 멈춤`, '처음 빠진 입력을 고친 뒤 처음부터 다시 확인하세요.');
      } else if (index === steps.length) {
        $(pipeline, '[data-pipe-evidence]').textContent = '가상 흐름 점검이 끝났습니다. 내 영상은 실제 출력본을 직접 재생해야 합니다.';
        report(pipeline, `${steps.length}단계 확인`, '파일 연결 다음에는 완성본의 소리·자막·화면을 직접 대조하세요.');
      } else {
        $(pipeline, '[data-pipe-evidence]').textContent = `다음에 기대하는 입력: ${expected[index]}`;
        report(pipeline, `${index}단계 확인`, '다음 단계 확인을 눌러 진행하세요.');
      }
    };
    const reset = () => { index = 0; stopped = false; render(); };
    failure.addEventListener('change', reset);
    $(pipeline, '[data-pipe-reset]').addEventListener('click', reset);
    next.addEventListener('click', () => {
      if (stopped || index >= steps.length) return;
      if (index === failures[failure.value]) stopped = true; else index++;
      render();
    });
    render();
  }

  const metadata = $(page, '#metadata-tool');
  if (metadata) {
    const upload = document.querySelector('#upload-tool');
    const title = $(metadata, '#meta-title'), description = $(metadata, '#meta-description'), credit = $(metadata, '#meta-credit');
    const visibility = $(metadata, '#meta-visibility'), zone = $(metadata, '#meta-zone');
    const audience = $(upload, '#audience'), ai = $(upload, '#ai-content'), music = $(upload, '#music-rights');
    const render = () => {
      zone.disabled = visibility.value !== 'schedule';
      const pending = [];
      if (title.value !== 'honest') pending.push('제목이 실제 돈의 용도 네 칸 설명과 맞는지 확인');
      if (!description.value.trim()) pending.push('설명에 영상 요약과 필요한 표시 작성');
      if (!credit.checked) pending.push('소재·음악의 필수 표시 대조');
      if (!visibility.value) pending.push('공개 범위 결정');
      if (visibility.value === 'schedule' && !zone.value.trim()) pending.push('예약 날짜·시간·시간대 메모');
      if (!audience.value || audience.value === 'unsure') pending.push('아동용 판단');
      if (!ai.value || ai.value === 'unsure' || (['cartoon', 'tts'].includes(ai.value) && !['own', 'clone', 'realistic'].includes($(upload, '#ai-voice').value))) pending.push('AI 공개 판단');
      if (!music.value || music.value === 'unknown') pending.push('음악 권리 확인');
      report(metadata, `${pending.length}개 확인 필요`, pending.length ? pending.join(' / ') : '메모가 채워졌습니다. 실제 영상·설정·사용권을 대조한 뒤 공개를 결정하세요.');
    };
    listen(metadata, render); upload.addEventListener('change', render);
    upload.querySelector('form').addEventListener('reset', () => setTimeout(render, 0));
    metadata.querySelectorAll('[data-meta-preset]').forEach(button => button.addEventListener('click', () => {
      const base = button.dataset.metaPreset === 'base';
      title.value = base ? 'honest' : ''; description.value = base ? '월세·생활비·비상금·목표 네 칸을 적는 과정. 직접 만든 카드·본인 녹음, 음악 없음.' : '';
      credit.checked = base; visibility.value = base ? 'unlisted' : ''; zone.value = '';
      audience.value = base ? 'general' : ''; ai.value = base ? 'none' : ''; music.value = base ? 'own' : '';
      upload.querySelector('form').dispatchEvent(new Event('change', {bubbles: true})); render();
    }));
    render();
  }

  const retention = $(page, '#retention-tool');
  if (retention) {
    const cases = {
      opening: [100, 55, 52, 50, 48, 46, 45],
      middle: [100, 92, 85, 55, 50, 48, 45],
      replay: [100, 92, 85, 80, 95, 78, 70]
    };
    const frames = ['가상 영상 시작 · 돈의 용도 네 칸', '빈 메모를 보여 주며 긴 인사', '월세·생활비 칸을 채우기', '네 칸의 뜻을 길게 반복 설명', '작은 글자로 비상금·목표 표시', '내 메모에 쓸 곳 적기', '완성된 네 칸 메모 보여 주기'];
    const kind = $(retention, '#curve-case'), time = $(retention, '#curve-time'), hypothesis = $(retention, '#curve-hypothesis');
    const button = $(retention, '[data-curve-suggest]');
    const render = () => {
      const values = cases[kind.value], empty = !values, i = Number(time.value) / 5;
      time.disabled = empty; hypothesis.disabled = empty; button.disabled = empty;
      $(retention, '[data-curve-line]').setAttribute('points', empty ? '' : values.map((v,j) => `${45+j*490/6},${200-v*1.8}`).join(' '));
      const x = 45+i*490/6, y = empty ? 200 : 200-values[i]*1.8;
      const head = $(retention, '[data-curve-head]'), dot = $(retention, '[data-curve-dot]');
      head.style.display = dot.style.display = empty ? 'none' : '';
      head.setAttribute('x1', x); head.setAttribute('x2', x); dot.setAttribute('cx', x); dot.setAttribute('cy', y);
      $(retention, '[data-curve-time]').textContent = empty ? '데이터 없음 · 시점 판단 보류' : `${time.value}초에 정지 · 가상 유지 비율 ${values[i]}%`;
      const frame = $(retention, '[data-curve-frame]');
      frame.replaceChildren();
      const caption = document.createElement('span'); caption.textContent = empty ? '곡선이 나타나면 장면을 대조하세요' : frames[i];
      const sub = document.createElement('small'); sub.textContent = '직접 그린 장면 도식 · 실제 업로드 화면이 아닙니다'; frame.append(caption, sub);
      frame.setAttribute('aria-label', caption.textContent);
      $(retention, '[data-curve-observation]').textContent = empty ? '수치가 없으므로 이탈 지점이나 원인을 정하지 않습니다.' : i === 0 ? '시작점입니다. 다음 지점과 비교해 보세요.' : `가상 관찰: ${Number(time.value)-5}초 ${values[i-1]}% → ${time.value}초 ${values[i]}%. 장면을 보고 가능한 이유를 고르세요.`;
      $(retention, '[data-curve-table]').replaceChildren(...(empty ? [] : values.map((v,j) => {
        const tr = document.createElement('tr'), th = document.createElement('th'), td = document.createElement('td');
        th.scope = 'row'; th.textContent = `${j*5}초`; td.textContent = `${v}%`; tr.append(th,td); return tr;
      })));
      report(retention, '—', empty ? '데이터가 처리될 때까지 기다리고 영상 자체를 검수하세요.' : '선택한 구간을 보고 원인 가설을 고른 뒤 수정안을 확인하세요.');
    };
    kind.addEventListener('change', () => { time.value = kind.value === 'middle' ? '15' : kind.value === 'replay' ? '20' : '5'; hypothesis.value = ''; render(); });
    time.addEventListener('input', render); time.addEventListener('change', render);
    hypothesis.addEventListener('change', render);
    button.addEventListener('click', () => {
      const edits = {intro:'완성된 네 칸 메모를 먼저 보여 주고 긴 인사말을 줄이세요.', dense:'반복 설명을 빼거나 자막을 나눠 읽을 시간을 주세요.', replay:'같은 구간을 직접 읽어 보고 작은 글자를 나누는 안을 비교하세요.'};
      if (!edits[hypothesis.value]) { report(retention, '—', '원인 가설을 먼저 선택하세요.'); return; }
      report(retention, `${time.value}초 수정안`, `${edits[hypothesis.value]} 이 가설을 다음 편에서 시험하고 같은 기간의 지표를 비교하세요.`);
    });
    render();
  }

  const policy = $(page, '#policy-tool');
  if (policy) {
    const origin = $(policy, '#policy-origin'), repeat = $(policy, '#policy-repeat'), ai = $(policy, '#policy-ai'), music = $(policy, '#policy-music');
    const render = () => {
      const notes = [
        origin.value === 'own' ? [false,'독창성: 직접 촬영·설명한 내용과 소재 증거를 보관하세요.'] : [true,origin.value === 'reuse' ? '재사용: 허락이 있어도 자막만 더한 편집에는 수익화 문제가 남습니다. 직접 검증·해설한 장면을 만드세요.' : '소재 허락: 출처와 사용권을 확인할 때까지 게시를 보류하고 직접 촬영으로 바꾸세요.'],
        repeat.value === 'new' ? [false,'제작 방식: 이번 편만의 문제·설명·장면을 유지하세요.'] : [true,'양산형·스팸: 이름만 바꾸는 대량생산을 멈추고, 이번 편에서 새로 설명할 내용을 만드세요.'],
        ai.value === 'assist' ? [false,'AI 공개: 대본·자막 보조만 쓴 예외에 해당하는지 최종 영상을 대조하세요.'] : [true,ai.value === 'unknown' ? 'AI 사용: 생성한 부분부터 확인한 뒤 공식 공개 예시와 대조하세요.' : 'AI 공개: 사실적 합성·AI 음악은 공개 예시입니다. AI 사용 설정에 반영하고 소재 권리도 확인하세요.'],
        music.value === 'unknown' ? [true,'음악: 출처만 적어서는 사용권이 해결되지 않습니다. 사용권을 확보하거나 음원을 바꾸거나 빼세요.'] : [false,music.value === 'library' ? '음악: 오디오 보관함 트랙의 이용 조건과 필수 저작자 표시를 대조하세요.' : '음악: 외부 녹음·샘플을 섞지 않았는지 확인하세요.']
      ];
      const count = notes.filter(([action]) => action).length;
      report(policy, `${count}개 조치`, count ? '아래 항목을 고친 뒤 영상과 증거를 다시 확인하세요.' : '선택한 예의 점검 메모입니다. 아동용·협찬·커뮤니티 가이드도 따로 확인하세요.');
      $(policy, '[data-policy-actions]').replaceChildren(...notes.map(([action,text]) => { const li=document.createElement('li'); li.textContent=`${action?'조치 필요':'대조·보관'} · ${text}`; return li; }));
    };
    listen(policy,render);
    policy.querySelectorAll('[data-policy-preset]').forEach(button=>button.addEventListener('click',()=>{
      const risk=button.dataset.policyPreset==='risk'; origin.value=risk?'reuse':'own'; repeat.value=risk?'mass':'new'; ai.value=risk?'realistic':'assist'; music.value=risk?'unknown':'own'; render();
    }));
    render();
  }

  const plan = $(page, '#plan-tool');
  if (plan) {
    const start = $(plan, '#plan-start'), minutes = $(plan, '#plan-minutes'), days = $(plan, '#plan-days');
    const calendar = $(plan, '[data-plan-calendar]'), copy = $(plan, '#plan-copy');
    // 작업별 분수는 모두 가상 추정이며 실제 제작 속도를 뜻하지 않는다.
    const tasks = [
      ['독자·주제·형식 메모',30], ['첫 편 대본·읽기 확인',50], ['첫 편 내레이션 녹음',40], ['첫 편 직접 촬영·소재 권리 메모',80],
      ['첫 편 컷 편집',100], ['첫 편 자막·소리 맞추기',60], ['첫 편 출력·전체 검수',50], ['첫 편 업로드·공개 주소 기록',30],
      ['첫 편 지표 관찰·없으면 관찰 메모 보류',30], ['다음 편에서 바꿀 장면·템플릿 정리',30],
      ['다음 편 새 대본·읽기 확인',40], ['다음 편 녹음·직접 촬영',90], ['다음 편 편집·자막',120], ['다음 편 출력·검수·업로드·주소 기록',90],
      ['같은 기간 지표·비용·개선 메모 비교',30], ['다음 달 계획·보류 작업 정리',30]
    ];
    let exportRows = [], pendingText = '';
    const renderCopy = () => { copy.value = ['가상 30일 계획 · 작업별 시간은 가상 추정', '날짜 | 작업 | 완료 | 실제 시간', ...exportRows.map((row,i)=>`${row.date} | ${row.text} | ${calendar.querySelector(`[data-plan-check="${i}"]`)?.checked?'완료':'미완료'} | __분`), '', pendingText, '체크는 이 페이지에서만 유지됩니다. 개인 메모로 옮기세요.'].join('\n'); };
    const render = () => {
      const inputs = [start,minutes,days];
      const invalid = inputs.some(input=>!input.value.trim()||!input.validity.valid||!Number.isFinite(input.valueAsNumber));
      inputs.forEach(input=>input.setAttribute('aria-invalid', String(!input.value.trim()||!input.validity.valid||!Number.isFinite(input.valueAsNumber))));
      if(invalid) {
        calendar.replaceChildren(); copy.value=''; exportRows=[]; pendingText='';
        $(plan,'[data-plan-formula]').textContent='날짜·시간·활동일 입력 범위를 확인하세요.';
        $(plan,'[data-plan-pending]').textContent=''; $(plan,'[data-plan-reviews]').replaceChildren();
        report(plan,'—','입력값을 고치면 날짜표를 다시 만듭니다.'); return;
      }
      const first = new Date(start.value+'T12:00:00Z'), active=Number(days.value), daily=Math.max(Number(minutes.value)-10,0);
      const dateAt=i=>{const date=new Date(first);date.setUTCDate(date.getUTCDate()+i);return date.toISOString().slice(0,10);};
      let task=0, remaining=tasks[0][1], usedDays=0, unused=0;
      exportRows=Array.from({length:30},(_,i)=>{
        let text;
        if(i%7>=active) text='쉬는 날 · 미완료는 다음 활동일로';
        else {
          usedDays++;
          if(daily===0) text='제작 배정 없음 · 시간·활동일 또는 작업 범위 조정';
          else if(task>=tasks.length) {text='여유일 · 보류 작업·소재·개선 메모 확인';unused+=daily;}
          else {
            const assigned=Math.min(daily,remaining); remaining-=assigned; unused+=daily-assigned;
            text=`${tasks[task][0]} · 가상 ${assigned}분 배정${remaining?` / 이 작업 잔여 ${remaining}분`: ' / 이 작업 배정 끝'} + 검수·메모 10분${daily>assigned?` / 여유 ${daily-assigned}분`:''}`;
            if(!remaining) {task++;remaining=tasks[task]?.[1]||0;}
          }
        }
        return {date:dateAt(i),text};
      });
      const left=remaining+tasks.slice(task+1).reduce((sum,[,time])=>sum+time,0);
      pendingText=task<tasks.length?`다음 활동일로 남길 가상 작업: ${tasks[task][0]}부터 ${left}분. 실제 작업 속도에 맞춰 다시 나누세요.`:'가상 작업 배정이 끝났습니다. 실제로 끝낸 결과물과 공개 상태는 직접 확인하세요.';
      const table=document.createElement('table'), caption=document.createElement('caption');caption.textContent=`가상 30일 초안 · 시작일부터 매 7일 중 앞 ${active}일 활동`;
      const thead=document.createElement('thead');thead.innerHTML='<tr><th scope="col">날짜</th><th scope="col">할 일</th><th scope="col">완료</th></tr>';
      const tbody=document.createElement('tbody');
      exportRows.forEach((row,i)=>{
        const tr=document.createElement('tr'), th=document.createElement('th'), td=document.createElement('td'), checkCell=document.createElement('td'), check=document.createElement('input');
        th.scope='row';th.textContent=row.date;td.textContent=row.text;check.type='checkbox';check.dataset.planCheck=i;check.setAttribute('aria-label',row.date+' 계획 확인');
        checkCell.append(check);tr.append(th,td,checkCell);tbody.append(tr);
      });
      table.append(caption,thead,tbody);calendar.replaceChildren(table);
      $(plan,'[data-plan-formula]').textContent=`가상 계산: 활동 ${usedDays}일 × max(${minutes.value}분 − 10분, 0) = ${usedDays*daily}분. 이 중 여유 ${unused}분. 작업별 분수는 가상 추정입니다.`;
      report(plan,`${(usedDays*daily).toLocaleString('ko-KR')}분`,daily&&usedDays?'검수·메모를 뺀 제작 예산입니다. 날짜별 배정과 보류 작업을 확인하세요.':'제작 배정 시간이 없으니 확보 시간·활동일·기간을 조정하세요.');
      $(plan,'[data-plan-pending]').textContent=pendingText;
      $(plan,'[data-plan-reviews]').replaceChildren(...[6,13,20,27,29].map(i=>{const li=document.createElement('li');li.textContent=`${dateAt(i)} 점검: 완료 / 보류 이유 / 실제 시간·비용 / 다음 편에서 바꿀 장면 / 다음 활동일`;return li;}));
      renderCopy();
    };
    const update = event=>{if([start,minutes,days].includes(event.target))render();};
    listen(plan,update); calendar.addEventListener('change',renderCopy);
    plan.querySelectorAll('[data-plan-preset]').forEach(button=>button.addEventListener('click',()=>{start.value='2026-10-27';minutes.value=button.dataset.planPreset==='zero'?'0':'60';days.value='5';render();}));
    $(plan,'[data-plan-copy]').addEventListener('click',()=>{copy.focus();copy.select();});
    render();
  }
})();
