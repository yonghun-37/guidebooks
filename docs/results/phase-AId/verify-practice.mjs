// Linux Chromium: AIc 소유 페이지의 화면·키보드·진행 기록·복사·링크 검사.
import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const base=process.env.SITE_URL||'http://127.0.0.1:8593/site/';
const out='docs/results/phase-AId/practice/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage(), checks=[],errors=[],screens=[],links=new Set();
page.on('console',m=>{if(m.type()==='error')errors.push({url:page.url(),message:m.text()});});
page.on('pageerror',e=>errors.push({url:page.url(),message:String(e)}));
page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push({url:r.url(),status:r.status()});});
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
const go=slug=>page.goto(base+'practice/'+slug+'.html',{waitUntil:'networkidle'});
const overflow=()=>page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,bad:[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left< -1)}).slice(0,5).map(e=>e.tagName+'#'+e.id)}));
try {
for(const width of [1280,375,360]){
 await page.setViewportSize({width,height:1000});
 for(const slug of ['00-start','03-copy','04-cards','05-reel','e2e']){
  await go(slug); await page.evaluate(()=>document.fonts.ready);
  for(const theme of ['light','dark']){
   await page.locator('[data-theme-select]').selectOption(theme);
   const before=await overflow();check(`${width} ${theme} ${slug} overflow ${JSON.stringify(before)}`,before.scroll<=before.width);
   if(theme==='light'){
    await page.screenshot({path:out+`${slug}-${width}.png`});screens.push(`${slug}-${width}.png`);
   }
   await page.locator('details').evaluateAll(ns=>ns.forEach(n=>n.open=true));
   const expanded=await overflow();check(`${width} ${theme} ${slug} expanded overflow ${JSON.stringify(expanded)}`,expanded.scroll<=expanded.width);
   check(`${width} ${theme} ${slug} image alt`,await page.locator('img').evaluateAll(ns=>ns.every(n=>n.alt.trim())));
   check(`${width} ${theme} ${slug} SVG labels`,await page.locator('svg[role="img"]').evaluateAll(ns=>ns.every(n=>n.getAttribute('aria-labelledby')?.split(' ').every(id=>document.getElementById(id)))));
   await page.locator('details').evaluateAll(ns=>ns.forEach(n=>n.open=false));
  }
  if(width===1280){
   (await page.locator('a[href]').evaluateAll(ns=>ns.map(n=>n.href).filter(h=>h.startsWith(location.origin)))).forEach(h=>links.add(h));
   // Every tab group, including the preserved kit alternative, supports arrows/Home/End.
   if(await page.locator('#kit').count())await page.locator('#kit').evaluate(e=>e.open=true);
   for(const group of await page.locator('[data-os-tabs]').all()){
    const tabs=group.locator('[role="tab"]');await tabs.first().focus();await page.keyboard.press('ArrowRight');
    check(slug+' tab right '+await tabs.first().getAttribute('id'),await tabs.nth(1).getAttribute('aria-selected')==='true'&&await tabs.nth(1).evaluate(e=>document.activeElement===e));
    check(slug+' active panel '+await tabs.first().getAttribute('id'),await group.locator('[role="tabpanel"]').nth(1).isVisible());
    await page.keyboard.press('Home');check(slug+' tab Home '+await tabs.first().getAttribute('id'),await tabs.first().getAttribute('aria-selected')==='true');
    await page.keyboard.press('End');check(slug+' tab End '+await tabs.first().getAttribute('id'),await tabs.nth(1).getAttribute('aria-selected')==='true');
    await page.keyboard.press('ArrowLeft');check(slug+' tab left '+await tabs.first().getAttribute('id'),await tabs.first().getAttribute('aria-selected')==='true');
   }
   for(const q of await page.locator('[data-question]').all()){
    await q.locator('[data-correct="true"]').focus();await page.keyboard.press('Enter');
    check(slug+' quiz keyboard',(await q.locator('[data-feedback]').innerText()).includes('정답입니다.'));
   }
   const summary=page.locator('#faq summary').first();await summary.focus();await page.keyboard.press('Enter');
   check(slug+' FAQ Enter',await summary.evaluate(e=>e.parentElement.open));
   await page.keyboard.press('Space');check(slug+' FAQ Space',!await summary.evaluate(e=>e.parentElement.open));
   if(await page.locator('#kit').count()){
    await page.locator('#kit').evaluate(e=>e.open=false);await page.locator('#kit > summary').focus();await page.keyboard.press('Enter');
    check(slug+' kit keyboard',await page.locator('#kit').evaluate(e=>e.open));
   }
   await page.locator('details').evaluateAll(ns=>ns.forEach(n=>n.open=false));
  }
  const focal={'00-start':'#route','03-copy':'#prompt','04-cards':'#render','05-reel':'#captions','e2e':'#service-review'}[slug];
  await page.locator('[data-theme-select]').selectOption('light');
  await page.evaluate(()=>document.activeElement?.blur());await page.locator(focal).scrollIntoViewIfNeeded();await page.locator(focal).screenshot({path:out+`${slug}-step-${width}.png`,style:'[data-site-header], .skip-link {visibility:hidden!important}'});screens.push(`${slug}-step-${width}.png`);
 }
}
await go('03-copy');await page.locator('#prompt .copy-button').focus();await page.keyboard.press('Enter');
await page.waitForFunction(()=>document.querySelector('#prompt .copy-status').textContent.includes('복사했습니다.'));
check('prompt keyboard copy status',(await page.locator('#prompt .copy-status').innerText()).includes('복사했습니다.'));
check('prompt clipboard exact',await page.evaluate(async()=>await navigator.clipboard.readText()===document.querySelector('#prompt code').textContent));
await page.locator('[data-practice-check="3:signup"]').focus();await page.keyboard.press('Space');
check('checkbox Space',await page.locator('[data-practice-check="3:signup"]').isChecked());
await page.reload();check('checkbox reload',await page.locator('[data-practice-check="3:signup"]').isChecked());
await go('e2e');check('E2E cross-page restore',await page.locator('[data-practice-check="3:signup"]').isChecked());
check('E2E max43',await page.locator('progress').getAttribute('max')==='43');
await page.locator('[data-practice-reset]').focus();await page.keyboard.press('Enter');
check('E2E reset keyboard',await page.locator('input:checked').count()===0);
await go('03-copy');check('reset cross-page',!await page.locator('[data-practice-check="3:signup"]').isChecked());
// Verify emitted links and anchors using a second tab to preserve page state.
const linkPage=await context.newPage();
for(const href of links){
 const response=await linkPage.goto(href,{waitUntil:'domcontentloaded'});check('link '+href,response===null||response.ok());
 const hash=decodeURIComponent(new URL(href).hash.slice(1));if(hash)check('anchor '+href,await linkPage.evaluate(id=>!!document.getElementById(id),hash));
}
await linkPage.close();
// Blocked storage must remain operable without exceptions.
const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked fixture')}})});
const blockedPage=await blocked.newPage();await blockedPage.goto(base+'practice/e2e.html');
check('blocked storage announced',(await blockedPage.locator('[data-practice-status]').innerText()).includes('저장할 수 없습니다'));
await blockedPage.locator('[data-practice-check="0:route"]').check();check('blocked storage checkbox works',await blockedPage.locator('[data-practice-check="0:route"]').isChecked());await blocked.close();
check('console/page/local HTTP errors zero',errors.length===0);
} finally {
 await fs.writeFile(out+'browser-check.json',JSON.stringify({base,passed:checks.length,checks,errors,screens},null,2));
 await browser.close();
}
console.log('PASS '+checks.length+' checks, '+screens.length+' screenshots');
