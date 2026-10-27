"""기본 mock 예제를 명시적 사람 승인 뒤 끝까지 실행한다."""
from core.workflow import make_draft, wordpress_connection
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft
from analytics.report import build_report


def run_demo(root, store, config, today, sample, config_path=None):
    if sample not in ('info', 'library') or config.get('wordpress', {}).get('mode') != 'mock':
        raise ValueError('전 과정 시연은 mock 정보 글만 가능 → 장별 draft·gate·publish를 사용하세요')
    if sample == 'library':
        return run_template_demo(root, store, config, today, config_path)
    doc = make_draft(root, store, sample, today, config_path=config_path)
    with wordpress_connection(root, config, today=today) as client:
        prepare_draft(root, store, client, doc, today, config_path=config_path)
        row = publish_draft(root, store, client, doc, today, config_path=config_path)
    build_report(root, store, today)
    print('✔ 통과: mock 초안 → 명시적 사람 승인 확인 → 예약 ' + str(row['post_id']))
    print('output/drafts/info.html\noutput/analytics/weekly.html')


def run_template_demo(root, store, config, today, config_path):
    """틀 승인은 미리 사람이 실행해야 하며 글별 승인을 만들지 않는다."""
    doc = make_draft(root, store, 'library', today, config_path=config_path)
    with wordpress_connection(root, config, today=today) as client:
        allowed = config.get('publishing', {}).get('auto_allowed_types', [])
        prepare_draft(root, store, client, doc, today, allowed, config_path=config_path)
        row = publish_draft(root, store, client, doc, today,
                            config.get('publishing', {}).get('mode', 'approval'), config_path=config_path)
    print('✔ 통과: mock 승인된 틀 + 검증 데이터 → 자동 예약 ' + str(row['post_id']))
    print('output/drafts/library.html')
