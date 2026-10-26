import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage(),origin='http://127.0.0.1:8594',base=origin+'/site-shorts/practice/',checks=[],errors=[],links=new Set();
const slugs=['00-start','01-account','02-setup','03-script','04-voice','05-scenes','06-edit','07-export','08-publish','09-api','10-insights','e2e'];
const check=(name,val)=>{assert.ok(val,name);checks.push(name);};
page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(r.url()+' '+r.status());});
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
try {
 for(const width of [1280,375,360]) for(const theme of ['light','dark']) for(const slug of slugs) {
  await page.setViewportSize({width,height:1000});await page.goto(base+slug+'.html');await page.locator('h1').waitFor();
  await page.locator('[data-theme-select]').selectOption(theme);
  await page.evaluate(()=>document.fonts.ready);
  check(`${slug}/${width}/${theme}: 가로 넘침 없음`,await overflow());
  check(`${slug}: 본문 제목`,Boolean(await page.locator('h1').innerText()));
  if(slug!=='e2e')check(`${slug}: FAQ5`,await page.locator('.chapter-faq details').count()===5);
  await page.locator('.chapter-faq details').evaluateAll(nodes=>nodes.forEach(n=>n.open=true));
  check(`${slug}/${width}: FAQ 펼친 뒤 넘침 없음`,await overflow());
  for(const tab of await page.locator('[data-os-tab]').all()){
   await tab.click();check(`${slug}: OS 탭 패널`,await page.locator('[data-os-panel]:visible').count()>=1);check(`${slug}: 탭 뒤 넘침`,await overflow());
  }
  for(const h of await page.locator('main a[href]').evaluateAll(nodes=>nodes.map(n=>n.href).filter(h=>h.startsWith(location.origin))))links.add(h);
  if(theme==='light'&&['00-start','03-script','05-scenes','06-edit','e2e'].includes(slug)){
   await page.evaluate(()=>{document.activeElement.blur();scrollTo(0,0);});
   await page.screenshot({path:`docs/results/phase-Y4p/${slug}-${width}.png`});
   if(slug==='05-scenes'){
    await page.locator('.ai-reference').scrollIntoViewIfNeeded();await page.screenshot({path:`docs/results/phase-Y4p/ai-example-${width}.png`});
    await page.evaluate(()=>scrollTo(0,document.getElementById('video').getBoundingClientRect().top+scrollY-90));await page.screenshot({path:`docs/results/phase-Y4p/ai-video-${width}.png`});
   }
  }
 }
 // Route choices with native keyboard.
 await page.goto(base+'00-start.html');await page.locator('input[value=film]').focus();await page.keyboard.press('ArrowDown');check('유형 키보드 선택',await page.locator('[data-route-result]').innerText().then(t=>t.includes('65분')));
 await page.keyboard.press('ArrowDown');check('생성 유형 선택',await page.locator('[data-route-result]').innerText().then(t=>t.includes('80분')));
 // Windows/macOS tabs support arrows, Home, End.
 await page.goto(base+'02-setup.html');const group=page.locator('[data-os-tabs]').first();await group.locator('[data-os-tab]').first().focus();await page.keyboard.press('End');check('OS End',await group.locator('[data-os-tab]').last().getAttribute('aria-selected')==='true');await page.keyboard.press('Home');check('OS Home',await group.locator('[data-os-tab]').first().getAttribute('aria-selected')==='true');await page.keyboard.press('ArrowRight');check('OS 방향키',await group.locator('[data-os-tab]').nth(1).getAttribute('aria-selected')==='true');
 // Prompt copy via Enter, verify actual clipboard text.
 await page.goto(base+'03-script.html');const copy=page.locator('.code-box').first();await copy.locator('.copy-button').focus();await page.keyboard.press('Enter');await page.waitForFunction(()=>document.querySelector('.copy-status')?.textContent==='복사했습니다.');check('프롬프트 키보드 복사',await page.evaluate(()=>navigator.clipboard.readText()).then(t=>t.includes('훅')&&t.includes('30~45초')));
 await page.locator('#faq-1 summary').focus();await page.keyboard.press('Enter');check('FAQ Enter 열기',await page.locator('#faq-1').getAttribute('open')!==null);
 // Cross-page checklist state and reload.
 const item=page.locator('[data-practice-check="3:verify"]');await item.focus();await page.keyboard.press('Space');check('단계 키보드 체크',await item.isChecked());
 await page.goto(base+'e2e.html');check('E2E 체크 공유',await page.locator('[data-practice-check="3:verify"]').isChecked());await page.reload();check('새로고침 복원',await page.locator('[data-practice-check="3:verify"]').isChecked());
 await page.locator('[data-practice-check="3:verify"]').uncheck();await page.goto(base+'03-script.html');check('실습에 역방향 반영',!await page.locator('[data-practice-check="3:verify"]').isChecked());
 await page.goto(base+'08-publish.html');await page.locator('#posted-url').fill('https://example.org/shorts/practice-only');await page.goto(base+'e2e.html');check('주소 기록 공유',await page.locator('#posted-url').inputValue()==='https://example.org/shorts/practice-only');
 // Exact set equality, including sample's differently named keys.
 const original=[];for(const slug of slugs.filter(s=>s!=='e2e')){await page.goto(base+slug+'.html');original.push(...await page.locator('[data-practice-check]').evaluateAll(ns=>ns.map(n=>n.dataset.practiceCheck)));}
 await page.goto(base+'e2e.html');const all=await page.locator('[data-practice-check]').evaluateAll(ns=>ns.map(n=>n.dataset.practiceCheck));check('E2E 키가 전체 실습과 정확히 일치',JSON.stringify([...original].sort())===JSON.stringify([...all].sort()));check('E2E 중복 키 없음',new Set(all).size===all.length);
 // Caption time, extreme case, reset, frame, playback and loop via keyboard.
 await page.goto(base+'06-edit.html');await page.locator('[data-caption-fix]').focus();await page.keyboard.press('Enter');check('자막 끝 복구',await page.locator('[data-caption-result]').innerText().then(t=>t.startsWith('0.0초')));
 await page.locator('[data-caption-bad]').click();check('일찍 끝나는 예',await page.locator('[data-caption-result]').innerText().then(t=>t.includes('5.0초 일찍')));check('지나간 자막 숨김',await page.locator('[data-caption-preview]').evaluate(n=>getComputedStyle(n).visibility==='hidden'));
 const before=Number(await page.locator('#playhead').inputValue());await page.locator('[data-caption-frame]').focus();await page.keyboard.press('Space');check('한 프레임 이동',Number(await page.locator('#playhead').inputValue())>before);await page.waitForTimeout(100);check('프레임 뒤 정지 유지',await page.locator('[data-caption-play]').innerText()==='재생');
 await page.locator('[data-caption-fix]').click();await page.locator('[data-caption-loop]').check();await page.locator('#playhead').fill('5.99');await page.locator('#playhead').dispatchEvent('input');await page.locator('[data-caption-play]').click();await page.waitForTimeout(350);check('구간 반복',Number(await page.locator('#playhead').inputValue())<1);await page.locator('[data-caption-play]').click();
 await page.locator('#caption-end').focus();await page.keyboard.press('End');check('슬라이더 키보드 끝',await page.locator('#caption-end').inputValue()==='12');check('긴 자막 해석',await page.locator('[data-caption-result]').innerText().then(t=>t.includes('늦게')));
 await page.locator('.skip-link').focus();await page.keyboard.press('Enter');check('본문 건너뛰기 키보드',page.url().endsWith('#main'));
 // Resolve all authored links and anchors on actual HTTP pages.
 const inspector=await context.newPage();for(const href of links){const r=await inspector.goto(href);check('링크 '+href.replace(origin,''),r ? r.ok() : inspector.url()===href);const hash=new URL(href).hash;if(hash)check('앵커 '+hash,await inspector.evaluate(h=>Boolean(document.getElementById(decodeURIComponent(h.slice(1)))),hash));}await inspector.close();
 // No persistence promises when storage is disabled.
 const blocked=await browser.newContext();await blocked.addInitScript(()=>{Storage.prototype.setItem=()=>{throw new DOMException('blocked','SecurityError');};});const bp=await blocked.newPage();await bp.goto(base+'e2e.html');check('저장 차단 안내',await bp.locator('[data-practice-status]').innerText().then(t=>t.includes('저장할 수 없습니다')));await bp.locator('[data-practice-check]').first().check();check('저장 차단 시 현재 체크 작동',await bp.locator('[data-practice-check]').first().isChecked());await blocked.close();
 check('콘솔·페이지·HTTP 오류 없음',errors.length===0);
 await fs.writeFile('docs/results/phase-Y4p/browser-check.json',JSON.stringify({scope:'Linux Chromium; all 12 pages; 1280/375/360; light/dark; actual pinned CDN font; no real account UI',passed:checks.length,checks,errors,authoredLinks:links.size,checklistKeys:all.length},null,2));console.log(`${checks.length} checks passed; ${links.size} links; ${all.length} checklist keys`);
} catch(e){await fs.writeFile('docs/results/phase-Y4p/browser-failure.json',JSON.stringify({error:String(e),url:page.url(),checks,errors},null,2));throw e;} finally {await browser.close();}
