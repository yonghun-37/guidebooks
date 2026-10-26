/* 원본 장 하나를 골라 표시한다. 입력 요약은 원본 모듈의 결과를 그대로 읽는다. */
(() => {
  'use strict';
  const picker = document.querySelector('#sim-picker');
  const frame = document.querySelector('#sim-frame');
  const month = document.querySelector('#month-scenario');
  const original = document.querySelector('#sim-original');
  const storageStatus = document.querySelector('[data-month-storage]');
  const put = (selector, text) => { document.querySelector(selector).textContent = text; };
  const summary = (state, missing) => !state ? missing : `${state.valid ? '' : '빈칸·무효 입력이 있습니다. 원본 장에서 수정하세요.\n'}${state.result}`;
  const refresh = () => {
    const savedPlan = ReelsSim.readState('planner-sim');
    const plan = savedPlan?.version === 2 ? savedPlan : null;
    put('[data-month-plan]', plan ? `시작 ${plan.values['plan-start'] || '미입력'} · 하루 ${plan.values['plan-minutes'] || '미입력'}분 · 주 ${plan.values['plan-days']}일\n${summary(plan, '').split('\n').slice(0,2).join('\n')}` : (savedPlan ? '이전 판의 시간 입력이 있습니다. 15장을 열어 새 계산으로 확인하세요.' : '아직 변경한 계획 입력이 없습니다. 15장에서 확보 시간과 활동일을 적어 보세요.'));
  };
  for (const sim of ReelsCatalog.filter(sim => sim.slug !== 'lab')) {
    const option = document.createElement('option');
    option.value = `${sim.chapter}:${sim.id}`; option.textContent = `${sim.chapter}장 · ${sim.title}`; picker.append(option);
  }
  let resizeObserver;
  frame.addEventListener('load', () => {
    resizeObserver?.disconnect();
    try {
      const doc = frame.contentDocument;
      if (!doc) throw new Error('프레임 접근 제한');
      const block = doc.querySelector('.chapter-block:not([hidden])');
      if (!block) throw new Error('도구를 열 수 없음');
      const resize = () => { const height = Math.ceil(block.getBoundingClientRect().height + 40); if (frame.style.height !== `${height}px`) frame.style.height = `${height}px`; };
      resizeObserver = new ResizeObserver(resize); resizeObserver.observe(block); resize();
    } catch {
      storageStatus.textContent = '이 환경에서는 프레임 크기나 저장 입력을 읽지 못할 수 있습니다. 위 원본 장 링크를 이용하세요. 정적 서버에서는 같은 브라우저의 입력을 이어 쓸 수 있습니다.';
    }
  });
  const select = () => {
    const isMonth = picker.value === 'month-scenario';
    month.hidden = !isMonth; frame.hidden = isMonth;
    if (isMonth) { original.href = 'chapters/14-plan.html#simulator'; refresh(); return; }
    const sim = ReelsCatalog.find(sim => `${sim.chapter}:${sim.id}` === picker.value);
    if (!sim) return;
    frame.title = `${sim.chapter}장 · ${sim.title}`;
    frame.src = `chapters/${sim.slug}.html?embed=${encodeURIComponent(sim.id)}`;
    original.href = `chapters/${sim.slug}.html#${sim.section}`;
  };
  picker.addEventListener('change', select);
  document.querySelector('[data-refresh-month]').addEventListener('click', refresh);
  document.querySelector('[data-clear-month]').addEventListener('click', () => {
    const cleared = ReelsSim.clearState(); refresh();
    storageStatus.textContent = cleared ? '15장 입력과 이전 판의 저장 입력을 삭제했습니다. 원본 장을 다시 열면 예시값으로 시작합니다.' : '현재 화면의 입력을 지웠습니다. 저장소 접근 제한으로 영구 저장값 삭제 여부는 확인할 수 없습니다.';
  });
  window.addEventListener('storage', refresh);
  window.addEventListener('reelsbook:inputs', refresh);
  window.addEventListener('pageshow', refresh);
  select();
})();
