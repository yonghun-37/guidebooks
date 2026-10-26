(() => { 'use strict';
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
 const id=button.dataset.copy, node=document.getElementById(id), status=document.querySelector(`[data-copy-status="${id}"]`);
 const value=node.value ?? node.textContent;
 try {await navigator.clipboard.writeText(value);status.textContent='복사했습니다. 내 메모와 출처를 채워 넣으세요.';}
 catch {status.textContent='자동 복사를 사용할 수 없습니다. 아래 글을 선택해 복사하세요.'; if(node.select){node.focus();node.select();}else{const range=document.createRange();range.selectNodeContents(node);const selection=getSelection();selection.removeAllRanges();selection.addRange(range);}}
}));
const days=[["독자·질문", "도울 독자와 해결할 질문을 정합니다.", "독자·질문 메모"], ["내 자료", "{materials}를 모읍니다.", "실제 자료 목록"], ["도구 준비", "ChatGPT 새 대화에서 자료를 넣고 부족한 점을 질문받습니다.", "빠진 자료 메모"], ["키워드", "데이터랩에서 같은 기간의 흐름을 비교하고 선택 이유를 씁니다.", "키워드·선택 이유"], ["개요", "검수한 자료로 제목·첫 답변·소제목을 받습니다.", "근거가 연결된 개요"], ["초안", "내 메모만 써서 초안을 만들고 직접 읽습니다.", "출처·경험이 보이는 초안"], ["첫 공개", "원문·권리·표시·모바일을 확인하고 공식 편집기로 공개합니다.", "공개 URL 또는 남은 수정 항목"], ["발행 확인", "다른 브라우저에서 공개 글·사진·링크를 읽습니다.", "공개 상태 기록"], ["시간 기록", "자료·초안·검수에 실제 쓴 분을 나눠 적습니다.", "작업시간 메모"], ["두 번째 질문", "첫 글에서 못 푼 다음 질문을 고릅니다.", "다음 독자 질문"], ["추가 자료", "두 번째 글에 필요한 {materials}를 보완합니다.", "새로 확인한 자료"], ["후속 초안", "ChatGPT에 새 자료만 넣고 개요·초안을 나눠 받습니다.", "후속 초안"], ["사진·구조", "직접 사진 또는 Canva·미리캔버스의 무료 요소로 설명을 만듭니다.", "권리를 적은 이미지·표"], ["두 번째 공개", "검수한 글을 공개합니다. 미완성이면 수정 목록부터 끝냅니다.", "공개 URL 또는 검수 목록"], ["주간 기록", "같은 기간의 방문·검색·수입 상태를 기록합니다.", "보고서 이름·기간·값"], ["검색 질문", "유입 검색어와 글의 첫 답변을 대조합니다.", "맞지 않는 질문 하나"], ["옛 글 보완", "빠진 답·깨진 링크·오래된 조건 중 하나를 고칩니다.", "수정 내역·날짜"], ["다음 자료", "{next}에 필요한 실제 메모와 사진을 확인합니다.", "후속 글의 자료 목록"], ["다음 개요", "자료가 있는 범위에서 제목·개요를 받습니다.", "사람이 확인한 개요"], ["사실 대조", "원문 날짜·숫자·단위와 내 관찰을 대조합니다.", "문단별 근거표"], ["다음 공개", "내용·권리·표시가 준비된 글만 발행합니다.", "공개 URL 또는 보완 메모"], ["수익 조건", "애드포스트·애드센스·제휴 중 내 경로의 조건을 확인합니다.", "신청 상태 또는 다음 확인일"], ["정산·세금", "수익원·예상·확정·입금·비용 증빙을 나눠 모읍니다.", "정산 기록·질문 목록"], ["반복 틀", "이번 달에 쓴 자료 칸·검수 순서를 저장합니다.", "다음 글 양식"], ["예약 선택", "완성 원고가 있으면 공식 예약을 고르고 없으면 보완합니다.", "예약 상태 또는 보완 목록"], ["숫자 비교", "같은 기간·필터의 CTR·RPM을 따로 비교합니다.", "계산식·다음 수정 하나"], ["도움 확인", "독자 질문에 빠진 답이 있는지 다시 읽습니다.", "보완할 답 하나"], ["부담 점검", "재미·자료 확보·작업시간을 돌아봅니다.", "유지·줄일 작업"], ["다음 달 결정", "유지할 주제와 줄일 반복 작업을 고릅니다.", "다음 달 선택 이유"], ["계획 저장", "공개 주소·실제 시간·변경 내역과 다음 행동을 정리합니다.", "다음 달 시작 메모"]];
const materials={"info": "공식 공고·확인일·대상·절차 메모", "review": "실제 한 달 사용 메모·사진·제공 관계", "travel": "내 당일치기 동선·사진·놓친 점", "all": "내 당일치기 동선·사진·놓친 점"};
const nexts={"info": "다음 지원 제도 질문", "review": "사용 환경이 다른 독자의 질문", "travel": "다음 여행자의 준비 질문", "all": "지원 제도 신청 방법과 실제 한 달 생활 가전 후기"};
const $=id=>document.getElementById(id), form=$('plan-form');
const update=()=>{
 const raw=$('plan-start').value,work=Number($('plan-work').value),date=new Date(raw+'T12:00:00');
 const validDate=/^\d{4}-\d{2}-\d{2}$/.test(raw)&&Number.isFinite(date.getTime())&&date.getFullYear()>=1&&date.getFullYear()<=9998;
 const validWork=$('plan-work').value.trim()!==''&&Number.isInteger(work)&&work>=10&&work<=30;
 $('plan-start').setAttribute('aria-invalid',String(!validDate));$('plan-work').setAttribute('aria-invalid',String(!validWork));
 if(!validDate||!validWork){$('plan-value').textContent='입력 확인';$('plan-meaning').textContent='시작일을 고르고 작업 시간을 10~30분의 정수로 넣으세요.';$('plan-body').replaceChildren();$('plan-export').value='';document.querySelector('[data-copy="plan-export"]').disabled=true;$('plan-budget').textContent='';return;}
 const focus=$('plan-focus').value,noReview=$('plan-used').value==='no'&&['all','review'].includes(focus),verify=50-work;
 const mat=noReview&&focus==='review'?'공식 사양·원문과 앞으로 모을 실제 사용 메모':materials[focus];
 const next=noReview?'생활 가전의 공식 사양 정보와 실제 사용 기록 준비':nexts[focus];
 const budget=`매일 작업 ${work}분 + 검수·보완 ${verify}분 + 기록 10분 = 60분`;
 $('plan-value').textContent='30시간';$('plan-meaning').textContent=noReview?'실제 사용 메모가 없으므로 후기 대신 공식 사양 정보·사용 기록 준비로 바꿉니다.':'준비·공개·수정·관찰을 나누고, 미완성 작업은 다음 날로 이어 씁니다.';$('plan-budget').textContent=budget;
 const lines=['하루 60분 × 30일 = 30시간',budget,noReview?'후기 자료 없음: 공식 사양 정보 또는 실제 사용 기록부터 준비':'내 자료가 있는 범위에서만 작성'];
 const fragment=document.createDocumentFragment();
 days.forEach(([name,task,output],index)=>{
  const day=new Date(date);day.setDate(day.getDate()+index);
  const stamp=`${String(day.getFullYear()).padStart(4,'0')}-${String(day.getMonth()+1).padStart(2,'0')}-${String(day.getDate()).padStart(2,'0')}`;
  task=task.replace('{materials}',mat).replace('{next}',next);
  const row=document.createElement('tr'),head=document.createElement('th');head.scope='row';head.textContent=`${index+1}일 · ${stamp}`;row.append(head);
  const topic=document.createElement('td');topic.dataset.label='주제';topic.textContent=name;row.append(topic);
  const details=document.createElement('td');details.dataset.label='할 일·남길 것';details.textContent=task;details.append(document.createElement('br'));const strong=document.createElement('strong');strong.textContent='남길 것: ';details.append(strong,output);row.append(details);
  const done=document.createElement('td');done.dataset.label='확인';const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.setAttribute('aria-label',`${index+1}일 작업 확인`);label.append(input,'완료');done.append(label);row.append(done);fragment.append(row);
  lines.push(`${index+1}일 ${stamp} | ${name} | ${task} | 남길 것: ${output}`);
 });
 document.querySelector('[data-copy="plan-export"]').disabled=false;$('plan-body').replaceChildren(fragment);$('plan-export').value=lines.join('\n');
 const copyStatus=document.querySelector('[data-copy-status="plan-export"]');copyStatus.textContent='';
};
form.addEventListener('submit',e=>{e.preventDefault();update();});
$('plan-extreme').addEventListener('click',()=>{$('plan-focus').value='review';$('plan-used').value='no';update();});
$('plan-reset').addEventListener('click',()=>{form.reset();update();});
update();
})();