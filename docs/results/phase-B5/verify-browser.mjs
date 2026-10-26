import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='docs/results/phase-B5', origin='http://127.0.0.1:8627', base=origin+'/site-blog/practice/';
const paths=['00-start','01-account','02-setup','03-keywords','04-draft','05-images','06-editor','07-publish','08-search','09-monetize','10-automation','e2e'];
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']}),page=await context.newPage();
const checks=[],errors=[],links=new Set();
const check=(name,v)=>{assert.ok(v,name);checks.push(name);};
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('pageerror',e=>errors.push(String(e)));
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(r.status()+' '+r.url());});
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
try {
 for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const slug of paths){
  await page.setViewportSize({width,height:1000});await page.goto(base+slug+'.html');await page.locator('[data-theme-select]').selectOption(theme);await page.evaluate(()=>document.fonts.ready);
  check(`${slug}/${width}/${theme}/넘침0`,await overflow());
  check(`${slug}/${width}/${theme}/제목`,await page.locator('h1').count()===1);
  for(const href of await page.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>a.href)))if(href.startsWith(origin))links.add(href);
  const groups=page.locator('[data-os-tabs]');
  for(let i=0;i<await groups.count();i++){
   const group=groups.nth(i);if(!await group.isVisible())continue;
   const tabs=group.locator(':scope > [data-tab-list] > [data-os-tab]');
   for(let j=0;j<await tabs.count();j++){
    await tabs.nth(j).click();check(`${slug}/${width}/${theme}/탭${i}-${j}`,await overflow());
    check(`${slug}/탭패널${i}-${j}`,await page.locator('#'+await tabs.nth(j).getAttribute('aria-controls')).isVisible());
   }
   await tabs.first().click();
   await tabs.first().focus();await page.keyboard.press('End');check(`${slug}/End${i}`,await tabs.last().getAttribute('aria-selected')==='true');
   await page.keyboard.press('Home');check(`${slug}/Home${i}`,await tabs.first().getAttribute('aria-selected')==='true');
   if(await tabs.count()>1){await page.keyboard.press('ArrowRight');check(`${slug}/Right${i}`,await tabs.nth(1).getAttribute('aria-selected')==='true');await page.keyboard.press('ArrowLeft');}
  }
  const menu=page.locator('[data-menu-toggle]');await menu.focus();await page.keyboard.press('Enter');check(`${slug}/목차키보드`,await menu.getAttribute('aria-expanded')==='true');await page.keyboard.press('Escape');
  await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:`${out}/${slug}-${width}-${theme}.png`});
 }
 for(const href of links){
  const url=new URL(href);const response=await context.request.get(url.origin+url.pathname+url.search);check('내부 링크 '+url.pathname,response.ok());
  if(url.hash){const html=await response.text();check('앵커 '+url.pathname+url.hash,html.includes('id="'+decodeURIComponent(url.hash.slice(1))+'"')||html.includes("id='"+decodeURIComponent(url.hash.slice(1))+"'"));}
 }
 await page.goto(base+'04-draft.html');const copy=page.locator('[data-copy-target="info-materials"]');await copy.focus();await page.keyboard.press('Enter');await page.waitForFunction(()=>document.querySelector('[data-copy-target="info-materials"]').textContent==='복사했어요');
 check('프롬프트 복사',await page.evaluate(async()=> (await navigator.clipboard.readText()).includes('[공식 자료 1]')));
 await page.goto(base+'03-keywords.html');const faq=page.locator('#faq details').first();await faq.locator('summary').focus();await page.keyboard.press('Enter');check('FAQ Enter',(await faq.getAttribute('open'))!==null);await page.keyboard.press('Enter');check('FAQ 닫기',(await faq.getAttribute('open'))===null);const keyboardCheck=page.locator('[data-practice-check="3:keywords"]');await keyboardCheck.focus();await page.keyboard.press('Space');check('체크 Space',await keyboardCheck.isChecked());await page.keyboard.press('Space');await page.locator('#keyword-notes').fill('실제 조회 조건과 선택 이유');await page.reload();check('메모 복원',await page.locator('#keyword-notes').inputValue()==='실제 조회 조건과 선택 이유');
 await page.locator('[data-practice-check="3:keywords"]').check();await page.goto(base+'e2e.html');check('E2E 교차 체크',await page.locator('[data-practice-check="3:keywords"]').isChecked());
 await page.locator('[data-practice-check="3:keywords"]').uncheck();await page.goto(base+'03-keywords.html');check('E2E 역방향 체크',!await page.locator('[data-practice-check="3:keywords"]').isChecked());
 await page.goto(base+'07-publish.html');await page.locator('[data-practice-field="posted-url"]').fill('https://example.invalid/my-first-post');await page.goto(base+'e2e.html');check('발행 주소 교차 복원',await page.locator('#e2e-url').inputValue()==='https://example.invalid/my-first-post');
 await page.locator('[data-practice-reset]').click();check('주소 초기화',await page.locator('#e2e-url').inputValue()==='');await page.locator('[data-work-clear]').click();await page.goto(base+'03-keywords.html');check('메모 초기화',await page.locator('#keyword-notes').inputValue()==='');
 await page.goto(base+'05-images.html');check('AI 예시 파일 로딩',await page.locator('img').evaluate(i=>i.complete&&i.naturalWidth===1672));
 for(const [slug,id] of [['03-keywords','trend'],['04-draft','compare'],['05-images','ai-image'],['05-images','compare'],['06-editor','disclosure'],['08-search','google'],['10-automation','dry-run']]){
  for(const [width,theme]of [[1280,'light'],[360,'dark']]){
   await page.setViewportSize({width,height:1000});await page.goto(base+slug+'.html');await page.locator('[data-theme-select]').selectOption(theme);await page.locator('#'+id).evaluate(el=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY-90));await page.screenshot({path:`${out}/${slug}-${id}-${width}-${theme}.png`});
  }
 }
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:900}}),np=await nojs.newPage();
 for(const slug of ['01-account','03-keywords','04-draft','05-images','10-automation','e2e']){
  await np.goto(base+slug+'.html');check(slug+'/JS없는본문',await np.locator('h1').isVisible());check(slug+'/JS없는넘침',await np.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if(slug==='01-account')check('JS없이두플랫폼',await np.locator('#panel-account-tistory').isVisible());
 }
 await nojs.close();
 const blocked=await browser.newContext({viewport:{width:360,height:900}});await blocked.addInitScript(()=>{Object.defineProperty(Storage.prototype,'setItem',{value(){throw new Error('blocked');}});});
 const bp=await blocked.newPage();await bp.goto(base+'03-keywords.html');await bp.locator('#keyword-notes').fill('저장 차단에서도 입력');check('저장차단안내',(await bp.locator('[data-work-status]').innerText()).includes('저장할 수 없어요'));check('저장차단입력',await bp.locator('#keyword-notes').inputValue()==='저장 차단에서도 입력');await bp.locator('[data-practice-check]').check();check('저장차단체크',await bp.locator('[data-practice-check]').isChecked());await blocked.close();
 const clipblock=await browser.newContext();await clipblock.addInitScript(()=>{Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('denied'))}});});const cp=await clipblock.newPage();await cp.goto(base+'04-draft.html');await cp.locator('[data-copy-target="info-materials"]').click();check('클립보드차단대안',(await cp.locator('[data-work-status]').innerText()).includes('문장을 선택했어요'));await clipblock.close();
 check('콘솔·페이지·HTTP오류0',errors.length===0);
 await fs.writeFile(out+'/browser-check.json',JSON.stringify({pages:paths.length,viewports:[1280,375,360],themes:['light','dark'],checks:checks.length,internalLinks:links.size,errors,passed:checks},null,2));
 console.log(JSON.stringify({checks:checks.length,links:links.size,errors}));
}finally{await browser.close();}
