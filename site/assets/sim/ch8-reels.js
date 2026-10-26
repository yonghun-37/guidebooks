/* 키트의 균등 장면 배분을 프레임 단위로 계산한다. 음성·영상 생성은 하지 않는다. */
(() => {
  'use strict';
  ReelsSim.mount('#ch8-flow', (root, report) => {
    const details = [
      'subtitle: 카드의 문장 전체보다 장면에서 읽을 핵심 문장을 남깁니다.',
      '음성 선택: 기본 무음, 선택 시 본인 녹음, 권리를 확인한 TTS 순서로 검토합니다.',
      '자막 시간표: subtitle을 장면별로 균등 배분합니다. 녹음을 인식하거나 단어별로 정렬하지 않습니다.',
      'MP4 검수: 소리를 끄고 자막을 읽은 뒤 소리를 켜서 내용·시간·권리 표시를 확인합니다.'
    ];
    ReelsSim.buttonGroup(root.querySelector('[data-flow-buttons]'), step => {
      root.querySelector('[data-flow-detail]').textContent = details[Number(step)];
      report(details[Number(step)]);
    });
  });
  ReelsSim.mount('#ch8-sim', (root, report) => {
    const duration = root.querySelector('#reel-duration');
    const scenes = root.querySelector('#reel-scenes');
    const chars = root.querySelector('#reel-chars');
    const selected = root.querySelector('#reel-scene-select');
    const bars = root.querySelector('[data-timeline-bars]');
    const svgNode = (name, attrs) => {
      const node = document.createElementNS('http://www.w3.org/2000/svg', name);
      Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, String(value)));
      return node;
    };
    const render = () => {
      const seconds = Number(duration.value), count = Number(scenes.value), letters = Number(chars.value);
      const frames = Math.round(seconds * 24);
      root.querySelector('#reel-duration-out').textContent = `${seconds}초`;
      root.querySelector('#reel-scenes-out').textContent = `${count}개`;
      root.querySelector('#reel-chars-out').textContent = `${letters}자`;
      if (selected.options.length !== count) {
        const previous = Number(selected.value || 0);
        selected.replaceChildren();
        for (let i = 0; i < count; i += 1) selected.add(new Option(`${i + 1}번 장면`, String(i)));
        selected.value = String(Math.min(previous, count - 1));
      }
      const index = Number(selected.value);
      const start = Math.round(index * frames / count) / 24;
      const end = Math.round((index + 1) * frames / count) / 24;
      const speed = letters / (end - start);
      const shortest = Math.floor(frames / count) / 24;
      const worstSpeed = letters / shortest;
      bars.replaceChildren();
      for (let i = 0; i < count; i += 1) {
        const x = Math.round(i * frames / count) / frames * 360;
        const right = Math.round((i + 1) * frames / count) / frames * 360;
        bars.append(svgNode('rect', { x: x + 1, y: 20, width: right - x - 2, height: 48, rx: 3, fill: i === index ? 'var(--accent)' : 'var(--soft)', stroke: 'var(--accent)' }));
        const label = svgNode('text', { x: x + (right - x) / 2, y: 50, 'text-anchor': 'middle', 'font-size': 12, fill: i === index ? 'var(--paper)' : 'var(--ink)' });
        label.textContent = String(i + 1);
        bars.append(label);
      }
      root.querySelector('[data-hook-line]').setAttribute('d', `M${3 / seconds * 360} 12V77`);
      report(`${index + 1}번 장면: ${start.toFixed(2)}~${end.toFixed(2)}초 · ${letters}자 / ${(end - start).toFixed(2)}초 = ${speed.toFixed(1)}자/초. ${worstSpeed > 8 ? '읽기 경고: 한 장면 이상이 연습 경고선 8자/초를 넘습니다. 대본을 줄이거나 시간을 늘려 보세요.' : '연습 경고선 안입니다. 실제로 읽고 들어 보며 조정하세요.'} 첫 3초는 성공 법칙이 아닌 학습용 표식입니다.`);
    };
    root.addEventListener('input', render);
    root.addEventListener('change', render);
    root.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const reset = button.dataset.preset === 'reset';
      duration.value = reset ? '20' : '15';
      scenes.value = reset ? '5' : '10';
      chars.value = reset ? '24' : '150';
      selected.value = '0';
      render();
    }));
    render();
  });
})();
