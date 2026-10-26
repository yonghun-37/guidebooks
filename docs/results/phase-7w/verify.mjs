// 실습·이론 전체의 폭, 런타임 링크, 키보드, 저장 성공/실패를 실제 Chromium에서 확인한다.
import { chromium } from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const base=process.env.SITE_URL || 'http://127.0.0.1:8517/';
const output='docs/results/phase-7w';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({viewport:{width:1280,height:1000}});
// 외부 폰트만 빈 CSS로 대체해 시스템 폰트 대체 표시를 검사한다.
await context.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({status:200,contentType:'text/css',body:''}));
const errors=[], checks=[], links=new Map();
context.on('page',page=>{page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});});
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
const page=await context.newPage();
const routes=[];
async function collect(directory){for(const item of await fs.readdir(directory,{withFileTypes:true})){const file=path.join(directory,item.name);if(item.isDirectory())await collect(file);else if(item.name.endsWith('.html'))routes.push(path.relative('site',file));}}
await collect('site');
try{
 for(const width of [1280,375,360]){
  await page.setViewportSize({width,height:1000});
  for(const route of routes){
   await page.goto(new URL(route,base).href);await page.waitForTimeout(30);
   check(`${width} ${route} 가로 넘침 없음`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   const runtimeLinks=await page.locator('a[href],img[src],script[src],link[rel="stylesheet"]').evaluateAll(nodes=>nodes.map(e=>e.href||e.src));
   for(const href of runtimeLinks){if(href.startsWith(base))links.set(href,route);}
   if(route==='index.html'){
    check('두 트랙 표지',await page.locator('#track-theory').count()===1 && await page.locator('#track-practice').count()===1);
    check('실습편 0~10 데이터',await page.evaluate(()=>ReelsBook.practice.length===11 && ReelsBook.practice[0].number===0));
    await page.locator('[data-menu-toggle]').focus();await page.keyboard.press('Enter');
    check('목차 두 트랙 키보드',await page.locator('#book-menu section').count()===2 && await page.locator('#book-menu').isVisible());
    check('열린 목차 넘침 없음',await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await page.keyboard.press('Escape');check('Escape 목차 닫기',!await page.locator('#book-menu').isVisible());
   }
   if(route.startsWith('practice/') && route!=='practice/e2e.html'){
    check(`${route} 실습 상단`,(await page.locator('h1').textContent()).includes('(실습)'));
    for(const group of await page.locator('[data-os-tabs]').all()){
     const tabs=group.locator('[role="tab"]');
     await tabs.first().focus();await page.keyboard.press('ArrowRight');
     check(`${width} ${route} 오른쪽 탭`,await tabs.nth(1).getAttribute('aria-selected')==='true' && await group.locator('[data-os-panel="macos"]').isVisible());
     await page.keyboard.press('Home');check('Home 첫 탭',await tabs.first().getAttribute('aria-selected')==='true');
     await page.keyboard.press('End');check('End 마지막 탭',await tabs.nth(1).getAttribute('aria-selected')==='true');
     await page.keyboard.press('ArrowLeft');check('왼쪽 첫 탭',await tabs.first().getAttribute('aria-selected')==='true');
     await page.keyboard.press('Tab');check('Tab 본문 패널 진입',await group.locator('[data-os-panel="windows"]').evaluate(e=>e===document.activeElement));
    }
    const first=page.locator('[data-practice-check]').first();await first.focus();const before=await first.isChecked();await page.keyboard.press('Space');
    check(`${width} ${route} Space 체크`,await first.isChecked()!==before);
    await page.reload();check('실습 체크 새로고침 복원',await first.isChecked()!==before);
   }
   if(route==='practice/07-publish.html'){
    await page.locator('#posted-url').fill('https://www.instagram.com/p/EXAMPLE_TEST/');await page.reload();
    check('게시물 주소 복원',await page.locator('#posted-url').inputValue()==='https://www.instagram.com/p/EXAMPLE_TEST/');
   }
   const capture=['index.html','practice/07-publish.html','practice/e2e.html'].includes(route) || (width===375 && ['practice/01-account.html','practice/02-setup.html','practice/08-api.html'].includes(route));
   if(capture){await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${output}/${route.replace(/\//g,'-').replace('.html','')}-${width}.png`,fullPage:route==='practice/e2e.html'});}
  }
 }
 for(const [href,source] of links){
  const u=new URL(href);const response=await context.request.get(u.href.split('#')[0]);
  check(`링크 ${source}: ${u.pathname}${u.hash}`,response.ok());
  if(u.hash && u.pathname.endsWith('.html')){
   await page.goto(u.href.split('#')[0]);check(`앵커 ${u.pathname}${u.hash}`,await page.evaluate(id=>!!document.getElementById(id),decodeURIComponent(u.hash.slice(1))));
  }
 }
 await page.goto(base+'practice/e2e.html');
 check('E2E 전체 단계 35개',await page.locator('[data-practice-check]').count()===35);
 const e2e=page.locator('[data-practice-check="2:first-run"]');
 await e2e.focus();const before=await e2e.isChecked();await page.keyboard.press('Space');
 await page.goto(base+'practice/02-setup.html');check('E2E→실습 상태 공유',await page.locator('[data-practice-check="2:first-run"]').isChecked()!==before);
 await page.goto(base+'practice/e2e.html');await page.locator('[data-practice-reset]').focus();await page.keyboard.press('Enter');
 check('기록 초기화',await page.locator('[data-practice-check]:checked').count()===0);
 await page.goto(base+'practice/07-publish.html');check('게시물 주소 삭제',await page.locator('#posted-url').inputValue()==='');
 for(const mode of ['throw','quota','malformed']){
  const blocked=await browser.newContext({viewport:{width:360,height:900}});
  await blocked.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({status:200,contentType:'text/css',body:''}));
  await blocked.addInitScript(mode=>{
   if(mode==='throw'){Storage.prototype.getItem=()=>{throw new Error('blocked')};Storage.prototype.setItem=()=>{throw new Error('blocked')};}
   if(mode==='quota')Storage.prototype.setItem=()=>{throw new DOMException('quota','QuotaExceededError')};
   if(mode==='malformed')localStorage.setItem('reelsbook:practice:v1','{"version":1,"checks":[],"fields":{"posted-url":3}}');
  },mode);
  const p=await blocked.newPage();p.on('pageerror',e=>errors.push(String(e)));
  await p.goto(base+'practice/e2e.html');
  const input=p.locator('[data-practice-check]').first();await input.focus();await p.keyboard.press('Space');
  check(`${mode} 체크 계속 동작`,await input.isChecked());
  if(mode!=='malformed')check(`${mode} 저장 실패 알림`,(await p.locator('[data-practice-status]').textContent()).includes('저장할 수 없습니다'));
  await p.goto(base+'practice/07-publish.html');await p.locator('#posted-url').fill('https://www.instagram.com/p/LOCAL_ONLY/');
  check(`${mode} 주소 입력 유지`,await p.locator('#posted-url').inputValue()==='https://www.instagram.com/p/LOCAL_ONLY/');
  const tab=p.locator('[data-os-tab="macos"]').first();await tab.focus();await p.keyboard.press('Enter');check(`${mode} 탭 동작`,await tab.getAttribute('aria-selected')==='true');
  await blocked.close();
 }
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:900}});
 await nojs.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({status:200,contentType:'text/css',body:''}));
 const fallback=await nojs.newPage();await fallback.goto(base+'practice/02-setup.html');
 check('JS 없음 양쪽 OS 설명',await fallback.locator('[data-os-panel]:visible').count()===8);
 check('JS 없음 다음 실습 링크',await fallback.locator('[data-chapter-pager] a').count()===1);
 await nojs.close();
 check('콘솔·페이지 오류 0',errors.length===0);
 await fs.writeFile(`${output}/browser-check.json`,JSON.stringify({base,pages:routes.length,widths:[1280,375,360],links:links.size,checks,errors,externalFont:'mocked empty CSS / system fallback'},null,2)+'\n');
 console.log(`${checks.length} checks passed; ${routes.length} pages; ${links.size} runtime links`);
}catch(error){await fs.writeFile(`${output}/browser-failure.json`,JSON.stringify({message:String(error),checks,errors},null,2));throw error;}
finally{await browser.close();}
