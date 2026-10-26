import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='docs/results/phase-A4', origin='http://127.0.0.1:8624', base=origin+'/site-shorts/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage(), checks=[],errors=[],layouts=[],svgIssues=[];
page.on('pageerror',e=>errors.push(String(e)));
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(r.url()+' '+r.status());});
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
const htmls=(await fs.readdir('site-shorts/advanced')).filter(n=>n.endsWith('.html')).map(n=>'advanced/'+n);
const regressions=['index.html','glossary.html','credits.html','practice/09-api.html','practice/e2e.html','chapters/01-map.html'];
for(const file of [...htmls,...regressions])for(const width of [1280,375,360])for(const theme of ['light','dark']){
 await page.setViewportSize({width,height:900});await page.goto(base+file);await page.locator('[data-theme-select]').selectOption(theme);await page.evaluate(()=>document.fonts.ready);
 const size=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,width:innerWidth}));
 layouts.push({file,width,theme,...size});check(`${file} ${width} ${theme} overflow`,size.scroll<=width);
 check(`${file} ${width} ${theme} main`,await page.locator('main h1').count()===1);
 check(`${file} ${width} ${theme} advanced menu`,await page.locator('#book-menu a[href$="advanced/00-overview.html"]').count()===1);
 if(file.startsWith('advanced/')){
  check(`${file} current chapter`,await page.locator('.sidebar-chapters a[aria-current=page]').count()===1);
  const issues=await page.locator('main svg').evaluateAll(svgs=>svgs.flatMap(svg=>[...svg.querySelectorAll('text')].flatMap(t=>{const b=t.getBBox(),v=svg.viewBox.baseVal;return b.x < -1 || b.x+b.width > v.width+1 || b.y < -1 || b.y+b.height>v.height+1 ? [{text:t.textContent,box:{x:b.x,width:b.width},view:v.width}]:[];})));
  if(issues.length)svgIssues.push({file,width,theme,issues});
  if(width===360||((file.includes('00-overview')||file.includes('05-youtube'))&&width===1280)){
   await page.screenshot({path:`${out}/${file.split('/')[1].replace('.html','')}-${width}-${theme}.png`,fullPage:true});
  }
 }
}
await page.setViewportSize({width:1280,height:900});await page.goto(base+'advanced/02-credentials.html');await page.locator('[data-theme-select]').selectOption('light');
check('default cost',await page.locator('#cost-result').textContent()==='월 $0.11520 · 내 월 상한 안이에요. 고정비와 실제 usage도 더 확인하세요.');
await page.locator('[data-cost-preset=image]').click();check('image cost',(await page.locator('#cost-result').textContent()).includes('$8.51400'));
await page.locator('[data-cost-preset=extreme]').focus();await page.keyboard.press('Enter');check('extreme cap',(await page.locator('#cost-result').textContent()).includes('초과'));
await page.locator('#cost-count').fill('-1');check('negative rejected',(await page.locator('#cost-result').textContent()).includes('계산할 수 없어요'));
await page.locator('#cost-count').fill('');check('empty rejected',(await page.locator('#cost-result').textContent()).includes('계산할 수 없어요'));
await page.locator('#cost-count').fill('0');check('zero cost',(await page.locator('#cost-result').textContent()).includes('$0.00000'));
await page.locator('#cost-count').fill('10001');check('out-of-range rejected',(await page.locator('#cost-result').textContent()).includes('계산할 수 없어요'));
await page.locator('[data-cost-preset=low]').click();await page.locator('#calculator').screenshot({path:out+'/calculator-1280.png'});
// Native tab keyboard pattern.
const win=page.locator('#commands-win');await win.focus();await page.keyboard.press('ArrowRight');
check('OS tab focus',await page.locator('#commands-mac').evaluate(el=>document.activeElement===el));
check('OS tab visible',await page.locator('#commands-pm').isVisible());
await page.keyboard.press('Home');check('OS Home',await win.getAttribute('aria-selected')==='true');
await page.locator('#commands-pw .copy-button').click();await page.waitForFunction(()=>document.querySelector('#commands-pw .copy-status').textContent.includes('복사'));check('copy status',(await page.locator('#commands-pw .copy-status').textContent()).includes('복사'));
await page.goto(base+'advanced/06-gates.html');
for(const mode of ['approval','post_review','auto'])for(const test of ['pass','facts','similarity','cost']){
 await page.locator('#gate-mode').selectOption(mode);await page.locator('#gate-case').selectOption(test);
 const text=await page.locator('#gate-result').textContent();check(`gate ${mode} ${test}`,test!=='pass'?text.includes('예외'):text.includes(mode==='auto'?'자동 게시':mode==='post_review'?'예약':'승인 대기'));
}
await page.goto(base+'advanced/07-operations.html');
await page.locator('#runner-pc').selectOption('no');check('runner preparation',(await page.locator('#runner-result').textContent()).includes('이전 준비'));
await page.locator('#runner-state').selectOption('yes');check('runner Actions',(await page.locator('#runner-result').textContent()).includes('GitHub Actions'));
await page.locator('#runner-pc').selectOption('yes');check('runner local',(await page.locator('#runner-result').textContent()).includes('로컬'));
// Quiz: correct feedback, reset, incorrect feedback, reset by keyboard.
for(const file of htmls){await page.goto(base+file);await page.locator('[data-question] button[data-correct=true]').first().click();check(file+' quiz feedback',(await page.locator('[data-feedback]').first().textContent()).includes('정답입니다'));
 await page.locator('[data-quiz-reset]').click();await page.locator('[data-question] button[data-correct=false]').first().click();check(file+' wrong feedback',(await page.locator('[data-feedback]').first().textContent()).includes('다시 살펴보세요'));
 await page.locator('[data-quiz-reset]').focus();await page.keyboard.press('Enter');check(file+' quiz reset',await page.locator('[data-question] button').first().isEnabled());}
// Progress persists across chapters and E2E; reset affects only advanced records.
await page.goto(base+'advanced/00-overview.html');await page.evaluate(()=>localStorage.setItem('shortsbook:practice:v1',JSON.stringify({version:1,checks:{'9:cloud':true},fields:{}})));
await page.locator('[data-advanced-check]').check();await page.goto(base+'advanced/04-render.html');await page.locator('[data-advanced-check]').check();await page.goto(base+'advanced/e2e.html');
check('shared A0 progress',await page.locator('[data-advanced-check="A0:files"]').isChecked());check('shared A4 progress',await page.locator('[data-advanced-check="A4:files"]').isChecked());
await page.locator('[data-advanced-check="live:0"]').check();await page.reload();check('live check restore',await page.locator('[data-advanced-check="live:0"]').isChecked());
await page.locator('[data-advanced-reset]').click();check('advanced reset',await page.locator('[data-advanced-check]:checked').count()===0);
check('practice preserved',await page.evaluate(()=>JSON.parse(localStorage.getItem('shortsbook:practice:v1')).checks['9:cloud']));
// Menu keyboard and theme persistence.
await page.locator('[data-menu-toggle]').focus();await page.keyboard.press('Enter');check('menu keyboard',await page.locator('#book-menu').isVisible());await page.keyboard.press('Escape');check('menu Escape',await page.locator('#book-menu').isHidden());
await page.locator('[data-theme-select]').selectOption('dark');await page.reload();check('theme persistence',await page.locator('html').getAttribute('data-theme')==='dark');
// Video is the clean-copy output, actually decode metadata and play.
await page.goto(base+'advanced/04-render.html');const video=page.locator('video');await video.evaluate(v=>{v.muted=true;v.load();});
await page.waitForFunction(()=>document.querySelector('video').readyState>=1);const duration=await video.evaluate(v=>v.duration);check('mock video duration',duration>36&&duration<37);
await video.evaluate(v=>v.play());await page.waitForFunction(()=>document.querySelector('video').currentTime>0);check('mock video playback',await video.evaluate(v=>!v.paused));await video.evaluate(v=>v.pause());
// Check links rendered by common navigation too, using actual HTTP pages and anchors.
const links=new Set();for(const file of htmls){await page.goto(base+file);for(const href of await page.locator('a[href]').evaluateAll(nodes=>nodes.map(n=>typeof n.href==='string'?n.href:new URL(n.getAttribute('href'),location.href).href)))if(href.startsWith(origin))links.add(href);}
for(const href of links){const u=new URL(href),res=await context.request.get(u.href.split('#')[0]);check('internal '+href,res.ok());if(u.hash){const content=await res.text();check('anchor '+href,content.includes(`id="${decodeURIComponent(u.hash.slice(1))}"`));}}
// JS-disabled access and blocked storage fallback.
const nojs=await browser.newContext({javaScriptEnabled:false});const plain=await nojs.newPage();for(const file of htmls){await plain.goto(base+file);check(file+' no JS content',(await plain.locator('main h1').textContent()).length>0);check(file+' no JS nav',await plain.locator('.adv-chapters a').count()===11);}await nojs.close();
const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError');}});});const bp=await blocked.newPage();await bp.goto(base+'advanced/e2e.html');await bp.locator('[data-advanced-check]').first().check();check('storage blocked keeps check',await bp.locator('[data-advanced-check]').first().isChecked());check('storage blocked notice',(await bp.locator('[data-advanced-progress]').textContent()).includes('저장할 수 없어요'));await blocked.close();
await page.goto(base+'advanced/00-overview.html');for(const width of [1280,375,360])for(const theme of ['light','dark']){await page.setViewportSize({width,height:900});await page.locator('[data-theme-select]').selectOption(theme);await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${out}/representative-${width}-${theme}.png`});await page.locator('#map figure').screenshot({path:`${out}/pipeline-${width}-${theme}.png`});}
await fs.writeFile(out+'/browser-check.json',JSON.stringify({checks:checks.length,layouts,svgIssues,errors,internalLinks:links.size,mockVideoDuration:duration},null,2));
await browser.close();assert.equal(errors.length,0,'console/page/HTTP errors');assert.equal(svgIssues.length,0,'SVG text outside viewBox');console.log(JSON.stringify({checks:checks.length,layouts:layouts.length,errors,svgIssues,links:links.size}));
