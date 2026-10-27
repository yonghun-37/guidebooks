"""발행 관문의 안전 차단과 보고서를 검증한다."""
import tempfile
import unittest
from pathlib import Path
from content.samples import load_sample, with_human_notes
from gates.engine import evaluate, write_report
from gates.risk import requires_human
from gates.privacy_exif import inspect_exif, strip_exif

class GateTests(unittest.TestCase):
    def test_info_passes_and_health_cannot_bypass_review(self):
        self.assertFalse(any(r['decision'] != 'pass' for r in evaluate(load_sample('info'))))
        doc = load_sample('play'); doc['risk_flags'] = []
        self.assertTrue(requires_human(doc))
        self.assertTrue(any(r['rule_id'] == 'health_safety.H1' and r['human_resolvable'] for r in evaluate(doc)))

    def test_experience_disclosure_and_sleep_product(self):
        doc = load_sample('sponsor')
        self.assertTrue(any(r['rule_id'] == 'disclosure.D4' and r['decision'] == 'block' for r in evaluate(doc)))
        self.assertFalse(any(r['decision'] == 'block' for r in evaluate(with_human_notes(doc))))
        doc['product_records'][0]['intended_use'] = '영아 낮잠 이불'
        self.assertTrue(any(r['rule_id'] == 'product_rules.P7' for r in evaluate(doc)))

    def test_exif_removed_and_report_written(self):
        data = (Path(__file__).resolve().parents[1] / 'samples' / 'fake-exif.jpg').read_bytes()
        self.assertTrue(inspect_exif(data))
        self.assertEqual(inspect_exif(strip_exif(data)), [])
        with tempfile.TemporaryDirectory() as tmp:
            doc = load_sample('info'); write_report(Path(tmp), doc, evaluate(doc))
            self.assertTrue((Path(tmp) / 'output/gates/info.json').exists())
            self.assertTrue((Path(tmp) / 'output/queue.json').exists())

    def test_missing_source_and_product_information_are_not_resolvable_by_approval(self):
        doc = load_sample('play'); doc['source_notes'] = []
        finding = next(r for r in evaluate(doc) if r['rule_id'] == 'health_safety.H2')
        self.assertFalse(finding['human_resolvable'])
        doc = load_sample('sponsor'); doc['product_records'][0]['recall_check'] = 'unknown'
        self.assertFalse(next(r for r in evaluate(doc) if r['rule_id'] == 'product_rules.P3')['human_resolvable'])

    def test_emergency_text_must_match(self):
        doc = load_sample('play'); doc['emergency_topics'] = ['fever']
        self.assertTrue(any(r['rule_id'] == 'health_safety.H4' and r['decision'] == 'block' for r in evaluate(doc)))

    def test_jpeg_with_exif_is_blocked_when_referenced(self):
        doc = load_sample('info')
        doc['media'][0]['path'] = 'samples/fake-exif.jpg'
        self.assertTrue(any(r['rule_id'] == 'child_privacy.C2' and r['decision'] == 'block' for r in evaluate(doc)))

    def test_structured_output_and_sensitive_details(self):
        doc = load_sample('play'); doc['generation_status'] = 'truncated'
        self.assertTrue(any(r['rule_id'] == 'health_safety.H5' for r in evaluate(doc)))
        doc = load_sample('info'); doc['markdown'] += '\n아이 생일: 2026-01-02'
        self.assertTrue(any(r['rule_id'] == 'child_privacy.C2' and r['decision'] == 'block' for r in evaluate(doc)))
        doc['contact_form'] = {'data_minimized': False}
        self.assertTrue(any(r['rule_id'] == 'child_privacy.C4' for r in evaluate(doc)))

    def test_disclosure_location_photos_and_multiple_relations(self):
        doc = load_sample('affiliate'); doc['markdown'] = '본문\n\n제휴 수수료를 받습니다.'
        self.assertTrue(any(r['rule_id'] == 'disclosure.D2' for r in evaluate(doc)))
        doc = load_sample('affiliate'); doc['media'][0]['independent_reuse'] = True
        self.assertTrue(any(r['rule_id'] == 'disclosure.D3' for r in evaluate(doc)))
        doc['commercial_relations'].append({'kind':'sponsor','program':'','brand':'가상','details':'상품'})
        self.assertTrue(any(r['rule_id'] == 'disclosure.D5' for r in evaluate(doc)))

    def test_product_classification_and_advertising_rules(self):
        doc = load_sample('affiliate'); product = doc['product_records'][0]
        product['product_type'] = '조제분유'; doc['commercial_relations'] = []; doc['content_type'] = 'info'
        self.assertFalse(any(r['rule_id'] == 'product_rules.P2' for r in evaluate(doc)))
        doc['commercial_relations'] = [{'kind':'affiliate','program':'','brand':'','details':''}]
        doc['content_type'] = 'affiliate'
        product.update(regulated_category='infant_formula', classification_basis='가상 품목 자료: 조제유류')
        self.assertTrue(any(r['rule_id'] == 'product_rules.P2' for r in evaluate(doc)))
        product.update(product_type='화장품', regulated_category='other'); doc['markdown'] += '\n피부 질병을 치료합니다.'
        self.assertTrue(any(r['rule_id'] == 'product_rules.P4' and r['decision'] == 'block' for r in evaluate(doc)))
        product['product_type'] = '건강기능식품'; product['ad_review_scope'] = 'unknown'
        self.assertTrue(any(r['rule_id'] == 'product_rules.P6' for r in evaluate(doc)))
        product['product_type'] = '의료기기'; product['ad_review_scope'] = 'unknown'
        self.assertTrue(any(r['rule_id'] == 'product_rules.P5' for r in evaluate(doc)))

    def test_duplicate_uncertain_and_seo(self):
        doc = load_sample('info'); doc['post_status'] = 'unknown'
        self.assertTrue(any(r['rule_id'] == 'duplicate.U2' for r in evaluate(doc)))
        doc['spam_intent'] = True
        self.assertTrue(any(r['rule_id'] == 'seo.S2' and r['decision'] == 'block' for r in evaluate(doc)))
        self.assertTrue(any(r['rule_id'] == 'seo.S3' for r in evaluate(doc, daily_count=2)))
        self.assertTrue(any(r['rule_id'] == 'duplicate.U1' for r in evaluate(doc, recent=[doc])))

    def test_health_and_product_safe_noncommercial_classification(self):
        doc = load_sample('info'); doc['risk_flags'] = []; doc['title'] = '아기 수유와 건강'
        self.assertTrue(requires_human(doc))
        doc = load_sample('affiliate'); product = doc['product_records'][0]
        product['product_type'] = '담요'; product['intended_use'] = '깨어 있을 때 놀이 매트'
        self.assertFalse(any(r['rule_id'] == 'product_rules.P7' for r in evaluate(doc)))
        product['product_type'] = '베개'; product['intended_use'] = '영아 수면'
        self.assertTrue(any(r['rule_id'] == 'product_rules.P7' for r in evaluate(doc)))

    def test_medication_dose_and_emergency_subject_detection(self):
        doc = load_sample('play'); doc['markdown'] += '\n약을 5mg 먹이세요.'
        self.assertTrue(any(r['rule_id'] == 'health_safety.H3' for r in evaluate(doc)))
        doc = load_sample('info'); doc['title'] = '아기 발열 대처'
        self.assertTrue(any(r['rule_id'] == 'health_safety.H4' for r in evaluate(doc)))

    def test_seo_source_and_paid_link_checks(self):
        doc = load_sample('info'); doc['media'][0]['alt'] = ''
        self.assertTrue(any(r['rule_id'] == 'seo.S1' for r in evaluate(doc)))
        doc = load_sample('affiliate'); doc['paid_links'] = [{'url': 'https://example.com', 'rel': ''}]
        self.assertTrue(any(r['rule_id'] == 'seo.S2' for r in evaluate(doc)))
        doc['paid_links'][0]['rel'] = 'sponsored'
        self.assertFalse(any(r['rule_id'] == 'seo.S2' for r in evaluate(doc)))

    def test_sources_have_claims_and_health_age(self):
        doc = load_sample('play'); doc['source_notes'][0]['claims'] = []
        self.assertTrue(any(r['rule_id'] == 'health_safety.H2' for r in evaluate(doc)))

    def test_risk_flags_and_metadata_alone_require_human(self):
        for flag in ('child_photo', 'experience', 'health', 'sponsor', 'affiliate', 'existing_update'):
            doc = load_sample('info'); doc['risk_flags'] = [flag]
            self.assertTrue(requires_human(doc), flag)
        doc = load_sample('info'); doc['description'] = '아이의 사진 기록'
        self.assertTrue(requires_human(doc))

    def test_remaining_rule_branches(self):
        doc = load_sample('play'); doc['source_notes'][0]['official'] = False
        self.assertTrue(any(r['rule_id'] == 'health_safety.H2' for r in evaluate(doc)))
        doc = load_sample('info'); doc['media'][0].update(child_photo=True, permissions='')
        rules = {r['rule_id'] for r in evaluate(doc)}
        self.assertTrue({'child_privacy.C1', 'child_privacy.C3'} <= rules)
        doc = load_sample('affiliate'); doc['markdown'] = '관계를 밝히지 않은 글'
        self.assertTrue(any(r['rule_id'] == 'disclosure.D1' for r in evaluate(doc)))
        doc = load_sample('sponsor'); doc['product_records'][0]['model'] = ''
        self.assertTrue(any(r['rule_id'] == 'product_rules.P1' for r in evaluate(doc)))
        doc['product_records'][0]['recall_check'] = '리콜 확인'
        doc['product_records'][0]['recall_status'] = 'recalled'
        self.assertTrue(any(r['rule_id'] == 'product_rules.P3' and r['decision'] == 'block' for r in evaluate(doc)))
        doc = load_sample('info'); old = dict(doc, markdown=doc['markdown'] + ' ' + '추가')
        self.assertTrue(any(r['rule_id'] == 'duplicate.U3' for r in evaluate(doc, recent=[old])))

    def test_final_html_is_checked_and_mismatch_cannot_pass(self):
        doc = load_sample('info'); doc['html'] += '<p>아이 생일: 2026-01-02</p>'
        rules = {r['rule_id'] for r in evaluate(doc)}
        self.assertIn('child_privacy.C2', rules)
        self.assertIn('content.consistency', rules)
        doc['html'] += '<p>아세트아미노펜을 먹이세요.</p>'
        self.assertTrue(any(r['rule_id'] == 'health_safety.H3' for r in evaluate(doc)))

    def test_numeric_claim_requires_relevant_citation(self):
        doc = load_sample('info'); doc['markdown'] += '\n\n부모급여는 월 999만원입니다.'
        self.assertTrue(any(r['rule_id'] == 'sources.N1' for r in evaluate(doc)))
        doc['markdown'] += ' [N037]'
        self.assertTrue(any(r['rule_id'] == 'sources.N1' for r in evaluate(doc)))
        doc['source_notes'][0]['claims'].append('부모급여는 월 999만원입니다.')
        self.assertFalse(any(r['rule_id'] == 'sources.N1' for r in evaluate(doc)))

    def test_explicit_root_inspects_actual_media_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); data = (Path(__file__).resolve().parents[1] / 'samples/fake-exif.jpg').read_bytes()
            (root / 'photo.jpg').write_bytes(data)
            doc = load_sample('info'); doc['media'][0]['path'] = 'photo.jpg'
            self.assertTrue(any(r['rule_id'] == 'child_privacy.C2' and r['decision'] == 'block' for r in evaluate(doc, root=root)))

    def test_emergency_waiting_and_product_classification(self):
        doc = load_sample('info'); doc['title'] = '아기 호흡 문제'
        self.assertTrue(any(r['rule_id'] == 'health_safety.H4' for r in evaluate(doc)))
        doc = load_sample('affiliate'); doc['product_records'] = []
        self.assertTrue(any(r['rule_id'] == 'product_rules.P1' and r['classification'] == '자료 보류' for r in evaluate(doc)))
        doc = load_sample('sponsor'); doc['product_records'][0]['intended_use'] = '영아 낮잠 이불'
        self.assertTrue(any(r['rule_id'] == 'product_rules.P7' and r['classification'] == '프로젝트 거절' for r in evaluate(doc)))

    def test_same_number_in_unrelated_source_does_not_satisfy_claim(self):
        doc = load_sample('info'); doc['markdown'] += '\n\n치료제는 월 100만원입니다. [N037]'
        self.assertTrue(any(r['rule_id'] == 'sources.N1' for r in evaluate(doc)))

    def test_exact_emergency_text_does_not_allow_delayed_action(self):
        import json
        row = json.loads((Path(__file__).resolve().parents[1] / 'samples/emergency.json').read_text())['items'][0]
        doc = load_sample('info'); doc['emergency_topics'] = ['fever']
        doc['markdown'] += '\n\n' + row['text'] + ' 하루 기다린 뒤 진료하세요.'
        self.assertTrue(any(r['rule_id'] == 'health_safety.H4' and r['decision'] == 'block' for r in evaluate(doc)))

    def test_missing_or_escaping_media_needs_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = load_sample('info'); doc['media'][0]['path'] = '../outside.jpg'
            self.assertTrue(any(r['rule_id'] == 'child_privacy.C2' and r['decision'] != 'pass' for r in evaluate(doc, root=Path(tmp))))
