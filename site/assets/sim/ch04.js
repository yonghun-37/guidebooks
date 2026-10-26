(() => {
  'use strict';
  ReelsSim.mount('#concept-figure', (el, report) => {
    const details = ["독자: 누구의 어떤 업무·상황을 돕는지 구체적으로 적습니다.", "문제: 반복해서 답할 질문을 적고, 수요 관찰과 내 추측을 구별합니다.", "약속: 형식·원문 근거·다루지 않을 범위와 시간 예산을 기획 시트에 붙입니다."];
    ReelsSim.buttonGroup(el.querySelector('[data-concept-buttons]'), step => {
      el.querySelectorAll('[data-node]').forEach(node => { node.dataset.active = String(node.dataset.node === step); });
      report(details[Number(step)]);
    });
  });
  ReelsSim.mount('#niche-sim', (el, report) => {
    const keys = ['interest', 'demand', 'gap', 'revenue', 'capacity'];
    const inputs = keys.map(key => el.querySelector('#' + key));
    const evidence = el.querySelector('#evidence');
    const update = () => {
      const values = inputs.map(input => Number(input.value));
      inputs.forEach((input, i) => { el.querySelector(`[data-value="${input.id}"]`).textContent = values[i] + ' / 5'; });
      const total = values.reduce((a,b) => a+b,0);
      const status = values[4] === 0 ? '제작 여유가 0입니다. 합계와 무관하게 범위·형식·일정을 다시 정하세요.' : '점수 옆에 근거와 실제 초안 시간을 적어 후보를 비교하세요.';
      const evidenceText = evidence.value === 'unknown' ? '수요·수익은 아직 가정입니다.' : '관찰 메모를 남겼다는 자기보고입니다. 근거의 질과 날짜를 직접 확인하세요.';
      report(`자기평가 합계 ${total} / 25 · 환산 ${total * 4} / 100. ${status} ${evidenceText} 성장 가능성이나 수입 확률이 아닙니다.`);
    };
    inputs.forEach(input => input.addEventListener('input', update)); evidence.addEventListener('change', update);
    el.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const values = button.dataset.preset === 'break' ? [5,5,5,5,0] : [3,2,3,1,3];
      inputs.forEach((input, i) => { input.value = values[i]; }); evidence.value = 'unknown'; update();
    }));
    update();
  });
})();
