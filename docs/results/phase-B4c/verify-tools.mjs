import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const page=await browser.newPage();
const base=process.env.B4C_BASE || 'http://127.0.0.1:8624/site-blog/';
try {
 await page.goto(base+'chapters/11-analytics.html');
 assert.equal(await page.locator('#analytics-tool').count(),1,'11장 숫자 해석 도구 필요');
 await page.locator('#analytics-run').click();
 assert.equal(await page.locator('#analytics-value').innerText(),'2%');
 await page.selectOption('#metric','rpm');await page.locator('#analytics-run').click();
 assert.equal(await page.locator('#analytics-value').innerText(),'500원');
 await page.locator('#analytics-zero').click();
 assert.match(await page.locator('#analytics-meaning').innerText(),/분모|계산/);
 await page.goto(base+'chapters/12-policy.html');
 assert.equal(await page.locator('#disclosure-tool').count(),1,'12장 표시 위치 도구 필요');
 await page.locator('#place-end').check();await page.locator('#disclosure-run').click();
 assert.equal(await page.locator('#disclosure-value').innerText(),'수정');
 await page.locator('#place-first').check();await page.locator('#disclosure-run').click();
 assert.equal(await page.locator('#disclosure-value').innerText(),'위치 적절');
 await page.goto(base+'chapters/13-plan.html');
 assert.equal(await page.locator('#plan-body tr').count(),30,'30일 전체 계획 필요');
 await page.locator('#plan-run').click();
 assert.equal(await page.locator('#plan-value').innerText(),'30시간');
 await page.selectOption('#plan-focus','review');await page.selectOption('#plan-used','no');await page.locator('#plan-run').click();
 assert.match(await page.locator('#plan-export').inputValue(),/공식 사양|사용 메모/);
 console.log('도구 핵심 사용자 흐름 통과');
} finally {await browser.close();}
