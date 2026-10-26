import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';import fs from 'node:fs/promises';
const b=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox'],headless:true});
const p=await b.newPage();let checks=0;const errors=[];p.on('pageerror',e=>errors.push(String(e)));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
try{for(const width of [1280,375,360])for(const theme of ['light','dark']){
 await p.setViewportSize({width,height:1000});await p.emulateMedia({colorScheme:theme});
 for(const path of ['progress/','']){
  await p.goto('http://127.0.0.1:8597/'+path);assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));checks++;
  if(path){assert.ok((await p.locator('main').innerText()).includes('AId AI 제작 모듈 통합'));checks++;
   if(theme==='light')await p.screenshot({path:`docs/results/phase-AId/shelf-progress-index-${width}.png`});}
 }
}assert.equal(errors.length,0);checks++;}finally{await fs.writeFile('docs/results/phase-AId/progress-check.json',JSON.stringify({checks,errors},null,2));await b.close()}
console.log('PASS '+checks+' progress checks');
