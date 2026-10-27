/* node --test scripts/test_baby_benefits.cjs */
const {test}=require('node:test');
const assert=require('node:assert/strict');
const {calculate,AS_OF}=require('../site-baby/assets/benefits.js');
const base={birth:'2026-10-06',order:'first',daycare:false,region:'capital'};
test('0세 가정양육: 월 현금과 1회 바우처를 분리한다',()=>{
 const r=calculate(base);assert.equal(r.asOf,AS_OF);assert.equal(r.months,0);
 assert.equal(r.parent,1000000);assert.equal(r.child,100000);assert.equal(r.monthly,1100000);
 assert.equal(r.firstMeeting,2000000);assert.equal(r.childcare,0);
});
test('둘째 이상은 첫만남만 달라진다',()=>{
 const r=calculate({...base,order:'later'});assert.equal(r.monthly,1100000);assert.equal(r.firstMeeting,3000000);
});
test('0세 어린이집은 58.4만원 바우처를 현금에 더하지 않는다',()=>{
 const r=calculate({...base,daycare:true});assert.equal(r.parent,416000);assert.equal(r.childcare,584000);assert.equal(r.monthly,516000);
});
test('첫 생일 전날과 당일의 11/12개월 경계',()=>{
 assert.equal(calculate({...base,birth:'2025-10-28'}).months,11);
 const r=calculate({...base,birth:'2025-10-27'});assert.equal(r.months,12);assert.equal(r.parent,500000);
});
test('1세 어린이집: 부모 현금 차액은 음수가 아닌 0원',()=>{
 const r=calculate({...base,birth:'2025-10-27',daycare:true});assert.equal(r.parent,0);assert.equal(r.childcare,515000);assert.equal(r.monthly,100000);
});
for(const [region,amount] of Object.entries({capital:100000,other:105000,preferred:110000,special:120000})){
 test(`지역 ${region}: 중복 가산과 상품권의 현금 합산을 하지 않는다`,()=>{
  const r=calculate({...base,region});assert.equal(r.child,amount);assert.equal(r.monthly,1000000+amount);
  assert.equal(r.localVoucherPossible,['preferred','special'].includes(region));
 });
}
test('지역 모름: 정확한 아동수당과 합계를 만들지 않는다',()=>{
 const r=calculate({...base,region:'unknown'});assert.equal(r.child,null);assert.equal(r.monthly,null);assert.equal(r.parent,1000000);
});
test('달력 날짜를 검증하고 실제 윤일은 월령 범위로 판정한다',()=>{
 assert.throws(()=>calculate({...base,birth:'2024-02-29'}), /0~23개월/);
 assert.throws(()=>calculate({...base,birth:'2025-02-29'}), /실제 달력/);
});

test('조사일 당일 출생과 23개월 경계',()=>{
 assert.equal(calculate({...base,birth:'2026-10-27'}).months,0);
 assert.equal(calculate({...base,birth:'2024-10-28'}).months,23);
 assert.throws(()=>calculate({...base,birth:'2024-10-27'}),/0~23개월/);
});
for(const birth of ['',null,'2026-2-03','2026-02-30','2026-13-01','2026-10-28','2027-01-01']){
 test(`빈 값·잘못된 달력·조사일 뒤 출생 차단: ${birth}`,()=>assert.throws(()=>calculate({...base,birth})));
}
test('2026 숫자를 2027 정책으로 연장하지 않는다',()=>assert.throws(()=>calculate(base,'2027-01-01'),/2026년/));
for(const changes of [{order:'third'},{daycare:'yes'},{region:'all'}]){
 test(`선택값 검증: ${JSON.stringify(changes)}`,()=>assert.throws(()=>calculate({...base,...changes})));
}
