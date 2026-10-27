(() => {
  'use strict';
  const tool = document.querySelector('[data-gate-tool]');
  if (!tool) return;
  // 키트 고정 샘플의 evaluate 검사 기록이며 새 판정을 만들지 않아요.
  const snapshots = {"info": [{"rule_id": "general", "decision": "pass", "reason_ko": "자동 검사에서 차단이나 검토 항목이 없습니다.", "next_action_ko": "발행 설정을 확인하세요."}], "play": [{"rule_id": "health_safety.H1", "decision": "review", "reason_ko": "건강·안전 주제는 사람 검토가 필요합니다.", "next_action_ko": "의료 근거와 문맥을 확인하세요."}, {"rule_id": "health_safety.H4", "decision": "review", "reason_ko": "건강 글의 공통 응급 문구 적용 여부를 확인해야 합니다.", "next_action_ko": "해당 응급 신호가 있으면 공통 문구를 그대로 넣고 사람이 검토하세요."}], "affiliate": [{"rule_id": "disclosure.D1", "decision": "block", "reason_ko": "첫 문단에 수수료 관계가 공개되지 않았습니다.", "next_action_ko": "실제 받는 관계를 첫 문단에 각각 밝히세요."}], "sponsor": [{"rule_id": "health_safety.H1", "decision": "review", "reason_ko": "건강·안전 주제는 사람 검토가 필요합니다.", "next_action_ko": "의료 근거와 문맥을 확인하세요."}, {"rule_id": "health_safety.H4", "decision": "review", "reason_ko": "건강 글의 공통 응급 문구 적용 여부를 확인해야 합니다.", "next_action_ko": "해당 응급 신호가 있으면 공통 문구를 그대로 넣고 사람이 검토하세요."}, {"rule_id": "disclosure.D4", "decision": "block", "reason_ko": "실제 경험은 사람이 작성해야 합니다.", "next_action_ko": "사람의 경험을 직접 입력하세요."}]};
  const stages = [
    ['구조·원문 일치', ['schema', 'content']], ['출처·소제목', ['seo']],
    ['건강·안전', ['health_safety']], ['아이 사생활', ['child_privacy']],
    ['관계 표시·사람 경험', ['disclosure']], ['제품 분류·자료', ['product_rules']],
    ['중복·발행 상한', ['duplicate', 'quota']],
  ];
  const select = tool.querySelector('select');
  const log = tool.querySelector('[data-gate-log]');
  const next = tool.querySelector('[data-gate-next]');
  const result = tool.querySelector('[data-gate-result]');
  const progress = tool.querySelector('[data-gate-progress]');
  const names = { pass: '자동 항목 없음', review: '사람 검토 대기', block: '차단' };
  let step = 0;
  function reset() {
    step = 0;
    log.replaceChildren();
    next.disabled = false;
    progress.textContent = '검사를 시작하기 전이에요.';
    result.textContent = '다음 검사 보기를 눌러 이유와 행동을 확인하세요.';
  }
  next.addEventListener('click', () => {
    if (step >= stages.length) return;
    const [name, prefixes] = stages[step];
    const rows = snapshots[select.value];
    const found = rows.filter(row => prefixes.includes(row.rule_id.split('.')[0]));
    const item = document.createElement('li');
    item.textContent = `${name}: ` + (found.length ? found.map(row => `${names[row.decision]} · ${row.reason_ko} ${row.next_action_ko}`).join(' / ') : '이 고정 샘플의 검사 기록에 걸린 항목이 없어요.');
    log.append(item);
    step += 1;
    progress.textContent = `${step} / ${stages.length} 검사 기록을 읽었어요.`;
    if (step === stages.length) {
      next.disabled = true;
      const decision = rows.some(row => row.decision === 'block') ? 'block' : rows.some(row => row.decision === 'review') ? 'review' : 'pass';
      result.textContent = `${names[decision]} · ` + ({block: '해당 내용이나 자료를 고친 뒤 재검사하세요. 차단을 승인으로 덮지 않아요.', review: '공식 근거와 문맥을 사람이 확인하고 최종본을 승인하세요.', pass: '기본은 서버 초안 준비 → 최종 사람 승인이에요. 선택 자동 예약은 auto 설정·허용 info/play·모든 관문 pass·전체 위험 신호 없음·직접 제작 삽화만·서버 신규 확인을 모두 충족해야 해요.'}[decision]);
    } else {
      result.textContent = '아직 남은 검사가 있어요. 최종 판정 전이에요.';
    }
  });
  select.addEventListener('change', reset);
  tool.querySelector('[data-gate-reset]').addEventListener('click', reset);
  tool.querySelector('[data-gate-controls]').hidden = false;
  reset();
})();
