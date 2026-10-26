// 저장소 루트의 HTTP 서버를 8543에서 제공한 뒤 node docs/results/phase-9c/verify.mjs
import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base=process.env.SITE_URL || 'http://127.0.0.1:8543/';
const out='docs/results/phase-9c/';
const files=['10-publishing','11-analytics','12-safety','13-roadmap','14-plan'];
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage();
const errors=[],checks=[],links=new Set();
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('pageerror',e=>errors.push(String(e)));
const check=(name,yes)=>{assert.ok(yes,name);checks.push(name);};
async function fits(name){check(name,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
async function value(id,v){await page.locator(id).fill(v);}
try{
 for(const width of [1280,375,360]){
  await page.setViewportSize({width,height:1000});
  for(const file of files){
   await page.goto(base+'site/chapters/'+file+'.html',{waitUntil:'networkidle'});
   await fits(`${file} ${width} 가로 넘침 없음`);
   check(`${file} ${width} 9블록`,await page.locator('[data-block]').count()===9);
   check(`${file} ${width} FAQ 5개`,await page.locator('.chapter-faq details').count()===5);
   check(`${file} ${width} 축 고정 6줄`,await page.locator('.axis-rows').evaluateAll(rows=>rows.every(row=>row.children.length===6)));
   check(`${file} ${width} 핵심정리 3개`,await page.locator('.key-takeaways>li').count()===3);
   check(`${file} ${width} 본문 금지어 없음`,!await page.locator('main').evaluate(main=>{
    const clone=main.cloneNode(true);clone.querySelectorAll('.source-notes,nav,noscript').forEach(n=>n.remove());return /장부|현금\s*잔액|지급자|적격|Hermes|Phase|원응답/.test(clone.textContent);
   }));
   const all=await page.locator('a[href]').evaluateAll(as=>as.map(a=>a.href));all.forEach(x=>{if(x.startsWith(locationBase()))links.add(x);});
   function locationBase(){return base;}
   await page.locator('.axis-card').first().focus();await page.keyboard.press('Enter');
   check(`${file} ${width} 축 키보드 초점`,await page.evaluate(()=>document.activeElement.id===location.hash.slice(1)));
   for(let i=1;i<=5;i++){
    const summary=page.locator(`#faq-${i} summary`);await summary.focus();await page.keyboard.press('Enter');
    check(`${file} ${width} FAQ ${i} 열림`,await page.locator(`#faq-${i}`).getAttribute('open')!==null);
   }
   await fits(`${file} ${width} FAQ 펼친 뒤 넘침 없음`);
   const questions=page.locator('[data-question]');
   for(let i=0;i<await questions.count();i++){
    const q=questions.nth(i);await q.locator('[data-correct=false]').click();
    check(`${file} ${width} 퀴즈 ${i+1} 오답 피드백`,await q.locator('[data-feedback]').isVisible()&& (await q.locator('[data-feedback]').textContent()).length>0);
   }
   await page.locator('[data-quiz-reset]').click();
   for(let i=0;i<await questions.count();i++)await questions.nth(i).locator('[data-correct=true]').click();
   check(`${file} ${width} 퀴즈 모두 정답`,(await page.locator('[data-quiz-score]').textContent()).includes(`${await questions.count()}문항 정답`));
   await page.locator('[data-quiz-reset]').click();
   if(['11-analytics','13-roadmap','14-plan'].includes(file)){
    const tool=page.locator('.simulator');const result=tool.locator('[data-sim-result]');
    await tool.locator('[data-preset=normal]').click();
    check(`${file} ${width} 기본 계산`,(await result.textContent()).startsWith({'11-analytics':'5%','13-roadmap':'4건','14-plan':'440분'}[file]));
    await tool.locator('[data-preset=break]').focus();await page.keyboard.press('Enter');
    check(`${file} ${width} 극단값`,(await result.textContent()).startsWith(file==='14-plan'?'0분':'—'));
    await tool.locator('[data-preset=normal]').click();
    const input=tool.locator('input[type=number]').first();await input.fill('');
    check(`${file} ${width} 빈칸을 0으로 계산하지 않음`,(await result.textContent()).startsWith('—'));
    await tool.locator('[data-preset=normal]').click();await input.fill('-1');
    check(`${file} ${width} 음수 거부`,(await result.textContent()).startsWith('—'));
    await tool.locator('[data-preset=normal]').click();await input.focus();await page.keyboard.press('ArrowUp');
    check(`${file} ${width} 방향키 계산 갱신`,!(await result.textContent()).startsWith({'11-analytics':'5%','13-roadmap':'4건','14-plan':'440분'}[file]));
    await tool.locator('[data-preset=normal]').click();
   }else check(`${file} ${width} 불필요 도구 분리`,await page.locator('.simulator').count()===0);
   await page.evaluate(()=>{document.querySelectorAll('.chapter-faq details').forEach(n=>n.open=false);window.scrollTo({top:0,behavior:'instant'});});
   if(width!==360)await page.screenshot({path:out+file+'-'+width+'.png'});
  }
 }
 // 일반 계산과 분모가 0인 조건을 따로 검증한다.
 await page.goto(base+'site/chapters/11-analytics.html');
 await value('#metric-a-saved','0');await value('#metric-a-shares','0');
 check('저장·공유 실측 0은 0% 허용',(await page.locator('[data-sim-result]').textContent()).startsWith('0%'));
 await value('#metric-a-reach','1');await value('#metric-a-saved','2');
 check('행동 횟수 비율 100% 초과 허용',(await page.locator('[data-sim-result]').textContent()).startsWith('200%'));
 await page.goto(base+'site/chapters/13-roadmap.html');await value('#goal-price','90000');
 check('거래 수 올림 계산',(await page.locator('[data-sim-result]').textContent()).startsWith('5건'));
 await value('#goal-price','0');check('가격 0 나눗셈 차단',(await page.locator('[data-sim-result]').textContent()).startsWith('—'));
 await page.goto(base+'site/chapters/14-plan.html');
 await page.locator('[data-preset=normal]').click();await page.locator('#plan-days').selectOption('0');
 check('활동일 0은 시간 0',(await page.locator('[data-sim-result]').textContent()).startsWith('0분'));
 await page.locator('#plan-days').selectOption('7');await value('#plan-minutes','30');
 check('30일 전부 활동하면 제작 600분',(await page.locator('[data-sim-result]').textContent()).startsWith('600분'));
 await value('#plan-minutes','5');check('점검 시간보다 짧으면 제작 0',(await page.locator('[data-sim-result]').textContent()).startsWith('0분'));
 await page.locator('[data-preset=normal]').click();await value('#plan-minutes','60');
 await page.reload();check('14장 입력 저장·복원',(await page.locator('#plan-minutes').inputValue())==='60'&&(await page.locator('[data-sim-result]').textContent()).startsWith('1,100분'));
 await page.goto(base+'site/lab.html');await page.locator('[data-refresh-month]').click();
 check('실험실에 14장 새 시간 요약 전달',(await page.locator('[data-month-plan]').textContent()).includes('1,100분'));
 // 옛 실험실 URL에서도 빈 화면이나 오류 없이 대응 절을 연다.
 for(const [file,id] of [['10-publishing','publishing-sim'],['11-analytics','analytics-sim'],['12-safety','safety-sim'],['13-roadmap','roadmap-sim'],['14-plan','planner-sim']]){
  await page.goto(base+`site/chapters/${file}.html?embed=${id}`);
  check(`${file} 기존 실험실 embed 절 표시`,await page.locator('.chapter-block:visible').count()===1);
 }
 await page.goto(base+'site/chapters/13-roadmap.html#faq-2');
 check('FAQ 직접 앵커 열기',await page.locator('#faq-2').getAttribute('open')!==null);
 await page.locator('[data-theme-select]').selectOption('dark');await page.locator('#stages').scrollIntoViewIfNeeded();
 await fits('360 다크 단계표 넘침 없음');await page.screenshot({path:out+'13-stages-dark-360.png'});
 await page.locator('[data-theme-select]').selectOption('light');await page.locator('#stages').scrollIntoViewIfNeeded();
 await page.screenshot({path:out+'13-stages-360.png'});
 await page.locator('#story').scrollIntoViewIfNeeded();await page.screenshot({path:out+'13-faq-360.png'});
 for(const file of files){
  await page.goto(base+'site/chapters/'+file+'.html');await page.emulateMedia({media:'print'});
  await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));
  check(`${file} 인쇄 FAQ 전부 열기`,await page.locator('.chapter-faq details[open]').count()===5);
  await page.evaluate(()=>dispatchEvent(new Event('afterprint')));await page.emulateMedia({media:'screen'});
 }
 for(const href of links){
  const url=new URL(href);url.hash='';const response=await page.request.get(url.href);
  check('내부 요청 '+url.pathname,response.ok());
  if(new URL(href).hash){
   const parsed=new URL(href);
   const exists=await page.evaluate(async ({url,id})=>{
    const html=await (await fetch(url)).text();const doc=new DOMParser().parseFromString(html,'text/html');return !!doc.getElementById(decodeURIComponent(id));
   },{url:url.href,id:parsed.hash.slice(1)});
   // book-menu is generated by the shared navigation script.
   check('내부 앵커 '+parsed.pathname+parsed.hash,exists||parsed.hash==='#book-menu');
  }
 }
 const nojs=await browser.newContext({javaScriptEnabled:false});
 await nojs.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({contentType:'text/css',body:''}));
 const plain=await nojs.newPage();await plain.setViewportSize({width:375,height:900});
 await plain.goto(base+'site/chapters/13-roadmap.html');await plain.locator('.axis-card').first().click();
 check('JS 없이 축 이동',plain.url().endsWith('#payers'));await plain.locator('#faq-1 summary').click();
 check('JS 없이 FAQ 열기',await plain.locator('#faq-1').getAttribute('open')!==null);await nojs.close();
 check('콘솔·페이지 오류 0',errors.length===0);
 await fs.writeFile(out+'browser-check.json',JSON.stringify({pages:5,widths:[1280,375,360],checks:checks.length,errors,passed:checks},null,2)+'\n');
 console.log(JSON.stringify({checks:checks.length,errors}));
}finally{await browser.close();}
