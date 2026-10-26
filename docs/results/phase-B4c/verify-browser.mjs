import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='docs/results/phase-B4c',origin='http://127.0.0.1:8624',base=origin+'/site-blog/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage(),checks=[],errors=[],links=new Set();
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
const watch=p=>{p.on('console',m=>{if(m.type()==='error')errors.push(m.text());});p.on('pageerror',e=>errors.push(String(e)));p.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(r.status()+' '+r.url());});};watch(page);
const slugs=['10-automation','11-analytics','12-policy','13-plan'],tools=['automation-tool','analytics-tool','disclosure-tool','plan-tool'];
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
try {
 for(const width of [1280,375,360])for(const theme of ['light','dark'])for(let i=0;i<slugs.length;i++){
  const slug=slugs[i],tag=`${slug}/${width}/${theme}`;
  await page.setViewportSize({width,height:1000});await page.goto(base+`chapters/${slug}.html`);await page.selectOption('[data-theme-select]',theme);await page.evaluate(()=>document.fonts.ready);
  check(`${tag} body overflow0`,await overflow());
  check(`${tag} nine blocks`,await page.locator('[data-block]').count()===9);
  check(`${tag} FAQ5`,await page.locator('.chapter-faq details').count()===5);
  check(`${tag} quiz3`,await page.locator('[data-question]').count()===3);
  await page.locator('[data-menu-toggle]').focus();await page.keyboard.press('Enter');check(`${tag} menu Enter`,await page.locator('[data-menu-toggle]').getAttribute('aria-expanded')==='true');await page.keyboard.press('Escape');check(`${tag} menu Escape focus`,await page.locator('[data-menu-toggle]').evaluate(n=>document.activeElement===n&&n.getAttribute('aria-expanded')==='false'));
  await page.locator('[data-axis-nav] a').first().focus();await page.keyboard.press('Enter');check(`${tag} axis focus`,await page.evaluate(()=>document.activeElement.id==='templates'||document.activeElement.id==='visits'||document.activeElement.id==='disclosure'||document.activeElement.id==='first'));
  const faq=page.locator('.chapter-faq summary').first();await faq.focus();await page.keyboard.press('Enter');check(`${tag} FAQ keyboard`,await faq.evaluate(n=>n.parentElement.open));
  for(const q of await page.locator('[data-question]').all()){await q.locator('[data-correct=true]').focus();await page.keyboard.press('Enter');check(`${tag} quiz correct`,await q.locator('[data-feedback]').isVisible());}
  await page.locator('[data-quiz-reset]').focus();await page.keyboard.press('Enter');check(`${tag} quiz reset`,await page.locator('[data-feedback]:visible').count()===0);
  for(const href of await page.locator('a[href]').evaluateAll(ns=>ns.map(n=>n.href).filter(h=>h.startsWith(location.origin))))links.add(href);
  await page.locator('main details').evaluateAll(ns=>ns.forEach(n=>n.open=true));check(`${tag} opened FAQ overflow0`,await overflow());
  await page.locator('#'+tools[i]).scrollIntoViewIfNeeded();
  if(i===0){await page.selectOption('#template-kind','review');check(`${tag} template selection`,await page.locator('#template-value').innerText()==='사용 메모');}
  if(i===1){await page.locator('#analytics-run').focus();await page.keyboard.press('Enter');check(`${tag} CTR keyboard`,await page.locator('#analytics-value').innerText()==='2%');await page.selectOption('#metric','rpm');check(`${tag} RPM`,await page.locator('#analytics-value').innerText()==='500원');}
  if(i===2){await page.locator('#place-first').focus();await page.keyboard.press('ArrowDown');await page.locator('#disclosure-run').focus();await page.keyboard.press('Enter');check(`${tag} radio keyboard`,await page.locator('#place-title').isChecked());}
  if(i===3){await page.locator('#plan-run').focus();await page.keyboard.press('Enter');check(`${tag} generate keyboard`,await page.locator('#plan-body tr').count()===30);const box=page.locator('#plan-body input').first();await box.focus();await page.keyboard.press('Space');check(`${tag} plan checkbox`,await box.isChecked());}
  check(`${tag} tool overflow0`,await overflow());
  await page.locator('#'+tools[i]).evaluate(n=>{n.scrollIntoView({block:'start'});scrollBy(0,-85);});await page.screenshot({path:`${out}/${slug}-${width}-${theme}.png`});
  if(width===1280&&theme==='light'){await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${out}/${slug}-hero.png`});}
 }
 // Search/advertising denominators, missing values and invalid counts.
 await page.goto(base+'chapters/11-analytics.html');
 await page.selectOption('#query-fit','unknown');await page.click('#analytics-run');check('unknown query prompts report',/보고서/.test(await page.locator('#analytics-meaning').innerText()));
 await page.fill('#clicks-after','2001');await page.click('#analytics-run');check('clicks > impressions rejected',await page.locator('#analytics-value').innerText()==='입력 확인');
 await page.fill('#clicks-after','-1');await page.click('#analytics-run');check('negative rejected',await page.locator('#analytics-value').innerText()==='입력 확인');
 await page.fill('#clicks-after','0.5');await page.click('#analytics-run');check('fractional count rejected',await page.locator('#analytics-value').innerText()==='입력 확인');
 await page.click('#analytics-default');await page.click('#analytics-zero');check('CTR zero denominator',await page.locator('#analytics-value').innerText()==='계산 보류');
 await page.selectOption('#metric','rpm');check('RPM zero denominator',await page.locator('#analytics-value').innerText()==='계산 보류');
 await page.click('#analytics-default');await page.fill('#income-after','0');await page.click('#analytics-run');check('zero income valid',await page.locator('#analytics-value').innerText()==='0원');
 await page.click('#analytics-missing');check('missing is not zero',await page.locator('#analytics-value').innerText()==='미집계');
 await page.click('#analytics-run');check('blank not calculated',await page.locator('#analytics-value').innerText()==='입력 확인');
 await page.click('#analytics-default');await page.fill('#income-after','1e308');await page.fill('#pv-after','1');await page.click('#analytics-run');check('overflow no Infinity',await page.locator('#analytics-value').innerText()==='입력 확인');
 // Both valid and hidden/end positions for every relationship.
 await page.goto(base+'chapters/12-policy.html');
 for(const relation of ['product','both','affiliate'])for(const place of ['first','title','end','hidden']){
  await page.selectOption('#disclosure-relation',relation);await page.check('#place-'+place);await page.click('#disclosure-run');check(`${relation}/${place} verdict`,await page.locator('#disclosure-value').innerText()===(['first','title'].includes(place)?'위치 적절':'수정'));
  const sentence=await page.locator(place==='first'?'#preview-disclosure':place==='title'?'#preview-title':'#preview-end').innerText();check(`${relation}/${place} real relationship`,relation==='both'?sentence.includes('제품과 원고료'):relation==='affiliate'?sentence.includes('수수료'):sentence.includes('제품을 무료'));
 }
 await page.locator('#disclosure-extreme').focus();await page.keyboard.press('Space');check('disclosure extreme keyboard',await page.locator('#place-hidden').isChecked());
 // Date arithmetic, 60-minute budget, no invented experience, export and reset.
 await page.goto(base+'chapters/13-plan.html');
 await page.fill('#plan-start','2028-02-20');await page.fill('#plan-work','10');await page.click('#plan-run');check('date crosses leap day',/2028-03-20/.test(await page.locator('#plan-body tr').last().innerText()));check('budget exactly60',/10분.*40분.*10분.*60분/.test(await page.locator('#plan-budget').innerText()));
 for(const focus of ['all','info','travel','review']){await page.selectOption('#plan-focus',focus);await page.selectOption('#plan-used','no');await page.click('#plan-run');check(`${focus} complete plan`,await page.locator('#plan-body tr').count()===30);if(['all','review'].includes(focus))check(`${focus} no false review`,/공식 사양/.test(await page.locator('#plan-meaning').innerText()));}
 await page.fill('#plan-work','31');await page.click('#plan-run');check('over budget rejected',await page.locator('#plan-value').innerText()==='입력 확인'&&await page.locator('#plan-body tr').count()===0&&await page.locator('#plan-export').inputValue()==='');
 check('invalid plan cannot copy stale result',await page.locator('[data-copy="plan-export"]').isDisabled());
 await page.fill('#plan-work','9');await page.click('#plan-run');check('minimum budget enforced',await page.locator('#plan-value').innerText()==='입력 확인');
 await page.fill('#plan-work','');await page.click('#plan-run');check('blank budget rejected',await page.locator('#plan-value').innerText()==='입력 확인');
 await page.click('#plan-reset');await page.fill('#plan-start','');await page.click('#plan-run');check('blank date rejected',await page.locator('#plan-value').innerText()==='입력 확인');
 await page.click('#plan-reset');await page.locator('#plan-extreme').focus();await page.keyboard.press('Enter');check('plan extreme keyboard',await page.locator('#plan-focus').inputValue()==='review'&&await page.locator('#plan-used').inputValue()==='no');
 const copy=page.locator('[data-copy="plan-export"]');await copy.focus();await page.keyboard.press('Enter');await page.waitForFunction(()=>document.querySelector('[data-copy-status="plan-export"]').textContent.includes('복사했습니다'));
 check('valid plan copy reenabled',await copy.isEnabled());
 check('clipboard full30days',(await page.evaluate(()=>navigator.clipboard.readText())).includes('30일 2026-11-24'));
 // All prompt copy controls can copy without exposing private data.
 for(const slug of slugs){await page.goto(base+'chapters/'+slug+'.html');for(const button of await page.locator('[data-copy]').all()){await button.click();const id=await button.getAttribute('data-copy');await page.waitForFunction(id=>document.querySelector(`[data-copy-status="${id}"]`).textContent.includes('복사했습니다'),id);check(`${slug} copy ${id}`,true);}}
 // Clipboard denial uses a visible select-and-copy fallback.
 await page.goto(base+'chapters/13-plan.html');await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('blocked'))},configurable:true}));await page.click('[data-copy="plan-export"]');await page.waitForFunction(()=>document.querySelector('[data-copy-status="plan-export"]').textContent.includes('자동 복사'));check('clipboard fallback focused',await page.locator('#plan-export').evaluate(n=>document.activeElement===n&&n.selectionEnd>n.selectionStart));
 // Direct tool embedding for future lab integration.
 for(let i=0;i<slugs.length;i++){await page.goto(base+`chapters/${slugs[i]}.html?embed=${tools[i]}`);check(`${slugs[i]} embed visible`,await page.locator('#'+tools[i]).isVisible());check(`${slugs[i]} embed no overflow`,await overflow());}
 // With JavaScript disabled all chapters, FAQs, source notes and plan remain readable.
 const plain=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:1000}}),nojs=await plain.newPage();watch(nojs);
 for(const slug of slugs){await nojs.goto(base+'chapters/'+slug+'.html');check(`${slug} noJS content`,await nojs.locator('main').innerText().then(t=>t.length>3000));check(`${slug} noJS FAQ5`,await nojs.locator('.chapter-faq details').count()===5);check(`${slug} noJS overflow0`,await nojs.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
 check('noJS full plan',await nojs.locator('#plan-body tr').count()===30);await plain.close();
 const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('storage blocked');}});});const privatePage=await blocked.newPage();watch(privatePage);await privatePage.goto(base+'chapters/13-plan.html');await privatePage.click('#plan-run');check('storage blocked tool works',await privatePage.locator('#plan-body tr').count()===30);await blocked.close();
 // Validate rendered internal links, including dynamically generated navigation and anchors.
 for(const href of links){const url=new URL(href),res=await context.request.get(url.href);check(`link ${url.pathname}${url.search}${url.hash}`,res.ok());if(url.hash){const body=await res.text();const id=decodeURIComponent(url.hash.slice(1));check(`anchor ${id}`,body.includes(`id="${id}"`)||body.includes(`id='${id}'`));}}
 check('console/page/http errors0',errors.length===0);
 await fs.writeFile(out+'/browser-check.json',JSON.stringify({checks:checks.length,passed:checks,errors,links:links.size,widths:[1280,375,360],themes:['light','dark'],scope:slugs},null,2));
 console.log(`${checks.length} checks passed; ${links.size} internal links; console/page/http errors: ${errors.length}`);
} catch(error){await fs.writeFile(out+'/browser-failure.json',JSON.stringify({error:String(error),checks:checks.length,errors},null,2));throw error;}finally{await browser.close();}
