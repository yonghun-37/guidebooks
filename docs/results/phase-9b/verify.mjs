// 재현: 저장소 루트에서 python3 -m http.server 8542 --bind 127.0.0.1
// 이후 node docs/results/phase-9b/verify.mjs
import { chromium } from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const base=process.env.SITE_URL || 'http://127.0.0.1:8542/';
const output='docs/results/phase-9b/';
const chapters=['05-sources','06-writing','07-cards','08-reels','09-pipeline'];
const sims=['rights-sim','ch6-sim','ch7-sim','ch8-sim','ch9-sim'];
const expected=['3개','3개','29줄','42.7자/초','90,000원'];
const basic=['0개','0개','4줄','6.0자/초','6,000원'];
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage();
const errors=[],checks=[],links=new Set();
page.on('pageerror',error=>errors.push(String(error)));
page.on('console',message=>{if(message.type()==='error')errors.push(message.text());});
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
try {
 for(const width of [1280,375,360]) {
  await page.setViewportSize({width,height:1000});
  for(let i=0;i<chapters.length;i++) {
   const slug=chapters[i];
   await page.goto(base+'site/chapters/'+slug+'.html',{waitUntil:'networkidle'});
   check(`${width} ${slug} 가로 넘침 없음`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   check(`${width} ${slug} 9블록`,await page.locator('[data-block]').count()===9);
   check(`${width} ${slug} 도구 하나`,await page.locator('.simulator').count()===1);
   check(`${width} ${slug} 축 고정 6줄`,await page.locator('.axis-rows').evaluateAll(rows=>rows.every(row=>row.children.length===6)));
   check(`${width} ${slug} FAQ 5개`,await page.locator('.chapter-faq details').count()===5);
   check(`${width} ${slug} 정리 3줄`,await page.locator('.key-takeaways li').count()===3);
   check(`${width} ${slug} 목차 FAQ`,(await page.locator('[data-mobile-outline]').textContent()).includes('자주 묻는 질문'));
   check(`${width} ${slug} 기본 계산`,(await page.locator('[data-sim-result]').textContent()).startsWith(basic[i]));
   await page.locator('[data-preset=extreme]').click();
   check(`${width} ${slug} 극단 계산`,(await page.locator('[data-sim-result]').textContent()).startsWith(expected[i]));
   check(`${width} ${slug} 극단 결과 한 숫자 한 문장`,await page.locator('[data-sim-result]').evaluate(node=>/^\d[\d,.]*[^0-9]* · [^0-9]+[.]$/.test(node.textContent)));
   check(`${width} ${slug} 극단 가로 넘침 없음`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   await page.locator('[data-preset=default]').click();
   check(`${width} ${slug} 기본 복원`,(await page.locator('[data-sim-result]').textContent()).startsWith(basic[i]));
   const firstInput=page.locator('.simulator input').first();await firstInput.focus();
   await page.keyboard.press(i<2?'Space':'ArrowRight');
   check(`${width} ${slug} 키보드 입력 갱신`,!(await page.locator('[data-sim-result]').textContent()).startsWith(basic[i]) || i===2);
   if(i>=2)check(`${width} ${slug} 입력값 표시`,await firstInput.evaluate(input=>input.value===document.querySelector(`output[for="${input.id}"]`).value));
   await page.locator('[data-preset=default]').click();
   await page.locator('.axis-card').first().focus();await page.keyboard.press('Enter');
   check(`${width} ${slug} 축 링크 키보드 초점`,await page.evaluate(()=>document.activeElement.id===location.hash.slice(1)));
   await page.locator('#faq-1 summary').focus();await page.keyboard.press('Enter');
   check(`${width} ${slug} FAQ 키보드 펼침`,await page.locator('#faq-1').getAttribute('open')!==null);
   for(let q=0;q<3;q++) {
    const question=page.locator('[data-question]').nth(q);
    await question.locator('[data-correct=false]').click();
    check(`${width} ${slug} 퀴즈 ${q+1} 오답 해설`,await question.locator('[data-feedback]').isVisible());
    await page.locator('[data-quiz-reset]').click();
   }
   for(const question of await page.locator('[data-question]').all()) await question.locator('[data-correct=true]').click();
   check(`${width} ${slug} 퀴즈 3문항 정답`,(await page.locator('[data-quiz-score]').textContent()).includes('3문항 정답'));
   await page.locator('[data-quiz-reset]').click();
   check(`${width} ${slug} 퀴즈 초기화`,(await page.locator('[data-quiz-score]').textContent()).includes('0문항 풀이'));
   const hrefs=await page.locator('a[href],script[src],link[href],img[src]').evaluateAll(nodes=>nodes.map(node=>node.href || node.src));
   hrefs.forEach(href=>{if(href.startsWith(base))links.add(href);});
   if(width!==360) {
    await page.evaluate(()=>scrollTo({top:document.querySelector('#question').offsetTop-90,behavior:'instant'}));
    await page.screenshot({path:output+slug+'-'+width+'.png'});
   }
   await page.goto(base+'site/chapters/'+slug+'.html#faq-5');
   check(`${width} ${slug} FAQ 직접 링크`,await page.locator('#faq-5').getAttribute('open')!==null);
   const previousOpen=await page.locator('.chapter-faq details[open]').count();
   await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));
   check(`${width} ${slug} 인쇄 FAQ 전부 펼침`,await page.locator('.chapter-faq details[open]').count()===5);
   await page.evaluate(()=>dispatchEvent(new Event('afterprint')));
   check(`${width} ${slug} 인쇄 뒤 복원`,await page.locator('.chapter-faq details[open]').count()===previousOpen);
  }
 }
 // 생성된 내비를 포함한 담당 페이지의 로컬 링크·자산·앵커 대조.
 const cache=new Map();
 for(const href of links) {
  const url=new URL(href);const fragment=decodeURIComponent(url.hash.slice(1));url.hash='';
  if(!cache.has(url.href)){const response=await context.request.get(url.href);check(`링크 ${url.pathname} HTTP 성공`,response.ok());cache.set(url.href,{type:response.headers()['content-type']||'',text:await response.text()});}
  const result=cache.get(url.href);
  if(fragment&&result.type.includes('text/html'))check(`앵커 ${new URL(href).pathname}#${fragment}`,new RegExp(`\\bid=["']${fragment.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}["']`).test(result.text));
 }
 // 기존 실험실 iframe 주소 10개가 모두 열린다.
 for(let i=0;i<chapters.length;i++)for(const id of [i===0?'concept-figure':`ch${i+5}-flow`,sims[i]]) {
  await page.goto(base+`site/chapters/${chapters[i]}.html?embed=${id}`);
  check(`실험실 ${id} embed`,await page.locator('html').evaluate(node=>node.classList.contains('sim-embed')));
  check(`실험실 ${id} 표시`,await page.locator('#'+id).isVisible());
 }
 await page.goto(base+'site/chapters/08-reels.html#principle');
 await page.locator('[data-theme-select]').selectOption('dark');
 check('360px 다크 모드',await page.evaluate(()=>document.documentElement.dataset.theme==='dark'&&document.documentElement.scrollWidth<=innerWidth));
 await page.locator('#audio-rights').scrollIntoViewIfNeeded();
 await page.screenshot({path:output+'08-reels-dark-360.png'});
 await page.goto(base+'site/chapters/09-pipeline.html#simulator');
 await page.locator('[data-theme-select]').selectOption('light');
 await page.locator('#simulator').scrollIntoViewIfNeeded();
 await page.screenshot({path:output+'09-cost-360.png'});
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:375,height:900}});
 await nojs.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({contentType:'text/css',body:''}));
 const plain=await nojs.newPage();
 for(const slug of chapters) {
  await plain.goto(base+'site/chapters/'+slug+'.html');
  await plain.locator('.axis-card').first().click();check(`${slug} JS 없이 축 이동`,new URL(plain.url()).hash.length>1);
  await plain.locator('#faq-1 summary').click();check(`${slug} JS 없이 FAQ`,await plain.locator('#faq-1').getAttribute('open')!==null);
  await plain.emulateMedia({media:'print'});check(`${slug} JS 없이 인쇄 FAQ`,await plain.locator('#faq-5 .faq-answer').isVisible());await plain.emulateMedia({media:'screen'});
 }
 await nojs.close();check('콘솔·페이지 오류 없음',errors.length===0);
 await fs.writeFile(output+'browser-check.json',JSON.stringify({chapters,widths:[1280,375,360],checks:checks.length,local_links:links.size,errors,passed:checks},null,2)+'\n');
 console.log(JSON.stringify({checks:checks.length,links:links.size,errors}));
} finally {await browser.close();}
