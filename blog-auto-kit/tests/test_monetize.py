"""협찬 전이와 제휴 문구·보고서를 검증한다."""
import unittest
from monetize.sponsor.ledger import create_inquiry, transition
from monetize.affiliate import prepare_affiliate


class Store:
    def __init__(self): self.tables = {}
    def get(self, table, key, default=None): return self.tables.get(table, {}).get(key, default)
    def put(self, table, key, value): self.tables.setdefault(table, {})[key] = value
    def all(self, table): return list(self.tables.get(table, {}).values())


class SponsorTests(unittest.TestCase):
    def test_transition_requires_records_and_prevents_wrong_resume(self):
        store = Store()
        create_inquiry(store, 'a', {'advertiser': '가상', 'contact': 'x', 'offer': '물품', 'channel': '블로그'}, '2026-10-27')
        with self.assertRaises(ValueError): transition(store, 'a', 'reviewing', {}, '2026-10-27')
        transition(store, 'a', 'on_hold', {'reason': '확인', 'request': '자료', 'owner': '나', 'return_state': 'inquiry', 'deadline': '2026-11-01'}, '2026-10-27')
        with self.assertRaises(ValueError): transition(store, 'a', 'contracted', {}, '2026-10-27')

    def test_every_transition_requires_records(self):
        from monetize.sponsor.states import STATES
        for source, (_, targets) in STATES.items():
            for target in targets:
                store = Store()
                store.put('sponsors', 'x', {'id': 'x', 'state': source, 'history': [{'state': source, 'records': {}}]})
                with self.subTest(source=source, target=target), self.assertRaises(ValueError):
                    transition(store, 'x', target, {}, '2026-10-27')

    def test_affiliate_marks_only_registered_links(self):
        import tempfile
        from monetize.affiliate import register_link
        store = Store()
        register_link(store, {'id': 'a', 'url': 'https://example.test/a'})
        with tempfile.TemporaryDirectory() as root:
            result = prepare_affiliate(root, store, {'html': '<a href="https://example.test/a">광고</a><a href="https://example.test/b">출처</a>', 'commercial_relations': []})
        self.assertIn('href="https://example.test/a" rel="sponsored"', result['html'])
        self.assertIn('<a href="https://example.test/b">', result['html'])

    def test_live_api_unavailable(self):
        from monetize.affiliate import live_coupang
        with self.assertRaises(NotImplementedError): live_coupang()

    def test_analytics_adapters_empty_and_timezone(self):
        from analytics.adapters import fetch_ga4, fetch_gsc
        ga = fetch_ga4('p', '2026-10-01', '2026-10-27', lambda req: {'rows': [], 'metadata': {'timeZone': 'Asia/Seoul'}})
        gsc = fetch_gsc('s', '2026-10-01', '2026-10-27', lambda req: {})
        self.assertTrue(ga['empty']); self.assertEqual(ga['timezone'], 'Asia/Seoul')
        self.assertTrue(gsc['empty']); self.assertIn('지연', gsc['note'])
        self.assertEqual(gsc['timezone'], 'America/Los_Angeles')

    def test_demo_stops_before_human_approval(self):
        import tempfile
        from monetize.sponsor.demo import run_sponsor_demo
        store = Store()
        with tempfile.TemporaryDirectory() as root: run_sponsor_demo(root, store, '2026-10-27')
        self.assertEqual(store.get('sponsors', 'shelf')['state'], 'brand_review')
        self.assertEqual(store.get('sponsors', 'shelf')['content_id'], 'sponsor')

    def test_old_dated_amount_post_requires_update(self):
        import tempfile
        from pathlib import Path
        from analytics.report import build_report
        store = Store()
        store.put('posts', 'x', {'title': '지원금', 'as_of': '2025-01-01', 'markdown': '2025년 지원금 100원'})
        with tempfile.TemporaryDirectory() as root:
            content = Path(build_report(root, store, '2026-10-27')[0]).read_text(encoding='utf-8')
        self.assertIn('지원금</li>', content)

    def test_hold_resumes_only_original_state_and_requires_records(self):
        store = Store()
        create_inquiry(store, 'a', {'advertiser': '가상', 'contact': 'x', 'offer': '물품', 'channel': '블로그'}, '2026-10-27')
        transition(store, 'a', 'on_hold', {'reason': '확인', 'request': '자료', 'owner': '나', 'return_state': 'inquiry', 'deadline': '2026-11-01'}, '2026-10-27')
        with self.assertRaises(ValueError): transition(store, 'a', 'inquiry', {}, '2026-10-28')
        row = transition(store, 'a', 'inquiry', {'advertiser': '가상', 'contact': 'x', 'offer': '물품', 'channel': '블로그'}, '2026-10-28')
        self.assertEqual(row['state'], 'inquiry')

    def test_human_written_path_does_not_require_ai(self):
        from monetize.sponsor.demo import run_sponsor_demo
        import tempfile
        store = Store()
        with tempfile.TemporaryDirectory() as root: run_sponsor_demo(root, store, '2026-10-27')
        entries = store.get('sponsors', 'shelf')['history']
        review = next(x for x in entries if x['state'] == 'reviewing')
        writing = next(x for x in entries if x['state'] == 'writing')
        self.assertIs(review['records']['ai_allowed'], False)
        self.assertTrue(writing['records']['authoring_path'])

    def test_offer_contract_and_product_classification(self):
        from monetize.sponsor.ledger import assess_offer
        product = {'product_type': '그림책꽂이', 'intended_use': '정리', 'model': 'A', 'maker': '가상', 'certification_scheme': '확인', 'recall_check': '확인', 'ad_review_scope': '확인'}
        doc = {'product_records': [product], 'contract': {'ai_allowed': False}, 'commercial_relations': [{'kind': 'sponsor'}]}
        self.assertEqual(assess_offer(doc)['decision'], 'accepted')
        doc['contract']['ai_allowed'] = None
        self.assertEqual(assess_offer(doc)['decision'], 'on_hold')
        doc['contract'] = {'ai_allowed': True, 'requires_false_review': True}
        self.assertEqual(assess_offer(doc)['decision'], 'declined')
        doc['contract'] = {'ai_allowed': True}
        doc['product_records'][0]['product_type'] = '조제유류'
        doc['commercial_relations'] = []
        self.assertNotEqual(assess_offer(doc)['decision'], 'declined')

    def test_sponsor_reports_regenerate_and_keep_tax_fields(self):
        import csv
        import tempfile
        from pathlib import Path
        from monetize.sponsor.demo import run_sponsor_demo, export_reports
        store = Store()
        with tempfile.TemporaryDirectory() as root:
            run_sponsor_demo(root, store, '2026-10-27')
            shelf = store.get('sponsors', 'shelf')
            shelf['state'] = 'published'
            shelf['history'].append({'state': 'published', 'date': '2026-10-27', 'records': {'url': 'https://example.test/published'}})
            store.put('sponsors', 'shelf', shelf)
            export_reports(root, store, '2026-10-27')
            base = Path(root) / 'output' / 'sponsor'
            self.assertIn('https://example.test/published', (base / 'advertiser-report.html').read_text())
            self.assertIn('<table>', (base / 'media-kit.html').read_text())
            with (base / 'tax.csv').open() as stream:
                row = next(csv.DictReader(stream))
            self.assertTrue({'date', 'cash', 'goods', 'valuation_basis', 'withholding', 'paid_amount', 'evidence', 'tax_guide'} <= row.keys())
