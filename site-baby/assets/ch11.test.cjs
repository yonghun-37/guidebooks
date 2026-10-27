/* node --test site-baby/assets/ch11.test.cjs */
const {test}=require('node:test'),assert=require('node:assert/strict'),{plan}=require('./ch11.js');
const base={aStart:'22:00',aEnd:'06:00',bStart:'22:00',bEnd:'06:00'};
test('동일한 가능 시간은 가운데 교대, 각자 4시간 휴식 예정',()=>{const p=plan(base);assert.equal(p.aRest,240);assert.equal(p.bRest,240);assert.deepEqual(p.segments.map(s=>s.owner),['A','B']);});
test('겹침 없이 이어지는 교대',()=>{const p=plan({...base,aEnd:'02:00',bStart:'02:00'});assert.equal(p.aRest,240);assert.equal(p.bRest,240);});
test('중간에 아무도 못 맡는 시간은 도움 필요, 휴식으로 세지 않음',()=>{const p=plan({aStart:'18:00',aEnd:'20:00',bStart:'06:00',bEnd:'08:00'});assert.deepEqual(p.segments.map(s=>s.owner),['A','help','B']);assert.equal(p.aRest,120);assert.equal(p.bRest,120);});
test('연속 휴식은 분리된 구간을 합하지 않는다',()=>{const p=plan({...base,aStart:'18:00',aEnd:'12:00'});assert.equal(p.bRest,480);assert.equal(p.aRest,240);});
test('분 단위 가능 시간도 손실 없이 배정',()=>{const p=plan({aStart:'22:01',aEnd:'23:00',bStart:'22:01',bEnd:'23:00'});assert.equal(p.aRest+p.bRest,59);assert.ok(Number.isInteger(p.aRest));});
for(const changes of [{aStart:''},{aStart:'24:00'},{aStart:'22:60'},{aStart:'15:00'},{aEnd:'22:00'},{aEnd:'21:00'},{bStart:null}])test('시간 누락·범위·역순 차단 '+JSON.stringify(changes),()=>assert.throws(()=>plan({...base,...changes})));
