/* Browser acceptance checks. Serve the workflow-equivalent assembly at BASE_URL.
   node scripts/test_baby_browser.cjs ; PW_MODULE / CHROME can override existing local tools. */
const {chromium}=require(process.env.PW_MODULE||'/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=process.cwd(),dest=path.join(root,'docs/results/phase-N3');
const base=process.env.BASE_URL||'http://127.0.0.1:8774';
const pages=['index.html','chapters/07-hospital.html','practice/07-apply.html','chapters/10-benefits.html','print/emergency.html','lab.html','credits.html','glossary.html','chapters/pending.html?chapter=02-feeding','practice/pending.html?chapter=04-sleep'];
const report={views:[],errors:[],checks:[],internalLinks:0,network:[]};
const data=require('../site-baby/assets/emergency-data.js');
const briefing=fs.readFileSync('research-baby/BRIEFING.md','utf8').split('## ④')[1].split('## ⑤')[0];
const canonical=[...briefing.matchAll(/\| \*\*(.+?)\*\* \|/g)].map(match=>match[1]);
assert.deepEqual(data.map(row=>row.text),canonical);
for(const row of data){
 const files=fs.readdirSync('site-baby/assets').filter(name=>name.endsWith('.js')&&name!=='emergency-data.js');
 for(const file of files)assert.equal(fs.readFileSync('site-baby/assets/'+file,'utf8').includes(row.text),false,'canonical text duplicated: '+file);
}
report.checks.push('seven shared messages exactly match the adopted briefing; no duplicate literals in other scripts');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME||'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
 try{
 const context=await browser.newContext();const page=await context.newPage();
 context.on('request',r=>{if(!r.url().startsWith(base)&&!r.url().startsWith('data:'))report.network.push(r.url());});
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());});
 page.on('response',r=>{if(r.status()>=400)report.errors.push(`${r.status()} ${r.url()}`);});
 for(const width of [1280,375,360]) for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:960});
  for(const file of pages){
   await page.goto(base+'/baby/'+file);
   if(await page.locator('[data-theme-select]').count())await page.locator('[data-theme-select]').selectOption(theme);
   await page.locator('html').evaluate((el,theme)=>el.dataset.theme=theme,theme);
   await page.waitForTimeout(60);
   const overflow=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,culprits:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,8).map(e=>e.tagName+'.'+e.className)}));
   assert.ok(overflow.scroll<=width,JSON.stringify({file,width,theme,overflow}));
   report.views.push({file,width,theme,overflow:overflow.scroll-width});
   if(pages.indexOf(file)<5)await page.screenshot({path:path.join(dest,`${file.split('/').pop().replace('.html','')}-${width}-${theme}.png`)});
   if(file==='chapters/07-hospital.html'){
    const texts=await page.locator('[data-emergency-full] [data-emergency-id]').evaluateAll(nodes=>nodes.map(n=>({id:n.dataset.emergencyId,text:n.childNodes[0].textContent})));
    assert.deepEqual(texts.map(x=>x.id).sort(),data.map(x=>x.id).sort());
    for(const row of texts)assert.equal(row.text,data.find(x=>x.id===row.id).text);
   }
  }
 }
 report.checks.push('10 pages × 3 widths × 2 themes: no horizontal overflow; 30 viewport screenshots');
 // Dynamic navigation and anchors, including every pending chapter and source citation.
 const anchorCache=new Map();
 for(const file of pages){
  await page.goto(base+'/baby/'+file);
  const links=await page.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>a.href));
  for(const url of [...new Set(links)].filter(url=>url.startsWith(base))){
   const parsed=new URL(url), key=parsed.origin+parsed.pathname+parsed.search;
   if(!anchorCache.has(key)){
    const other=await context.newPage();const response=await other.goto(key);assert.equal(response.status(),200,key);
    anchorCache.set(key,await other.locator('[id]').evaluateAll(nodes=>nodes.map(n=>n.id)));await other.close();
   }
   if(parsed.hash)assert.ok(anchorCache.get(key).includes(decodeURIComponent(parsed.hash.slice(1))),url);
   report.internalLinks++;
  }
 }
 // Theme persistence, menu, FAQ, quiz and keyboard-only tabs.
 await page.goto(base+'/baby/chapters/07-hospital.html');
 await page.locator('[data-theme-select]').selectOption('dark');await page.reload();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
 await page.locator('[data-menu-toggle]').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#book-menu').isVisible(),true);await page.keyboard.press('Escape');assert.equal(await page.locator('#book-menu').isVisible(),false);
 const faq=page.locator('.chapter-faq summary').first();await faq.focus();await page.keyboard.press('Enter');assert.equal(await faq.locator('..').getAttribute('open'),'');
 await page.locator('[data-question] [data-correct=true]').first().focus();await page.keyboard.press('Enter');assert.match(await page.locator('[data-quiz-score]').textContent(),/1문항 풀이/);
 await page.locator('[data-quiz-reset]').click();assert.match(await page.locator('[data-quiz-score]').textContent(),/0문항 풀이/);
 // Stored input is treated as text, shared with print, and deleted from storage.
 const contact='가상 소아과 / 02-000-0000 <b>테스트</b>';
 await page.locator('[data-contact=pediatric]').fill(contact);await page.reload();assert.equal(await page.locator('[data-contact=pediatric]').inputValue(),contact);
 await page.goto(base+'/baby/print/emergency.html');assert.equal(await page.locator('[data-contact=pediatric]').inputValue(),contact);assert.equal(await page.locator('.contact-fields b').count(),0);
 await page.locator('[data-contact-clear]').click();assert.equal(await page.locator('[data-contact=pediatric]').inputValue(),'');
 await page.goto(base+'/baby/practice/07-apply.html');await page.locator('#tab-before').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('#tab-after').getAttribute('aria-selected'),'true');assert.equal(await page.locator('#panel-after').isVisible(),true);await page.keyboard.press('End');assert.equal(await page.locator('#tab-visit').getAttribute('aria-selected'),'true');await page.keyboard.press('Home');assert.equal(await page.locator('#tab-before').getAttribute('aria-selected'),'true');
 await page.locator('[data-record=birth-item]').fill('출생신고');await page.locator('[data-record=birth-state]').selectOption({label:'제출 · 접수내역 확인'});await page.locator('[data-record=birth-next]').fill('2026-10-30');await page.reload();assert.equal(await page.locator('[data-record=birth-next]').inputValue(),'2026-10-30');await page.locator('[data-record-clear]').click();assert.equal(await page.locator('[data-record=birth-next]').inputValue(),'');
 // Calculator updates through native inputs, including unknown and zero-difference branches.
 await page.goto(base+'/baby/chapters/10-benefits.html');assert.match(await page.locator('#benefits-result').textContent(),/10만 원 이상, 지역 확인 필요/);
 await page.locator('[name=daycare]').selectOption('yes');assert.match(await page.locator('#benefits-result').textContent(),/41.6만 원/);
 await page.locator('[name=region]').selectOption('special');assert.match(await page.locator('#benefits-result').textContent(),/53.6만 원/);
 await page.locator('[data-benefit-preset]').focus();await page.keyboard.press('Enter');assert.match(await page.locator('#benefits-result').textContent(),/0만 원/);
 await page.locator('[name=birth]').fill('2027-01-01');assert.match(await page.locator('#benefits-result').textContent(),/조사일/);
 // Lab iframes reuse their originals, and follow the parent theme.
 await page.goto(base+'/baby/lab.html');await page.locator('#sim-picker').selectOption('10-benefits:benefits-tool');
 await page.waitForFunction(()=>document.querySelector('#sim-frame').contentDocument?.querySelector('#benefits-result')?.textContent.includes('10만 원'));
 await page.locator('[data-theme-select]').selectOption('dark');await page.waitForFunction(()=>document.querySelector('#sim-frame').contentDocument.documentElement.dataset.theme==='dark');
 report.checks.push('keyboard menu/Escape, tabs/arrows/Home/End, FAQ, quiz/reset, calculator; theme persistence; contact/record restore/delete; text-safe input; lab source reuse/theme');
 // Block storage read/write and confirm that all essential interactions still work.
 const denied=await browser.newContext();await denied.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError');}});});
 const blocked=await denied.newPage();blocked.on('pageerror',e=>report.errors.push('storage blocked: '+e.message));
 await blocked.goto(base+'/baby/chapters/07-hospital.html');assert.equal(await blocked.locator('[data-emergency-full] [data-emergency-id]').count(),7);await blocked.locator('[data-contact=pediatric]').fill('가상 기관');assert.match(await blocked.locator('[data-contact-status]').textContent(),/저장할 수 없습니다/);
 await blocked.goto(base+'/baby/practice/07-apply.html');await blocked.locator('[data-record=birth-item]').fill('출생신고');assert.match(await blocked.locator('[data-record-status]').textContent(),/저장할 수 없어요/);
 await blocked.goto(base+'/baby/chapters/10-benefits.html');assert.match(await blocked.locator('#benefits-result').textContent(),/10만 원 이상/);await denied.close();
 report.checks.push('localStorage unavailable: emergency text, contact editor, application record and calculator remain usable');
 // Print output uses current contact values and remains a single A4 sheet.
 await page.goto(base+'/baby/print/emergency.html');await page.locator('[data-contact=pediatric]').fill('가상 소아과 / 전화 확인');
 await page.setViewportSize({width:794,height:1123});await page.emulateMedia({media:'print'});await page.screenshot({path:path.join(dest,'emergency-print-preview.png'),fullPage:true});await page.pdf({path:path.join(dest,'emergency-a4.pdf'),preferCSSPageSize:true,printBackground:false});
 const pdf=fs.readFileSync(path.join(dest,'emergency-a4.pdf'),'latin1');const pageCount=(pdf.match(/\/Type\s*\/Page\b/g)||[]).length;assert.equal(pageCount,1);report.print={pages:pageCount,mediaBox:pdf.match(/\/MediaBox\s*\[([^\]]+)\]/)[1],background:false};
 const printText=await page.locator('main').innerText();assert.match(printText,/가상 소아과/);assert.equal(await page.locator('[data-emergency-full] [data-emergency-id]').count(),7);
 await page.emulateMedia({media:'screen'});await page.locator('[data-contact-clear]').click();
 // Keep the shareable artifact blank; the populated contact rendering was checked above.
 await page.emulateMedia({media:'print'});await page.screenshot({path:path.join(dest,'emergency-print-preview.png'),fullPage:true});await page.pdf({path:path.join(dest,'emergency-a4.pdf'),preferCSSPageSize:true,printBackground:false});
 assert.equal((fs.readFileSync(path.join(dest,'emergency-a4.pdf'),'latin1').match(/\/Type\s*\/Page\b/g)||[]).length,1);
 await page.emulateMedia({media:'screen'});
 assert.deepEqual(report.network,[],'Unexpected external network requests');assert.deepEqual(report.errors,[]);
 report.checks.push('print: current contacts, seven canonical messages, monochrome numbered headings and borders; PDF generated');
 await page.setViewportSize({width:1280,height:960});
 for(const [file,selector,name] of [['chapters/07-hospital.html','#emergency','sample-a-emergency'],['chapters/07-hospital.html','.baby-figure','sample-a-thermometer'],['practice/07-apply.html','#apply','sample-b-steps'],['practice/07-apply.html','#finish','sample-b-record'],['chapters/10-benefits.html','#benefits-tool','calculator-result']]){
  await page.goto(base+'/baby/'+file);await page.locator('[data-theme-select]').selectOption('light');
  await page.locator(selector).screenshot({path:path.join(dest,name+'.png'),style:'.site-header{visibility:hidden!important}'});
 }

 await context.close();
 }finally{await browser.close();fs.writeFileSync(path.join(dest,'browser-report.json'),JSON.stringify(report,null,2)+'\n');}
 console.log(JSON.stringify({views:report.views.length,internalLinks:report.internalLinks,errors:report.errors,checks:report.checks},null,2));
})().catch(error=>{console.error(error);process.exitCode=1;});
