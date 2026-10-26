/* 장 전용 도구. 입력은 브라우저 안에서만 계산하며 저장·외부 호출하지 않는다. */
(() => {
  'use strict';
  ReelsSim.mount('#chapter-figure', (element, report) => {
    ReelsSim.buttonGroup(element.querySelector('[data-figure-buttons]'), key => {
      report(element.querySelector(`[data-figure-note="${key}"]`).textContent);
    });
  });

  ReelsSim.mount('#planner-sim', (element, report) => {
    // 아래 분량은 교육용 배분이며 실측이 아니다.
    const tasks = [
      [1, '목표·독자·시간 메모', 45], [1, '수익 경로 가설 두 개', 30],
      [1, '니치·계정 기획 시트', 45], [1, '소재·권리표', 45], [1, '원문 대조·문안 초안', 60], [1, '첫 주 기획 점검', 25],
      [8, '카드 생성·레이아웃 점검', 60], [8, '릴스·자막 생성', 60], [8, '영상·음성·소재 권리 검수', 60], [8, '사실·가독성 수정', 45], [8, '제작 시간·두 번째 주 점검', 25],
      [15, '생성 파이프라인 연결', 45], [15, '변경 감지·사람 승인', 45], [15, '게시 드라이런 요청서', 45], [15, '예약 시각·시간대 설정표', 40], [15, '실패·중단·재검수 연습', 40], [15, '세 번째 주 실행 기록 점검', 35],
      [22, '지표표·실측/가상/미게시 구분', 45], [22, '정정·보안·게시 전 체크', 30], [22, '현금 비용·지급·시간 장부', 40], [22, '수익 경로와 단계별 증거', 35], [22, '교차 게시 한 곳의 권리·자격 검토', 45], [22, '주간표·다음 실험 한 가지', 35], [22, '30일 결과와 다음 기간 판단', 20]
    ];
    const start = element.querySelector('#plan-start');
    const minutes = element.querySelector('#plan-minutes');
    const days = element.querySelector('#plan-days');
    const calendar = element.querySelector('[data-calendar]');
    const copy = document.querySelector('[data-plan-copy]');
    const update = () => {
      calendar.replaceChildren();
      if (!start.value || !start.checkValidity() || !minutes.value || !minutes.checkValidity()) {
        report('날짜와 확보 시간을 유효하게 입력하세요.'); copy.textContent = '유효한 날짜와 확보 시간 입력 후 일정을 복사하세요.'; return;
      }
      const first = new Date(start.value + 'T00:00:00Z');
      if (!Number.isFinite(first.getTime())) { report('시작 날짜를 확인하세요.'); copy.textContent = '시작 날짜 확인 필요.'; return; }
      const daily = Number(minutes.value), activeDays = Number(days.value), review = Math.min(10, daily);
      const workBudget = Math.max(0, daily - review);
      let index = 0, remaining = tasks[0][2], used = 0, reviewTotal = 0, buffer = 0;
      const rows = [];
      for (let day = 1; day <= 30; day++) {
        const date = new Date(first); date.setUTCDate(first.getUTCDate() + day - 1);
        const label = `${day}일차 · ${date.toISOString().slice(0,10)}`;
        let description;
        if ((day - 1) % 7 >= activeDays) description = '휴식 · 작업 배치 없음';
        else {
          let available = workBudget;
          const pieces = [];
          reviewTotal += review;
          while (available > 0 && index < tasks.length && tasks[index][0] <= day) {
            const spend = Math.min(available, remaining);
            remaining -= spend; available -= spend; used += spend;
            pieces.push(`${tasks[index][1]} ${spend}분${remaining ? ' (이어하기)' : ''}`);
            if (!remaining) { index++; remaining = index < tasks.length ? tasks[index][2] : 0; }
          }
          buffer += available;
          description = `점검 ${review}분` + (pieces.length ? ' / ' + pieces.join(' / ') : ' / 핵심 작업 배치 없음') + (available ? ` / 여유·휴식 ${available}분` : '');
        }
        rows.push(`${label}: ${description}`);
        const item = document.createElement('li'), title = document.createElement('strong');
        title.textContent = label; item.append(title, document.createTextNode(description)); calendar.append(item);
      }
      const unplaced = index >= tasks.length ? 0 : remaining + tasks.slice(index + 1).reduce((sum, task) => sum + task[2], 0);
      const pending = index >= tasks.length ? '미배치 핵심 작업 없음.' : '다음 기간으로: ' + tasks.slice(index).map((task, i) => `${task[1]} ${i ? task[2] : remaining}분`).join(' / ');
      const summary = `30일 중 핵심 작업 배치 ${used}분, 점검 ${reviewTotal}분, 여유·휴식 예산 ${buffer}분.\n작업 ${tasks.length}개 중 분량을 모두 배치한 작업 ${index}개. 남은 분량 ${unplaced}분. 실제 완료는 결과물 확인 후 표시하세요.\n${pending}`;
      report(summary); copy.textContent = '30일 작업 후보표 · 교육용 가정 모형\n' + rows.join('\n') + '\n\n' + summary;
    };
    element.querySelectorAll('input, select').forEach(input => input.addEventListener('input', update));
    element.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      minutes.value = button.dataset.preset === 'break' ? 0 : 60; days.value = 5; update();
    }));
    update();
  });

})();
