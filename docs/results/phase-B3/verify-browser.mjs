import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='docs/results/phase-B3', origin='http://127.0.0.1:8623', base=origin+'/site-blog/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'}), page=await context.newPage();
const checks=[], errors=[], links=new Set();
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('pageerror',e=>errors.push(String(e)));
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(r.status()+' '+r.url());});
const paths=(await fs.readdir('site-blog')).filter(p=>p.endsWith('.html'));
for(const d of ['chapters','practice'])for(const p of await fs.readdir('site-blog/'+d))if(p.endsWith('.html'))paths.push(d+'/'+p);
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
try {
 for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const path of paths){
  await page.setViewportSize({width,height:1000});await page.goto(base+path);await page.locator('[data-theme-select]').selectOption(theme);await page.evaluate(()=>document.fonts.ready);
  check(`${path}/${width}/${theme} 넘침0`,await overflow());
  const menu=page.locator('[data-menu-toggle]');await menu.focus();await page.keyboard.press('Enter');check(`${path}/${width}/${theme} 목차 Enter`,await menu.getAttribute('aria-expanded')==='true');
  await page.keyboard.press('Escape');check(`${path}/${width}/${theme} Escape 복귀`,await menu.getAttribute('aria-expanded')==='false'&&await menu.evaluate(n=>n===document.activeElement));
  for(const href of await page.locator('a[href]').evaluateAll(ns=>ns.map(n=>n.href).filter(h=>h.startsWith(location.origin))))links.add(href);
  if(['index.html','chapters/02-revenue.html','practice/07-publish.html'].includes(path)){
   await page.evaluate(()=>{document.activeElement?.blur();scrollTo(0,0);});await page.screenshot({path:`${out}/${path.replaceAll('/','-').replace('.html','')}-${width}-${theme}.png`});
   if(path==='chapters/02-revenue.html'){
    // 원본 임베드에는 고정 헤더가 없으므로 긴 도구를 가리지 않고 캡처한다.
    const embedded=await context.newPage();await embedded.setViewportSize({width,height:1000});await embedded.goto(base+'chapters/02-revenue.html?embed=revenue-tool');
    await embedded.evaluate(t=>document.documentElement.dataset.theme=t,theme);
    await embedded.locator('#revenue-tool').screenshot({path:`${out}/calculator-${width}-${theme}.png`});await embedded.close();
    await page.selectOption('#calc-mode','affiliate');check(`${width}/${theme} 제휴 넘침0`,await overflow());
   }
   if(path==='practice/07-publish.html'){
    for(const platform of ['naver','tistory']){
     await page.locator(`#tab-${platform}`).click();
     for(const device of ['pc','mobile']){
      await page.locator(`#tab-${platform}-${device}`).click();check(`${width}/${theme}/${platform}/${device} 패널`,await page.locator(`#panel-${platform}-${device}`).isVisible());
      check(`${width}/${theme}/${platform}/${device} 넘침0`,await overflow());
     }
    }
    await page.locator('#tab-naver').click();await page.locator('#tab-naver-pc').click();
    await page.locator('#publish').screenshot({path:`${out}/publish-tabs-${width}-${theme}.png`});
   }
  }
  await page.locator('main details').evaluateAll(ns=>ns.forEach(n=>n.open=true));check(`${path}/${width}/${theme} FAQ 펼침 넘침0`,await overflow());
 }
 console.log(`화면 확인 ${checks.length}`);
 await page.goto(base+'index.html');
 const data=await page.evaluate(()=>({theory:BlogBook.chapters,practice:BlogBook.practice,tracks:BlogBook.tracks}));
 check('이론 13 + 실험실·용어집',data.theory.length===15);
 check('실습 0~10 + E2E',data.practice.length===12);
 check('장 샘플 두 개만', [...data.theory,...data.practice].filter(c=>c.status==='샘플').length===2);
 check('나머지 장 준비중',[...data.theory,...data.practice].filter(c=>c.status!=='샘플').every(c=>c.status==='준비중'));
 await page.getByRole('link',{name:'오늘 첫 글 발행까지: 실습편 시작 →'}).click();check('표지 실습 시작',page.url().endsWith('/practice/00-start.html'));
 await page.goto(base+'chapters/pending.html?chapter=03-ai-tools');check('준비중 장 이름',await page.locator('h1').innerText().then(t=>t.includes('AI 도구 지도')));
 await page.goto(base+'practice/pending.html?chapter=08-search');check('준비중 실습 이름',await page.locator('h1').innerText().then(t=>t.includes('검색 등록')));
 await page.goto(base+'chapters/02-revenue.html');
 check('광고 참고 계산',await page.locator('#calc-result').innerText()==='US$29.70');
 await page.fill('#calc-visitors','2000');check('광고 두 배',await page.locator('#calc-result').innerText()==='US$59.40');
 await page.selectOption('#calc-approved','no');check('광고 미승인0',await page.locator('#calc-result').innerText()==='US$0.00');
 await page.getByRole('button',{name:'제휴 가상 예',exact:true}).click();check('제휴 가상9000',await page.locator('#calc-result').innerText()==='9,000원');
 await page.fill('#calc-cancel','100');check('전량 취소0',await page.locator('#calc-result').innerText()==='0원');
 await page.fill('#calc-cancel','101');check('초과 비율 거부',await page.locator('#calc-result').innerText()==='입력 확인');
 await page.getByRole('button',{name:'개인 RPM 참고 예',exact:true}).click();
 for(const bad of ['', '-1']){await page.fill('#calc-rpm',bad);check(`RPM ${bad||'빈값'} 거부`,await page.locator('#calc-result').innerText()==='입력 확인');}
 await page.getByRole('button',{name:'개인 RPM 참고 예',exact:true}).click();await page.selectOption('#calc-currency','KRW');check('통화 전환 재입력',await page.locator('#calc-result').innerText()==='입력 확인');
 await page.fill('#calc-rpm','1000');check('가상 원화30000',await page.locator('#calc-result').innerText()==='30,000원');
 await page.selectOption('#calc-base','visits');check('방문 분모 표시',await page.locator('#calc-pages-label').innerText()==='페이지/방문 · 가상');
 await page.locator('[data-preset=zero]').focus();await page.keyboard.press('Space');check('극단값 키보드0',await page.locator('#calc-result').innerText()==='0원');
 await page.locator('[data-preset=reference]').focus();await page.keyboard.press('Enter');check('프리셋 Enter 복원',await page.locator('#calc-result').innerText()==='US$29.70');
 await page.locator('[data-axis-nav] a').first().focus();await page.keyboard.press('Enter');check('수익 축 링크 초점',await page.evaluate(()=>document.activeElement.id==='ads'));
 for(const q of await page.locator('[data-question]').all()){await q.locator('[data-correct=true]').focus();await page.keyboard.press('Space');check('퀴즈 Space',await q.locator('[data-feedback]').innerText().then(t=>t.includes('정답입니다')));}
 await page.locator('[data-quiz-reset]').click();check('퀴즈 초기화',await page.locator('[data-question] button:disabled').count()===0);
 await page.goto(base+'practice/07-publish.html');
 await page.locator('#tab-naver').focus();await page.keyboard.press('ArrowRight');check('플랫폼 탭 화살표',await page.locator('#tab-tistory').getAttribute('aria-selected')==='true');
 await page.locator('#tab-tistory-pc').focus();await page.keyboard.press('End');check('기기 탭 End',await page.locator('#panel-tistory-mobile').isVisible());
 await page.keyboard.press('Home');check('기기 탭 Home',await page.locator('#panel-tistory-pc').isVisible());
 await page.locator('#tab-tistory').focus();await page.keyboard.press('Home');check('부모 탭 독립',await page.locator('#panel-naver-pc').isVisible()&&!await page.locator('#panel-tistory-pc').isVisible());
 await page.fill('#posted-url','https://example.com/my-post');await page.locator('[data-practice-check="7:url"]').check();await page.reload();check('공개 주소 복원',await page.locator('#posted-url').inputValue()==='https://example.com/my-post');check('확인 기록 복원',await page.locator('[data-practice-check="7:url"]').isChecked());
 check('다른 책 저장 키 없음',await page.evaluate(()=>Object.keys(localStorage).every(k=>!k.startsWith('shortsbook:')&&!k.startsWith('reelsbook:'))));
 await page.locator('[data-practice-reset]').click();await page.reload();check('기록 삭제',await page.locator('#posted-url').inputValue()===''&&!await page.locator('[data-practice-check="7:url"]').isChecked());
 await page.goto(base+'lab.html');const frame=page.frameLocator('#sim-frame');await frame.locator('#calc-result').waitFor({state:'visible'});check('실험실 원본 로드',await frame.locator('#calc-result').innerText()==='US$29.70');
 await page.selectOption('[data-theme-select]','dark');await page.waitForFunction(()=>document.querySelector('iframe').contentDocument.documentElement.dataset.theme==='dark');check('실험실 테마 연동',true);
 await page.setViewportSize({width:360,height:1000});check('실험실 모바일 넘침0',await frame.locator('html').evaluate(n=>n.scrollWidth<=innerWidth));
 const broken=[];
 for(const link of links){const u=new URL(link);const response=await context.request.get(u.href);if(!response.ok())broken.push(link);if(u.hash){const text=await response.text();if(!text.includes(`id="${decodeURIComponent(u.hash.slice(1))}"`))broken.push(link);}}
 check(`동적 내부 링크·앵커 ${links.size}`,broken.length===0);
 const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked');}});});const bp=await blocked.newPage();await bp.goto(base+'practice/07-publish.html');await bp.fill('#posted-url','https://example.com/blocked');check('저장 차단 안내',await bp.locator('[data-practice-field-status]').innerText().then(t=>t.includes('저장할 수 없습니다')));await bp.close();await blocked.close();
 const nojs=await browser.newContext({javaScriptEnabled:false});const np=await nojs.newPage();await np.goto(base+'index.html');check('JS 없는 목차',await np.locator('[data-chapter-toc] a').count()>20);await np.goto(base+'practice/07-publish.html');check('JS 없는 모든 기기 안내',await np.locator('#panel-tistory-mobile').isVisible()&&await np.locator('#panel-naver-pc').isVisible());await np.close();await nojs.close();
 check('콘솔·페이지·HTTP 오류0',errors.length===0);
 await fs.writeFile(out+'/browser-check.json',JSON.stringify({passed:true,checks:checks.length,pages:paths.length,widths:[1280,375,360],themes:['light','dark'],internalLinks:links.size,errors,details:checks},null,2));
 console.log(`통과: ${checks.length}개, ${paths.length}페이지, 링크 ${links.size}, 오류 ${errors.length}`);
} catch(error){await fs.writeFile(out+'/browser-check.json',JSON.stringify({passed:false,checks:checks.length,errors,error:String(error)},null,2));throw error;}
finally{await browser.close();}
