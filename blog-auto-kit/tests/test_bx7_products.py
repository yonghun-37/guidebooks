"""제품 광고·대가 공개 우회를 실제 초안/발행 경로에서 막는다."""
import copy
import shutil
from pathlib import Path

import pytest

from content.markdown import render
from content.samples import load_sample
from core.approval import approve_document
from core.state import Store
from gates.body import consistent
from gates.engine import evaluate
from gates.products import product_checks
from monetize.affiliate import COUPANG, prepare_affiliate
from monetize.ads import build_ads
from monetize.pages import generate_pages
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft

TODAY = '2026-10-27'


def commercial_doc():
    doc = load_sample('affiliate')
    doc['media'] = []
    doc['markdown'] = COUPANG + '\n\n' + doc['markdown']
    doc['html'] = render(doc['markdown'])
    doc['product_records'][0].update(recall_status='none_found',
        classification_basis='가상 모델의 품목 분류 자료', regulated_category='other')
    return doc


def product_findings(doc, rule):
    return [row for row in product_checks(doc) if row['rule_id'] == 'product_rules.' + rule]


@pytest.mark.parametrize('typ,claim,rule', [
    ('화장품', '아토피피부염을 예방합니다.', 'P4'),
    ('건강기능식품', '감기를 예방합니다.', 'P6'),
    ('일반 제품', '감기를 낫게 합니다.', 'P4'),
    ('의료기기', '질병을 완화합니다.', 'P5'),
])
def test_disease_prevention_treatment_and_relief_block(typ, claim, rule):
    doc = commercial_doc(); doc['product_records'][0]['product_type'] = typ
    doc['markdown'] += '\n\n' + claim; doc['html'] = render(doc['markdown'])
    assert any(row['decision'] == 'block' for row in product_findings(doc, rule))


def test_unknown_product_disease_claim_holds_instead_of_legal_determination():
    doc = commercial_doc(); doc['product_records'][0].update(product_type='분류 불명', classification_basis='')
    doc['markdown'] += '\n\n감기를 예방합니다.'; doc['html'] = render(doc['markdown'])
    rows = product_checks(doc)
    assert any(row['decision'] == 'review' and not row['human_resolvable'] for row in rows)
    assert not any(row['classification'] == '법적 금지' for row in rows)


@pytest.mark.parametrize('field', ['experience', 'markdown'])
def test_comparison_flag_cannot_exempt_actual_medical_device_testimonial(field):
    doc = commercial_doc(); doc['product_records'][0]['product_type'] = '의료기기'
    doc[field] += '\n제가 직접 써보니 정말 편했습니다.'
    doc['html'] = render(doc['markdown'])
    assert any(row['decision'] == 'block' and row['evidence_ids'] == ['BXF-048']
               for row in product_findings(doc, 'P5'))


def test_medical_device_non_testimonial_is_not_blocked_by_comparison_flag():
    doc = commercial_doc(); doc['comparison_only'] = False
    doc['product_records'][0]['product_type'] = '의료기기'
    assert not any(row['decision'] == 'block' for row in product_checks(doc))


@pytest.mark.parametrize('note', ['사용해 본 적이 없습니다. 공식 자료를 정리합니다.', '제가 직접 사용하지 않았습니다.', '공식 자료 비교입니다.'])
def test_medical_device_non_testimonial_notes_are_not_legal_bans(note):
    doc = commercial_doc(); doc['product_records'][0]['product_type'] = '의료기기'
    doc['experience'] = note
    assert not any(row['decision'] == 'block' for row in product_checks(doc))


def test_cosmetic_non_disease_moisturizing_description_is_not_a_legal_ban():
    doc = commercial_doc(); doc['product_records'][0]['product_type'] = '화장품'
    doc['markdown'] += '\n\n피부 건조를 완화하는 보습 기능을 자료에서 비교합니다.'
    doc['html'] = render(doc['markdown'])
    assert not any(row['decision'] == 'block' for row in product_checks(doc))


@pytest.mark.parametrize('status,decision', [('none_found', None), ('recalled', 'block'), ('unchecked', 'review')])
def test_recall_result_is_separate_from_check_procedure(status, decision):
    doc = commercial_doc(); doc['product_records'][0].update(recall_status=status, recall_check='리콜 확인 결과 없음')
    rows = product_findings(doc, 'P3')
    assert ([row['decision'] for row in rows] == [decision]) if decision else not rows
    if status == 'recalled':
        assert rows[0]['evidence_ids'] == ['BXF-044']
        assert rows[0]['classification'] == '프로젝트 거절'


def test_infant_formula_requires_classification_basis():
    doc = commercial_doc(); product = doc['product_records'][0]
    product.update(product_type='영아용 조제식', classification_basis='', regulated_category='unknown')
    assert not any(row['decision'] == 'block' for row in product_findings(doc, 'P2'))
    assert any(row['decision'] == 'review' for row in product_checks(doc))
    product.update(classification_basis='가상 품목제조 자료: 조제유류', regulated_category='infant_formula')
    assert any(row['decision'] == 'block' for row in product_findings(doc, 'P2'))


def test_verified_non_formula_is_not_inferred_from_product_name():
    doc = commercial_doc()
    doc['product_records'][0].update(product_type='영아용 조제식', regulated_category='other',
        classification_basis='가상 품목 자료를 대조한 결과 조제유류에 해당하지 않음')
    assert not product_findings(doc, 'P2')


@pytest.mark.parametrize('relation,opening', [
    ({'kind': 'affiliate', 'details': '수수료'}, '제휴 활동 안내입니다.'),
    ({'kind': 'sponsor', 'details': '상품 무료제공과 광고비'}, '상품을 무료 제공받았습니다.'),
    ({'kind': 'sponsor', 'details': '대여'}, '상품을 무료 제공받았습니다.'),
])
def test_each_actual_relationship_needs_its_own_opening_disclosure(relation, opening):
    doc = commercial_doc(); doc['commercial_relations'] = [dict(program='', brand='가상', **relation)]
    doc['markdown'] = opening + '\n\n## 비교\n\n자료 비교입니다.'; doc['html'] = render(doc['markdown'])
    assert any(row['rule_id'].startswith('disclosure.D') and row['decision'] == 'block' for row in evaluate(doc))


def test_empty_commercial_metadata_holds_without_human_override():
    doc = commercial_doc(); doc['commercial_relations'] = []
    assert any(row['rule_id'] == 'disclosure.D1' and row['decision'] == 'review'
               and not row['human_resolvable'] for row in evaluate(doc))


@pytest.mark.parametrize('kind,details,word', [('sponsor', '상품 무료제공', '무료 제공'),
    ('sponsor', '광고비', '광고비'), ('loan', '대여', '대여')])
def test_coupang_template_only_applies_to_commission(tmp_path, kind, details, word):
    doc = commercial_doc(); doc['commercial_relations'] = [dict(kind=kind, details=details, program='쿠팡', brand='가상')]
    doc['markdown'] = '## 비교\n\n내용'; doc['html'] = render(doc['markdown'])
    prepared = prepare_affiliate(tmp_path, Store(tmp_path), doc)
    assert COUPANG not in prepared['markdown'] and word in prepared['markdown'].split('\n\n')[0]
    assert consistent(prepared)


@pytest.mark.parametrize('mutation', ['hidden', 'style', 'class', 'raw'])
def test_final_html_must_be_exact_renderer_output(mutation):
    doc = commercial_doc()
    if mutation == 'raw':
        doc['markdown'] += '\n\n<span hidden>비공개</span>'; doc['html'] = render(doc['markdown'])
    else:
        attribute = {'hidden': 'hidden', 'style': 'style="display:none"', 'class': 'class="hidden"'}[mutation]
        doc['html'] = doc['html'].replace('<p>', '<p ' + attribute + '>', 1)
    assert not consistent(doc)


@pytest.mark.parametrize('attack', ['medical_experience', 'cosmetic_prevention', 'supplement_prevention',
    'vague_disclosure', 'hidden_disclosure', 'raw_html', 'empty_relations', 'loan_omitted'])
@pytest.mark.parametrize('mode', ['approval', 'auto'])
def test_counterexamples_never_reach_future_or_publish(tmp_path, attack, mode):
    """먼저 정상 초안을 준비한 뒤 우회 원고의 재준비·승인·발행을 모두 시도한다."""
    shutil.copy(Path(__file__).resolve().parents[1] / 'config.example.toml', tmp_path / 'config.example.toml')
    store = Store(tmp_path); doc = commercial_doc()
    with running_server(tmp_path, port=0) as url:
        client = Client(url); row = prepare_draft(tmp_path, store, client, doc, TODAY)
        bad = copy.deepcopy(doc)
        if attack == 'medical_experience':
            bad['product_records'][0]['product_type'] = '의료기기'
            bad['experience'] = '제가 직접 써보니 편했습니다.'; bad['experience_by'] = 'human'
        if attack in ('cosmetic_prevention', 'supplement_prevention'):
            bad['product_records'][0]['product_type'] = '화장품' if attack.startswith('cosmetic') else '건강기능식품'
            bad['markdown'] += '\n\n아토피피부염을 예방합니다.'
        if attack == 'vague_disclosure': bad['markdown'] = bad['markdown'].replace(COUPANG, '제휴 활동 안내입니다.')
        if attack == 'raw_html': bad['markdown'] += '\n\n<span hidden>광고 표시</span>'
        if attack == 'empty_relations': bad['commercial_relations'] = []
        if attack == 'loan_omitted': bad['commercial_relations'].append(dict(kind='loan', program='', brand='가상', details='대여'))
        bad['html'] = render(bad['markdown'])
        if attack == 'hidden_disclosure': bad['html'] = bad['html'].replace('<p>', '<p style="display:none">', 1)
        for operation in (lambda: prepare_draft(tmp_path, store, client, bad, TODAY),
                          lambda: approve_document(tmp_path, store, bad, '사람', TODAY),
                          lambda: publish_draft(tmp_path, store, client, bad, TODAY, mode)):
            with pytest.raises(ValueError): operation()
        assert client.request('GET', f"posts/{row['post_id']}")['status'] == 'draft'


def test_generated_policy_has_required_completion_checklist(tmp_path):
    generate_pages(tmp_path, {}, TODAY)
    text = (tmp_path / 'output/pages/privacy.html').read_text()
    for term in ('제30조', '제31조', '안전성 확보조치', '성명', '부서', '법정대리인', '민감정보', '가명정보', '국외 이전'):
        assert term in text
    assert '완성본이 아닙니다' in text


def test_korean_ads_age_has_no_18_year_old_exception(tmp_path):
    build_ads(tmp_path, {}, TODAY)
    text = (tmp_path / 'output/ads/checklist.txt').read_text()
    assert '만 19세' in text and '18세' not in text
