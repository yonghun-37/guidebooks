/* 마지막 1장 장면 정리 뒤 여섯 조합만 다시 확인한다. 서버·도구 경로는 통합 검사와 같다. */
const {chromium}=require(process.env.PW_MODULE||'/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME||'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
 const report={views:[],errors:[]};try{
 const page=await browser.newPage();page.on('pageerror',e=>report.errors.push(e.message));page.on('console',m=>{if(m.type()==='error')report.errors.push(m.text())});
 for(const width of [1280,375,360])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:960});await page.goto((process.env.BASE_URL||'http://127.0.0.1:8796')+'/baby/chapters/01-map.html');await page.locator('[data-theme-select]').selectOption(theme);
  assert.match(await page.locator('#case').textContent(),/전화할 날을 확인/);
  assert.match(await page.locator('#case').textContent(),/퇴원 5일째/);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth),0);
  await page.locator('#birth-date').fill('2026-10-01');await page.locator('#deadline-form button').click();
  for(const href of await page.locator('#deadline-result a').evaluateAll(ns=>ns.map(n=>n.getAttribute('href'))))assert.match(href,/credits\.html#n\d{3}$/);
  report.views.push({width,theme,overflow:0});
 }
 assert.deepEqual(report.errors,[]);fs.writeFileSync(__dirname+'/timeline-browser.json',JSON.stringify(report,null,2)+'\n');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
