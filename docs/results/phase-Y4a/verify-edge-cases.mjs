import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const context=await browser.newContext({reducedMotion:'reduce'}),page=await context.newPage(),checks=[],errors=[];
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
const base='http://127.0.0.1:8594/site-shorts/chapters/';
page.on('pageerror',e=>errors.push(e.message));
try{
 await page.goto(base+'01-map.html');await page.locator('#pipeline-empty').click();
 check('전체 누락 3',/3개 누락/.test(await page.locator('#pipeline-result').innerText()));
 for(const stage of ['script','sound','scene','edit','export','publish']){await page.locator('#stage').selectOption(stage);check('단계 '+stage,Boolean(await page.locator('#stage-note').innerText()));check('누락 상태 유지 '+stage,/3개 누락/.test(await page.locator('#pipeline-result').innerText()));}
 await page.goto(base+'03-hook.html');await page.locator('#hook-play').click();await page.waitForTimeout(3300);
 check('3초 종료 정지',await page.locator('#hook-play').getAttribute('aria-pressed')==='false'&&await page.locator('#hook-time').inputValue()==='3');
 await page.locator('#hook-extreme').click();check('빈 문장 프리셋',/첫 문장 없음/.test(await page.locator('#hook-line').innerText()));
 await page.locator('#hook-choice').selectOption('specific');check('문장 복구',/케이블/.test(await page.locator('#hook-line').innerText()));
 await page.locator('#hook-play').click();await page.waitForTimeout(160);await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));await page.waitForTimeout(180);
 check('그림 화면 밖 정지',await page.locator('#hook-play').getAttribute('aria-pressed')==='false');
 await page.goto(base+'04-script.html');
 await page.locator('#script-text').fill('가 나.\n다');await page.locator('#sample-chars').fill('5');await page.locator('#sample-seconds').fill('1');await page.locator('#pause-seconds').fill('0');
 check('공백·기호 포함 줄바꿈 제외 5자',/^5자/.test(await page.locator('#script-count').innerText()));
 check('샘플 읽기 공식 1초',/1\.0초/.test(await page.locator('#script-result').innerText()));
 for(const [id,value]of [['sample-chars','0'],['sample-chars','1.5'],['sample-chars','20001'],['sample-seconds','-1'],['sample-seconds','3601'],['pause-seconds',''],['pause-seconds','3601']]){
  await page.locator('#script-reset').click();await page.locator('#'+id).fill(value);
  check('범위 검증 '+id+':'+value,/입력값을 확인/.test(await page.locator('#script-result').innerText()));
  check('이전 진행 표시 없음 '+id+':'+value,await page.locator('#script-progress').isHidden());
 }
 await page.locator('#script-reset').click();await page.locator('#script-text').fill('가'.repeat(360));await page.locator('#pause-seconds').fill('0');await page.locator('#script-goal').selectOption('60');
 check('가상 60초 계산',/60\.0초/.test(await page.locator('#script-result').innerText()));
 await page.goto(base+'05-audio.html');
 // 비트 순서: 말 뮤트, 음악 뮤트, 말 솔로, 음악 솔로. 기대값은 살아 있는 트랙 이름.
 const cases=[['0000','두 트랙'],['1000','배경음만'],['0100','내레이션만'],['1100','무음'],['0010','내레이션만'],['1010','무음'],['0110','내레이션만'],['1110','무음'],['0001','배경음만'],['1001','배경음만'],['0101','무음'],['1101','무음'],['0011','두 트랙'],['1011','배경음만'],['0111','내레이션만'],['1111','무음']];
 for(const [bits,expected] of cases){await page.locator('#audio-reset').click();const selectors=['#voice-mute','#music-mute','#voice-solo','#music-solo'];for(let i=0;i<4;i++)if(bits[i]==='1')await page.locator(selectors[i]).click();check('뮤트/솔로 '+bits,(await page.locator('#audio-state').innerText()).endsWith(expected));}
 await page.locator('#audio-reset').click();await page.locator('#voice-level').focus();await page.keyboard.press('Home');await page.locator('#music-level').focus();await page.keyboard.press('Home');
 check('두 막대 0은 무음',/무음/.test(await page.locator('#audio-state').innerText()));
 await page.locator('#audio-reset').click();await page.locator('#audio-play').click();await page.waitForTimeout(100);
 check('실제 AudioContext 실행',await page.evaluate(()=>window.audioLessonState.contextState==='running'));
 await page.locator('#voice-mute').click();check('재생 중 말 뮤트 적용',await page.evaluate(()=>window.audioLessonState.levels[0]===0&&window.audioLessonState.levels[1]===20));
 await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));await page.waitForTimeout(200);
 check('화면 밖 소스 정지',await page.locator('#audio-play').getAttribute('aria-pressed')==='false');
 check('화면 밖 실제 Context 중단',await page.evaluate(()=>window.audioLessonState.contextState==='suspended'));
 await page.locator('#audio-reset').click();await page.locator('#audio-play').click();await page.waitForTimeout(100);check('재생 재시작',await page.evaluate(()=>window.audioLessonState.contextState==='running'));
 const other=await context.newPage();await other.goto('about:blank');await page.evaluate(()=>window.dispatchEvent(new PageTransitionEvent('pagehide',{persisted:true})));
 // persisted pagehide는 브라우저 뒤로 가기로 되돌아올 때를 재현한다.
 await page.evaluate(()=>window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true})));
 await page.locator('#audio-play').click();await page.waitForTimeout(120);
 check('페이지 복원 후 다시 재생',await page.locator('#audio-play').getAttribute('aria-pressed')==='true');await other.close();
 const unsupported=await browser.newContext();await unsupported.addInitScript(()=>{window.AudioContext=undefined;window.webkitAudioContext=undefined;});
 const fallback=await unsupported.newPage();await fallback.goto(base+'05-audio.html');await fallback.locator('#audio-play').click();
 check('소리 미지원 안내',/재생할 수 없습니다/.test(await fallback.locator('#audio-state').innerText()));await unsupported.close();
 check('페이지 오류 없음',errors.length===0);
 console.log(JSON.stringify({checks:checks.length,errors}));await fs.writeFile('docs/results/phase-Y4a/edge-check.json',JSON.stringify({checks:checks.length,passed:checks,errors},null,2)+'\n');
}finally{await browser.close();}
