import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='docs/results/phase-B6', origin='http://127.0.0.1:8636', base=origin+'/site-blog/';
const files=(await fs.readdir('site-blog/chapters')).filter(f=>f.endsWith('.html')).map(f=>'chapters/'+f);
files.push(...(await fs.readdir('site-blog/practice')).filter(f=>f.endsWith('.html')).map(f=>'practice/'+f));
files.push('index.html','lab.html','glossary.html','prompts.html','ai-models.html','credits.html','samples/blog-kit/preview.html');
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']}),page=await context.newPage();
const checks=[],errors=[],links=new Set(),refs=[];
const check=(name,v)=>{assert.ok(v,name);checks.push(name);};
const monitor=p=>{p.on('console',m=>{if(m.type()==='error')errors.push(m.text());});p.on('pageerror',e=>errors.push(String(e)));p.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(r.status()+' '+r.url());});};monitor(page);
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
try {
 for(const width of [1280,375,360])for(const theme of ['light','dark']){
  for(const file of files){
   await page.setViewportSize({width,height:960});await page.goto(base+file);
   if(await page.locator('[data-theme-select]').count())await page.locator('[data-theme-select]').selectOption(theme);
   await page.evaluate(()=>document.fonts.ready);
   check(`${file}/${width}/${theme}/넘침0`,await overflow());check(`${file}/${width}/${theme}/제목`,await page.locator('h1').count()===1);
   for(const href of await page.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>new URL(a.getAttribute("href"),location.href).href)))if(href.startsWith(origin))links.add(href);
   if(!file.includes('pending')&&!file.startsWith('samples/')){
    check(`${file}/준비중경로없음`,await page.locator('a[href*="pending.html"]').count()===0);
    check(`${file}/목차완성`,await page.locator('#book-menu .status').evaluateAll(ns=>ns.length===30&&ns.every(n=>n.textContent==='완성')));
    const menu=page.locator('[data-menu-toggle]');await menu.focus();await page.keyboard.press('Enter');check(`${file}/목차Enter`,await menu.getAttribute('aria-expanded')==='true');await page.keyboard.press('Escape');check(`${file}/목차Escape초점`,await menu.evaluate(n=>document.activeElement===n)&&await menu.getAttribute('aria-expanded')==='false');
   }
   if(['index.html','lab.html','glossary.html','prompts.html','ai-models.html'].includes(file)){
    await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${out}/${file.replace('.html','')}-${width}-${theme}.png`});
   }
  }
  // 실험실의 모든 원본을 좁은 화면·두 테마에서도 직접 로드한다.
  await page.goto(base+'lab.html');await page.locator('[data-theme-select]').selectOption(theme);
  const tools=await page.evaluate(()=>window.BlogCatalog);
  for(const tool of tools){
   await page.locator('#sim-picker').selectOption(`${tool.slug}:${tool.id}`);
   const frame=page.frameLocator('#sim-frame');await frame.locator('#'+tool.id).waitFor({state:'visible'});
   await page.waitForFunction(id=>{const f=document.querySelector('#sim-frame');return f.contentDocument?.documentElement.dataset.theme===document.documentElement.dataset.theme&&f.contentDocument.getElementById(id)?.getBoundingClientRect().height>0;},tool.id);
   check(`lab/${tool.chapter}/${width}/${theme}/원본`,(await page.locator('#sim-frame').getAttribute('src')).includes(`?embed=${tool.id}`));
   check(`lab/${tool.chapter}/${width}/${theme}/가로넘침0`,await frame.locator('html').evaluate(n=>n.scrollWidth<=n.clientWidth));
   check(`lab/${tool.chapter}/${width}/${theme}/테마`,await frame.locator('html').getAttribute('data-theme')===theme);
   check(`lab/${tool.chapter}/${width}/${theme}/외곽숨김`,!await frame.locator('[data-site-header]').isVisible());
   const controls=frame.locator('#'+tool.id).locator('input:not([type=hidden]),select,textarea,button');
   if(await controls.count()){const c=controls.first();await c.focus();check(`lab/${tool.chapter}/키보드초점`,await c.evaluate(n=>document.activeElement===n));}
  }
  if(width===360){await page.locator('#sim-picker').selectOption('13-plan:plan-tool');await page.frameLocator('#sim-frame').locator('#plan-tool').waitFor();await page.screenshot({path:`${out}/lab-plan-360-${theme}.png`});}
 }
 // 모든 동적 내부 링크와 앵커, 숫자가 있는 장/실습 링크를 대조한다.
 for(const href of links){
  const url=new URL(href);const r=await context.request.get(url.origin+url.pathname+url.search);check('링크 '+url.pathname,r.ok());
  if(url.hash){const html=await r.text();check('앵커 '+url.pathname+url.hash,html.includes('id="'+decodeURIComponent(url.hash.slice(1))+'"')||html.includes("id='"+decodeURIComponent(url.hash.slice(1))+"'"));}
 }
 for(const file of files.filter(f=>!f.includes('pending')&&!f.startsWith('samples/'))){
  await page.goto(base+file);
  const pager=page.locator('[data-chapter-pager]');
  if(await pager.count()){
   const expected=await page.evaluate(()=>{
    const slug=document.body.dataset.chapter||document.body.dataset.practice||document.body.dataset.appendix;
    const sequence=window.BlogBook.tracks.find(t=>t.chapters.some(c=>c.slug===slug))?.chapters;
    if(!sequence)return null;
    const i=sequence.findIndex(c=>c.slug===slug);
    return [i>0?window.BlogBook.chapterUrl(sequence[i-1]):window.BlogBook.url('index.html'),i<sequence.length-1?window.BlogBook.chapterUrl(sequence[i+1]):window.BlogBook.url('index.html#contents')].map(u=>new URL(u,location.href).href);
   });
   if(expected){const actual=await pager.locator('a').evaluateAll(as=>as.map(a=>a.href));check('이전다음 '+file,JSON.stringify(actual)===JSON.stringify(expected));}
  }
  const data=await page.locator('main a[href]').evaluateAll(as=>as.filter(a=>!a.closest('[data-chapter-toc]')).map(a=>({text:a.textContent,url:new URL(a.getAttribute("href"),location.href).href})));
  for(const a of data){
   const u=new URL(a.url);if(!u.href.startsWith(base))continue;
   const tm=a.text.match(/(?<!실습\s)(\d+)장/),pm=a.text.match(/실습\s*(\d+)/);
   const number=u.pathname.match(/\/(chapters|practice)\/(\d+)-/);
   if(!number)continue;
   if(tm&&number[1]==='chapters'){check(`장번호 ${file} ${a.text.slice(0,38)}`,Number(tm[1])===Number(number[2]));refs.push({file,...a});}
   if(pm&&number[1]==='practice'){check(`실습번호 ${file} ${a.text.slice(0,38)}`,Number(pm[1])===Number(number[2]));refs.push({file,...a});}
  }
 }
 await page.goto(base+'prompts.html');
 const boxes=page.locator('[data-prompt-origin]');check('프롬프트18개',await boxes.count()===18);
 for(let i=0;i<await boxes.count();i++){
  const b=boxes.nth(i);const expected=await b.locator('code').textContent();await b.locator('.copy-button').focus();await page.keyboard.press('Enter');await page.waitForFunction(i=>document.querySelectorAll('[data-prompt-origin]')[i].querySelector('[role=status]').textContent==='복사했습니다.',i);
  check('프롬프트복사'+i,await page.evaluate(async()=>navigator.clipboard.readText())===expected);
 }
 await page.goto(base+'glossary.html');await page.locator('#term-search').fill('인증 토큰');check('인증토큰검색',await page.locator('#token').isVisible());check('사용량토큰분리',!await page.locator('#ai-token').isVisible());await page.locator('#term-search').fill('API');check('용어검색축소',await page.locator('[data-glossary-entry]:visible').count()<43);await page.evaluate(()=>location.hash='pv');check('직접앵커검색해제',await page.locator('#pv').isVisible());
 await page.goto(base+'chapters/01-map.html');const term=page.locator('a[data-term]').first();await term.focus();check('용어키보드설명',await term.locator('[role=tooltip]').isVisible());await page.keyboard.press('Escape');check('용어Escape',!await term.locator('[role=tooltip]').isVisible());
 await page.goto(base+'practice/03-keywords.html');await page.locator('[data-practice-check="3:keywords"]').focus();await page.keyboard.press('Space');await page.goto(base+'practice/e2e.html');check('실습E2E진행공유',await page.locator('[data-practice-check="3:keywords"]').isChecked());await page.locator('#e2e-url').fill('https://example.invalid/blog-test');await page.goto(base+'practice/07-publish.html');check('E2E주소복원',await page.locator('[data-practice-field="posted-url"]').inputValue()==='https://example.invalid/blog-test');
 // sample은 동봉 파일만 요청하며 서버 하위 경로에서 열린다.
 await page.goto(base+'index.html');await page.locator('#kit-sample').scrollIntoViewIfNeeded();const sample=page.frameLocator('.sample-preview');await sample.locator('h1').waitFor();check('샘플제목',await sample.locator('h1').innerText()==='청년 직장인 지원 제도, 신청 전에 어디부터 볼까');await sample.locator('img').scrollIntoViewIfNeeded();await page.waitForFunction(()=>document.querySelector('.sample-preview').contentDocument.querySelector('img').naturalWidth>0);check('샘플그림',await sample.locator('img').evaluate(i=>i.complete&&i.naturalWidth>0));check('샘플모바일넘침0',await sample.locator('html').evaluate(n=>n.scrollWidth<=n.clientWidth));
 for(const [width,theme] of [[1280,'light'],[375,'light'],[360,'dark']]){
  await page.setViewportSize({width,height:960});
  for(const [file,id] of [['index.html','ai-start'],['index.html','quick-paths'],['index.html','kit-sample'],['ai-models.html','per-article'],['prompts.html','review']]){
   await page.goto(base+file);await page.locator('[data-theme-select]').selectOption(theme);await page.locator('#'+id).evaluate(n=>scrollTo(0,n.getBoundingClientRect().top+scrollY-85));await page.screenshot({path:`${out}/${file.replace('.html','')}-${id}-${width}-${theme}.png`});
  }
  await page.goto(base+'index.html');await page.locator('[data-theme-select]').selectOption(theme);await page.locator('#kit-sample').scrollIntoViewIfNeeded();await page.frameLocator('.sample-preview').locator('img').scrollIntoViewIfNeeded();await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${out}/cover-full-${width}-${theme}.png`,fullPage:true});
 }
 // JavaScript 없이도 표지 전체 목차와 부록·본문은 읽힌다.
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:900}}),np=await nojs.newPage();monitor(np);
 for(const file of ['index.html','prompts.html','ai-models.html','glossary.html','lab.html','practice/01-account.html']){
  await np.goto(base+file);check(file+'/JS없는본문',await np.locator('h1').isVisible());check(file+'/JS없는넘침',await np.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(file==='index.html')check('JS없는전체목차',await np.locator('[data-chapter-toc] a').count()===30);
 }
 await nojs.close();
 const blocked=await browser.newContext({viewport:{width:360,height:900}});await blocked.addInitScript(()=>{Object.defineProperty(Storage.prototype,'getItem',{value(){throw new Error('blocked');}});Object.defineProperty(Storage.prototype,'setItem',{value(){throw new Error('blocked');}});Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('denied'))}});});const bp=await blocked.newPage();monitor(bp);
 await bp.goto(base+'prompts.html');await bp.locator('.copy-button').first().click();check('클립보드차단대안',(await bp.locator('.copy-status').first().textContent()).includes('직접 복사'));check('복사내용선택',await bp.evaluate(()=>getSelection().toString().length>50));await bp.goto(base+'practice/03-keywords.html');await bp.locator('[data-practice-check]').check();check('저장차단계속체크',await bp.locator('[data-practice-check]').isChecked());check('저장차단안내',(await bp.locator('[data-practice-status]').first().innerText()).includes('저장할 수 없습니다'));await blocked.close();
 check('콘솔·페이지·내부HTTP오류0',errors.length===0);
 await fs.writeFile(out+'/browser-check.json',JSON.stringify({pages:files.length,viewports:[1280,375,360],themes:['light','dark'],checks:checks.length,internalLinks:links.size,numberedReferences:refs.length,errors,passed:checks},null,2));await fs.writeFile(out+'/numbered-references.json',JSON.stringify(refs,null,2));
 console.log(JSON.stringify({pages:files.length,checks:checks.length,links:links.size,numberedReferences:refs.length,errors}));
} catch(e){await fs.writeFile(out+'/browser-failure.json',JSON.stringify({error:String(e),checks:checks.length,errors},null,2));throw e;}finally{await browser.close();}
