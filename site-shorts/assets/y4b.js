/* 직접 만든 네 칸 메모 예제로 구도·시간·글자·압축을 비교한다. 계정/네트워크 호출 없음. */
(() => {
  'use strict';
  const one = (root, selector) => root.querySelector(selector);
  const listen = (root, render) => {
    root.addEventListener('input', render);
    root.addEventListener('change', render);
  };
  const result = (root, number, message) => {
    const strong = document.createElement('strong');
    strong.textContent = number;
    one(root, '[data-sim-result]').replaceChildren(strong, document.createTextNode(message));
  };
  const outputs = root => root.querySelectorAll('output[data-value]').forEach(el => {
    const value = one(root, '#' + el.dataset.value).valueAsNumber;
    el.textContent = Number.isInteger(value) ? value : value.toFixed(2);
  });
  const valuesValid = inputs => inputs.map(input => {
    const valid = input.value.trim() !== '' && input.validity.valid && Number.isFinite(input.valueAsNumber);
    input.setAttribute('aria-invalid', String(!valid));
    return valid;
  }).every(Boolean);
  const intersects = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
  // 각 도구는 자동 재생하지 않는다. 화면 밖/숨김/동작 줄이기 전환 때 멈춘다.
  function transport(root, draw, { end, getLoop = () => null, fps = 30 }) {
    let time = 0, running = false, raf = 0, stamp;
    const button = one(root, '[data-edit-play], [data-caption-play], [data-quality-play]');
    const paint = () => draw(time, running);
    const pause = () => {
      running = false;
      cancelAnimationFrame(raf);
      button.setAttribute('aria-pressed', 'false');
      button.textContent = button.hasAttribute('data-caption-play') ? '한 번 재생' : '재생';
      paint();
    };
    const frame = now => {
      if (!running) return;
      const range = getLoop();
      time += Math.min((now - stamp) / 1000, .1);
      stamp = now;
      if (range && time >= range[1]) time = range[0] + (time - range[0]) % (range[1] - range[0]);
      else if (time >= end()) { time = end(); pause(); return; }
      paint();
      raf = requestAnimationFrame(frame);
    };
    const play = () => {
      if (running) { pause(); return; }
      const range = getLoop();
      if (time >= end() || (range && (time < range[0] || time >= range[1]))) time = range ? range[0] : 0;
      running = true;
      button.setAttribute('aria-pressed', 'true');
      button.textContent = '일시 정지';
      stamp = performance.now();
      paint();
      raf = requestAnimationFrame(frame);
    };
    const seek = value => { pause(); time = Math.max(0, Math.min(end(), value)); paint(); };
    button.addEventListener('click', play);
    document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });
    new IntersectionObserver(entries => { if (!entries[0].isIntersecting) pause(); }).observe(root);
    matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', pause);
    window.addEventListener('pagehide', pause);
    return { seek, pause, paint, get time() { return time; }, step(direction) { seek((Math.round(time * fps()) + direction) / fps()); } };
  }

  const framing = document.getElementById('framing-tool');
  if (framing) {
    const x = one(framing, '#subject-x'), y = one(framing, '#subject-y');
    const render = () => {
      outputs(framing);
      const zoom = one(framing, '#shot').value === 'detail' ? 1.35 : 1;
      const subject = one(framing, '[data-subject]');
      subject.setAttribute('transform', `translate(${(x.valueAsNumber - 50) * 1.8} ${(y.valueAsNumber - 50) * 3.2}) translate(90 193) scale(${zoom}) translate(-90 -193)`);
      const show = one(framing, '#show-ui').checked;
      framing.querySelectorAll('.occlusion').forEach(el => { el.hidden = !show; el.style.display = show ? '' : 'none'; });
      const bounds = subject.getBoundingClientRect(), viewport = one(framing, '.portrait-frame').getBoundingClientRect();
      const clipped = bounds.left < viewport.left || bounds.right > viewport.right || bounds.top < viewport.top || bounds.bottom > viewport.bottom;
      const overlaps = show ? [...framing.querySelectorAll('.occlusion')].filter(el => intersects(bounds, el.getBoundingClientRect())).length : 0;
      result(framing, `${overlaps}곳 겹침`, !show ? '가림 영역이 숨겨져 있습니다. 다시 켜서 확인하세요.' : clipped ? '물건이 프레임 밖으로 잘립니다. 위치나 구도를 바꾸세요.' : overlaps ? '가상 가림 영역과 물건이 겹칩니다. 중앙 쪽으로 옮겨 보세요.' : '이 그림에서는 물건이 가려지지 않습니다. 실제 앱에서도 확인하세요.');
    };
    framing.querySelectorAll('[data-scene-preset]').forEach(button => button.addEventListener('click', () => {
      const edge = button.dataset.scenePreset === 'edge';
      x.value = edge ? 85 : 50; y.value = edge ? 80 : 50;
      one(framing, '#shot').value = 'wide'; one(framing, '#show-ui').checked = true;
      render();
    }));
    listen(framing, render);
    new ResizeObserver(render).observe(one(framing, '.portrait-frame'));
    render();
  }

  const editing = document.getElementById('rhythm-tool');
  if (editing) {
    const fields = Object.fromEntries(['cut-time', 'caption-start', 'caption-end', 'voice-start', 'music-end', 'loop-start', 'loop-end'].map(id => [id, one(editing, '#' + id)]));
    const val = key => fields[key].valueAsNumber;
    const seek = one(editing, '#edit-seek');
    const loop = one(editing, '#loop-on');
    const names = ['네 칸 소개', '월세부터 따로', '메모 완성'];
    let valid = true, player;
    const check = () => {
      let okay = valuesValid(Object.values(fields));
      for (const [start, end] of [['caption-start', 'caption-end'], ['loop-start', 'loop-end']]) {
        const ordered = val(start) < val(end);
        if (!ordered) [start, end].forEach(id => fields[id].setAttribute('aria-invalid', 'true'));
        okay = okay && ordered;
      }
      return okay;
    };
    const paint = (time, playing) => {
      seek.value = Math.round(time * 30);
      one(editing, '[data-value="edit-seek"]').textContent = `${time.toFixed(2)}초`;
      one(editing, '[data-edit-clock]').textContent = `${time.toFixed(2)}초 / 12초`;
      const status = one(editing, '[data-play-state]');
      const message = playing ? '재생 중 · 도식은 무음입니다.' : '프레임 정지 · 도식은 무음입니다.';
      if (status.textContent !== message) status.textContent = message;
      const lane = one(editing, '.track-area');
      one(editing, '.timeline-head').style.left = `${42 + (lane.clientWidth - 42) * time / 12}px`;
      if (!valid) { one(editing, '[data-edit-caption]').textContent = ''; one(editing, '[data-edit-scene]').textContent = '입력 시간을 확인하세요'; return; }
      const scene = time < val('cut-time') ? 0 : time < 8 ? 1 : 2;
      one(editing, '[data-edit-scene]').textContent = names[scene];
      one(editing, '[data-subject]').setAttribute('transform', `translate(${scene === 1 ? Math.sin(time * 2) * 8 : 0} 0)`);
      const captions = [[0, 4, '네 칸 소개'], [val('caption-start'), val('caption-end'), names[1]], [8, 12, '메모 완성']];
      one(editing, '[data-edit-caption]').textContent = captions.filter(([s,e]) => time >= s && time < e).map(a => a[2]).join(' / ');
    };
    player = transport(editing, paint, {end: () => 12, fps: () => 30, getLoop: () => valid && loop.checked ? [val('loop-start'), val('loop-end')] : null});
    const render = () => {
      valid = check();
      one(editing, '[data-edit-play]').disabled = !valid;
      if (!valid) {
        editing.querySelectorAll('.track-lane').forEach(el => el.replaceChildren());
        result(editing, '—', '빈 값·입력 범위와 시작 < 끝을 확인하세요.');
        player.pause();
        return;
      }
      const tracks = {
        scene: [[0,val('cut-time'),names[0]],[val('cut-time'),8,'용도'],[8,12,names[2]]],
        caption: [[0,4,'네 칸 소개'],[val('caption-start'),val('caption-end'),'월세'],[8,12,'메모 완성']],
        voice: [[val('voice-start'),4+val('voice-start'),'상황'],[4+val('voice-start'),8+val('voice-start'),'방법'],[8+val('voice-start'),12+val('voice-start'),'결과']],
        music: [[0,val('music-end'),'가상 음악 구간']]
      };
      Object.entries(tracks).forEach(([key, clips]) => {
        const lane = one(editing, `[data-track="${key}"]`);
        lane.replaceChildren(...clips.filter(([s]) => s < 12).map(([s,e,text]) => {
          const clip = document.createElement('span'); clip.className = 'track-clip';
          clip.style.left = `${s / 12 * 100}%`; clip.style.width = `${(Math.min(e,12) - s) / 12 * 100}%`;
          clip.textContent = `${text}\n${s.toFixed(1)}~${e.toFixed(1)}`;
          clip.title = `${text}: ${s.toFixed(1)}~${e.toFixed(1)}초${e > 12 ? ' (영상 끝에서 잘림)' : ''}`;
          return clip;
        }));
      });
      const difference = val('caption-end') - (8 + val('voice-start'));
      result(editing, `${difference.toFixed(1)}초`, difference < 0 ? '중간 자막이 말보다 먼저 끝납니다. 끝을 늘리거나 문장을 나누세요.' : difference > 0 ? '중간 자막이 말보다 늦게 끝납니다. 다음 자막과 겹치는지도 보세요.' : val('caption-start') !== 4 + val('voice-start') ? '끝은 맞습니다. 중간 자막 시작을 음성 시작과 맞추세요.' : '중간 자막의 시작·끝이 중간 음성에 맞습니다. 실제 파일에서도 들어 보세요.');
      player.paint();
    };
    listen(editing, event => {
      if (event.target === seek) return;
      player.pause(); render();
    });
    seek.addEventListener('input', () => { if (valid) player.seek(seek.valueAsNumber / 30); });
    one(editing, '[data-edit-home]').addEventListener('click', () => player.seek(0));
    editing.querySelectorAll('[data-edit-frame]').forEach(button => button.addEventListener('click', () => { if (valid) player.step(Number(button.dataset.editFrame)); }));
    editing.querySelectorAll('[data-edit-preset]').forEach(button => button.addEventListener('click', () => {
      Object.values(fields).forEach(field => { field.value = field.defaultValue; });
      loop.checked = false;
      if (button.dataset.editPreset === 'early') fields['caption-end'].value = '6';
      render(); player.seek(button.dataset.editPreset === 'early' ? 7 : 0);
    }));
    new ResizeObserver(() => player.paint()).observe(one(editing, '.track-area'));
    render();
  }

  const caption = document.getElementById('caption-tool');
  if (caption) {
    const size = one(caption, '#caption-size'), y = one(caption, '#caption-y'), duration = one(caption, '#caption-duration'), copy = one(caption, '#caption-copy');
    const text = one(caption, '[data-caption-demo]');
    const stage = one(caption, '.portrait-frame');
    let valid = true, preview = true, player;
    const paint = (time, running) => {
      const visible = preview || (valid && time < duration.valueAsNumber);
      text.style.visibility = visible ? 'visible' : 'hidden';
      one(caption, '[data-caption-clock]').textContent = preview ? '정지 미리보기 · 말 길이는 가상 3초' : `${time.toFixed(2)}초 / 3초 · ${time < 3 ? '가상 말 구간' : '말 끝'} · ${visible ? '자막 표시' : '자막 사라짐'}${running ? ' · 재생 중' : ''}`;
    };
    player = transport(caption, paint, {end: () => Math.max(3, duration.valueAsNumber || 3), fps: () => 30});
    const render = () => {
      outputs(caption);
      valid = valuesValid([duration]) && copy.value.trim() !== '';
      copy.setAttribute('aria-invalid', String(!copy.value.trim()));
      one(caption, '[data-caption-play]').disabled = !valid;
      if (!valid) { text.textContent = ''; player.pause(); result(caption, '—', '문장을 채우고 표시 시간의 입력 범위를 확인하세요.'); return; }
      text.textContent = copy.value;
      text.style.top = `${y.value}%`;
      text.style.fontSize = `${size.valueAsNumber * stage.clientWidth / 1080}px`;
      text.classList.toggle('low-contrast', one(caption, '#caption-contrast').value === 'plain');
      const bounds = text.getBoundingClientRect(), view = stage.getBoundingClientRect();
      const overlap = [...caption.querySelectorAll('.occlusion')].some(el => intersects(bounds, el.getBoundingClientRect()));
      const clipped = bounds.top < view.top || bounds.bottom > view.bottom;
      const speed = [...copy.value.replace(/\s/g, '')].length / duration.valueAsNumber;
      const warning = overlap || clipped ? '글자가 가림 영역에 겹치거나 잘립니다. 위치·문장 길이를 바꾸세요.' : duration.valueAsNumber < 3 ? '가상 말보다 먼저 사라집니다. 시간을 늘리거나 문장을 나누세요.' : text.classList.contains('low-contrast') ? '밝은 글자가 배경과 섞입니다. 짙은 바탕을 켜 보세요.' : '자동 합격 판정은 없습니다. 재생하며 끝까지 읽고 실제 폰에서도 확인하세요.';
      result(caption, `${speed.toFixed(1)}글자/초`, warning);
      player.paint();
    };
    // 재생 도중 입력하면 정지 미리보기로 돌아간다.
    listen(caption, () => { preview = true; player.pause(); render(); });
    one(caption, '[data-caption-play]').addEventListener('click', () => { preview = false; player.paint(); });
    one(caption, '[data-caption-show]').addEventListener('click', () => { preview = true; player.pause(); render(); });
    caption.querySelectorAll('[data-caption-preset]').forEach(button => button.addEventListener('click', () => {
      const fast = button.dataset.captionPreset === 'fast';
      copy.value = fast ? '월세와 생활비와 비상금과 목표를 한꺼번에 길게 적으면 작은 화면에서 끝까지 읽기 어려워요' : '월세부터 따로';
      duration.value = fast ? .5 : 3; size.value = 64; y.value = fast ? 90 : 65;
      one(caption, '#caption-contrast').value = 'back'; preview = true; player.seek(0); render();
    }));
    new ResizeObserver(render).observe(stage);
    document.fonts?.ready.then(render);
    render();
  }

  const quality = document.getElementById('quality-tool');
  if (quality) {
    const source = one(quality, '#quality-original'), target = one(quality, '#quality-processed');
    const sc = source.getContext('2d'), tc = target.getContext('2d');
    const small = document.createElement('canvas'), sx = small.getContext('2d');
    const size = one(quality, '#export-size'), fps = one(quality, '#export-fps'), rate = one(quality, '#export-rate');
    function scene(ctx, time) {
      ctx.fillStyle = '#f7d4a5'; ctx.fillRect(0,0,270,480);
      ctx.fillStyle='#59374b'; ctx.font='bold 22px sans-serif'; ctx.fillText('월급날 네 칸',45,86);
      const names=['월세','생활비','비상금','목표'];
      for(let i=0;i<4;i++) {
        const x=25+(i%2)*120,y=140+Math.floor(i/2)*98;
        ctx.fillStyle=['#d88060','#719882','#7196af','#d7b255'][i]; ctx.fillRect(x,y,100,78);
        ctx.fillStyle='#302134'; ctx.font='bold 18px sans-serif'; ctx.fillText(names[i],x+13,y+46);
      }
      // 이동하는 메모와 가는 글자 가장자리로 같은 압축 비교를 한다.
      const x=135+Math.sin(time * 2.5)*67;
      ctx.fillStyle='#fff7e9'; ctx.fillRect(x-23,348,46,25);
      ctx.strokeStyle='#59374b'; ctx.lineWidth=2; ctx.strokeRect(x-23,348,46,25);
      ctx.fillStyle='#352135'; ctx.fillRect(24,395,222,42);
      ctx.fillStyle='#fff7e9'; ctx.font='bold 20px sans-serif'; ctx.fillText('월세부터 따로',55,423);
    }

    const paint = (time, running) => {
      scene(sc, Math.floor(time*60)/60);
      const sample = Math.floor((time + 1e-7)*Number(fps.value))/Number(fps.value);
      scene(tc, sample);
      const factor = size.value === '540' ? .5 : 1;
      const block = rate.value === '2' ? 6 : 1;
      small.width=Math.max(1,Math.round(270*factor/block)); small.height=Math.max(1,Math.round(480*factor/block));
      sx.imageSmoothingEnabled=true; sx.drawImage(target,0,0,small.width,small.height);
      tc.imageSmoothingEnabled=rate.value!=='2'; tc.drawImage(small,0,0,270,480);
      one(quality,'[data-quality-clock]').textContent=`${time.toFixed(2)}초 · ${running ? '재생 중' : '프레임 정지'}`;
    };
    const player=transport(quality,paint,{end:()=>12,fps:()=>Number(fps.value)});
    const render=()=> {
      result(quality,`${(Number(rate.value)*12/8).toFixed(0)}MB`,'가상 영상 데이터 크기입니다. 원본과 글자 가장자리·움직임을 비교하세요.');
      player.paint();
    };
    listen(quality,()=>{player.pause();render();});
    one(quality,'[data-quality-step]').addEventListener('click',()=>player.step(1));
    quality.querySelectorAll('[data-quality-preset]').forEach(button=>button.addEventListener('click',()=>{
      const low=button.dataset.qualityPreset==='low'; size.value=low?'540':'1080'; fps.value='30'; rate.value=low?'2':'8'; player.seek(0); render();
    }));
    render();
  }
})();
