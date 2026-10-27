"""본문과 HTML에 숨은 상업·미허용 링크도 사람 검토에 연결한다."""
from pathlib import Path
import pytest
from content.samples import load_sample
from content.markdown import render
from core.approval import inspect_document
from core.state import Store
from gates.engine import evaluate

@pytest.mark.parametrize('text', [
    '[여기서 구매](https://link.coupang.com/a/abc123)',
    'https://LINK.COUPANG.COM/a/abc123',
    '<a href="//link.coupang.com/a/abc123">구매</a>',
    '<img src="https://shopping.naver.com/x">',
    '<img srcset="https://link.coupang.com/a/x 1x, https://example.test/x 2x">',
])
def test_all_commercial_body_urls_trigger_disclosure(text):
    doc = load_sample('info')
    doc['markdown'] += '\n\n' + text
    doc['html'] = render(doc['markdown']) + text
    rows = evaluate(doc)
    assert any(r['rule_id'].startswith('disclosure.D') and r['decision'] != 'pass' for r in rows)


def test_shop_link_with_visible_disclosure_still_needs_human(tmp_path):
    doc = load_sample('info')
    doc.update(media=[], markdown='이 링크로 구매하면 수수료를 받습니다.\n\n## 구매\n\n[구매](https://link.coupang.com/a/x)')
    doc['html'] = render(doc['markdown'])
    rows = inspect_document(tmp_path, doc, store=Store(tmp_path))
    assert any(r['rule_id'] == 'links.L1' and r['decision'] == 'review' for r in rows)


@pytest.mark.parametrize('url', ['https://evil.test/a', 'https://www.nl.go.kr.evil.test',
                                'https://www.nl.go.kr@evil.test', '//evil.test/x'])
def test_unknown_domains_require_human(tmp_path, url):
    doc = load_sample('info')
    doc['markdown'] += '\n\n[자료](' + url + ')'
    doc['html'] = render(doc['markdown'])
    (tmp_path / 'config.example.toml').write_text('[publishing]\nauto_allowed_domains=["www.nl.go.kr"]\n')
    rows = evaluate(doc, root=tmp_path)
    assert any(r['rule_id'] == 'links.L2' and r['decision'] == 'review' for r in rows)


@pytest.mark.parametrize('markup', ['<a href="/local">자료</a>', '[자료](/local)',
                                   '<a href="ftp://files.test/a">자료</a>'])
def test_relative_and_other_scheme_urls_are_also_reported(markup):
    from gates.links import link_checks
    rows = link_checks({'markdown': markup, 'html': markup}, None)
    assert any(r['rule_id'] == 'links.L2' for r in rows)


@pytest.mark.parametrize('markup', ['[ref]: /relative', '<button formaction="/submit">전송</button>'])
def test_reference_and_formaction_urls_are_reported(markup):
    from gates.links import link_checks
    assert any(r['rule_id'] == 'links.L2' for r in link_checks({'markdown': markup}, None))
