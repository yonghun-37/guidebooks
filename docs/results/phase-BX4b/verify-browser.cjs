/* 실행: node docs/results/phase-BX4b/verify-browser.cjs (localhost:8844에서 저장소 제공). */
const {chromium}=require(process.env.BX4B_PLAYWRIGHT||'/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const out=__dirname;
const slugs=['07-ads','08-affiliate','10-analytics','11-operations','12-policy','e2e'];
const base='http://127.0.0.1:8844/site-blog/advanced/';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.BX4B_CHROMIUM||'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome'});
 const records=[],errors=[];
 for(const slug of slugs)for(const width of [1280,375,360])for(const theme of ['light','dark']){
  const ctx=await browser.newContext({viewport:{width,height:900},colorScheme:theme});
  const page=await ctx.newPage();
  page.on('pageerror',e=>errors.push(`${slug} ${width} ${theme}: ${e.message}`));
  page.on('console',msg=>{if(msg.type()==='error')errors.push(`${slug} ${width} ${theme}: ${msg.text()}`)});
  await page.goto(base+slug+'.html');await page.waitForLoadState('networkidle');
  const detail=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,complete:document.body.dataset.manuscript,theme:document.documentElement.dataset.theme,sections:document.querySelectorAll('.chapter-block').length,figures:[...document.querySelectorAll('figure')].every(f=>f.querySelector('figcaption')&&f.querySelector('[aria-label],svg title,img[alt]')),links:[...document.querySelectorAll('main a[href]')].map(a=>a.getAttribute('href'))}));
  assert.equal(detail.overflow,false,`${slug} ${width} ${theme} 가로 넘침`);
  assert.equal(detail.complete,'complete');assert.equal(detail.theme,theme);assert(detail.sections>=9);assert(detail.figures,`${slug} 그림 설명`);
  await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('href'),'#main');await page.keyboard.press('Enter');
  const broken=[];
  for(const href of new Set(detail.links)){
   if(/^(https?:|mailto:|tel:)/.test(href))continue;
   const url=new URL(href,page.url());
   const file=path.join(process.cwd(),decodeURIComponent(url.pathname));
   if(!fs.existsSync(file)){broken.push(href);continue;}
   if(url.hash){const text=fs.readFileSync(file,'utf8');const id=decodeURIComponent(url.hash.slice(1));if(!text.includes(`id="${id}"`)&&!text.includes(`id='${id}'`))broken.push(href);}
  }
  assert.deepEqual(broken,[],`${slug} 깨진 본문 링크`);
  if(slug==='e2e'){
   const cellOverflow=await page.locator('#steps td,#scenarios td').evaluateAll(cells=>cells.filter(c=>c.scrollWidth>c.clientWidth+1).length);
   assert.equal(cellOverflow,0,'E2E 셀 안의 체크·메모가 옆 셀을 침범함');
   if(width<700){const scroller=page.locator('#steps .table-scroll');await scroller.focus();await page.keyboard.press('ArrowRight');await page.waitForFunction(()=>document.querySelector('#steps .table-scroll').scrollLeft>0);}
  }
  await page.screenshot({path:path.join(out,`${slug}-${width}-${theme}.png`)});
  if(slug==='08-affiliate'){
   const opening=page.locator('[data-disclosure-controls] input[value="opening"]');
   await opening.focus();await page.keyboard.press('ArrowRight');
   assert.equal(await page.locator('[data-disclosure-controls] input[value="link"]').isChecked(),true);
   assert((await page.locator('[data-disclosure-result]').innerText()).includes('부족'));
   await page.reload();assert.equal(await page.locator('input[value="link"]').isChecked(),true);
   await page.locator('[data-disclosure-reset]').click();assert.equal(await opening.isChecked(),true);
   await opening.focus();await page.keyboard.press('ArrowLeft');
   assert((await page.locator('[data-preview-title]').innerText()).includes('수수료'));
   await page.locator('[data-disclosure-reset]').click();
   await page.locator('[data-disclosure-tool]').screenshot({path:path.join(out,`affiliate-tool-${width}-${theme}.png`)});
  }
  records.push({slug,width,theme,overflow:0,keyboard_skip:true,internal_links:new Set(detail.links).size});await ctx.close();
 }
 for(const slug of slugs){
  const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:900}});const page=await ctx.newPage();await page.goto(base+slug+'.html');
  assert(await page.locator('#answer').isVisible());assert(await page.locator('#checkpoint').isVisible());assert(await page.locator('#summary').isVisible());assert((await page.locator('code[data-run]').allTextContents()).join('').includes('python '));assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  if(slug==='08-affiliate')assert(await page.locator('[data-preview-disclosure]').isVisible());
  records.push({slug,js_disabled_reading:true});await ctx.close();
 }
 // 저장 차단·잘못된 저장값에서도 본문과 기록 조작이 동작해야 한다.
 for(const failure of ['blocked','corrupt']){
  const ctx=await browser.newContext();await ctx.addInitScript(mode=>{if(mode==='blocked')Object.defineProperty(window,'localStorage',{get(){throw Error('blocked')}});else localStorage.setItem('blogbook:advanced:e2e:v1','{broken');},failure);
  const page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'e2e.html');await page.locator('[data-e2e-check]').first().check();await page.locator('[data-e2e-note]').first().fill('보류 · 다시 확인');assert.equal(await page.locator('[data-e2e-check]').first().isChecked(),true);await page.locator('[data-e2e-reset]').click();assert.equal(await page.locator('[data-e2e-check]:checked').count(),0);records.push({e2e_storage_failure:failure,passed:true});await ctx.close();
 }
 for(const failure of ['blocked','corrupt']){
  const ctx=await browser.newContext();await ctx.addInitScript(mode=>{if(mode==='blocked')Object.defineProperty(window,'localStorage',{get(){throw Error('blocked')}});else localStorage.setItem('blogbook:advanced:affiliate-position:v1','nonsense');},failure);
  const page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'08-affiliate.html');
  await page.locator('input[value="opening"]').focus();await page.keyboard.press('ArrowRight');assert.equal(await page.locator('input[value="link"]').isChecked(),true);await page.locator('[data-disclosure-reset]').click();assert.equal(await page.locator('input[value="opening"]').isChecked(),true);
  records.push({affiliate_storage_failure:failure,passed:true});await ctx.close();
 }
 assert.deepEqual(errors,[],'콘솔·페이지 오류');
 fs.writeFileSync(path.join(out,'browser.json'),JSON.stringify({screens:36,js_disabled_pages:6,console_errors:errors,records},null,2)+'\n');
 await browser.close();console.log('36 화면, 6 JS 없는 읽기, 키보드·링크·저장 예외 PASS');
})().catch(e=>{fs.writeFileSync(path.join(out,'browser-failure.txt'),String(e.stack));console.error(e);process.exit(1)});
