/** Phase 3 브라우저 회귀 검증. 별도 설치한 playwright-core와 Chromium을 인자로 받는다.
 * node docs/results/phase-3/verify.mjs /path/to/playwright-core/index.mjs /path/to/chrome
 * 먼저 python3 -m http.server 8765 --bind 127.0.0.1 --directory site 실행.
 * 사이트의 런타임·빌드 의존성은 추가하지 않는다.
 */
import assert from 'node:assert/strict';
import { writeFile, readFile, readdir } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
const { chromium } = await import(pathToFileURL(process.argv[2]).href);
const base = 'http://127.0.0.1:8765/';
const out = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch({ executablePath: process.argv[3], headless: true, args: ['--no-sandbox'] });
const errors = [], failures = [], checks = [], widths = [], localLinks = new Set();
const check = (name, result = true) => { assert.ok(result, name); checks.push(name); };
const watch = page => {
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  page.on('requestfailed', request => failures.push({ url: request.url(), reason: request.failure()?.errorText }));
};
const dimensions = page => page.evaluate(() => ({ viewport: innerWidth, client: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth }));
try {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: 'light', reducedMotion: 'reduce' });
  const page = await context.newPage(); watch(page);
  for (const width of [1280, 375, 360]) {
    await page.setViewportSize({ width, height: width < 600 ? 812 : 900 });
    for (const route of ['index.html', 'chapters/01-map.html', 'chapters/coming-soon.html?chapter=02-formats', 'lab.html', 'glossary.html', 'credits.html']) {
      await page.goto(base + route); await page.evaluate(() => document.fonts.ready);
      const size = await dimensions(page); widths.push({ route, ...size });
      check(`no horizontal overflow: ${route} @${width}`, size.scroll === size.client);
      for (const href of await page.locator('a[href]').evaluateAll(anchors => anchors.map(a => a.href))) if (href.startsWith(base)) localLinks.add(href);
      if ([1280, 375].includes(width) && ['index.html', 'chapters/01-map.html'].includes(route)) {
        const name = `${width === 1280 ? 'desktop' : 'mobile'}-${route === 'index.html' ? 'cover' : 'chapter'}`;
        await page.screenshot({ path: path.join(out, `${name}.png`) });
        if (route === 'chapters/01-map.html') {
          await page.locator('#map').evaluate(n => n.scrollIntoView({ block: 'start' }));
          await page.screenshot({ path: path.join(out, `${width === 1280 ? 'desktop' : 'mobile'}-pipeline.png`) });
        }
      }
    }
  }
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(base + 'chapters/01-map.html');
  check('nine blocks in chapter, in order', JSON.stringify(await page.locator('[data-block]').evaluateAll(nodes => nodes.map(n => n.dataset.block))) === JSON.stringify(['question','figure','principle','simulator','case','workshop','story','summary','quiz']));
  const chapterData = await page.evaluate(() => ReelsBook.chapters);
  check('single dataset: 16 chapters plus credits, only chapter 1 complete', chapterData.length === 17 && chapterData.filter(c => c.status === '완성').length === 1);
  for (const chapter of chapterData) {
    const href = await page.evaluate(slug => ReelsBook.chapterUrl(ReelsBook.chapters.find(c => c.slug === slug)), chapter.slug);
    localLinks.add(href);
  }
  for (const [step, title] of [['source','소재'],['copy','문안'],['make','카드/릴스'],['review','검수'],['publish','게시'],['analyze','분석'],['revenue','수익']]) {
    await page.locator(`[data-step="${step}"]`).click();
    check(`map detail, tools, budget, related links: ${step}`, (await page.locator('[data-pipeline-detail] h3').textContent()).startsWith(title) && await page.locator('[data-pipeline-detail] dd').count() === 2 && await page.locator('[data-pipeline-detail] a').count() >= 1);
    check(`one pressed pipeline button: ${step}`, await page.locator('.pipeline [aria-pressed="true"]').count() === 1);
    for (const href of await page.locator('[data-pipeline-detail] a').evaluateAll(a => a.map(n => n.href))) localLinks.add(href);
  }
  await page.locator('[data-step="source"]').focus(); await page.keyboard.press('ArrowRight');
  check('map ArrowRight changes focus and detail', await page.locator('[data-step="copy"]').evaluate(n => n === document.activeElement && n.getAttribute('aria-pressed') === 'true'));
  await page.keyboard.press('End'); check('map End key', await page.locator('[data-step="revenue"]').evaluate(n => n === document.activeElement));
  await page.keyboard.press('Home'); await page.keyboard.press('Enter'); check('map Home/Enter', await page.locator('[data-step="source"]').getAttribute('aria-pressed') === 'true');
  for (const [hours, expected] of [[0,0],[0.5,0],[1,0],[1.5,2],[3,8],[5,17]]) {
    await page.locator('#weekly-hours').evaluate((input, value) => { input.value = value; input.dispatchEvent(new Event('input', { bubbles: true })); }, hours);
    check(`budget ${hours}h = ${expected} posts`, await page.locator('[data-post-count]').textContent() === String(expected));
    check(`budget result text ${hours}h`, (await page.locator('#time-budget [data-sim-result]').textContent()).includes(`게시물 ${expected}개`));
  }
  await page.locator('#weekly-hours').focus(); await page.keyboard.press('ArrowLeft');
  check('range native keyboard updates output', await page.locator('[data-weekly-hours]').textContent() === '주 4.5시간' && await page.locator('[data-post-count]').textContent() === '15');
  await page.locator('[data-check="audience"]').check(); await page.reload();
  check('checklist restored after reload', await page.locator('[data-check="audience"]').isChecked());
  const questions = page.locator('[data-question]');
  await questions.nth(0).locator('[data-correct="false"]').first().click();
  check('quiz wrong answer explanation and explicit correct answer', (await questions.nth(0).locator('[data-feedback]').textContent()).includes('정답: B.') && await questions.nth(0).locator('button:disabled').count() === 3);
  await questions.nth(1).locator('[data-correct="true"]').click();
  check('quiz correct answer and score', (await page.locator('[data-quiz-score]').textContent()).includes('2문항 풀이 · 1문항 정답'));
  await page.locator('[data-quiz-reset]').click();
  check('quiz reset', await page.locator('[data-question] button:disabled').count() === 0 && (await page.locator('[data-quiz-score]').textContent()).includes('0문항 풀이'));
  for (let i = 0; i < 4; i += 1) await questions.nth(i).locator('[data-correct="true"]').click();
  check('all four quiz answers and explanations', (await page.locator('[data-quiz-score]').textContent()).includes('4문항 풀이 · 4문항 정답'));
  await page.locator('[data-theme-select]').selectOption('system'); await page.emulateMedia({ colorScheme: 'dark' }); await page.waitForFunction(() => document.documentElement.dataset.theme === 'dark');
  check('theme follows system dark', await page.locator('html').getAttribute('data-theme') === 'dark');
  await page.locator('[data-theme-toggle]').click();
  check('theme toggle overrides system', await page.locator('html').getAttribute('data-theme') === 'light');
  await page.reload(); check('manual theme survives reload', await page.locator('html').getAttribute('data-theme') === 'light');
  await page.locator('[data-theme-select]').selectOption('system');
  check('theme can return to system', await page.locator('html').getAttribute('data-theme') === 'dark');
  await page.setViewportSize({ width: 375, height: 812 });
  check('dark mobile no overflow', (await dimensions(page)).scroll === 375);
  await page.locator('#time-budget').evaluate(n => n.scrollIntoView({ block: 'start' })); await page.screenshot({ path: path.join(out, 'mobile-dark-budget.png') });
  await page.locator('[data-menu-toggle]').click(); check('mobile menu opens', await page.locator('#book-menu').isVisible());
  await page.keyboard.press('Escape'); check('menu Escape closes and restores focus', !await page.locator('#book-menu').isVisible() && await page.locator('[data-menu-toggle]').evaluate(n => n === document.activeElement));
  await page.locator('a[data-term]').first().focus();
  check('term tooltip keyboard focus', await page.locator('.term-tip').first().evaluate(n => getComputedStyle(n).visibility === 'visible'));
  await page.keyboard.press('Escape'); check('term tooltip Escape dismisses', await page.locator('.term-tip').first().getAttribute('hidden') !== null);
  await page.locator('a[data-term]').first().blur();
  await page.emulateMedia({ media: 'print' }); check('print hides simulators', await page.locator('#time-budget').evaluate(n => getComputedStyle(n).display === 'none')); await page.emulateMedia({ media: 'screen' });
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  await page.locator('.copy-button').click();
  await page.waitForFunction(() => document.querySelector('.copy-status').textContent.includes('복사했습니다'));
  check('copy success', (await page.locator('.copy-status').textContent()).includes('복사했습니다'));
  check('clipboard exact memo content', await page.evaluate(async () => (await navigator.clipboard.readText()) === document.querySelector('.code-box code').textContent));
  await page.evaluate(() => { Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: () => Promise.reject(new Error('test denied')) } }); });
  await page.locator('.copy-button').click();
  check('clipboard denied: selectable fallback', (await page.locator('.copy-status').textContent()).includes('직접 복사') && await page.evaluate(() => getSelection().toString().includes('나의 작은 작업실')));
  // 모든 생성 내비의 실제 파일·앵커를 확인한다. 준비 중 장도 URL로 방문할 수 있어야 한다.
  for (const href of localLinks) {
    const target = new URL(href);
    const response = await context.request.get(target.href);
    assert.equal(response.status(), 200, href);
    if (target.hash) {
      const html = await response.text();
      const valid = await page.evaluate(({ html, id }) => { const doc = new DOMParser().parseFromString(html, 'text/html'); return !!doc.getElementById(id); }, { html, id: decodeURIComponent(target.hash.slice(1)) });
      assert.ok(valid, `missing anchor ${href}`);
    }
  }
  check(`${localLinks.size} unique local links/anchors return 200 and resolve`);
  await page.goto(base + 'chapters/coming-soon.html?chapter=02-formats');
  check('pending chapter title and next navigation from data', await page.locator('h1').textContent() === chapterData[1].title && (await page.locator('[data-chapter-pager]').textContent()).includes(chapterData[2].title));
  // 저장 API 읽기/쓰기 모두 차단해도 공통 기능과 시뮬레이터가 작동한다.
  const blocked = await browser.newContext({ viewport: { width: 375, height: 812 } });
  await blocked.addInitScript(() => { Storage.prototype.getItem = () => { throw new DOMException('blocked', 'SecurityError'); }; Storage.prototype.setItem = () => { throw new DOMException('blocked', 'SecurityError'); }; });
  const blockedPage = await blocked.newPage(); watch(blockedPage); await blockedPage.goto(base + 'chapters/01-map.html');
  await blockedPage.locator('[data-check="budget"]').check();
  check('storage denied: checkbox still changes with message', await blockedPage.locator('[data-check="budget"]').isChecked() && (await blockedPage.locator('[data-save-status]').textContent()).includes('저장할 수 없는'));
  await blockedPage.locator('[data-theme-toggle]').click(); check('storage denied: theme still toggles', await blockedPage.locator('html').getAttribute('data-theme') === 'dark');
  check('storage denied: simulator still runs', await blockedPage.locator('[data-post-count]').textContent() === '17');
  await blocked.close();
  // 저장 JSON 손상도 장 로딩을 막지 않는다.
  await page.evaluate(() => localStorage.setItem('reelsbook:checklist:01-map-output', '{bad-json'));
  await page.goto(base + 'chapters/01-map.html'); check('corrupt stored JSON recovers', await page.locator('[data-check="audience"]').isChecked() === false && await page.locator('.copy-button').count() === 1);
  const offline = await browser.newContext({ javaScriptEnabled: false });
  const staticPage = await offline.newPage(); await staticPage.goto(base + 'chapters/01-map.html');
  check('no JS: chapter body and fallback quiz readable', await staticPage.locator('[data-block]').count() === 9 && await staticPage.locator('noscript details').count() === 1);
  await offline.close();
  // 직접 파일 열기에서 경로 계산과 장 기능이 유지되는지 확인한다.
  const filePage = await context.newPage(); watch(filePage);
  await filePage.goto(pathToFileURL(path.resolve('site/chapters/01-map.html')).href);
  check('file protocol: navigation and simulator work', (await filePage.locator('[data-chapter-pager] a').first().getAttribute('href')).startsWith('file:') && await filePage.locator('[data-post-count]').textContent() === '17');
  await filePage.close();
  // 템플릿도 실제 공통 엔진으로 읽고 세 문항을 푼다 (정적 서버의 루트를 바꾸지 않고 file로 접근).
  const template = await context.newPage(); watch(template);
  await template.goto(pathToFileURL(path.resolve('docs/chapter-template.html')).href);
  check('template has all nine blocks', await template.locator('[data-block]').count() === 9);
  await template.locator('[data-question] [data-correct="true"]').nth(0).click();
  check('template quiz engine works', (await template.locator('[data-quiz-score]').textContent()).includes('1문항 정답'));
  await template.close();
  // 정적 문서 구조: 모든 HTML에 lang/title/viewport/main, 중복 ID 없음.
  const files = ['site/index.html', 'site/lab.html', 'site/glossary.html', 'site/credits.html', 'site/chapters/01-map.html', 'site/chapters/coming-soon.html', 'docs/chapter-template.html'];
  for (const file of files) {
    const html = await readFile(file, 'utf8');
    const issues = await page.evaluate(html => { const doc = new DOMParser().parseFromString(html, 'text/html'); const ids = [...doc.querySelectorAll('[id]')].map(n => n.id); return { lang: doc.documentElement.lang, title: !!doc.title, viewport: !!doc.querySelector('meta[name="viewport"]'), main: doc.querySelectorAll('main').length, duplicate: ids.length !== new Set(ids).size }; }, html);
    assert.deepEqual(issues, { lang: 'ko', title: true, viewport: true, main: 1, duplicate: false }, file);
  }
  check('seven HTML documents: lang, title, viewport, one main, unique IDs');
  check('console/page errors absent', errors.length === 0);
  check('failed network requests absent', failures.length === 0);
  await writeFile(path.join(out, 'verification.json'), JSON.stringify({ testedAt: new Date().toISOString(), browser: await browser.version(), checks, widths, localLinkCount: localLinks.size, errors, failedRequests: failures, screenshots: (await readdir(out)).filter(file => file.endsWith('.png')) }, null, 2) + '\n');
  console.log(JSON.stringify({ passed: checks.length, localLinks: localLinks.size, errors, failures }, null, 2));
} catch (error) {
  console.error(error);
  await writeFile(path.join(out, 'verification-failure.json'), JSON.stringify({ message: error.message, checks, widths, errors, failures }, null, 2));
  process.exitCode = 1;
} finally { await browser.close(); }
