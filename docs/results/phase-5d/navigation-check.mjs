import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const base='http://127.0.0.1:8515/reels/';
const b=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',args:['--no-sandbox']});
const checks=[],errors=[],links=new Set();
const check=(name,value)=>{assert.ok(value,name);checks.push(name);};
try{
 const p=await b.newPage({viewport:{width:1280,height:1000}});p.on('pageerror',e=>errors.push(String(e)));p.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 await p.goto(base);const chapters=await p.evaluate(()=>ReelsBook.chapters);
 for(let i=0;i<chapters.length;i++){
  const c=chapters[i],path=c.number<=14&&c.number?`chapters/${c.slug}.html`:`${c.slug}.html`;
  await p.goto(base+path);
  const pager=p.locator('[data-chapter-pager] a');
  const next=chapters[i+1];const previous=chapters[i-1];
  const actual=await pager.evaluateAll(as=>as.map(a=>a.href));
  const pathFor=c=>c.number&&c.number<=14?`chapters/${c.slug}.html`:`${c.slug}.html`;
  check(`${c.slug} 이전 이동`,actual[0]===base+(previous?pathFor(previous):'index.html'));
  check(`${c.slug} 다음 이동`,actual[1]===base+(next?pathFor(next):'index.html#contents'));
  check(`${c.slug} 공개 상태`,!await p.title().then(t=>t.includes('준비 중')));
  check(`${c.slug} 상대 내부 링크`,await p.locator('a[href]').evaluateAll(as=>as.filter(a=>a.origin===location.origin).every(a=>!/^\/|^https?:/.test(a.getAttribute('href')))));
  (await p.locator('a[href]').evaluateAll(as=>as.map(a=>a.href).filter(url=>url.startsWith(location.origin)))).forEach(url=>links.add(url));
  if(c.number<=14 && c.number){check(`${c.slug} 공통 메타 4항목`,await p.locator('[data-chapter-meta] dt').count()===4);}
 }
 // 동적으로 생성된 링크까지 실제 호스팅 prefix에서 요청·앵커 대조.
 const cache=new Map();
 for(const link of links){const url=new URL(link);const target=url.origin+url.pathname;
  if(!cache.has(target)){const response=await p.request.get(target);check(`HTTP ${url.pathname}`,response.ok());cache.set(target,await response.text());}
  if(url.hash){const id=decodeURIComponent(url.hash.slice(1));check(`anchor ${url.pathname}#${id}`,cache.get(target).includes(`id="${id}"`));}
 }
 await p.goto(base+'lab.html');await p.locator('#sim-picker').selectOption('14:planner-sim');await p.frameLocator('#sim-frame').locator('#planner-sim').waitFor();
 check('하위 경로 프레임 원본 재사용',p.frames().some(f=>f.url()===base+'chapters/14-plan.html?embed=planner-sim'));
 await p.setViewportSize({width:375,height:900});await p.goto(base+'glossary.html');await p.locator('#term-search').fill('zz-no-result');
 await p.evaluate(()=>{location.hash='dry-run';});await p.waitForTimeout(100);check('검색 후 용어 앵커 열면 결과 복원',await p.locator('#dry-run').isVisible());
 // file://에서도 표지·내부 경로·장 모듈을 확인. 프레임 교차 문서 저장은 브라우저 제한 범위다.
 await p.goto('file:///home/yonghun/project/ai-insta/site/index.html');check('파일로 열기 표지 계산',await p.locator('[data-sim-count]').textContent()==='29');
 await p.goto('file:///home/yonghun/project/ai-insta/site/chapters/03-revenue.html');await p.locator('#brand').fill('100');check('파일로 열기 장부',(await p.locator('#ledger-sim [data-sim-result]').textContent()).includes('100원'));
 check('콘솔·페이지 오류 0',errors.length===0);
 await fs.writeFile('docs/results/phase-5d/navigation-check.json',JSON.stringify({base,checks,uniqueRuntimeLinks:links.size,errors},null,2));console.log(`${checks.length} navigation checks passed; ${links.size} runtime links`);
}finally{await b.close();}
