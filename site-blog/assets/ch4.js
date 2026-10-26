(() => {
  'use strict';
  const goal = document.getElementById('platform-goal');
  const api = document.getElementById('platform-api');
  const domain = document.getElementById('platform-domain');
  const render = () => {
    let choice;
    const conflict = goal.value === 'naver' && (api.value === 'yes' || domain.value !== 'no');
    if (conflict) {
      choice = '이 조건을 함께 충족하기 어렵습니다. 애드포스트·네이버 중심이면 네이버 블로그에서 직접 발행하세요. API가 필수면 Blogger, 독립 도메인은 티스토리·Blogger, 서버 관리는 설치형 WordPress로 목표를 바꿔 비교하세요.';
    } else if (domain.value === 'control') {
      choice = '설치형 WordPress: 서버·도메인·광고 자리를 관리할 수 있습니다. 보안·백업·갱신 비용과 시간을 먼저 적으세요.';
    } else if (api.value === 'yes') {
      choice = `Blogger: 무료 기본 호스팅과 공식 API가 있습니다. ${domain.value === 'yes' ? '독립 도메인은 따로 구매·연결하세요.' : '기본 blogspot 주소로 시작하세요.'} 애드센스는 별도 검토가 필요합니다.`;
    } else if (goal.value === 'adsense' || domain.value === 'yes') {
      choice = '티스토리: 직접 편집·애드센스 신청 경로와 개인 도메인 연결을 살펴보세요. 자체 광고와 광고 형식 제한을 확인합니다. 공식 API는 종료됐습니다.';
    } else {
      choice = '네이버 블로그: 오늘은 공식 편집기에서 첫 글을 공개하세요. 수익은 애드포스트·제휴의 신청 조건부터 확인합니다.';
    }
    document.getElementById('platform-count').textContent = conflict ? '0개 · 조건 재선택' : '1개부터 검토';
    document.getElementById('platform-choice').textContent = choice;
  };
  [goal,api,domain].forEach(input => input.addEventListener('change',render)); render();
})();
