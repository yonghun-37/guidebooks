/* 답변에 맞는 수정 행동만 안내한다. 정책 심사·법적 판정이 아니다. */
(() => {
  'use strict';
  const tool = document.querySelector('#publish-tool');
  if (!tool) return;
  const field = name => tool.querySelector(`#check-${name}`);
  const render = () => {
    const benefit = field('benefit').value, ai = field('ai').value;
    tool.querySelector('#disclosure-question').hidden = benefit !== 'yes';
    tool.querySelector('#ai-question').hidden = !['text', 'image'].includes(ai);
    const actions = [];
    if (benefit === 'unknown') actions.push('제휴·제품 제공·원고료 관계가 있는지 확인하세요.');
    else if (benefit === 'yes' && field('disclosure').value !== 'yes') actions.push('실제 제휴·제공 관계를 제목 또는 본문 첫 부분에 분명히 적으세요.');
    if (!['yes', 'none'].includes(field('rights').value)) actions.push('사진·소재의 사용 허락과 상업 이용 조건을 확인하거나 내 사진·직접 만든 표로 바꾸세요.');
    if (ai === 'unknown') actions.push('AI를 쓴 범위를 확인하고, 썼다면 사실·경험·표시 조건을 점검하세요.');
    else if (ai !== 'none' && field('ai-review').value !== 'yes') actions.push(ai === 'image' ? '생성 이미지를 체험 사진과 구분하고, 사실·입력 권리·서비스와 플랫폼의 표시 조건을 확인하세요.' : 'AI 초안의 숫자·출처·경험을 원문과 대조하고 표시 조건을 확인하세요.');
    if (!['none', 'safe'].includes(field('ad').value)) actions.push('광고가 본문 버튼·다운로드로 오인되지 않게 배치와 모바일 화면을 확인하세요.');
    tool.querySelector('#publish-result').textContent = actions.length ? `${actions.length}곳을 먼저 확인하세요. 아래 행동을 마친 뒤 다시 점검하세요.` : '0곳 남았습니다. 선택한 답변에 따른 결과이므로 실제 글과 모바일 화면을 마지막으로 읽으세요.';
    tool.querySelector('#publish-actions').replaceChildren(...actions.map(text => { const item = document.createElement('li'); item.textContent = text; return item; }));
  };
  tool.querySelectorAll('select').forEach(select => select.addEventListener('change', render));
  const set = values => { Object.entries(values).forEach(([name, value]) => { field(name).value = value; }); render(); };
  tool.querySelector('#check-ready').addEventListener('click', () => set({benefit:'yes', disclosure:'yes', rights:'yes', ai:'image', 'ai-review':'yes', ad:'safe'}));
  tool.querySelector('#check-extreme').addEventListener('click', () => set({benefit:'yes', disclosure:'no', rights:'no', ai:'image', 'ai-review':'no', ad:'unsafe'}));
  tool.querySelector('#check-reset').addEventListener('click', () => { tool.querySelectorAll('select').forEach(select => { select.value = 'unknown'; }); render(); });
  render();
})();
