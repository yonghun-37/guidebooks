(() => {
  'use strict';
  const root = document.querySelector('#signal-sim');
  if (!root) return;
  const points = root.querySelector('#points');
  const update = () => {
    const count = Number(points.value);
    points.setAttribute('aria-valuetext', `설명 항목 ${count}개`);
    root.querySelector('[data-sim-result]').textContent = `${count + 2}장 · ${count ? '표지와 요약 사이에 설명을 한 장씩 넣는 구성입니다.' : '표지와 요약만 있으니 독자에게 전할 설명을 추가하세요.'}`;
  };
  points.addEventListener('input', update);
  root.querySelector('[data-zero]').addEventListener('click', () => {
    points.value = '0';
    update();
  });
  update();
})();
