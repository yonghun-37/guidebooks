import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'});
await context.route('https://cdn.jsdelivr.net/**',r=>r.fulfill({contentType:'text/css',body:''}));
const page=await context.newPage(), checks=[],errors=[];
const check=(label,truth)=>{assert.ok(truth,label);checks.push(label);};
page.on('pageerror',e=>errors.push(String(e)));
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
const base=process.env.SITE_URL||'http://127.0.0.1:8589/shorts/';
const result=()=>page.locator('[data-sim-result]').innerText();
const count=()=>page.locator('[data-upload-count]').innerText();
const actions=()=>page.locator('[data-upload-actions]').innerText();
try {
 await page.goto(base+'chapters/02-revenue.html');
 check('참고 기본값', /US\$185\.00/.test(await result()));
 await page.locator('#views').fill('10000');
 check('유효 1만 회', /US\$1\.85/.test(await result()));
 await page.locator('#rpm').fill('0.5');
 check('내 RPM 입력', /US\$5\.00/.test(await result()));
 await page.locator('#views').fill('0');
 check('0회', /US\$0\.00/.test(await result()));
 for (const [field,value] of [['#views','-1'],['#views','1.5'],['#views',''],['#views','100000000001'],['#rpm','-0.1'],['#rpm',''],['#rpm','1000001']]) {
  await page.locator('[data-rpm-preset="base"]').click();
  await page.locator(field).fill(value);
  check(`무효 입력 ${field}:${value}`,/입력값을 확인/.test(await result()) && await page.locator(field).getAttribute('aria-invalid')==='true');
  check('무효 입력에 이전 금액 없음', !/US\$185/.test(await result()));
 }
 await page.locator('[data-rpm-preset="base"]').click();
 await page.locator('#monetized').selectOption('no');
 check('광고 미가입은 0',/US\$0\.00/.test(await result()) && /동의 전/.test(await result()));
 await page.locator('[data-rpm-preset="zero"]').click();
 check('극단값 프리셋',/US\$0\.00/.test(await result()));
 await page.locator('[data-rpm-preset="base"]').click();
 await page.locator('#views').focus();await page.keyboard.press('ArrowUp');
 check('숫자 입력 키보드',await page.locator('#views').inputValue()==='1000001');
 await page.locator('[data-axis-nav] a').first().focus();await page.keyboard.press('Enter');
 check('축 이동과 초점',await page.evaluate(()=>location.hash==='#ads'&&document.activeElement.id==='ads'));
 for (const question of await page.locator('[data-question]').all()) {
  await question.locator('[data-correct="true"]').focus();await page.keyboard.press('Enter');
  check('퀴즈 키보드 정답',/정답입니다/.test(await question.locator('[data-feedback]').innerText()));
 }
 check('퀴즈 3문항 채점',/3문항 정답/.test(await page.locator('[data-quiz-score]').innerText()));
 await page.locator('[data-quiz-reset]').click();check('퀴즈 초기화',/0문항 풀이/.test(await page.locator('[data-quiz-score]').innerText()));
 await page.goto(base+'chapters/02-revenue.html#faq-4');
 check('FAQ 직접 링크 펼치기',await page.locator('#faq-4').evaluate(n=>n.open));
 await page.goto(base+'practice/08-publish.html');
 check('미응답 기본값',await count()==='0/3개 답변');
 await page.locator('#audience').selectOption('kids');
 check('부분 응답',await count()==='1/3개 답변');
 for(const audience of ['kids','general','unsure']) for(const ai of ['realistic','music','assist','none','unsure']) for(const music of ['own','library','licensed','unknown']) {
  await page.locator('#audience').selectOption(audience);await page.locator('#ai-content').selectOption(ai);await page.locator('#music-rights').selectOption(music);
  const unresolved=Number(audience==='unsure')+Number(ai==='unsure')+Number(music==='unknown');
  check(`독립 분기 ${audience}/${ai}/${music}`, await count()===(unresolved?`공개 전 확인 ${unresolved}개`:'3개 설정 메모 준비'));
  const text=await actions();
  check('필요한 설정 안내', text.includes(audience==='kids'?'아동용 예':audience==='general'?'아동용 아니요':'먼저 판단') && text.includes(['realistic','music'].includes(ai)?'AI 사용: 예':ai==='unsure'?'AI 사용 방식':'AI 사용: 선택한 조건만이라면 아니요'));
 }
 await page.locator('#audience').selectOption('general');await page.locator('#ai-content').selectOption('realistic');await page.locator('#music-rights').selectOption('unknown');
 check('AI 표시로 음악권리 해소 안 됨', /공개 전 확인 1개/.test(await count())&&/사용권 확인 전에는 공개를 보류/.test(await actions()));
 await page.locator('button[type="reset"]').focus();await page.keyboard.press('Enter');
 await page.waitForFunction(()=>document.querySelector('#audience').value===''&&document.querySelector('[data-upload-count]').textContent==='0/3개 답변');
 check('분기 키보드 초기화',await count()==='0/3개 답변');
 await page.locator('#platform-win-tab').focus();await page.keyboard.press('ArrowRight');
 check('macOS 방향키',await page.locator('#platform-mac-tab').getAttribute('aria-selected')==='true' && await page.locator('#platform-mac').isVisible());
 await page.keyboard.press('End');check('모바일 End 키',await page.locator('#platform-mobile-tab').getAttribute('aria-selected')==='true' && await page.locator('#platform-mobile').isVisible());
 await page.keyboard.press('Home');check('Windows Home 키',await page.locator('#platform-win-tab').getAttribute('aria-selected')==='true');
 await page.locator('[data-practice-check]').first().check();await page.locator('#posted-url').fill('https://www.youtube.com/shorts/example');await page.reload();
 check('체크·주소 복원',await page.locator('[data-practice-check]').first().isChecked() && await page.locator('#posted-url').inputValue()==='https://www.youtube.com/shorts/example');
 check('ReelsBook 저장과 분리',await page.evaluate(()=>localStorage.getItem('reelsbook:practice:v1')===null));
 await page.locator('#posted-url').fill('https://www.youtube.com/shorts/second');
 check('입력 직후 저장 안내',/주소를 기록했습니다/.test(await page.locator('[data-practice-field-status]').innerText()));
 await page.locator('[data-practice-reset]').click();check('기록 삭제',!await page.locator('[data-practice-check]').first().isChecked()&&await page.locator('#posted-url').inputValue()==='');
 check('기록 삭제 후 이전 저장 문구 제거',await page.locator('[data-practice-field-status]').innerText()==='');
 // Stored fields are plain strings, never interpreted as HTML.
 await page.evaluate(()=>localStorage.setItem('shortsbook:practice:v1','{broken'));await page.reload();
 check('손상 저장값',await page.locator('#posted-url').inputValue()==='');
 await page.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked storage');}}));await page.reload();
 check('저장 차단 안내',/저장할 수 없습니다/.test(await page.locator('[data-practice-status]').innerText()));
 await page.locator('#audience').selectOption('general');check('저장 차단 중 분기 사용',await count()==='1/3개 답변');
 check('콘솔·페이지 오류 0',errors.length===0);
 await fs.writeFile('docs/results/phase-Y3/tools-check.json',JSON.stringify({checks:checks.length,passed:checks,errors},null,2)+'\n');
 console.log(`${checks.length} interaction checks PASS, errors ${errors.length}`);
} finally { await browser.close(); }
