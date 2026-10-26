/* 검색 서비스 UI·순위·길이 제한의 재현이 아닌, 제목 배치 연습이다. */
(() => {
  'use strict';
  const title = document.querySelector('#search-title');
  if (!title) return;
  const description = document.querySelector('#search-description');
  const device = document.querySelector('#search-device');
  const initial = {title: title.value, description: description.value};
  const render = () => {
    const text = title.value.trim();
    document.querySelector('#search-preview-title').textContent = text || '제목을 입력하세요';
    document.querySelector('#search-preview-description').textContent = description.value.trim() || '독자에게 줄 답을 설명에 적으세요.';
    document.querySelector('#search-preview').dataset.device = device.value;
    document.querySelector('[data-search-result]').textContent = text ? `제목 ${Array.from(text).length}자입니다. 말줄임이 생겨도 주제와 질문이 남는지 확인하세요.` : '제목을 입력하고 미리보기에서 핵심이 앞에 오는지 확인하세요.';
  };
  [title, description].forEach(input => input.addEventListener('input', render));
  device.addEventListener('change', render);
  document.querySelector('#search-long').addEventListener('click', () => { title.value = '퇴근하고 바쁜 하루를 보낸 직장인이라면 누구나 꼭 한 번쯤 읽어 보아야 하는 아주 유용한 생활 정보 모음: 지원 제도 신청 대상과 준비물 확인하기'; render(); });
  document.querySelector('#search-reset').addEventListener('click', () => { title.value = initial.title; description.value = initial.description; device.value = 'mobile'; render(); });
  render();
})();
