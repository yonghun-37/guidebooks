/* 장 전용 도구. 입력은 브라우저 안에서만 계산하며 저장·외부 호출하지 않는다. */
(() => {
  'use strict';
  ReelsSim.mount('#chapter-figure', (element, report) => {
    ReelsSim.buttonGroup(element.querySelector('[data-figure-buttons]'), key => {
      report(element.querySelector(`[data-figure-note="${key}"]`).textContent);
    });
  });

  ReelsSim.mount('#analytics-sim', (element, report) => {
    const table = element.querySelector('[data-metric-table]');
    const feedback = element.querySelector('[data-interpret-feedback]');
    let mismatch = false;
    const read = id => {
      const input = element.querySelector(`#${id}`);
      return input.value === '' || !input.checkValidity() ? null : Number(input.value);
    };
    const update = () => {
      mismatch = element.querySelector('#metric-a-scope').value !== element.querySelector('#metric-b-scope').value;
      let incomplete = false;
      const rows = ['a', 'b'].map(side => {
        const values = ['views', 'reach', 'saved', 'shares'].map(key => read(`metric-${side}-${key}`));
        if (values.some(value => value === null)) {
          incomplete = true;
          return `${side.toUpperCase()}: 빈칸·범위 밖 값이 있어 측정 확인 필요. 비율 계산 보류.`;
        }
        const [views, reach, saved, shares] = values;
        if (!reach) { incomplete = true; return `${side.toUpperCase()}: 조회 ${views}회, 도달 0계정, 저장+공유 ${saved + shares}회. 0 분모로 비율 계산 불가.`; }
        return `${side.toUpperCase()}: 조회 ${views}회, 도달 ${reach}계정, 저장+공유 ${saved + shares}회. 도달 대비 횟수 비율 ${((saved + shares) / reach * 100).toFixed(2)}%.`;
      });
      table.textContent = rows.join('\n');
      report((mismatch ? '측정 범위가 달라 우열 비교를 보류합니다. ' : '선택한 측정 범위는 같습니다. ') + (incomplete ? '빈칸·0 분모 항목은 이유부터 확인하세요. ' : '횟수와 비율을 따로 읽으세요. ') + '고유 사람의 행동 비율·구매율·성장 효과는 알 수 없습니다.');
      feedback.textContent = '';
    };
    element.querySelectorAll('input, select').forEach(input => input.addEventListener('input', update));
    element.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const broken = button.dataset.preset === 'break';
      for (const [side, values] of [['a', [800, broken ? 0 : 400, 16, 4]], ['b', [1800, 1000, broken ? '' : 20, 10]]]) {
        ['views', 'reach', 'saved', 'shares'].forEach((key, i) => { element.querySelector(`#metric-${side}-${key}`).value = values[i]; });
      }
      element.querySelector('#metric-a-scope').value = 'ig';
      element.querySelector('#metric-b-scope').value = broken ? 'total' : 'ig'; update();
    }));
    element.querySelectorAll('[data-interpret]').forEach(button => button.addEventListener('click', () => {
      feedback.textContent = button.dataset.interpret === 'scope'
        ? `맞습니다. ${mismatch ? '현재는 범위가 달라 비교부터 보류합니다.' : '횟수와 분모를 같이 적습니다.'} 수입은 지급 근거가 따로 필요합니다. 근거: 원리의 같은 범위·비율 절.`
        : '이 표에는 구매·지급 자료가 없습니다. 조회 증가를 수입 증가로 단정할 수 없습니다. 근거: 원리의 다음 주 실험 절.';
    }));
    update();
  });

})();
