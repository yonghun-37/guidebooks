import copy
import json
import pytest
from common import load_config, read_json, ROOT
from state import Store, BudgetExceeded
from providers import Provider
from gates import inspect_text

def test_daily_and_monthly_budget(tmp_path):
    store = Store(tmp_path)
    ticket = store.reserve('r', 'llm', .06, daily=.1, monthly=.1)
    with pytest.raises(BudgetExceeded):
        store.reserve('r', 'retry', .06, daily=.1, monthly=.1)
    store.settle(ticket, .02, {'input_tokens': 10})
    assert store.spend()['total'] == pytest.approx(.02)
    with pytest.raises(BudgetExceeded):
        store.reserve('r', 'image', .03, daily=.1, monthly=.04)

def test_mock_schema_and_cost(tmp_path):
    store = Store(tmp_path)
    config = load_config()
    provider = Provider(config, store, 'r', mock=True)
    value = provider.draft(read_json(ROOT / 'sources/sample.json')[0], 'insta')
    assert len(value['scenes']) >= 2
    assert store.spend()['total'] == 0
    assert len(store.calls()) == 1

def test_fact_policy_gate():
    config = load_config()
    draft = {'title': '청년 지원금 확인', 'caption': '지원금 99만원. NASA 발표', 'narration': '', 'entities': ['NASA'], 'scenes': []}
    results = inspect_text(draft, read_json(ROOT / 'sources/sample.json')[0], [], config['gates'])
    assert not results['facts']['passed']
    assert '99' in str(results['facts']['reasons'])
    assert 'NASA' in str(results['facts']['reasons'])

@pytest.mark.parametrize('flow', ['insta', 'shorts'])
@pytest.mark.parametrize('invented_number', [False, True])
def test_example_fact_gate(flow, invented_number):
    source = next(s for s in read_json(ROOT / 'sources/sample.json') if s['flow'] == flow)
    draft = Provider.mock_draft(source, flow)
    if invented_number:
        draft['caption'] += '\n지원금 99만원' if flow == 'insta' else '\n매달 99만원 절약'
    facts = inspect_text(draft, source, [], load_config()['gates'])['facts']
    assert facts['passed'] is (not invented_number)
    assert facts['reasons'] == (['원문에 없는 숫자: 99'] if invented_number else [])

def test_schema_retry_is_charged(tmp_path):
    config = load_config()
    config['providers']['llm'] = 'openai'
    attempts = []
    def invoke(kind, payload, model):
        attempts.append(kind)
        if len(attempts) == 1:
            return {'value': {'invalid': True}, 'usage': {'input_tokens': 3, 'output_tokens': 2}}
        return {'value': Provider.mock_draft(payload['source'], payload['flow']), 'usage': {'input_tokens': 3, 'output_tokens': 2}}
    store = Store(tmp_path)
    p = Provider(config, store, 'r', invoke=invoke)
    p.draft({'title': '청년 지원금 확인', 'text': '공고에서 신청 기간을 확인해요.', 'entities': []}, 'insta')
    assert len(attempts) == 2
    assert len(store.calls()) == 2
    assert store.spend()['total'] > 0
