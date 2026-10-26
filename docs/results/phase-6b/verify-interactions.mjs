import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base=process.env.SITE_URL || 'http://127.0.0.1:8561/';
const out='docs/results/phase-6b/interaction/';
const executablePath=process.env.CHROMIUM_PATH || '/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome';
const browser=await chromium.launch({executablePath,headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage();const checks=[],errors=[],requests=[],sizes=[];
let actions=false;
page.on('pageerror',e=>errors.push(String(e)));
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
page.on('request',r=>{if(actions)requests.push(r.url());});
const check=(label,condition)=>{assert.ok(condition,label);checks.push(label);};
const key=async(locator,press='Enter')=>{await locator.focus();await page.keyboard.press(press);};
const text=async(locator,value)=>{await locator.focus();await page.keyboard.press('ControlOrMeta+A');await page.keyboard.insertText(String(value));};
const choose=async(locator,index)=>{await locator.focus();await page.keyboard.press('Home');for(let i=0;i<index;i++)await page.keyboard.press('ArrowDown');await page.keyboard.press('Tab');};
const open=async(root,needle)=>{const s=root.locator('summary').filter({hasText:needle});if(!(await s.evaluate(e=>e.parentElement.open)))await key(s);};
const result=async root=>root.locator('[data-sim-result]').textContent();
const shot=async(name,root)=>{if(!['R01-after-360','R02-after-360','R03-after-360','R03-after-1280'].includes(name))return;await root.evaluate(e=>window.scrollTo({top:e.getBoundingClientRect().top+scrollY-76,behavior:'instant'}));await page.screenshot({path:out+name+'.png'});};
const rows=[['R01','revenue','chapters/03-revenue'],['R02','cards','chapters/07-cards'],['R03','reels','chapters/08-reels'],['R04','publishing','chapters/10-publishing'],['R05','safety','chapters/12-safety'],['P04','cards','practice/04-cards'],['P05','reels','practice/05-reel'],['P08','publishing','practice/08-api'],['P06','safety','practice/06-review']];
async function revenue(root,tag){
 check(tag+' affiliate default',(await result(root)).startsWith('30,000원'));
 await text(root.locator('[data-value="1"]'),0);check(tag+' actual zero',(await result(root)).startsWith('0원'));
 await text(root.locator('[data-value="1"]'),'');check(tag+' empty not zero',(await result(root)).startsWith('—'));
 await text(root.locator('[data-value="1"]'),1.5);check(tag+' fraction refused',(await result(root)).startsWith('—'));
 await text(root.locator('[data-value="1"]'),21);
 await key(root.locator('[data-choice="sponsor"]'));check(tag+' sponsor isolated',(await result(root)).startsWith('170,000원'));
 await key(root.locator('[data-choice="affiliate"]'));check(tag+' route remembers',(await result(root)).startsWith('31,500원'));
 await open(root,'요율');await text(root.locator('[data-value="3"]'),50000);check(tag+' negative net',(await result(root)).startsWith('-18,500원'));
 await key(root.locator('[data-choice="platform"]'));check(tag+' no views income',(await result(root)).startsWith('0원'));
 check(tag+' no invented views',await root.locator('input:not(:disabled)').count()===2);
 await choose(root.locator('[data-mode]'),1);await text(root.locator('[data-value="0"]'),2000);check(tag+' confirmed manual',(await result(root)).startsWith('2,000원'));
 await key(root.locator('[data-choice="own"]'));check(tag+' own isolated',(await result(root)).startsWith('40,000원'));
 await key(root.locator('[data-choice="affiliate"]'));await key(root.locator('[data-reset]'));
 check(tag+' reset current only',(await result(root)).startsWith('30,000원'));
}
async function cards(root,tag){
 check(tag+' fits default',(await result(root)).startsWith('0줄'));
 await key(root.locator('[data-preset="overflow"]'));check(tag+' actual text overflow',!((await result(root)).startsWith('0줄')));if(tag==='R02 360')await shot('R02-overflow-360',root);
 check(tag+' clipping marked',await root.locator('[data-after] .is-clipped').count()>0);
 await open(root,'크기·여백');await key(root.locator('[data-compare]'));const frozen=await root.locator('[data-before] .card-text').textContent();
 await text(root.locator('[data-copy]'),'짧은 문장입니다.');check(tag+' before remains same source',await root.locator('[data-before] .card-text').textContent()===frozen);
 check(tag+' fixed overflow',(await result(root)).startsWith('0줄'));
 await text(root.locator('[data-copy]'),'<img src=x onerror=alert(1)>\n한글 줄바꿈');check(tag+' escaped text',await root.locator('[data-after] img').count()===0);
 check(tag+' newline kept',(await root.locator('[data-after] .card-text').textContent()).includes('\n'));
 await text(root.locator('[data-copy]'),'A'.repeat(1000));check(tag+' long word overflow',!((await result(root)).startsWith('0줄')));
 await text(root.locator('[data-copy]'),'');await text(root.locator('[data-title]'),'');await text(root.locator('[data-source]'),'');check(tag+' empty strings allowed',(await result(root)).startsWith('0줄'));
 await text(root.locator('[data-value="size"]'),'');check(tag+' empty size refused',(await result(root)).startsWith('—'));
 await text(root.locator('[data-value="size"]'),90);await key(root.locator('[data-size-range]'),'Home');check(tag+' equivalent range',await root.locator('[data-value="size"]').inputValue()==='24');
 await key(root.locator('[data-small]'));check(tag+' small selected',await root.locator('[data-small]').getAttribute('aria-pressed')==='true');
 await key(root.locator('[data-small]'));await key(root.locator('[data-compare]'));await key(root.locator('[data-preset="default"]'));
 const color=await root.locator('[data-after] .card-sheet').evaluate(e=>getComputedStyle(e).backgroundColor);
 await page.evaluate(()=>document.documentElement.dataset.theme='dark');check(tag+' independent artwork',color===await root.locator('[data-after] .card-sheet').evaluate(e=>getComputedStyle(e).backgroundColor));
 await page.evaluate(()=>document.documentElement.dataset.theme='light');
}
async function reels(root,tag){
 check(tag+' tracks',await root.locator('.track').count()===3);check(tag+' repeat named',await root.locator('[data-loop]').getAttribute('aria-label')==='선택 자막 구간 반복');
 await key(root.locator('[data-seek]'),'End');check(tag+' end seek',(await root.locator('[data-clock]').textContent()).startsWith('20.00'));
 check(tag+' end caption blank',(await root.locator('[data-subtitle]').textContent()).includes('없음'));
 await key(root.locator('[data-seek]'),'Home');await key(root.locator('[data-frame="1"]'));check(tag+' one frame',(await root.locator('[data-clock]').textContent()).startsWith('0.04'));
 await key(root.locator('[data-scenes] button').nth(1));check(tag+' scene selected',await root.locator('[data-scenes] button').nth(1).getAttribute('aria-pressed')==='true');
 check(tag+' common clock',(await root.locator('[data-clock]').textContent()).startsWith('4.00'));
 await open(root,'시간 숫자');await text(root.locator('[data-value="start"]'),8);await text(root.locator('[data-value="end"]'),4);await key(root.locator('[data-apply]'));check(tag+' reversed refused',(await result(root)).startsWith('—'));
 await text(root.locator('[data-value="start"]'),3);await text(root.locator('[data-value="end"]'),8);await key(root.locator('[data-apply]'));check(tag+' overlap refused',(await result(root)).startsWith('—'));
 await text(root.locator('[data-value="start"]'),4.1);await text(root.locator('[data-value="end"]'),7.9);await key(root.locator('[data-apply]'));check(tag+' gap reported',(await result(root)).includes('빈 구간'));
 await text(root.locator('[data-value="scene-end"]'),9);await key(root.locator('[data-scene-apply]'));check(tag+' scene boundary accepted',(await root.locator('[data-scenes] button').nth(1).getAttribute('aria-label')).includes('9.0초'));
 await key(root.locator('[data-preset="fast"]'));check(tag+' failure preset',(await result(root)).startsWith('1.0초'));
 const long=await root.locator('[data-caption]').inputValue();await key(root.locator('[data-repair]'));check(tag+' repairs one variable',(await root.locator('[data-caption]').inputValue()).length<long.length && (await result(root)).startsWith('1.0초'));
 await key(root.locator('[data-loop]'));await key(root.locator('[data-play]'));await page.waitForTimeout(1350);
 const during=await root.locator('[data-seek]').inputValue();check(tag+' repeat stays in range',Number(during)>=0 && Number(during)<24);
 await key(root.locator('[data-play]'));const paused=await root.locator('[data-clock]').textContent();await page.waitForTimeout(300);check(tag+' frame frozen',paused===await root.locator('[data-clock]').textContent());
 await key(root.locator('[data-play]'));await text(root.locator('[data-caption]'),'새 자막');check(tag+' editing shares clock',await root.locator('[data-play]').getAttribute('aria-pressed')==='true');
 await page.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));delete document.hidden;});check(tag+' hidden event pauses',await root.locator('[data-play]').getAttribute('aria-pressed')==='false');
 await key(root.locator('[data-preset="default"]'));
}
async function publishing(root,tag){
 for(let i=0;i<2;i++)await key(root.locator('[data-next]'));
 check(tag+' accepted not posted',(await result(root)).startsWith('0건') && (await root.locator('[data-state]').textContent()).includes('생성 요청 성공'));
 for(let i=0;i<3;i++)await key(root.locator('[data-next]'));
 check(tag+' complete requires verification',(await result(root)).startsWith('1건'));
 await key(root.locator('[data-prev]'));check(tag+' previous snapshot',(await result(root)).startsWith('0건'));
 for(const [index,stage] of [[1,1],[2,3],[3,4]]){
  await choose(root.locator('[data-scenario]'),index);
  for(let i=0;i<stage;i++)await key(root.locator('[data-next]'));
  check(tag+` failure ${index} blocked`,await root.locator('[data-next]').isDisabled());
  if(index===3){if(tag==='R04 360')await shot('R04-unknown-360',root);await key(root.locator('[data-retry]'));check(tag+' unknown avoids duplicate',(await result(root)).startsWith('0건 재시도'));}
  await key(root.locator('[data-resolve]'));
  check(tag+` failure ${index} resolve`,index===3?(await result(root)).startsWith('1건'):!await root.locator('[data-next]').isDisabled());
 }
 await choose(root.locator('[data-scenario]'),0);await key(root.locator('[data-auto]'));await page.waitForTimeout(1900);check(tag+' automatic advances',await root.locator('.step-flow li').nth(1).getAttribute('aria-current')==='step');await key(root.locator('[data-auto]'));check(tag+' automatic stops',await root.locator('[data-auto]').getAttribute('aria-pressed')==='false');
 await key(root.locator('[data-reset]'));
}
async function safety(root,tag){
 check(tag+' clue live',await root.locator('[data-clue]').getAttribute('aria-live')==='polite');
 check(tag+' evidence gates judgment',await root.locator('[data-decision]:disabled').count()===4);
 await key(root.locator('[data-evidence] [data-choice="rights"]'));await choose(root.locator('[data-decision="rights"]'),2);check(tag+' evidence absence not permission',(await result(root)).includes('문제가 남아'));
 await key(root.locator('[data-evidence] [data-choice="rights"]'));check(tag+' clues deduplicated',await root.locator('[data-evidence-log] li').count()===1);
 await key(root.locator('[data-evidence] [data-choice="ad"]'));check(tag+' labels need both clues',await root.locator('[data-decision="labels"]').isDisabled());
 await key(root.locator('[data-evidence] [data-choice="ai"]'));await open(root,'문제 고치기');await key(root.locator('[data-fix="labels"]'));await choose(root.locator('[data-decision="labels"]'),2);check(tag+' labels fix independent',(await result(root)).startsWith('3개') && await root.locator('[data-decision="rights"]').inputValue()!=='clear');
 for(const clue of ['facts','security'])await key(root.locator(`[data-evidence] [data-choice="${clue}"]`));
 for(const group of ['rights','facts']){await key(root.locator(`[data-fix="${group}"]`));await choose(root.locator(`[data-decision="${group}"]`),2);}
 await choose(root.locator('[data-decision="security"]'),2);check(tag+' evidence based completion',(await result(root)).startsWith('0개'));
 await choose(root.locator('[data-case]'),1);check(tag+' case resets',(await result(root)).startsWith('4개') && await root.locator('[data-evidence-log] li').count()===0);
 for(const clue of ['rights','facts','ad','ai','security'])await key(root.locator(`[data-evidence] [data-choice="${clue}"]`));
 await choose(root.locator('[data-decision="rights"]'),2);check(tag+' documented permission',(await result(root)).startsWith('3개'));
 for(const group of ['facts','labels','security']){await key(root.locator(`[data-fix="${group}"]`));await choose(root.locator(`[data-decision="${group}"]`),2);}
 check(tag+' second case complete',(await result(root)).startsWith('0개'));
 await choose(root.locator('[data-case]'),0);
}
const test={revenue,cards,reels,publishing,safety};
try{
 for(const width of [360,375,1280]){
  await page.setViewportSize({width,height:850});
  for(const [id,kind,slug] of rows){
   actions=false;await page.goto(base+'site/'+slug+'.html',{waitUntil:'networkidle'});actions=true;
   const root=page.locator('[data-interaction]'),tag=`${id} ${width}`;
   check(tag+' single tool',await root.count()===1);
   check(tag+' no overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   check(tag+' named region',await root.getAttribute('role')==='region' && !!await root.getAttribute('aria-labelledby'));
   check(tag+' live state',await root.locator('[data-sim-result]').getAttribute('aria-live')==='polite');
   const primary=await root.evaluate(e=>{const r=e.getBoundingClientRect(),s=e.querySelector('[data-sim-result]').getBoundingClientRect();return {height:r.height,resultBottom:s.bottom-r.top,width:r.width};});sizes.push({id,viewportWidth:width,...primary});
   check(tag+' primary result near one screen',primary.resultBottom <= (kind === 'reels' ? 950 : 740));
   if(id.startsWith('R'))await shot(`${id}-after-${width}`,root);
   // Tab으로 실제 도구 순서를 끝까지 지나며 초점과 탈출을 확인한다.
   const focusable=root.locator('button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea, summary, a').filter({visible:true});
   await focusable.first().focus();let traversed=0;
   for(let n=0;n<70;n++){
    if(!await root.evaluate(e=>e.contains(document.activeElement)))break;
    check(tag+` focus ${n}`,await page.evaluate(()=>getComputedStyle(document.activeElement).outlineStyle!=='none'));
    traversed++;await page.keyboard.press('Tab');
   }
   check(tag+' tab exits',traversed>4 && !await root.evaluate(e=>e.contains(document.activeElement)));
   await test[kind](root,tag);
   check(tag+' edited no overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   check(tag+' reduced animations',await root.evaluate(e=>[e,...e.querySelectorAll('*')].every(n=>getComputedStyle(n).animationName==='none' && getComputedStyle(n).transitionDuration.split(',').every(v=>parseFloat(v)===0))));
   console.log(tag+' passed');
  }
  actions=false;await page.goto(base+'site/lab.html',{waitUntil:'networkidle'});
  for(const [id,kind,slug] of rows.filter(r=>r[0].startsWith('R'))){
   // 원본 목록의 도구 ID로 선택한다. 선택 자체도 키보드로 한다.
   const toolId={R01:'ledger-sim',R02:'ch7-sim',R03:'ch8-sim',R04:'publishing-sim',R05:'safety-sim'}[id];
   const index=await page.locator('#sim-picker option').evaluateAll((opts,id)=>opts.findIndex(o=>o.value.endsWith(':'+id)),toolId);
   await choose(page.locator('#sim-picker'),index);
   const embedded=page.frameLocator('#sim-frame').locator('[data-interaction]');await page.waitForFunction(kind=>document.querySelector('#sim-frame').contentDocument?.querySelector('[data-interaction]')?.dataset.interaction===kind,kind);await embedded.waitFor({state:'visible'});
   check(`lab ${id} ${width}`,await embedded.getAttribute('data-interaction')===kind);
  }
  check('lab '+width+' no overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.goto(base+'site/index.html',{waitUntil:'networkidle'});check('cover paths '+width,await page.locator('#short-paths a').count()===6);check('cover no overflow '+width,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 }
 // 오답 링크가 실제로 해당 도구의 실패/오해 상태를 연다.
 for(const [slug,index,preset] of [['03-revenue',0,'platform'],['07-cards',0,'overflow'],['08-reels',1,'fast'],['10-publishing',2,'unknown'],['12-safety',0,'mixed']]){
  actions=false;await page.goto(base+'site/chapters/'+slug+'.html',{waitUntil:'networkidle'});
  await key(page.locator('[data-question]').nth(index).locator('[data-correct="false"]').first());
  const link=page.locator('[data-question]').nth(index).locator('[data-feedback] a');check('retry link '+slug,(await link.getAttribute('href')).includes('toolPreset='+preset));
  await Promise.all([page.waitForURL(url=>url.searchParams.get('toolPreset')===preset),key(link)]);await page.waitForLoadState('networkidle');check('retry loaded '+slug,new URL(page.url()).searchParams.get('toolPreset')===preset);
  if(preset==='overflow')check('retry card preset',!((await result(page.locator('[data-interaction]'))).startsWith('0줄')));
  if(preset==='fast')check('retry reel preset',(await result(page.locator('[data-interaction]'))).startsWith('1.0초'));
  if(preset==='platform')check('retry platform preset',await page.locator('[data-routes] [data-choice="platform"]').getAttribute('aria-pressed')==='true');
  if(preset==='unknown')check('retry publish preset',await page.locator('[data-scenario]').inputValue()==='unknown');
 }
 for(const [slug,id] of [['10-publishing','simulator'],['12-safety','simulator'],['10-publishing','publishing-sim'],['12-safety','safety-sim']]) {
  actions=false;await page.goto(base+'site/chapters/'+slug+'.html?embed='+id,{waitUntil:'networkidle'});
  check('legacy embed '+slug+' '+id,await page.locator('[data-interaction]').isVisible());
 }
 // 일반 모션도 사용자가 누를 때만 재생되며 같은 시계를 따른다.
 actions=false;await page.emulateMedia({reducedMotion:'no-preference'});await page.goto(base+'site/chapters/08-reels.html',{waitUntil:'networkidle'});
 await page.waitForTimeout(300);check('no autoplay',await page.locator('[data-play]').getAttribute('aria-pressed')==='false');await key(page.locator('[data-play]'));await page.waitForTimeout(400);check('normal motion progresses',Number(await page.locator('[data-seek]').inputValue())>0);await key(page.locator('[data-play]'));
 check('no action network requests',requests.length===0);check('console page http errors zero',errors.length===0);
 await fs.writeFile(out+'browser-check.json',JSON.stringify({checks:checks.length,errors,actionRequests:requests,sizes,details:checks},null,2)+'\n');
 console.log(JSON.stringify({checks:checks.length,errors,actionRequests:requests.length,sizes},null,2));
}finally{await browser.close();}
