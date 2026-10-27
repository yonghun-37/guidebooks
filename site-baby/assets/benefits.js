/* 2026-10-27 단면 예상액. 임의 연도에 2026 정책을 연장하지 않는다.
   근거: BRIEFING 결론 B, FACT-SHEET NB-MONEY-01~07 / N036 N037 N095 N105. */
(function(root) {
  'use strict';
  const AS_OF = '2026-10-27';
  const regions = Object.freeze({capital:100000,other:105000,preferred:110000,special:120000});
  function parseDate(value) {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error('출생일을 정확히 입력하세요.');
    const date = new Date(value+'T00:00:00Z');
    if (!Number.isFinite(+date) || date.toISOString().slice(0,10)!==value) throw new Error('실제 달력에 있는 출생일을 입력하세요.');
    return date;
  }
  function calculate({birth,order,daycare,region}, asOf=AS_OF) {
    const date=parseDate(birth), now=parseDate(asOf);
    if(asOf!==AS_OF) throw new Error('이 도구는 2026년 10월 27일 기준으로만 계산합니다.');
    if(date>now) throw new Error('조사일 뒤 출생은 계산하지 않습니다. 출생 후 현행 안내를 확인하세요.');
    if(!['first','later'].includes(order) || typeof daycare!=='boolean' || !['unknown',...Object.keys(regions)].includes(region)) throw new Error('출생순위·어린이집·지역 선택을 확인하세요.');
    let months=(now.getUTCFullYear()-date.getUTCFullYear())*12+now.getUTCMonth()-date.getUTCMonth();
    if(now.getUTCDate()<date.getUTCDate()) months--;
    if(months>=24) throw new Error('이 도구는 조사일 기준 0~23개월만 계산합니다. 현재 지원은 주민센터에 확인하세요.');
    const base=months<12 ? 1000000 : 500000;
    const childcare=daycare ? (months<12 ? 584000 : 515000) : 0;
    const parent=daycare ? Math.max(0,base-childcare) : base;
    const child=region==='unknown' ? null : regions[region];
    return Object.freeze({asOf,months,parent,child,monthly:child===null?null:parent+child,childcare,firstMeeting:order==='first'?2000000:3000000,localVoucherPossible:['preferred','special'].includes(region)});
  }
  const api=Object.freeze({AS_OF,calculate});
  if(typeof module!=='undefined'&&module.exports) module.exports=api;
  else root.BabyBenefits=api;
})(typeof window!=='undefined'?window:globalThis);
