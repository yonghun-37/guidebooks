// 로컬 그림/샘플만 Chromium으로 확인한다. 외부 네트워크는 차단한다.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname,'..');
async function main(){
  const browser = await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH || undefined,args:['--no-sandbox']});
  const context = await browser.newContext();
  await context.route(/^https?:\/\//, r=>r.abort());
  const page=await context.newPage();const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  let checks=0;
  for(const theme of ['light','dark']){
    await page.emulateMedia({colorScheme:theme});
    for(const width of [1280,375,360]){
      await page.setViewportSize({width,height:900});
      for(const file of ['docs/figures.html','samples/dashboard.html','samples/insta/preview.html','samples/shorts/preview.html']){
        await page.goto('file://'+path.join(root,file));
        await page.waitForLoadState('load');
        const bad=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,images:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)}));
        if(bad.overflow||bad.images.length)throw new Error(file+' '+width+' '+JSON.stringify(bad));
        checks++;
        if(file==='docs/figures.html'&&width===1280){fs.mkdirSync(path.join(root,'docs/verification'),{recursive:true});await page.screenshot({path:path.join(root,'docs/verification/figures-'+theme+'.png')});}
      }
    }
  }
  for(const name of fs.readdirSync(path.join(root,'docs/figures')).filter(n=>n.endsWith('.svg'))){
    await page.goto('file://'+path.join(root,'docs/figures',name));
    const bad=await page.evaluate(()=>[...document.querySelectorAll('a')].flatMap(a=>{const r=a.querySelector('rect');if(!r)return[];const x=+r.getAttribute('x'),w=+r.getAttribute('width');return [...a.querySelectorAll('text')].filter(t=>t.getBBox().x+t.getBBox().width>x+w-8).map(t=>t.textContent)}));
    if(bad.length)throw new Error(name+' 텍스트 영역 초과: '+bad.join(' / '));
    checks++;
  }
  if(errors.length)throw new Error(errors.join('\n'));
  console.log(JSON.stringify({checks,pageErrors:errors.length,themes:2,widths:[1280,375,360]}));
  await browser.close();
}
main().catch(e=>{console.error(e.message);process.exit(1)});
