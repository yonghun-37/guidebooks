import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='docs/results/phase-Y5', origin='http://127.0.0.1:8615', base=origin+'/site-shorts/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage(),checks=[],errors=[],links=new Set();
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('pageerror',e=>errors.push(String(e)));
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(r.url()+' '+r.status());});
const htmls=(await fs.readdir('site-shorts')).filter(n=>n.endsWith('.html'));
for(const dir of ['chapters','practice'])for(const n of await fs.readdir('site-shorts/'+dir))if(n.endsWith('.html')&&n!=='coming-soon.html')htmls.push(dir+'/'+n);
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
try{
 for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const path of htmls){
  await page.setViewportSize({width,height:1000});await page.goto(base+path);await page.locator('h1').waitFor();
  await page.locator('[data-theme-select]').selectOption(theme);await page.evaluate(()=>document.fonts.ready);
  check(`${path}/${width}/${theme} 넘침0`,await overflow());
  check(`${path}/${width}/${theme} 제목 완성`,!/준비\s*중/.test(await page.title()));
  await page.locator('main details').evaluateAll(ns=>ns.forEach(n=>n.open=true));
  check(`${path}/${width}/${theme} 펼친 뒤 넘침0`,await overflow());
  for(const href of await page.locator('a[href], [data-retry-tool]').evaluateAll(ns=>ns.map(n=>n.href||new URL(n.dataset.retryTool,location.href).href).filter(h=>h.startsWith(location.origin))))links.add(href);
  const menu=page.locator('[data-menu-toggle]');await menu.focus();await page.keyboard.press('Enter');
  check(`${path}/${width}/${theme} 목차 Enter`,await menu.getAttribute('aria-expanded')==='true');
  check(`${path}/${width}/${theme} 목차 넘침0`,await overflow());await page.keyboard.press('Escape');
  check(`${path}/${width}/${theme} 목차 Escape`,await menu.evaluate(n=>n===document.activeElement)&&await menu.getAttribute('aria-expanded')==='false');
  if(theme==='light'&&['index.html','lab.html','glossary.html'].includes(path)){
   await page.locator('main details').evaluateAll(ns=>ns.forEach(n=>n.open=false));await page.evaluate(()=>scrollTo(0,0));
   await page.screenshot({path:`${out}/${path.replace('.html','')}-${width}.png`});
   if(path==='index.html'){await page.locator('#ai-production').screenshot({path:`${out}/cover-ai-${width}.png`});await page.locator('#kit-sample').screenshot({path:`${out}/cover-kit-${width}.png`});}
  }
  if(width===360&&theme==='dark'&&['index.html','lab.html','glossary.html','chapters/02b-ai-tools.html','practice/e2e.html'].includes(path)){
   await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${out}/${path.replaceAll('/','-').replace('.html','')}-360-dark.png`});
  }
 }
 console.log(`화면·목차 ${checks.length} 확인`);
 await page.goto(base+'index.html');
 const book=await page.evaluate(()=>({chapters:window.ShortsBook.chapters,practice:window.ShortsBook.practice,tracks:window.ShortsBook.tracks}));
 check('이론 15장 + 실험실·용어집',book.chapters.length===17);
 check('실습 0~10 + E2E',book.practice.length===12);
 check('목차 모두 완성',book.tracks.flatMap(t=>t.chapters).every(c=>c.status==='완성'));
 check('도구 지도 3장',book.chapters[2].slug==='02b-ai-tools'&&book.chapters[2].number===3);
 check('목차 준비중 링크0',await page.locator('[data-chapter-toc] a[href*="coming-soon"]').count()===0);
 for(let i=0;i<15;i++){
  const c=book.chapters[i];await page.goto(base+`chapters/${c.slug}.html`);
  check(`이론${i+1} 9블록`,await page.locator('[data-block]').count()===9);
  check(`이론${i+1} FAQ5`,await page.locator('.chapter-faq details').count()===5);
  check(`이론${i+1} 표시번호`,await page.title().then(t=>t.includes(`${i+1}장`)));
  const next=book.chapters[i+1];check(`이론${i+1} 다음 slug`,await page.locator('[data-chapter-pager] a').last().getAttribute('href')===(next.number?`../chapters/${next.slug}.html`:`../${next.slug}.html`));
  for(const q of await page.locator('[data-question]').all()){
   await q.locator('[data-correct=true]').focus();await page.keyboard.press('Space');
   check(`이론${i+1} 퀴즈 키보드`,(await q.locator('[data-feedback]').innerText()).includes('정답입니다'));
  }
  await page.locator('[data-quiz-reset]').click();check(`이론${i+1} 초기화`,await page.locator('[data-question] button:disabled').count()===0);
 }
 // 모든 원본 도구를 세 폭에서 실제 로드하고 DOM·높이·테마를 확인한다.
 for(const width of [1280,375,360]){
  await page.setViewportSize({width,height:1000});await page.goto(base+'lab.html');
  const tools=await page.evaluate(()=>window.ShortsCatalog);
  check('31개 원본 도구',tools.length===31&&new Set(tools.map(t=>t.slug)).size===15);
  for(const tool of tools){
   await page.locator('#sim-picker').selectOption(`${tool.slug}:${tool.id}`);
   const frame=page.frameLocator('#sim-frame');await frame.locator(`html.sim-embed #${tool.id}`).waitFor({state:'visible'});
   await page.waitForFunction(()=>{const f=document.querySelector('#sim-frame');return f.clientHeight>=f.contentDocument.body.getBoundingClientRect().height;});
   check(`${width}/${tool.slug}/${tool.id} 임베드 넘침0`,await frame.locator('html').evaluate(n=>n.scrollWidth<=innerWidth));
   check(`${width}/${tool.slug}/${tool.id} 원본 연결`,await page.locator('#sim-original').getAttribute('href')===`chapters/${tool.slug}.html#${tool.id}`);
   const input=frame.locator('input:not([type=hidden]),select,button').filter({visible:true}).first();
   if(await input.count()){await input.focus();check(`${width}/${tool.slug}/${tool.id} 초점`,await input.evaluate(n=>n===document.activeElement));}
   const range=frame.locator('input[type=range]').filter({visible:true}).first();
   if(await range.count()){await range.focus();await page.keyboard.press('Home');await page.keyboard.press('End');check(`${width}/${tool.slug}/${tool.id} 슬라이더 키보드`,await range.evaluate(n=>Number(n.value)===Number(n.max)));}
   await page.locator('[data-theme-select]').selectOption('dark');
   await page.waitForFunction(()=>document.querySelector('#sim-frame').contentDocument.documentElement.dataset.theme==='dark');
   check(`${width}/${tool.slug}/${tool.id} 다크 전달`,true);
   if(['rhythm-tool','audio-tool','simulator'].includes(tool.id)&&width!==375)await page.locator('.lab-stage').screenshot({path:`${out}/lab-${tool.slug}-${tool.id}-${width}.png`});
  }
 }
 // 숨긴 다른 절로 이어지는 원본 링크는 전체 장을 열어야 한다.
 await page.goto(base+'lab.html?tool=02b-ai-tools:simulator');
 const recipeFrame=page.frameLocator('#sim-frame');await recipeFrame.locator('#ai-route').selectOption('faceless');
 const recipeLink=recipeFrame.locator('#ai-route-link');
 await recipeLink.click();await page.waitForURL('**/chapters/02b-ai-tools.html#route-faceless');
 check('임베드에서 연 레시피 본문 표시',await page.locator('#route-faceless').isVisible());
 console.log(`원본 도구·이동 ${checks.length} 확인`);
 // 용어 검색과 직접 앵커 이동.
 await page.goto(base+'glossary.html');check('용어48',await page.locator('[data-glossary-entry]').count()===48);
 await page.locator('#term-search').fill('없는용어xyz');check('용어0결과',(await page.locator('#term-count').innerText()).startsWith('0/'));
 await page.locator('#term-search').fill('토큰');check('두 뜻의 토큰 검색',await page.locator('[data-glossary-entry]:visible').count()>=2);
 await page.goto(base+'glossary.html#tts');check('직접 용어 앵커',await page.locator('#tts').isVisible());
 // 실제 인용 번호의 집합·역링크.
 const cited=new Set();for(const path of htmls.filter(p=>p!=='credits.html')){
  const source=await fs.readFile('site-shorts/'+path,'utf8');for(const m of source.matchAll(/href="#source-(y\d{3})"/g))cited.add(m[1]);
 }
 await page.goto(base+'credits.html');const creditIds=await page.locator('.source-entry').evaluateAll(ns=>ns.map(n=>n.id.replace('source-','')));
 check('출처 실제 인용 집합 일치',creditIds.length===cited.size&&creditIds.every(id=>cited.has(id)));
 // 프롬프트 복사와 OS 탭 키보드.
 await page.goto(base+'prompts.html');const box=page.locator('.code-box').first();await box.locator('.copy-button').focus();await page.keyboard.press('Enter');
 await page.waitForFunction(()=>document.querySelector('.copy-status').textContent==='복사했습니다.');check('프롬프트 실제 복사',await page.evaluate(()=>navigator.clipboard.readText()).then(t=>t.length>20));
 await page.goto(base+'practice/07-export.html');const tabs=page.locator('[data-os-tabs]').first();await tabs.locator('[data-os-tab]').first().focus();await page.keyboard.press('End');check('OS 탭 End',await tabs.locator('[data-os-tab]').last().getAttribute('aria-selected')==='true');
 // 체크·주소 공유와 복원.
 await page.goto(base+'practice/e2e.html');const first=page.locator('[data-practice-check]').first(),key=await first.getAttribute('data-practice-check');await first.check();
 await page.locator('[data-practice-field]').fill('https://www.youtube.com/shorts/example-y5');await page.reload();check('진행 복원',await page.locator(`[data-practice-check="${key}"]`).isChecked());
 check('주소 복원',(await page.locator('[data-practice-field]').inputValue()).endsWith('example-y5'));await page.locator('[data-practice-reset]').click();check('진행 삭제',await page.locator('[data-practice-check]:checked').count()===0);
 console.log(`용어·출처·저장 ${checks.length} 확인`);
 // 표지의 실제 샘플 재생·타임라인 키보드.
 await page.goto(base+'index.html');await page.locator('video').scrollIntoViewIfNeeded();await page.locator('video').evaluate(v=>{v.muted=true;return v.play();});await page.waitForFunction(()=>document.querySelector('video').currentTime>0.1);check('표지 MP4 재생',true);await page.locator('video').evaluate(v=>v.pause());
 await page.goto(base+'assets/samples/preview.html');await page.locator('video').scrollIntoViewIfNeeded();await page.locator('video').evaluate(v=>{v.muted=true;return v.play();});await page.waitForFunction(()=>document.querySelector('video').currentTime>0.1);check('키트 미리보기 재생',true);console.log(`샘플 재생 ${checks.length} 확인`);
 // 저장 차단 환경도 읽기·목차·체크를 유지한다.
 const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked');}});});
 const bp=await blocked.newPage();await bp.goto(base+'practice/e2e.html');await bp.locator('[data-practice-check]').first().check();check('저장 차단 체크',await bp.locator('[data-practice-check]').first().isChecked());check('저장 차단 안내',(await bp.locator('[data-practice-status]').innerText()).includes('저장할 수 없습니다'));await blocked.close();
 const nojs=await browser.newContext({javaScriptEnabled:false});const np=await nojs.newPage();await np.goto(base+'index.html');check('JS 없는 전체 목차',await np.locator('noscript a').count()>=28);await np.goto(base+'chapters/06-scenes.html');check('JS 없는 정적7장',await np.locator('[data-chapter-kicker]').innerText().then(t=>t.endsWith('/ 7')));await np.goto(base+'lab.html');check('JS 없는 원본31 링크',await np.locator('main ol a').count()===31);await nojs.close();
 console.log(`저장 차단·JS 없는 읽기 ${checks.length} 확인`);
 // 생성된 링크·앵커는 브라우저와 별개로 실서버 응답에서 확인한다.
 for(const href of links){const u=new URL(href);const response=await context.request.get(u.origin+u.pathname);check(`내부 링크 ${u.pathname}${u.hash}`,response.ok());if(u.hash&&u.pathname.endsWith('.html')){const body=await response.text();const id=decodeURIComponent(u.hash.slice(1));check(`앵커 ${u.pathname}${u.hash}`,body.includes(`id="${id}"`)||body.includes(`id='${id}'`));}}
 check('콘솔·페이지·내부HTTP 오류0',errors.length===0);
 await fs.writeFile(`${out}/browser-check.json`,JSON.stringify({passed:checks.length,pages:htmls.length,widths:[1280,375,360],themes:['light','dark'],internalLinks:links.size,errors,checks},null,2));
 await fs.rm(`${out}/browser-failure.json`,{force:true});
 console.log(JSON.stringify({passed:checks.length,pages:htmls.length,internalLinks:links.size,errors}));
}catch(error){await fs.writeFile(`${out}/browser-failure.json`,JSON.stringify({error:String(error),url:page.url(),checks:checks.length,errors},null,2));throw error;}
finally{await browser.close();}
