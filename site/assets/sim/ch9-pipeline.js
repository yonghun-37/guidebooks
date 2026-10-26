/* 로컬 생성·검수·승인·수정의 상태 모형. 실제 요청이나 파일 변경은 없다. */
(() => {
  'use strict';
  ReelsSim.mount('#ch9-flow', (root, report) => {
    const details = [
      '입력·초안: 소재를 확인하고 copy.json 구조와 출처를 검증합니다.',
      '카드·릴스: 같은 문안으로 이미지·영상·자막을 만듭니다.',
      '사람 검수: 실제 파일과 사실·권리·표시를 확인하고 그 파일에 승인을 남깁니다.',
      '드라이런: 승인한 묶음의 요청 계획을 미리 봅니다. 실제 게시나 계정 검증이 아닙니다.'
    ];
    ReelsSim.buttonGroup(root.querySelector('[data-flow-buttons]'), step => {
      root.querySelector('[data-flow-detail]').textContent = details[Number(step)];
      report(details[Number(step)]);
    });
  });
  ReelsSim.mount('#ch9-sim', (root, report) => {
    const inputs = ['copy', 'cards', 'reel', 'review'].map(name => root.querySelector(`#pipe-${name}`));
    const failure = root.querySelector('#pipe-failure');
    let generated = false, approved = false;
    const show = (message, lines) => {
      report(message);
      const log = root.querySelector('[data-pipe-log]');
      log.replaceChildren();
      lines.forEach(text => {
        const item = document.createElement('li');
        item.textContent = text;
        log.append(item);
      });
    };
    // Any changed input invalidates the old simulated artifacts and approval.
    const resetState = message => {
      generated = false; approved = false;
      show(message, ['입력 대기 · 생성과 승인을 새로 진행하세요.']);
    };
    root.addEventListener('change', () => resetState('연결·실패 조건 변경: 예전 결과와 승인은 무효입니다. 생성부터 다시 진행하세요.'));
    root.querySelectorAll('[data-pipe-action]').forEach(button => button.addEventListener('click', () => {
      const action = button.dataset.pipeAction;
      if (action === 'run') {
        generated = false; approved = false;
        const names = ['문안', '카드', '릴스', '사람 검수'];
        const stages = ['copy', 'cards', 'reel', 'review'];
        const log = ['입력 확인'];
        for (let i = 0; i < inputs.length; i += 1) {
          if (!inputs[i].checked) {
            show(`${names[i]} 연결 누락으로 중단했습니다. 검수를 건너뛰어 드라이런할 수 없습니다.`, [...log, `${names[i]}: 연결 누락`]);
            return;
          }
          if (failure.value === stages[i]) {
            show(`${names[i]} 단계 실패: ${failure.options[failure.selectedIndex].text}. 오류를 고친 뒤 다시 생성하세요. 기존 승인은 없습니다.`, [...log, `${names[i]}: 오류로 중단`]);
            return;
          }
          log.push(i === 3 ? '검수 대기 · 사람 확인 필요' : `${names[i]} 생성 완료`);
        }
        generated = true;
        show('생성 완료 · 사람 검수 대기. 아직 승인과 드라이런은 하지 않았습니다.', log);
      } else if (action === 'approve') {
        if (!generated) {
          show('승인 차단: 검수 가능한 생성 결과가 없습니다. 연결·오류를 고치고 생성하세요.', ['생성 결과 없음 → 승인 불가']);
          return;
        }
        approved = true;
        show('모형 속 사람 검수·승인 기록 완료. 승인 대상이 바뀌면 다시 검수합니다.', ['생성 완료', '사람 검수 완료로 가정', '현재 결과 승인']);
      } else if (action === 'edit') {
        resetState('문안 수정: 기존 승인은 무효입니다. 카드·릴스를 다시 생성하고 재검수·재승인하세요.');
      } else if (action === 'dryrun') {
        if (!generated || !approved) {
          show('드라이런 차단: 현재 파일의 승인이 없습니다. 생성 → 사람 검수·승인 순서로 진행하세요.', ['현재 승인 없음 → 드라이런 불가']);
          return;
        }
        show('드라이런 준비 완료: 캐러셀·릴스 요청 계획만 표시합니다. 실제 전송·게시·계정 확인은 없습니다.', ['승인 대상 확인', '캐러셀 요청 계획', '릴스 요청 계획', '실제 전송 없음']);
      }
    }));
    root.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
      const reset = button.dataset.preset === 'reset';
      inputs.forEach(input => { input.checked = true; });
      inputs[3].checked = reset;
      failure.value = reset ? 'none' : 'reel';
      resetState(reset ? '입력 대기: 생성 → 사람 검수·승인 → 드라이런 순서로 눌러 보세요.' : '무너뜨리기: 검수 연결 없음 + 음원 누락. 연결과 실패 조건을 모두 복구한 뒤 생성하세요.');
    }));
    resetState('입력 대기: 생성 → 사람 검수·승인 → 드라이런 순서로 눌러 보세요.');
  });
})();
