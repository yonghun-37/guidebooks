import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
const out='docs/results/phase-V-shorts', origin='http://127.0.0.1:8637', base=origin+'/site-shorts/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'}), page=await context.newPage();
const checks=[],failures=[],errors=[],metrics=[],shots=[];
const check=(name,ok,detail)=>{checks.push(name);if(!ok)failures.push({name,detail});};
page.on('console',m=>{if(m.type()==='error')errors.push({url:page.url(),message:m.text()});});
page.on('pageerror',e=>errors.push({url:page.url(),message:String(e)}));
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push({url:r.url(),status:r.status()});});
const files=[];
async function scan(dir,prefix=''){for(const e of await fs.readdir(dir,{withFileTypes:true})){if(e.isDirectory())await scan(dir+'/'+e.name,prefix+e.name+'/');else if(e.name.endsWith('.html'))files.push(prefix+e.name);}}
await scan('site-shorts');
const mainShots=new Set(['shot-sizes','caption-placement','editor-regions','export-settings']);
const secondary=new Set(['audio-tracks','keyframe-comparison','subtitle-files','aspect-resolution','template-layers','paper-shot-sizes','practice-timeline','upload-overview','published-result','api-sequence','v-fig-4','v-fig-8','v-fig-63','v-fig-99','v-fig-203','v-fig-204','v-fig-205']);
try {
for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const file of files){
 await page.setViewportSize({width,height:1000});await page.goto(base+file);
 await page.evaluate(theme=>{document.documentElement.dataset.theme=theme;const t=document.querySelector('[data-theme-select]');if(t){t.value=theme;t.dispatchEvent(new Event('change',{bubbles:true}));}},theme);
 await page.evaluate(()=>document.fonts.ready);
 const key=`${file}/${width}/${theme}`;
 check(key+'/가로 넘침0',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 check(key+'/테마',await page.evaluate(theme=>document.documentElement.dataset.theme===theme,theme));
 for(const f of await page.locator('figure').all()){
  await f.scrollIntoViewIfNeeded();await f.locator('img').evaluateAll(ns=>Promise.all(ns.map(n=>n.decode().catch(()=>{}))));
  const result=await f.evaluate(f=>{
   const box=f.getBoundingClientRect();const bad=[],sizes=[];
   for(const t of f.querySelectorAll('.v-svg text')){
    const r=t.getBoundingClientRect(),matrix=t.getScreenCTM(),size=parseFloat(getComputedStyle(t).fontSize)*Math.hypot(matrix.a,matrix.b);
    sizes.push({text:t.textContent,pixels:Number(size.toFixed(2))});
    const root=t.closest('svg').getBoundingClientRect();
    if(size<13.95)bad.push({text:t.textContent,reason:'small',size});
    if(r.left<root.left-1||r.right>root.right+1||r.top<root.top-2||r.bottom>root.bottom+2)bad.push({text:t.textContent,reason:'svg boundary',r:r.toJSON(),root:root.toJSON()});
   }
   const images=[...f.querySelectorAll('img')];
   return {id:f.id,caption:!!f.querySelector(':scope>figcaption')?.textContent.trim(),imagesLoaded:images.every(n=>n.complete&&n.naturalWidth>0),within:box.left>=-1&&box.right<=innerWidth+1,bad,sizes};
  });
  check(key+'/'+result.id+'/캡션',result.caption);
  check(key+'/'+result.id+'/이미지 로드',result.imagesLoaded);
  check(key+'/'+result.id+'/경계',result.within);
  check(key+'/'+result.id+'/SVG 글자',!result.bad.length,result.bad);
  if(result.sizes.length)metrics.push({key,id:result.id,min:Math.min(...result.sizes.map(s=>s.pixels)),sizes:result.sizes});
  if(mainShots.has(result.id)||(width===360&&theme==='dark'&&secondary.has(result.id))){
   const name=`${result.id}-${width}-${theme}.png`;
   await f.screenshot({path:out+'/'+name,animations:'disabled',style:'.site-header{visibility:hidden!important}'});shots.push(name);
  }
 }
 await page.locator('main details').evaluateAll(ns=>ns.forEach(n=>n.open=true));
 check(key+'/접힌 설명 펼친 뒤 가로 넘침0',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
}
// The visual-only changes must leave native keyboard interactions working.
await page.setViewportSize({width:360,height:1000});
for(const file of files.filter(f=>f.startsWith('chapters/')&&!f.includes('coming-soon'))){
 await page.goto(base+file);
 for(const q of await page.locator('[data-question]').all()){
  await q.locator('[data-correct=true]').focus();await page.keyboard.press('Space');
  check(file+'/퀴즈 Space',await q.locator('[data-feedback]').innerText().then(t=>t.includes('정답입니다')));
 }
}
await page.goto(base+'practice/06-edit.html');
const range=page.locator('.caption-lab input[type=range]').first();const before=await range.inputValue();await range.focus();await page.keyboard.press('ArrowRight');check('실습6 자막 시간 방향키',await range.inputValue()!==before);
const checkbox=page.locator('input[data-step]').first();
if(await checkbox.count()){await checkbox.focus();await page.keyboard.press('Space');check('실습 체크 Space',await checkbox.isChecked());}
await page.goto(base+'lab.html');
const picker=page.locator('#sim-picker');
const options=await picker.locator('option').evaluateAll(ns=>ns.map(n=>n.value));
for(const value of options){await picker.selectOption(value);const f=page.frameLocator('#sim-frame');await f.locator('html.sim-embed').waitFor();check('원본 도구 임베드/'+value,await f.locator('main').count()===1);}
check('콘솔·페이지·내부HTTP 오류0',!errors.length,errors);
} finally {
 const result={pages:files.length,variants:6,pageRenders:files.length*6,checks:checks.length,failures,errors,metrics,screenshots:shots};
 await fs.writeFile(out+'/browser-check.json',JSON.stringify(result,null,2)+'\n');
 await browser.close();console.log(JSON.stringify({pages:files.length,variants:6,checks:checks.length,failures:failures.length,errors:errors.length,screenshots:shots.length}));
 if(failures.length||errors.length)process.exitCode=1;
}
