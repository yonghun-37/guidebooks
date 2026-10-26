import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='docs/results/phase-B4b', origin='http://127.0.0.1:8864', base=origin+'/site-blog/';
const paths=['06-writing','07-images','08-seo','09-monetize'];
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'}), page=await context.newPage();
const checks=[], errors=[], links=new Set();
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('pageerror',e=>errors.push(String(e)));
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(r.status()+' '+r.url());});
try {
 for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const slug of paths){
  await page.setViewportSize({width,height:1000});await page.goto(base+'chapters/'+slug+'.html');await page.selectOption('[data-theme-select]',theme);await page.evaluate(()=>document.fonts.ready);
  check(`${slug}/${width}/${theme} 넘침0`,await overflow());
  check(`${slug}/${width}/${theme} 장 틀`,await page.locator('[data-block]').count()===9&&await page.locator('.chapter-faq details').count()===5);
  for(const href of await page.locator('a[href]').evaluateAll(ns=>ns.map(n=>n.href).filter(h=>h.startsWith(location.origin))))links.add(href);
  const menu=page.locator('[data-menu-toggle]');await menu.focus();await page.keyboard.press('Enter');check(`${slug}/${width}/${theme} 목차 Enter`,await menu.getAttribute('aria-expanded')==='true');await page.keyboard.press('Escape');check(`${slug}/${width}/${theme} Escape 복귀`,await menu.getAttribute('aria-expanded')==='false'&&await menu.evaluate(n=>n===document.activeElement));
  await page.locator('[data-axis-nav] a').first().focus();await page.keyboard.press('Enter');check(`${slug}/${width}/${theme} 축 이동 초점`,await page.evaluate(()=>document.activeElement.id===location.hash.slice(1)));
  await page.locator('main details').evaluateAll(ns=>ns.forEach(n=>n.open=true));check(`${slug}/${width}/${theme} FAQ 펼침 넘침0`,await overflow());
  await page.locator('.chapter-faq details').evaluateAll(ns=>ns.forEach(n=>n.open=false));
  await page.evaluate(()=>{document.activeElement?.blur();scrollTo(0,0);});await page.screenshot({path:`${out}/${slug}-${width}-${theme}.png`});
  // 각 도구를 같은 폭·테마에서 확인한다. 원본 임베드로 고정 헤더의 가림을 피한다.
  const toolIds={'06-writing':'draft-tool','07-images':'thumbnail-tool','08-seo':'search-tool','09-monetize':'publish-tool'};
  const embed=await context.newPage();await embed.setViewportSize({width,height:1000});await embed.goto(base+`chapters/${slug}.html?embed=${toolIds[slug]}`);await embed.evaluate(t=>document.documentElement.dataset.theme=t,theme);await embed.locator('#'+toolIds[slug]).screenshot({path:`${out}/${slug}-tool-${width}-${theme}.png`});await embed.close();
  for(const q of await page.locator('[data-question]').all()){await q.locator('[data-correct=true]').focus();await page.keyboard.press('Space');check(`${slug}/${width}/${theme} 퀴즈 Space`,await q.locator('[data-feedback]').innerText().then(t=>t.includes('정답입니다')));}
  await page.locator('[data-quiz-reset]').click();check(`${slug}/${width}/${theme} 퀴즈 초기화`,await page.locator('[data-question] button:disabled').count()===0);
 }
 await page.goto(base+'chapters/06-writing.html');
 await page.locator('[data-highlight=fact]').focus();await page.keyboard.press('Space');check('사실 강조만 끄기',await page.locator('mark[data-kind=fact].highlight-off').count()===2&&await page.locator('mark[data-kind=experience].highlight-off').count()===0);
 check('강조 수2',await page.locator('[data-draft-result]').innerText().then(t=>t.startsWith('2가지')));
 await page.locator('#draft-off').focus();await page.keyboard.press('Enter');check('강조 모두 끄기 Enter',await page.locator('mark.highlight-off').count()===6);
 await page.locator('[data-highlight=experience]').check();check('강조 복원',await page.locator('mark[data-kind=experience].highlight-off').count()===0);
 await page.goto(base+'chapters/07-images.html');
 for(const img of await page.locator('img').all()){await img.scrollIntoViewIfNeeded();await img.evaluate(n=>n.decode());}
 check('래스터 실제 크기·치수',await page.locator('img').evaluateAll(ns=>ns.every(n=>n.naturalWidth>0&&Number(n.width)>0&&Math.abs(Number(n.getAttribute('width'))/Number(n.getAttribute('height'))-n.naturalWidth/n.naturalHeight)<.01)));
 await page.fill('#thumb-title','<img src=x onerror=alert(1)>');check('썸네일 입력을 텍스트로 처리',await page.locator('#thumb-output').innerText()==='<img src=x onerror=alert(1)>'&&await page.locator('#thumb-output img').count()===0);
 await page.fill('#thumb-title','');check('빈 제목 안내',await page.locator('#thumb-result').innerText().then(t=>t.includes('입력')));
 await page.locator('#thumb-reset').focus();await page.keyboard.press('Space');check('썸네일 Space 초기화',await page.locator('#thumb-output').innerText()==='지원 제도 신청 전 확인');
 await page.goto(base+'chapters/08-seo.html');
 await page.locator('#search-long').focus();await page.keyboard.press('Enter');check('긴 제목 프리셋 Enter',await page.locator('#search-title').inputValue().then(t=>t.length>60));
 check('모바일 제목 잘림',await page.locator('#search-preview-title').evaluate(n=>n.scrollHeight>n.clientHeight));
 await page.locator('#search-device').focus();await page.keyboard.press('ArrowDown');await page.keyboard.press('Tab');check('기기 선택 키보드',await page.locator('#search-preview').getAttribute('data-device')==='desktop');
 check('PC 줄 수 반영',await page.locator('#search-preview-title').evaluate(n=>getComputedStyle(n).webkitLineClamp)==='1');
 await page.fill('#search-title','<script>alert(1)</script>');check('검색 입력 텍스트 처리',await page.locator('#search-preview-title').innerText()==='<script>alert(1)</script>'&&await page.locator('#search-preview-title script').count()===0);
 await page.fill('#search-title','');await page.fill('#search-description','');check('검색 빈값 안내',await page.locator('[data-search-result]').innerText().then(t=>t.includes('입력')));
 await page.locator('#search-reset').click();check('검색 초기화',await page.locator('#search-device').inputValue()==='mobile');
 for(const width of [360,375,1280]){await page.setViewportSize({width,height:1000});await page.click('#search-long');for(const d of ['mobile','desktop']){await page.selectOption('#search-device',d);check(`검색 ${width}/${d} 긴 값 넘침0`,await overflow());}}
 await page.goto(base+'chapters/09-monetize.html');
 check('초기 확인할 항목4',await page.locator('#publish-actions li').count()===4);
 check('불필요 조건 감춤',!await page.locator('#disclosure-question').isVisible()&&!await page.locator('#ai-question').isVisible());
 await page.selectOption('#check-benefit','yes');await page.selectOption('#check-ai','image');check('답에 따라 분기 표시',await page.locator('#disclosure-question').isVisible()&&await page.locator('#ai-question').isVisible());
 await page.locator('#check-ready').focus();await page.keyboard.press('Space');check('완료 예시 키보드0',await page.locator('#publish-result').innerText().then(t=>t.startsWith('0곳'))&&await page.locator('#publish-actions li').count()===0);
 await page.locator('#check-extreme').focus();await page.keyboard.press('Enter');check('극단값 Enter4',await page.locator('#publish-actions li').count()===4);
 await page.selectOption('#check-benefit','no');await page.selectOption('#check-rights','none');await page.selectOption('#check-ai','none');await page.selectOption('#check-ad','none');check('해당 없음0',await page.locator('#publish-actions li').count()===0&&!await page.locator('#ai-question').isVisible());
 await page.selectOption('#check-ai','text');await page.selectOption('#check-ai-review','no');check('AI 글 검수 분기',await page.locator('#publish-actions').innerText().then(t=>t.includes('숫자·출처·경험')));
 await page.locator('#check-reset').click();check('점검 초기화',await page.locator('#publish-actions li').count()===4);
 const broken=[];
 for(const link of links){const u=new URL(link);const response=await context.request.get(u.href);if(!response.ok())broken.push(link);if(u.hash){const body=await response.text();if(!body.includes(`id="${decodeURIComponent(u.hash.slice(1))}"`))broken.push(link);}}
 check(`내부 링크·앵커 ${links.size}`,broken.length===0);
 const nojs=await browser.newContext({javaScriptEnabled:false});const np=await nojs.newPage();for(const slug of paths){await np.goto(base+'chapters/'+slug+'.html');check(slug+' JS 없어도 본문·FAQ',await np.locator('[data-block]').count()===9&&await np.locator('.chapter-faq details').count()===5);}await nojs.close();
 const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked');}});});const bp=await blocked.newPage();await bp.goto(base+'chapters/09-monetize.html');await bp.click('#check-ready');check('저장 차단 환경 도구 동작',await bp.locator('#publish-result').innerText().then(t=>t.startsWith('0곳')));await blocked.close();
 check('콘솔·페이지·HTTP 오류0',errors.length===0);
 await fs.writeFile(out+'/browser-check.json',JSON.stringify({passed:true,checks:checks.length,pages:paths.length,widths:[1280,375,360],themes:['light','dark'],internalLinks:links.size,errors,details:checks},null,2));
 console.log(`통과 ${checks.length}개 / 4장 × 3폭 × 2테마 / 내부 링크 ${links.size} / 오류 ${errors.length}`);
} catch(error){await fs.writeFile(out+'/browser-check.json',JSON.stringify({passed:false,checks:checks.length,errors,error:String(error)},null,2));throw error;}
finally{await browser.close();}
