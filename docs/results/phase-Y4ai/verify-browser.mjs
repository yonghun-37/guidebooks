import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage();
const origin='http://127.0.0.1:8597',base=origin+'/site-shorts/',checks=[],errors=[],links=new Set();
const paths=['chapters/02b-ai-tools','chapters/04-script','chapters/05-audio','chapters/06-scenes','chapters/07-editing','chapters/08-captions','prompts','ai-models'];
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('pageerror',e=>errors.push(String(e)));
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(r.url()+' '+r.status());});
try {
 for(const width of [1280,375,360]) for(const theme of ['light','dark']) for(const path of paths){
  await page.setViewportSize({width,height:1000});await page.goto(base+path+'.html');await page.locator('h1').waitFor();
  await page.locator('[data-theme-select]').selectOption(theme);await page.evaluate(()=>document.fonts.ready);
  check(`${path}/${width}/${theme} 가로 넘침 0`,await overflow());
  check(`${path}/${width}/${theme} 본문 제목`,Boolean(await page.locator('h1').innerText()));
  for(const href of await page.locator('main a[href]').evaluateAll(nodes=>nodes.map(n=>n.href).filter(h=>h.startsWith(location.origin))))links.add(href);
  await page.locator('main details').evaluateAll(nodes=>nodes.forEach(n=>n.open=true));
  check(`${path}/${width}/${theme} 펼친 뒤 넘침 0`,await overflow());
  for(const img of await page.locator('main img').all()){
   await img.scrollIntoViewIfNeeded();await img.evaluate(n=>n.decode());check(`${path} 이미지 로드`,await img.evaluate(n=>n.complete&&n.naturalWidth>0));
   check(`${path} 9:16 이미지`,await img.evaluate(n=>n.naturalWidth*16===n.naturalHeight*9));
  }
  const region=page.locator('.ai-table').first();
  if(await region.count()){
   await region.focus();const before=await region.evaluate(n=>n.scrollLeft);await page.keyboard.press('ArrowRight');await page.waitForTimeout(80);
   check(`${path}/${width}/${theme} 표 키보드`,await region.evaluate((n,b)=>n.scrollWidth<=n.clientWidth||n.scrollLeft>b,before));
  }
  await page.evaluate(()=>window.scrollTo(0,0));
  if(theme==='light'&&['chapters/02b-ai-tools','chapters/04-script','chapters/06-scenes','prompts','ai-models'].includes(path))
   await page.screenshot({path:`docs/results/phase-Y4ai/${path.split('/').pop()}-${width}.png`});
 }
 // New path selector is operable using native keyboard selection.
 await page.goto(base+'chapters/02b-ai-tools.html');await page.locator('#ai-route').focus();await page.keyboard.press('End');
 check('경로 선택 키보드',await page.locator('#ai-route').inputValue()==='generate');
 check('생성 경로 비용 결과',await page.locator('#ai-route-result').innerText().then(t=>t.includes('80크레딧')));
 check('생성 레시피 링크',await page.locator('#ai-route-link').getAttribute('href')==='#route-generate');
 await page.locator('#ai-route-link').focus();await page.keyboard.press('Enter');check('경로 앵커 Enter',page.url().endsWith('#route-generate'));
 // New theory block structure and quiz.
 check('도구 지도 9블록',await page.locator('[data-block]').count()===9);
 check('도구 지도 FAQ5',await page.locator('.chapter-faq details').count()===5);
 for(const q of await page.locator('[data-question]').all()){await q.locator('[data-correct=true]').focus();await page.keyboard.press('Space');check('지도 퀴즈 키보드',await q.locator('[data-feedback]').innerText().then(t=>t.includes('정답입니다')));}
 await page.locator('[data-quiz-reset]').click();check('지도 퀴즈 초기화',await page.locator('[data-question] button:disabled').count()===0);
 // Copy every prompt: exact text and keyboard activation; test fallback too.
 await page.goto(base+'prompts.html');const boxes=await page.locator('.code-box').all();
 for(const box of boxes){const expected=await box.locator('code').innerText();await box.locator('.copy-button').focus();await page.keyboard.press('Enter');
  await page.waitForFunction(n=>n.textContent==='복사했습니다.',await box.locator('[role=status]').elementHandle());
  check('프롬프트 복사 상태',await box.locator('[role=status]').innerText()==='복사했습니다.');
  check('프롬프트 정확한 복사',await page.evaluate(()=>navigator.clipboard.readText())===expected);
 }
 await page.evaluate(()=>{navigator.clipboard.writeText=async()=>{throw new Error('blocked');};});
 await page.locator('.copy-button').first().click();check('복사 거부 시 대체 선택',await page.locator('.copy-status').first().innerText().then(t=>t.includes('직접 복사')));
 // Model search includes versioned text and supports empty results / reset.
 await page.goto(base+'ai-models.html');check('모델 271개',await page.locator('[data-ai-model]').count()===271);
 await page.locator('#ai-model-query').fill('Veo');check('Veo 검색',await page.locator('#ai-model-count').innerText().then(t=>!t.startsWith('0개')));
 check('검색 결과 전부 일치',await page.locator('[data-ai-model]:not([hidden])').evaluateAll(nodes=>nodes.every(n=>n.textContent.toLowerCase().includes('veo'))));
 await page.locator('#ai-model-query').fill('no_matching_model_xyz');check('검색 결과 없음',await page.locator('#ai-model-count').innerText().then(t=>t.startsWith('0개')));
 await page.locator('#ai-model-reset').focus();await page.keyboard.press('Enter');check('검색 초기화 키보드',await page.locator('[data-ai-model]:not([hidden])').count()===271);check('검색 초기화 초점',await page.locator('#ai-model-query').evaluate(n=>n===document.activeElement));
 await page.locator('.ai-model-group summary').first().focus();await page.keyboard.press('Space');check('분류 펼치기 키보드',await page.locator('.ai-model-group').first().getAttribute('open')!==null);
 // Existing tools retain behavior and keyboard access.
 await page.goto(base+'chapters/04-script.html');await page.locator('#script-empty').focus();await page.keyboard.press('Enter');check('기존 대본 빈 입력',await page.locator('#script-result').innerText().then(t=>t.includes('0.0초')));await page.locator('#script-reset').click();check('기존 대본 복구',await page.locator('#script-text').inputValue().then(t=>t.length>0));
 await page.goto(base+'chapters/05-audio.html');await page.locator('#voice-mute').focus();await page.keyboard.press('Space');check('기존 소리 뮤트',await page.locator('#voice-mute').getAttribute('aria-pressed')==='true');await page.locator('#audio-reset').click();check('기존 소리 복구',await page.locator('#voice-mute').getAttribute('aria-pressed')==='false');
 await page.goto(base+'chapters/06-scenes.html');await page.locator('#subject-x').focus();await page.keyboard.press('End');check('기존 구도 방향키',await page.locator('#subject-x').inputValue()==='85');await page.locator('[data-scene-preset=base]').click();check('기존 구도 복구',await page.locator('#subject-x').inputValue()==='50');
 await page.goto(base+'chapters/07-editing.html');await page.locator('[data-edit-frame="1"]').focus();await page.keyboard.press('Enter');check('기존 편집 한 프레임',Number(await page.locator('#edit-seek').inputValue())>0);await page.locator('[data-edit-home]').click();check('기존 편집 처음으로',Number(await page.locator('#edit-seek').inputValue())===0);
 await page.goto(base+'chapters/08-captions.html');await page.locator('[data-caption-preset=fast]').focus();await page.keyboard.press('Space');check('기존 자막 극단값',Number(await page.locator('#caption-duration').inputValue())<3);await page.locator('[data-caption-preset=base]').click();check('기존 자막 복구',Number(await page.locator('#caption-duration').inputValue())===3);
 for(const path of paths){await page.goto(base+path+'.html');await page.locator('.skip-link').focus();await page.keyboard.press('Enter');check(`${path} 본문 건너뛰기`,page.url().endsWith('#main'));}
 // Local authored file+anchor links, including staged practice pages.
 const inspector=await context.newPage();for(const href of links){const r=await inspector.goto(href);check('링크 '+href.replace(origin,''),r ? r.ok() : inspector.url()===href);const hash=new URL(href).hash;if(hash)check('앵커 '+hash,await inspector.evaluate(h=>Boolean(document.getElementById(decodeURIComponent(h.slice(1)))),hash));}await inspector.close();
 // Representative content screenshots, not service UI captures.
 for(const width of [1280,375,360]){
  await page.setViewportSize({width,height:1000});await page.goto(base+'chapters/06-scenes.html');await page.locator('[data-theme-select]').selectOption('light');await page.locator('.ai-gallery').scrollIntoViewIfNeeded();
  await page.screenshot({path:`docs/results/phase-Y4ai/ai-examples-${width}.png`});
  await page.goto(base+'chapters/02b-ai-tools.html#route-shoot');await page.screenshot({path:`docs/results/phase-Y4ai/recipe-${width}.png`});
 }
 check('콘솔·페이지·내부 HTTP 오류 0',errors.length===0);
 await fs.writeFile('docs/results/phase-Y4ai/browser-check.json',JSON.stringify({scope:'Linux Chromium; 8 authored/changed pages; 1280/375/360; light/dark; real pinned CDN font; no service account UI',passed:checks.length,checks,errors,internalLinks:links.size},null,2));
 console.log(`${checks.length} checks passed; ${links.size} links; errors ${errors.length}`);
} catch(e){await fs.writeFile('docs/results/phase-Y4ai/browser-failure.json',JSON.stringify({error:String(e),url:page.url(),passed:checks.length,checks,errors},null,2));throw e;}finally{await browser.close();}
