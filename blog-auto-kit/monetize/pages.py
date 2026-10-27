"""운영 안내용 정적 페이지를 만든다."""
from html import escape
from pathlib import Path


def generate_pages(root, config, today):
    """개인정보 의무와 권장 안내 페이지를 구분해 생성한다."""
    base = Path(root) / 'output' / 'pages'
    base.mkdir(parents=True, exist_ok=True)
    email = escape(str(config.get('email', '문의 이메일을 설정하세요')))
    days = int(config.get('retention_days', 30))
    privacy = (f'이 정적 양식은 정보를 수집하지 않습니다. 연결할 경우의 수집 항목은 이메일과 문의 내용입니다. '
               f'목적은 문의 답변이며 답변 완료 후 {days}일 보유하고 파일과 메일을 파기하는 예시입니다. '
               f'동의를 거부할 권리가 있으며 거부하면 답변을 받을 수 없습니다. 열람·정정·삭제 등 권리 행사와 '
               f'처리 담당자 연락은 {email}로 요청하는 예시입니다. 실제 운영 전 연락처·파기 주기·처리근거를 확정하세요. '
               '현재는 쿠키·분석·광고·위탁·제3자 제공·국외 이전을 연결하지 않았습니다. '
               '연결하면 실제 업체·항목·보유기간·이전 근거와 자동 수집 거부 방법을 추가하세요.')
    pages = {
        'about.html': ('소개 (권장)', '가상 육아·교육 블로그입니다.'),
        'privacy.html': ('개인정보처리방침 (실제 처리 시 의무)', privacy),
        'contact.html': ('문의 (권장)', f'연락처: {email}. 이메일과 문의 내용만 받는 미연결 양식입니다. '
                         f'답변 목적, 답변 완료 후 {days}일 보유·파기하는 예시이며 동의를 거부하면 답변을 받을 수 없습니다. '
                         '실제 처리방침 확정 전 전송을 연결하지 마세요.'),
        'advertising.html': ('광고·협찬 정책 (권장)', '경제적 이해관계를 첫 부분에 밝히고 실제 경험만 기록합니다.'),
    }
    for name, (title, body) in pages.items():
        form = ('<form><fieldset disabled><label>이메일<input type="email" name="email"></label>'
                '<label>문의 내용<textarea name="message"></textarea></label>'
                '<label><input type="checkbox">문의 답변을 위한 수집·이용 동의</label>'
                '<button type="button">전송 미연결</button></fieldset></form>') if name == 'contact.html' else ''
        (base / name).write_text(f'<!doctype html><html lang="ko"><meta charset="utf-8"><title>{title}</title><h1>{title}</h1><p>{body}</p>{form}<p>기준일 {escape(today)}</p></html>', encoding='utf-8', newline='\n')
    return [str(base / name) for name in pages]
