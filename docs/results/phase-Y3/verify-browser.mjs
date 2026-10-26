import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
// Verify offline/system font layout. The only CDN is a pinned optional font.
if(!process.env.FONT_NETWORK) await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage(), checks=[], errors=[], links=new Set(),screens=[];
const origin=process.env.SITE_ORIGIN||'http://127.0.0.1:8589';
const check=(name,truth)=>{assert.ok(truth,name);checks.push(name);};
const overflow=()=>page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,bad:[...document.querySelectorAll('main *')].filter(e=>e.getBoundingClientRect().width>innerWidth&&getComputedStyle(e).position!=='fixed').map(e=>e.tagName+'.'+e.className).slice(0,8)}));
page.on('console',m=>{if(m.type()==='error')errors.push({url:page.url(),message:m.text()});});
page.on('pageerror',e=>errors.push({url:page.url(),message:String(e)}));
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push({url:r.url(),status:r.status()});});
const paths=['/shorts/','/shorts/chapters/02-revenue.html','/shorts/practice/08-publish.html','/shorts/practice/00-start.html','/shorts/chapters/coming-soon.html?chapter=lab','/shorts/practice/coming-soon.html?chapter=07-export','/shorts/credits.html','/','/progress/'];
try {
for(const width of [1280,375,360]) for(const theme of ['light','dark']) {
 await page.setViewportSize({width,height:1100});
 for(const path of paths) {
  await page.goto(origin+path);await page.evaluate(t=>{localStorage.setItem('shortsbook:theme',t);},theme);await page.reload();
  const state=await overflow();check(`가로 넘침 ${width}/${theme}/${path} ${JSON.stringify(state)}`,state.scroll<=width);
  check('제목 있음',Boolean(await page.title()));
  if(path.includes('/shorts/')) {
   check('올바른 책 이름', (await page.locator('.brand').innerText()).includes('ShortsBook'));
   check('본문 건너뛰기',await page.locator('a.skip-link').getAttribute('href')==='#main');
   await page.locator('[data-menu-toggle]').click();check('목차 열기',await page.locator('#book-menu').isVisible());
   check('목차 27개',await page.locator('#book-menu li').count()===27);
   await page.keyboard.press('Escape');check('목차 Escape와 초점',!await page.locator('#book-menu').isVisible()&&await page.locator('[data-menu-toggle]').evaluate(n=>n===document.activeElement));
   if(path.includes('coming-soon'))check('준비중 화면 제목',/준비 중/.test(await page.title()));
   const local=await page.locator('a[href]').evaluateAll(anchors=>anchors.map(a=>a.href).filter(h=>h.startsWith(location.origin)));
   local.forEach(h=>links.add(h));
  }
  await page.locator('.chapter-faq details').evaluateAll(nodes=>nodes.forEach(n=>n.open=true));
  check('FAQ 펼친 뒤 넘침', (await overflow()).scroll<=width);
  if(theme==='light'&&['/shorts/','/shorts/chapters/02-revenue.html','/shorts/practice/08-publish.html'].includes(path)) {
   await page.evaluate(()=>{document.activeElement.blur();scrollTo(0,0);});const name=path==='/shorts/'?'cover':path.includes('02-revenue')?'sample-A':'sample-B';const file=`docs/results/phase-Y3/${name}-${width}.png`;await page.screenshot({path:file});screens.push(file);
  }
  if(path.includes('08-publish')&&theme==='light') {
   await page.locator('#audience').selectOption('general');await page.locator('#ai-content').selectOption('realistic');await page.locator('#music-rights').selectOption('unknown');await page.locator('#upload-tool').scrollIntoViewIfNeeded();await page.evaluate(()=>document.activeElement.blur());
   check('도구 펼친 뒤 넘침',(await overflow()).scroll<=width);
   const file=`docs/results/phase-Y3/upload-check-${width}.png`;await page.screenshot({path:file});screens.push(file);
  }
 }
}
// Every generated internal href, including query-selected preparation pages, resolves.
const inspector=await context.newPage();
for(const href of links) {
 const response=await inspector.goto(href);
 check(`동적 링크 ${href.replace(origin,'')}`,response ? response.status()===200 : inspector.url()===href);
 const hash=new URL(href).hash;
 if(hash)check('동적 앵커 있음',await inspector.evaluate(h=>Boolean(document.getElementById(decodeURIComponent(h.slice(1)))),hash));
}
await inspector.close();
await page.goto(origin+'/shorts/');
check('목차 상태 준비중·샘플 수', await page.evaluate(()=>ShortsBook.chapters.length===16&&ShortsBook.practice.length===11&&[...ShortsBook.chapters,...ShortsBook.practice].every(c=>c.status==='준비중')&&[...ShortsBook.chapters,...ShortsBook.practice].filter(c=>c.sample).length===2));
await page.locator('.skip-link').focus();await page.keyboard.press('Enter');check('본문 이동 키보드',await page.evaluate(()=>location.hash==='#main'));
await page.setViewportSize({width:360,height:1000});
await page.locator('[data-theme-select]').selectOption('dark');
await page.screenshot({path:'docs/results/phase-Y3/cover-360-dark.png'});screens.push('docs/results/phase-Y3/cover-360-dark.png');
if(errors.length) {await fs.writeFile('docs/results/phase-Y3/browser-errors.json',JSON.stringify(errors,null,2)+'\n');console.error(JSON.stringify(errors));}
check('콘솔·페이지·요청 오류 0',errors.length===0);
await fs.writeFile('docs/results/phase-Y3/browser-check.json',JSON.stringify({checks:checks.length,passed:checks,errors,generated_links:links.size,screens,scope:'Chromium; 1280/375/360px; light/dark; '+(process.env.FONT_NETWORK?'actual pinned CDN font enabled.':'optional CDN font disabled to verify fallback.')},null,2)+'\n');
console.log(`${checks.length} browser checks PASS, links ${links.size}, errors ${errors.length}`);
} finally {await browser.close();}
