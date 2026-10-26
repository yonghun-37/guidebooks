import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const b=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox'],headless:true});
const c=await b.newContext();await c.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const p=await c.newPage(),checks=[],errors=[];p.on('pageerror',e=>errors.push(String(e)));
const check=(label,ok)=>{assert.ok(ok,label);checks.push(label)};
try{
for(const name of ['chapters/05b-ai-tools.html','prompts.html','ai-models.html']){
 await p.goto('file:///tmp/aia-integration-site/site/'+name);
 for(const [slug,end] of [['05b-ai-tools','chapters/05b-ai-tools.html'],['prompts','prompts.html'],['ai-models','ai-models.html']]){
  const href=await p.evaluate(slug=>ReelsBook.chapterUrl(ReelsBook.chapters.find(c=>c.slug===slug)),slug);
  check(name+' registered '+slug,href.endsWith(end));
 }
 check(name+' menu links to appendix',(await p.locator('#book-menu a[href$="ai-models.html"]').count())===1);
 check(name+' footer prompt link',(await p.locator('footer a[href$="prompts.html"]').count())===1);
 if(name.includes('05b')){
  check('previous source',(await p.locator('[data-chapter-pager] a').first().getAttribute('href')).endsWith('05-sources.html'));
  check('next writing',(await p.locator('[data-chapter-pager] a').last().getAttribute('href')).endsWith('06-writing.html'));
  check('theory outline 9',await p.locator('[data-book-sidebar] nav').first().locator('li').count()===9);
 }
}
check('no errors',errors.length===0);
}finally{await fs.writeFile(new URL('./integration-browser.json',import.meta.url),JSON.stringify({checks,errors},null,2));await b.close()}
console.log(checks.length+' integration checks passed');
