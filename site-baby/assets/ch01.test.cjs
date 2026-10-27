const test=require('node:test'),assert=require('node:assert/strict');
const {calendar}=require('./ch01.js');
test('ordinary dates distinguish birth-inclusive 60 days and 14w6',()=>{
 const r=calendar('2026-10-01');
 assert.deepEqual(r,{month:'2026-11-01',clamped:false,benefit:'2026-11-29',screenStart:'2026-10-15',screenEnd:'2026-11-05',rota:'2027-01-13'});
});
test('month-end keeps reference separate from legal deadline',()=>{
 const r=calendar('2026-01-31');assert.equal(r.month,'2026-02-28');assert.equal(r.clamped,true);assert.equal(r.benefit,'2026-03-31');
});
test('leap years and year rollovers',()=>{
 assert.equal(calendar('2024-01-31').month,'2024-02-29');assert.equal(calendar('2024-02-29').benefit,'2024-04-28');assert.equal(calendar('2026-12-31').month,'2027-01-31');
});
test('invalid or absent dates rejected',()=>{
 for(const d of ['', '2026-02-29','2026-04-31','2026-13-01','2026-00-01','<img>','2026-1-1','0000-01-01'])assert.throws(()=>calendar(d));
});
test('local timezone does not change calendar dates',()=>{
 assert.equal(calendar('2026-03-01').screenStart,'2026-03-15');assert.equal(calendar('2026-10-31').screenEnd,'2026-12-05');
});
