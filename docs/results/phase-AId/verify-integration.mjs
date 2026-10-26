// AId: 번호와 URL의 분리, 서비스 기본 경로, 부록 재사용과 키보드 동작.
import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const base=process.env.SITE_URL||'http://127.0.0.1:8596/site/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage(),checks=[],errors=[];
page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
const check=(label,ok)=>{assert.ok(ok,label);checks.push(label)};
const go=path=>page.goto(base+path,{waitUntil:'networkidle'});
const key=async(loc,k='Enter')=>{await loc.focus();await page.keyboard.press(k)};
try{
 await go('index.html');
 const chapters=await page.evaluate(()=>ReelsBook.chapters);
 const numbered=chapters.filter(c=>/^\d/.test(c.slug));
 check('15 theory chapters contiguous',JSON.stringify(numbered.map(c=>c.number))===JSON.stringify(Array.from({length:15},(_,i)=>i+1)));
 check('cover 15 theory count',await page.locator('[data-chapter-count]').innerText()==='15');
 check('AI cover entrance',await page.locator('.home-hero a[href="chapters/05b-ai-tools.html"]').innerText()==='AI로 무엇을 어떻게 만드나 →');
 for(const [index,c] of chapters.entries()){
  const path=await page.evaluate(slug=>ReelsBook.chapterUrl(ReelsBook.chapters.find(c=>c.slug===slug)),c.slug);
  await page.goto(new URL(path,page.url()).href,{waitUntil:"networkidle"});
  check(c.slug+' current H1',(await page.locator('h1').innerText()).includes(c.title));
  if(c.number!==null)check(c.slug+' current document number',(await page.title()).includes(c.number+'장'));
  const pager=page.locator('[data-chapter-pager] a');
  if(index>0)check(c.slug+' previous',new URL(await pager.first().getAttribute('href'),page.url()).pathname.endsWith(chapters[index-1].slug+'.html'));
  if(index+1<chapters.length)check(c.slug+' next',new URL(await pager.last().getAttribute('href'),page.url()).pathname.endsWith(chapters[index+1].slug+'.html'));
  check(c.slug+' prompt footer',await page.locator('footer a[href$="prompts.html"]').count()===1);
  // All visible chapter link numbers agree with the target metadata, rather than URL prefix.
  const mismatches=await page.locator('a[href]').evaluateAll((links,chapters)=>links.flatMap(a=>{
   const target=chapters.find(c=>new URL(a.href).pathname.endsWith('/'+c.slug+'.html'));
   const match=a.textContent.match(/(?:이론\)?\s*|^\s*)(\d+)장/);
   return target&&match&&Number(match[1])!==target.number?[{text:a.textContent,slug:target.slug,number:target.number}]:[];
  }),chapters);
  check(c.slug+' link numbers '+JSON.stringify(mismatches),mismatches.length===0);
 }
 for(const [slug,previous,next] of [['01-account','00-start','03-copy'],['03-copy','01-account','04-cards'],['06-review','05-reel','07-publish'],['07-publish','06-review','10-insights']]){
  await go('practice/'+slug+'.html');const links=page.locator('[data-chapter-pager] a');
  check(slug+' default previous',(await links.first().getAttribute('href')).endsWith(previous+'.html'));
  check(slug+' default next',(await links.last().getAttribute('href')).endsWith(next+'.html'));
 }
 await go('practice/06-review.html');
 check('service review before kit approval',await page.locator('aside.practice-box').innerText().then(t=>t.includes('Canva·CapCut')&&t.includes('review.txt')));
 check('kit approval remains explicit',await page.locator('#approve h2').innerText().then(t=>t.includes('키트 선택')));
 check('kit approval command preserved',await page.locator('#approve pre code').first().innerText().then(t=>t.includes('run_pipeline.py approve output/first-post')));
 await go('lab.html');const catalog=await page.evaluate(()=>ReelsCatalog);
 check('catalog all 31 tools',catalog.length===31);
 check('lab uses number16',catalog.find(t=>t.slug==='lab').chapter===16);
 check('plan uses number15',catalog.find(t=>t.slug==='14-plan').chapter===15);
 check('31 lab options',await page.locator('#sim-picker option').count()===31);
 for(const width of [1280,375,360]){
  await page.setViewportSize({width,height:1000});
  for(const entry of catalog.filter(c=>c.slug!=='lab')){
   await page.locator('#sim-picker').selectOption(`${entry.chapter}:${entry.id}`);
   await page.waitForFunction(entry=>{const f=document.querySelector('#sim-frame');return f.contentWindow.location.pathname.endsWith('/'+entry.slug+'.html')&&f.contentDocument?.documentElement?.classList.contains('sim-embed')&&!!f.contentDocument.getElementById(entry.id)},entry);
   await page.frameLocator('#sim-frame').locator('#'+entry.id).waitFor({state:'visible'});
   const result=await page.locator('#sim-frame').evaluate(frame=>({height:frame.clientHeight,overflow:frame.contentDocument.documentElement.scrollWidth>frame.contentWindow.innerWidth}));
   check(`lab ${entry.slug}#${entry.id} ${width}`,result.height>100&&!result.overflow);
   check(`lab original ${entry.id} ${width}`,(await page.locator('#sim-original').getAttribute('href')).endsWith(entry.slug+'.html#'+entry.section));
  }
  await page.locator('#sim-picker').selectOption('6:ai-tools-sim');
  const choice=page.frameLocator('#sim-frame').locator('#tool-content');await choice.focus();await page.keyboard.press('End');await page.keyboard.press('Tab');
  check('AI choice keyboard in lab '+width,await choice.inputValue()==='video');
  check('AI choice result in lab '+width,(await page.frameLocator('#sim-frame').locator('#tool-reason').innerText()).includes('무료'));
 }
 await go('chapters/14-plan.html');await page.locator('#plan-minutes').fill('45');
 await go('lab.html');check('plan saved input passed to lab',(await page.locator('[data-month-plan]').innerText()).includes('하루 45분'));
 await key(page.locator('[data-clear-month]'));check('lab input clear',(await page.locator('[data-month-plan]').innerText()).includes('아직 변경한 계획 입력'));
 await go('glossary.html');await page.locator('#term-search').fill('키프레임');check('new term searchable',await page.locator('[data-glossary-entry]:visible').count()===1);
 await page.locator('#term-search').fill('AI 모델');check('model term searchable',await page.locator('[data-glossary-entry]:visible').count()>0);
 check('console clean',errors.length===0);
}finally{await fs.writeFile('docs/results/phase-AId/integration-check.json',JSON.stringify({passed:checks.length,checks,errors},null,2));await browser.close()}
console.log('PASS '+checks.length+' integration checks');
