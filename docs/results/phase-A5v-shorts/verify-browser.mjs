import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
const out='docs/results/phase-A5v-shorts',origin='http://127.0.0.1:8625',base=origin+'/site-shorts/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const ctx=await browser.newContext({reducedMotion:'reduce'});
// External font availability is not the target of this local rendering check.
await ctx.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.fulfill({status:200,contentType:'text/css',body:''}));
const page=await ctx.newPage(),errors=[],layouts=[],svgIssues=[],images=[],links=new Set(),interactions=[];
page.on('pageerror',e=>errors.push({type:'page',message:String(e)}));
page.on('console',m=>{if(m.type()==='error')errors.push({type:'console',message:m.text()});});
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push({type:'http',message:r.url()+' '+r.status()});});
const files=(await fs.readdir('site-shorts/advanced')).filter(f=>f.endsWith('.html'));
for(const file of files)for(const width of [1280,375,360])for(const theme of ['light','dark']){
 await page.setViewportSize({width,height:960});await page.goto(base+'advanced/'+file);await page.locator('[data-theme-select]').selectOption(theme);await page.evaluate(()=>document.fonts.ready);
 // Trigger lazy image requests before reading natural dimensions.
 await page.locator('main img').evaluateAll(async els=>{for(const el of els){el.loading='eager';await el.decode();}});
 const layout=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,main:!!document.querySelector('main h1')}));layouts.push({file,width,theme,...layout});
 if(layout.scroll>width)errors.push({type:'overflow',file,width,theme,...layout});
 const issue=await page.locator('main svg').evaluateAll(svgs=>svgs.flatMap(svg=>[...svg.querySelectorAll('text')].flatMap(t=>{
  const b=t.getBBox(),v=svg.viewBox.baseVal,r=svg.getBoundingClientRect(),size=parseFloat(getComputedStyle(t).fontSize)*r.width/v.width;
  const failures=[];if(b.x < -1||b.x+b.width>v.width+1||b.y< -1||b.y+b.height>v.height+1)failures.push('outside SVG');
  // Text starting in a panel must fit that panel, avoiding hidden overlap.
  const panel=[...svg.querySelectorAll('rect')].reverse().find(n=>{const q=n.getBBox();return b.x>=q.x&&b.x<q.x+q.width&&b.y>=q.y&&b.y<q.y+q.height&&q.height>40;});
  if(panel){const q=panel.getBBox();if(b.x+b.width>q.x+q.width-3)failures.push('outside panel');}
  return failures.length?[{text:t.textContent,failures,x:b.x,width:b.width,view:v.width,size}]:[];
 })));
 if(issue.length)svgIssues.push({file,width,theme,issue});
 images.push({file,width,theme,...await page.locator('main img').evaluateAll(els=>({count:els.length,broken:els.filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src)}))});
 if(width===360){await page.screenshot({style:"header{visibility:hidden!important}",path:`${out}/${file.replace('.html','')}-360-${theme}.png`,fullPage:true});}
 if(width===360&&['00-overview.html','02-credentials.html','04-render.html','06-gates.html','07-operations.html'].includes(file)){
  for(const id of await page.locator('figure[id]').evaluateAll(els=>els.map(e=>e.id)))await page.locator('#'+id).screenshot({style:"header{visibility:hidden!important}",path:`${out}/${id}-360-${theme}.png`});
 }
 if(width===1280&&['00-overview.html','04-render.html','07-operations.html'].includes(file)){
  const id=file.startsWith('00')?'system-map':file.startsWith('04')?'render-frames':'report-sample';await page.locator('#'+id).screenshot({style:"header{visibility:hidden!important}",path:`${out}/${id}-1280-${theme}.png`});
 }
 for(const href of await page.locator('a[href]').evaluateAll(els=>els.map(e=>new URL(e.getAttribute('href'),location.href).href)))if(href.startsWith(origin))links.add(href);
}
for(const href of links){const u=new URL(href),res=await ctx.request.get(u.href.split('#')[0]);if(!res.ok())errors.push({type:'link',href,status:res.status()});else if(u.hash){const body=await res.text();if(!body.includes(`id="${decodeURIComponent(u.hash.slice(1))}"`))errors.push({type:'anchor',href});}}
await page.setViewportSize({width:360,height:960});await page.goto(base+'advanced/00-overview.html');
for(const link of await page.locator('#system-map svg a').all()){
 const href=await link.getAttribute('href');await link.focus();const focused=await link.evaluate(e=>document.activeElement===e);interactions.push({name:'system link focus',href,pass:focused});
}
await page.locator('#system-map a[href="06-gates.html"]').focus();await page.keyboard.press('Enter');await page.waitForURL('**/06-gates.html');interactions.push({name:'system link Enter',pass:page.url().endsWith('06-gates.html')});
await page.locator('#gate-mode').selectOption('auto');await page.locator('#gate-case').selectOption('facts');interactions.push({name:'gate failure still exception',pass:(await page.locator('#gate-result').textContent()).includes('예외')});
await page.goto(base+'advanced/02-credentials.html');await page.locator('[data-cost-preset=image]').click();interactions.push({name:'calculator preserved',pass:(await page.locator('#cost-result').textContent()).includes('$8.51400')});
await page.goto(base+'advanced/04-render.html');const video=page.locator('video');await video.evaluate(v=>{v.muted=true;v.load()});await page.waitForFunction(()=>document.querySelector('video').readyState>=1);interactions.push({name:'original video metadata',pass:(await video.evaluate(v=>v.duration))>36});
// New visual narratives remain available without JS.
const plain=await browser.newContext({javaScriptEnabled:false});await plain.route(/fonts\.(googleapis|gstatic)\.com/,r=>r.fulfill({status:200,contentType:'text/css',body:''}));const pp=await plain.newPage();
for(const f of files){await pp.goto(base+'advanced/'+f);interactions.push({name:f+' no JS figure',pass:await pp.locator('figure').count()>0});}
await plain.close();
const report={combinations:layouts.length,layouts,svgIssues,images,errors,internalLinks:links.size,interactions};await fs.writeFile(out+'/browser-check.json',JSON.stringify(report,null,2));
await browser.close();console.log(JSON.stringify({combinations:layouts.length,svgIssues,errors,brokenImages:images.filter(i=>i.broken.length),internalLinks:links.size,failedInteractions:interactions.filter(i=>!i.pass)},null,2));
if(errors.length||svgIssues.length||images.some(i=>i.broken.length)||interactions.some(i=>!i.pass))process.exitCode=1;
