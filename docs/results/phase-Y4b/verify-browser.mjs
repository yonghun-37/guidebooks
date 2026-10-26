import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const output=new URL('./',import.meta.url);
const origin=process.env.SITE_URL||'http://127.0.0.1:18634/site-shorts/';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const ctx=await browser.newContext({reducedMotion:'reduce'});
if(!process.env.FONT_NETWORK)await ctx.route('https://cdn.jsdelivr.net/**',route=>route.fulfill({contentType:'text/css',body:''}));
const page=await ctx.newPage(),checks=[],errors=[];
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
page.on('pageerror',e=>errors.push(String(e)));
page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
const chapters=['06-scenes','07-editing','08-captions','09-export'];
const result=()=>page.locator('[data-sim-result]').innerText();
const set=async(id,value)=>{await page.locator('#'+id).fill(String(value));};
const goto=async slug=>{await page.goto(origin+'chapters/'+slug+'.html');await page.evaluate(()=>document.fonts.ready);};
const overflow=async name=>check('가로 넘침 없음 '+name,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
try {
for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const chapter of chapters){
 await page.setViewportSize({width,height:1100});await goto(chapter);
 await page.locator('[data-theme-select]').selectOption(theme);
 await overflow(`${width}/${theme}/${chapter}`);
 check('9블록 '+chapter,await page.locator('[data-block]').count()===9);
 check('FAQ5 '+chapter,await page.locator('.chapter-faq details').count()===5);
 check('정리3 '+chapter,await page.locator('#summary li').count()===3);
 await page.locator('.chapter-faq summary').first().focus();await page.keyboard.press('Enter');
 check('FAQ 키보드 '+chapter,await page.locator('.chapter-faq details').first().getAttribute('open')!==null);
 await page.locator('[data-menu-toggle]').click();await page.keyboard.press('Escape');
 check('목차 Escape '+chapter,await page.locator('#book-menu').isHidden());
 const anchors=await page.locator('main a[href^="#"]').evaluateAll(els=>els.map(el=>el.hash.slice(1)));
 check('내부 앵커 '+chapter,await page.evaluate(ids=>ids.every(id=>document.getElementById(id)),anchors));
 if(theme==='light'){
  await page.locator('#simulator').scrollIntoViewIfNeeded();
  await page.evaluate(()=>document.activeElement?.blur());
  await page.locator('.production-tool').screenshot({style:'.site-header,.skip-link { visibility: hidden !important; }',path:new URL(`${chapter}-${width}.png`,output).pathname});
  if(width===1280){await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:new URL(`${chapter}-opening.png`,output).pathname});}
 }
}
await page.setViewportSize({width:1280,height:1100});
await goto('06-scenes');await page.locator('#simulator').scrollIntoViewIfNeeded();
check('구도 기본 가림0',(await result()).includes('0곳'));
await page.locator('[data-scene-preset="edge"]').click();
check('가장자리 가림 경고',!(await result()).includes('0곳'));
await page.locator('#show-ui').uncheck();check('가림 숨김 안내',(await result()).includes('숨겨져'));
await page.locator('[data-scene-preset="base"]').click();
await page.locator('#subject-x').focus();await page.keyboard.press('ArrowRight');
check('구도 키보드',await page.locator('#subject-x').inputValue()==='51');
await page.locator('#shot').selectOption('detail');
check('가까운 구도',await page.locator('[data-subject]').getAttribute('transform').then(t=>t.includes('1.35')));

await goto('07-editing');await page.locator('#simulator').scrollIntoViewIfNeeded();
check('타임라인 기본 동기',(await result()).includes('0.0초'));
check('4개 트랙',await page.locator('.track-lane').count()===4);
await page.locator('[data-edit-preset="early"]').click();
check('자막 먼저 끝남',(await result()).includes('-2.0초'));
check('7초 자막 공백',(await page.locator('[data-edit-caption]').innerText())==='');
await page.locator('[data-edit-frame="1"]').focus();await page.keyboard.press('Enter');
check('프레임 이동',await page.locator('[data-edit-clock]').innerText().then(t=>t.startsWith('7.03')));
await set('caption-end',8);check('자막 복구',(await result()).includes('0.0초'));
await set('caption-start',8);check('뒤집힌 자막 시간',(await result()).includes('—'));
check('무효 입력 재생 불가',await page.locator('[data-edit-play]').isDisabled());
await set('caption-start',4);await set('voice-start',1);
check('음성 위치 이동',(await result()).includes('-1.0초'));
await set('music-end',6);
check('음악 길이 적용',await page.locator('[data-track="music"]').innerText().then(t=>t.includes('6.0')));
await set('voice-start','');check('빈 입력 과거 결과 제거',(await result()).includes('—'));
await set('voice-start',-1);check('음수 입력 거부',(await result()).includes('—'));
await set('voice-start',5);check('상한 입력 거부',(await result()).includes('—'));
await page.locator('[data-edit-preset="base"]').click();
await set('loop-start',8);await set('loop-end',4);
check('반복 역순 거부',(await result()).includes('—'));
await set('loop-start',4);await set('loop-end',4.2);await page.locator('#loop-on').check();
await page.locator('[data-edit-play]').focus();await page.keyboard.press('Enter');await page.waitForTimeout(600);
const loopTime=await page.locator('[data-edit-clock]').innerText();check('구간 반복 유지',Number.parseFloat(loopTime)>=4&&Number.parseFloat(loopTime)<4.21);
await page.keyboard.press('Enter');check('키보드 정지',await page.locator('[data-edit-play]').getAttribute('aria-pressed')==='false');
await page.locator('#loop-on').uncheck();await page.locator('[data-edit-home]').click();
await page.locator('#edit-seek').focus();await page.keyboard.press('End');
check('재생 헤드 End',await page.locator('[data-edit-clock]').innerText().then(t=>t.startsWith('12.00')));
await page.keyboard.press('Home');check('재생 헤드 Home',await page.locator('[data-edit-clock]').innerText().then(t=>t.startsWith('0.00')));
await page.locator('[data-edit-play]').click();await page.locator('#question').scrollIntoViewIfNeeded();await page.waitForTimeout(200);
check('화면 밖 정지',await page.locator('[data-edit-play]').getAttribute('aria-pressed')==='false');

await goto('08-captions');await page.locator('#simulator').scrollIntoViewIfNeeded();
check('기본 글자속도',(await result()).includes('2.3글자/초'));
await page.locator('[data-caption-preset="fast"]').click();
check('긴 자막 가림',(await result()).includes('겹치거나'));
await page.locator('[data-caption-preset="base"]').click();
await set('caption-duration',1);check('먼저 끝나는 자막',(await result()).includes('먼저 사라집니다'));
await page.locator('[data-caption-play]').click();await page.waitForTimeout(1200);
check('실제 자막 사라짐',await page.locator('[data-caption-demo]').evaluate(el=>getComputedStyle(el).visibility)==='hidden');
await page.locator('[data-caption-show]').click();check('정지 복원',await page.locator('[data-caption-demo]').evaluate(el=>getComputedStyle(el).visibility)==='visible');
await set('caption-duration','');check('빈 시간 거부',(await result()).includes('—'));
await set('caption-duration',0);check('0시간 거부',(await result()).includes('—'));
await page.locator('[data-caption-preset="base"]').click();
await page.locator('#caption-copy').fill('');check('빈 문장 거부',(await result()).includes('—'));
await page.locator('[data-caption-preset="base"]').click();await page.locator('#caption-contrast').selectOption('plain');
check('낮은 대비 안내',(await result()).includes('배경과 섞입니다'));
await page.locator('#caption-size').focus();await page.keyboard.press('ArrowRight');
check('자막 크기 키보드',await page.locator('#caption-size').inputValue()==='65');
await page.locator('#caption-y').focus();await page.keyboard.press('End');
check('자막 위치 키보드',await page.locator('#caption-y').inputValue()==='92');

await goto('09-export');await page.locator('#simulator').scrollIntoViewIfNeeded();
check('기본 크기 계산',(await result()).includes('12MB'));
const hash=()=>page.locator('#quality-processed').evaluate(el=>el.toDataURL());
const base=await hash();await page.locator('#export-size').selectOption('540');check('해상도 시각 변화',base!==await hash());
await page.locator('#export-size').selectOption('1080');await page.locator('#export-rate').selectOption('2');
check('압축 시각 변화',base!==await hash());check('낮은 데이터 계산',(await result()).includes('3MB'));
await page.locator('[data-quality-preset="base"]').click();
await page.locator('[data-quality-step]').focus();await page.keyboard.press('Enter');
check('30fps 한 프레임',await page.locator('[data-quality-clock]').innerText().then(t=>t.startsWith('0.03')));
await page.locator('[data-quality-preset="base"]').click();await page.locator('#export-fps').selectOption('60');
await page.locator('[data-quality-step]').click();check('60fps 한 프레임',await page.locator('[data-quality-clock]').innerText().then(t=>t.startsWith('0.02')));
await page.locator('[data-quality-play]').click();await page.waitForTimeout(150);await page.locator('[data-quality-play]').click();
check('화질 재생 정지',await page.locator('[data-quality-play]').getAttribute('aria-pressed')==='false');

for(const chapter of chapters){await goto(chapter);for(const q of await page.locator('[data-question]').all()){
 await q.locator('[data-correct="true"]').click();check('퀴즈 정답 '+chapter,await q.locator('[data-feedback]').innerText().then(t=>t.includes('정답입니다')));
}await page.locator('[data-quiz-reset]').click();check('퀴즈 초기화 '+chapter,await page.locator('[data-feedback]:not([hidden])').count()===0);}
// 저장이 금지되어도 도구와 테마/퀴즈는 동작한다.
await ctx.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError');}});});
for(const chapter of chapters){await goto(chapter);await overflow('저장 차단 '+chapter);check('저장 차단 결과 '+chapter,(await result()).length>0);}
const nojs=await browser.newContext({javaScriptEnabled:false});const nj=await nojs.newPage();
for(const chapter of chapters){await nj.goto(origin+'chapters/'+chapter+'.html');check('JS 꺼도 본문 '+chapter,await nj.locator('h1').innerText().then(Boolean));check('JS 꺼도 안내 '+chapter,await nj.locator('noscript').isVisible());}
await nojs.close();
check('콘솔·페이지·HTTP 오류0',errors.length===0);
await fs.writeFile(new URL('browser-check.json',output),JSON.stringify({checks:checks.length,errors,fontNetwork:!!process.env.FONT_NETWORK,details:checks},null,2));
console.log(JSON.stringify({checks:checks.length,errors}));
} catch(error){await fs.writeFile(new URL('browser-failure.json',output),JSON.stringify({checks:checks.length,errors,error:String(error)},null,2));throw error;} finally {await browser.close();}
