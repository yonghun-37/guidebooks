/* 이론 AI 제작 모듈 전용: 경로 비교와 모델 표 검색. */
(() => {
  'use strict';
  const route = document.querySelector('#ai-route');
  if (route) {
    const plans = {
      shoot: ['약 60분 · 무료 대본+본인 촬영·녹음+Clipchamp로 short.mp4를 만듭니다.', 'route-shoot'],
      faceless: ['약 65분 · 녹음·자체 카드면 추가 0원, 유료 교체안은 표시가 ₩24,800/월입니다.', 'route-faceless'],
      generate: ['약 80분+대기 · Veo Fast 네 샷은 80크레딧, 유료 교체안은 표시가 ₩29,000/월입니다.', 'route-generate']
    };
    const update = () => {
      const [text, id] = plans[route.value];
      document.querySelector('#ai-route-result').textContent = text;
      document.querySelector('#ai-route-link').setAttribute('href', '#' + id);
    };
    route.addEventListener('change', update);
    update();
  }
  const query = document.querySelector('#ai-model-query');
  if (query) {
    const groups = [...document.querySelectorAll('.ai-model-group')];
    const rows = [...document.querySelectorAll('[data-ai-model]')];
    const index = new Map(rows.map(row => [row, row.textContent.normalize('NFC').toLocaleLowerCase()]));
    const update = () => {
      const value = query.value.trim().normalize('NFC').toLocaleLowerCase();
      for (const row of rows) row.hidden = !index.get(row).includes(value);
      for (const group of groups) {
        group.hidden = !group.querySelector('[data-ai-model]:not([hidden])');
        group.open = Boolean(value) && !group.hidden;
      }
      const count = rows.filter(row => !row.hidden).length;
      document.querySelector('#ai-model-count').textContent = `${count}개 항목 · ${value ? '검색 결과를 펼쳤습니다.' : '분류를 펼쳐 모델과 버전을 읽으세요.'}`;
    };
    query.addEventListener('input', update);
    document.querySelector('#ai-model-reset').addEventListener('click', () => { query.value = ''; update(); query.focus(); });
    update();
  }
})();
