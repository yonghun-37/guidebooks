// 저장소 루트에서 node docs/results/phase-9/verify.mjs. 저장소 루트를 8539에서 제공한다.
import { chromium } from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base = process.env.SITE_URL || 'http://127.0.0.1:8539/';
const out = 'docs/results/phase-9/';
const browser = await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome', headless:true, args:['--no-sandbox']});
const context = await browser.newContext({reducedMotion:'reduce'});
await context.route('https://cdn.jsdelivr.net/**', route => route.fulfill({contentType:'text/css',body:''}));
const page = await context.newPage();
const errors = [], checks = [];
page.on('pageerror', error => errors.push(String(error)));
page.on('console', message => { if(message.type() === 'error') errors.push(message.text()); });
const check = (name, value) => { assert.ok(value, name); checks.push(name); };
const template = 'docs/chapter-template-v2.html';
const existing = [
  ...(await fs.readdir('site/chapters')).filter(name => /^\d\d-.*\.html$/.test(name)).map(name => 'site/chapters/' + name),
  ...(await fs.readdir('site/practice')).filter(name => /^\d\d-.*\.html$/.test(name)).map(name => 'site/practice/' + name),
  'site/index.html', 'site/lab.html', 'site/glossary.html', 'site/credits.html', 'site/practice/e2e.html',
  'site/drafts/index.html', 'site/drafts/ch03-a-axes.html', 'site/drafts/ch03-b-faq.html', 'site/drafts/ch03-c-journey.html'
];
try {
  for(const width of [1280, 375, 360]) {
    await page.setViewportSize({width,height:1000});
    for(const file of [template, ...existing]) {
      await page.goto(base + file, {waitUntil:'networkidle'});
      check(`${width} ${file} 가로 넘침 없음`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      if(file === template) {
        check(`${width} 템플릿 9블록`, await page.locator('[data-block]').count() === 9);
        check(`${width} 축 3개 고정 6줄`, await page.locator('.axis-rows > div').count() === 18);
        check(`${width} FAQ 5개`, await page.locator('.chapter-faq details').count() === 5);
        await page.locator('.axis-card').first().focus();
        await page.keyboard.press('Enter');
        await page.waitForTimeout(200);
        check(`${width} 카드 키보드 절 이동·초점`, await page.evaluate(() => location.hash === '#axis-reader' && document.activeElement.id === 'axis-reader'));
        await page.locator('#faq-first summary').focus();
        await page.keyboard.press('Enter');
        check(`${width} FAQ 키보드 펼치기`, await page.locator('#faq-first').getAttribute('open') !== null);
        await page.keyboard.press('Enter');
        check(`${width} FAQ 키보드 접기`, await page.locator('#faq-first').getAttribute('open') === null);
        await page.locator('#plan-reader').check();
        check(`${width} 도구 1개 결과`, (await page.locator('[data-sim-result]').textContent()).startsWith('1개'));
        await page.locator('#plan-message').check();
        await page.locator('#plan-action').check();
        check(`${width} 도구 극단값 3개 결과`, (await page.locator('[data-sim-result]').textContent()).startsWith('3개'));
        await page.locator('[data-question] [data-correct=true]').first().click();
        check(`${width} 기존 퀴즈 엔진`, (await page.locator('[data-quiz-score]').textContent()).includes('1문항 정답'));
        await page.locator('[data-quiz-reset]').click();
        check(`${width} 기존 퀴즈 초기화`, (await page.locator('[data-quiz-score]').textContent()).includes('0문항 풀이'));
        await page.evaluate(() => window.scrollTo({top:document.querySelector('#question').offsetTop-90,behavior:'instant'}));
        if(width !== 360) await page.screenshot({path:out + `template-${width}.png`});
      }
    }
  }
  await page.goto(base + template + '#faq-answer');
  check('FAQ 직접 링크 펼침', await page.locator('#faq-answer').getAttribute('open') !== null);
  await page.evaluate(() => { location.hash = '#faq-action'; });
  await page.waitForTimeout(100);
  check('FAQ hashchange 펼침', await page.locator('#faq-action').getAttribute('open') !== null);
  const previousOpen = await page.locator('.chapter-faq details[open]').count();
  await page.evaluate(() => dispatchEvent(new Event('beforeprint')));
  check('인쇄 시 FAQ 전부 펼침', await page.locator('.chapter-faq details[open]').count() === 5);
  await page.evaluate(() => dispatchEvent(new Event('afterprint')));
  check('인쇄 후 FAQ 원래 상태 복원', await page.locator('.chapter-faq details[open]').count() === previousOpen);
  await page.evaluate(() => document.querySelector('[data-theme-select]').value = 'dark');
  await page.locator('[data-theme-select]').dispatchEvent('change');
  check('다크 모드', await page.evaluate(() => document.documentElement.dataset.theme === 'dark'));
  await page.locator('#question').scrollIntoViewIfNeeded();
  await page.screenshot({path:out + 'template-dark-360.png'});
  // 복사된 장의 실제 내비 통합도 확인한다. HTML 파일은 수정하지 않는다.
  await page.route('**/site/chapters/01-map.html', async route => {
    const html = (await fs.readFile(template, 'utf8')).replaceAll('../site/assets/', '../assets/').replaceAll('../site/practice/', '../practice/').replace('data-chapter="REPLACE-SLUG"','data-chapter="01-map"');
    await route.fulfill({contentType:'text/html',body:html});
  });
  await page.goto(base + 'site/chapters/01-map.html');
  check('등록된 장 9블록 목차 통합', await page.locator('[data-mobile-outline] nav a').count() === 9);
  check('FAQ 목차 이름', (await page.locator('[data-mobile-outline]').textContent()).includes('자주 묻는 질문'));
  await page.unroute('**/site/chapters/01-map.html');
  const nojs = await browser.newContext({javaScriptEnabled:false});
  await nojs.route('https://cdn.jsdelivr.net/**', route => route.fulfill({contentType:'text/css',body:''}));
  const plain = await nojs.newPage();
  await plain.goto(base + template);
  await plain.locator('.axis-card').first().click();
  check('JS 없이 카드 절 이동', plain.url().endsWith('#axis-reader'));
  await plain.locator('#faq-first summary').click();
  check('JS 없이 FAQ 펼침', await plain.locator('#faq-first').getAttribute('open') !== null);
  await plain.locator('#faq-first summary').click();
  await plain.emulateMedia({media:'print'});
  check('JS 없이 인쇄 시 접힌 FAQ 보임', await plain.locator('#faq-first .faq-answer').isVisible());
  await nojs.close();
  check('콘솔·페이지 오류 없음', errors.length === 0);
  await fs.writeFile(out + 'browser-check.json', JSON.stringify({pages:existing.length+1,widths:[1280,375,360],checks:checks.length,errors,passed:checks},null,2)+'\n');
  console.log(JSON.stringify({pages:existing.length+1,checks:checks.length,errors}));
} finally {
  await browser.close();
}
