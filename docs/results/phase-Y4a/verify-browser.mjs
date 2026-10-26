import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'}),page=await context.newPage();
const checks=[],errors=[],screens=[],links=new Set(),known=[];
const base=process.env.SITE_URL||'http://127.0.0.1:8594/site-shorts/chapters/';
const chapters=['01-map','03-hook','04-script','05-audio'];
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
page.on('pageerror',e=>errors.push({url:page.url(),error:e.message}));
page.on('console',m=>{if(m.type()==='error')errors.push({url:page.url(),error:m.text()});});
page.on('response',r=>{if(r.url().startsWith('http://127.0.0.1:8594')&&r.status()>=400)errors.push({url:r.url(),status:r.status()});});
const overflow=()=>page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth}));
try {
for(const chapter of chapters)for(const width of [1280,375,360])for(const theme of ['light','dark']){
 await page.setViewportSize({width,height:900});
 await page.goto(base+chapter+'.html');
 await page.locator('[data-theme-select]').selectOption(theme);
 await page.evaluate(()=>document.fonts.ready);
 check(`${chapter}/${width}/${theme}: 테마`,await page.locator('html').getAttribute('data-theme')===theme);
 let size=await overflow();check(`${chapter}/${width}/${theme}: 가로 넘침 없음`,size.scroll<=size.viewport);
 check(`${chapter}: 9블록`,await page.locator('[data-block]').count()===9);
 check(`${chapter}: FAQ 5`,await page.locator('.chapter-faq details').count()===5);
 check(`${chapter}: 도구 1`,await page.locator('.lesson-tool').count()===1);
 if(theme==='light'){
  const file=`docs/results/phase-Y4a/${chapter}-${width}.png`;
  await page.screenshot({path:file});screens.push(file);
 }
 for(const summary of await page.locator('.chapter-faq summary').all()){
  await summary.focus();await page.keyboard.press('Space');
  check(`${chapter}/${width}: FAQ 키보드 펼치기`,await summary.evaluate(e=>e.parentElement.open));
 }
 size=await overflow();check(`${chapter}/${width}/${theme}: FAQ 펼친 뒤 넘침 없음`,size.scroll<=size.viewport);
 const firstAxis=page.locator('[data-axis-nav] a').first();await firstAxis.focus();await page.keyboard.press('Enter');
 check(`${chapter}: 축 링크 초점 이동`,await page.evaluate(()=>document.activeElement.id===location.hash.slice(1)));
 const tool=page.locator('.lesson-tool');await tool.scrollIntoViewIfNeeded();
 if(theme==='light'||width===360){
  const file=`docs/results/phase-Y4a/${chapter}-tool-${width}${theme==='dark'?'-dark':''}.png`;
  await tool.screenshot({path:file,style:'.site-header,.skip-link{visibility:hidden !important;} '});screens.push(file);
 }
 const inputs=page.locator('.lesson-tool input[type=range]');
 for(const input of await inputs.all()){
  await input.focus();await page.keyboard.press('Home');check(`${chapter}: range Home`,await input.inputValue()===await input.getAttribute('min'));
  await page.keyboard.press('End');check(`${chapter}: range End`,await input.inputValue()===await input.getAttribute('max'));
 }
 for(const question of await page.locator('[data-question]').all()){
  const correct=question.locator('[data-correct=true]');await correct.focus();await page.keyboard.press('Enter');
  check(`${chapter}: 퀴즈 피드백`,/정답입니다/.test(await question.locator('[data-feedback]').innerText()));
 }
 check(`${chapter}: 3정답`,/3문항 정답/.test(await page.locator('[data-quiz-score]').innerText()));
 await page.locator('[data-quiz-reset]').click();
 check(`${chapter}: 퀴즈 초기화`,/0문항 풀이/.test(await page.locator('[data-quiz-score]').innerText()));
 await page.locator('[data-menu-toggle]').focus();await page.keyboard.press('Enter');await page.keyboard.press('Escape');
 check(`${chapter}: 목차 Escape 초점 복귀`,await page.locator('[data-menu-toggle]').evaluate(e=>e===document.activeElement&&e.getAttribute('aria-expanded')==='false'));
 const local=await page.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>a.href).filter(h=>h.startsWith(location.origin)));
 for(const href of local)links.add(href);
 check(`${chapter}: 앵커 누락 없음`,await page.evaluate(()=>[...document.querySelectorAll('a[href^="#"]')].every(a=>document.getElementById(a.hash.slice(1)))));
 if(width===1280&&theme==='light')known.push({chapter,title:await page.title(),integration:'공통 book.js의 준비중 표시·목차 링크는 통합 diff 적용 전 상태'});
}
for(const link of links){const response=await context.request.get(link);check('내부 링크 '+new URL(link).pathname,response.status()===200);}
// 저장소 접근 차단에도 본문과 장 도구가 작동해야 한다.
const denied=await browser.newContext();await denied.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new Error('storage denied');}}));
const deniedPage=await denied.newPage();deniedPage.on('pageerror',e=>errors.push({mode:'storage-denied',error:e.message}));
for(const chapter of chapters){await deniedPage.goto(base+chapter+'.html');check(chapter+': 저장 차단 본문',await deniedPage.locator('h1').isVisible());}
await denied.close();
// 자바스크립트 없이도 원고·질문 답·직접 계산 설명을 읽을 수 있다.
const fallback=await browser.newContext({javaScriptEnabled:false});const fallbackPage=await fallback.newPage();
for(const chapter of chapters){await fallbackPage.goto(base+chapter+'.html');check(chapter+': JS 없이 원고',await fallbackPage.locator('h1').isVisible());check(chapter+': JS 없이 도구 설명',await fallbackPage.locator('noscript').isVisible());}
await fallback.close();
check('콘솔·페이지·로컬 요청 오류 0',errors.length===0);
const report={checks:checks.length,passed:checks,errors,screens,knownIntegration:known};
await fs.writeFile('docs/results/phase-Y4a/browser-check.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({checks:checks.length,errors,screens:screens.length,links:links.size}));
} finally {await browser.close();}
