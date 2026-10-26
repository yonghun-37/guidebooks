// 실행: node docs/results/phase-A6/verify-browser.mjs
// ROOT_URL에는 reels/·shorts/ 배포 구조로 제공하는 로컬 서버를 지정한다.
import { chromium } from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
const origin=process.env.ROOT_URL||'http://127.0.0.1:8876';
const out='docs/results/phase-A6';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.fulfill({status:200,contentType:'text/css',body:''}));
const page=await context.newPage(),errors=[],screens=[],links=new Set(),interactions=[];
page.on('pageerror',e=>errors.push({type:'page',message:e.message}));
page.on('console',m=>{if(m.type()==='error')errors.push({type:'console',message:m.text()});});
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push({type:'http',url:r.url(),status:r.status()});});
const expect=(name,pass,details)=>{interactions.push({name,pass,...details});};
for(const [folder,prefix] of [['site','reels'],['site-shorts','shorts']]){
 const files=(await fs.readdir(folder+'/advanced')).filter(f=>f.endsWith('.html'));
 for(const file of files)for(const width of [1280,375,360])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:960});await page.goto(`${origin}/${prefix}/advanced/${file}`);
  await page.locator('[data-theme-select]').selectOption(theme);
  await page.evaluate(()=>document.fonts.ready);
  await page.locator('main img').evaluateAll(async els=>{for(const e of els){e.loading='eager';await e.decode();}});
  const data=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,broken:[...document.querySelectorAll('main img')].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src),
   svg:[...document.querySelectorAll('main svg')].flatMap(s=>[...s.querySelectorAll('text')].flatMap(t=>{const b=t.getBBox(),v=s.viewBox.baseVal;return v.width&& (b.x < -1 || b.x+b.width>v.width+1 || b.y< -1 || b.y+b.height>v.height+1)?[t.textContent]:[];}))}));
  screens.push({folder,file,width,theme,...data});
  if(data.overflow||data.broken.length||data.svg.length)errors.push({type:'layout',folder,file,width,theme,...data});
  for(const href of await page.locator('a[href]').evaluateAll(es=>es.map(e=>new URL(e.getAttribute('href'),location.href).href)))if(href.startsWith(origin))links.add(href);
  if(width===360&&['02-keys.html','05-publish.html','02-credentials.html','06-gates.html','07-operations.html','04-render.html'].includes(file)){
   // 새 설명 그림을 우선 저장한다. 본문 전체의 긴 이미지는 만들지 않는다.
   const figure=file==='02-credentials.html'?'#tts-key-map':file==='05-publish.html'?'#hosting-pages figure':file==='07-operations.html'?(prefix==='shorts'?'#messenger-setup':'#messenger-setup figure'):file==='04-render.html'?(prefix==='shorts'?'#editorial-sample':'#editorial-sample'):null;
   const target=figure?page.locator(figure):page.locator('main figure').first();
   if(await target.count())await target.first().screenshot({path:`${out}/${prefix}-${file.slice(0,2)}-360-${theme}.png`});
  }
 }
 // Both OS tabs remain reachable by keyboard.
 await page.goto(`${origin}/${prefix}/advanced/${files.find(f=>f.startsWith('03-'))}`);
 const tabs=page.locator('[data-os-tab]');
 for(const tab of await tabs.all()){
  await tab.focus();await page.keyboard.press('Enter');
  const id=await tab.getAttribute('aria-controls');
  expect(prefix+' OS tab '+id,await page.locator('#'+id).isVisible());
 }
 const quiz=page.locator('[data-quiz] [data-question]').first();
 const right=quiz.locator('button[data-correct="true"]');
 await right.focus();await page.keyboard.press('Enter');
 expect(prefix+' quiz keyboard',await right.getAttribute('disabled')!==null||await right.getAttribute('aria-pressed')==='true');
 // Checks persist on reload and reset with Space/Enter.
 await page.goto(`${origin}/${prefix}/advanced/e2e.html`);
 const check=page.locator('[data-advanced-check]').first();
 if(await check.isChecked())await check.uncheck();
 await check.focus();await page.keyboard.press('Space');await page.reload();
 expect(prefix+' checkbox saved',await page.locator('[data-advanced-check]').first().isChecked());
 const reset=page.locator('[data-advanced-reset]');await reset.focus();await page.keyboard.press('Enter');
 expect(prefix+' checklist reset',await page.locator('[data-advanced-check]:checked').count()===0);
 await page.goto(`${origin}/${prefix}/advanced/04-render.html`);
 const editorial=page.locator('video').filter({has:page.locator('source[src*="editorial"]')});
 const videos=await page.locator('video').all();
 for(const video of videos){
  await video.evaluate(v=>{v.muted=true;v.load();});
  await video.evaluate(v=>new Promise((resolve,reject)=>{if(v.readyState>=1)resolve();else{v.addEventListener('loadedmetadata',resolve,{once:true});v.addEventListener('error',()=>reject(new Error('video metadata error')),{once:true});}}));
  const src=await video.getAttribute('src')||await video.locator('source').first().getAttribute('src');
  await video.evaluate(v=>v.play());await page.waitForTimeout(300);
  expect(prefix+' video playback '+src,await video.evaluate(v=>v.currentTime>0),{duration:await video.evaluate(v=>v.duration)});
  await video.evaluate(v=>v.pause());
 }
}
// Relative links are checked against the actual deployment paths, including cross-book links.
for(const href of links){
 const u=new URL(href);const response=await context.request.get(href.split('#')[0]);
 if(!response.ok())errors.push({type:'link',href,status:response.status()});
 else if(u.hash){const body=await response.text();const id=decodeURIComponent(u.hash.slice(1));if(!body.includes(`id="${id}"`)&&!body.includes(`id='${id}'`))errors.push({type:'anchor',href});}
}
await page.goto(origin+'/shorts/advanced/02-credentials.html');
const extreme=page.locator('[data-cost-preset="extreme"]');await extreme.focus();await page.keyboard.press('Enter');
expect('shorts cost extreme',(await page.locator('#cost-result').textContent()).includes('초과'));
expect('shorts cost HTML numbers',await page.locator('#cost-breakdown').evaluate(e=>parseFloat(getComputedStyle(e).fontSize)>=14));
await page.goto(origin+'/reels/advanced/02-keys.html');
await page.locator('[data-cost-extreme]').focus();await page.keyboard.press('Enter');
expect('reels cost extreme',(await page.locator('#monthly-cost').textContent()).includes('넘어요'));
await page.goto(origin+'/shorts/advanced/06-gates.html');
await page.locator('#gate-mode').selectOption('auto');
await page.locator('#gate-case').focus();await page.keyboard.press('Home');await page.keyboard.press('ArrowDown');await page.keyboard.press('Enter');
expect('gate keyboard failure never auto publishes',(await page.locator('#gate-result').textContent()).includes('예외'));
await page.goto(origin+'/shorts/advanced/07-operations.html');
await page.locator('#runner-pc').selectOption('no');await page.locator('#runner-state').selectOption('no');
expect('cloud without state refused',(await page.locator('#runner-result').textContent()).includes('로컬'));
const summary={screens:screens.length,widths:[1280,375,360],themes:['light','dark'],internalLinks:links.size,keyboardAndMedia:interactions.length,errors,failedInteractions:interactions.filter(i=>!i.pass)};
await fs.writeFile(out+'/browser.json',JSON.stringify({summary,screens,interactions},null,2)+'\n');
console.log(JSON.stringify(summary,null,2));await browser.close();
if(errors.length||summary.failedInteractions.length)process.exitCode=1;
