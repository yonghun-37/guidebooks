/* 첫 빈 단계부터 이어가는, 현재 화면 전용 진행 지도. */
(() => {
  'use strict';
  const tool = document.getElementById('first-post-tool');
  const steps = [...tool.querySelectorAll('input[type="checkbox"]')];
  const next = [
    ['독자와 질문을 한 문장으로 적으세요.', '#material', '자료 고르기로 이동 →'],
    ['플랫폼을 고르고 블로그를 만드세요.', '04-platforms.html', '플랫폼 비교로 이동 →'],
    ['내 자료를 AI로 정리해 원고를 만드세요.', '03-ai-tools.html', 'AI 도구 지도로 이동 →'],
    ['공식 원문·사진 권리·필요한 표시를 확인하세요.', '../practice/07-publish.html#review', '발행 전 검수로 이동 →'],
    ['글을 공개하고 휴대폰에서 읽은 주소를 기록하세요.', '../practice/07-publish.html', '첫 공개 실습으로 이동 →'],
    ['공개 주소를 남겼습니다. 수익 신청 조건과 다음 글을 살펴보세요.', '02-revenue.html', '수익 경로로 이동 →']
  ];
  const render = () => {
    const missing = steps.findIndex(input => !input.checked);
    const state = next[missing === -1 ? steps.length : missing];
    document.getElementById('map-result').textContent = `${steps.filter(input => !input.checked).length}단계 남음`;
    document.getElementById('map-next').textContent = state[0];
    const link = document.getElementById('map-link');
    link.href = state[1]; link.textContent = state[2];
  };
  tool.addEventListener('change', render);
  document.getElementById('map-reset').addEventListener('click', () => {steps.forEach(input => {input.checked = false;}); render();});
  render();
})();
