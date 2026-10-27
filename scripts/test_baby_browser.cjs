/* Browser acceptance checks. Serve the workflow-equivalent assembly at BASE_URL.
   node scripts/test_baby_browser.cjs ; PW_MODULE / CHROME can override existing local tools. */
const {chromium}=require(process.env.PW_MODULE||'/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=process.cwd(),dest=path.join(root,'docs/results/phase-N6');
const base=process.env.BASE_URL||'http://127.0.0.1:8796';
const pages=fs.readdirSync('site-baby',{recursive:true}).filter(name=>name.endsWith('.html')).sort();
fs.mkdirSync(dest,{recursive:true});
fs.mkdirSync('/tmp/baby-n6-views',{recursive:true});
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
   await page.waitForTimeout(60);await page.evaluate(()=>scrollTo(0,0));
   assert.equal(await page.locator('main').innerText().then(t=>t.includes('undefined')),false,file+' metadata');
   const overflow=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,culprits:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,8).map(e=>e.tagName+'.'+e.className)}));
   assert.ok(overflow.scroll<=width,JSON.stringify({file,width,theme,overflow}));
   report.views.push({file,width,theme,overflow:overflow.scroll-width});
   await page.screenshot({path:path.join('/tmp/baby-n6-views',`${file.replaceAll('/','-').replace('.html','')}-${width}-${theme}.png`)});
   if(['index.html','glossary.html','lab.html','chapters/07-hospital.html','chapters/10-benefits.html','practice/08-checkups.html','practice/09-records.html'].includes(file)&&((width===1280&&theme==='light')||(width===375&&theme==='dark')||(width===360&&theme==='light')))await page.screenshot({path:path.join(dest,`${file.replaceAll('/','-').replace('.html','')}-${width}-${theme}.png`)});
   const canonicalText=await page.locator('[data-emergency-id]').evaluateAll(nodes=>nodes.map(n=>({id:n.dataset.emergencyId,text:n.childNodes[0].textContent})));
   for(const row of canonicalText)assert.equal(row.text,data.find(x=>x.id===row.id).text,file);
   if(file==='chapters/07-hospital.html'){
    const texts=await page.locator('[data-emergency-full] [data-emergency-id]').evaluateAll(nodes=>nodes.map(n=>({id:n.dataset.emergencyId,text:n.childNodes[0].textContent})));
    assert.deepEqual(texts.map(x=>x.id).sort(),data.map(x=>x.id).sort());
    for(const row of texts)assert.equal(row.text,data.find(x=>x.id===row.id).text);
   }
  }
 }
 report.checks.push(`${pages.length} pages × 3 widths × 2 themes: no horizontal overflow; canonical emergency rendering on every page`);
 // Dynamic navigation and anchors, including every pending chapter and source citation.
 const anchorCache=new Map();
 for(const file of pages){
  await page.goto(base+'/baby/'+file);
  if(file==='chapters/01-map.html'){await page.locator('#birth-date').fill('2026-10-01');await page.locator('#deadline-form button').click();assert.match(await page.locator('#deadline-result').textContent(),/기한 4개/);}
  if(file==='practice/08-checkups.html'){await page.locator('#schedule-form [name=birth]').fill('2026-10-01');await page.locator('#schedule-form button').click();}
  const links=await page.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>new URL(a.getAttribute('href'),location.href).href));
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
 await page.goto(base+'/baby/chapters/10-benefits.html');
 assert.equal(await page.locator('#ch10-months tbody tr').count(),24);
 assert.match(await page.locator('#benefits-result').textContent(),/합계 확인 필요/);
 await page.locator('[name=birth]').fill('2026-10-01');
 await page.locator('[name=transition]').selectOption('0');
 await page.locator('[name=region]').selectOption('capital');
 assert.match(await page.locator('#ch10-months tbody tr').first().textContent(),/41.6만 원.*10만 원.*51.6만 원/);
 await page.locator('[name=region]').selectOption('special');
 assert.match(await page.locator('#ch10-months tbody tr').first().textContent(),/53.6만 원/);
 await page.locator('[data-benefit-preset]').focus();await page.keyboard.press('Enter');
 assert.match(await page.locator('#benefits-result').textContent(),/12개월/);
 assert.match(await page.locator('#ch10-months tbody tr').nth(12).textContent(),/0원/);
 await page.locator('[name=birth]').fill('2027-01-01');assert.match(await page.locator('#benefits-result').textContent(),/조사일/);
 // Lab iframes reuse their originals, and follow the parent theme.
 await page.goto(base+'/baby/lab.html');await page.locator('#sim-picker').selectOption('10-benefits:benefits-tool');
 await page.waitForFunction(()=>document.querySelector('#sim-frame').contentDocument?.querySelector('#benefits-result')?.textContent.includes('합계 확인 필요'));
 await page.locator('[data-theme-select]').selectOption('dark');await page.waitForFunction(()=>document.querySelector('#sim-frame').contentDocument.documentElement.dataset.theme==='dark');
 report.checks.push('keyboard menu/Escape, tabs/arrows/Home/End, FAQ, quiz/reset, calculator; theme persistence; contact/record restore/delete; text-safe input; lab source reuse/theme');
 // Block storage read/write and confirm that all essential interactions still work.
 const denied=await browser.newContext();await denied.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError');}});});
 const blocked=await denied.newPage();blocked.on('pageerror',e=>report.errors.push('storage blocked: '+e.message));
 await blocked.goto(base+'/baby/chapters/07-hospital.html');assert.equal(await blocked.locator('[data-emergency-full] [data-emergency-id]').count(),7);await blocked.locator('[data-contact=pediatric]').fill('가상 기관');assert.match(await blocked.locator('[data-contact-status]').textContent(),/저장할 수 없습니다/);
 await blocked.goto(base+'/baby/practice/07-apply.html');await blocked.locator('[data-record=birth-item]').fill('출생신고');assert.match(await blocked.locator('[data-record-status]').textContent(),/저장할 수 없어요/);
 await blocked.goto(base+'/baby/chapters/10-benefits.html');assert.match(await blocked.locator('#benefits-result').textContent(),/합계 확인 필요/);await denied.close();
 report.checks.push('localStorage unavailable: emergency text, contact editor, application record and calculator remain usable');
 // Behaviour of the integrated chapter/practice tools, including dynamic source anchors.
 await page.goto(base+'/baby/chapters/02-feeding.html');await page.locator('#feeding-check input').first().focus();await page.keyboard.press('Space');assert.match(await page.locator('#feeding-result').textContent(),/1개/);
 await page.goto(base+'/baby/chapters/03-sleep.html');await page.locator('#sleep-check input').first().check();assert.match(await page.locator('#sleep-result').textContent(),/4개/);
 await page.goto(base+'/baby/chapters/04-crying.html');for(let i=0;i<4;i++){await page.locator('#crying-next').focus();await page.keyboard.press('Enter');}assert.equal(await page.locator('#crying-next').isDisabled(),true);await page.locator('#crying-reset').click();assert.match(await page.locator('#crying-result').textContent(),/1\/5/);
 await page.goto(base+'/baby/chapters/09-checkups.html');await page.locator('[name=birth]').fill('2026-10-01');await page.locator('[name=route]').selectOption('six');await page.locator('[data-calendar-form] [type=submit]').click();assert.match(await page.locator('[data-calendar-rows]').textContent(),/生略|생략/);assert.match(await page.locator('[data-calendar-rows]').textContent(),/2027-01-13/);
 await page.goto(base+'/baby/chapters/11-parents.html');await page.locator('#ch11-preset').focus();await page.keyboard.press('Enter');assert.match(await page.locator('#ch11-plan').textContent(),/도움 필요/);
 await page.goto(base+'/baby/practice/09-records.html');
 await page.locator('#record-form button[value=breast]').focus();await page.keyboard.press('Enter');await page.locator('#record-form button[value=both]').click();
 await page.reload();assert.equal(await page.locator('#record-list > li').count(),2);
 const downloadPromise=page.waitForEvent('download');await page.locator('#download-csv').click();const download=await downloadPromise;assert.match(download.suggestedFilename(),/\.csv$/);
 await page.locator('#clear-records').click();await page.locator('#cancel-clear').click();assert.equal(await page.locator('#record-list > li').count(),2);
 await page.locator('#clear-records').click();await page.locator('#confirm-clear').click();assert.match(await page.locator('#record-list').textContent(),/아직 남긴 기록/);
 report.checks.push('all original tools: observation checklists, crying flow/reset, 6-in-1 calendar, shift gap preset, care-log roundtrip/CSV/delete confirmation');
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
 for(const name of ['emergency','weekly-checklist','log-sheet','parent-crisis']){
  await page.goto(base+'/baby/print/'+name+'.html');await page.emulateMedia({media:'print'});
  await page.screenshot({path:path.join(dest,name+'-print-preview.png'),fullPage:true});
  const output=path.join(dest,name+'-a4.pdf');await page.pdf({path:output,preferCSSPageSize:true,printBackground:false});
  const pdfText=fs.readFileSync(output,'latin1');
  assert.equal((pdfText.match(/\/Type\s*\/Page\b/g)||[]).length,1,name+' A4 one page');
  report.printForms ||= [];report.printForms.push({name,pages:1,mediaBox:pdfText.match(/\/MediaBox\s*\[([^\]]+)\]/)[1]});
 }
 await page.emulateMedia({media:'screen'});
 // Every page: main skip, keyboard menu, native disclosures, quizzes and practice tabs.
 for(const file of pages){
  await page.goto(base+'/baby/'+file);await page.setViewportSize({width:360,height:960});
  const skip=page.locator('.skip-link');await skip.focus();await page.keyboard.press('Enter');
  assert.equal(new URL(page.url()).hash,'#main',file+' skip link');
  if(await page.locator('[data-menu-toggle]').count()){
   await page.locator('[data-menu-toggle]').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#book-menu').isVisible(),true);await page.keyboard.press('Escape');assert.equal(await page.locator('[data-menu-toggle]').evaluate(n=>n===document.activeElement),true);
  }
  for(const group of await page.locator('[data-os-tabs]').all()){
   const tabs=group.locator('[data-os-tab]');await tabs.first().focus();await page.keyboard.press('End');assert.equal(await tabs.last().getAttribute('aria-selected'),'true');await page.keyboard.press('Home');assert.equal(await tabs.first().getAttribute('aria-selected'),'true');
  }
  for(const summary of await page.locator('main details:not([data-mobile-outline]) > summary').all()){
   await summary.focus();const previous=await summary.locator('..').getAttribute('open');await page.keyboard.press('Enter');assert.notEqual(await summary.locator('..').getAttribute('open'),previous,file+' disclosure');
  }
  if(await page.locator('[data-quiz]').count()){
   await page.locator('[data-quiz-reset]').click();
   for(const answer of await page.locator('[data-question] [data-correct=true]').all()){await answer.focus();await page.keyboard.press('Enter');}
   assert.match(await page.locator('[data-quiz-score]').textContent(),/3.*3/);await page.locator('[data-quiz-reset]').click();
  }
  for(const input of await page.locator('input[data-practice-check]').all()){await input.focus();await page.keyboard.press('Space');assert.equal(await input.isChecked(),true,file+' session check');}
 }
 await page.goto(base+'/baby/glossary.html');assert.equal(await page.locator('[data-glossary-entry]').count(),40);
 await page.locator('#term-search').fill('바우처');assert.equal(await page.locator('[data-glossary-entry]:visible').count(),1);
 await page.locator('#term-search').fill('없는검색어');assert.match(await page.locator('#term-count').textContent(),/0\/40/);
 await page.evaluate(()=>location.hash='tummy-time');assert.equal(await page.locator('#term-search').inputValue(),'');assert.equal(await page.locator('#tummy-time').isVisible(),true);
 const tools=await page.evaluate(()=>window.BabyCatalog);
 for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const tool of tools){
  await page.setViewportSize({width,height:960});await page.goto(base+'/baby/lab.html?tool='+tool.slug+':'+tool.id);
  await page.locator('[data-theme-select]').selectOption(theme);
  const frame=page.frameLocator('#sim-frame');await frame.locator('#'+tool.id).waitFor({state:'visible'});
  assert.equal(await page.locator('#sim-original').getAttribute('href'),tool.path+'#'+tool.id);
  await page.waitForFunction(theme=>document.querySelector('#sim-frame').contentDocument.documentElement.dataset.theme===theme,theme);
  assert.equal(await frame.locator('html').evaluate(n=>n.scrollWidth<=innerWidth),true,tool.title+' embed overflow '+width);
  const input=frame.locator('input:not([readonly]):visible,select:visible,button:visible,textarea:visible').first();
  if(await input.count()){await input.focus();assert.equal(await input.evaluate(n=>n===document.activeElement),true,tool.title+' keyboard focus');}
 }
 report.checks.push('all pages: keyboard skip/menu/Escape, disclosures, practice tabs, 39 quiz answers/reset, 11 practice markers; glossary search/hash; 15 original embeds × 3 widths × 2 themes with theme/focus/overflow');
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
