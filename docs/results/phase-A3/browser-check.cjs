/* 실행: node docs/results/phase-A3/browser-check.cjs
   PW_MODULE·CHROME·BASE_URL로 로컬 검증 환경을 바꿀 수 있다. */
const {chromium}=require(process.env.PW_MODULE||'/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const assert=require('node:assert/strict');
const fs=require('node:fs');const path=require('node:path');
const root=process.cwd(), dest=path.join(root,'docs/results/phase-A3');
const base=process.env.BASE_URL||'http://127.0.0.1:8763';
const files=fs.readdirSync('site/advanced').filter(x=>x.endsWith('.html')).sort();
const report={views:[],errors:[],checks:[],links:0};
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME||'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
 try {
 const context=await browser.newContext();
 // The only third-party resource is the existing optional font CSS. Test the documented system-font fallback deterministically.
 await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({status:200,contentType:'text/css',body:''}));
 const page=await context.newPage();
 page.on('pageerror',e=>report.errors.push('page: '+e.message));
 page.on('console',m=>{if(m.type()==='error')report.errors.push('console: '+m.text());});
 page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)report.errors.push('HTTP '+r.status()+': '+r.url());});
 await page.goto(base+'/site/advanced/00-start.html');
 assert.equal(await page.evaluate(()=>localStorage.getItem('reelsbook:practice:v1')),null);
 const practiceState=JSON.stringify({version:1,checks:{'8:token':true},fields:{'posted-url':'https://example.org/my-post'}});
 await page.evaluate(value=>localStorage.setItem('reelsbook:practice:v1',value),practiceState);
 await page.goto(base+'/site/advanced/02-keys.html');
 assert.equal(await page.evaluate(()=>localStorage.getItem('reelsbook:practice:v1')),practiceState);
 await page.evaluate(()=>localStorage.removeItem('reelsbook:practice:v1'));
 report.checks.push('track isolation: advanced pages neither create nor rewrite practice storage');
 const links=new Set();
 for(const file of [...files.map(x=>'advanced/'+x),'index.html','glossary.html','credits.html','practice/02-setup.html','practice/08-api.html','practice/e2e.html']) {
  for(const width of [1280,375,360])for(const theme of ['light','dark']){
   await page.setViewportSize({width,height:900});
   await page.goto(base+'/site/'+file,{waitUntil:'domcontentloaded'});
   await page.locator('[data-theme-select]').selectOption(theme);
   await page.locator('img').evaluateAll(images=>images.forEach(im=>{im.loading='eager';}));
   await page.waitForFunction(()=>[...document.images].every(im=>im.complete));
   const problems=await page.evaluate(()=>{
    const issues=[];
    if(document.documentElement.scrollWidth>innerWidth+1)issues.push('horizontal overflow '+document.documentElement.scrollWidth);
    for(const im of document.images)if(!im.complete||!im.naturalWidth)issues.push('broken image '+im.src);
    for(const svg of document.querySelectorAll('main svg')){
     const view=svg.viewBox.baseVal;
     for(const text of svg.querySelectorAll('text')){
      const b=text.getBBox();
      if(b.x< -1||b.x+b.width>view.width+1)issues.push('SVG text clipped: '+text.textContent);
     }
    }
    return issues;
   });
   report.views.push({file,width,theme,issues:problems});
   if(problems.length)report.errors.push(file+' '+width+' '+theme+': '+problems.join('; '));
   if(width===1280&&theme==='light')for(const href of await page.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>new URL(a.getAttribute('href'),location.href).href)))if(href.startsWith(locationOrigin(base)+'/'))links.add(href);
  }
 }
 for(const href of links){
  const url=new URL(href);const response=await context.request.get(url.origin+url.pathname);
  assert(response.ok(),'link HTTP '+href);
  if(url.hash){const text=await response.text();const id=decodeURIComponent(url.hash.slice(1));assert(text.includes('id="'+id+'"')||text.includes("id='"+id+"'"),'anchor '+href);}
  report.links++;
 }
 await page.goto(base+'/site/advanced/02-keys.html');
 await page.locator('#cost-count').fill('30');assert.match(await page.locator('#monthly-cost').innerText(),/0\.02400/);
 await page.locator('#cost-provider').selectOption('sol');assert.match(await page.locator('#monthly-cost').innerText(),/0\.48000/);
 await page.locator('#cost-images').fill('1');assert.match(await page.locator('#monthly-cost').innerText(),/1\.49250/);
 await page.locator('#cost-allowance').fill('20');assert.match(await page.locator('#monthly-cost').innerText(),/1\.79100/);
 for(const val of ['', '-1','0.5','100001']){await page.locator('#cost-count').fill(val);assert.match(await page.locator('#monthly-cost').innerText(),/확인/);}
 await page.locator('[data-cost-reset]').click();await page.locator('#cost-count').fill('0');await page.locator('#cost-cap').fill('0');assert.match(await page.locator('#monthly-cost').innerText(),/0\.00000/);
 await page.locator('[data-cost-extreme]').click();assert.match(await page.locator('#monthly-cost').innerText(),/상한을 넘/);
 report.checks.push('calculator: source scenarios, allowance, empty/negative/fractional/too-large, zero cap, extreme');
 const firstTab=page.locator('[data-os-tab="windows"]').first();await firstTab.focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('[data-os-tab="macos"]').first().getAttribute('aria-selected'),'true');
 await page.keyboard.press('Home');assert.equal(await firstTab.getAttribute('aria-selected'),'true');await page.keyboard.press('End');assert.equal(await page.locator('[data-os-tab="macos"]').first().getAttribute('aria-selected'),'true');
 const q=page.locator('[data-question]').first();await q.locator('[data-correct="true"]').focus();await page.keyboard.press('Enter');assert.match(await q.locator('[data-feedback]').innerText(),/정답/);await page.locator('[data-quiz-reset]').click();assert.equal(await q.locator('[data-correct="true"]').isEnabled(),true);
 await page.locator('[data-menu-toggle]').click();assert.equal(await page.locator('#book-menu').isVisible(),true);await page.keyboard.press('Escape');assert.equal(await page.locator('#book-menu').isVisible(),false);
 report.checks.push('keyboard: OS arrows/Home/End, quiz Enter/reset, menu Escape');
 await page.locator('[data-advanced-check="a2"]').check();await page.goto(base+'/site/advanced/e2e.html');assert.equal(await page.locator('[data-advanced-check="a2"]').isChecked(),true);
 await page.evaluate(()=>localStorage.setItem('reelsbook:practice:v1','{"keep":"sentinel"}'));
 await page.locator('[data-advanced-reset]').click();assert.equal(await page.locator('[data-advanced-check="a2"]').isChecked(),false);assert.equal(await page.evaluate(()=>localStorage.getItem('reelsbook:practice:v1')),'{"keep":"sentinel"}');
 await page.evaluate(()=>localStorage.setItem('reelsbook:advanced:v1','{broken'));await page.reload();assert.match(await page.locator('[data-advanced-status]').first().innerText(),/0\/16/);
 report.checks.push('progress: chapter/E2E sync, reset keeps practice, corrupt JSON recovery');
 await page.goto(base+'/site/advanced/00-start.html');assert.equal(await page.locator('main svg a').count(),7);await page.locator('main svg a').first().focus();await page.keyboard.press('Enter');await page.waitForURL('**/01-pipeline.html');assert(page.url().includes('01-pipeline'));
 const advancedLinks=await page.locator('#book-menu a[href*="advanced/"]').count();assert.equal(advancedLinks,11);
 assert.match(await page.locator('[data-chapter-pager]').innerText(),/A0/);assert.match(await page.locator('[data-chapter-pager]').innerText(),/A2/);
 await page.goto(base+'/site/practice/08-api.html');assert.match(await page.locator('[data-chapter-title]').innerText(),/실습/);assert.doesNotMatch(await page.locator('[data-chapter-pager]').innerText(),/심화/);
 report.checks.push('navigation: SVG Enter, third track 11 links, advanced pager, practice isolation');
 const blocked=await browser.newContext();await blocked.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({status:200,contentType:'text/css',body:''}));
 await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError');}});});
 const bp=await blocked.newPage();bp.on('pageerror',e=>report.errors.push('blocked: '+e.message));await bp.goto(base+'/site/advanced/e2e.html');await bp.locator('[data-advanced-check="a0"]').check();assert.match(await bp.locator('[data-advanced-status]').innerText(),/保存|저장할 수 없/);assert.equal(await bp.locator('[data-advanced-check="a0"]').isChecked(),true);await blocked.close();
 report.checks.push('storage blocked: readable, checkbox works, notice');
 const nojs=await browser.newContext({javaScriptEnabled:false});await nojs.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({status:200,contentType:'text/css',body:''}));const np=await nojs.newPage();
 for(const f of files){await np.goto(base+'/site/advanced/'+f);assert(await np.locator('main').innerText());assert(await np.locator('a[href]').count());}
 await nojs.close();report.checks.push('all 11 pages readable with JavaScript disabled');
 for(const [file,theme,width,selector,name] of [
 ['00-start.html','light',1280,'#map','pipeline-light'],['00-start.html','dark',375,'#build','modes-dark-mobile'],['02-keys.html','dark',1280,'#calculator','cost-dark'],['04-render.html','light',375,'.adv-card-pair','cards-mobile'],['05-publish.html','light',360,'#map','sequence-mobile'],['06-gates.html','dark',375,'#map','gates-dark-mobile'],['07-operations.html','light',1280,'#build .adv-figure','operations-light'],['08-insights.html','dark',360,'#map','loop-dark-mobile'],['e2e.html','light',375,'main','e2e-mobile']]){
  await page.setViewportSize({width,height:900});await page.goto(base+'/site/advanced/'+file);await page.locator('[data-theme-select]').selectOption(theme);await page.locator('[data-site-header]').evaluate(el=>{el.style.position='static';});await page.locator(selector).first().screenshot({path:path.join(dest,name+'.png')});
 }
 for(const [width,theme,name] of [[1280,'light','cover-light'],[375,'dark','cover-dark-mobile']]){await page.setViewportSize({width,height:900});await page.goto(base+'/site/advanced/00-start.html');await page.locator('[data-theme-select]').selectOption(theme);await page.screenshot({path:path.join(dest,name+'.png')});}
 assert.equal(report.errors.length,0,report.errors.join('\n'));
 report.passed=true;
 }finally{fs.writeFileSync(path.join(dest,'browser-check.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}
 console.log(JSON.stringify({views:report.views.length,links:report.links,checks:report.checks.length,errors:report.errors}));
})().catch(e=>{console.error(e);process.exitCode=1;});
function locationOrigin(value){return new URL(value).origin;}
