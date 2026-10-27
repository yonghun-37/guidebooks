"""장 번호가 있는 한국어 명령 도움말을 구성한다."""
import argparse

DESCRIPTIONS = {
    'topics': 'A3 월령·발달·제도·놀이·그림책 주제 지도',
    'draft': 'A4 JSON 초안과 비어 있는 사람 경험 칸',
    'gate': 'A5 자동 관문 검사와 별도의 사람 승인',
    'publish': 'A6 WordPress 초안 저장과 승인 후 예약',
    'pages': 'A2 소개·개인정보·문의·광고 정책 페이지',
    'ads': 'A7 광고 준비 점검·ads.txt·광고 위치',
    'affiliate': 'A8 수동 제휴 링크 대장과 대가성 문구',
    'sponsor': 'A9 협찬 대장과 가상 거절·수락·정산',
    'report': 'A10 주간 보고서와 다음 글감',
    'run': 'A11 운영 도구 / A12 출시 점검 / mock 전 과정',
    'status': 'A1 mock 연결 / A6·A11 서버 공개 상태 확인',
}


def make_parser():
    parser = argparse.ArgumentParser(description='봄이랑 크는 집 · 코드 운영 실습')
    parser._positionals.title = '명령'
    parser._optionals.title = '선택 항목'
    commands = parser.add_subparsers(dest='command', required=True)
    for name, description in DESCRIPTIONS.items():
        sub = commands.add_parser(name, help=description, description=description)
        sub.add_argument('--today', default=None, help='고정 기준일 YYYY-MM-DD(기본 설정 날짜)')
        sub.add_argument('--config', default=None, help='TOML 설정 파일(기본 config.toml 또는 예제)')
        sub.add_argument('--live', action='store_true', help='본인 .env로 실제 연결(기본 드라이런)')
        add_options(sub, name)
    return parser


def add_options(sub, name):
    if name in ('draft', 'gate', 'publish', 'affiliate', 'status', 'run'):
        sub.add_argument('--sample', nargs='?', const='info', default='info',
                         choices=('info', 'play', 'affiliate', 'sponsor'), help='가상 글 선택')
    if name == 'draft':
        sub.add_argument('--human-notes', action='store_true', help='가상 사람 메모를 명시적으로 적용')
    if name == 'gate':
        sub.add_argument('--approve', metavar='검토자', help='현재 최종본을 사람이 검토하고 승인')
    if name == 'publish':
        sub.add_argument('--prepare', action='store_true', help='공개하지 않고 서버 초안 저장')
    if name == 'status':
        sub.add_argument('--costs', action='store_true', help='A4 비용 예약·확정 기록 읽기(서버 연결 없음)')
        sub.add_argument('--mock', action='store_true', help='내장 mock 서버에 실제 HTTP 연결 검사')
        sub.add_argument('--advance-days', type=int, default=0, help='mock 시계만 앞으로 이동')
    if name == 'sponsor':
        sub.add_argument('action', choices=('demo', 'review', 'settle', 'status'), nargs='?', default='status')
    if name == 'run':
        for flag, help_text in [('ops', 'A11 알림·백업·예약 예시'),
                                ('restore', 'A11 저장된 백업 복원'),
                                ('audit', 'A12 출시 전 점검표'),
                                ('scenarios', '7종 안전·복구 시나리오')]:
            sub.add_argument('--' + flag, action='store_true', help=help_text)
