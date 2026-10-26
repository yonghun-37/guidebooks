import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({permissions:['clipboard-read','clipboard-write'],reducedMotion:'reduce'});
if(!process.env.FONT_NETWORK)await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage(),checks=[],errors=[];
const base='http://127.0.0.1:8596/site/';
const check=(name,value)=>{assert.ok(value,name);checks.push(name)};
const key=async(loc,k='Enter')=>{await loc.focus();await page.keyboard.press(k)};
page.on('pageerror',e=>errors.push(String(e)));
page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
try{
for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const path of ['chapters/05b-ai-tools.html','prompts.html','ai-models.html']){
 await page.setViewportSize({width,height:1000});
 const response=await page.goto(base+path);check('페이지 존재 '+path,response.status()===200);
 await page.locator('[data-theme-select]').selectOption(theme);await page.evaluate(()=>document.fonts.ready);
 check('가로 넘침 없음 '+path+width+theme,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 if(path.includes('05b')){
  await page.selectOption('#tool-content','cards');await key(page.locator('#tool-content'),'ArrowDown');
  check('select keyboard content',await page.locator('#tool-content').inputValue()==='motion');
  await page.selectOption('#tool-budget','free');await key(page.locator('#tool-budget'),'ArrowDown');
  check('select keyboard budget',(await page.locator('#tool-price').textContent()).includes('24,800'));

  check('9 blocks',await page.locator('[data-block]').count()===9);check('FAQ5',await page.locator('.chapter-faq details').count()===5);
  for(const content of ['cards','motion','explain','video'])for(const budget of ['free','paid'])for(const ko of ['yes','no']){
   await page.selectOption('#tool-content',content);await page.selectOption('#tool-budget',budget);await page.selectOption('#tool-korean',ko);
   const result=await page.locator('#tool-result').textContent();check('selection '+content+budget+ko,result.includes('ChatGPT')&&result.includes(budget==='free'?'0원':content==='video'?'29,000':content==='cards'?'14,900':'24,800'));
  }
  await key(page.locator('[data-tool-preset]'));check('free extreme',await page.locator('#tool-budget').inputValue()==='free');
  for(const q of await page.locator('[data-question]').all())await key(q.locator('[data-correct="true"]'),'Space');
  check('quiz correct',(await page.locator('[data-quiz-score]').textContent()).includes('3문항 정답'));
  await key(page.locator('[data-quiz-reset]'));
 }
 if(path==='prompts.html'){
  check('six prompts',await page.locator('[data-prompt]').count()===6);
  for(const p of await page.locator('[data-prompt]').all()){
   await key(p.locator('[data-copy-prompt]'));
   check('clipboard exact',await page.evaluate(()=>navigator.clipboard.readText())===await p.locator('textarea').inputValue());
  }
 }
 if(path==='ai-models.html'){
  check('Codex service preserved',(await page.locator('[data-model-row]').first().textContent()).includes('Codex'));
  const total=await page.locator('[data-model-row]').count();check('research full table',total===274);
  for(const cat of ['text','image','video','voice','music','editor']){
   await page.selectOption('#model-category',cat);
   if(width<700)check('mobile caption width '+cat,await page.locator('[data-model-section]:visible caption').first().evaluate(e=>e.getBoundingClientRect().width>=e.closest('table').getBoundingClientRect().width-2));
   check('category only '+cat,await page.locator('[data-model-row]:visible').evaluateAll((rows,cat)=>rows.length>0&&rows.every(r=>r.dataset.category===cat),cat));
  }
  await page.selectOption('#model-category','all');await page.fill('#model-search','없는모델xyz');check('empty state',await page.locator('#model-empty').isVisible());
  await page.fill('#model-search','GPT');check('search matches',await page.locator('[data-model-row]:visible').count()>0);
  await key(page.locator('#model-reset'));check('reset all',await page.locator('[data-model-row]:visible').count()===total);
  for(const content of ['cards','explain','video'])for(const combo of ['free','low','high']){
   await page.selectOption('#cost-content',content);await page.selectOption('#cost-combo',combo);await page.selectOption('#cost-attempts','1');
   const expected={cards:{free:0,low:95.445,high:1211.625},explain:{free:0,low:101.655,high:1294.125},video:{free:0,low:2776.545,high:17374.5}}[content][combo];
   check('cost '+content+combo,Math.abs(Number(await page.locator('#cost-result').getAttribute('data-value'))-expected)<0.001);
  }
  await page.selectOption('#cost-content','explain');await page.selectOption('#cost-combo','high');await page.selectOption('#cost-attempts','2');
  check('TTS not double billed',Math.abs(Number(await page.locator('#cost-result').getAttribute('data-value'))-2505.75)<0.001);
  check('new Typecast cash',(await page.locator('#cost-cash').textContent()).includes('12,323.25'));
  await page.selectOption('#cost-content','video');await page.selectOption('#cost-combo','free');
  check('free overflow headline',(await page.locator('#cost-result').textContent()).includes('초과'));
  check('free credit overflow',(await page.locator('#cost-formula').textContent()).includes('96'));
  check('no guaranteed free',(await page.locator('#cost-note').textContent()).includes('50'));
  await key(page.locator('[data-cost-reset]'));
  await key(page.locator('#cost-attempts'),'ArrowDown');check('cost keyboard retry',(await page.locator('#cost-formula').textContent()).includes('2회'));
  await key(page.locator('[data-cost-reset]'));
  await page.selectOption('#model-category','text');await page.fill('#model-search','GPT-6 Luna');
  if(theme==='light'){
   await page.locator('#model-search').evaluate(e=>window.scrollTo({top:e.getBoundingClientRect().top+scrollY-160,behavior:"instant"}));
   await page.screenshot({path:new URL(`./models-table-${width}.png`,import.meta.url).pathname});
  }
  await key(page.locator('#model-reset'));

 }
 if(theme==='light'){
  const selector=path.includes('05b')?'#simulator':path==='prompts.html'?'#summary-prompt':'#cost-calculator';
  await page.locator(selector).evaluate(e=>window.scrollTo({top:e.getBoundingClientRect().top+scrollY-85,behavior:"instant"}));
  await page.screenshot({path:new URL(`./ai-${path.includes('05b')?'tools':path==='prompts.html'?'prompts':'models'}-${width}.png`,import.meta.url).pathname});
 }
 check('after interaction overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
}
await page.goto(base+'prompts.html');await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{value:{writeText:async()=>{throw Error('denied')}}}));
await key(page.locator('[data-copy-prompt]').first());check('denied fallback',(await page.locator('[data-copy-status]').first().textContent()).includes('Ctrl+C'));
check('fallback selected',await page.locator('[data-prompt] textarea').first().evaluate(e=>e.selectionStart===0&&e.selectionEnd===e.value.length));
const nojs=await browser.newContext({javaScriptEnabled:false});const plain=await nojs.newPage();
for(const p of ['chapters/05b-ai-tools.html','prompts.html','ai-models.html']){await plain.goto(base+p);check('noJS readable '+p,(await plain.locator('main').textContent()).length>500)}
check('console and requests clean',errors.length===0);
}finally{
 await fs.writeFile(new URL('./ai-check.json',import.meta.url),JSON.stringify({checks:checks.length,errors,passed:checks},null,2)+'\n');await browser.close();
}
console.log(`${checks.length} checks passed`);
