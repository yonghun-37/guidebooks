import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const dir=new URL('.',import.meta.url), checks=[], errors=[];
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const page=await browser.newPage({reducedMotion:'reduce'});
page.setDefaultTimeout(15000);
await page.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
page.on('pageerror',e=>errors.push(String(e)));
page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
const check=(name,value)=>{assert.ok(value,name);checks.push(name)};
const origin='http://127.0.0.1:8593';
try {
for(const width of [1280,375,360]) {
 await page.setViewportSize({width,height:1100});
 await page.goto(new URL('../../../shorts-kit/samples/preview.html',import.meta.url).href);
 await page.waitForFunction(()=>document.querySelector('video').readyState>=2);
 check(`재생 전 버튼 상태 ${width}`,await page.locator('#next').isDisabled());
 await page.locator('video').evaluate(v=>v.play());
 await page.waitForFunction(()=>document.querySelector('video').currentTime>0.1);
 await page.locator('video').evaluate(v=>v.pause());
 check(`실제 영상 규격 ${width}`,await page.locator('video').evaluate(v=>v.videoWidth===1080&&v.videoHeight===1920&&v.duration===36));
 await page.locator('video').evaluate(v=>{v.currentTime=1;v.pause()});
 await page.waitForTimeout(250);
 check(`키트 넘침 없음 ${width}`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.locator('#next').focus();await page.keyboard.press('Enter');
 check(`다음 프레임 Enter ${width}`,await page.locator('video').evaluate(v=>Math.abs(v.currentTime-(1+1/30))<0.001));
 await page.locator('#back').focus();await page.keyboard.press('Space');
 check(`이전 프레임 Space ${width}`,await page.locator('video').evaluate(v=>Math.abs(v.currentTime-1)<0.001));
 await page.locator('#safe').focus();await page.keyboard.press('Space');
 check(`안전 영역 키보드 ${width}`,await page.locator('#guide').isVisible());
 await page.locator('[data-start]').nth(1).focus();await page.keyboard.press('Enter');
 check(`장면 선택 키보드 ${width}`,await page.locator('video').evaluate(v=>v.currentTime===12));
 await page.locator('#loop').focus();await page.keyboard.press('Space');
 await page.locator('video').evaluate(v=>{v.pause();v.currentTime=24.1;v.dispatchEvent(new Event('timeupdate'))});
 check(`프레임 정지 중 자동 재생 없음 ${width}`,await page.locator('video').evaluate(v=>v.paused));
 await page.locator('video').evaluate(async v=>{await v.play();v.dispatchEvent(new Event('timeupdate'))});
 await page.waitForTimeout(100);
 check(`장면 반복 ${width}`,await page.locator('video').evaluate(v=>v.currentTime>=12&&v.currentTime<13));
 await page.locator('[data-start]').last().click();
 await page.locator('video').evaluate(async v=>{v.currentTime=35.97;await v.play()});
 await page.waitForFunction(()=>{const v=document.querySelector('video');return v.currentTime>=24&&v.currentTime<25});
 check(`마지막 장면 반복 ${width}`,true);
 await page.locator('[data-start]').first().click();
 await page.locator('video').evaluate(v=>{v.pause();v.currentTime=1});await page.waitForTimeout(200);
 await page.screenshot({path:new URL(`kit-${width}.png`,dir).pathname,fullPage:true});
 check(`접근성 상태 안내 ${width}`,(await page.locator('[role="status"]').innerText()).includes('재생 버튼'));
 for(const [slug,name] of [['chapters/02-revenue.html','sample-A'],['practice/08-publish.html','sample-B']]) {
  await page.goto(origin+'/shorts/'+slug);
  check(`승인 샘플 넘침 없음 ${name}/${width}`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  const faq=page.locator('#faq-1');await faq.locator('summary').focus();await page.keyboard.press('Enter');
  check(`승인 샘플 FAQ 키보드 ${name}/${width}`,await faq.getAttribute('open')!==null);
  await page.screenshot({path:new URL(`${name}-${width}.png`,dir).pathname,fullPage:true});
 }
}
check('콘솔·페이지·HTTP 오류 없음',errors.length===0);
await fs.writeFile(new URL('browser-check.json',dir),JSON.stringify({passed:true,checks,errors,font_network:'optional CDN replaced by empty CSS; kit has no external resources'},null,2)+'\n');
console.log(`${checks.length} browser checks passed`);
} finally {await browser.close()}
