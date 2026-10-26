import { writeFile } from 'node:fs/promises';
import { strict as assert } from 'node:assert';
const { chromium } = await import(process.argv[2] || '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs');
const executablePath = process.argv[3] || '/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome';
const base = process.env.SITE_URL || 'http://127.0.0.1:8765';
const browser = await chromium.launch({ executablePath, headless: true, args: ['--no-sandbox'] });
const slugs = ['02-formats', '03-revenue', '04-niche', '05-sources'];
const reports = [];
const errors = [];
const links = new Set();
const blockNames = ['question','figure','principle','simulator','case','workshop','story','summary','quiz'];
try {
  for (const width of [1280,375]) {
    for (const [index,slug] of slugs.entries()) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      page.on('pageerror', error => errors.push(`${slug}/${width}: ${error.message}`));
      page.on('console', message => { if (message.type() === 'error') errors.push(`${slug}/${width}: ${message.text()}`); });
      await page.goto(`${base}/chapters/${slug}.html`, {waitUntil:'networkidle'});
      await page.evaluate(() => document.fonts.ready);
      assert.deepEqual(await page.locator('[data-block]').evaluateAll(nodes => nodes.map(n=>n.dataset.block)), blockNames);
      assert.equal(await page.locator('[data-question]').count(),4);
      assert.equal(await page.locator('.simulator').count(),2);
      const duplicateIds = await page.locator('[id]').evaluateAll(nodes=>nodes.map(n=>n.id).filter((id,i,ids)=>ids.indexOf(id)!==i));
      assert.deepEqual(duplicateIds,[]);
      const concept = page.locator('[data-concept-buttons] button');
      await concept.first().focus(); await page.keyboard.press('ArrowRight');
      assert.equal(await concept.nth(1).getAttribute('aria-pressed'),'true');
      await page.keyboard.press('End'); assert.equal(await concept.nth(2).getAttribute('aria-pressed'),'true');
      await page.keyboard.press('Home'); assert.equal(await concept.first().getAttribute('aria-pressed'),'true');
      const questions = page.locator('[data-question]');
      await questions.first().locator('[data-correct="false"]').first().click();
      assert.match(await questions.first().locator('[data-feedback]').innerText(),/다시 살펴보세요/);
      assert.equal(await questions.first().locator('button:disabled').count(),3);
      await page.locator('[data-quiz-reset]').click();
      for(const q of await questions.all()) { await q.locator('[data-correct="true"]').click(); assert.match(await q.locator('[data-feedback]').innerText(),/정답입니다/); }
      assert.match(await page.locator('[data-quiz-score]').innerText(),/4문항 풀이 · 4문항 정답/);
      await page.locator('[data-quiz-reset]').click(); assert.equal(await page.locator('[data-question][data-answered]').count(),0);
      const main = page.locator('.block-simulator .simulator');
      const result = main.locator('[data-sim-result]');
      const normal = await result.innerText();
      if(index === 0) {
        await page.locator('#watch').focus(); await page.keyboard.press('ArrowRight'); assert.equal(await page.locator('#watch').inputValue(),'4');
        await page.keyboard.press('End'); assert.equal(await page.locator('#watch').inputValue(),'5');
        await main.locator('[data-preset="default"]').click(); assert.match(await result.innerText(),/A가 앞섬/);
        await main.locator('[data-preset="save"]').click(); assert.match(await result.innerText(),/B가 앞섬/);
      } else if(index === 1) {
        await main.locator('[data-preset="example"]').click(); assert.match(await result.innerText(),/90,000원/); assert.match(await result.innerText(),/9,000원/);
        await page.locator('#hours').focus(); await page.keyboard.press('ArrowUp'); assert.equal(await page.locator('#hours').inputValue(),'10.5');
        await page.locator('#brand').fill(''); assert.match(await result.innerText(),/빈칸은 미확인/);
        await page.locator('#brand').fill('-1'); assert.match(await result.innerText(),/계산을 멈췄습니다/);
        await page.locator('#brand').fill('1000000001'); assert.match(await result.innerText(),/계산을 멈췄습니다/);
        await main.locator('[data-preset="zero"]').click(); assert.match(await result.innerText(),/시간당 값은 계산할 수 없습니다/);
      } else if(index === 2) {
        await page.locator('#interest').focus(); await page.keyboard.press('ArrowRight'); assert.equal(await page.locator('#interest').inputValue(),'4');
        await page.locator('#evidence').focus(); await page.keyboard.press('End'); await page.keyboard.press('Tab');
        assert.equal(await page.locator('#evidence').inputValue(),'observed'); assert.match(await result.innerText(),/자기보고/);
      } else {
        await page.locator('#origin').focus(); await page.keyboard.press('ArrowDown'); await page.keyboard.press('Tab');
        assert.equal(await page.locator('#origin').inputValue(),'yes');
        await main.locator('[data-preset="reviewed"]').click(); assert.match(await result.innerText(),/검토 기록이 모였습니다/);
        await page.locator('#permission').selectOption('no'); await page.locator('#quotation').selectOption('yes');
        assert.match(await result.innerText(),/개별 적합성 재확인/);
        await page.locator('#people').selectOption('no'); assert.match(await result.innerText(),/다른 권리/);
      }
      await main.locator('[data-preset="break"]').focus(); await page.keyboard.press('Enter');
      const broken = await result.innerText();
      assert.match(broken,[/분모가 사라졌습니다/,/현금 잔액 -50,000원/,/제작 여유가 0/,/허락 또는 인용/][index]);
      for(const input of await main.locator('input[type="range"]').all()) {
        await input.focus(); await page.keyboard.press('Home'); await page.keyboard.press('End');
      }
      const overflow = await page.evaluate(()=>({viewport:innerWidth,document:document.documentElement.scrollWidth}));
      assert(overflow.document <= width,`${slug}/${width} overflow ${overflow.document}`);
      await page.locator('[data-theme-select]').selectOption('light');
      await page.getByRole('button',{name:'다크 모드로 전환',exact:true}).click();
      assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
      const darkOverflow = await page.evaluate(()=>document.documentElement.scrollWidth); assert(darkOverflow <= width);
      await page.getByRole('button',{name:'라이트 모드로 전환',exact:true}).click();
      const anchors = await page.locator('a[href]').evaluateAll(nodes=>nodes.map(n=>n.href));
      anchors.filter(href=>href.startsWith(locationBase())).forEach(href=>links.add(href));
      function locationBase(){return base+'/';}
      const check = page.locator('[data-checklist] input').first(); await check.check(); await page.reload({waitUntil:'networkidle'}); assert(await check.isChecked());
      // Capture two reviewable views, with simulator inputs and explanation together.
      if(width === 1280 && index === 1) {
        await main.locator('[data-preset="example"]').click();
        await page.setViewportSize({width:1280,height:1700});
        await main.scrollIntoViewIfNeeded();
        await page.screenshot({path:'docs/results/phase-5a/desktop-ledger.png'});
      }
      if(width === 375 && index === 3) {
        await main.locator('[data-preset="break"]').click();
        await page.setViewportSize({width:375,height:1900});
        await main.scrollIntoViewIfNeeded();
        await page.screenshot({path:'docs/results/phase-5a/mobile-rights.png'});
      }
      reports.push({slug,width,blocks:9,quiz:4,simulators:2,overflow,darkOverflow,normal,breakResult:broken});
      console.log(`${slug} / ${width}px pass`);
      await page.close();
    }
  }
  const linkPage = await browser.newPage();
  const missing=[];
  for(const href of links) {
    const url = new URL(href); const response = await linkPage.goto(href,{waitUntil:'domcontentloaded'});
    if(response && !response.ok()) missing.push({href,status:response.status()});
    else if(url.hash) {
      const exists=await linkPage.evaluate(hash=>Boolean(document.getElementById(decodeURIComponent(hash.slice(1)))),url.hash);
      if(!exists)missing.push({href,reason:'fragment missing'});
    }
  }
  assert.deepEqual(missing,[]); assert.deepEqual(errors,[]);
  // Storage denial and no-JS remain usable for the authored core content.
  const context = await browser.newContext();
  await context.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('denied');}});});
  const fallback=await context.newPage();
  const fallbackErrors=[]; fallback.on('pageerror',e=>fallbackErrors.push(e.message));
  await fallback.goto(`${base}/chapters/03-revenue.html`); await fallback.locator('[data-checklist] input').first().check();
  await fallback.locator('[data-preset="example"]').click(); assert.match(await fallback.locator('#ledger-sim [data-sim-result]').innerText(),/90,000원/);
  assert.deepEqual(fallbackErrors,[]); await context.close();
  const nojs=await browser.newContext({javaScriptEnabled:false}); const print=await nojs.newPage();
  await print.goto(`${base}/chapters/02-formats.html`); assert.equal(await print.locator('[data-block]').count(),9); assert.equal(await print.locator('noscript details').count(),1); await nojs.close();
  await writeFile('docs/results/phase-5a/verification.json',JSON.stringify({base,reports,checkedInternalLinks:links.size,consoleErrors:errors,missing,storageDenied:'pass',noJavaScript:'pass'},null,2));
  console.log(JSON.stringify({pages:reports.length,internalLinks:links.size,consoleErrors:errors.length,missing:missing.length,screenshots:2}));
} finally {await browser.close();}
