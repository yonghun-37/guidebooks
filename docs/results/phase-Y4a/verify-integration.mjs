import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const page=await browser.newPage(),checks=[];
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
const base='http://127.0.0.1:8594/site-shorts/chapters/';
try{
 // requests.md의 diff를 /tmp 복사본에 적용한 JS만 응답한다. 저장소 공통 파일은 수정하지 않는다.
 const proposed=await fs.readFile('/tmp/y4a-integration/site-shorts/assets/book.js','utf8');
 await page.route('**/site-shorts/assets/book.js',route=>route.fulfill({contentType:'text/javascript',body:proposed}));
 for(const [number,slug]of [[1,'01-map'],[3,'03-hook'],[4,'04-script'],[5,'05-audio']]){
  await page.goto(base+slug+'.html');
  check(slug+': 준비중 제목 제거',!/(준비 ?중)/.test(await page.title()));
  const href=await page.evaluate(n=>window.ShortsBook.chapterUrl(window.ShortsBook.byNumber(n)),number);
  check(slug+': 실제 본문 연결',href.endsWith('/'+slug+'.html'));
  check(slug+': 완성 표시',await page.locator('.sidebar-chapters a[aria-current=page] .status').innerText()==='완성');
 }
 await page.goto(base+'02-revenue.html');check('이론2 샘플 보존',await page.locator('.sidebar-chapters a[aria-current=page] .status').innerText()==='확인용 샘플');
 check('이론6 준비 상태 보존',await page.evaluate(()=>window.ShortsBook.chapterUrl(window.ShortsBook.byNumber(6)).includes('coming-soon.html?chapter=06-scenes')));
 await page.goto(base+'../practice/08-publish.html');check('실습8 샘플 보존',await page.locator('.sidebar-chapters a[aria-current=page] .status').innerText()==='확인용 샘플');
 await fs.writeFile('docs/results/phase-Y4a/integration-diff-check.json',JSON.stringify({checks:checks.length,passed:checks,mode:'requests diff applied to /tmp copy only'},null,2)+'\n');
 console.log(JSON.stringify({checks:checks.length,mode:'제안 diff 임시 적용, 저장소 공통 파일 미수정'}));
}finally{await browser.close();}
