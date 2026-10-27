"""기본 mock 예제를 가상 승인 시연과 함께 끝까지 실행한다."""
from core.workflow import make_draft, wordpress_connection
from core.approval import approve_document
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft
from analytics.report import build_report


def run_demo(root, store, config, today, sample):
    if sample != 'info' or config.get('wordpress', {}).get('mode') != 'mock':
        raise ValueError('전 과정 시연은 mock 정보 글만 가능 → 장별 draft·gate·publish를 사용하세요')
    doc = make_draft(root, store, sample, today)
    with wordpress_connection(root, config, today=today) as client:
        prepare_draft(root, store, client, doc, today)
        approve_document(root, store, doc, '가상 승인 시연', today)
        row = publish_draft(root, store, client, doc, today)
    build_report(root, store, today)
    print('✔ 통과: mock 초안 → 가상 사람 승인 시연 → 예약 ' + str(row['post_id']))
    print('output/drafts/info.html\noutput/analytics/weekly.html')
