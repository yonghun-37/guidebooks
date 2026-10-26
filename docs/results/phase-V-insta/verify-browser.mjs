import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
const base='http://127.0.0.1:8614/';
const out='docs/results/phase-V-insta/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'}),page=await context.newPage();
const errors=[],failures=[],checks=[],screens=[];
page.on('console',m=>{if(m.type()==='error')errors.push({url:page.url(),message:m.text()});});
page.on('pageerror',e=>errors.push({url:page.url(),message:String(e)}));
page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push({url:r.url(),status:r.status()});});
async function walk(dir){let files=[];for(const p of await fs.readdir(dir,{withFileTypes:true})){const f=dir+'/'+p.name;if(p.isDirectory())files.push(...await walk(f));else if(f.endsWith('.html'))files.push(f);}return files;}
const files=(await walk('site')).sort();
const selected=new Set(['visual-aspect-ratios','visual-canvas-screen','visual-timeline-screen','visual-gallery-screen','visual-count-ratio','visual-hosting-boundary']);
const verify=(name,ok,details)=>{checks.push(name);if(!ok)failures.push({name,details});};
try{
for(const width of [1280,375,360]){
 await page.setViewportSize({width,height:1000});
 for(const file of files){
  await page.goto(base+file,{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);
  for(const theme of ['light','dark']){
   const select=page.locator('[data-theme-select]');
   if(await select.count())await select.selectOption(theme);else{await page.emulateMedia({colorScheme:theme});await page.evaluate(t=>document.documentElement.dataset.theme=t,theme);}
   await page.locator('details').evaluateAll(ns=>ns.forEach(n=>n.open=true));
   verify(`${width} ${theme} ${file} page width`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   const figs=page.locator('figure');
   for(let i=0;i<await figs.count();i++){
    const f=figs.nth(i);await f.scrollIntoViewIfNeeded();
    await f.locator('img').evaluateAll(async ns=>{for(const n of ns){if(!n.complete)await new Promise(resolve=>{n.onload=resolve;n.onerror=resolve;});}});
    const info=await f.evaluate(el=>{
     const r=el.getBoundingClientRect(),badText=[],clipped=[],htmlOverflow=[];
     const isVisible=e=>!!(e.getClientRects().length&&e.getBoundingClientRect().width)&&getComputedStyle(e).visibility!=='hidden'&&getComputedStyle(e).opacity!=='0';
     for(const t of el.querySelectorAll('svg text')){
      if(!isVisible(t))continue;
      const matrix=t.getScreenCTM(),size=parseFloat(getComputedStyle(t).fontSize)*Math.hypot(matrix.a,matrix.b);
      if(size<13.9)badText.push({text:t.textContent,size});
      const box=t.getBoundingClientRect(),root=t.ownerSVGElement.getBoundingClientRect();
      if(box.left<root.left-1||box.right>root.right+1||box.top<root.top-1||box.bottom>root.bottom+1)clipped.push({text:t.textContent,box:{left:box.left,right:box.right},root:{left:root.left,right:root.right}});
     }
     if(el.classList.contains('book-figure'))for(const n of el.querySelectorAll('*')){
      if(n.closest('svg,.footnote-ref')||!isVisible(n))continue;
      const text=Array.from(n.childNodes).filter(n=>n.nodeType===Node.TEXT_NODE).map(n=>n.textContent.trim()).join('');
      if(text&&parseFloat(getComputedStyle(n).fontSize)<13.9)badText.push({text,size:getComputedStyle(n).fontSize});
      if(n.clientWidth&&n.scrollWidth>n.clientWidth+1)htmlOverflow.push({tag:n.tagName,cls:n.className,text:n.textContent.slice(0,80)});
     }
     return {id:el.id||'figure',left:r.left,right:r.right,width:r.width,badText,clipped,htmlOverflow,caption:!!el.querySelector('figcaption')?.textContent.trim(),images:Array.from(el.querySelectorAll('img')).every(n=>n.complete&&n.naturalWidth>0)};
    });
    const label=`${width} ${theme} ${file} ${info.id}`;
    verify(label+' boundaries',info.left>=-1&&info.right<=width+1,info);
    verify(label+' caption/image',info.caption&&info.images,info);
    if((await f.getAttribute('class')||'').includes('book-figure')){
     verify(label+' readable',!info.badText.length,info.badText);
     verify(label+' text bounds',!info.clipped.length&&!info.htmlOverflow.length,{svg:info.clipped,html:info.htmlOverflow});
    }
    if(selected.has(info.id)||(width===360&&theme==='light'&&i===0)){
     const name=file.replaceAll('/','-').replace('.html','')+'-'+info.id+`-${width}-${theme}.png`;
     await f.screenshot({path:out+name});screens.push(name);
    }
   }
   // 공통 SVG 부품 로드는 로컬 HTTP 오류와 대표 화면에서도 확인한다.
  }
  if(width===1280){
   const quizzes=page.locator('[data-quiz]');
   for(const quiz of await quizzes.all()){
    const qs=quiz.locator('[data-question]');
    for(const q of await qs.all()){
     await q.locator('[data-correct="true"]').focus();await page.keyboard.press('Enter');
     verify(file+' quiz keyboard correct',(await q.locator('[data-feedback]').innerText()).includes('정답입니다.'));
    }
    await quiz.locator('[data-quiz-reset]').click();
    verify(file+' quiz reset',(await quiz.locator('[data-quiz-score]').innerText()).includes('0문항'));
   }
  }
 }
 console.log(`width ${width}: ${files.length} pages checked, failures ${failures.length}`);
}
verify('console/page/local HTTP errors zero',errors.length===0,errors);
await fs.writeFile(out+'browser-check.json',JSON.stringify({html_pages:files.length,widths:[1280,375,360],themes:['light','dark'],checks:checks.length,failures,errors,screens},null,2));
console.log(JSON.stringify({checks:checks.length,failures:failures.length,errors:errors.length,screens:screens.length}));
if(failures.length)process.exitCode=1;
}finally{await browser.close();}
