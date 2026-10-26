import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const out='docs/results/phase-B8',base='http://127.0.0.1:8638/site-blog/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'}),p=await context.newPage(),checks=[],errors=[];
const check=(name,ok)=>{assert.ok(ok,name);checks.push(name);};
p.on('console',e=>{if(e.type()==='error')errors.push(e.text());});p.on('pageerror',e=>errors.push({url:p.url(),stack:e.stack}));
try{
 const diagrams=[['practice/02-setup.html','chat-map-title'],['practice/05-images.html','template-map-title'],['practice/06-editor.html','editor-map-title'],['practice/08-search.html','gsc-map-title']];
 for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const [file,id] of diagrams){
  await p.setViewportSize({width,height:960});await p.goto(base+file);await p.locator('[data-theme-select]').selectOption(theme);
  const svg=p.locator(`svg[aria-labelledby="${id}"]`),figure=svg.locator('..');await figure.scrollIntoViewIfNeeded();
  check(`${file}/${width}/${theme}/화면 틀`,await svg.locator('circle').count()>=3);
  check(`${file}/${width}/${theme}/문자 영역`,await svg.locator('text').evaluateAll(ns=>ns.every(n=>{const b=n.getBBox();return b.x>=0&&b.x+b.width<=320&&b.y>=0&&b.y+b.height<=286;})));
  check(`${file}/${width}/${theme}/넘침0`,await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if((width===1280&&theme==='light')||(width===375&&theme==='light')||(width===360&&theme==='dark'))await figure.screenshot({path:`${out}/${id}-${width}-${theme}.png`});
 }
 await p.goto(base+'chapters/06-writing.html#info');
 const info=p.locator('#info');check('채운 요청문에 실제 공공 URL',await info.locator('pre').first().innerText().then(t=>t.includes('www.nonsan.go.kr')&&t.includes('2025. 5. 2.')&&t.includes('2026-10-26')));
 check('수정 전후 표시',await info.locator('del').count()===1&&await info.locator('ins').count()===1);
 check('완성글에 실제 출처·종료 안내',await info.locator('.draft-sheet').innerText().then(t=>t.includes('모집은 접수가 끝났습니다')&&t.includes('논산시 주민생활지원과')&&t.includes('월 50만원 초과 ~ 250만원 이하')));
 check('공공 원문과 이용조건 각주',await p.locator('#source-b213').count()===1&&await p.locator('#source-b214').count()===1);
 await p.setViewportSize({width:375,height:960});await p.locator('[data-theme-select]').selectOption('light');await p.addStyleTag({content:'[data-site-header], .skip-link {visibility:hidden!important}'});await info.locator('.draft-sheet').screenshot({path:out+'/completed-info-375-light.png'});
 await p.goto(base+'practice/04-draft.html');check('실습 요청 동일 자료',await p.locator('#info-materials').innerText().then(t=>t.includes('www.nonsan.go.kr')&&t.includes('support-check.svg')));
 check('본문 일반 텍스트 요청',await p.locator('#draft-prompt').innerText().then(t=>t.includes('파이프 표 없이 일반 텍스트')));
 // 실제 탭 id를 사용하고 키보드로 이동·선택한다.
 const firstTab=p.locator('[role=tab]').first();await firstTab.focus();await p.keyboard.press('ArrowRight');await p.keyboard.press('Enter');
 check('자료 탭 키보드 이동',await p.locator('[role=tab][aria-selected=true]').innerText().then(t=>t.includes('후기')));
 await p.goto(base+'practice/06-editor.html#plain-text');check('기호와 서식 전후',await p.locator('#plain-text').locator('..').innerText().then(t=>t.includes('**준비물**')&&t.includes('대상: 원문 확인')));
 await p.goto(base+'practice/08-search.html#rss');check('RSS의 정확한 주소·미제출 상태',await p.locator('main').innerText().then(t=>t.includes('https://내블로그.tistory.com/rss')&&t.includes('미제출: 피드 확인 필요')));
 await p.goto(base+'chapters/09-monetize.html#combinations');check('광고 조합별 표',await p.locator('#combinations').locator('..').innerText().then(t=>t.includes('티스토리 애드센스 + 쿠팡')&&t.includes('네이버 애드포스트 + 쿠팡')&&t.includes('새 티스토리 + AdFit')));
 await p.goto(base+'chapters/11-analytics.html#money');check('CPC 주체 직답',await p.locator('#money').innerText().then(t=>t.includes('광고주가 쓴 비용')&&t.includes('계산할 필요가 없습니다')));
 await p.goto(base+'glossary.html#cpc');check('CPC 용어집 일치',await p.locator('#cpc').innerText().then(t=>t.includes('광고주가 지출한 광고비')&&t.includes('페이지 RPM')));
 await p.goto(base+'chapters/13-plan.html');await p.locator('#plan-focus').selectOption('travel');await p.locator('#plan-form button[type=submit]').click();check('여행 계획 조사',await p.locator('#plan-body').innerText().then(t=>!t.includes('점를')&&t.includes('실수 메모를')));
 // README/예시 문서의 실제 상대 링크 검사. 코드 예시 안 가짜 링크는 제외.
 for(const folder of ['blog-kit','site-blog/samples/blog-kit'])for(const file of [folder+'/README.md',folder+'/samples/routes.md'].filter(f=>!f.includes('site-blog/samples/blog-kit/samples/'))){
  const body=(await fs.readFile(file,'utf8')).replace(/```[\s\S]*?```/g,'').replace(/`[^`\n]*`/g,'');
  for(const m of body.matchAll(/\[[^\]\n]+\]\(([^)]+)\)/g)){
   if(/^(https?:|#)/.test(m[1]))continue;
   const target=path.resolve(path.dirname(file),m[1].split('#')[0]);check('문서링크 '+file+' '+m[1],(await fs.stat(target)).isFile());
  }
 }
 const webRoutes=await fs.readFile('site-blog/samples/blog-kit/routes.md','utf8');for(const m of webRoutes.matchAll(/\[[^\]\n]+\]\(([^)]+)\)/g))check('웹경로표 '+m[1],(await fs.stat(path.resolve('site-blog/samples/blog-kit',m[1]))).isFile());
 check('B8 콘솔·페이지 오류0',errors.length===0);
 await fs.writeFile(out+'/b8-check.json',JSON.stringify({checks:checks.length,errors,passed:checks},null,2));console.log(JSON.stringify({checks:checks.length,errors}));
} catch(e){await fs.writeFile(out+'/b8-failure.json',JSON.stringify({error:String(e),checks,errors},null,2));throw e;}finally{await browser.close();}
