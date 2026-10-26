import { chromium } from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base=process.env.SITE_URL || 'http://127.0.0.1:39369/';
const out='docs/results/phase-9d/';
const files=(await fs.readdir('site/practice')).filter(x=>x.endsWith('.html')).sort();
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage(); const checks=[],errors=[],links=new Set();
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('pageerror',e=>errors.push(String(e)));
const check=(name,v)=>{assert.ok(v,name);checks.push(name);};
try {
 for (const width of [1280,375,360]) {
  await page.setViewportSize({width,height:1000});
  for (const file of files) {
   await page.goto(base+'site/practice/'+file,{waitUntil:'networkidle'});
   check(`${file} ${width} no overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   check(`${file} ${width} five FAQ`,await page.locator('.chapter-faq details').count()===5);
   check(`${file} ${width} deliverable`,(await page.locator('.chapter-hero').innerText()).includes('이 실습이 끝나면 내 손에 있는 것'));
   await page.locator('.chapter-faq summary').first().focus();await page.keyboard.press('Enter');
   check(`${file} ${width} FAQ keyboard`,await page.locator('.chapter-faq details').first().getAttribute('open')!==null);
   const groups=await page.locator('[data-os-tabs]').count();
   for(let n=0;n<groups;n++) {
    const group=page.locator('[data-os-tabs]').nth(n),tabs=group.locator('[data-os-tab]');
    await tabs.first().focus();await page.keyboard.press('ArrowRight');
    check(`${file} ${width} OS ${n} keyboard`,await tabs.nth(1).getAttribute('aria-selected')==='true' && await group.locator('[data-os-panel="macos"]').isVisible());
    check(`${file} ${width} OS ${n} expanded no overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   }
   if(file!=='e2e.html') {
    const correct=page.locator('[data-question] [data-correct="true"]');
    await correct.click();
    check(`${file} ${width} correct quiz`,(await page.locator('[data-quiz-score]').textContent()).includes('1문항 정답'));
    check(`${file} ${width} explanation`,!(await page.locator('[data-feedback]').textContent()).includes('undefined'));
    await page.locator('[data-quiz-reset]').click();await page.locator('[data-correct="false"]').click();
    check(`${file} ${width} wrong quiz`,(await page.locator('[data-quiz-score]').textContent()).includes('0문항 정답'));
    check(`${file} ${width} six step blocks`,await page.locator('[data-step]').evaluateAll(ns=>ns.every(n=>['practice-now','practice-why','practice-follow','practice-success','practice-errors','os-tabs'].every(c=>n.querySelector('.'+c)))));
   }
   const hrefs=await page.locator('a[href]').evaluateAll(ns=>ns.map(n=>n.href).filter(s=>s.startsWith(location.origin)));
   hrefs.forEach(x=>links.add(x));
   if(width!==360){await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));await page.screenshot({path:out+file.replace('.html','')+`-${width}.png`});}
  }
 }
 // Check all rendered local links, including dynamically inserted book navigation.
 for(const href of links){
  const u=new URL(href);const response=await context.request.get(u.origin+u.pathname);check(`link ${u.pathname}`,response.ok());
  if(u.hash){const body=await response.text();const id=decodeURIComponent(u.hash.slice(1));check(`anchor ${u.pathname}${u.hash}`,new RegExp(`\\bid=["']${id.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}["']`).test(body));}
 }
 await page.goto(base+'site/practice/07-publish.html');
 await page.locator('[data-practice-check="7:share"]').check();
 await page.locator('[data-practice-field]').fill('https://www.instagram.com/p/phase9d-test-only/');
 await page.reload();check('posted URL restored',await page.locator('[data-practice-field]').inputValue()==='https://www.instagram.com/p/phase9d-test-only/');
 await page.goto(base+'site/practice/e2e.html');check('E2E shared step restored',await page.locator('[data-practice-check="7:share"]').isChecked());
 check('E2E 35 preserved step keys',await page.locator('[data-practice-check]').count()===35);
 await page.locator('[data-practice-reset]').click();check('reset checks',await page.locator('[data-practice-check]:checked').count()===0);
 await page.goto(base+'site/practice/07-publish.html');check('reset posted URL',await page.locator('[data-practice-field]').inputValue()==='');
 await page.setViewportSize({width:375,height:1000});
 await page.locator('#caption-label').scrollIntoViewIfNeeded();await page.screenshot({path:out+'publish-labels-375.png'});
 await page.evaluate(()=>{document.documentElement.dataset.theme='dark';});
 await page.screenshot({path:out+'publish-labels-dark-375.png'});
 await page.goto(base+'site/practice/01-account.html');await page.locator('#test-account').scrollIntoViewIfNeeded();await page.screenshot({path:out+'account-step-375.png'});
 await page.goto(base+'site/practice/09-schedule.html');await page.locator('#schedule').scrollIntoViewIfNeeded();await page.screenshot({path:out+'schedule-step-375.png'});
 const previous=await page.locator('.chapter-faq details[open]').count();
 await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));check('print all FAQ open',await page.locator('.chapter-faq details[open]').count()===5);
 await page.evaluate(()=>dispatchEvent(new Event('afterprint')));check('print restores FAQ',await page.locator('.chapter-faq details[open]').count()===previous);
 // Storage failures still allow local interaction.
 const blocked=await browser.newContext();await blocked.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
 await blocked.addInitScript(()=>{Storage.prototype.setItem=()=>{throw new DOMException('test','QuotaExceededError');};});
 const bp=await blocked.newPage();await bp.goto(base+'site/practice/00-start.html');
 await bp.locator('[data-practice-check]').first().check();check('storage blocked checkbox usable',await bp.locator('[data-practice-check]').first().isChecked());
 check('storage blocked explained',(await bp.locator('[data-practice-status]').textContent()).includes('저장할 수 없습니다'));await blocked.close();
 const plain=await browser.newContext({javaScriptEnabled:false});await plain.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
 const np=await plain.newPage();await np.goto(base+'site/practice/02-setup.html');await np.locator('.chapter-faq summary').first().click();
 check('no JS FAQ usable',await np.locator('.chapter-faq details').first().getAttribute('open')!==null);
 check('no JS both OS panels readable',await np.locator('[data-os-panel="macos"]').first().isVisible() && await np.locator('[data-os-panel="windows"]').first().isVisible());await plain.close();
 check('console and page errors zero',errors.length===0);
 await fs.writeFile(out+'browser-check.json',JSON.stringify({pages:files.length,widths:[1280,375,360],checks:checks.length,localLinks:links.size,errors,passed:checks},null,2)+'\n');
 console.log(JSON.stringify({pages:files.length,checks:checks.length,localLinks:links.size,errors}));
} finally {await browser.close();}
