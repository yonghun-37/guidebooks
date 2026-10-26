/* 공통 장 데이터. 새 장 완성 시 본문 파일을 만들고 status를 '완성'으로 바꾼다.
   모든 경로는 이 스크립트 위치를 기준으로 계산하므로 file://와 하위 경로 호스팅을 지원한다. */
(() => {
  'use strict';
  const root = new URL('../', document.currentScript.src);
  const chapterRows = [
  [
    1,
    "01-map",
    "이론편",
    "블로그 글 한 편이 돈이 되기까지",
    "내 글의 독자와 첫 발행 경로",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    2,
    "02-revenue",
    "이론편",
    "블로그는 무엇으로 돈을 버나",
    "내 수익 경로와 참고 계산",
    "내 속도로",
    "입문",
    "샘플"
  ],
  [
    3,
    "03-ai-tools",
    "이론편",
    "AI 도구 지도",
    "글·이미지·키워드 작업별 도구 메모",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    4,
    "04-platforms",
    "이론편",
    "플랫폼 고르기",
    "목표에 맞는 블로그 플랫폼",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    5,
    "05-keywords",
    "이론편",
    "주제와 키워드",
    "키워드와 고른 이유",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    6,
    "06-writing",
    "이론편",
    "AI로 글 쓰기 레시피",
    "사실 확인과 내 경험을 더한 초안",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    7,
    "07-images",
    "이론편",
    "이미지·썸네일",
    "권리와 사용 범위를 확인한 이미지",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    8,
    "08-seo",
    "이론편",
    "검색에 잘 보이는 글",
    "검색 의도와 글 구조 점검",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    9,
    "09-monetize",
    "이론편",
    "수익 장치 붙이기",
    "신청 가능 여부와 다음 확인일",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    10,
    "10-automation",
    "이론편",
    "반복과 자동화",
    "직접 발행·예약·선택 API 구분",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    11,
    "11-analytics",
    "이론편",
    "숫자 읽기",
    "방문·조회·확정 수입 기록",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    12,
    "12-policy",
    "이론편",
    "정책·저작권·광고 표시·세금",
    "내 글의 권리·표시 점검",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    13,
    "13-plan",
    "이론편",
    "30일 운영 계획",
    "내 시간에 맞춘 운영 메모",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    14,
    "lab",
    "이론편",
    "블로그 실험실",
    "원본 계산기로 이어지는 실험실",
    "내 속도로",
    "입문",
    "준비중"
  ],
  [
    15,
    "glossary",
    "이론편",
    "용어집",
    "글을 읽다 만나는 용어",
    "내 속도로",
    "입문",
    "준비중"
  ]
];
  const chapters = chapterRows.map(([number, slug, part, title, deliverable, duration, difficulty, status]) => Object.freeze({number, slug, part, title, deliverable, duration, difficulty, status, track:'theory'}));
  const practiceRows = [
  [
    "00-start",
    "시작 전에: 오늘 쓸 글 고르기",
    "글 유형·플랫폼·준비 자료"
  ],
  [
    "01-account",
    "계정과 블로그 만들기",
    "연습용 블로그와 보안 설정"
  ],
  [
    "02-setup",
    "도구 준비",
    "처음 쓸 AI와 이미지 도구"
  ],
  [
    "03-keywords",
    "키워드 고르기",
    "무료 도구로 고른 키워드"
  ],
  [
    "04-draft",
    "AI 초안과 사실 확인",
    "내 경험과 출처를 더한 원고"
  ],
  [
    "05-images",
    "이미지·썸네일 만들기",
    "직접 사진·AI 삽화·권리 메모"
  ],
  [
    "06-editor",
    "편집기에서 글 다듬기",
    "제목·소제목·링크·표시를 검수한 글"
  ],
  [
    "07-publish",
    "첫 글 실제로 발행하기",
    "모바일로 확인한 첫 공개 글과 주소"
  ],
  [
    "08-search",
    "검색 등록",
    "플랫폼에 맞는 검색 확인 기록"
  ],
  [
    "09-monetize",
    "수익 장치 신청",
    "신청 상태 또는 다음 확인일"
  ],
  [
    "10-automation",
    "선택: 자동화와 첫 숫자 확인",
    "Blogger 기본·설치형 WordPress 심화 계획"
  ]
];
  const practice = practiceRows.map(([slug,title,deliverable],number) => Object.freeze({number,slug,title,deliverable,duration:'내 속도로',track:'practice',part:'실습편',difficulty:'입문',status:number===7?'샘플':'준비중'}));
  practice.push(Object.freeze({number:null,slug:'e2e',title:'한 편 완성 체크리스트',deliverable:'공개 글과 실습 기록',duration:'필요할 때',track:'practice',part:'실습편',difficulty:'입문',status:'준비중'}));
  const appendices = [['prompts','프롬프트 모음'],['ai-models','AI 모델·사용처·비용 총정리'],['credits','출처·크레딧']].map(([slug,title])=>Object.freeze({number:null,slug,title,deliverable:slug==='credits'?'샘플에서 인용한 원문':'블로그 작업별 자료 준비중',track:'appendix',part:'부록',status:slug==='credits'?'샘플':'준비중'}));
  const tracks = Object.freeze([
    { id: 'theory', title: '(이론) 이론편', chapters },
    { id: 'practice', title: '(실습) 실습편', chapters: practice },
    { id: 'appendix', title: '부록', chapters: appendices }
  ]);
  const allChapters = [...chapters, ...practice, ...appendices];
  const prefix = new URL('.', location.href).href === root.href ? '' : '../';
  const url = path => prefix + path;
  const chapterUrl = chapter => {
    if (chapter.track === 'appendix' || ['lab', 'glossary'].includes(chapter.slug)) return url(`${chapter.slug}.html`);
    const folder = chapter.track === 'practice' ? 'practice' : 'chapters';
    return url(chapter.status === '준비중' ? `${folder}/pending.html?chapter=${encodeURIComponent(chapter.slug)}` : `${folder}/${chapter.slug}.html`);
  };
  const byNumber = number => chapters.find(chapter => chapter.number === number);
  const esc = text => String(text).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
  const status = chapter => `<span class="status ${chapter.status === '샘플' ? 'ready' : ''}">${esc(chapter.status)}</span>`;
  const label = chapter => `(${chapter.track === 'practice' ? '실습' : chapter.track === 'appendix' ? '부록' : '이론'}) ${chapter.number != null ? chapter.number + (chapter.track === 'practice' ? '. ' : '장 · ') : ''}${chapter.title}`;
  const link = chapter => `<a href="${chapterUrl(chapter)}">${esc(label(chapter))} ${status(chapter)}</a>`;
  const selected = (document.body.dataset.chapter === 'pending' || document.body.dataset.practice === 'pending') ? new URLSearchParams(location.search).get('chapter') : document.body.dataset.chapter || document.body.dataset.appendix;
  const current = allChapters.find(chapter => chapter.slug === (document.body.dataset.practice && document.body.dataset.practice !== 'pending' ? document.body.dataset.practice : selected));
  if (current && (document.body.dataset.chapter === 'pending' || document.body.dataset.practice === 'pending')) {
    document.querySelector('[data-pending-result]').textContent = current.deliverable;
  }
  const trackLinks = () => tracks.map(track => `<section><h3>${track.title}</h3><ol>${track.chapters.map(chapter => `<li>${link(chapter)}</li>`).join('')}</ol></section>`).join('');
  document.querySelectorAll('[data-chapter-count]').forEach(node => { node.textContent = chapters.filter(chapter => chapter.number !== null).length; });
  document.querySelectorAll('[data-practice-count]').forEach(node => { node.textContent = practice.filter(chapter => chapter.number !== null).length; });
  document.querySelectorAll('[data-sim-count]').forEach(node => { node.textContent = (window.BlogCatalog || []).length; });
  window.BlogBook = Object.freeze({ chapters: Object.freeze(chapters), practice: Object.freeze(practice), tracks, url, chapterUrl, byNumber });

  document.querySelectorAll('[data-site-header]').forEach(header => {
    header.className = 'site-header';
    header.innerHTML = `<div class="header-inner"><a class="brand" href="${url('index.html')}"><span class="brand-mark" aria-hidden="true">b</span>BlogBook</a><div class="header-actions"><a href="${url('index.html#contents')}">전체 목차</a><button type="button" data-menu-toggle aria-expanded="false" aria-controls="book-menu">목차</button><label><span class="sr-only">화면 테마</span><select class="theme-select" data-theme-select><option value="system">시스템</option><option value="light">라이트</option><option value="dark">다크</option></select></label><button type="button" data-theme-toggle aria-label="다크 모드 전환" aria-pressed="false">◐</button></div></div><nav id="book-menu" class="menu-panel" aria-label="전체 장" hidden>${trackLinks()}</nav>`;
    const toggle = header.querySelector('[data-menu-toggle]');
    const panel = header.querySelector('#book-menu');
    const close = () => { panel.hidden = true; toggle.setAttribute('aria-expanded', 'false'); };
    toggle.addEventListener('click', () => { panel.hidden = !panel.hidden; toggle.setAttribute('aria-expanded', String(!panel.hidden)); });
    header.addEventListener('keydown', event => { if (event.key === 'Escape' && !panel.hidden) { close(); toggle.focus(); } });
    panel.addEventListener('click', event => { if (event.target.closest('a')) close(); });
  });

  document.querySelectorAll('[data-chapter-toc]').forEach(toc => {
    toc.innerHTML = tracks.map(track => `<section class="toc-track" id="track-${track.id}"><h2>${track.title}</h2>${[...new Set(track.chapters.map(chapter => chapter.part))].map(part => `<section class="toc-part"><h3>${esc(part)}</h3><ol class="chapter-list">${track.chapters.filter(chapter => chapter.part === part).map(chapter => `<li><a href="${chapterUrl(chapter)}"><span class="chapter-num">${chapter.number != null ? String(chapter.number).padStart(2, '0') : '＋'}</span><span class="chapter-title">${esc(label(chapter))}<span class="chapter-deliverable">${esc(chapter.deliverable)}</span></span>${status(chapter)}</a></li>`).join('')}</ol></section>`).join('')}</section>`).join('');
  });
  document.querySelectorAll('[data-chapter-link]').forEach(anchor => {
    const chapter = byNumber(Number(anchor.dataset.chapterLink));
    if (chapter) anchor.href = chapterUrl(chapter);
  });
  if (current) {
    document.querySelectorAll('[data-chapter-title]').forEach(node => { node.textContent = label(current); });
    document.querySelectorAll('[data-chapter-kicker]').forEach(node => { node.textContent = `(${current.track === 'practice' ? '실습' : '이론'}) ${current.part}${current.number != null ? ' / ' + current.number : ''}`; });
    document.querySelectorAll('[data-chapter-meta]').forEach(meta => {
      const sequence = current.track === 'practice' ? practice : current.track === 'appendix' ? appendices : chapters;
      const previous = sequence[sequence.indexOf(current) - 1];
      meta.className = 'chapter-meta';
      meta.innerHTML = `<div class="deliverable"><dt>이 장을 마치면 만들어지는 것</dt><dd>${esc(current.deliverable)}</dd></div><div><dt>예상 소요 시간</dt><dd>${esc(current.duration)}${current.track === 'theory' ? ' · 읽기·메모, 연결 실습 별도' : ''}</dd></div><div><dt>난이도</dt><dd>${esc(current.difficulty)}</dd></div><div><dt>선행 장</dt><dd>${previous ? link(previous) : '없음 · 여기서 시작'}</dd></div>`;
    });
    const blocks = [...document.querySelectorAll('.chapter-block[id]')];
    const outline = blocks.map(block => `<li><a href="#${block.id}">${esc(block.querySelector('.block-label')?.lastChild.textContent.trim() || block.querySelector('h2').textContent)}</a></li>`).join('');
    document.querySelectorAll('[data-book-sidebar]').forEach(sidebar => {
      sidebar.className = 'book-sidebar';
      sidebar.innerHTML = `<p class="sidebar-label">(${current.track === 'practice' ? '실습' : '이론'}) ${esc(current.part)} · ${current.number ?? '부록'}</p><nav aria-label="이 장의 흐름"><ol>${outline}</ol></nav><nav class="sidebar-chapters" aria-label="장 이동"><p class="sidebar-label">책의 지도</p>${trackLinks()}</nav>`;
    });
    document.querySelectorAll('[data-mobile-outline]').forEach(details => {
      details.className = 'mobile-outline';
      details.innerHTML = `<summary>이 장의 흐름 · ${blocks.length}단계</summary><nav aria-label="이 장의 흐름 (모바일)"><ol>${outline}</ol></nav>`;
    });
    document.querySelectorAll('[data-chapter-pager]').forEach(pager => {
      const sequence = current.track === 'practice' ? practice : current.track === 'appendix' ? appendices : chapters;
      const index = sequence.indexOf(current);
      const previous = sequence[index - 1], next = sequence[index + 1];
      pager.className = 'chapter-pager';
      pager.innerHTML = `${previous ? `<a href="${chapterUrl(previous)}"><small>← 이전 장</small>${esc(label(previous))} ${status(previous)}</a>` : `<a href="${url('index.html')}"><small>← 표지로</small>책의 전체 지도</a>`}${next ? `<a href="${chapterUrl(next)}"><small>다음 장 →</small>${esc(label(next))} ${status(next)}</a>` : `<a href="${url('index.html#contents')}"><small>목차로 →</small>다른 장 살펴보기</a>`}`;
    });
    document.title = `${label(current)} | BlogBook`;
    document.querySelectorAll('.sidebar-chapters a').forEach(anchor => { if (new URL(anchor.href).pathname + new URL(anchor.href).search === location.pathname + location.search) anchor.setAttribute('aria-current', 'page'); });

  }
  document.querySelectorAll('[data-site-footer]').forEach(footer => {
    footer.className = 'site-footer';
    footer.innerHTML = `<span>BlogBook · AI로 쓰는 블로그 수익화 입문</span><span><a href="${url('glossary.html')}">용어집</a> &nbsp; <a href="${url('prompts.html')}">프롬프트</a> &nbsp; <a href="${url('ai-models.html')}">모델·비용</a> &nbsp; <a href="${url('credits.html')}">출처·크레딧</a></span>`;
  });

  // 저장소 접근 자체도 실패할 수 있다. 테마와 체크 상태 모두 읽기/쓰기를 보호한다.
  const storage = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); return true; } catch { return false; } }
  };
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let theme = storage.get('blogbook:theme') || 'system';
  if (!['light', 'dark', 'system'].includes(theme)) theme = 'system';
  const applyTheme = () => {
    const dark = theme === 'dark' || (theme === 'system' && media.matches);
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    document.querySelectorAll('[data-theme-select]').forEach(select => { select.value = theme; });
    document.querySelectorAll('[data-theme-toggle]').forEach(button => { button.setAttribute('aria-pressed', String(dark)); button.setAttribute('aria-label', dark ? '라이트 모드로 전환' : '다크 모드로 전환'); });
  };
  const setTheme = value => { theme = value; storage.set('blogbook:theme', theme); applyTheme(); };
  document.querySelectorAll('[data-theme-select]').forEach(select => select.addEventListener('change', () => setTheme(select.value)));
  document.querySelectorAll('[data-theme-toggle]').forEach(button => button.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark')));
  media.addEventListener('change', applyTheme);
  window.addEventListener('storage', event => {
    if (event.key !== 'blogbook:theme') return;
    const savedTheme = storage.get('blogbook:theme');
    theme = ['light', 'dark', 'system'].includes(savedTheme) ? savedTheme : 'system';
    applyTheme();
  });
  applyTheme();

  const embedId = new URLSearchParams(location.search).get('embed');
  const embedded = embedId && document.getElementById(embedId);
  if (embedded?.closest('.block-figure, .block-simulator')) {
    const block = embedded.closest('.chapter-block') || embedded;
    let node = block;
    while (node && node !== document.body) {
      [...node.parentElement.children].forEach(sibling => { if (sibling !== node && !['SCRIPT', 'STYLE'].includes(sibling.tagName)) sibling.hidden = true; });
      node = node.parentElement;
    }
    block.querySelectorAll('.simulator').forEach(sim => { if (sim !== embedded && !embedded.contains(sim)) sim.hidden = true; });
    document.documentElement.classList.add('sim-embed');
    // 숨긴 설명·각주로 향하는 링크는 전체 장에서 읽는다. 동적 도구 링크도 포함한다.
    document.addEventListener('click', event => {
      const anchor = event.target.closest('a[href]');
      if (!anchor) return;
      const destination = new URL(anchor.href);
      if (destination.origin !== location.origin || destination.pathname !== location.pathname || !destination.hash) return;
      const target = document.getElementById(decodeURIComponent(destination.hash.slice(1)));
      if (!target?.closest('[hidden]')) return;
      anchor.href = `${location.pathname.split('/').pop()}${destination.hash}`;
      anchor.target = '_top';
    }, {capture: true});
  }
  document.querySelectorAll('a[data-term]').forEach((anchor, index) => {
    anchor.classList.add('term');
    const tooltip = document.createElement('span');
    tooltip.className = 'term-tip'; tooltip.id = `term-tip-${index}`; tooltip.role = 'tooltip';
    tooltip.textContent = `${(anchor.dataset.termDescription || anchor.dataset.term)} · 용어집에서 보기`;
    anchor.setAttribute('aria-describedby', tooltip.id);
    anchor.append(tooltip);
    anchor.addEventListener('keydown', event => { if (event.key === 'Escape') tooltip.hidden = true; });
    anchor.addEventListener('blur', () => { tooltip.hidden = false; });
    anchor.addEventListener('mouseleave', () => { tooltip.hidden = false; });
  });
  document.querySelectorAll('[data-checklist]').forEach(list => {
    const key = `blogbook:checklist:${list.dataset.checklist}`;
    let saved = {};
    try { const value = JSON.parse(storage.get(key) || '{}'); if (value && typeof value === 'object' && !Array.isArray(value)) saved = value; } catch { /* 손상된 저장값은 빈 체크리스트로 시작 */ }
    const inputs = [...list.querySelectorAll('input[type="checkbox"][data-check]')];
    const message = list.querySelector('[data-save-status]');
    inputs.forEach(input => {
      input.checked = saved[input.dataset.check] === true;
      input.addEventListener('change', () => {
        const success = storage.set(key, JSON.stringify(Object.fromEntries(inputs.map(item => [item.dataset.check, item.checked]))));
        if (message) message.textContent = success ? `${inputs.filter(item => item.checked).length}/${inputs.length} 완료 · 이 브라우저에 저장됨` : '저장할 수 없는 환경입니다. 이 페이지에서는 계속 체크할 수 있습니다.';
      });
    });
    if (message) message.textContent = `${inputs.filter(item => item.checked).length}/${inputs.length} 완료 · 이 브라우저에만 저장합니다.`;
  });
  document.querySelectorAll('.code-box').forEach(box => {
    const code = box.querySelector('code');
    if (!code) return;
    const button = document.createElement('button'); button.type = 'button'; button.className = 'copy-button'; button.textContent = '복사'; button.setAttribute('aria-label', '코드와 메모 복사');
    const message = document.createElement('p'); message.className = 'copy-status'; message.setAttribute('role', 'status');
    box.append(button, message);
    button.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(code.textContent); message.textContent = '복사했습니다.'; }
      catch { const range = document.createRange(); range.selectNodeContents(code); const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range); message.textContent = '자동 복사를 사용할 수 없습니다. 선택된 내용을 직접 복사하세요.'; }
    });
  });
  document.querySelectorAll('[data-quiz]').forEach(quiz => {
    const questions = [...quiz.querySelectorAll('[data-question]')];
    let answered = 0, correct = 0;
    const score = quiz.querySelector('[data-quiz-score]');
    const update = () => { if (score) score.textContent = `${questions.length}문항 중 ${answered}문항 풀이 · ${correct}문항 정답`; };
    const resetQuestion = question => {
      delete question.dataset.answered;
      question.querySelectorAll('button[data-correct]').forEach(button => { button.disabled = false; button.classList.remove('correct', 'incorrect'); });
      const feedback = question.querySelector('[data-feedback]'); feedback.textContent = ''; feedback.hidden = true;
    };
    questions.forEach(question => {
      question.querySelectorAll('button[data-correct]').forEach(button => button.addEventListener('click', () => {
        if (question.dataset.answered) return;
        question.dataset.answered = 'true';
        const isCorrect = button.dataset.correct === 'true'; answered += 1; if (isCorrect) correct += 1;
        question.querySelectorAll('button[data-correct]').forEach(option => { option.disabled = true; if (option.dataset.correct === 'true') option.classList.add('correct'); });
        if (!isCorrect) button.classList.add('incorrect');
        const feedback = question.querySelector('[data-feedback]'); feedback.hidden = false;
        feedback.textContent = `${isCorrect ? '✓ 정답입니다.' : '↻ 다시 살펴보세요.'} 정답: ${question.querySelector('[data-correct="true"]').textContent} — ${question.dataset.explanation}`;
        if (!isCorrect && question.dataset.retryTool) {
          const retry = document.createElement('a');
          retry.href = question.dataset.retryTool;
          retry.textContent = '관련 도구에서 다시 해 보기 →';
          feedback.append(document.createElement('br'), retry);
        }
        update();
      }));
    });
    quiz.querySelector('[data-quiz-reset]')?.addEventListener('click', () => { questions.forEach(resetQuestion); answered = 0; correct = 0; update(); questions[0]?.querySelector('button').focus(); });
    update();
  });
})();
