// GitHub Actions와 같은 배치를 /guidebooks/ 아래에 조립해 검사한다.
import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const root='/tmp/phase9int-pages/guidebooks';
await fs.cp('shelf',root,{recursive:true});await fs.cp('site',root+'/reels',{recursive:true});
await fs.mkdir(root+'/progress/samples',{recursive:true});
for(const name of await fs.readdir('starter-kit/samples'))if(/\.(png|mp4)$/.test(name))await fs.copyFile('starter-kit/samples/'+name,root+'/progress/samples/'+name);
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const page=await browser.newPage(),errors=[],checks=[];
await page.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
const check=(name,ok)=>{assert.ok(ok,name);checks.push(name);};
try{
 for(const width of [1280,375,360]){
  await page.setViewportSize({width,height:1000});
  for(const path of ['','progress/','reels/','reels/lab.html','reels/practice/00-start.html']){
   await page.goto('http://127.0.0.1:8550/guidebooks/'+path,{waitUntil:'networkidle'});
   check(`${path} ${width} no overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   const links=await page.locator('a[href],img[src],video[src]').evaluateAll(ns=>ns.map(n=>n.href||n.src).filter(s=>s.startsWith(location.origin)));
   for(const url of new Set(links))check(`deployed ${new URL(url).pathname}`,(await page.request.get(url)).ok());
   if(path==='progress/'&&width===375)await page.screenshot({path:'docs/results/phase-9-int/progress-375.png'});
  }
 }
 check('no errors',errors.length===0);
 await fs.writeFile('docs/results/phase-9-int/deployed-check.json',JSON.stringify({checks:checks.length,errors,passed:checks},null,2)+'\n');
 console.log(JSON.stringify({checks:checks.length,errors}));
}finally{await browser.close();}
