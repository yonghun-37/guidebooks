/* 장 전용 도구. 입력은 브라우저 안에서만 계산하며 저장·외부 호출하지 않는다. */
(() => {
  'use strict';
  ReelsSim.mount('#chapter-figure', (element, report) => {
    ReelsSim.buttonGroup(element.querySelector('[data-figure-buttons]'), key => {
      report(element.querySelector(`[data-figure-note="${key}"]`).textContent);
    });
  });

  ReelsSim.mount('#safety-sim', (element, report) => {
    const get = key => element.querySelector(`#safety-${key}`).value;
    const update = () => {
      const reasons = [];
      if (get('rights') !== 'clear') reasons.push(get('rights') === 'blocked' ? '권리: 조건 불일치 자산을 교체하거나 이용 허락부터 확인.' : '권리: 자산별 허락 범위와 증빙 확인.');
      if (get('facts') !== 'clear') reasons.push(get('facts') === 'error' ? '정확성: 오류·가짜 체험 수정, 예약 중단, 다른 게시본 점검.' : '정확성: 원출처·인물·수치·이미지 실제성 대조.');
      if (get('ad') === 'hidden') reasons.push('광고: 실제 관계와 노출 위치·플랫폼 표시 검토.');
      if (get('ai') === 'unknown') reasons.push('AI·가상인물: 사용 유형과 해당 표시를 별도로 확인.');
      if (get('security') !== 'clear') reasons.push(get('security') === 'exposed' ? '보안: 예약을 멈추고 공식 보안 경로에서 노출 대응. 비밀 값을 결과표에 쓰지 않기.' : '보안: 추가 인증·복구·비밀 값 보관 상태 확인.');
      if (get('ledger') !== 'clear') reasons.push('세무: 지급·비용·활동 형태와 추가 문의 목록 정리.');
      report(reasons.length ? `보류할 확인 항목 ${reasons.length}개\n` + reasons.map(reason => '• ' + reason).join('\n') + '\n표시를 마쳐도 나머지 문제는 사라지지 않습니다.' : '입력상 미확인 항목 없음. 자기 점검 기록을 검수표에 남기세요. 법률 적합·계정 안전·실제 게시를 승인한 결과가 아닙니다.');
    };
    element.querySelectorAll('select').forEach(input => input.addEventListener('input', update));
    element.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const broken = button.dataset.preset === 'break';
      const values = {rights: broken ? 'blocked' : 'clear', facts: broken ? 'error' : 'clear', ad: 'clear', ai: 'clear', security: broken ? 'exposed' : 'clear', ledger: 'clear'};
      Object.entries(values).forEach(([key, value]) => { element.querySelector(`#safety-${key}`).value = value; }); update();
    }));
    update();
  });

})();
