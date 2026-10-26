import copy
import json
import pytest
from common import load_config
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
    value = provider.draft({'title': '도서관 소식', 'text': '가상도서관은 책 12권을 소개한다.', 'entities': ['가상도서관']}, 'insta')
    assert len(value['scenes']) >= 2
    assert store.spend()['total'] == 0
    assert len(store.calls()) == 1

def test_fact_policy_gate():
    config = load_config()
    draft = {'title': '가상도서관', 'caption': '책 99권. NASA 발표', 'narration': '', 'entities': ['NASA'], 'scenes': []}
    results = inspect_text(draft, {'text': '책 12권', 'entities': []}, [], config['gates'])
    assert not results['facts']['passed']
    assert '99' in str(results['facts']['reasons'])
    assert 'NASA' in str(results['facts']['reasons'])

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
    p.draft({'title': '책', 'text': '책을 읽어요.', 'entities': []}, 'insta')
    assert len(attempts) == 2
    assert len(store.calls()) == 2
    assert store.spend()['total'] > 0
