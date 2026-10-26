// 저장소 루트를 로컬 제공. 모든 HTML의 화면 폭·테마·오류와 실제 퀴즈를 확인한다.
import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base=process.env.SITE_URL||'http://127.0.0.1:8587/';
const out='docs/results/phase-6b/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage(),checks=[],errors=[],screens=[],links=new Set();
page.on('console',m=>{if(m.type()==='error')errors.push({url:page.url(),message:m.text()});});
page.on('pageerror',e=>errors.push({url:page.url(),message:String(e)}));
page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push({url:r.url(),status:r.status()});});
async function htmlFiles(dir){let paths=[];for(const ent of await fs.readdir(dir,{withFileTypes:true})){const p=dir+'/'+ent.name;if(ent.isDirectory()) paths.push(...await htmlFiles(p));else if(p.endsWith('.html'))paths.push(p);}return paths;}
const files=[...await htmlFiles('site'),...await htmlFiles('shelf')];
const check=(label,condition)=>{assert.ok(condition,label);checks.push(label);};
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
try {
for(const width of [1280,375,360]){
 await page.setViewportSize({width,height:1000});
 for(const file of files){
  await page.goto(base+(file.startsWith('site/') ? 'reels/'+file.slice(5) : file.slice(6)),{waitUntil:'load'});
  await page.waitForFunction(()=>document.readyState==='complete');
  for(const theme of ['light','dark']){
   if(await page.locator('[data-theme-select]').count())await page.locator('[data-theme-select]').selectOption(theme);
   else await page.emulateMedia({colorScheme:theme});
   check(`${width} ${theme} ${file} overflow`,await overflow());
   await page.locator('details').evaluateAll(ns=>ns.forEach(n=>n.open=true));
   check(`${width} ${theme} ${file} expanded overflow`,await overflow());
   check(`${width} ${theme} ${file} image alt`,await page.locator('img').evaluateAll(ns=>ns.every(n=>n.hasAttribute('alt'))));
   if(theme==='dark'&&file==='site/chapters/08-reels.html'){
    const tool=page.locator('#ch8-sim');await tool.evaluate(e=>window.scrollTo({top:e.getBoundingClientRect().top+scrollY-80,behavior:'instant'}));const name=`reel-${width}-dark.png`;await page.screenshot({path:out+name});screens.push(name);
   }
  }
  if(width===1280){
   (await page.locator('a[href]').evaluateAll(ns=>ns.map(n=>n.href).filter(x=>x.startsWith(location.origin)))).forEach(href=>links.add(href));
   const quiz=page.locator('[data-quiz]');
   if(await quiz.count()){
    const qs=quiz.locator('[data-question]');
    for(let i=0;i<await qs.count();i++){
     const q=qs.nth(i);await q.locator('[data-correct="true"]').focus();await page.keyboard.press('Enter');
     check(`${file} quiz${i} correct`,(await q.locator('[data-feedback]').innerText()).includes('정답입니다.'));
     check(`${file} quiz${i} explanation`,(await q.locator('[data-feedback]').innerText()).includes(await q.getAttribute('data-explanation')));
    }
    await quiz.locator('[data-quiz-reset]').click();
    check(`${file} reset`,(await quiz.locator('[data-quiz-score]').innerText()).includes('0문항 풀이'));
    for(let i=0;i<await qs.count();i++){
     const q=qs.nth(i);await q.locator('[data-correct="false"]').first().focus();await page.keyboard.press('Enter');
     check(`${file} quiz${i} wrong`,(await q.locator('[data-feedback]').innerText()).includes('다시 살펴보세요'));
    }
   }
   for(const group of await page.locator('[data-os-tabs]').all()){
    const tabs=group.locator('[data-os-tab]');await tabs.first().focus();await page.keyboard.press('End');
    check(`${file} OS End`,await tabs.last().getAttribute('aria-selected')==='true');
    await page.keyboard.press('Home');check(`${file} OS Home`,await tabs.first().getAttribute('aria-selected')==='true');
   }
   if(file.startsWith('site/chapters/')&&/^\d\d-/.test(file.split('/').at(-1))){
    const meta=await page.locator('.chapter-meta').innerText();check(`${file} metadata`,meta.includes('예상 소요 시간')&&meta.includes('선행 장')&&meta.includes('연결 실습 별도'));
   }
  }
 }
}
for(const href of links){
 const url=new URL(href),response=await context.request.get(url.origin+url.pathname);
 check('runtime link '+url.pathname,response.ok());
 if(url.hash){const text=await response.text(),id=decodeURIComponent(url.hash.slice(1));check('runtime anchor '+url.pathname+url.hash,text.includes('id="'+id+'"')||text.includes("id='"+id+"'"));}
}
check('console/page/network errors zero',errors.length===0);
await fs.writeFile(out+'browser-check.json',JSON.stringify({html_pages:files.length,widths:[1280,375,360],themes:['light','dark'],runtime_links:links.size,passed:checks.length,checks,errors,screens},null,2));
console.log(`PASS ${checks.length}, pages ${files.length}, errors ${errors.length}`);
} catch(error){await fs.writeFile(out+'browser-failure.json',JSON.stringify({message:String(error),passed:checks.length,errors},null,2));throw error;} finally {await browser.close();}
