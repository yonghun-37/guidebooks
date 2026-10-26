(() => {
  'use strict';
  ReelsSim.mount('#concept-figure', (el, report) => {
    const details = ["발견: RSS·검색·정부 자료에서 후보를 찾고 원문 URL·게시일·사건일·확인일을 남깁니다.", "대조: 원문에서 인명·수치·단위·조건을 직접 대조합니다. 못 읽은 자료는 미확인으로 남깁니다.", "권리 검토: 사실·기사 표현·사진을 나누고 허락 또는 인용 근거와 초상·개인정보 등을 별도로 살핍니다."];
    ReelsSim.buttonGroup(el.querySelector('[data-concept-buttons]'), step => {
      el.querySelectorAll('[data-node]').forEach(node => { node.dataset.active = String(node.dataset.node === step); });
      report(details[Number(step)]);
    });
  });
  ReelsSim.mount('#rights-sim', (el, report) => {
    const keys = ['origin', 'permission', 'quotation', 'people', 'verified'];
    const inputs = keys.map(key => el.querySelector('#' + key));
    const update = () => {
      const [origin, permission, quotation, people, verified] = inputs.map(input => input.value);
      const pending = [];
      if (origin !== 'yes') pending.push('원문・권리자 기록');
      if (permission !== 'yes') {
        if (quotation !== 'yes') pending.push('내 이용을 포괄하는 허락 또는 인용・공정 이용 검토 근거');
        else pending.push('인용・공정 이용 검토의 개별 적합성 재확인(일반 허락으로 확대하지 않기)');
      }
      if (people !== 'yes') pending.push('초상・개인정보 등 다른 권리');
      if (verified !== 'yes') pending.push('사실・수치・조건의 원문 대조');
      if (pending.length) report('검토 보류 항목: ' + pending.join(' / ') + '. 기록을 보완하거나 허락받은 다른 소재를 검토하세요. 자동 법률 판정이 아닙니다.');
      else report('선택상 검토 기록이 모였습니다. 허락의 실제 범위・첨부물・다른 권리와 출처 표기를 사람이 최종 확인하세요. 게시 허가・적법성・정확성을 자동 인증한 결과가 아닙니다.');
    };
    inputs.forEach(input => input.addEventListener('change', update));
    el.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const values = {default: ['unknown','unknown','unknown','unknown','unknown'], reviewed: ['yes','yes','unknown','yes','yes'], break: ['yes','no','no','unknown','no']}[button.dataset.preset];
      inputs.forEach((input, i) => { input.value = values[i]; }); update();
    }));
    update();
  });
})();
