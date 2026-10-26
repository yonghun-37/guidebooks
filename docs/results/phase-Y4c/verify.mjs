import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const out='docs/results/phase-Y4c';
const origin=process.env.SITE_ORIGIN || 'http://127.0.0.1:8606';
const base=origin+'/site-shorts/chapters/';
const slugs=['10-templates','11-upload','12-analytics','13-policy','14-plan'];
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
if(process.env.FALLBACK_FONT)await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage(), checks=[], errors=[], links=new Set(), screenshots=[];
page.on('pageerror',error=>errors.push(String(error)));
page.on('console',message=>{if(message.type()==='error')errors.push(message.text());});
page.on('response',response=>{if(response.status()>=400)errors.push(response.status()+' '+response.url());});
page.on('requestfailed',request=>errors.push(request.url()+' '+request.failure()?.errorText));
const check=(label,truth)=>{assert.ok(truth,label);checks.push(label);};
const text=selector=>page.locator(selector).innerText();
const result=()=>text('[data-ops-result]');
const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth);
const go=async slug=>{await page.goto(base+slug+'.html');await page.evaluate(()=>document.fonts.ready);};
const keyboardClick=async selector=>{await page.locator(selector).focus();await page.keyboard.press('Enter');};
const screen=async(name,selector)=>{if(selector)await page.locator(selector).evaluate(e=>e.scrollIntoView({block:'start'}));await page.evaluate(()=>document.activeElement.blur());const path=`${out}/${name}.png`;await page.screenshot({path});screenshots.push(path);};
try {
// 30개 화면 조합. 정적 본문과 펼친 FAQ·동적 도구·실제 생성 링크를 확인한다.
for(const width of [1280,375,360])for(const theme of ['light','dark'])for(const slug of slugs){
 await page.setViewportSize({width,height:1000});await go(slug);
 await page.locator('[data-theme-select]').selectOption(theme);
 check(`가로 넘침 없음 ${slug}/${width}/${theme}`,await overflow());
 check(`실제 문서 제목 ${slug}`,!(await page.title()).includes('준비 중'));
 check('FAQ 5개',await page.locator('.chapter-faq details').count()===5);
 check('퀴즈 3문항',await page.locator('[data-question]').count()===3);
 check('출처 각주 연결',await page.locator('.footnote-ref a').evaluateAll(links=>links.every(a=>document.querySelector(a.getAttribute('href')))));
 await keyboardClick('[data-menu-toggle]');check('목차 열기',await page.locator('#book-menu').isVisible());
 await page.keyboard.press('Escape');check('Escape 목차 닫기·초점',!await page.locator('#book-menu').isVisible()&&await page.locator('[data-menu-toggle]').evaluate(e=>e===document.activeElement));
 await page.locator('.chapter-faq details').evaluateAll(nodes=>nodes.forEach(n=>n.open=true));
 check('FAQ 펼친 뒤 넘침 없음',await overflow());
 const local=await page.locator('a[href]').evaluateAll(nodes=>nodes.map(a=>a.href).filter(h=>h.startsWith(location.origin)));local.forEach(h=>links.add(h));
 if(slug==='10-templates'){await page.locator('#pipe-failure').selectOption('captions');for(let i=0;i<3;i++)await keyboardClick('[data-pipe-next]');}
 if(slug==='11-upload')await keyboardClick('[data-meta-preset="base"]');
 if(slug==='12-analytics'){await page.locator('#curve-case').selectOption('middle');await page.locator('#curve-hypothesis').selectOption('dense');await keyboardClick('[data-curve-suggest]');}
 if(slug==='13-policy')await keyboardClick('[data-policy-preset="risk"]');
 check('동적 도구 펼친 뒤 넘침 없음',await overflow());
 if(theme==='light'&&!process.env.FALLBACK_FONT){await page.evaluate(()=>scrollTo(0,0));await screen(`${slug}-${width}`);await screen(`${slug}-tool-${width}`,slug==='11-upload'?'#metadata-tool':slug==='14-plan'?'#plan-tool':'#simulator');}
 if(theme==='dark'&&width===360&&!process.env.FALLBACK_FONT)await screen(`${slug}-tool-360-dark`,'#simulator');
}
const inspector=await context.newPage();
for(const href of links){const r=await inspector.goto(href);check(`링크 응답 ${href.replace(origin,'')}`,r ? r.status()===200 : inspector.url()===href);const hash=new URL(href).hash;if(hash)check('생성 링크 앵커 '+href,await inspector.evaluate(h=>Boolean(document.getElementById(decodeURIComponent(h.slice(1)))),hash));}
await inspector.close();
await page.setViewportSize({width:360,height:1000});
// 파이프라인: 최초 실패 지점·차단·문제 변경·초기화.
for(const [failure,clicks,stage] of [['voice',2,2],['captions',3,3],['clip',4,4],['sync',5,5],['all',2,2],['none',6,6]]){
 await go('10-templates');await page.locator('#pipe-failure').selectOption(failure);
 for(let i=0;i<clicks;i++)await keyboardClick('[data-pipe-next]');
 check(`파이프라인 ${failure}의 최초 위치`,(await result()).includes(`${stage}단계`));
 check('완료·실패 뒤 다음 단계 차단',await page.locator('[data-pipe-next]').isDisabled());
 check('기대 입력·수정 근거',Boolean((await text('[data-pipe-evidence]')).trim()));
 await keyboardClick('[data-pipe-reset]');check('흐름 초기화',(await result()).includes('0단계'));
}
await page.locator('#pipe-failure').focus();await page.keyboard.press('Home');await page.keyboard.press('ArrowDown');await page.keyboard.press('Enter');check('선택 키보드',await page.locator('#pipe-failure').inputValue()==='voice');
// 승인 샘플 재사용 분기의 120개 입력 조합과 메타데이터 합산.
await go('11-upload');
await keyboardClick('[data-meta-preset="base"]');check('메타데이터·설정 기본 예',(await result()).startsWith('0개'));
for(const audience of ['', 'kids','general','unsure'])for(const ai of ['', 'realistic','music','assist','none','unsure'])for(const music of ['', 'own','library','licensed','unknown']){
 await page.locator('#audience').selectOption(audience);await page.locator('#ai-content').selectOption(ai);await page.locator('#music-rights').selectOption(music);
 const expected=Number(!audience||audience==='unsure')+Number(!ai||ai==='unsure')+Number(!music||music==='unknown');
 check(`업로드 미결 ${audience}/${ai}/${music}`, (await result()).startsWith(expected+'개'));
 check('세 설정 메모 유지',await page.locator('[data-upload-actions] li').count()===3);
}
await keyboardClick('[data-meta-preset="base"]');await page.locator('#meta-title').selectOption('hype');check('장면과 제목 불일치',(await result()).startsWith('1개'));
await keyboardClick('[data-meta-preset="base"]');await page.locator('#meta-visibility').selectOption('schedule');check('예약 시간대 누락',(await result()).startsWith('1개'));
await page.locator('#meta-zone').fill('내 날짜 / 19:00 / Asia/Seoul');check('예약 메모 추가',(await result()).startsWith('0개'));
await page.locator('#meta-description').fill('   ');check('설명 공백',(await result()).startsWith('1개'));
await page.locator('#meta-description').fill('<img src=x onerror=alert(1)>');check('입력이 HTML로 실행되지 않음',await page.locator('#metadata-tool img').count()===0);
await keyboardClick('[data-meta-preset="base"]');await keyboardClick('#upload-answers [type="reset"]');await page.waitForTimeout(40);check('설정 초기화 뒤 두 도구 갱신',(await result()).startsWith('3개')&&(await text('[data-upload-count]')).includes('0/3'));
await keyboardClick('[data-meta-preset="risk"]');check('모두 미정 예',(await result()).startsWith('7개'));
// 곡선: 각 지점·원자료·가설·무자료·낡은 수정안 제거.
await go('12-analytics');
for(const kind of ['opening','middle','replay']){
 await page.locator('#curve-case').selectOption(kind);
 check(`곡선 원자료 ${kind}`,await page.locator('[data-curve-table] tr').count()===7);
 for(const seconds of [0,5,10,15,20,25,30]){
  await page.locator('#curve-time').fill(String(seconds));
  check(`곡선 시점·장면 ${kind}/${seconds}`,(await text('[data-curve-time]')).startsWith(seconds+'초')&&Boolean(await page.locator('[data-curve-frame]').getAttribute('aria-label')));
  check('재생 헤드 위치',Number(await page.locator('[data-curve-head]').getAttribute('x1'))>=45);
 }
 for(const h of ['intro','dense','replay']){await page.locator('#curve-hypothesis').selectOption(h);await keyboardClick('[data-curve-suggest]');check(`곡선 가설 수정안 ${h}`,(await result()).includes('다음 편에서 시험'));}
}
await page.locator('#curve-time').focus();await page.keyboard.press('Home');await page.keyboard.press('ArrowRight');check('곡선 슬라이더 방향키',await page.locator('#curve-time').inputValue()==='5');
check('시점 변경 시 낡은 수정안 제거',!(await result()).includes('다음 편에서 시험'));
await page.locator('#curve-case').selectOption('empty');check('데이터 없음의 판단 차단',await page.locator('#curve-time').isDisabled()&&await page.locator('[data-curve-suggest]').isDisabled()&&(await result()).includes('기다리고'));
check('데이터 없음에서 곡선·표 제거',await page.locator('[data-curve-line]').getAttribute('points')===''&&await page.locator('[data-curve-table] tr').count()===0);
await page.locator('#curve-case').selectOption('middle');check('데이터 복구·가설 초기화',!await page.locator('#curve-time').isDisabled()&&await page.locator('#curve-hypothesis').inputValue()==='');
// 정책 72조합: 각각의 조치가 서로를 지우지 않는다.
await go('13-policy');
for(const origin of ['own','reuse','unknown'])for(const repeat of ['new','mass'])for(const ai of ['assist','realistic','music','unknown'])for(const music of ['own','library','unknown']){
 for(const [id,value]of [['origin',origin],['repeat',repeat],['ai',ai],['music',music]])await page.locator('#policy-'+id).selectOption(value);
 const count=Number(origin!=='own')+Number(repeat==='mass')+Number(ai!=='assist')+Number(music==='unknown');
 check(`정책 독립 조치 ${origin}/${repeat}/${ai}/${music}`,(await result()).startsWith(count+'개'));
 check('정책 네 근거 유지',await page.locator('[data-policy-actions] li').count()===4);
}
await keyboardClick('[data-policy-preset="risk"]');check('정책 극단값',(await result()).startsWith('4개'));
await keyboardClick('[data-policy-preset="base"]');check('직접 제작 예·추가 점검 유지',(await result()).startsWith('0개')&&(await result()).includes('아동용·협찬'));
// 계획: 날짜 30행·예산·잔여·체크/메모·무효 입력·달/윤년 경계.
await go('14-plan');
check('기본 시간 예산',(await result()).startsWith('1,100분'));
check('30행과 날짜 끝',await page.locator('[data-plan-calendar] tbody tr').count()===30&&(await text('[data-plan-calendar] tbody tr:last-child th'))==='2026-11-25');
check('보류 작업 보존',(await text('[data-plan-pending]')).includes('다음 활동일'));
await page.locator('[data-plan-check="0"]').focus();await page.keyboard.press('Space');check('체크의 내보낼 메모 반영',(await page.locator('#plan-copy').inputValue()).includes('완료'));
await keyboardClick('[data-plan-copy]');check('메모 키보드 선택',await page.locator('#plan-copy').evaluate(n=>n.selectionEnd>n.selectionStart));
for(const [id,value]of [['plan-minutes','-1'],['plan-days','8'],['plan-minutes',''],['plan-days','1.5'],['plan-start','']]){
 await keyboardClick('[data-plan-preset="base"]');await page.locator('#'+id).fill(value);
 check(`무효 입력 ${id}/${value}`,await page.locator('[data-plan-calendar] tbody tr').count()===0&&await page.locator('#plan-copy').inputValue()===''&&(await result()).startsWith('—'));
}
await keyboardClick('[data-plan-preset="zero"]');check('0분에 제작 배정 없음',(await result()).startsWith('0분')&&(await text('[data-plan-calendar]')).includes('제작 배정 없음'));
await keyboardClick('[data-plan-preset="base"]');await page.locator('#plan-days').fill('0');check('활동일 0일',(await result()).startsWith('0분')&&!((await text('[data-plan-calendar]')).includes('가상 50분')));
await keyboardClick('[data-plan-preset="base"]');await page.locator('#plan-minutes').fill('10');check('검수만 남는 시간',(await result()).startsWith('0분'));
await keyboardClick('[data-plan-preset="base"]');await page.locator('#plan-days').fill('7');await page.locator('#plan-minutes').fill('480');check('최대 시간·작업 소진', (await result()).startsWith('14,100분')&&(await text('[data-plan-pending]')).includes('배정이 끝났습니다'));
await page.locator('#plan-start').fill('2028-02-28');check('윤년 날짜', (await text('[data-plan-calendar] tbody tr:nth-child(2) th'))==='2028-02-29'&&(await text('[data-plan-calendar] tbody tr:nth-child(3) th'))==='2028-03-01');
await page.locator('#plan-start').fill('2099-12-01');check('최대 날짜 끝', (await text('[data-plan-calendar] tbody tr:last-child th'))==='2099-12-30');
// 모든 장 퀴즈: 오답 피드백·초기화·정답 점수, FAQ 실제 키보드.
for(const slug of slugs){
 await go(slug);await page.locator('.chapter-faq details').first().locator('summary').focus();await page.keyboard.press('Enter');check('FAQ 키보드 열기',await page.locator('.chapter-faq details').first().getAttribute('open')!==null);
 await page.locator('[data-question]').first().locator('[data-correct="false"]').focus();await page.keyboard.press('Enter');check('오답 설명',await page.locator('[data-feedback]').first().isVisible());
 await keyboardClick('[data-quiz-reset]');
 for(const q of await page.locator('[data-question]').all()){await q.locator('[data-correct="true"]').focus();await page.keyboard.press('Enter');}
 check(`퀴즈 점수 ${slug}`,(await text('[data-quiz-score]')).includes('3문항 정답'));
 await page.locator('.skip-link').focus();await page.keyboard.press('Enter');check('본문 건너뛰기',new URL(page.url()).hash==='#main');
}
// 저장소 차단·JS 없음에서도 본문과 정적 대안을 읽을 수 있다.
const blocked=await browser.newContext();await blocked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('storage blocked');}});});const bp=await blocked.newPage();bp.on('pageerror',e=>errors.push(String(e)));
for(const slug of slugs){await bp.goto(base+slug+'.html');check('저장소 차단시 도구 유지',await bp.locator('[data-ops-result]').count()>0);}
await blocked.close();
const offline=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:1000}});const np=await offline.newPage();for(const slug of slugs){await np.goto(base+slug+'.html');check('JS 없이 FAQ·본문 유지',await np.locator('.chapter-faq details').count()===5);check('JS 없이 가로 넘침 없음',await np.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}await offline.close();
check('콘솔·페이지·요청 오류 0',errors.length===0);
if(!process.env.FALLBACK_FONT){for(const width of [1280,375,360]){await page.setViewportSize({width,height:1000});await go('11-upload');await keyboardClick('[data-meta-preset="base"]');await screen(`11-upload-branches-${width}`,'#upload-tool');await go('12-analytics');await page.locator('#curve-case').selectOption('middle');await page.locator('#curve-hypothesis').selectOption('dense');await keyboardClick('[data-curve-suggest]');await screen(`12-analytics-decision-${width}`,'#curve-hypothesis');}}
const name=process.env.FALLBACK_FONT?'fallback-browser-check.json':'browser-check.json';
await fs.writeFile(`${out}/${name}`,JSON.stringify({checks:checks.length,passed:checks,errors,internal_links:links.size,screenshots,font:process.env.FALLBACK_FONT?'system fallback':'pinned CDN enabled',scope:'Chromium, 1280/375/360px, light/dark; actual keyboard controls; no account login or posting'},null,2)+'\n');
console.log(`${checks.length} checks PASS; ${links.size} links; ${screenshots.length} screenshots; ${errors.length} errors`);
} catch(error) {await fs.writeFile(`${out}/browser-failure.json`,JSON.stringify({message:String(error),checks:checks.length,errors,url:page.url()},null,2)+'\n');throw error;}finally{await browser.close();}
