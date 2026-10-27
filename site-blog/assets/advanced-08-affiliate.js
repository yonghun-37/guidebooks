(() => {
  'use strict';
  const tool = document.querySelector('[data-disclosure-tool]');
  if (!tool) return;
  const form = tool.querySelector('[data-disclosure-controls]');
  const radios = Array.from(form.querySelectorAll('input[type="radio"]'));
  const title = tool.querySelector('[data-preview-title]');
  const disclosure = tool.querySelector('[data-preview-disclosure]');
  const linknote = tool.querySelector('[data-preview-linknote]');
  const result = tool.querySelector('[data-disclosure-result]');
  const save = tool.querySelector('[data-disclosure-save]');
  const key = 'blogbook:advanced:affiliate-position:v1';
  const message = '이 게시물은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.';
  const valid = value => ['title', 'opening', 'link'].includes(value);
  let position = 'opening';
  let storageReadable = true;
  try {
    const stored = localStorage.getItem(key);
    if (stored !== null) {
      if (valid(stored)) position = stored;
      else save.textContent = '저장된 위치가 맞지 않아 첫머리로 시작해요.';
    }
  } catch (_) {
    storageReadable = false;
    save.textContent = '이 브라우저에서는 저장을 읽을 수 없어요. 위치 연습은 계속할 수 있어요.';
  }
  function render(value) {
    position = value;
    radios.forEach(radio => { radio.checked = radio.value === value; });
    title.textContent = (value === 'title' ? message + ' ' : '') + '신생아 손톱 도구 고르는 기준';
    disclosure.hidden = value !== 'opening';
    linknote.textContent = value === 'link' ? message : '';
    const descriptions = {
      title: '제목: 전체 문구를 넣었어요. 실제 목록과 앱에서 잘리면 첫머리에도 표시하세요.',
      opening: '첫머리: 본문을 읽기 전에 수수료 관계를 볼 수 있어요. 실제 휴대폰에서 글자 크기와 펼침 여부를 확인하세요.',
      link: '링크 옆만: 첫 부분에 관계 표시가 없어 부족해요. 제목 또는 첫머리 표시를 추가하세요.'
    };
    result.textContent = descriptions[value];
  }
  function choose(value) {
    if (!valid(value)) return;
    render(value);
    try {
      localStorage.setItem(key, value);
      save.textContent = '위치 선택을 이 브라우저에 저장했어요. 외부 전송은 없어요.';
    } catch (_) {
      save.textContent = '저장할 수 없어 새로고침하면 선택이 사라져요. 위치 연습은 계속할 수 있어요.';
    }
  }
  form.addEventListener('change', event => {
    if (event.target.matches('input[type="radio"]')) choose(event.target.value);
  });
  form.addEventListener('submit', event => event.preventDefault());
  tool.querySelector('[data-disclosure-reset]').addEventListener('click', () => choose('opening'));
  form.hidden = false;
  render(position);
  if (storageReadable && position !== 'opening') save.textContent = '이 브라우저에 저장된 위치를 불러왔어요.';
})();
