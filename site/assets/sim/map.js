(() => {
  'use strict';
  // 모두 하린의 가상 연습값이다. 정책·작업 속도·수익의 실측 통계가 아니다.
  const steps = [
    { id: 'source', title: '소재 · 누구의 어떤 질문인가', description: '하린은 원문 링크와 독자가 궁금해할 질문을 메모합니다. 이 연습에서는 오늘 설명할 주제를 하나만 고릅니다.', tools: '브라우저, 원문 링크 메모', minutes: 10, chapters: [4, 5] },
    { id: 'copy', title: '문안 · 내 말로 설명하기', description: '핵심 메시지를 정리하고 카드 문안 또는 릴스 대본을 씁니다. AI의 초안은 사람이 원문과 대조하는 출발점으로 둡니다.', tools: '텍스트 편집기, 선택적으로 AI 글쓰기 도구', minutes: 15, chapters: [6] },
    { id: 'make', title: '카드/릴스 · 하나의 형식 고르기', description: '문안을 카드 묶음 또는 짧은 영상 중 하나로 만듭니다. 이 계산에서 카드 한 묶음과 릴스 한 편은 각각 게시물 1개입니다. 두 형식을 동시에 만드는 시간은 포함하지 않습니다.', tools: '카드 템플릿 또는 영상 편집 도구', minutes: 20, chapters: [7, 8, 9] },
    { id: 'review', title: '검수 · 잠깐, 게시해도 될까', description: '하린은 원문과 문안의 뜻이 같은지, 이미지 사용 근거와 필요한 표시를 확인했는지 점검합니다. 확인하지 못한 내용은 게시 대기 메모로 옮깁니다.', tools: '원문, 게시 전 체크리스트', minutes: 10, chapters: [5, 12] },
    { id: 'publish', title: '게시 · 승인한 결과물만', description: '검수를 마친 결과물의 게시 방식과 일정을 정하는 단계입니다. 이 지도는 흐름만 연습하며 실제 계정 연결이나 게시를 실행하지 않습니다.', tools: '게시 일정 메모, 향후 드라이런 설정', minutes: 5, chapters: [10] },
    { id: 'analyze', title: '분석 · 다음 소재로 돌아가기', description: '하린은 일주일에 한 번 어떤 질문을 다뤘는지, 제작에 시간이 얼마나 걸렸는지 돌아봅니다. 그 기록을 다음 소재와 시간 예산에 반영합니다.', tools: '주간 점검표, 작업 시간 기록', weekly: 30, chapters: [11, 14] },
    { id: 'revenue', title: '수익 · 경로를 검토하는 단계', description: '독자의 어떤 문제를 풀고, 어떤 방식으로 대가를 받을지 적어 봅니다. 이 모형은 금액이나 수익 달성 시점을 계산하지 않습니다. 하린은 별도의 수익 경로 검토 시간을 남겨 둡니다.', tools: '수익 경로 메모, 확인된 정책 자료', weekly: 30, chapters: [3, 12, 13] }
  ];
  const perPost = steps.reduce((total, step) => total + (step.minutes || 0), 0);
  const weeklyReview = steps.reduce((total, step) => total + (step.weekly || 0), 0);
  ReelsSim.mount('#pipeline-map', (element, announce) => {
    const detail = element.querySelector('[data-pipeline-detail]');
    ReelsSim.buttonGroup(element.querySelector('[data-pipeline-buttons]'), id => {
      const step = steps.find(item => item.id === id);
      detail.replaceChildren();
      const heading = document.createElement('h3'); heading.textContent = step.title;
      const description = document.createElement('p'); description.textContent = step.description;
      const meta = document.createElement('dl'); meta.className = 'detail-meta';
      for (const [label, value] of [['필요한 도구', step.tools], ['하린의 시간 예산 (가정)', step.minutes ? `게시물당 ${step.minutes}분` : `주당 ${step.weekly}분`]]) {
        const cell = document.createElement('div'), dt = document.createElement('dt'), dd = document.createElement('dd'); dt.textContent = label; dd.textContent = value; cell.append(dt, dd); meta.append(cell);
      }
      const links = document.createElement('div'); links.className = 'related-links';
      step.chapters.forEach(number => { const chapter = ReelsBook.byNumber(number), anchor = document.createElement('a'); anchor.href = ReelsBook.chapterUrl(chapter); anchor.textContent = `${number}장 · ${chapter.title}${chapter.status === '완성' ? '' : ' (준비 중)'}`; links.append(anchor); });
      detail.append(heading, description, meta, links);
      announce(`${step.title}. ${step.description} 필요한 도구: ${step.tools}. 시간 예산: ${step.minutes ? `게시물당 ${step.minutes}분` : `주당 ${step.weekly}분`} (가정).`);
    });
  });
  ReelsSim.mount('#time-budget', (element, announce) => {
    const slider = element.querySelector('input[type="range"]');
    const weekly = element.querySelector('[data-weekly-hours]');
    const count = element.querySelector('[data-post-count]');
    const bars = element.querySelector('[data-budget-bars]');
    for (let i = 0; i < 20; i += 1) bars.append(document.createElement('span'));
    const update = () => {
      const hours = Number(slider.value);
      const available = Math.max(0, hours * 60 - weeklyReview) * 30 / 7;
      const posts = Math.floor(available / perPost);
      weekly.textContent = `주 ${hours}시간`;
      slider.setAttribute('aria-valuetext', `주 ${hours}시간`);
      count.textContent = posts;
      [...bars.children].forEach((bar, index) => bar.classList.toggle('filled', index < posts));
      announce(`주 ${hours}시간이면 30일 동안 게시물 ${posts}개를 만드는 시간 예산입니다. 계산: floor(max(0, ${hours} × 60 − ${weeklyReview}) × (30 ÷ 7) ÷ ${perPost}). 수익이나 실제 제작량을 보장하지 않는 교육용 계산입니다.`);
    };
    slider.addEventListener('input', update);
    update();
  });
})();
