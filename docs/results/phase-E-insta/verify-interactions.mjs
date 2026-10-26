import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const checks=[],errors=[];
const check=(name,ok)=>{if(!ok)throw Error(name);checks.push(name);};
try {
for(const width of [1280,375,360])for(const theme of ['light','dark']){
 const context=await browser.newContext({viewport:{width,height:1000},reducedMotion:'reduce'});const p=await context.newPage();
 p.on('pageerror',e=>errors.push(String(e)));p.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 const go=async name=>{await p.goto('http://127.0.0.1:8647/site/chapters/'+name);await p.locator('[data-theme-select]').selectOption(theme);await p.evaluate(()=>document.fonts.ready);};
 const tag=`${width}/${theme}`;
 await go('07-cards.html');let tool=p.locator('[data-interaction="cards"]');
 check(tag+' card topic',(await tool.locator('[data-title]').inputValue()).includes('청년 지원금'));
 check(tag+' default no clipping',(await tool.locator('[data-sim-result]').innerText()).startsWith('0줄'));
 await tool.locator('[data-preset="overflow"]').focus();await p.keyboard.press('Enter');
 check(tag+' long example clips',!(await tool.locator('[data-sim-result]').innerText()).startsWith('0줄'));
 await tool.locator('[data-preset="default"]').click();await tool.locator('[data-small]').click();
 check(tag+' small preview complete',(await tool.locator('[data-sim-result]').innerText()).startsWith('0줄'));
 await go('08-reels.html');tool=p.locator('[data-interaction="reels"]');
 await tool.locator('[data-preset="fast"]').click();check(tag+' fast topic',(await tool.locator('[data-caption]').inputValue()).includes('청년 지원금'));
 await tool.locator('[data-repair]').focus();await p.keyboard.press('Enter');
 check(tag+' subtitle repair',(await tool.locator('[data-caption]').inputValue())==='신청 대상을 확인하세요.');
 const before=Number(await tool.locator('[data-seek]').inputValue());await tool.locator('[data-frame="1"]').click();
 check(tag+' next frame',Number(await tool.locator('[data-seek]').inputValue())===before+1);
 await tool.locator('[data-stop]').click();check(tag+' stop zero',Number(await tool.locator('[data-seek]').inputValue())===0);
 await go('12-safety.html');tool=p.locator('[data-interaction="safety"]');await p.locator('details').evaluateAll(ns=>ns.forEach(n=>n.open=true));
 for(const id of ['mixed','voice']){
  await tool.locator('[data-case]').selectOption(id);
  check(tag+' '+id+' gated',await tool.locator('[data-decision="facts"]').isDisabled());
  for(const clue of ['facts','rights','ad','ai','security'])await tool.locator(`[data-evidence] [data-choice="${clue}"]`).click();
  await tool.locator('[data-decision="facts"]').selectOption('clear');
  check(tag+' '+id+' rejects unfixed',await tool.locator('[data-decision="facts"]').inputValue()!=='clear');
  for(const group of ['rights','facts','labels','security']){await tool.locator(`[data-fix="${group}"]`).click();await tool.locator(`[data-decision="${group}"]`).selectOption('clear');}
  check(tag+' '+id+' resolves',(await tool.locator('[data-sim-result]').innerText()).startsWith('0개 남음'));
  if(id==='mixed')check(tag+' conditions restored',(await tool.locator('[data-changes]').innerText()).includes('대상·기간·서류 확인, 자동 지급 아님'));
 }
 await context.close();
}
check('console/page errors zero',!errors.length);
await fs.writeFile('docs/results/phase-E-insta/interaction-check.json',JSON.stringify({passed:checks.length,checks,errors},null,2));
console.log('PASS',checks.length);
}finally{await browser.close();}
