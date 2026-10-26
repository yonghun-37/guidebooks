import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
// Pages workflow와 같이 현황 샘플을 임시 호스트에 조립한다.
const host='/tmp/ai-insta-7w-host';
await fs.mkdir(host,{recursive:true});
try { if((await fs.lstat(host+'/progress')).isSymbolicLink()) await fs.unlink(host+'/progress'); } catch(error) { if(error.code!=='ENOENT')throw error; }
await fs.cp('shelf/progress',host+'/progress',{recursive:true});
await fs.mkdir(host+'/progress/samples',{recursive:true});
for(const name of await fs.readdir('starter-kit/samples')){if(/\.(png|mp4)$/.test(name))await fs.copyFile('starter-kit/samples/'+name,host+'/progress/samples/'+name);}
await fs.copyFile('shelf/index.html',host+'/index.html');
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({viewport:{width:1280,height:1000}});
await context.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({status:200,contentType:'text/css',body:''}));
const errors=[],checks=[];
context.on('page',p=>{p.on('pageerror',e=>errors.push(String(e)));p.on('console',m=>{if(m.type()==='error')errors.push(m.text());});});
const p=await context.newPage();const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
const base='http://127.0.0.1:8518/reels/';
try{
 await p.goto(base);
 const tracks=await p.evaluate(()=>ReelsBook.tracks.map(t=>t.chapters.map(c=>ReelsBook.chapterUrl(c))));
 for(const [trackIndex,track] of tracks.entries()){
  for(let i=0;i<track.length;i++){
   const href=new URL(track[i],base).href;await p.goto(href);
   const pager=p.locator('[data-chapter-pager]');
   const expectedNext=i+1<track.length ? new URL(track[i+1],base).href : base+'index.html#contents';
   check(`${trackIndex} ${i} 트랙 내 다음 이동`,await pager.locator('a').last().evaluate(a=>a.href)===expectedNext);
   const local=await p.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>a.href).filter(h=>h.startsWith(location.origin)));
   check(`${trackIndex} ${i} 배포 하위 경로 보존`,local.every(h=>h.startsWith('http://127.0.0.1:8518/reels/')));
  }
 }
 await p.goto(base+'practice/07-publish.html');
 await p.locator('[data-site-header]').evaluate(e=>{e.style.visibility='hidden'});
 await p.locator('#carousel').screenshot({path:'docs/results/phase-7w/practice-07-publish-step-1280.png'});
 await p.locator('[data-site-header]').evaluate(e=>{e.style.visibility=''});
 await p.locator('[data-theme-select]').selectOption('dark');
 check('실습 다크 테마',await p.locator('html').getAttribute('data-theme')==='dark');
 await p.locator('[data-site-header]').evaluate(e=>{e.style.visibility='hidden'});
 await p.locator('#caption-label').screenshot({path:'docs/results/phase-7w/practice-07-publish-labels-dark.png'});
 await p.locator('[data-site-header]').evaluate(e=>{e.style.visibility=''});
 await p.locator('[data-theme-select]').selectOption('light');
 for(const width of [1280,375,360]){
  await p.setViewportSize({width,height:1000});await p.goto('http://127.0.0.1:8518/progress/');
  check(`현황 ${width} 가로 넘침 없음`,await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  check('현황 7w·7v 구분',(await p.locator('main').textContent()).includes('작성·검증 완료') && (await p.locator('main').textContent()).includes('조건부 대기'));
 }
 for(const width of [1280,375,360]){
  await p.setViewportSize({width,height:1000});
  for(const slug of ['05-sources','06-writing','07-cards','08-reels','09-pipeline','10-publishing']){
   await p.goto(base+'chapters/'+slug+'.html');
   check(`이론 작업실 최종 ${width} ${slug}`,await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  }
 }
 // file://로도 두 트랙 링크와 실습 탭이 동작해야 한다. 저장은 브라우저별 정책에 따른다.
 await p.goto('file://'+process.cwd()+'/site/practice/02-setup.html');
 check('file 실습 제목',await p.locator('h1').textContent().then(t=>t.startsWith('(실습) 2.')));
 const link=await p.locator('[data-chapter-pager] a').last().evaluate(a=>a.href);
 check('file 상대 다음 경로',link==='file://'+process.cwd()+'/site/practice/03-copy.html');
 const tabs=p.locator('[data-os-tabs]').first();await tabs.locator('[role="tab"]').last().focus();await p.keyboard.press('Enter');
 check('file 탭',await tabs.locator('[data-os-panel="macos"]').isVisible());
 if(errors.length) console.log(JSON.stringify(errors));
 check('콘솔·페이지 오류 0',errors.length===0);
 await fs.writeFile('docs/results/phase-7w/edge-check.json',JSON.stringify({checks,errors,base},null,2)+'\n');console.log(`${checks.length} edge checks passed`);
}finally{await browser.close();}
