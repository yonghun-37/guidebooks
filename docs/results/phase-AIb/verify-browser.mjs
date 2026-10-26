import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out=new URL('./',import.meta.url);
const base=process.env.SITE_URL || 'http://127.0.0.1:18642/site/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
if(!process.env.FONT_NETWORK)await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage(),checks=[],errors=[],screenshots=[];
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('pageerror',e=>errors.push(String(e)));
page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
const check=(name,condition)=>{assert.ok(condition,name);checks.push(name);};
const key=async(loc,k='Enter')=>{await loc.focus();await page.keyboard.press(k);};
const text=async(loc,value)=>{await loc.focus();await page.keyboard.press('ControlOrMeta+A');await page.keyboard.insertText(String(value));};
const result=async(root)=>root.locator('[data-sim-result]').textContent();
const shot=async(name,selector)=>{
 await page.locator(selector).evaluate(e=>window.scrollTo({top:e.getBoundingClientRect().top+scrollY-80,behavior:'instant'}));
 await page.screenshot({path:new URL(name+'.png',out).pathname});screenshots.push(name+'.png');
};
const overflow=async tag=>check('가로 넘침 0 '+tag,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
try{
for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const slug of ['06-writing','07-cards','08-reels']){
 const tag=`${slug}/${width}/${theme}`;
 await page.setViewportSize({width,height:1000});await page.goto(base+'chapters/'+slug+'.html');
 await page.evaluate(()=>document.fonts.ready);await page.locator('[data-theme-select]').selectOption(theme);
 await overflow(tag);
 check('9블록 '+tag,await page.locator('[data-block]').count()===9);
 check('FAQ5 '+tag,await page.locator('.chapter-faq details').count()===5);
 for(const img of await page.locator('main img').all()){
  await img.scrollIntoViewIfNeeded();
  await page.waitForFunction(i=>i.complete&&i.naturalWidth>0,await img.elementHandle());
 }
 check('이미지 로드 '+tag,await page.locator('main img').evaluateAll(imgs=>imgs.every(i=>i.complete&&i.naturalWidth>0)));
 for(const summary of await page.locator('main details > summary').all()){
  if(!await summary.isVisible())continue;
  if(!await summary.evaluate(e=>e.parentElement.open))await key(summary);
  check('키보드 접기 '+tag,await summary.evaluate(e=>e.parentElement.open));
 }
 await overflow('접기 전체 펼침 '+tag);
 for(const anchor of await page.locator('[data-axis-nav] a').all()){
  const target=await anchor.getAttribute('href');await key(anchor);
  check('레시피 키보드 이동 '+tag+' '+target,await page.evaluate(target=>location.hash===target,target));
 }
 for(const box of await page.locator('.code-box').all()){
  const expected=await box.locator('code').textContent();await key(box.locator('.copy-button'));
  await page.waitForFunction(()=>[...document.querySelectorAll('.copy-status')].some(e=>e.textContent==='복사했습니다.'));
  check('프롬프트 키보드 복사 '+tag,await page.evaluate(()=>navigator.clipboard.readText())===expected);
 }
 const qs=await page.locator('[data-question]').all();
 for(const q of qs)await key(q.locator('[data-correct="true"]'),'Space');
 check('퀴즈 전체 정답 '+tag,(await page.locator('[data-quiz-score]').textContent()).includes('3문항 정답'));
 await key(page.locator('[data-quiz-reset]'));
 check('퀴즈 초기화 '+tag,(await page.locator('[data-quiz-score]').textContent()).includes('0문항 정답'));
 if(slug==='06-writing'){
  const root=page.locator('#ch6-sim');await key(root.locator('#prompt-source'),'Space');
  check('문안 체크 키보드 '+tag,(await result(root)).startsWith('1개'));
  await key(root.locator('[data-preset="extreme"]'));check('문안 전체 체크 '+tag,(await result(root)).startsWith('3개'));
  await key(root.locator('[data-preset="default"]'));
 }
 if(slug==='07-cards'){
  const root=page.locator('#ch7-sim');
  await key(root.locator('[data-preset="overflow"]'));check('카드 넘침 재현 '+tag,!(await result(root)).startsWith('0줄'));
  await text(root.locator('[data-copy]'),'주민 월 2권 대출\n공휴일 제외');
  check('카드 문안 수정 '+tag,(await result(root)).startsWith('0줄'));
  await key(root.locator('[data-small]'));check('카드 모바일 보기 '+tag,await root.locator('[data-small]').getAttribute('aria-pressed')==='true');
  await key(root.locator('[data-compare]'));await overflow('카드 비교 '+tag);
  await key(root.locator('[data-preset="default"]'));
 }
 if(slug==='08-reels'){
  const root=page.locator('#ch8-sim');
  check('타임라인 세 트랙 '+tag,await root.locator('.track').count()===3);
  await key(root.locator('[data-seek]'),'Home');await key(root.locator('[data-frame="1"]'));
  check('프레임 키보드 '+tag,(await root.locator('[data-clock]').textContent()).startsWith('0.04'));
  await key(root.locator('[data-seek]'),'End');check('시크 키보드 '+tag,(await root.locator('[data-clock]').textContent()).startsWith('20.00'));
  await key(root.locator('[data-preset="fast"]'));check('빠른 자막 재현 '+tag,(await result(root)).startsWith('1.0초'));
  const before=await root.locator('[data-caption]').inputValue();await key(root.locator('[data-repair]'));
  check('자막 줄이기 '+tag,(await root.locator('[data-caption]').inputValue()).length<before.length);
  await key(root.locator('[data-loop]'));await key(root.locator('[data-play]'));await page.waitForTimeout(300);
  check('키보드 재생 '+tag,await root.locator('[data-play]').getAttribute('aria-pressed')==='true');
  await key(root.locator('[data-play]'));const paused=await root.locator('[data-clock]').textContent();await page.waitForTimeout(100);
  check('키보드 일시정지 '+tag,paused===await root.locator('[data-clock]').textContent());
  await key(root.locator('[data-preset="default"]'));
 }
 if(theme==='light'){
  await shot(slug+'-'+width,slug==='06-writing'?'#prompt':slug==='07-cards'?'#readability':'#generated');
  if(slug==='07-cards'){
   await shot('cards-comparison-'+width,'#case');
   await shot('ai-example-'+width,'.practice-figure');
  }
  if(slug==='08-reels')await shot('timeline-'+width,'#ch8-sim');
 }
}
// Exercise the existing clipboard-denied fallback as well.
await page.goto(base+'chapters/06-writing.html');
await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('test-denied');}}}));
await key(page.locator('.copy-button').first());
check('복사 차단시 수동 선택',await page.locator('.copy-status').first().textContent()==='자동 복사를 사용할 수 없습니다. 선택된 내용을 직접 복사하세요.');
check('수동 선택 내용',await page.evaluate(()=>getSelection().toString())===await page.locator('.code-box code').first().textContent());
check('콘솔·페이지 오류 0',errors.length===0);
}finally{
 await fs.writeFile(new URL(process.env.FONT_NETWORK?'browser-font-network.json':'browser-check.json',out),JSON.stringify({checks:checks.length,passed:checks,errors,screenshots,fontNetwork:!!process.env.FONT_NETWORK},null,2)+'\n');
 await browser.close();
}
console.log(JSON.stringify({checks:checks.length,errors,screenshots:screenshots.length}));
