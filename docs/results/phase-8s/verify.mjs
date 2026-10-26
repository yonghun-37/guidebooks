// Run: node docs/results/phase-8s/verify.mjs (serve site/ on 8528).
import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base=process.env.SITE_URL || 'http://127.0.0.1:8528/';
const out='docs/results/phase-8s/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext();
const errors=[],checks=[],requests=[];
const check=(name,val)=>{assert.ok(val,name);checks.push(name);};
const page=await context.newPage();
page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('requestfailed',r=>requests.push({url:r.url(),error:r.failure()?.errorText}));
const files=['index.html','ch03-a-axes.html','ch03-b-faq.html','ch03-c-journey.html'];
try{
 for(const width of [1280,375]){
  await page.setViewportSize({width,height:1000});
  for(const file of files){
   await page.goto(base+'drafts/'+file,{waitUntil:'networkidle'});
   await page.evaluate(()=>document.fonts.ready);
   check(`${width} ${file} no horizontal overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   const bad=await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1 || e.getBoundingClientRect().left < -1).filter(e=>getComputedStyle(e).position!=='fixed').map(e=>e.tagName+'.'+e.className));
   check(`${width} ${file} no overflowing element`,bad.length===0);
   if(file!=='index.html'){
    check(`${width} ${file} nine blocks`,await page.locator('[data-block]').count()===9);
    check(`${width} ${file} one simulator`,await page.locator('[data-simulator]').count()===1);
    check(`${width} ${file} three quiz questions`,await page.locator('.draft-quiz details').count()===3);
    await page.locator('.draft-quiz summary').first().focus();await page.keyboard.press('Enter');
    check(`${width} ${file} quiz keyboard`,await page.locator('.draft-quiz details').first().getAttribute('open')!==null);
    await page.keyboard.press('Enter');
   }
   if(file==='ch03-a-axes.html'){
    await page.locator('#axis-picker').selectOption('brand');
    check(`${width} A brand formula`,(await page.locator('#axis-result').textContent()).includes('200,000원'));
    await page.locator('#calc-count').fill('2');check(`${width} A two contracts`,(await page.locator('#axis-result').textContent()).includes('400,000원'));
    await page.locator('#calc-count').fill('');check(`${width} A blank input`,(await page.locator('#axis-result').textContent()).includes('빈칸'));
    await page.locator('#axis-picker').selectOption('affiliate');check(`${width} A affiliate 3 percent`,(await page.locator('#axis-result').textContent()).includes('30,000원'));
    await page.locator('#calc-rate').fill('1');check(`${width} A product-specific rate`,(await page.locator('#axis-result').textContent()).includes('10,000원'));
    await page.locator('#calc-rate').fill('101');check(`${width} A rejects invalid rate`,(await page.locator('#axis-result').textContent()).includes('범위'));
    await page.locator('#axis-picker').selectOption('own');check(`${width} A own sales`,(await page.locator('#axis-result').textContent()).includes('100,000원'));
    await page.locator('#calc-count').fill('0');check(`${width} A zero sales`,(await page.locator('#axis-result .draft-big').textContent())==='0원');
    await page.locator('#calc-price').fill('-1');check(`${width} A rejects negative`,(await page.locator('#axis-result').textContent()).includes('범위'));
    await page.locator('#axis-picker').selectOption('views');check(`${width} A noninvited views zero`,(await page.locator('#axis-result .draft-big').textContent())==='0원');
   }
   if(file==='ch03-b-faq.html')for(let i=1;i<=10;i++){
    await page.locator('#question-picker').selectOption(`q-${i}`);
    check(`${width} B question ${i}`,await page.locator('#question-result h3').textContent()===await page.locator(`#q-${i} h3`).textContent());
   }
   if(file==='ch03-c-journey.html'){
    for(let i=0;i<5;i++){
     await page.locator('#stage-slider').fill(String(i));
     check(`${width} C stage ${i}`,await page.locator('#stage-result h3').textContent()===await page.locator('.draft-stage h3').nth(i).textContent());
    }
    await page.locator('#stage-slider').focus();await page.keyboard.press('Home');await page.keyboard.press('ArrowRight');
    check(`${width} C range keyboard`,await page.locator('#stage-label').textContent()==='500명');
   }
   const localLinks=await page.locator('a[href]').evaluateAll(as=>as.map(a=>a.href).filter(h=>h.startsWith(location.origin)));
   for(const href of [...new Set(localLinks)]){
    const u=new URL(href);const response=await context.request.get(u.origin+u.pathname);
    check(`${width} ${file} local link ${u.pathname}${u.hash}`,response.ok());
    if(u.hash){const html=await response.text();check(`${width} ${file} anchor ${u.hash}`,html.includes(`id="${decodeURIComponent(u.hash.slice(1))}"`));}
   }
   await page.goto(base+'drafts/'+file,{waitUntil:'networkidle'});
   await page.screenshot({path:out+file.replace('.html','')+`-${width}.png`,fullPage:true});
   if(file==='ch03-a-axes.html')await page.screenshot({path:out+`a-opening-${width}.png`,fullPage:false});
  }
 }
 // Storage denial should not break navigation, calculator, or checkboxes.
 await page.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError');}}));
 await page.goto(base+'drafts/ch03-a-axes.html');await page.locator('[data-draft-check]').first().check();
 check('storage denied status',(await page.locator('#save-status').textContent()).includes('저장할 수 없는'));
 await page.locator('#axis-picker').selectOption('brand');check('storage denied calculator',(await page.locator('#axis-result').textContent()).includes('200,000원'));
 await fs.writeFile(out+'last-run-errors.json',JSON.stringify({errors,failedRequests:requests},null,2));
 check('console and page errors zero',errors.length===0);
 await fs.writeFile(out+'browser-check.json',JSON.stringify({base,viewports:[1280,375],checks,errors,failedRequests:requests,fontMode:'Live CDN; document.fonts.ready awaited, no network mocks.'},null,2));
 console.log(checks.length+' checks passed; errors='+errors.length+'; failed requests='+requests.length);
}finally{await browser.close();}
