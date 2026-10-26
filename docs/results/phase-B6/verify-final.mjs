import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base='http://127.0.0.1:8636/site-blog/',out='docs/results/phase-B6';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({viewport:{width:360,height:960},reducedMotion:'reduce'}),page=await context.newPage(),checks=[],errors=[];
const check=(name,ok)=>{assert.ok(ok,name);checks.push(name);};
page.on('pageerror',e=>errors.push(String(e)));page.on('console',e=>{if(e.type()==='error')errors.push(e.text());});
try{
 for(const [folder,slug] of [['chapters','06-writing'],['practice','04-draft']]){
  await page.goto(base+folder+'/pending.html?chapter='+slug);
  const link=page.locator('[data-legacy-message] a');check('옛주소본문연결 '+slug,await link.evaluate(a=>a.href)===base+folder+'/'+slug+'.html');await link.click();check('옛주소도착 '+slug,page.url()===base+folder+'/'+slug+'.html');
 }
 await page.goto(base+'lab.html?tool=13-plan:plan-tool');check('원본선택주소복원',await page.locator('#sim-picker').inputValue()==='13-plan:plan-tool');await page.locator('[data-theme-select]').selectOption('dark');
 for(const t of await page.evaluate(()=>window.BlogCatalog)){
  await page.locator('#sim-picker').selectOption(`${t.slug}:${t.id}`);const tool=page.frameLocator('#sim-frame').locator('#'+t.id);await tool.waitFor({state:'visible'});
  const c=tool.locator('input:not([type=hidden]),select,textarea,button').first();await c.focus();const tag=await c.evaluate(n=>n.tagName),type=await c.getAttribute('type');const before=await c.evaluate(n=>n.type==='checkbox'||n.type==='radio'?n.checked:n.value);
  if(tag==='BUTTON'||type==='checkbox')await page.keyboard.press('Space');
  else if(tag==='SELECT'||type==='number'||type==='date')await page.keyboard.press('ArrowUp');
  else if(type==='radio')await page.keyboard.press('ArrowRight');
  else{await page.keyboard.press('End');await page.keyboard.type(' 확인');}
  if(tag==='SELECT'&&(await c.inputValue())===before)await page.keyboard.press('ArrowDown');
  if(tag!=='BUTTON'&&type!=='radio')check('도구키보드입력 '+t.chapter,await c.evaluate(n=>n.type==='checkbox'?n.checked:n.value)!==before);
  else check('도구키보드실행 '+t.chapter,await tool.isVisible());
 }
 check('최종오류0',errors.length===0);await fs.writeFile(out+'/final-browser-check.json',JSON.stringify({checks:checks.length,errors,passed:checks},null,2));console.log(JSON.stringify({checks:checks.length,errors}));
}finally{await browser.close();}
