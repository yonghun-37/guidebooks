/* 실행: node --test site-baby/assets/ch09.test.cjs */
const {test}=require('node:test');
const assert=require('node:assert/strict');
const {calendar,months,parse,format}=require('./ch09.js');
test('월말은 다음 달 말일로 맞추고 윤년을 구분한다',()=>{
 assert.equal(format(months(parse('2024-01-31'),1)),'2024-02-29');
 assert.equal(format(months(parse('2025-01-31'),1)),'2025-02-28');
 assert.equal(format(months(parse('2024-02-29'),12)),'2025-02-28');
});
test('경로 모름·단독·6가에서 1개월 접종을 구분한다',()=>{
 assert.match(calendar('2026-10-01','unknown')[3][1],/임의로 정하지/);
 assert.match(calendar('2026-10-01','single')[3][1],/1개월 B형간염 접종/);
 assert.match(calendar('2026-10-01','six')[3][1],/생략/);
 assert.match(calendar('2026-10-01','six')[4][1],/6가.*B형간염/);
});
test('일령과 달력 월령을 섞지 않고 검진·로타 날짜를 계산한다',()=>{
 const rows=calendar('2026-10-01','single','2026-10-27');
 assert.equal(rows[2][0],'2026-10-15 ~ 2026-11-05');
 assert.equal(rows[3][0],'2026-11-01');
 assert.equal(rows[5][0],'2027-01-13');
 assert.equal(rows[7][0],'2027-02-01 ~ 2027-04-30');
 assert.equal(rows[8][0],'2027-06-01');
});
test('없는 날짜·예정일·잘못된 경로는 거절한다',()=>{
 assert.throws(()=>calendar('2026-02-29','single'));
 assert.throws(()=>calendar('2026-12-01','single','2026-10-27'));
 assert.throws(()=>calendar('2026-10-01','other'));
 assert.throws(()=>calendar('','single'));
});
