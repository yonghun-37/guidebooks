/* 한글 글자 폭을 단순화한 배치 모형. 실제 Pillow 렌더링과 구분한다. */
(() => {
  'use strict';
  ReelsSim.mount('#ch7-flow', (root, report) => {
    const details = [
      'copy.json: 제목·요점·출처를 담는 공통 원본입니다. 본문 이미지는 points를 읽습니다.',
      '표지 cover: 무엇을 읽을지 title로 알리고 body로 범위를 덧붙입니다.',
      '본문 body: points를 번호 요점으로 배치합니다. 한 카드에서 답할 질문을 줄여 보세요.',
      '마무리 closing: 원출처와 저장·공유 안내를 남깁니다. 출처를 읽을 수 있는지 확인합니다.'
    ];
    ReelsSim.buttonGroup(root.querySelector('[data-flow-buttons]'), step => {
      root.querySelector('[data-flow-detail]').textContent = details[Number(step)];
      report(details[Number(step)]);
    });
  });
  ReelsSim.mount('#ch7-sim', (root, report) => {
    const chars = root.querySelector('#card-chars');
    const size = root.querySelector('#card-size');
    const colors = root.querySelector('#card-colors');
    const palettes = { forest: ['#173F34', '#FFF9EC'], ink: ['#182842', '#F0F3F8'], faint: ['#BBBBBB', '#EEEEEE'] };
    const luminance = hex => {
      const rgb = [1, 3, 5].map(start => parseInt(hex.slice(start, start + 2), 16) / 255)
        .map(value => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4);
      return rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722;
    };
    const render = () => {
      const count = Number(chars.value), fontSize = Number(size.value);
      root.querySelector('#card-chars-out').textContent = `${count}자`;
      root.querySelector('#card-size-out').textContent = `${fontSize}px`;
      const perLine = Math.floor(900 / fontSize);
      const lines = Math.ceil(count / perLine);
      const height = lines * fontSize * 1.45;
      const palette = palettes[colors.value];
      const a = luminance(palette[0]), b = luminance(palette[1]);
      const contrast = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
      root.querySelector('[data-card-bg]').setAttribute('fill', palette[1]);
      const ink = root.querySelector('[data-card-ink]');
      ink.setAttribute('fill', palette[0]);
      ink.style.color = palette[0];
      const text = root.querySelector('[data-card-lines]');
      text.replaceChildren();
      const sample = '원문을읽고조건과출처를확인한뒤요점을다시씁니다'.repeat(30).slice(0, count);
      for (let i = 0; i < lines; i += 1) {
        const span = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
        span.setAttribute('x', '27');
        span.setAttribute('y', String(105 + i * fontSize * 1.45 * 0.3));
        span.textContent = sample.slice(i * perLine, (i + 1) * perLine);
        text.append(span);
      }
      text.setAttribute('font-size', String(fontSize * 0.3));
      const warnings = [];
      if (height > 520) warnings.push('넘침 경고: 본문 상자 밖으로 글이 나갑니다. 문안을 줄여 보세요.');
      if (fontSize < 32) warnings.push('작은 글자 경고: 32px 미만은 이 모형에서 정한 연습 경고입니다. 실제 휴대폰에서 확인하세요.');
      if (contrast < 4.5) warnings.push('낮은 대비: 일반 글자 비교선 4.5:1 아래입니다. 색을 바꿔 보세요.');
      report(`모형상 ${lines}줄 · 필요 높이 ${Math.round(height)}px / 상자 520px · 대비 ${contrast.toFixed(2)}:1. ${warnings.join(' ') || '설정한 넘침·크기·대비 경고는 없습니다. 실제 PNG·JPEG와 작은 출처를 확인하세요.'}`);
    };
    root.addEventListener('input', render);
    root.addEventListener('change', render);
    root.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const reset = button.dataset.preset === 'reset';
      chars.value = reset ? '80' : '400';
      size.value = reset ? '44' : '64';
      colors.value = reset ? 'forest' : 'faint';
      render();
    }));
    render();
  });
})();
