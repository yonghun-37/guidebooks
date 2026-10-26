import {chromium} from '/tmp/ai-insta-phase3-browser/node_modules/playwright-core/index.mjs';
import fs from 'node:fs/promises';
const browser=await chromium.launch({executablePath:'/home/yonghun/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless:true,args:['--no-sandbox']});
const page=await browser.newPage();const issues=[];
for(const [slug,selector,width,theme,name] of [
 ['06-writing','#info',1280,'light','06-recipe-1280-light'],
 ['06-writing','#review',360,'dark','06-review-360-dark'],
 ['07-images','#generate',375,'light','07-ai-examples-375-light'],
 ['07-images','#layout',360,'dark','07-layout-360-dark'],
 ['08-seo','#structure',360,'light','08-structure-360-light'],
 ['09-monetize','#affiliate',375,'dark','09-affiliate-375-dark']]){
 await page.setViewportSize({width,height:1000});await page.goto('http://127.0.0.1:8864/site-blog/chapters/'+slug+'.html');await page.selectOption('[data-theme-select]',theme);
 await page.locator(selector).scrollIntoViewIfNeeded();for(const img of await page.locator(selector+' img').all()){await img.scrollIntoViewIfNeeded();await img.evaluate(n=>n.decode());}
 await page.addStyleTag({content:'[data-site-header],.skip-link{visibility:hidden!important}'});
 await page.locator(selector).screenshot({path:'docs/results/phase-B4b/'+name+'.png'});
 const svgIssues=await page.locator('svg text').evaluateAll(ns=>ns.flatMap(n=>{const b=n.getBBox(),box=n.ownerSVGElement.viewBox.baseVal;return b.x<0||b.x+b.width>box.width?[n.textContent]:[];}));issues.push(...svgIssues);
}
await fs.writeFile('docs/results/phase-B4b/visual-check.json',JSON.stringify({svgTextOutsideViewBox:[...new Set(issues)]},null,2));console.log(issues);await browser.close();
