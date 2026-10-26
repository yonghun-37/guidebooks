import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const base=process.env.SITE_URL || 'http://127.0.0.1:8514/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
const checks=[],errors=[];
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
try {
 const context=await browser.newContext();const p=await context.newPage();p.on('pageerror',e=>errors.push(String(e)));
 await p.goto(base+'chapters/10-publishing.html?embed=chapter-figure');
 check('10장 개념 그림만 임베드',await p.locator('[data-block]:visible').count()===1 && await p.locator('#chapter-figure').isVisible());
 await p.goto(base+'lab.html');
 await p.evaluate(()=>localStorage.setItem('reelsbook:sim:niche-sim',JSON.stringify({version:1,values:'broken',result:'오염된 결과'})));
 await p.reload();check('손상된 저장 구조 무시',!(await p.locator('[data-month-niche]').textContent()).includes('오염된 결과'));
 await p.locator('[data-clear-month]').click();
 check('초기 예시값 가져오지 않음',(await p.locator('[data-month-ledger]').textContent()).includes('아직 변경한'));
 await p.goto(base+'chapters/03-revenue.html');await p.locator('[data-preset="zero"]').focus();await p.keyboard.press('Enter');
 await p.goto(base+'lab.html');check('0 입력을 미입력과 구분',(await p.locator('[data-month-ledger]').textContent()).includes('현금 수입 0원'));
 await p.goto(base+'chapters/03-revenue.html');await p.locator('#brand').fill('');
 await p.goto(base+'lab.html');check('빈칸 입력은 계산 보류',(await p.locator('[data-month-ledger]').textContent()).includes('계산을 멈췄습니다'));
 await p.evaluate(()=>{localStorage.setItem('reelsbook:theme','dark');localStorage.setItem('reelsbook:checklist:keep','{"done":true}');});
 await p.locator('[data-clear-month]').click();
 check('입력 삭제는 테마·체크 보존',await p.evaluate(()=>localStorage.getItem('reelsbook:theme')==='dark'&&localStorage.getItem('reelsbook:checklist:keep')!==null&&localStorage.getItem('reelsbook:sim:ledger-sim')===null));
 await p.goto(base+'chapters/03-revenue.html');check('삭제 후 예시값 복귀',await p.locator('#brand').inputValue()==='0');
 await p.goto(base+'lab.html');await p.locator('#sim-picker').selectOption('3:ledger-sim');
 const frame=p.frameLocator('#sim-frame');await frame.locator('#ledger-sim').waitFor();await frame.locator('#brand').fill('123456');
 await p.locator('#sim-picker').selectOption('month-scenario');check('실험실 원본 도구 입력 즉시 반영',(await p.locator('[data-month-ledger]').textContent()).includes('123,456원'));
 await p.locator('#sim-picker').selectOption('2:concept-figure');await p.waitForFunction(()=>document.querySelector('iframe').contentDocument?.body?.dataset.chapter==='02-formats');
 await p.locator('#sim-picker').selectOption('4:concept-figure');await p.waitForFunction(()=>document.querySelector('iframe').contentDocument?.body?.dataset.chapter==='04-niche');
 check('같은 도구 ID라도 원본 장 교체',await frame.locator('#niche-sim').isHidden());
 await p.locator('[data-theme-select]').selectOption('light'); await p.locator('#sim-picker').selectOption('3:ledger-sim');await frame.locator('#ledger-sim').waitFor();
 await p.locator('[data-theme-select]').selectOption('dark');await p.waitForTimeout(100);check('부모 테마 변경을 원본 프레임에 반영',await frame.locator('html').getAttribute('data-theme')==='dark');
 for(const width of [1280,375]) {
  await p.setViewportSize({width,height:900});await p.goto(base+'lab.html');await p.locator('[data-theme-select]').selectOption('dark');
  check(`다크 실험실 ${width}`,await p.evaluate(()=>document.documentElement.scrollWidth===innerWidth));
 }
 const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError');}});});
 const bp=await blocked.newPage();bp.on('pageerror',e=>errors.push(String(e)));
 await bp.goto(base+'chapters/03-revenue.html');await bp.locator('#brand').fill('100');
 check('저장 차단에도 계산',(await bp.locator('#ledger-sim [data-sim-result]').textContent()).includes('100원'));
 check('저장 차단 알림',(await bp.locator('[data-input-save-status]').textContent()).includes('저장할 수 없는'));
 await bp.goto(base+'lab.html');check('저장 차단 실험실 폴백',(await bp.locator('[data-month-ledger]').textContent()).includes('아직 변경한'));
 const nojs=await browser.newContext({javaScriptEnabled:false});const np=await nojs.newPage();
 for(const route of ['glossary.html','credits.html','lab.html','chapters/01-map.html','chapters/14-plan.html']){await np.goto(base+route);check(`JS 없이 본문 ${route}`,(await np.locator('main').textContent()).length>500);}
 await p.goto(base);const video=p.locator('video');await video.evaluate(v=>v.play());await p.waitForTimeout(300);check('샘플 영상 재생',await video.evaluate(v=>v.currentTime>0 && v.videoWidth===1080));
 check('페이지 오류 0',errors.length===0);
 await fs.writeFile('docs/results/phase-5d/edge-check.json',JSON.stringify({checks,errors},null,2));console.log(`${checks.length} edge checks passed`);
}finally{await browser.close();}
