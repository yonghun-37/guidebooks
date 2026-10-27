/* Run from repository root: node docs/results/phase-N5/verify-browser.cjs
   Serve root at BASE_URL (default localhost:8785). Uses installed Playwright/Chromium. */
const {chromium}=require(process.env.PW_MODULE||'/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const dest=__dirname,base=(process.env.BASE_URL||'http://127.0.0.1:8785')+'/site-baby/';
const owned=['00-start','01-home','02-diaper','03-feeding','04-sleep','05-bath','06-emergency','08-checkups','09-records','10-play','e2e'].map(x=>'practice/'+x+'.html').concat(['weekly-checklist','log-sheet','parent-crisis','emergency'].map(x=>'print/'+x+'.html'));
const report={views:[],checks:[],errors:[],links:[],pdf:[]};
const data=require('../../../site-baby/assets/emergency-data.js');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME||'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
 const context=await browser.newContext({timezoneId:'Asia/Seoul'}),page=await context.newPage();
 page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text())});
 page.on('response',r=>{if(r.status()>=400&&r.url().startsWith(base))report.errors.push(r.status()+' '+r.url())});
 const anchorCache=new Map();
 for(const file of owned){
  for(const width of [375,1280])for(const theme of ['light','dark']){
   await page.setViewportSize({width,height:900});await page.goto(base+file);await page.evaluate(t=>{document.documentElement.dataset.theme=t;localStorage.setItem('theme',t)},theme);
   await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(80);
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
   assert.equal(overflow,false,file+' overflow '+width+' '+theme);
   await page.screenshot({path:path.join(dest,file.replace('/','-').replace('.html','')+'-'+width+'-'+theme+'.png')});
   const texts=await page.locator('[data-emergency-id]').evaluateAll(ns=>ns.map(n=>({id:n.dataset.emergencyId,text:n.childNodes[0].textContent})));
   for(const row of texts)assert.equal(row.text,data.find(x=>x.id===row.id).text,'canonical '+file+' '+row.id);
   report.views.push({file,width,theme,overflow});
  }
  const links=await page.locator('main a[href]').evaluateAll(ns=>ns.map(n=>n.getAttribute('href')));
  for(const href of [...new Set(links)]){
   if(/^(https?:|mailto:|tel:)/.test(href))continue;
   const u=new URL(href,base+file),res=await context.request.get(u.href.split('#')[0]);
   assert.equal(res.ok(),true,'internal file '+href+' from '+file);
   if(u.hash){
    const location=u.href.split('#')[0];if(!anchorCache.has(location))anchorCache.set(location,await res.text());
    const exists=anchorCache.get(location).includes('id="'+decodeURIComponent(u.hash.slice(1))+'"');
    if(!exists)report.links.push({from:file,href,reason:'anchor missing; common credits integration pending'});
   }
  }
 }
 report.checks.push('15 pages × 2 widths × 2 themes; no overflow; exact emergency strings; 60 screenshots');
 // Tabs are usable with a keyboard and reveal the matching panel.
 await page.goto(base+'practice/03-feeding.html');await page.locator('#tab-breast').focus();await page.keyboard.press('ArrowRight');
 assert.equal(await page.locator('#tab-formula').getAttribute('aria-selected'),'true');assert.equal(await page.locator('#panel-breast').isVisible(),false);assert.equal(await page.locator('#panel-formula').isVisible(),true);
 await page.keyboard.press('Home');assert.equal(await page.locator('#tab-breast').getAttribute('aria-selected'),'true');
 report.checks.push('feeding tabs: ArrowRight and Home activate matching visible panel');
 // Contacts are the same component/storage as the theory sample and print sheet.
 await page.goto(base+'practice/00-start.html');await page.locator('[data-contact="pediatric"]').fill('가상기관 02-000-0000');
 await page.goto(base+'practice/06-emergency.html');assert.equal(await page.locator('[data-contact="pediatric"]').inputValue(),'가상기관 02-000-0000');
 await page.goto(base+'print/emergency.html');assert.equal(await page.locator('[data-contact="pediatric"]').inputValue(),'가상기관 02-000-0000');await page.locator('[data-contact-clear]').click();
 report.checks.push('contacts restored across practice 0, practice 6, and emergency print; clear works');
 // Calendar months, leap day, week/day cap, unknown and individual pathways.
 await page.goto(base+'practice/08-checkups.html');
 async function schedule(birth,route){await page.locator('[name=birth]').fill(birth);await page.locator('[name=route]').selectOption(route);await page.locator('#schedule-form button').click();return page.locator('#schedule-result').innerText();}
 let output=await schedule('2024-01-31','single');assert.match(output,/2024-02-29/);assert.match(output,/2024-03-31/);assert.match(output,/2024-05-14/);assert.match(output,/1개월/);
 output=await schedule('2024-02-29','six');assert.match(output,/2024-04-29/);assert.match(output,/1개월 B형간염 생략/);assert.match(output,/2024-06-12/);
 output=await schedule('2026-08-31','unknown');assert.match(output,/아직 경로/);assert.doesNotMatch(output,/B형간염 단독 · 1개월/);
 output=await schedule('2026-08-31','individual');assert.match(output,/개별 계획/);
 output=await schedule('2099-01-01','single');assert.match(output,/실제 생년월일/);
 await page.locator('#booking-record [name=clinic]').fill('가상 예약기관');await page.locator('#booking-record [name=state]').selectOption('통화함 · 예약 대기');await page.reload();
 assert.equal(await page.locator('#booking-record [name=clinic]').inputValue(),'가상 예약기관');assert.equal(await page.locator('#booking-record [name=state]').inputValue(),'통화함 · 예약 대기');await page.locator('#booking-clear').click();
 report.checks.push('calendar leap/month-end 2024-01-31 & 2024-02-29; 104-day cap; unknown/individual/future input; booking restore/clear');
 // Actual record persistence, today-only summary, compound diaper and safe CSV.
 await page.goto(base+'practice/09-records.html');
 await page.locator('[name=note]').fill('=SUM(1,2)');await page.locator('button[value=breast]').click();
 await page.locator('[name=amount]').fill('60');await page.locator('button[value=formula]').click();
 await page.locator('button[value=sleep-start]').click();await page.locator('button[value=sleep-end]').click();await page.locator('button[value=both]').click();
 assert.match(await page.locator('#today-summary').innerText(),/수유 2회/);assert.match(await page.locator('#today-summary').innerText(),/소변 1회 · 대변 1회/);assert.match(await page.locator('#today-summary').innerText(),/잠 시작 1회 \/ 끝 1회/);
 const previous=await page.evaluate(()=>{const d=new Date();d.setDate(d.getDate()-1);return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}T12:00`});
 await page.locator('[name=at]').fill(previous);await page.locator('[name=note]').fill('<img src=x onerror=alert(1)>');await page.locator('button[value=wet]').click();
 assert.match(await page.locator('#today-summary').innerText(),/소변 1회/);assert.equal(await page.locator('#record-list img').count(),0);
 await page.reload();assert.equal(await page.locator('#record-list li').count(),6);assert.match(await page.locator('#record-list').innerText(),/60 mL/);
 const downloadPromise=page.waitForEvent('download');await page.locator('#download-csv').click();const download=await downloadPromise;const downloadPath=await download.path(),csv=fs.readFileSync(downloadPath,'utf8');
 assert.match(csv,/"'[/=]/);assert.match(csv,/"60"/);assert.match(csv,/소변\+대변/);assert.match(csv,/"시각","종류"/);
 await page.locator('#record-list button').first().click();assert.equal(await page.locator('#record-list li').count(),5);
 await page.locator('#clear-records').click();await page.locator('#cancel-clear').click();assert.equal(await page.locator('#record-list li').count(),5);
 await page.locator('#clear-records').click();await page.locator('#confirm-clear').click();await page.reload();assert.match(await page.locator('#record-list').innerText(),/아직 남긴 기록/);
 report.checks.push('all record kinds; today-only counts; compound diaper counted once per category; HTML escaped; persistence; UTF-8 CSV formula neutralization; delete/cancel/clear');
 // Storage failure still permits in-page records and export.
 const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError')}})});
 const bp=await blocked.newPage();bp.on('pageerror',e=>report.errors.push('blocked: '+e.message));await bp.goto(base+'practice/09-records.html');
 assert.match(await bp.locator('#record-status').innerText(),/읽을 수 없/);await bp.locator('button[value=wet]').click();assert.match(await bp.locator('#record-status').innerText(),/저장할 수 없/);assert.match(await bp.locator('#today-summary').innerText(),/소변 1회/);
 const bdl=bp.waitForEvent('download');await bp.locator('#download-csv').click();await bdl;await bp.goto(base+'practice/08-checkups.html');await bp.locator('#booking-record [name=clinic]').fill('저장 차단');assert.match(await bp.locator('#booking-status').innerText(),/저장할 수 없/);await blocked.close();
 report.checks.push('blocked localStorage: records still usable/exportable; booking failure message');
 // Malformed storage is reported, rather than crashing the recording UI.
 await page.goto(base+'practice/09-records.html');await page.evaluate(()=>localStorage.setItem('babybook:care-log:v1','{"not":"an array"}'));await page.reload();assert.match(await page.locator('#record-status').innerText(),/읽을 수 없/);await page.locator('button[value=wet]').click();assert.match(await page.locator('#today-summary').innerText(),/소변 1회/);await page.evaluate(()=>localStorage.removeItem('babybook:care-log:v1'));
 report.checks.push('malformed stored JSON value: explanation and working in-memory UI');
 // Print PDFs and selected instructional figures, light/dark.
 for(const file of owned.filter(x=>x.startsWith('print/'))){await page.goto(base+file);await page.emulateMedia({media:'print'});const pdf=path.join(dest,path.basename(file,'.html')+'-a4.pdf');await page.pdf({path:pdf,format:'A4',preferCSSPageSize:true,printBackground:false});const raw=fs.readFileSync(pdf,'latin1');const count=(raw.match(/\/Type\s*\/Page\b/g)||[]).length;assert.equal(count,1,file+' must print on one A4 page');report.pdf.push({file:path.basename(pdf),pages:count,mediaBox:raw.match(/\/MediaBox\s*\[([^\]]+)\]/)[1]});await page.emulateMedia({media:'screen'});}
 for(const file of ['01-home','02-diaper','03-feeding','05-bath','06-emergency','10-play']){
  await page.setViewportSize({width:375,height:900});await page.goto(base+'practice/'+file+'.html');
  for(const theme of ['light','dark']){await page.evaluate(t=>document.documentElement.dataset.theme=t,theme);await page.locator('.baby-figure').first().screenshot({path:path.join(dest,'figure-'+file+'-'+theme+'.png')});}
 }
 assert.deepEqual(report.errors,[]);fs.writeFileSync(path.join(dest,'browser-report.json'),JSON.stringify(report,null,2));await browser.close();console.log(JSON.stringify({views:report.views.length,checks:report.checks.length,errors:report.errors,missingAnchors:report.links.length,pdf:report.pdf},null,2));
})().catch(error=>{fs.writeFileSync(path.join(dest,'browser-failure.json'),JSON.stringify({error:error.stack,report},null,2));console.error(error);process.exit(1)});
