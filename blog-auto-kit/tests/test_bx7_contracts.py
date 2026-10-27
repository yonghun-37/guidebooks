"""통합 재검토에서 확인한 계약 관계와 용량 조사 표현 회귀 검사."""
import pytest
from content.samples import load_sample
from content.markdown import render
from core.approval import approve_document
from core.state import Store
from gates.engine import evaluate
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft

TODAY = '2026-10-27'


@pytest.mark.parametrize('mode', ['approval', 'auto'])
@pytest.mark.parametrize('typ,body', [
    ('조제분유', '품목 정보를 정리해요.'),
    ('의료기기', '제가 직접 써보니 편했습니다.'),
    ('화장품', '아토피피부염을 예방합니다.'),
])
def test_contract_only_relation_cannot_bypass_product_prohibitions(tmp_path, mode, typ, body):
    doc = load_sample('affiliate')
    doc.update(content_type='info', commercial_relations=[], media=[])
    doc['contract']['commercial_relations'] = [{'kind': 'affiliate', 'details': '판매 수수료'}]
    doc['product_records'][0].update(product_type=typ,
        regulated_category='infant_formula' if typ == '조제분유' else 'other',
        classification_basis='가상 품목 분류 자료')
    doc['markdown'] = '제휴 링크 구매 시 수수료를 제공받습니다.\n\n## 제품 자료\n\n' + body
    doc['html'] = render(doc['markdown'])
    store = Store(tmp_path)
    with running_server(tmp_path, port=0, today=TODAY) as url:
        client = Client(url)
        for action in (lambda: prepare_draft(tmp_path, store, client, doc, TODAY, ['info']),
                       lambda: approve_document(tmp_path, store, doc, '가상 검토자', TODAY),
                       lambda: publish_draft(tmp_path, store, client, doc, TODAY, mode)):
            with pytest.raises(ValueError):
                action()
        assert client.request('GET', 'posts') == []
    assert any(r['rule_id'].startswith('product_rules.') and r['decision'] == 'block'
               for r in evaluate(doc))


@pytest.mark.parametrize('text', ['5ml를 복용해요.', '2정을 먹어요.', '1포씩 투약해요.'])
def test_dose_units_with_korean_particles_trigger_specific_safety_rule(tmp_path, text):
    doc = load_sample('info'); doc['media'] = []
    doc['markdown'] += '\n\n' + text; doc['html'] = render(doc['markdown'])
    # 숫자 출처 관문으로 막힌 것을 약 검사 성공으로 세지 않는다.
    doc['source_notes'][0]['claims'].append(text)
    assert any(r['rule_id'] == 'health_safety.H3' and r['decision'] == 'block'
               for r in evaluate(doc))
    store = Store(tmp_path)
    with running_server(tmp_path, port=0, today=TODAY) as url:
        client = Client(url)
        for action in (lambda: prepare_draft(tmp_path, store, client, doc, TODAY, ['info']),
                       lambda: publish_draft(tmp_path, store, client, doc, TODAY, 'auto')):
            with pytest.raises(ValueError):
                action()
        assert client.request('GET', 'posts') == []


@pytest.mark.parametrize('opening', ['제휴 링크를 포함하지만 수수료는 받지 않습니다.',
                                    '수수료에 관한 안내입니다.'])
def test_denied_or_ambiguous_relationship_is_not_receipt_disclosure(tmp_path, opening):
    doc = load_sample('affiliate'); doc['media'] = []
    doc['markdown'] = opening + '\n\n## 제품 비교\n\n자료를 비교해요.'
    doc['html'] = render(doc['markdown']); store = Store(tmp_path)
    with running_server(tmp_path, port=0, today=TODAY) as url:
        client = Client(url)
        for action in (lambda: prepare_draft(tmp_path, store, client, doc, TODAY),
                       lambda: approve_document(tmp_path, store, doc, '가상 검토자', TODAY),
                       lambda: publish_draft(tmp_path, store, client, doc, TODAY, 'auto')):
            with pytest.raises(ValueError):
                action()
        assert client.request('GET', 'posts') == []
