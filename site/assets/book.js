/* 공통 장 데이터. 새 장 완성 시 본문 파일을 만들고 status를 '완성'으로 바꾼다.
   모든 경로는 이 스크립트 위치를 기준으로 계산하므로 file://와 하위 경로 호스팅을 지원한다. */
(() => {
  'use strict';
  const root = new URL('../', document.currentScript.src);
  const chapterRows = [
    [1, '01-map', '전체 지도', '계정 하나가 돈이 되기까지', '나의 목표와 시간 예산 메모', '약 30분', '입문', '완성'],
    [2, '02-formats', '1부 · 이해하기', '알고리즘과 포맷: 첫 형식을 고릅니다', '첫 포맷 선택 메모', '약 30분', '입문', '완성'],
    [3, '03-revenue', '1부 · 이해하기', '돈은 네 갈래로 들어옵니다', '내 수익 경로와 오늘 할 일', '약 35분', '입문', '완성'],
    [4, '04-niche', '1부 · 이해하기', '니치와 계정 기획: 도울 독자를 좁힙니다', '계정 기획 시트', '약 40분', '입문', '완성'],
    [5, '05-sources', '2부 · 만들기', '소재 찾기: 뉴스 소싱과 저작권', '원문·권리·출처를 적은 소재 메모', '약 45분', '입문', '완성'],
    [6, '06-writing', '2부 · 만들기', 'AI로 글쓰기: 카드 문안과 릴스 대본', '지시문과 사실 대조 항목', '약 55분', '입문 · 파일 편집', '완성'],
    [7, '07-cards', '2부 · 만들기', '뉴스카드 디자인 자동화', '카드 정보 역할과 검수 기준', '약 50분', '입문 · 문안과 색 편집', '완성'],
    [8, '08-reels', '2부 · 만들기', '릴스 자동 생성: 대본에서 영상까지', '대본·음성·자막의 검수 계획', '약 60분', '입문 · 영상 검수', '완성'],
    [9, '09-pipeline', '3부 · 자동화', '파이프라인 잇기', '검수·실패 대응·외부 비용 메모', '약 60분', '입문 · 생성과 승인', '완성'],
    [10, '10-publishing', '3부 · 자동화', '첫 게시와 예약 경로를 고릅니다', '게시 경로와 예약 확인 메모', '약 45분', '입문', '완성'],
    [11, '11-analytics', '3부 · 자동화', '처음 볼 숫자와 다음 수정을 정합니다', '첫 주 지표와 다음 수정 메모', '약 30분', '입문', '완성'],
    [12, '12-safety', '4부 · 지키기·벌기', '게시 전 권리·표시·대응을 정합니다', '게시 전 확인표와 대응 메모', '약 40분', '입문', '완성'],
    [13, '13-roadmap', '4부 · 지키기·벌기', '첫 독자에서 첫 수익으로 이어갑니다', '첫 협찬 제안과 목표 거래 수', '약 35분', '입문', '완성'],
    [14, '14-plan', '4부 · 지키기·벌기', '30일 동안 할 일을 내 시간에 맞춥니다', '내 달력과 주간 점검표', '약 25분', '입문', '완성'],
    [15, 'lab', '실험실', '자동화 실험실', '그림·계산·연습 모음', '자유롭게', '입문', '완성'],
    [16, 'glossary', '부록', '용어집', '용어 찾아보기', '자유롭게', '입문', '완성'],
    [null, 'credits', '부록', '출처·크레딧', '출처와 업데이트 기록', '자유롭게', '입문', '완성']
  ];
  const chapters = chapterRows.map(([number, slug, part, title, deliverable, duration = '추후 안내', difficulty = '추후 안내', status = '준비중']) =>
    Object.freeze({ number, slug, part, title, deliverable, duration, difficulty, status, track: 'theory' }));
  const practiceRows = [
    ['00-start', '시작 전에', '오늘 할 경로와 준비물 메모', '약 10분'],
    ['01-account', '테스트 계정과 보안 준비', '대상 계정 이름·공개 범위·복구 수단', '약 25분'],
    ['02-setup', '키트 설치와 첫 실행', '카드·영상과 검수 대기 폴더', '약 35분'],
    ['03-copy', '소재 고르기와 웹 채팅 문안', '원출처가 담긴 copy.json', '약 30분'],
    ['04-cards', '뉴스카드 캐러셀 만들기', '순서와 글자를 확인한 JPEG 카드 묶음', '약 20분'],
    ['05-reel', '본인 녹음과 릴스 만들기', '끝까지 재생해 본 reel.mp4', '약 25분'],
    ['06-review', '게시 전 사람 검수', '검수표·APPROVED.json·드라이런', '약 20분'],
    ['07-publish', '앱으로 첫 게시하기', '직접 확인한 첫 게시물과 그 주소', '약 30분'],
    ['08-api', '선택 · API 자동 게시', '계정·권한·공개 URL을 확인한 요청 미리보기', '약 60분 이상 · 선택 심화'],
    ['09-schedule', '매일 생성 예약과 사람 승인', '매일 생성 설정·날짜별 폴더·검수와 게시 계획', '약 30분 + 다음 날 확인'],
    ['10-insights', '첫 24시간·7일 지표', '두 시점의 관찰 기록과 다음 수정점', '약 15분씩 · 관찰할 때마다']
  ];
  const practice = practiceRows.map(([slug, title, deliverable, duration], number) => Object.freeze({
    number, slug, title, deliverable, duration, track: 'practice', part: '실습편', status: '완성'
  }));
  const tracks = Object.freeze([
    { id: 'theory', title: '(이론) 이론편', chapters },
    { id: 'practice', title: '(실습) 실습편', chapters: practice }
  ]);
  const allChapters = [...chapters, ...practice];
  const prefix = new URL('.', location.href).href === root.href ? '' : '../';
  const url = path => prefix + path;
  const chapterUrl = chapter => {
    if (chapter.track === 'practice') return url(`practice/${chapter.slug}.html`);
    if (['lab', 'glossary', 'credits'].includes(chapter.slug)) return url(`${chapter.slug}.html`);
    return chapter.status === '완성' ? url(`chapters/${chapter.slug}.html`) : url(`chapters/coming-soon.html?chapter=${chapter.slug}`);
  };
  const byNumber = number => chapters.find(chapter => chapter.number === number);
  const esc = text => String(text).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
  const status = chapter => `<span class="status ${chapter.status === '완성' ? 'ready' : ''}">${chapter.status === '완성' ? '읽기 가능' : '준비 중'}</span>`;
  const label = chapter => `(${chapter.track === 'practice' ? '실습' : '이론'}) ${chapter.number != null ? chapter.number + (chapter.track === 'practice' ? '. ' : '장 · ') : ''}${chapter.title}`;
  const link = chapter => `<a href="${chapterUrl(chapter)}">${esc(label(chapter))} ${status(chapter)}</a>`;
  const selected = document.body.dataset.chapter === 'pending' ? new URLSearchParams(location.search).get('chapter') : document.body.dataset.chapter;
  const current = allChapters.find(chapter => chapter.slug === (document.body.dataset.practice || selected));
  const trackLinks = () => tracks.map(track => `<section><h3>${track.title}</h3><ol>${track.chapters.map(chapter => `<li>${link(chapter)}</li>`).join('')}</ol></section>`).join('') + `<p><a href="${url('practice/e2e.html')}">(실습) E2E 한눈에 보기</a></p>`;
  document.querySelectorAll('[data-chapter-count]').forEach(node => { node.textContent = chapters.filter(c => c.number && c.status === '완성').length; });
  document.querySelectorAll('[data-practice-count]').forEach(node => { node.textContent = practice.length; });
  document.querySelectorAll('[data-sim-count]').forEach(node => { node.textContent = (window.ReelsCatalog || []).length; });
  window.ReelsBook = Object.freeze({ chapters: Object.freeze(chapters), practice: Object.freeze(practice), tracks, url, chapterUrl, byNumber });

  document.querySelectorAll('[data-site-header]').forEach(header => {
    header.className = 'site-header';
    header.innerHTML = `<div class="header-inner"><a class="brand" href="${url('index.html')}"><span class="brand-mark" aria-hidden="true">r</span>ReelsBook</a><div class="header-actions"><a href="${url('index.html#contents')}">전체 목차</a><button type="button" data-menu-toggle aria-expanded="false" aria-controls="book-menu">목차</button><label><span class="sr-only">화면 테마</span><select class="theme-select" data-theme-select><option value="system">시스템</option><option value="light">라이트</option><option value="dark">다크</option></select></label><button type="button" data-theme-toggle aria-label="다크 모드 전환" aria-pressed="false">◐</button></div></div><nav id="book-menu" class="menu-panel" aria-label="전체 장" hidden>${trackLinks()}</nav>`;
    const toggle = header.querySelector('[data-menu-toggle]');
    const panel = header.querySelector('#book-menu');
    const close = () => { panel.hidden = true; toggle.setAttribute('aria-expanded', 'false'); };
    toggle.addEventListener('click', () => { panel.hidden = !panel.hidden; toggle.setAttribute('aria-expanded', String(!panel.hidden)); });
    header.addEventListener('keydown', event => { if (event.key === 'Escape' && !panel.hidden) { close(); toggle.focus(); } });
    panel.addEventListener('click', event => { if (event.target.closest('a')) close(); });
  });

  document.querySelectorAll('[data-chapter-toc]').forEach(toc => {
    toc.innerHTML = tracks.map(track => `<section class="toc-track" id="track-${track.id}"><h2>${track.title}</h2>${[...new Set(track.chapters.map(chapter => chapter.part))].map(part => `<section class="toc-part"><h3>${esc(part)}</h3><ol class="chapter-list">${track.chapters.filter(chapter => chapter.part === part).map(chapter => `<li><a href="${chapterUrl(chapter)}"><span class="chapter-num">${chapter.number != null ? String(chapter.number).padStart(2, '0') : '＋'}</span><span class="chapter-title">${esc(label(chapter))}<span class="chapter-deliverable">${esc(chapter.deliverable)}</span></span>${status(chapter)}</a></li>`).join('')}</ol></section>`).join('')}</section>`).join('') + `<p><a href="${url('practice/e2e.html')}">(실습) E2E 한눈에 보기 →</a></p>`;
  });
  document.querySelectorAll('[data-chapter-link]').forEach(anchor => {
    const chapter = byNumber(Number(anchor.dataset.chapterLink));
    if (chapter) { anchor.href = chapterUrl(chapter); if (chapter.status !== '완성') anchor.append(' · 준비 중'); }
  });
  if (current) {
    document.querySelectorAll('[data-chapter-title]').forEach(node => { node.textContent = label(current); });
    document.querySelectorAll('[data-chapter-kicker]').forEach(node => { node.textContent = `(${current.track === 'practice' ? '실습' : '이론'}) ${current.part}${current.number != null ? ' / ' + current.number : ''}`; });
    document.querySelectorAll('[data-chapter-meta]').forEach(meta => {
      const sequence = current.track === 'practice' ? practice : chapters;
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
      const sequence = current.track === 'practice' ? practice : chapters;
      const index = sequence.indexOf(current);
      const previous = sequence[index - 1], next = sequence[index + 1];
      pager.className = 'chapter-pager';
      pager.innerHTML = `${previous ? `<a href="${chapterUrl(previous)}"><small>← 이전 장</small>${esc(label(previous))} ${status(previous)}</a>` : `<a href="${url('index.html')}"><small>← 표지로</small>책의 전체 지도</a>`}${next ? `<a href="${chapterUrl(next)}"><small>다음 장 →</small>${esc(label(next))} ${status(next)}</a>` : `<a href="${url('index.html#contents')}"><small>목차로 →</small>다른 장 살펴보기</a>`}`;
    });
    document.title = `${label(current)} | ReelsBook`;
    document.querySelectorAll('.sidebar-chapters a').forEach(anchor => { if (new URL(anchor.href).pathname === location.pathname) anchor.setAttribute('aria-current', 'page'); });
    if (current.status !== '완성') document.title = `${current.title} · 준비 중 | ReelsBook`;
  }
  if (document.body.dataset.practice === 'e2e') {
    document.querySelectorAll('[data-book-sidebar]').forEach(sidebar => {
      sidebar.className = 'book-sidebar';
      sidebar.innerHTML = `<p class="sidebar-label">(실습) E2E 한눈에 보기</p><nav class="sidebar-chapters" aria-label="책의 두 트랙">${trackLinks()}</nav>`;
    });
  }
  document.querySelectorAll('[data-site-footer]').forEach(footer => {
    footer.className = 'site-footer';
    footer.innerHTML = `<span>ReelsBook · 작은 콘텐츠 작업실을 만드는 책</span><span><a href="${url('glossary.html')}">용어집</a> &nbsp; <a href="${url('credits.html')}">출처·크레딧</a></span>`;
  });

  // 저장소 접근 자체도 실패할 수 있다. 테마와 체크 상태 모두 읽기/쓰기를 보호한다.
  const storage = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); return true; } catch { return false; } }
  };
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let theme = storage.get('reelsbook:theme') || 'system';
  if (!['light', 'dark', 'system'].includes(theme)) theme = 'system';
  const applyTheme = () => {
    const dark = theme === 'dark' || (theme === 'system' && media.matches);
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    document.querySelectorAll('[data-theme-select]').forEach(select => { select.value = theme; });
    document.querySelectorAll('[data-theme-toggle]').forEach(button => { button.setAttribute('aria-pressed', String(dark)); button.setAttribute('aria-label', dark ? '라이트 모드로 전환' : '다크 모드로 전환'); });
  };
  const setTheme = value => { theme = value; storage.set('reelsbook:theme', theme); applyTheme(); };
  document.querySelectorAll('[data-theme-select]').forEach(select => select.addEventListener('change', () => setTheme(select.value)));
  document.querySelectorAll('[data-theme-toggle]').forEach(button => button.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark')));
  media.addEventListener('change', applyTheme);
  window.addEventListener('storage', event => {
    if (event.key !== 'reelsbook:theme') return;
    const savedTheme = storage.get('reelsbook:theme');
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
    const key = `reelsbook:checklist:${list.dataset.checklist}`;
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
