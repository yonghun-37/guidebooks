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
    "쇼츠 한 편이 만들어지기까지",
    "내 영상 제작 메모와 다음에 할 일",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    2,
    "02-revenue",
    "이론편",
    "쇼츠는 어떻게 보이고 무엇으로 돈이 되나",
    "내 수익 경로와 참고 계산",
    "약 15분",
    "입문",
    "완성"
  ],
  [
    3,
    "02b-ai-tools",
    "이론편",
    "AI 도구 지도",
    "내 제작 경로와 도구·파일·비용 메모",
    "약 15분",
    "입문",
    "완성"
  ],
  [
    4,
    "03-hook",
    "이론편",
    "기획: 첫 3초와 한 편의 구조",
    "좁힌 주제와 첫 문장 두 안, 시작·과정·결과 메모",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    5,
    "04-script",
    "이론편",
    "대본 쓰기와 AI 활용",
    "읽기 시간을 확인한 대본과 말·장면·자막 메모",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    6,
    "05-audio",
    "이론편",
    "소리: 내레이션·TTS·음악",
    "시험 녹음 비교와 소리 균형·음악 이용 조건 메모",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    7,
    "06-scenes",
    "이론편",
    "그림: 촬영·소재·AI 영상 생성",
    "촬영 장면과 소재 권리 메모",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    8,
    "07-editing",
    "이론편",
    "편집: 컷·리듬·전환",
    "컷·자막·소리 시간표",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    9,
    "08-captions",
    "이론편",
    "자막과 화면 글자",
    "읽기·가림·시간을 확인한 자막",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    10,
    "09-export",
    "이론편",
    "출력과 화질",
    "원본과 비교한 출력 설정 메모",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    11,
    "10-templates",
    "이론편",
    "자동화: 템플릿과 반복 제작",
    "다음 편에 재사용할 틀과 사람 검수표",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    12,
    "11-upload",
    "이론편",
    "업로드와 메타데이터",
    "제목·설명·공개 범위·표시 설정 메모",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    13,
    "12-analytics",
    "이론편",
    "분석: 숫자 읽기",
    "같은 기간으로 읽은 지표와 다음 수정 한 가지",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    14,
    "13-policy",
    "이론편",
    "정책·저작권·AI 표시·세금",
    "소재 권리·표시·수입 신고 확인 목록",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    15,
    "14-plan",
    "이론편",
    "30일 운영 계획",
    "제작 시간과 주간 점검을 나눈 30일 계획",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    null,
    "lab",
    "도구와 용어",
    "영상 실험실",
    "원본 도구로 비교한 제작 설정",
    "내 속도로",
    "입문",
    "완성"
  ],
  [
    null,
    "glossary",
    "도구와 용어",
    "용어집",
    "용어 뜻과 처음 설명한 장",
    "필요할 때",
    "입문",
    "완성"
  ]
];
  const chapters = chapterRows.map(([number, slug, part, title, deliverable, duration = '내 속도로', difficulty = '입문', status = '완성']) =>
    Object.freeze({ number, slug, part, title, deliverable, duration, difficulty, status, sample: slug === '02-revenue', track: 'theory' }));
  const practiceRows = [
  [
    "00-start",
    "시작 전에: 오늘 만들 쇼츠 고르기",
    "내 영상 유형·파일 폴더·오늘의 일정",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ],
  [
    "01-account",
    "계정·연습 채널·보안",
    "연습 채널과 계정 보호 설정",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ],
  [
    "02-setup",
    "ChatGPT와 편집기 준비",
    "무료 AI 대화창·편집 프로젝트·선택 키트",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ],
  [
    "03-script",
    "AI로 기획·대본 만들기",
    "검수한 내 대본·장면표·제목·설명",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ],
  [
    "04-voice",
    "내 목소리 또는 AI 음성 만들기",
    "재생 확인한 녹음/TTS 파일과 사용 조건 메모",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ],
  [
    "05-scenes",
    "촬영·스톡·AI로 장면 만들기",
    "내 장면 원본·샷 MP4·출처와 생성 이력",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ],
  [
    "06-edit",
    "편집과 AI 자동 자막",
    "말·장면·교정 자막이 맞는 편집 프로젝트",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ],
  [
    "07-export",
    "세로 출력·화질·AI 기록",
    "검수한 세로 MP4와 AI 사용 기록",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ],
  [
    "08-publish",
    "YouTube Studio로 첫 쇼츠 올리기",
    "첫 쇼츠와 공개 주소",
    "약 20분 + 처리 대기"
  ],
  [
    "09-api",
    "선택: Data API 업로드",
    "선택한 API 설정과 비공개 시험·전송 결과",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ],
  [
    "10-insights",
    "첫 숫자 읽고 다음 영상 고치기",
    "첫 기록표와 다음 영상의 수정 한 가지",
    "내 속도로 · 실습 0에서 전체 일정 선택"
  ]
];
  const practice = practiceRows.map(([slug, title, deliverable, duration], number) => Object.freeze({
    number, slug, title, deliverable, duration, track: 'practice', part: '실습편', difficulty: '입문', status: '완성', sample: number === 8
  }));
  practice.push(Object.freeze({number: null, slug: 'e2e', title: '한 편 완성 체크리스트', deliverable: '실습 확인 기록과 내 공개 주소', duration: '필요할 때', track: 'practice', part: '실습편', difficulty: '입문', status: '완성'}));
  const appendices = [
    ['prompts', '프롬프트 모음', '작업별 복사 지시문과 좋은·나쁜 예'],
    ['ai-models', 'AI 모델·사용처·비용 총정리', '모델 검색과 한 편 비용 비교'],
    ['credits', '출처·크레딧', '본문에서 실제 인용한 원문과 제작 고지']
  ].map(([slug, title, deliverable]) => Object.freeze({number: null, slug, title, deliverable, duration: '필요할 때', track: 'appendix', part: '부록', difficulty: '입문', status: '완성'}));
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
    return url(`${chapter.track === 'practice' ? 'practice' : 'chapters'}/${chapter.slug}.html`);
  };
  const byNumber = number => chapters.find(chapter => chapter.number === number);
  const esc = text => String(text).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
  const status = chapter => `<span class="status ready">${esc(chapter.status)}</span>`;
  const label = chapter => `(${chapter.track === 'practice' ? '실습' : chapter.track === 'appendix' ? '부록' : '이론'}) ${chapter.number != null ? chapter.number + (chapter.track === 'practice' ? '. ' : '장 · ') : ''}${chapter.title}`;
  const link = chapter => `<a href="${chapterUrl(chapter)}">${esc(label(chapter))} ${status(chapter)}</a>`;
  const selected = (document.body.dataset.chapter === 'pending' || document.body.dataset.practice === 'pending') ? new URLSearchParams(location.search).get('chapter') : document.body.dataset.chapter || document.body.dataset.appendix;
  const current = allChapters.find(chapter => chapter.slug === (document.body.dataset.practice && document.body.dataset.practice !== 'pending' ? document.body.dataset.practice : selected));
  if (current && (document.body.dataset.chapter === 'pending' || document.body.dataset.practice === 'pending')) {
    location.replace(chapterUrl(current));
    return;
  }
  const trackLinks = () => tracks.map(track => `<section><h3>${track.title}</h3><ol>${track.chapters.map(chapter => `<li>${link(chapter)}</li>`).join('')}</ol></section>`).join('');
  document.querySelectorAll('[data-chapter-count]').forEach(node => { node.textContent = chapters.filter(chapter => chapter.number !== null).length; });
  document.querySelectorAll('[data-practice-count]').forEach(node => { node.textContent = practice.filter(chapter => chapter.number !== null).length; });
  document.querySelectorAll('[data-sim-count]').forEach(node => { node.textContent = (window.ShortsCatalog || []).length; });
  window.ShortsBook = Object.freeze({ chapters: Object.freeze(chapters), practice: Object.freeze(practice), tracks, url, chapterUrl, byNumber });

  document.querySelectorAll('[data-site-header]').forEach(header => {
    header.className = 'site-header';
    header.innerHTML = `<div class="header-inner"><a class="brand" href="${url('index.html')}"><span class="brand-mark" aria-hidden="true">s</span>ShortsBook</a><div class="header-actions"><a href="${url('index.html#contents')}">전체 목차</a><button type="button" data-menu-toggle aria-expanded="false" aria-controls="book-menu">목차</button><label><span class="sr-only">화면 테마</span><select class="theme-select" data-theme-select><option value="system">시스템</option><option value="light">라이트</option><option value="dark">다크</option></select></label><button type="button" data-theme-toggle aria-label="다크 모드 전환" aria-pressed="false">◐</button></div></div><nav id="book-menu" class="menu-panel" aria-label="전체 장" hidden>${trackLinks()}</nav>`;
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
    document.title = `${label(current)} | ShortsBook`;
    document.querySelectorAll('.sidebar-chapters a').forEach(anchor => { if (new URL(anchor.href).pathname + new URL(anchor.href).search === location.pathname + location.search) anchor.setAttribute('aria-current', 'page'); });

  }
  document.querySelectorAll('[data-site-footer]').forEach(footer => {
    footer.className = 'site-footer';
    footer.innerHTML = `<span>ShortsBook · 영상 제작에 집중한 쇼츠 입문서</span><span><a href="${url('glossary.html')}">용어집</a> &nbsp; <a href="${url('prompts.html')}">프롬프트</a> &nbsp; <a href="${url('ai-models.html')}">모델·비용</a> &nbsp; <a href="${url('credits.html')}">출처·크레딧</a></span>`;
  });

  // 저장소 접근 자체도 실패할 수 있다. 테마와 체크 상태 모두 읽기/쓰기를 보호한다.
  const storage = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); return true; } catch { return false; } }
  };
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let theme = storage.get('shortsbook:theme') || 'system';
  if (!['light', 'dark', 'system'].includes(theme)) theme = 'system';
  const applyTheme = () => {
    const dark = theme === 'dark' || (theme === 'system' && media.matches);
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    document.querySelectorAll('[data-theme-select]').forEach(select => { select.value = theme; });
    document.querySelectorAll('[data-theme-toggle]').forEach(button => { button.setAttribute('aria-pressed', String(dark)); button.setAttribute('aria-label', dark ? '라이트 모드로 전환' : '다크 모드로 전환'); });
  };
  const setTheme = value => { theme = value; storage.set('shortsbook:theme', theme); applyTheme(); };
  document.querySelectorAll('[data-theme-select]').forEach(select => select.addEventListener('change', () => setTheme(select.value)));
  document.querySelectorAll('[data-theme-toggle]').forEach(button => button.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark')));
  media.addEventListener('change', applyTheme);
  window.addEventListener('storage', event => {
    if (event.key !== 'shortsbook:theme') return;
    const savedTheme = storage.get('shortsbook:theme');
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
    const key = `shortsbook:checklist:${list.dataset.checklist}`;
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
