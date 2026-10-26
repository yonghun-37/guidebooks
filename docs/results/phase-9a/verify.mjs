// 저장소 루트를 http.server 8541로 제공한 뒤 실행합니다.
import { chromium } from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base = process.env.SITE_URL || 'http://127.0.0.1:8541/';
const out = 'docs/results/phase-9a/';
const files = ['01-map', '02-formats', '03-revenue', '04-niche'];
const checks = [], errors = [], responses = [];
const check = (name, value) => { assert.ok(value, name); checks.push(name); };
const browser = await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome', headless:true, args:['--no-sandbox']});
const context = await browser.newContext({reducedMotion:'reduce'});
await context.route('https://cdn.jsdelivr.net/**', route => route.fulfill({contentType:'text/css',body:''}));
const page = await context.newPage();
page.on('pageerror', error => errors.push(String(error)));
page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
page.on('response', response => { if (response.url().startsWith(base) && response.status() >= 400) responses.push({url:response.url(),status:response.status()}); });
try {
  for (const width of [1280,375,360]) {
    await page.setViewportSize({width,height:1000});
    for (const slug of files) {
      await page.goto(base + `site/chapters/${slug}.html`,{waitUntil:'networkidle'});
      const key = `${slug}/${width}`;
      check(key+' overflow',await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      check(key+' nine blocks',await page.locator('[data-block]').count() === 9);
      check(key+' four axes',await page.locator('.axis-block').count() === 4);
      check(key+' repeated rows',await page.locator('.axis-rows > div').count() === 24);
      check(key+' five FAQs',await page.locator('.chapter-faq details').count() === 5);
      check(key+' three takeaways',await page.locator('.key-takeaways > li').count() === 3);
      await page.locator('.axis-card').first().focus();
      await page.keyboard.press('Enter');
      check(key+' axis keyboard focus',await page.evaluate(() => document.activeElement.id === location.hash.slice(1)));
      await page.locator('#faq-1 summary').focus();
      await page.keyboard.press('Enter');
      check(key+' FAQ keyboard',await page.locator('#faq-1').getAttribute('open') !== null);
      await page.evaluate(() => document.querySelectorAll('.chapter-faq details').forEach(d => d.open = true));
      check(key+' FAQ open overflow',await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      if (width !== 360) {
        await page.evaluate(() => {document.querySelectorAll('.chapter-faq details').forEach(d => d.open = false); scrollTo({top:0,behavior:'instant'});});
        await page.screenshot({path:out+`${slug}-${width}.png`,fullPage:true});
      }
      const result = page.locator('[data-sim-result]');
      if(slug === '01-map') {
        check(key+' default budget',(await result.textContent()).startsWith('6편 ·'));
        await page.locator('#available').fill('60');
        check(key+' equal overhead',(await result.textContent()).startsWith('0편 ·'));
        await page.locator('#per-post').fill('0');
        check(key+' zero denominator rejected',(await result.textContent()).includes('입력하세요'));
        await page.locator('#per-post').fill('60');
        await page.locator('#overhead').fill('');
        check(key+' blank rejected',(await result.textContent()).includes('입력하세요'));
        await page.locator('#overhead').fill('60');
      } else if(slug === '02-formats') {
        check(key+' default cards',(await result.textContent()).startsWith('5장 ·'));
        await page.locator('#points').focus();
        await page.keyboard.press('End');
        check(key+' keyboard maximum',(await result.textContent()).startsWith('20장 ·'));
        await page.keyboard.press('Home');
        check(key+' keyboard minimum',(await result.textContent()).startsWith('2장 ·'));
      } else if(slug === '03-revenue') {
        check(key+' one purchase',(await result.textContent()).startsWith('1,500원 ·'));
        await page.locator('#sales').fill('20');
        check(key+' twenty purchases',(await result.textContent()).startsWith('30,000원 ·'));
        await page.locator('#sales').fill('');
        check(key+' blank purchase rejected',(await result.textContent()).includes('입력하세요'));
        await page.locator('#sales').fill('1.5');
        check(key+' fractional purchase rejected',(await result.textContent()).includes('입력하세요'));
        await page.locator('#sales').fill('-1');
        check(key+' negative purchase rejected',(await result.textContent()).includes('입력하세요'));
        check(key+' stage table',await page.locator('.stage-table tbody tr').count() === 5);
        if(width === 375) {
          await page.locator('#stages').scrollIntoViewIfNeeded();
          await page.screenshot({path:out+'03-stages-375.png'});
        }
      } else {
        check(key+' empty plan',(await result.textContent()).startsWith('0개 ·'));
        await page.locator('[data-plan]').first().focus();
        await page.keyboard.press('Space');
        check(key+' keyboard checkbox',(await result.textContent()).startsWith('1개 ·'));
        await page.locator('[data-all]').click();
        check(key+' all plan',(await result.textContent()).startsWith('3개 ·'));
      }
      await page.locator('[data-zero]').focus();
      await page.keyboard.press('Enter');
      check(key+' extreme preset',/^(0편|2장|0원|0개) ·/.test(await result.textContent()));
      for (const question of await page.locator('[data-question]').all()) {
        await question.locator('[data-correct=false]').first().click();
        check(key+' wrong feedback',await question.locator('[data-feedback]').isVisible());
      }
      await page.locator('[data-quiz-reset]').click();
      for (const question of await page.locator('[data-question]').all()) {
        await question.locator('[data-correct=true]').click();
        check(key+' correct feedback',await question.locator('[data-feedback]').isVisible());
      }
      check(key+' quiz score',(await page.locator('[data-quiz-score]').textContent()).includes('3문항 정답'));
      await page.locator('[data-quiz-reset]').click();
      check(key+' quiz reset',(await page.locator('[data-quiz-score]').textContent()).includes('0문항 풀이'));
      await page.goto(base+`site/chapters/${slug}.html#faq-5`);
      check(key+' direct FAQ fragment',await page.locator('#faq-5').getAttribute('open') !== null);
      const opened = await page.locator('.chapter-faq details[open]').count();
      await page.evaluate(() => dispatchEvent(new Event('beforeprint')));
      check(key+' FAQ print open',await page.locator('.chapter-faq details[open]').count() === 5);
      await page.evaluate(() => dispatchEvent(new Event('afterprint')));
      check(key+' FAQ print restore',await page.locator('.chapter-faq details[open]').count() === opened);
      await page.locator('[data-theme-select]').selectOption('dark');
      check(key+' dark overflow',await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      if(width === 360 && slug === '03-revenue') {
        await page.locator('#principle').scrollIntoViewIfNeeded();
        await page.screenshot({path:out+'03-revenue-dark-360.png'});
      }
      await page.locator('[data-theme-select]').selectOption('light');
    }
  }
  for (const [slug, id] of [['01-map','pipeline-map'],['01-map','time-budget'],['02-formats','concept-figure'],['02-formats','signal-sim'],['03-revenue','concept-figure'],['03-revenue','ledger-sim'],['04-niche','concept-figure'],['04-niche','niche-sim']]) {
    await page.goto(base+`site/chapters/${slug}.html?embed=${id}`);
    check(slug+'/'+id+' embed block',await page.locator('.chapter-block:not([hidden])').count() === 1);
    check(slug+'/'+id+' embed target visible',await page.locator('#'+id).evaluate(el => !el.closest('[hidden]')));
  }
  const nojs = await browser.newContext({javaScriptEnabled:false});
  await nojs.route('https://cdn.jsdelivr.net/**', route => route.fulfill({contentType:'text/css',body:''}));
  const plain = await nojs.newPage();
  for(const slug of files) {
    await plain.goto(base+`site/chapters/${slug}.html`);
    await plain.locator('.axis-card').first().click();
    check(slug+' no-JS navigation',plain.url().includes('#'));
    await plain.locator('#faq-1 summary').click();
    check(slug+' no-JS FAQ',await plain.locator('#faq-1').getAttribute('open') !== null);
    check(slug+' no-JS answers',await plain.locator('noscript details').count() === 1);
  }
  await nojs.close();
  check('console/page errors zero',errors.length === 0);
  check('local HTTP errors zero',responses.length === 0);
  await fs.writeFile(out+'browser-check.json',JSON.stringify({pages:4,widths:[1280,375,360],checks:checks.length,errors,responses,passed:checks,externalFonts:'빈 CSS로 대체',browser:'Chromium 1228 headless'},null,2)+'\n');
  console.log(JSON.stringify({checks:checks.length,errors,responses}));
} finally {await browser.close();}
