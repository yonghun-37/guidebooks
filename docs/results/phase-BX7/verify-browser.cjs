/* node docs/results/phase-BX7/verify-browser.cjs; starts and closes its own free-port server. */
const {chromium}=require('/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const http=require('node:http'),crypto=require('node:crypto');
const out=__dirname,root=process.cwd();let base,browser;
const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{let file;try{file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(root+path.sep))throw Error('outside');if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');const data=fs.readFileSync(file);res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(data)}catch{res.writeHead(404);res.end('Not found')}});
function fingerprint(){const files=[...new Set(routes.map(r=>'site-blog/'+r.split('#')[0])),...fs.readdirSync('site-blog/assets').filter(n=>/\.(css|js)$/.test(n)).map(n=>'site-blog/assets/'+n)];return Object.fromEntries(files.sort().map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')]))} 
const slugs=fs.readdirSync('site-blog/advanced').filter(x=>x.endsWith('.html')).sort();
const routes=[...slugs.map(x=>'advanced/'+x),'index.html','index.html#contents','credits.html'];
const errors=[],records=[],tools=[];
function listen(page,route){page.on('pageerror',e=>errors.push(route+': '+e.message));page.on('console',m=>{if(m.type()==='error')errors.push(route+': '+m.text())});page.on('response',r=>{if(r.url().startsWith(new URL(base).origin)&&r.status()>=400)errors.push(route+': HTTP '+r.status()+' '+r.url())});page.on('requestfailed',r=>{if(r.url().startsWith(new URL(base).origin))errors.push(route+': request failed '+r.url()+' '+r.failure()?.errorText)})}
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));base=`http://127.0.0.1:${server.address().port}/site-blog/`;const before=fingerprint(),started=new Date().toISOString();
 browser=await chromium.launch({headless:true,executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome'});
 for(const route of routes)for(const width of [1280,375,360])for(const theme of ['light','dark']){
  const ctx=await browser.newContext({viewport:{width,height:900},colorScheme:theme,acceptDownloads:true});const page=await ctx.newPage();listen(page,route);
  await page.goto(base+route);await page.waitForFunction(()=>document.documentElement.dataset.theme);await page.evaluate(()=>document.fonts.ready);
  const details=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,theme:document.documentElement.dataset.theme,links:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),sections:[...document.querySelectorAll('.chapter-block[id]')].map(n=>n.id)}));
  assert.equal(details.overflow,false,`${route} ${width} ${theme}: overflow`);assert.equal(details.theme,theme);
  if(route.includes('#'))await page.locator('.skip-link').focus();else await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('href'),'#main');await page.keyboard.press('Enter');
  let links=0;
  for(const href of new Set(details.links)){
   if(/^(https?:|mailto:|tel:|data:)/.test(href))continue;const url=new URL(href,page.url());const file=path.join(process.cwd(),decodeURIComponent(url.pathname));assert(fs.existsSync(file),route+' missing '+href);
   if(url.hash){const id=decodeURIComponent(url.hash.slice(1)),text=fs.readFileSync(file,'utf8');assert(text.includes(`id="${id}"`)||text.includes(`id='${id}'`),route+' anchor '+href)}links++;
  }
  if(route.startsWith('advanced/')){
   const required=['answer','make','overview','start','read','change','errors','checkpoint','caution','summary'];let last=-1;for(const id of required){const index=details.sections.indexOf(id);assert(index>last,`${route} common structure ${id}`);last=index}
   assert.equal(await page.locator('body').getAttribute('data-manuscript'),'complete');
  }else if(route.startsWith('index.html')){assert.equal(await page.locator('[data-chapter-toc] a[href*="advanced/"]').count(),14);assert.equal(await page.locator('[data-chapter-toc]').innerText().then(t=>t.includes('준비 중')),false)}
  if(width===1280&&theme==='light'||width===360&&theme==='dark'){
   const name=route.replace(/[\/#.]/g,'-')+`-${width}-${theme}`;await page.screenshot({path:path.join(out,name+'.png')});
   if(['advanced/02-wordpress.html','advanced/05-gates.html','advanced/06-publish.html','advanced/12-policy.html'].includes(route)){await page.locator('#overview figure').screenshot({path:path.join(out,name+'-flow.png')});if(await page.locator('#automatic-conditions').count())await page.locator('#automatic-conditions').screenshot({path:path.join(out,name+'-auto.png')})}
   if(route==='credits.html'){await page.locator('#source-bx133').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,name+'-sources.png')})}
  }
  if(route==='advanced/01-environment.html'){
   const first=page.locator('[data-os-tabs]').first();await first.locator('[data-os="windows"]').focus();await page.keyboard.press('ArrowRight');assert.equal(await first.locator('[data-os="unix"]').getAttribute('aria-selected'),'true');await page.keyboard.press('Home');assert.equal(await first.locator('[data-os="windows"]').getAttribute('aria-selected'),'true');tools.push({width,theme,tool:'os-tabs'});
  }
  if(route==='advanced/00-start.html'){
   const values={pv:1000,rpm:2000,orders:2,basket:10000,rate:3,sponsor:10000};for(const [n,v]of Object.entries(values))await page.locator(`#revenue-form [name="${n}"]`).fill(String(v));await page.locator('#revenue-form button[type="submit"]').focus();await page.keyboard.press('Enter');assert((await page.locator('[data-revenue-result]').innerText()).startsWith('12,600원'));
   await page.locator('[data-zero-cost]').click();assert((await page.locator('[data-cost-result]').innerText()).startsWith('0원/월'));
   await page.locator('#revenue-form [name="rate"]').fill('101');assert.equal(await page.locator('#revenue-form').evaluate(f=>f.checkValidity()),false);await page.locator('[data-zero-revenue]').click();
   const download=page.waitForEvent('download');await page.locator('[data-save-plan]').click();assert.equal((await download).suggestedFilename(),'운영계획.txt');tools.push({width,theme,tool:'income-cost-download'});
  }
  if(route==='advanced/05-gates.html'){
   for(const sample of ['info','play','affiliate','sponsor']){await page.locator('[data-gate-tool] select').selectOption(sample);for(let i=0;i<7;i++){await page.locator('[data-gate-next]').focus();await page.keyboard.press('Enter')}assert.equal(await page.locator('[data-gate-next]').isDisabled(),true);assert.equal(await page.locator('[data-gate-log] li').count(),7);const final=await page.locator('[data-gate-result]').innerText();assert(final.startsWith(({info:'자동 항목 없음',play:'사람 검토 대기',affiliate:'차단',sponsor:'차단'})[sample]));if(sample==='info')assert(final.includes('최종 사람 승인'))}tools.push({width,theme,tool:'gate-4-samples'});
  }
  if(route==='advanced/08-affiliate.html'){
   await page.locator('input[value="opening"]').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('input[value="link"]').isChecked(),true);assert((await page.locator('[data-disclosure-result]').innerText()).includes('부족'));await page.reload();assert.equal(await page.locator('input[value="link"]').isChecked(),true);await page.locator('[data-disclosure-reset]').click();assert.equal(await page.locator('input[value="opening"]').isChecked(),true);tools.push({width,theme,tool:'affiliate-storage-keyboard'});
  }
  if(route==='advanced/09-sponsorship.html'){
   const routeStates=['reviewing','accepted','contracted','received','writing','brand_review','human_approval','approved','scheduled','published','reported','settlement_pending','settled'];
   for(const state of routeStates){for(const input of await page.locator('[data-sponsor-records] input').all()){await input.focus();await page.keyboard.press('Space')}const btn=page.locator('[data-sponsor-actions] button').filter({hasText:state==='reviewing'?'다음 상태: 검토':({accepted:'다음 상태: 수락',contracted:'다음 상태: 계약',received:'다음 상태: 제품 수령',writing:'다음 상태: 작성',brand_review:'다음 상태: 광고주 확인',human_approval:'다음 상태: 최종 사람 승인',approved:'다음 상태: 발행 준비',scheduled:'다음 상태: 예약',published:'다음 상태: 발행',reported:'다음 상태: 성과 보고',settlement_pending:'다음 상태: 정산 대기',settled:'다음 상태: 정산'}[state])}).first();await btn.focus();await page.keyboard.press('Enter');assert((await page.locator('[data-sponsor-state]').innerText()).endsWith('· '+state))}
   await page.reload();assert((await page.locator('[data-sponsor-state]').innerText()).endsWith('· settled'));await page.locator('[data-sponsor-reset]').click();tools.push({width,theme,tool:'sponsor-13-states'});
  }
  if(route==='advanced/e2e.html'){
   assert.equal(await page.locator('[data-e2e-check]').count(),24);await page.locator('[data-e2e-check]').first().focus();await page.keyboard.press('Space');await page.locator('[data-e2e-note]').first().fill('통과 · 재현 로그');await page.locator('[data-e2e-note]').first().blur();await page.reload();assert.equal(await page.locator('[data-e2e-check]').first().isChecked(),true);assert.equal(await page.locator('[data-e2e-note]').first().inputValue(),'통과 · 재현 로그');await page.locator('[data-e2e-reset]').click();assert.equal(await page.locator('[data-e2e-check]:checked').count(),0);tools.push({width,theme,tool:'e2e-storage-keyboard'});
  }
  records.push({route,width,theme,overflow:0,links,keyboard:true});await ctx.close();
 }
 for(const route of routes)for(const theme of ['light','dark']){
  const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:900},colorScheme:theme}),page=await ctx.newPage();listen(page,route);await page.goto(base+route);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,route+' noJS overflow');
  if(route.startsWith('advanced/')){for(const id of ['answer','make','read','checkpoint','summary'])assert(await page.locator('#'+id).isVisible());assert((await page.locator('.advanced-static-nav a').count())>=4)}else if(route.startsWith('index.html')) assert.equal(await page.locator('a[href*="advanced/"]').count()>=14,true);else assert(await page.locator('#advanced-sources').isVisible());
  records.push({route,theme,noJS:true});await ctx.close();
 }
 for(const storage of ['blocked','corrupt'])for(const slug of ['08-affiliate','09-sponsorship','e2e']){
  const ctx=await browser.newContext();await ctx.addInitScript(mode=>{if(mode==='blocked')Object.defineProperty(window,'localStorage',{get(){throw Error('blocked')}});else for(const key of ['blogbook:advanced:affiliate-position:v1','blogbook:advanced:sponsor:v1','blogbook:advanced:e2e:v1'])localStorage.setItem(key,'{broken');},storage);const page=await ctx.newPage();listen(page,slug);await page.goto(base+'advanced/'+slug+'.html');
  const selector=slug==='08-affiliate'?'[data-disclosure-reset]':slug==='09-sponsorship'?'[data-sponsor-reset]':'[data-e2e-reset]';await page.locator(selector).click();assert(await page.locator('#summary').isVisible());tools.push({storage,tool:slug});await ctx.close();
 }
 assert.deepEqual(errors,[]);assert.deepEqual(fingerprint(),before,'sources changed while browser checks were running');
 const screens=records.filter(r=>!r.noJS).length,noJS=records.filter(r=>r.noJS).length;
 fs.writeFileSync(path.join(out,'browser.json'),JSON.stringify({started,finished:new Date().toISOString(),base,browser:browser.version(),screens,noJS,console_errors:errors,source_hashes:before,records,tools},null,2)+'\n');
 console.log(`PASS ${screens} screens + ${noJS} no-JS + ${tools.length} tool/storage checks; console/HTTP errors 0; source hashes stable`);
})().catch(e=>{fs.writeFileSync(path.join(out,'browser-failure.txt'),e.stack);console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close();if(server.listening)await new Promise(resolve=>server.close(resolve))});
