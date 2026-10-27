/* BASE_URL=http://127.0.0.1:8786 node docs/results/phase-N4c/browser-check.cjs */
const {chromium}=require(process.env.PW_MODULE||'/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.BASE_URL||'http://127.0.0.1:8786',dest=__dirname,report={views:[],errors:[],checks:[],links:0,externalRequests:[]};
const files=['10-benefits','11-parents','12-safety','13-hundred-days'],canonical=require('../../../site-baby/assets/emergency-data.js');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME||'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
 try{
 const context=await browser.newContext(),page=await context.newPage();
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());});page.on('response',r=>{if(r.status()>=400)report.errors.push(r.status()+' '+r.url());});
 context.on('request',r=>{if(!r.url().startsWith(base)&&!r.url().startsWith('data:'))report.externalRequests.push(r.url());});
 for(const width of [375,1280,360])for(const theme of ['light','dark'])for(const slug of files){
  await page.setViewportSize({width,height:960});await page.goto(`${base}/site-baby/chapters/${slug}.html`);await page.locator('[data-theme-select]').selectOption(theme);
  assert.equal(await page.locator('[data-block]').count(),9);assert.equal(await page.locator('.chapter-faq details').count(),5);assert.equal(await page.locator('[data-question]').count(),3);
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);assert.equal(overflow,0,`${slug} ${width} ${theme}`);
  assert.ok(await page.locator('[data-chapter-meta]').innerText(),slug+' metadata missing');
  for(const figure of await page.locator('svg').all()){
   const bad=await figure.evaluate(svg=>{const box=svg.viewBox.baseVal;return [...svg.querySelectorAll('text')].filter(t=>{const r=t.getBBox();return r.x<box.x-1||r.x+r.width>box.width+1||r.y+r.height>box.height+1;}).map(t=>t.textContent);});
   assert.deepEqual(bad,[],`${slug}: SVG text clipped`);
  }
  if(width!==360)await page.screenshot({path:path.join(dest,`${slug}-${width}-${theme}.png`)});
  const detail=slug==='10-benefits'?'#benefits-tool':slug==='11-parents'?'#sleep-shifts':slug==='12-safety'?'#car .baby-figure':null;
  if(detail&&width!==360)await page.locator(detail).screenshot({path:path.join(dest,`${slug}-detail-${width}-${theme}.png`),style:'.site-header,.skip-link{visibility:hidden!important}'});
  report.views.push({slug,width,theme,overflow});
 }
 report.checks.push('4 chapters × 3 widths × 2 themes; 9 blocks, FAQ5, quiz3; SVG text bounds; screenshots at 375/1280');
 const cache=new Map();
 for(const slug of files){await page.goto(`${base}/site-baby/chapters/${slug}.html`);
  for(const url of [...new Set(await page.locator('a[href]').evaluateAll(as=>as.map(a=>a.href)))].filter(u=>u.startsWith(base))){
   const parsed=new URL(url),key=parsed.origin+parsed.pathname+parsed.search;
   if(!cache.has(key)){const other=await context.newPage(),r=await other.goto(key);assert.equal(r.status(),200,key);cache.set(key,await other.locator('[id]').evaluateAll(es=>es.map(e=>e.id)));await other.close();}
   if(parsed.hash)assert.ok(cache.get(key).includes(decodeURIComponent(parsed.hash.slice(1))),url);report.links++;
  }
  const faq=page.locator('.chapter-faq summary').first();await faq.focus();await page.keyboard.press('Enter');assert.equal(await faq.locator('..').getAttribute('open'),'');
  for(const b of await page.locator('[data-question] [data-correct=true]').all()){await b.focus();await page.keyboard.press('Enter');}
  assert.match(await page.locator('[data-quiz-score]').innerText(),/3/);await page.locator('[data-quiz-reset]').click();
  for(const message of await page.locator('[data-emergency-id]').all()){const id=await message.getAttribute('data-emergency-id');const text=await message.evaluate(el=>el.childNodes[0].textContent);assert.equal(text,canonical.find(r=>r.id===id).text);}
 }
 report.checks.push('rendered internal links/anchors, keyboard FAQ/quiz/reset; emergency messages equal shared data');
 await page.goto(`${base}/site-baby/chapters/10-benefits.html`);
 assert.equal(await page.locator('#ch10-months tbody tr').count(),24);assert.match(await page.locator('#benefits-result').innerText(),/합계 확인 필요/);
 await page.locator('[name=region]').selectOption('capital');await page.locator('[name=transition]').selectOption('6');
 assert.match(await page.locator('#ch10-months tbody tr').nth(5).innerText(),/110만 원/);assert.match(await page.locator('#ch10-months tbody tr').nth(6).innerText(),/51.6만 원/);assert.match(await page.locator('#ch10-months tbody tr').nth(12).innerText(),/51.5만 원/);
 await page.locator('[data-benefit-preset]').focus();await page.keyboard.press('Enter');assert.match(await page.locator('#ch10-months tbody tr').nth(12).innerText(),/0원/);assert.match(await page.locator('[data-benefit-preset]').innerText(),/1세·어린이집/);
 
 await page.locator('[name=birth]').fill('2027-01-01');assert.equal(await page.locator('#ch10-months tbody tr').count(),0);assert.match(await page.locator('#benefits-result').innerText(),/조사일/);
 await page.locator('[name=birth]').fill('2026-01-31');assert.match(await page.locator('#ch10-months tbody tr').nth(1).innerText(),/2026-02-28/);
 const scroll=page.locator('#ch10-months [role=region]');await scroll.focus();assert.equal(await scroll.evaluate(el=>document.activeElement===el),true);
 await page.goto(`${base}/site-baby/chapters/11-parents.html`);assert.match(await page.locator('#ch11-result').innerText(),/4시간/);
 await page.locator('#ch11-preset').focus();await page.keyboard.press('Enter');assert.match(await page.locator('#ch11-plan').innerText(),/도움 필요/);
 await page.locator('[name=aEnd]').fill('18:00');assert.match(await page.locator('#ch11-result').innerText(),/끝 시각/);assert.equal(await page.locator('#ch11-plan').innerText(),'');
 assert.equal(await page.locator('[href="tel:109"]').count(),1);assert.equal(await page.locator('[href="tel:15770199"]').count(),1);assert.equal(await page.locator('[href="tel:16447373"]').count(),1);
 report.checks.push('24 monthly rows; transition 5/6/12 months; 1-year daycare preset; month-end dates; invalid date clears stale output; keyboard table focus; sleep default/gaps/invalid input; crisis phone links');
 const denied=await browser.newContext();await denied.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked');}}));
 const blocked=await denied.newPage();blocked.on('pageerror',e=>report.errors.push('storage blocked '+e.message));
 for(const slug of ['10-benefits','11-parents']){await blocked.goto(`${base}/site-baby/chapters/${slug}.html`);assert.ok(await blocked.locator(slug==='10-benefits'?'#benefits-result':'#ch11-result').innerText());}await denied.close();
 const nojs=await browser.newContext({javaScriptEnabled:false}),plain=await nojs.newPage();
 for(const slug of files){await plain.goto(`${base}/site-baby/chapters/${slug}.html`);assert.equal(await plain.locator('.axis-block').count(),slug==='10-benefits'?6:slug==='12-safety'?5:4);assert.equal(await plain.locator('.chapter-faq details').count(),5);}await nojs.close();
 report.checks.push('storage blocked tools remain usable; JS disabled axes/FAQ/sources remain readable');
 assert.deepEqual(report.externalRequests,[]);assert.deepEqual(report.errors,[]);await context.close();
 }finally{await browser.close();fs.writeFileSync(path.join(dest,'browser-report.json'),JSON.stringify(report,null,2)+'\n');}
 console.log(JSON.stringify({views:report.views.length,links:report.links,checks:report.checks,errors:report.errors},null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
