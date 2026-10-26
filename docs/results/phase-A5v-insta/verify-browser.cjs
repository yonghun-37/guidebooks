/* 저장소 루트에서 로컬 서버를 연 뒤 node docs/results/phase-A5v-insta/verify-browser.cjs.
   BASE_URL, PW_MODULE, CHROME으로 환경 변경 가능. */
const {chromium}=require(process.env.PW_MODULE||'/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const fs=require('node:fs');const assert=require('node:assert/strict');
const base=process.env.BASE_URL||'http://127.0.0.1:8768',dest='docs/results/phase-A5v-insta';
const files=fs.readdirSync('site/advanced').filter(f=>f.endsWith('.html')).sort();
const result={views:[],screenshots:[],errors:[],links:0,keyboardLinks:[],checks:[]};
const cleanScreenshot='[data-site-header], .skip-link { visibility: hidden !important; }';
(async()=>{
const browser=await chromium.launch({executablePath:process.env.CHROME||'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
try{
 const ctx=await browser.newContext();
 // Existing optional CDN font: verify the site's supported system-font fallback deterministically.
 await ctx.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({status:200,contentType:'text/css',body:''}));
 const page=await ctx.newPage();page.on('pageerror',e=>result.errors.push('page: '+e.message));page.on('console',m=>{if(m.type()==='error')result.errors.push('console: '+m.text())});
 page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)result.errors.push('HTTP '+r.status()+' '+r.url())});
 const links=new Set();
 for(const file of files)for(const width of [1280,375,360])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:900});await page.goto(base+'/site/advanced/'+file,{waitUntil:'domcontentloaded'});
  await page.locator('[data-theme-select]').selectOption(theme);await page.evaluate(()=>document.activeElement.blur());
  await page.locator('img').evaluateAll(imgs=>imgs.forEach(i=>i.loading='eager'));
  await page.waitForFunction(()=>[...document.images].every(i=>i.complete));
  const report=await page.evaluate(()=>{
   const errors=[];let minTextPx=Infinity;
   if(document.documentElement.scrollWidth>innerWidth+1)errors.push('page overflow');
   for(const img of document.images)if(!img.naturalWidth)errors.push('broken image '+img.src);
   for(const figure of document.querySelectorAll('main figure')){
    if(!figure.querySelector('figcaption')?.textContent.trim())errors.push('missing figcaption');
   }
   for(const svg of document.querySelectorAll('main svg')){
    const v=svg.viewBox.baseVal,scale=svg.getBoundingClientRect().width/v.width;
    for(const text of svg.querySelectorAll('text')){
     const b=text.getBBox(),size=parseFloat(getComputedStyle(text).fontSize)*scale;
     minTextPx=Math.min(minTextPx,size);
     if(b.x< -1||b.x+b.width>v.width+1||b.y< -1||b.y+b.height>v.height+1)errors.push('SVG clipped: '+text.textContent);
     if(size<13)errors.push('text below 13px: '+text.textContent+' '+size);
    }
   }
   // New diagrams must inherit theme colors rather than retaining literal light backgrounds.
   const sample=document.querySelector('.vi-svg .vi-box');
   return {errors,minTextPx,boxFill:sample?getComputedStyle(sample).fill:null,theme:document.documentElement.dataset.theme};
  });
  result.views.push({file,width,theme,...report});result.errors.push(...report.errors.map(e=>file+' '+width+' '+theme+': '+e));
  if(report.theme!==theme)result.errors.push(file+': theme mismatch');
  if(width===1280&&theme==='light')for(const href of await page.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>new URL(a.getAttribute('href'),location.href).href)))if(href.startsWith(base+'/'))links.add(href);
  // Each new figure gets desktop light + narrow dark evidence; the complete matrix is checked above.
  if((width===1280&&theme==='light')||(width===360&&theme==='dark')){
   const figures=page.locator('figure[id^="visual-"]');
   for(let n=0;n<await figures.count();n++){
    const f=figures.nth(n),id=await f.getAttribute('id');
    const path=dest+'/'+file.replace('.html','')+'-'+id+'-'+width+'-'+theme+'.png';
    await f.screenshot({path,style:cleanScreenshot});result.screenshots.push(path);
   }
  }
 }
 for(const href of links){
  const u=new URL(href),r=await ctx.request.get(u.origin+u.pathname);if(!r.ok()){result.errors.push('link '+href);continue;}
  if(u.hash){const text=await r.text(),id=decodeURIComponent(u.hash.slice(1));if(!text.includes('id="'+id+'"')&&!text.includes("id='"+id+"'"))result.errors.push('anchor '+href);}
  result.links++;
 }
 await page.setViewportSize({width:360,height:900});
 await page.goto(base+'/site/advanced/00-start.html');
 const hrefs=await page.locator('#visual-system svg a').evaluateAll(as=>as.map(a=>a.getAttribute('href')));
 for(let n=0;n<hrefs.length;n++){
  await page.goto(base+'/site/advanced/00-start.html');await page.locator('#visual-system svg a').nth(n).focus();
  await page.keyboard.press('Enter');await page.waitForURL('**/'+hrefs[n]);result.keyboardLinks.push(hrefs[n]);
 }
 result.checks.push('all system map nodes: focus + Enter reaches the matching chapter');
 // Existing chapter controls should still work after inserting the large figures.
 await page.goto(base+'/site/advanced/02-keys.html');await page.locator('[data-cost-reset]').click();
 assert.match(await page.locator('#monthly-cost').innerText(),/0\.02400/);await page.locator('#cost-provider').selectOption('sol');await page.locator('#cost-images').fill('1');
 assert.match(await page.locator('#monthly-cost').innerText(),/1\.49250/);result.checks.push('calculator source scenarios retained');
 const tab=page.locator('[data-os-tab="windows"]').first();await tab.focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('[data-os-tab="macos"]').first().getAttribute('aria-selected'),'true');
 const q=page.locator('[data-question]').first();await q.locator('[data-correct="true"]').focus();await page.keyboard.press('Enter');assert.match(await q.locator('[data-feedback]').innerText(),/정답/);
 result.checks.push('OS keyboard tabs + quiz retained');
 // A0 extra 375px captures complete all three widths in the saved screenshot set.
 for(const theme of ['light','dark']){
  await page.setViewportSize({width:375,height:900});await page.goto(base+'/site/advanced/00-start.html');await page.locator('[data-theme-select]').selectOption(theme);
  const path=dest+'/system-375-'+theme+'.png';await page.locator('#visual-system').screenshot({path,style:cleanScreenshot});result.screenshots.push(path);
 }
 // JS disabled: inline SVG, real images and explanations remain available.
 const nojs=await browser.newContext({javaScriptEnabled:false});await nojs.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({status:200,body:''}));const np=await nojs.newPage();
 for(const file of files){await np.goto(base+'/site/advanced/'+file);assert(await np.locator('main').isVisible());if(file!=='e2e.html')assert(await np.locator('figure').count()>0);}
 await nojs.close();result.checks.push('all 11 pages readable with JavaScript disabled');
}catch(e){result.errors.push(e.stack||String(e));}
finally{
 await browser.close();fs.writeFileSync(dest+'/browser-check.json',JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({views:result.views.length,links:result.links,keyboardLinks:result.keyboardLinks.length,screenshots:result.screenshots.length,errors:result.errors},null,2));
 if(result.errors.length)process.exitCode=1;
}
})();
