// 접기 상자로 옮긴 기존 카드/릴스 도구의 키보드 조작과 재측정을 검사.
import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const page=await browser.newPage(),checks=[],errors=[];
page.on('pageerror',e=>errors.push(String(e)));
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
try{
for(const width of [1280,375,360]){
 await page.setViewportSize({width,height:900});
 for(const theme of ['light','dark']){
  await page.goto('http://127.0.0.1:8593/site/practice/04-cards.html');
  await page.locator('[data-theme-select]').selectOption(theme);
  check(`card initially folded ${width} ${theme}`,!await page.locator('#kit').evaluate(e=>e.open));
  await page.locator('#kit > summary').focus();await page.keyboard.press('Enter');
  await page.waitForFunction(()=>document.querySelector('#ch7-sim .card-sheet').style.transform!=='scale(0)');
  check(`card visible preview ${width} ${theme}`,await page.locator('#ch7-sim [data-after] .card-sheet').evaluate(e=>e.getBoundingClientRect().width>100));
  await page.locator('#ch7-sim [data-preset="overflow"]').focus();await page.keyboard.press('Enter');
  check(`card overflow preset ${width} ${theme}`,!(await page.locator('#ch7-sim [data-sim-result]').innerText()).startsWith('0줄'));
  await page.locator('#ch7-sim [data-preset="default"]').focus();await page.keyboard.press('Enter');
  check(`card restore ${width} ${theme}`,(await page.locator('#ch7-sim [data-sim-result]').innerText()).startsWith('0줄'));
  await page.goto('http://127.0.0.1:8593/site/practice/05-reel.html');
  await page.locator('[data-theme-select]').selectOption(theme);
  await page.locator('#kit > summary').focus();await page.keyboard.press('Enter');
  const seek=page.locator('#ch8-sim [data-seek]');await seek.focus();await page.keyboard.press('ArrowRight');
  check(`reel keyboard seek ${width} ${theme}`,Number(await seek.inputValue())>0);
  const play=page.locator('#ch8-sim [data-play]');await play.focus();await page.keyboard.press('Enter');
  check(`reel keyboard play ${width} ${theme}`,await play.getAttribute('aria-pressed')==='true');
  await page.keyboard.press('Enter');check(`reel keyboard pause ${width} ${theme}`,await play.getAttribute('aria-pressed')==='false');
  check(`expanded no overflow ${width} ${theme}`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 }
}
check('preserved tools page errors zero',errors.length===0);
}finally{await fs.writeFile('docs/results/phase-AIc/preserved-check.json',JSON.stringify({passed:checks.length,checks,errors},null,2));await browser.close();}
console.log('PASS '+checks.length);
