import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const page=await browser.newPage(),results=[];
const base='http://127.0.0.1:8594/site-shorts/chapters/';
try{
 await page.goto(base+'04-script.html');
 await page.locator('#script-text').fill('가'.repeat(120));await page.locator('#sample-chars').fill('60');await page.locator('#sample-seconds').fill('10');await page.locator('#pause-seconds').fill('2');
 await page.locator('#sample-seconds').fill('0');
 const old=await page.locator('#script-progress').getAttribute('aria-valuetext');
 results.push({name:'무효 입력 후 이전 진행값 읽히지 않음',passed:!old?.includes('22.0초'),actual:old});
 await page.goto(base+'05-audio.html');await page.locator('#music-solo').click();
 const message=await page.locator('#audio-result').innerText();
 results.push({name:'음악 솔로를 균형 과다로 평가하지 않음',passed:/한 트랙/.test(message)&&!/막대가 더 높/.test(message),actual:message});
 console.log(JSON.stringify(results,null,2));
 const red=process.argv.includes('--red');
 await fs.writeFile(`docs/results/phase-Y4a/regressions-${red?'red':'green'}.json`,JSON.stringify(results,null,2)+'\n');
 process.exitCode=results.every(r=>r.passed)?0:1;
}finally{await browser.close();}
