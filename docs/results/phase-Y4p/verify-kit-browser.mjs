import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';import assert from 'node:assert/strict';
const root=(await fs.readFile('/tmp/y4p-kit-path','utf8')).trim();
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});const page=await browser.newPage();const checks=[],errors=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});const check=(s,v)=>{assert.ok(v,s);checks.push(s);};
try{
 await page.goto('file://'+root+'/output/my-script/preview.html');
 const video=page.locator('video').first();await video.evaluate(v=>v.play());await page.waitForTimeout(450);
 check('실제 MP4 재생',await video.evaluate(v=>v.currentTime>0));check('실제 출력 치수',await video.evaluate(v=>v.videoWidth===1080&&v.videoHeight===1920));
 await video.evaluate(v=>{v.pause();v.currentTime=18;});await page.waitForTimeout(250);check('중간 장면 탐색',await video.evaluate(v=>Math.abs(v.currentTime-18)<0.2));
 for(const width of [1280,375,360]){await page.setViewportSize({width,height:1000});check('키트 넘침 '+width,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.screenshot({path:`docs/results/phase-Y4p/kit-preview-${width}.png`});}
 await video.evaluate(v=>{v.currentTime=35;return v.play();});await page.waitForTimeout(1600);check('마지막까지 재생',await video.evaluate(v=>v.ended||v.currentTime>=35.9));check('브라우저 오류 0',errors.length===0);
 await fs.writeFile('docs/results/phase-Y4p/kit-browser-check.json',JSON.stringify({scope:'Linux Chromium; actual clean-copy MP4; synthetic tone M4A, generated illustration, no human recording or TTS login',checks,errors},null,2));console.log(checks.length+' checks passed');
}finally{await browser.close();}
