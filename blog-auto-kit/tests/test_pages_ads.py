"""문의 항목과 처리방침·광고 자리표시의 정합성을 검사한다."""
import json
from monetize.pages import generate_pages
from monetize.ads import build_ads


def test_contact_and_policy_share_minimum_fields(tmp_path):
    generate_pages(tmp_path, {'email': 'editor@example.invalid', 'retention_days': 30}, '2026-10-27')
    policy = (tmp_path / 'output/pages/privacy.html').read_text()
    contact = (tmp_path / 'output/pages/contact.html').read_text()
    assert '이메일' in policy and '문의 내용' in policy and '30일' in policy
    assert '파기' in policy and '권리' in policy and '수집하지' in policy
    assert 'name="email"' in contact and 'name="message"' in contact
    assert 'disabled' in contact


def test_ads_publisher_placeholder_and_no_approval_count_rule(tmp_path):
    build_ads(tmp_path, {'publisher_id': 'pub-REPLACE_ME', 'ad_after_h2': 1}, '2026-10-27')
    text = (tmp_path / 'output/ads/ads.txt').read_text()
    assert 'pub-REPLACE_ME' in text
    assert 'google.com' in text
    checklist = (tmp_path / 'output/ads/checklist.txt').read_text()
    assert '최소 글 수' in checklist and '공식 기준 없음' in checklist
    metrics = json.loads((tmp_path / 'output/ads/metrics.json').read_text())
    assert metrics['mock'] is True
    assert metrics['estimated_usd'] == '0.12' and metrics['paid_usd'] == '0.00'
