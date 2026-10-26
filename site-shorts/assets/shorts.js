/* 두 샘플의 계산·설정 메모. 외부 요청과 계정 조작은 하지 않는다. */
(() => {
  'use strict';
  window.ShortsSim.mount('#rpm-tool', (root, report) => {
    const views = root.querySelector('#views');
    const rpm = root.querySelector('#rpm');
    const approved = root.querySelector('#monetized');
    const formula = root.querySelector('[data-rpm-formula]');
    const format = value => value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const render = () => {
      let valid = true;
      [views, rpm].forEach(input => {
        const ok = input.value.trim() !== '' && input.validity.valid && Number.isFinite(input.valueAsNumber);
        input.setAttribute('aria-invalid', String(!ok));
        if (!ok) valid = false;
      });
      if (!valid) {
        formula.textContent = '유효 조회수는 0 이상 정수, RPM은 0 이상 숫자로 입력하세요. 입력칸의 최댓값도 확인하세요.';
        report('— · 입력값을 확인하면 다시 계산합니다.');
        return;
      }
      const count = views.valueAsNumber, rate = rpm.valueAsNumber;
      formula.textContent = `${count.toLocaleString('en-US')} ÷ 1,000 × ${rate.toLocaleString('en-US', {maximumFractionDigits: 10})}`;
      const income = approved.value === 'yes' ? count / 1000 * rate : 0;
      const value = document.createElement('strong');
      value.textContent = `US$${format(income)}`;
      const output = root.querySelector('[data-sim-result]');
      output.replaceChildren(value, document.createTextNode(approved.value === 'yes'
        ? '가상 참고 계산입니다. 실제 수입은 Studio에서 확인하세요.'
        : '광고 미가입·약관 동의 전 조회수는 피드 광고 수입에 반영되지 않습니다.'));
      if (approved.value !== 'yes') formula.textContent += ' → 광고 공유 전이므로 0';
    };
    root.addEventListener('input', render);
    root.addEventListener('change', render);
    root.querySelectorAll('[data-rpm-preset]').forEach(button => button.addEventListener('click', () => {
      views.value = button.dataset.rpmPreset === 'zero' ? '0' : '1000000';
      rpm.value = '0.185';
      approved.value = button.dataset.rpmPreset === 'unapproved' ? 'no' : 'yes';
      render();
    }));
    render();
  });

  const root = document.querySelector('#upload-tool');
  if (!root) return;
  const form = root.querySelector('form');
  const audience = form.querySelector('#audience');
  const ai = form.querySelector('#ai-content');
  const music = form.querySelector('#music-rights');
  const voice = form.querySelector('#ai-voice');
  const voiceBranch = form.querySelector('[data-voice-branch]');
  const render = () => {
    const needsVoice = ['cartoon', 'tts'].includes(ai.value);
    voiceBranch.hidden = !needsVoice;
    voice.disabled = !needsVoice;
    const voicePending = needsVoice && !['own', 'clone', 'realistic'].includes(voice.value);
    const answered = [audience, ai, music].filter(input => input.value !== '').length;
    const unresolved = [!audience.value || audience.value === 'unsure',
      !ai.value || ai.value === 'unsure' || voicePending, !music.value || music.value === 'unknown'].filter(Boolean).length;
    const actions = [];
    if (audience.value === 'kids') actions.push(['시청자층: 아동용 예를 선택하세요. 의도한 시청자와 콘텐츠 요소를 다시 대조하세요.', '#audience-step']);
    else if (audience.value === 'general') actions.push(['시청자층: 아동용 아니요. 어린이 대상 영상이 아닌지 실제 내용을 대조하세요.', '#audience-step']);
    else actions.push(['아동용 여부를 먼저 판단하세요. 공식 판단 기준에서 의도한 시청자·주제·표현을 확인하세요.', '#audience-step']);
    if (['realistic', 'music'].includes(ai.value) || (needsVoice && ['clone', 'realistic'].includes(voice.value))) actions.push(['AI 사용: 예. 사실적 합성·타인 목소리 복제·AI 음악 등 공개 대상이 있습니다. 속성 → AI 사용 또는 더보기 → 변경된 콘텐츠에서 표시하고 소재 권리도 확인하세요.', '#ai-step']);
    else if (needsVoice && voice.value === 'own') actions.push([ai.value === 'cartoon'
      ? 'AI 사용: 선택한 조건만이라면 아니요. 비현실적 종이 로봇 삽화·본인 음성은 공개 불필요 예시에 대조할 수 있습니다. 실제처럼 보이는 합성이나 AI 음악이 섞이지 않았는지 확인하세요.'
      : 'AI 사용: 선택한 조건만이라면 아니요. 본인 녹음·본인 음성 복제 외 공개 대상 합성이 없는지 확인하세요.', '#ai-step']);
    else if (needsVoice) actions.push(['AI 사용: 음성 조건 확인 전에는 판단을 보류하세요. 일반 TTS도 실제 인물의 발언으로 오인될지 듣고 공식 예시와 대조하세요. 사용 허락도 확인한 뒤 실제 화면에서 결정하세요.', '#ai-step']);
    else if (['assist', 'none'].includes(ai.value)) actions.push(['AI 사용: 선택한 조건만이라면 아니요. 대본·자막 보조 외 사실적 합성이나 AI 음악이 없는지 확인하세요.', '#ai-step']);
    else actions.push(['AI 사용 방식부터 확인하세요. 실제처럼 보이는 합성·생성 내용이 있는지 공식 예시와 대조하세요.', '#ai-step']);
    if (music.value === 'own') actions.push(['음악: 넣지 않았거나 모두 직접 만든 음악인지 확인하세요. 타인의 녹음·샘플을 섞었다면 사용권을 다시 확인하세요.', '#review']);
    else if (music.value === 'library') actions.push(['음악: Studio 오디오 보관함의 이용 조건과 필요한 저작자 표시를 설명에 넣으세요.', '#review']);
    else if (music.value === 'licensed') actions.push(['음악: 확보한 사용권이 이 영상의 공개·수익화 용도까지 허용하는지 대조하고 증거를 보관하세요.', '#review']);
    else actions.push(['음악: 사용권 확인 전에는 공개를 보류하세요. 허락을 확보하거나 권리 확인 음원으로 바꾸거나 빼세요.', '#review']);
    root.querySelector('[data-upload-count]').textContent = answered < 3 ? `${answered}/3개 답변` : unresolved ? `공개 전 확인 ${unresolved}개` : '3개 설정 메모 준비';
    root.querySelector('[data-upload-message]').textContent = answered < 3
      ? '세 질문에 모두 답하세요. 아직 답하지 않은 항목도 공개 전에 확인해야 해요.'
      : unresolved ? '아래의 남은 항목을 확인한 뒤 공개 여부를 정하세요.'
      : '아래 메모를 실제 업로드 화면에 옮기고, 영상 전체와 사용권을 직접 확인하세요.';
    const list = root.querySelector('[data-upload-actions]');
    list.replaceChildren(...actions.map(([text, href]) => {
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = href;
      link.textContent = text;
      item.append(link);
      return item;
    }));
  };
  form.addEventListener('change', render);
  form.addEventListener('submit', event => event.preventDefault());
  // 네이티브 reset의 기본 동작이 입력값을 바꾼 다음 결과를 갱신한다.
  form.addEventListener('reset', () => setTimeout(render, 0));
  render();
})();
