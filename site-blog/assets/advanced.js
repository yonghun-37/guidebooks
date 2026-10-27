/* 심화편 전용: 운영체제 탭과 외부 전송 없는 가상 협찬 대장. */
(() => {
  'use strict';
  document.querySelectorAll('[data-os-tabs]').forEach((box, index) => {
    const tabs = [...box.querySelectorAll('[data-os]')];
    const panels = [...box.querySelectorAll('[data-os-panel]')];
    box.classList.add('is-enhanced');
    box.querySelector('.os-switch').setAttribute('role', 'tablist');
    const activate = selected => {
      tabs.forEach(tab => {
        const active = tab === selected;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
      });
      panels.forEach(panel => { panel.hidden = panel.dataset.osPanel !== selected.dataset.os; });
    };
    tabs.forEach((tab, i) => {
      const panel = panels.find(item => item.dataset.osPanel === tab.dataset.os);
      tab.id = `os-tab-${index}-${i}`;
      panel.id = `os-panel-${index}-${i}`;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panel.id);
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
      tab.addEventListener('click', () => activate(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (i + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (i + tabs.length - 1) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); activate(tabs[next]); tabs[next].focus(); }
      });
    });
    activate(tabs[0]);
  });

  const tool = document.querySelector('[data-sponsor-tool]');
  if (!tool) return;
  const key = 'blogbook:advanced:sponsor:v1';
  // 이름·전이는 키트 monetize/sponsor/states.py를 따른다. 입력은 가상 확인 항목뿐이다.
  const states = {
    inquiry: ['문의', '광고주·조건·게시할 매체를 기록해요.', ['연락처·제공 조건·게시 매체 기록'], ['reviewing', 'declined', 'on_hold']],
    reviewing: ['검토', '도담도 분류·리콜·AI·권리 답을 받은 뒤 수락해요.', ['분류·모델·업체·리콜 자료 확인', 'AI 사용 불허 확인 → 사람 작성 선택', '첫머리 표시·아이 정보 비노출·권리·기한 합의'], ['accepted', 'declined', 'on_hold']],
    accepted: ['수락', '수락한 조건을 계약에 옮겨요.', ['서면으로 제안 조건 수락 기록'], ['contracted', 'on_hold', 'cancelled']],
    contracted: ['계약', '블로그 게시 범위와 2차 사용권을 구별해요.', ['계약 버전·현금·현물·반납·기한 기록', '수정 범위·권리·취소·지급 조건 기록'], ['received', 'on_hold', 'cancelled']],
    received: ['제품 수령', '받은 모델과 상태를 자료와 대조해요.', ['수령일·모델·파손·리콜 재확인', '사용 메모·가액 근거·반납 조건 보관'], ['writing', 'on_hold', 'cancelled', 'declined']],
    writing: ['작성', 'AI가 사용 경험을 만들지 않게 사람 메모를 써요.', ['직접 사용한 메모와 아쉬운 점 작성', '허락된 사진·아이 비노출·출처·첫머리 표시 확인'], ['brand_review', 'on_hold']],
    brand_review: ['광고주 확인', '광고주의 사실관계 확인 뒤에도 내 승인이 남아요.', ['광고주 답변·확인 원고 버전·수정 횟수 기록'], ['human_approval', 'writing', 'on_hold']],
    human_approval: ['최종 사람 승인', '공개될 원고·사진·표시·링크를 직접 읽어요.', ['최종본 해시·검토자·확인 시각 기록'], ['approved', 'writing', 'on_hold']],
    approved: ['발행 준비', '승인한 내용과 발행할 내용이 같아야 해요.', ['승인 해시 일치·발행 시각·목적지 확인'], ['scheduled', 'published', 'writing', 'on_hold']],
    scheduled: ['예약', '예약과 실제 공개는 다른 상태예요.', ['서버 글 ID·예약 시각·시간대 기록', '서버 공개 상태를 재조회하고 공개 주소 확인'], ['published', 'writing', 'on_hold']],
    published: ['발행', '서버를 다시 조회해 공개 주소를 확인해요.', ['공개 상태·주소·표시·계약 해시 기록'], ['reported', 'on_hold']],
    reported: ['성과 보고', '개인정보 없이 합의한 집계만 보고해요.', ['기간·지표 정의·공유 허용 자료·아이 비노출 확인'], ['settlement_pending', 'on_hold']],
    settlement_pending: ['정산 대기', '현물과 현금 입금을 나눠 기록해요.', ['현금·현물·반납·원천징수·지급일 확인', '입금일·실입금·현물·비용·증빙·세금 확인 과제 기록'], ['settled', 'on_hold']],
    settled: ['정산', '가상 문의를 끝냈어요. 실제 세금 판단은 공식 안내로 확인해요.', [], []],
    declined: ['거절', '거절 이유를 남겼어요. 포근담요는 영아 수면 안전 충돌이에요.', [], []],
    cancelled: ['취소', '반납·미지급·비용 합의와 통지 기록을 남겼어요.', [], []],
    on_hold: ['자료 보류', '시간이 지나도 자동 승인하지 않아요. 자료가 해결되면 원래 상태로 돌아가요.', ['요청 자료·담당자·확인 기한 기록', '누락 자료를 받고 확인 완료'], []]
  };
  const select = tool.querySelector('#sponsor-case');
  const stateNode = tool.querySelector('[data-sponsor-state]');
  const help = tool.querySelector('[data-sponsor-help]');
  const records = tool.querySelector('[data-sponsor-records]');
  const actions = tool.querySelector('[data-sponsor-actions]');
  const history = tool.querySelector('[data-sponsor-history]');
  const saveStatus = tool.querySelector('[data-sponsor-save]');
  let model = { case: 'shelf', state: 'inquiry', history: ['inquiry'], returnState: null };
  let storageAvailable = true;
  const allowed = value => {
    if (value.state === 'on_hold') return [value.returnState];
    if (value.state === 'reviewing' && value.case === 'blanket') return ['declined'];
    if (value.state === 'reviewing' && value.case === 'missing') return ['on_hold'];
    return states[value.state][3];
  };
  try {
    const saved = JSON.parse(localStorage.getItem(key) || 'null');
    if (saved && ['shelf', 'blanket', 'missing'].includes(saved.case) && Array.isArray(saved.history) && saved.history.length <= 100 && saved.history[0] === 'inquiry') {
      // 저장값도 허용된 경로인지 검사해 손상된 값의 단계 건너뛰기를 막는다.
      const probe = {case: saved.case, state: 'inquiry', returnState: null};
      const valid = saved.history.slice(1).every(next => {
        if (!states[next] || !allowed(probe).includes(next)) return false;
        if (next === 'on_hold') probe.returnState = probe.state;
        // 자료 부족 문의의 복귀는 누락 자료를 받은 것으로 연습한다.
        if (probe.state === 'on_hold' && probe.case === 'missing') probe.case = 'shelf';
        probe.state = next;
        return true;
      });
      if (valid && probe.state === saved.state && probe.case === saved.case) model = {...probe, history: saved.history};
    }
    localStorage.setItem(key, JSON.stringify(model));
  } catch { storageAvailable = false; }
  function save() {
    try { localStorage.setItem(key, JSON.stringify(model)); storageAvailable = true; }
    catch { storageAvailable = false; }
  }
  function render(focus = false) {
    select.value = model.case;
    stateNode.textContent = `${states[model.state][0]} · ${model.state}`;
    help.textContent = model.state === 'declined' && model.case !== 'blanket' ? '거절 이유·통지·반납·비용 처리 기록을 남겼어요.' : model.state === 'reviewing' && model.case === 'blanket'
      ? '안전 수면 원칙과 충돌해요. 프로젝트 거절 사유와 정중한 회신을 남기세요.'
      : model.state === 'reviewing' && model.case === 'missing'
        ? '모델과 리콜 자료가 없어요. 자료 보류로 옮기고 확인 요청을 남겨요.' : states[model.state][1];
    records.replaceChildren();
    const labels = model.state === 'reviewing' && model.case === 'blanket'
      ? ['영아 수면 안전 충돌 사유 기록', '거절 회신·반납·비용 처리 기록']
      : model.state === 'reviewing' && model.case === 'missing'
        ? ['누락 모델·리콜 자료를 요청하고 담당자·확인 기한·복귀 상태 기록'] : states[model.state][2];
    tool.querySelector('fieldset').hidden = labels.length === 0;
    const inputs = labels.map(label => {
      const node = document.createElement('label');
      const input = document.createElement('input'); input.type = 'checkbox';
      node.append(input, document.createTextNode(label)); records.append(node);
      return input;
    });
    actions.replaceChildren();
    const nextStates = allowed(model);
    nextStates.forEach(next => {
      const button = document.createElement('button'); button.type = 'button';
      button.textContent = `다음 상태: ${states[next][0]}`;
      button.disabled = inputs.length > 0;
      button.addEventListener('click', () => {
        if (next === 'on_hold') model.returnState = model.state;
        if (model.state === 'on_hold' && model.case === 'missing') model.case = 'shelf';
        model.state = next; model.history.push(next);
        save(); render(true);
      });
      actions.append(button);
    });
    inputs.forEach(input => input.addEventListener('change', () => {
      actions.querySelectorAll('button').forEach(button => { button.disabled = !inputs.every(item => item.checked); });
    }));
    history.replaceChildren();
    model.history.forEach(name => { const li = document.createElement('li'); li.textContent = `${states[name][0]} · ${name}`; history.append(li); });
    saveStatus.textContent = storageAvailable ? '이 브라우저에만 저장돼요. 실제 발행·회신은 하지 않아요.' : '저장이 차단됐어요. 현재 화면에서 계속 연습할 수 있지만 이동하면 기록이 사라져요.';
    if (focus) { stateNode.tabIndex = -1; stateNode.focus({preventScroll: true}); }
  }
  const reset = () => { model = {case: select.value, state: 'inquiry', history: ['inquiry'], returnState: null}; save(); render(true); };
  select.addEventListener('change', reset);
  tool.querySelector('[data-sponsor-reset]').addEventListener('click', reset);
  tool.querySelector('[data-sponsor-controls]').hidden = false;
  render();
})();
