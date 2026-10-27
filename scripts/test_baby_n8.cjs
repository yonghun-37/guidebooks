/* N7 발견의 재현 입력과 N8 정적 응급 안내·도해 집중 검사. 합성 입력만 사용. */
const {chromium}=require(process.env.PW_MODULE||'/tmp/ai-insta-phase3-browser/node_modules/playwright-core');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.BASE_URL||'http://127.0.0.1:8798',dest=path.resolve('docs/results/phase-N8');
const canonical=require('../site-baby/assets/emergency-data.js'),report={checks:[],errors:[],noJS:[],figures:[]};
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME||'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
 try{
  const context=await browser.newContext({viewport:{width:360,height:900}}),page=await context.newPage();
  page.on('pageerror',e=>report.errors.push(e.message));
  const go=f=>page.goto(base+'/baby/'+f);
  await go('practice/08-checkups.html');
  await page.locator('[name=birth]').fill('2026-08-01');await page.locator('[name=route]').selectOption('single');await page.locator('#schedule-form button').click();
  assert.match(await page.locator('#schedule-result').innerText(),/2026-08-01.*단독 경로/);
  await page.locator('[name=birth]').fill('2026-09-01');assert.match(await page.locator('#schedule-result').innerText(),/入力|입력이 바뀌었어요/);
  assert.doesNotMatch(await page.locator('#schedule-result').innerText(),/2026-11-13/);
  await page.locator('[name=route]').selectOption('six');await page.locator('#schedule-form button').click();
  assert.match(await page.locator('#schedule-result').innerText(),/2026-12-14/);assert.doesNotMatch(await page.locator('#schedule-result').innerText(),/B형간염 단독 · 1개월/);
  await page.locator('#booking-record [name=state]').selectOption({label:'통화함 · 예약 확정'});
  assert.match(await page.locator('#booking-warning').innerText(),/기관 이름과 날짜/);
  await page.reload();assert.match(await page.locator('#booking-warning').innerText(),/기관 이름과 날짜/);
  await page.locator('[name=clinic]').fill('가상 기관');await page.locator('[name=appointment]').fill('2026-10-30T10:00');
  assert.equal(await page.locator('#booking-warning').innerText(),'');
  await page.locator('#booking-clear').click();
  report.checks.push('M07: birth/route changes clear stale dates, identify actual calculation inputs; C04: missing confirmed date/clinic warns before and after reload');
  // The laboratory must use the corrected original, including invalidation.
  await go('lab.html?tool=08-checkups:schedule-tool');const frame=page.frameLocator('#sim-frame');
  await frame.locator('[name=birth]').fill('2026-08-01');await frame.locator('[name=route]').selectOption('single');await frame.locator('#schedule-form button').click();
  await frame.locator('[name=route]').selectOption('six');assert.match(await frame.locator('#schedule-result').innerText(),/입력이 바뀌었어요/);
  report.checks.push('M07: laboratory iframe invalidates the same original result');
  await go('chapters/10-benefits.html');await page.locator('[name=region]').selectOption('special');
  assert.match(await page.locator('#ch10-months tbody tr').first().innerText(),/12만 원.*현금\/지역상품권 확인 필요/);
  assert.match(await page.locator('#benefits-result').innerText(),/합계 확인 필요/);
  await page.locator('[name=payment]').selectOption('voucher');assert.match(await page.locator('#benefits-result').innerText(),/월 현금 100만 원/);
  await page.locator('[name=payment]').selectOption('cash');assert.match(await page.locator('#benefits-result').innerText(),/월 현금 112만 원/);
  report.checks.push('M09: unknown payment withholds total; voucher base amount excluded; explicit cash selection totals separately');
  await go('practice/09-records.html');await page.locator('button[value=formula]').click();assert.match(await page.locator('#record-status').innerText(),/기록했어요/);
  const before=await page.locator('#record-list > li').count();await page.locator('[name=amount]').fill('-1');await page.locator('button[value=formula]').click();
  assert.equal(await page.locator('#record-list > li').count(),before);assert.match(await page.locator('#record-status').innerText(),/이번 입력은 저장하지 않았어요/);
  assert.doesNotMatch(await page.locator('#record-status').innerText(),/기록했어요/);
  await page.locator('#clear-records').click();await page.locator('#confirm-clear').click();report.checks.push('C11: negative amount is rejected with a fresh error and no extra row');
  await go('practice/07-apply.html');for(const key of ['birth','support']){await page.locator(`[data-record=${key}-visit]`).fill('2026-10-30');}
  await page.reload();assert.equal(await page.locator('[data-record=birth-visit]').inputValue(),'2026-10-30');assert.equal(await page.locator('[data-record=support-visit]').inputValue(),'2026-10-30');await page.locator('[data-record-clear]').click();
  report.checks.push('C02/C03: visit dates separate from submission and restore, per-benefit paper example present');
  for(const file of ['index.html','practice/00-start.html','practice/e2e.html']){await go(file);assert.match(await page.locator('#before-after').innerText(),/출산 전 오늘/);assert.match(await page.locator('#before-after').innerText(),/출생 후/);assert.match(await page.locator('#before-after').innerText(),/185분/);}
  report.checks.push('C01/S02: prenatal/postnatal branches and preparation estimates present at all three entries');
  for(const file of ['practice/00-start.html','practice/06-emergency.html']){await go(file);const labels=await page.locator('[data-mobile-outline] a').allTextContents();assert.equal(labels.filter(t=>t==='따라 하기').length,0);}
  for(const theme of ['light','dark']) for(const [file,key] of [['practice/03-feeding.html','latch'],['practice/03-feeding.html','burp'],['practice/03-feeding.html','bottle'],['practice/02-diaper.html','diaper'],['practice/05-bath.html','wash'],['practice/06-emergency.html','temperature'],['practice/10-play.html','tummy']]){
   await go(file);await page.locator('[data-theme-select]').selectOption(theme);const figure=page.locator(`[data-care-figure=${key}]`);
   for(const svg of await figure.locator('svg').all()){
    const clipped=await svg.evaluate(el=>[...el.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x<0||b.x+b.width>el.viewBox.baseVal.width;}).map(t=>t.textContent));assert.deepEqual(clipped,[],key+' clipped SVG text');
   }
   await figure.screenshot({path:path.join(dest,`${key}-360-${theme}.png`),style:'.site-header,.skip-link{visibility:hidden!important}'});report.figures.push({file,key,width:360,theme});
  }
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:900}}),staticPage=await nojs.newPage();
  for(const file of ['chapters/07-hospital.html','practice/06-emergency.html','print/emergency.html']){
   await staticPage.goto(base+'/baby/'+file);const full=staticPage.locator('[data-emergency-full]').first();
   for(const row of canonical){const item=full.locator(`[data-emergency-id=${row.id}]`);assert.equal(await item.isVisible(),true);assert.equal(await item.evaluate(el=>el.firstChild.textContent),row.text);}
   assert.match(await full.innerText(),/冬|冬|목록이 모든 응급 상황을 담지는 않아요/);assert.match(await full.innerText(),/겨드랑이에서 38℃가 될 때까지 기다리는 뜻은 아니에요/);
   report.noJS.push({file,visibleMessages:canonical.length});
  }
  for(const name of ['emergency','weekly-checklist','log-sheet','parent-crisis']){
   await staticPage.goto(base+'/baby/print/'+name+'.html');const output=path.join(dest,name+'-nojs-a4.pdf');await staticPage.pdf({path:output,preferCSSPageSize:true,printBackground:false});
   assert.equal((fs.readFileSync(output,'latin1').match(/\/Type\s*\/Page\b/g)||[]).length,1,name+' nojs A4');
  }
  report.checks.push('B01: JS disabled: hospital chapter/practice6/emergency print expose all canonical messages; four monochrome PDFs one A4 page each');
  assert.deepEqual(report.errors,[]);await nojs.close();await context.close();
 }finally{await browser.close();fs.writeFileSync(path.join(dest,'n8-regressions.json'),JSON.stringify(report,null,2)+'\n');}
 console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
