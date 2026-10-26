// 저장소 루트를 SITE_URL로 제공한 뒤 실행한다. 실제 계정·외부 API는 사용하지 않는다.
import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base=process.env.SITE_URL||'http://127.0.0.1:8549/';
const out='docs/results/phase-9-int/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage(),checks=[],errors=[],links=new Set();
page.on('console',m=>{if(m.type()==='error')errors.push({url:page.url(),error:m.text()});});
page.on('pageerror',e=>errors.push({url:page.url(),error:String(e)}));
page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push({url:r.url(),status:r.status()});});
const check=(label,value)=>{assert.ok(value,label);checks.push(label);};
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
const keyboard=async locator=>{await locator.focus();await page.keyboard.press('Space');};
const files=['site/index.html','site/lab.html','site/glossary.html','site/credits.html','site/chapters/coming-soon.html',
 ...(await fs.readdir('site/chapters')).filter(x=>/^\d\d-.*html$/.test(x)).map(x=>'site/chapters/'+x),
 ...(await fs.readdir('site/practice')).filter(x=>x.endsWith('.html')).map(x=>'site/practice/'+x),
 ...(await fs.readdir('site/drafts')).filter(x=>x.endsWith('.html')).map(x=>'site/drafts/'+x)];
try{
 for(const width of [1280,375,360]){
  await page.setViewportSize({width,height:1000});
  for(const file of files){
   await page.goto(base+file,{waitUntil:'networkidle'});
   check(`${width} ${file} overflow`,await overflow());
   await page.locator('.chapter-faq details').evaluateAll(ns=>ns.forEach(n=>n.open=true));
   check(`${width} ${file} expanded FAQ overflow`,await overflow());
   if(width===375){
    await page.evaluate(()=>document.documentElement.dataset.theme='dark');
    check(`${file} dark overflow`,await overflow());
   }
   (await page.locator('a[href]').evaluateAll(ns=>ns.map(n=>n.href).filter(x=>x.startsWith(location.origin)))).forEach(x=>links.add(x));
   if(width!==1280)continue;
   const faq=page.locator('.chapter-faq details').first();
   if(await faq.count()){
    await faq.evaluate(n=>n.open=false);await keyboard(faq.locator('summary'));
    check(`${file} FAQ Space`,await faq.getAttribute('open')!==null);
    await page.keyboard.press('Enter');check(`${file} FAQ Enter`,await faq.getAttribute('open')===null);
    const initial=await page.locator('.chapter-faq details[open]').count();
    await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));
    check(`${file} FAQ print`,await page.locator('.chapter-faq details[open]').count()===await page.locator('.chapter-faq details').count());
    await page.evaluate(()=>dispatchEvent(new Event('afterprint')));
    check(`${file} FAQ print restore`,await page.locator('.chapter-faq details[open]').count()===initial);
   }
   const axis=page.locator('[data-axis-nav] a').first();
   if(await axis.count()){
    const hash=await axis.getAttribute('href');await axis.focus();await page.keyboard.press('Enter');
    check(`${file} axis keyboard focus`,await page.evaluate(hash=>location.hash===hash&&document.activeElement.id===hash.slice(1),hash));
   }
   const quiz=page.locator('[data-quiz]');
   if(await quiz.count()){
    const questions=quiz.locator('[data-question]'),n=await questions.count();
    for(let i=0;i<n;i++){
     await questions.nth(i).locator('[data-correct="true"]').focus();await page.keyboard.press('Enter');
     check(`${file} quiz ${i} correct`,(await questions.nth(i).locator('[data-feedback]').innerText()).includes('정답입니다.')&&!(await questions.nth(i).locator('[data-feedback]').innerText()).includes('undefined'));
    }
    check(`${file} quiz score`,(await quiz.locator('[data-quiz-score]').innerText()).includes(`${n}문항 정답`));
    await keyboard(quiz.locator('[data-quiz-reset]'));
    check(`${file} quiz keyboard reset`,(await quiz.locator('[data-quiz-score]').innerText()).includes('0문항 풀이'));
    for(let i=0;i<n;i++){
     await keyboard(questions.nth(i).locator('[data-correct="false"]').first());
     check(`${file} quiz ${i} wrong`,(await questions.nth(i).locator('[data-feedback]').innerText()).includes('다시 살펴보세요'));
    }
    await keyboard(quiz.locator('[data-quiz-reset]'));
   }
   const groups=page.locator('[data-os-tabs]');
   for(let i=0;i<await groups.count();i++){
    const tabs=groups.nth(i).locator('[data-os-tab]');await tabs.first().focus();await page.keyboard.press('End');
    check(`${file} OS ${i} End`,await tabs.last().getAttribute('aria-selected')==='true');
    await page.keyboard.press('ArrowRight');check(`${file} OS ${i} wrap`,await tabs.first().getAttribute('aria-selected')==='true');
    await page.keyboard.press('ArrowLeft');check(`${file} OS ${i} left`,await tabs.last().getAttribute('aria-selected')==='true');
    await page.keyboard.press('Home');check(`${file} OS ${i} Home`,await tabs.first().getAttribute('aria-selected')==='true');
   }
   const boxes=page.locator('[data-practice-check], [data-checklist] [data-check]');
   for(let i=0;i<await boxes.count();i++){
    const box=boxes.nth(i),before=await box.isChecked();await keyboard(box);
    check(`${file} checklist ${i} keyboard`,await box.isChecked()!==before);
    await keyboard(box);
   }
  }
 }
 // Check generated metadata against the current HTML and cover TOC.
 await page.goto(base+'site/index.html');
 const data=await page.evaluate(()=>ReelsBook.chapters.filter(c=>c.number<=14&&c.number).map(c=>({slug:c.slug,title:c.title,deliverable:c.deliverable})));
 for(const c of data){
  check(`${c.slug} cover title`,(await page.locator(`[data-chapter-toc] a[href="chapters/${c.slug}.html"]`).innerText()).includes(c.title));
  await page.goto(base+`site/chapters/${c.slug}.html`);
  check(`${c.slug} chapter title`,(await page.locator('h1').innerText()).includes(c.title));
  check(`${c.slug} deliverable`,(await page.locator('.chapter-meta').innerText()).includes(c.deliverable));
  check(`${c.slug} document title`,(await page.title()).includes(c.title));
  await page.goto(base+'site/index.html');
 }
 // Actual rendered relative links and anchors, including JS navigation.
 for(const href of links){
  const u=new URL(href),response=await context.request.get(u.origin+u.pathname);
  check(`link ${u.pathname}`,response.ok());
  if(u.hash){const body=await response.text();const id=decodeURIComponent(u.hash.slice(1));check(`anchor ${u.pathname}${u.hash}`,new RegExp(`\\bid=["']${id.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}["']`).test(body));}
 }
 // Restore old plan inputs while replacing the obsolete calendar result.
 await page.goto(base+'site/lab.html');
 await page.evaluate(()=>localStorage.setItem('reelsbook:sim:planner-sim',JSON.stringify({version:1,values:{'plan-start':'2026-10-27','plan-minutes':'60','plan-days':'5'},result:'STALE-OLD-PLAN',valid:true})));
 await page.reload();check('lab hides old calendar result',!(await page.locator('[data-month-plan]').innerText()).includes('STALE-OLD-PLAN'));
 check('lab old plan explains migration',(await page.locator('[data-month-plan]').innerText()).includes('14장을 열어'));
 await page.goto(base+'site/chapters/14-plan.html');check('old plan values preserved',await page.locator('#plan-minutes').inputValue()==='60');
 const restoredResult=await page.locator('[data-sim-result]').innerText();await page.goto(base+'site/lab.html');
 check('old plan result recalculated',(await page.locator('[data-month-plan]').innerText()).includes(restoredResult));
 // Historical 3/4 values must never appear as results of current tools.
 await page.goto(base+'site/lab.html');
 await page.evaluate(()=>{
  for(const id of ['ledger-sim','niche-sim'])localStorage.setItem(`reelsbook:sim:${id}`,JSON.stringify({version:1,values:{},result:'STALE-OLD-RESULT',valid:true}));
 });await page.reload();
 check('lab ignores old 3/4 results',!(await page.locator('#month-scenario').innerText()).includes('STALE-OLD-RESULT'));
 const catalog=await page.evaluate(()=>ReelsCatalog.filter(c=>c.chapter!==15));
 for(const sim of catalog){
  await page.selectOption('#sim-picker',`${sim.chapter}:${sim.id}`);
  await page.waitForFunction(sim=>{const doc=document.querySelector('#sim-frame').contentDocument;return doc?.readyState==='complete'&&doc.location.pathname.endsWith('/'+sim.slug+'.html')&&doc.location.search==='?embed='+encodeURIComponent(sim.id);},sim);
  const block=page.frameLocator('#sim-frame').locator('.chapter-block:not([hidden])');
  await block.waitFor();check(`embed ${sim.chapter}:${sim.id}`,await block.isVisible());
  check(`embed overflow ${sim.chapter}:${sim.id}`,await page.frameLocator('#sim-frame').locator('html').evaluate(n=>n.scrollWidth<=innerWidth));
 }
 await page.selectOption('#sim-picker','month-scenario');await page.locator('#sim-picker').focus();await page.keyboard.press('ArrowDown');
 check('lab select keyboard',await page.locator('#sim-picker').inputValue()!=='month-scenario');
 await page.goto(base+'site/chapters/14-plan.html');await page.locator('#plan-minutes').fill('60');
 const result=await page.locator('[data-sim-result]').innerText();await page.goto(base+'site/lab.html');
 check('lab uses current plan result',(await page.locator('[data-month-plan]').innerText()).includes(result));
 await page.goto(base+'site/chapters/14-plan.html');await page.locator('#plan-minutes').fill('');await page.goto(base+'site/lab.html');
 check('lab invalid input shown',(await page.locator('[data-month-plan]').innerText()).includes('빈칸·무효 입력'));
 await keyboard(page.locator('[data-clear-month]'));
 check('lab removes legacy and current saved inputs',await page.evaluate(()=>['ledger-sim','niche-sim','planner-sim'].every(id=>localStorage.getItem(`reelsbook:sim:${id}`)===null)));
 await page.goto(base+'site/practice/07-publish.html');await keyboard(page.locator('[data-practice-check="7:share"]'));
 await page.locator('[data-practice-field]').fill('https://www.instagram.com/p/integration-fixture/');await page.reload();
 check('posted URL restored',(await page.locator('[data-practice-field]').inputValue()).endsWith('/integration-fixture/'));
 await page.goto(base+'site/practice/e2e.html');check('E2E shared step',await page.locator('[data-practice-check="7:share"]').isChecked());
 check('E2E 35 steps',await page.locator('[data-practice-check]').count()===35);await keyboard(page.locator('[data-practice-reset]'));
 check('E2E reset',await page.locator('[data-practice-check]:checked').count()===0);
 await page.goto(base+'site/glossary.html');await page.locator('#term-search').fill('지시문');
 check('renamed glossary term searchable',await page.locator('[data-glossary-entry]:visible').count()===1);
 await page.goto(base+'site/drafts/index.html');check('draft selection notice',(await page.locator('main').innerText()).includes('선택 완료: A 뼈대 + B·C, 3장에 반영됨'));
 // Storage failures and JS-off support.
 const blocked=await browser.newContext();await blocked.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
 await blocked.addInitScript(()=>{Storage.prototype.setItem=()=>{throw new DOMException('fixture','QuotaExceededError');};});
 const bp=await blocked.newPage();await bp.goto(base+'site/practice/00-start.html');await bp.locator('[data-practice-check]').first().focus();await bp.keyboard.press('Space');
 check('blocked storage keyboard usable',await bp.locator('[data-practice-check]').first().isChecked());
 check('blocked storage explained',(await bp.locator('[data-practice-status]').innerText()).includes('저장할 수 없습니다'));await blocked.close();
 const plain=await browser.newContext({javaScriptEnabled:false});await plain.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
 const np=await plain.newPage();await np.goto(base+'site/practice/02-setup.html');await np.locator('.chapter-faq summary').first().focus();await np.keyboard.press('Enter');
 check('no JS FAQ',await np.locator('.chapter-faq details').first().getAttribute('open')!==null);
 check('no JS OS readable',await np.locator('[data-os-panel="macos"]').first().isVisible()&&await np.locator('[data-os-panel="windows"]').first().isVisible());await plain.close();
 for(const [file,name] of [['site/index.html','cover'],['site/lab.html','lab'],['site/glossary.html','glossary'],['site/drafts/index.html','drafts']]){
  await page.goto(base+file);for(const width of [1280,375]){await page.setViewportSize({width,height:1000});await page.screenshot({path:out+`${name}-${width}.png`});}
 }
 check('no console/page/HTTP errors',errors.length===0);
 await fs.writeFile(out+'browser-check.json',JSON.stringify({pages:files.length,widths:[1280,375,360],checks:checks.length,localLinks:links.size,errors,passed:checks},null,2)+'\n');
 console.log(JSON.stringify({pages:files.length,checks:checks.length,localLinks:links.size,errors}));
}finally{await browser.close();}
