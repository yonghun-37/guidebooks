import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
const out='docs/results/phase-E-shorts', origin='http://127.0.0.1:8637', base=origin+'/site-shorts/';
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
for(const width of [1280,375,360])for(const theme of ['light','dark']) {
 await page.setViewportSize({width,height:1000}); await page.goto(base+'prompts.html');
 await page.evaluate(t=>document.documentElement.dataset.theme=t,theme);
 for(const id of ['three-videos','actual-image-prompts']) {
  const target=page.locator('#'+id); await target.screenshot({path:out+'/'+id+'-'+width+'-'+theme+'.png',style:'.site-header{visibility:hidden!important}'}); shots.push(id+'-'+width+'-'+theme+'.png');
 }
 await page.goto(base+'assets/samples/preview.html'); await page.locator('video').evaluate(async v=>{await v.play();await new Promise(r=>setTimeout(r,300));v.pause();});
 await page.screenshot({path:out+'/sample-'+width+'-'+theme+'.png',fullPage:true}); shots.push('sample-'+width+'-'+theme+'.png');
}
// Preserve native keyboard interactions across the changed examples.
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

await page.goto(base+'chapters/03-hook.html');
await page.selectOption('#hook-choice','specific'); await page.locator('#hook-time').fill('3');
check('훅 새 예문',await page.locator('#hook-line').innerText().then(t=>t.includes('네 칸')));
const noteEnd=await page.locator('#moving-note').getAttribute('d');
await page.locator('#hook-start').click();check('훅 이동 도식',await page.locator('#moving-note').getAttribute('d')!==noteEnd);
await page.locator('#hook-extreme').click();check('훅 빈 문장',await page.locator('#hook-line').innerText().then(t=>t.includes('문장 없음')));
await page.goto(base+'chapters/07-editing.html');
await page.locator('[data-edit-preset=early]').click();check('편집 자막 끝 비교',await page.locator('[data-sim-result]').innerText().then(t=>t.includes('-2.0초')));
await page.goto(base+'chapters/08-captions.html');
await page.locator('[data-caption-preset=fast]').click();check('자막 극단값',await page.locator('#caption-copy').inputValue().then(t=>t.includes('월세')));
await page.locator('[data-caption-preset=base]').click();check('자막 기본 예문',await page.locator('#caption-copy').inputValue()==='월세부터 따로');
await page.goto(base+'chapters/09-export.html');
await page.selectOption('#export-rate','2');check('압축 크기 계산 유지',await page.locator('[data-sim-result]').innerText().then(t=>t.startsWith('3MB')));
await page.goto(base+'chapters/11-upload.html');
await page.locator('[data-meta-preset=base]').click();check('업로드 기본안 검토',await page.locator('#metadata-tool [data-ops-result]').innerText().then(t=>t.startsWith('0개')));
check('업로드 새 설명',await page.locator('#meta-description').inputValue().then(t=>t.includes('비상금')));
await page.goto(base+'chapters/12-analytics.html');
await page.selectOption('#curve-case','middle');check('분석 장면 연결',await page.locator('[data-curve-frame]').innerText().then(t=>t.includes('네 칸')));
await page.selectOption('#curve-hypothesis','dense');await page.locator('[data-curve-suggest]').click();check('분석 수정안',await page.locator('[data-ops-result]').innerText().then(t=>t.includes('반복 설명')));
await page.goto(base+'chapters/13-policy.html');await page.locator('[data-policy-preset=risk]').click();check('정책 분기 보존',await page.locator('[data-ops-result]').innerText().then(t=>t.startsWith('4개')));
await page.goto(base+'assets/samples/preview.html');await page.locator('video').evaluate(async v=>{await v.play();await new Promise(r=>setTimeout(r,400));v.pause();});
await page.locator('[data-start]').nth(1).click();check('샘플 새 장면 탐색',await page.locator('video').evaluate(v=>Math.abs(v.currentTime-12)<.1));
const beforeFrame=await page.locator('video').evaluate(v=>v.currentTime);await page.locator('#next').click();check('샘플 다음 프레임',await page.locator('video').evaluate((v,t)=>v.currentTime>t,beforeFrame));

check('콘솔·페이지·내부HTTP 오류0',!errors.length,errors);
} finally {
 const result={pages:files.length,variants:6,pageRenders:files.length*6,checks:checks.length,failures,errors,metrics,screenshots:shots};
 await fs.writeFile(out+'/browser-check.json',JSON.stringify(result,null,2)+'\n');
 await browser.close();console.log(JSON.stringify({pages:files.length,variants:6,checks:checks.length,failures:failures.length,errors:errors.length,screenshots:shots.length}));
 if(failures.length||errors.length)process.exitCode=1;
}
