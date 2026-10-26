// 실제 Chromium에서 원본 장·공통 계약·실험실을 함께 검증한다.
import { chromium } from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const base = process.env.SITE_URL || 'http://127.0.0.1:8514/';
const browser = await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context = await browser.newContext({viewport:{width:1280,height:1000}});
const page = await context.newPage();
const errors = [], checks = [];
context.on('page', p => { p.on('pageerror', e => errors.push(String(e))); p.on('console', m => {if(m.type()==='error') errors.push(m.text());}); });
page.on('pageerror',e=>errors.push(String(e))); page.on('console',m=>{if(m.type()==='error') errors.push(m.text());});
const check = (name, value) => {assert.ok(value, name); checks.push(name);};
try {
 await page.goto(base);
 check('표지 실제 장 수', (await page.locator('[data-chapter-count]').textContent())==='16');
 check('표지 실제 도구 수', (await page.locator('[data-sim-count]').textContent())==='29');
 await page.goto(base+'chapters/03-revenue.html');
 await page.locator('#brand').fill('200000'); await page.locator('#cost').fill('30000'); await page.locator('#refund').fill('0');
 await page.goto(base+'chapters/04-niche.html');
 await page.locator('#niche-name').fill('직장인 AI 변경점'); await page.locator('#niche-weekly-hours').fill('7');
 await page.goto(base+'chapters/14-plan.html');
 await page.locator('#plan-minutes').fill('30'); await page.locator('#plan-days').selectOption('5');
 await page.goto(base+'lab.html'); await page.locator('#sim-picker').selectOption('month-scenario');
 check('3·4·14장 입력 이어받기', (await page.locator('#month-scenario').textContent()).includes('직장인 AI 변경점'));
 check('주당 시간 이어받기', (await page.locator('#month-scenario').textContent()).includes('주 7시간'));
 check('장부 원본 결과 이어받기', (await page.locator('[data-month-ledger]').textContent()).includes('170,000원'));
 check('계획 원본 결과 이어받기', (await page.locator('[data-month-plan]').textContent()).includes('30일 중'));
 console.log('integration smoke passed');
 if (process.env.SMOKE_ONLY) process.exitCode=0;
 else {
 const routes = await page.evaluate(()=>ReelsBook.chapters.map(c=>({slug:c.slug,number:c.number,url:ReelsBook.chapterUrl(c)})));
 for (const width of [1280,375]) {
  await page.setViewportSize({width,height:1000});
  for (const route of [{slug:'index',url:base},...routes,{slug:'coming-soon',url:base+'chapters/coming-soon.html'}]) {
   console.log(`${width} ${route.slug}`); await page.goto(new URL(route.url,base).href); await page.waitForTimeout(70);
   check(`${width} ${route.slug} 가로 넘침 없음`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   if(route.number>=1 && route.number<=14) {
    if(route.number>=2) check(`${width} ${route.slug} 9블록`,await page.locator('[data-block]').count()===9);
    const qs=page.locator('[data-question]'); check(`${route.slug} 퀴즈 3~5개`,(await qs.count())>=3 && (await qs.count())<=5);
    await qs.first().locator('[data-correct="false"]').first().focus(); await page.keyboard.press('Enter');
    check(`${route.slug} 오답 해설`,!(await qs.first().locator('[data-feedback]').getAttribute('hidden')));
    await page.locator('[data-quiz-reset]').click();
    for (const q of await qs.all()) {await q.locator('[data-correct="true"]').focus(); await page.keyboard.press('Enter');}
    check(`${route.slug} 전 문항 정답`,(await page.locator('[data-quiz-score]').textContent()).includes(`${await qs.count()}문항 정답`));
    await page.locator('[data-quiz-reset]').click();
   }
   if(route.number && route.number<=14) {
    for(const sim of await page.locator('[role="region"]').all()) {
     const result=sim.locator('[data-sim-result]'); check(`${route.slug} 도구 텍스트 결과`,(await result.textContent()).trim().length>0);
     const buttons=sim.locator('button');
     const input=sim.locator('input:not([type="hidden"]),select,textarea').first();
     if(await input.count()) {await input.focus(); const tag=await input.evaluate(e=>e.tagName); const type=await input.getAttribute('type');
      if(type==='range') {const before=await input.inputValue(); await page.keyboard.press('Home');await page.keyboard.press('ArrowRight');check(`${route.slug} 범위 입력 키보드`,await input.inputValue()!==before || await input.inputValue()!=='0');}
      else if(type==='checkbox') await page.keyboard.press('Space');
      else if(tag==='SELECT') {await page.keyboard.press('ArrowDown'); await page.keyboard.press('Enter');}
      else if(type==='text') {await page.keyboard.type(' 키보드');check(`${route.slug} 텍스트 입력 키보드`,(await input.inputValue()).includes('키보드'));}
      else {await page.keyboard.press('ArrowUp'); await page.keyboard.press('Tab');}
     } else {const before=await result.textContent();await buttons.first().focus();await page.keyboard.press('ArrowRight');check(`${route.slug} 그림 방향키 결과 변경`,(await result.textContent())!==before);await page.keyboard.press('End');await page.keyboard.press('Home');await page.keyboard.press('Enter');}
     check(`${width} ${route.slug} 도구 키보드 결과`,(await result.textContent()).trim().length>0);
    }
    const terms=page.locator('a[data-term]');
    for(const term of await terms.all()) {await term.focus();check(`${width} ${route.slug} 용어 포커스 넘침 없음`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
   }
   if(route.slug==='index') await page.screenshot({path:`docs/results/phase-5d/cover-${width}.png`,fullPage:true});
   if(['glossary','credits'].includes(route.slug)) await page.screenshot({path:`docs/results/phase-5d/${route.slug}-${width}.png`,fullPage:false});
  }
 }
 await page.goto(base+'lab.html');
 const catalog=await page.evaluate(()=>ReelsCatalog);
 for(const sim of catalog.filter(s=>s.chapter!==15)) {
  await page.locator('#sim-picker').selectOption(`${sim.chapter}:${sim.id}`);
  await page.waitForFunction(slug=>document.querySelector('iframe').contentDocument?.body?.dataset.chapter===slug, sim.slug);
  const frame=page.frameLocator('#sim-frame'); await frame.locator('#'+sim.id).waitFor();
  check(`실험실 원본 ${sim.chapter}:${sim.id}`,await frame.locator('#'+sim.id).isVisible());
  check(`실험실 한 도구 ${sim.chapter}:${sim.id}`,await frame.locator('[role="region"]:visible').count()===1);
  const controls=frame.locator('#'+sim.id).locator('button,input,select,textarea'); await controls.first().focus(); await page.keyboard.press('Tab');
  check(`실험실 키보드 ${sim.chapter}:${sim.id}`,await frame.locator('#'+sim.id+' [data-sim-result]').textContent());
  check(`실험실 모바일 넘침 ${sim.chapter}:${sim.id}`,await frame.locator('html').evaluate(e=>e.scrollWidth<=innerWidth));
 }
 await page.locator('#sim-picker').selectOption('month-scenario');
 await page.locator('#sim-picker').focus(); await page.evaluate(()=>{document.activeElement.blur();scrollTo({top:0,behavior:'instant'});});
 await page.screenshot({path:'docs/results/phase-5d/lab-375.png',fullPage:true});
 await page.setViewportSize({width:1280,height:1000}); await page.evaluate(()=>scrollTo({top:0,behavior:'instant'})); await page.screenshot({path:'docs/results/phase-5d/lab-1280.png',fullPage:true});
 await page.goto(base+'glossary.html');
 await page.locator('#term-search').fill('드라이런'); check('용어 검색',await page.locator('[data-glossary-entry]:visible').count()===1);
 await page.locator('#term-category').selectOption('세금');check('용어 검색+분류 교집합',await page.locator('[data-glossary-entry]:visible').count()===0);
 await page.locator('#term-search').fill('');check('세금 분류',await page.locator('[data-glossary-entry]:visible').count()===1);
 check('콘솔·페이지 오류 0',errors.length===0);
 await fs.writeFile('docs/results/phase-5d/browser-check.json',JSON.stringify({base,checks,errors},null,2));
 console.log(`${checks.length} checks passed`);
 }
} finally {await browser.close();}
