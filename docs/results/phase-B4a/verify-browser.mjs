import { chromium } from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const base = process.env.BLOG_BASE || 'http://127.0.0.1:8314/site-blog/';
const out = new URL('./', import.meta.url).pathname;
const pages = ['01-map','03-ai-tools','04-platforms','05-keywords'];
for (const slug of pages) assert.ok(fs.existsSync(`site-blog/chapters/${slug}.html`), `${slug}: 담당 원고 필요`);
const browser = await chromium.launch({headless:true, executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome', args:['--no-sandbox']});
const report = {screens:[], interactions:[], errors:[]};
const context = await browser.newContext({reducedMotion:"reduce",permissions:["clipboard-read","clipboard-write"]});
const page = await context.newPage();
page.on('pageerror', e => report.errors.push(e.message));
page.on('console', m => {if(m.type()==='error') report.errors.push(m.text());});
page.on('response', r => {if(r.status()>=400) report.errors.push(`${r.status()} ${r.url()}`);});
try {
 for(const slug of pages) for(const width of [1280,375,360]) for(const theme of ['light','dark']) {
  await page.setViewportSize({width,height:900});
  await page.goto(`${base}chapters/${slug}.html`);
  await page.locator('[data-theme-select]').selectOption(theme);
  await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth), false, `${slug}/${width}/${theme}: overflow`);
  assert.equal(await page.locator('.chapter-faq details').count(),5);
  assert.equal(await page.locator('[data-question]').count(),3);
  const file=`${slug}-${width}-${theme}.png`;
  await page.screenshot({path:out+file,fullPage:true});
  await page.locator('.chapter-faq details').evaluateAll(nodes=>nodes.forEach(node=>{node.open=true;}));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth), false, `${slug}/${width}/${theme}: FAQ overflow`);
  if(width===360 && slug!=='01-map') {
   const table=page.locator('.table-scroll').first(); await table.focus(); await page.keyboard.press('ArrowRight');
   await page.waitForFunction(()=>document.activeElement.scrollLeft>0);
  }
  report.screens.push({slug,width,theme,file,overflow:0,expandedFaqOverflow:0});
 }
 await page.goto(`${base}chapters/01-map.html#first-post-tool`);
 assert.match(await page.locator('#map-result').innerText(),/5/);
 for(let i=1;i<=5;i++) await page.locator(`#map-step-${i}`).check();
 assert.match(await page.locator('#map-result').innerText(),/0/);
 assert.match(await page.locator('#map-next').innerText(),/公開|공개/);
 await page.locator('#map-step-1').uncheck();
 assert.match(await page.locator('#map-next').innerText(),/독자/);
 await page.locator('#map-reset').focus(); await page.keyboard.press('Enter');
 assert.equal(await page.locator('#first-post-tool input:checked').count(),0);
 report.interactions.push('1장: 전부/부분 완료·초기화·다음 행동');
 await page.goto(`${base}chapters/03-ai-tools.html#tool-picker`);
 for(const [task,expected] of [['draft','ChatGPT'],['proof','ChatGPT'],['image','미리캔버스'],['keyword','데이터랩'],['analytics','Search Console']]) {
  await page.locator('#tool-task').selectOption(task);
  assert.ok((await page.locator('#tool-choice').innerText()).includes(expected));
 }
 await page.locator('#tool-task').focus(); await page.keyboard.press('Home'); await page.keyboard.press('ArrowDown');
 assert.match(await page.locator('#tool-choice').innerText(),/ChatGPT/);
 report.interactions.push('3장: 5개 작업 전환·키보드 선택');
 await page.goto(`${base}chapters/04-platforms.html#platform-tool`);
 for(const goal of ['start','adsense','naver']) for(const api of ['no','yes']) for(const domain of ['no','yes','control']) {
  await page.locator('#platform-goal').selectOption(goal); await page.locator('#platform-api').selectOption(api); await page.locator('#platform-domain').selectOption(domain);
  const text=await page.locator('#platform-choice').innerText();
  if(goal==='naver' && (api==='yes'||domain!=='no')) assert.match(text,/함께|동시에|충돌/);
  else if(domain==='control') assert.match(text,/설치형 WordPress/);
  else if(api==='yes') assert.match(text,/Blogger/);
  else if(goal==='adsense'||domain==='yes') assert.match(text,/티스토리/);
  else assert.match(text,/네이버/);
 }
 report.interactions.push('4장: 목표×API×도메인 18조합·충돌 안내');
 await page.goto(`${base}chapters/05-keywords.html#keyword-tool`);
 for(const key of ['broad','specific','thin']) {
  await page.locator(`#keyword-${key}`).focus(); await page.keyboard.press('Space');
  assert.equal(await page.locator(`#keyword-${key}`).isChecked(),true);
  assert.match(await page.locator('#keyword-result').innerText(),/1/);
  assert.ok((await page.locator('#keyword-reason').innerText()).length>30);
 }
 report.interactions.push('5장: 모든 선택지·이유·키보드');
 for(const slug of pages) {
  await page.goto(`${base}chapters/${slug}.html`);
  for(const q of await page.locator('[data-question]').all()) await q.locator('[data-correct="true"]').click();
  assert.match(await page.locator('[data-quiz-score]').innerText(),/3문항 정답/);
  await page.locator('[data-quiz-reset]').click();
  assert.match(await page.locator('[data-quiz-score]').innerText(),/0문항 풀이/);
  await page.locator('.chapter-faq summary').first().focus(); await page.keyboard.press('Enter');
  assert.equal(await page.locator('.chapter-faq details').first().getAttribute('open'),'');
  await page.locator('[data-axis-nav] a').first().focus(); await page.keyboard.press('Enter');
  assert.ok(await page.evaluate(()=>document.activeElement.id.length>0));
 }
 await page.locator('.copy-button').first().focus(); await page.keyboard.press('Enter');
 await page.locator('.copy-status').first().filter({hasText:'복사했습니다.'}).waitFor();
 assert.ok((await page.evaluate(()=>navigator.clipboard.readText())).length>40);
 report.interactions.push('네 장 공통: 퀴즈 정답/초기화·FAQ·축 앵커 키보드, 복사 버튼 Enter');
 const off = await browser.newContext({javaScriptEnabled:false});
 for(const slug of pages) {
  const p=await off.newPage(); await p.goto(`${base}chapters/${slug}.html`);
  assert.ok((await p.locator('h1').innerText()).length>3);
  assert.ok(await p.locator('noscript').count()); await p.close();
 }
 await off.close(); report.interactions.push('4장 JS 꺼짐: 본문·도구 대안');
 const blocked = await browser.newContext();
 await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError');}});});
 const bp=await blocked.newPage(); let blockedErrors=[];bp.on('pageerror',e=>blockedErrors.push(e.message));
 for(const slug of pages) {await bp.goto(`${base}chapters/${slug}.html`);assert.equal(await bp.locator('[data-theme-select]').count(),1);}
 assert.deepEqual(blockedErrors,[]); await blocked.close();
 report.interactions.push('localStorage 차단 환경: 4장 본문·테마 초기화 오류 없음');
 for(const [slug,id] of [['01-map','first-post-tool'],['03-ai-tools','tool-picker'],['04-platforms','platform-tool'],['05-keywords','keyword-tool']]) {
  await page.goto(`${base}chapters/${slug}.html?embed=${id}`);
  assert.equal(await page.locator(`#${id}`).isVisible(),true);
  assert.equal(await page.locator('header[data-site-header]').isVisible(),false);
 }
 report.interactions.push('4장 도구 embed 진입');
 assert.deepEqual(report.errors,[]);
 report.status='PASS';
} catch(e) {report.status='FAIL';report.failure=e.stack;throw e;}
finally {fs.writeFileSync(out+'browser-check.json',JSON.stringify(report,null,2));await browser.close();}
console.log(JSON.stringify({status:report.status,screens:report.screens.length,interactions:report.interactions,errors:report.errors}));
