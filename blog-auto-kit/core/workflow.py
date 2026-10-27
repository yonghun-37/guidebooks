"""원고 파일과 mock 또는 실제 WordPress 연결을 준비한다."""
from contextlib import contextmanager
from datetime import date, timedelta
from urllib.parse import urlsplit
from content.samples import load_sample, with_human_notes
from core.config import read_secrets
from core.files import read_json, write_json, write_text
from providers.mock import draft_sample
from providers.costs import reserve_cost, settle_cost
from wordpress.client import Client
from wordpress.mock_server import running_server


def draft_path(root, name):
    return root / 'output/drafts' / (name + '.json')


def read_document(root, name):
    path = draft_path(root, name)
    if not path.exists():
        raise ValueError('초안 없음 → python blog.py draft --sample ' + name)
    return read_json(path)


def make_draft(root, store, name, today, human_notes=False, config=None):
    config = config or {}
    allowed = None
    if name == 'sponsor':
        sponsor = store.get('sponsors', 'shelf', {})
        review = next((e['records'] for e in reversed(sponsor.get('history', [])) if e['state'] == 'reviewing'), {})
        allowed = review.get('ai_allowed')
        if not human_notes and allowed is not True:
            raise ValueError('협찬 계약 AI 허용 미확인 → 사람 작성 또는 계약 확인이 필요합니다')
    if human_notes:
        doc = with_human_notes(load_sample(name))
        doc['authoring_path'] = '사람 작성(가상 시연)'
    else:
        contract = load_sample(name).get('contract', {})
        if contract.get('ai_allowed') is not True:
            raise ValueError('AI 허용 미확인 → 계약을 확인하거나 draft --human-notes로 작성하세요')
        key = 'draft:' + name + ':' + today
        if store.get('costs', key) is None:
            reserve_cost(store, key, '0', today, config.get('monthly_cap_usd', '1.00'))
            settle_cost(store, key, '0', today)
        doc = draft_sample(name, today)
    if name == 'sponsor':
        doc['contract'] = dict(doc.get('contract', {}), ai_allowed=allowed)
    doc['as_of'] = today
    save_document(root, doc)
    return doc


def save_document(root, doc):
    write_json(draft_path(root, doc['content_id']), doc)
    write_text(root / 'output/drafts' / (doc['content_id'] + '.html'), doc['html'])


@contextmanager
def wordpress_connection(root, config, live=False, today='2026-10-27', advance=0):
    wp = config.get('wordpress', {})
    mode = wp.get('mode', 'mock')
    if mode == 'mock':
        moved = (date.fromisoformat(today) + timedelta(days=advance)).isoformat()
        with running_server(root, port=0, today=moved) as url:
            yield Client(url)
        return
    if not live:
        yield None
        return
    url = wp['url']; parsed = urlsplit(url)
    local = parsed.hostname in ('127.0.0.1', 'localhost') and mode == 'local'
    if (parsed.scheme != 'https' and not local) or parsed.username or parsed.password:
        raise ValueError('운영 HTTPS 필요 → wordpress.url을 인증정보 없는 HTTPS 주소로 고치세요')
    values = read_secrets(root)
    if not values.get('WP_USERNAME') or not values.get('WP_APP_PASSWORD'):
        raise ValueError('인증정보 없음 → .env에 WP_USERNAME과 WP_APP_PASSWORD를 넣으세요')
    yield Client(url, values['WP_USERNAME'], values['WP_APP_PASSWORD'], destination=url)
