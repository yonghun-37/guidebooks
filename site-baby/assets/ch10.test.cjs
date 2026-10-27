/* node --test site-baby/assets/ch10.test.cjs */
const {test}=require('node:test'),assert=require('node:assert/strict');
const {calculate}=require('./ch10.js');
const base={birth:'2026-10-06',order:'first',transition:null,region:'capital'};
test('출생~23개월 24개 행과 11/12개월 경계',()=>{const r=calculate(base);assert.equal(r.rows.length,24);assert.deepEqual(r.rows.map(r=>r.month),Array.from({length:24},(_,i)=>i));assert.equal(r.rows[0].date,base.birth);assert.equal(r.rows[11].parent,1000000);assert.equal(r.rows[12].parent,500000);assert.equal(r.rows[23].date,'2028-09-06');});
test('전환 전후 현금과 보육료 분리',()=>{const r=calculate({...base,transition:6});assert.equal(r.rows[5].monthly,1100000);assert.equal(r.rows[6].monthly,516000);assert.equal(r.rows[6].childcare,584000);assert.equal(r.rows[12].parent,0);assert.equal(r.rows[12].monthly,100000);assert.equal(r.rows[12].childcare,515000);});
test('출생부터 이용과 23개월 전환',()=>{assert.equal(calculate({...base,transition:0}).rows[0].parent,416000);const r=calculate({...base,transition:23});assert.equal(r.rows[22].parent,500000);assert.equal(r.rows[23].parent,0);});
test('1세 어린이집 예시는 이전 월령 현금도 남긴다',()=>{const r=calculate({...base,birth:'2025-10-27',transition:12});assert.equal(r.age,12);assert.equal(r.rows[11].parent,1000000);assert.equal(r.rows[12].parent,0);});
test('지역 모름의 24개 행에서 확정 합계를 만들지 않음',()=>{const r=calculate({...base,region:'unknown'});for(const row of r.rows){assert.equal(row.child,null);assert.equal(row.monthly,null);}});
for(const [region,amount] of Object.entries({capital:100000,other:105000,preferred:110000,special:120000}))test('지역 배타 선택: '+region,()=>{const r=calculate({...base,region});assert.equal(r.rows[0].monthly,1000000+amount);assert.equal(r.rows[23].monthly,500000+amount);assert.equal(r.localVoucherPossible,['preferred','special'].includes(region));});
test('출생순위는 일회 바우처만 변경',()=>{const first=calculate(base),later=calculate({...base,order:'later'});assert.equal(first.firstMeeting,2000000);assert.equal(later.firstMeeting,3000000);assert.deepEqual(first.rows,later.rows);});
test('31일 출생은 각 달 말일로 조정하고 다음 달 원래 일자 회복',()=>{const r=calculate({...base,birth:'2026-01-31'});assert.equal(r.rows[1].date,'2026-02-28');assert.equal(r.rows[2].date,'2026-03-31');assert.equal(r.rows[3].date,'2026-04-30');});
test('2028 윤년 월령 시작일과 연도 넘김',()=>{const r=calculate({...base,birth:'2026-03-31'});assert.equal(r.rows[23].date,'2028-02-29');assert.equal(calculate({...base,birth:'2025-12-31'}).rows[1].date,'2026-01-31');});
for(const changes of [{birth:''},{birth:null},{birth:'2026-02-30'},{birth:'2025-02-29'},{birth:'2026-10-28'},{birth:'2024-10-27'},{transition:-1},{transition:24},{transition:1.5},{transition:'12'},{transition:NaN},{region:'all'},{order:'third'}])test('잘못된 날짜·선택 차단 '+JSON.stringify(changes),()=>assert.throws(()=>calculate({...base,...changes})));
test('조사일 출생과 23개월 경계 허용',()=>{assert.equal(calculate({...base,birth:'2026-10-27'}).age,0);assert.equal(calculate({...base,birth:'2024-10-28'}).age,23);});
