(() => {
  'use strict';
  ReelsSim.mount('#concept-figure', (el, report) => {
    const details = ["질문: 독자가 조건을 비교해야 하는지, 사용 장면을 봐야 하는지 먼저 적습니다.", "형식: 비교 설명은 카드, 움직임 설명은 릴스로 구상해 보고 검수할 시간을 남깁니다.", "관찰: 기간·형식·주제·광고 포함 여부를 적고 조회·도달·저장·공유를 같은 범위로 읽습니다."];
    ReelsSim.buttonGroup(el.querySelector('[data-concept-buttons]'), step => {
      el.querySelectorAll('[data-node]').forEach(node => { node.dataset.active = String(node.dataset.node === step); });
      report(details[Number(step)]);
    });
  });
  ReelsSim.mount('#signal-sim', (el, report) => {
    const keys = ['watch', 'save', 'send'];
    const inputs = keys.map(key => el.querySelector('#' + key));
    const update = () => {
      const weights = inputs.map(input => Number(input.value));
      inputs.forEach((input, i) => { el.querySelector(`[data-value="${input.id}"]`).textContent = weights[i]; });
      const sum = weights.reduce((a, b) => a + b, 0);
      if (!sum) { report('가중치 합이 0이라 점수를 계산할 수 없습니다. 모형의 분모가 사라졌습니다. 실제 게시물의 노출이 0이라는 뜻은 아닙니다.'); return; }
      const score = rates => rates.reduce((total, rate, i) => total + rate * weights[i], 0) / sum;
      const a = score([80, 20, 10]), b = score([30, 60, 40]);
      const order = a === b ? '동점' : a > b ? 'A가 앞섬' : 'B가 앞섬';
      report(`가상 점수 A ${a.toFixed(1)} · B ${b.toFixed(1)} / 100 · ${order}. 가중치 합 ${sum}. 실제 추천·노출·수익의 예측이 아닙니다.`);
    };
    inputs.forEach(input => input.addEventListener('input', update));
    el.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const values = { default: [3, 1, 1], save: [1, 5, 3], break: [0, 0, 0] }[button.dataset.preset];
      inputs.forEach((input, i) => { input.value = values[i]; }); update();
    }));
    update();
  });
})();
