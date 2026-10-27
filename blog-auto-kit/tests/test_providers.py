"""공급자 오류와 비용 상한을 검증한다."""
import unittest
from providers.openai_adapter import draft


class ProviderTests(unittest.TestCase):
    def test_contract_blocks_before_transport(self):
        called = []
        result = draft('x', {}, {'ai_allowed': False}, lambda request: called.append(request))
        self.assertEqual(result['status'], 'on_hold')
        self.assertEqual(called, [])

    def test_structured_response_and_refusal(self):
        requests = []
        def transport(request):
            requests.append(request)
            return {'status': 'completed', 'output': [{'content': [{'type': 'output_text', 'text': '{"title":"예"}'}]}]}
        result = draft('x', {}, {'ai_allowed': True}, transport)
        self.assertEqual(result['data']['title'], '예')
        self.assertTrue(requests[0]['text']['format']['strict'])
        result = draft('x', {}, {'ai_allowed': True}, lambda request: {'status': 'incomplete'})
        self.assertEqual(result['status'], 'on_hold')

    def test_unknown_contract_and_error_responses_hold(self):
        for contract in ({}, {'ai_allowed': None}):
            self.assertEqual(draft('x', {}, contract, lambda request: self.fail('호출 금지'))['status'], 'on_hold')
        for response in ({'status': 'incomplete'}, {'status': 'completed', 'output': [{'content': [{'type': 'refusal', 'refusal': 'no'}]}]}, {'status': 'completed', 'output': [{'content': [{'type': 'output_text', 'text': '{'}]}]}):
            self.assertEqual(draft('x', {}, {'ai_allowed': True}, lambda request: response)['status'], 'on_hold')

    def test_cost_reservations_atomic_and_monthly(self):
        import tempfile
        import sqlite3
        from concurrent.futures import ThreadPoolExecutor
        from pathlib import Path
        from providers.costs import reserve_cost, settle_cost
        class SQLiteStore:
            def __init__(self, path): self.path = path
            def connect(self): return sqlite3.connect(self.path, timeout=5)
        with tempfile.TemporaryDirectory() as tmp:
            store = SQLiteStore(Path(tmp) / 'db')
            with store.connect() as db: db.execute('CREATE TABLE costs (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
            def reserve(key):
                try: return reserve_cost(store, key, '0.6', '2026-10-27', '1')
                except ValueError: return None
            with ThreadPoolExecutor(max_workers=2) as pool: rows = list(pool.map(reserve, ['a', 'b']))
            self.assertEqual(sum(row is not None for row in rows), 1)
            reserve_cost(store, 'next', '0.8', '2026-11-01', '1')
            winner = next(row['run_id'] for row in rows if row)
            settle_cost(store, winner, '0.5', '2026-10-27')
            with self.assertRaises(ValueError): settle_cost(store, winner, '0.5', '2026-10-27')
            with self.assertRaises(ValueError): reserve_cost(store, 'invalid', '-1', '2026-10-27', '1')

    def test_schema_mismatch_and_transport_failure_hold(self):
        schema = {'type': 'object', 'required': ['title'], 'properties': {'title': {'type': 'string'}}, 'additionalProperties': False}
        response = {'status': 'completed', 'output': [{'content': [{'type': 'output_text', 'text': '{"title": 2}'}]}]}
        self.assertEqual(draft('x', schema, {'ai_allowed': True}, lambda _: response)['status'], 'on_hold')
        def fail(_): raise OSError('연결 실패')
        self.assertEqual(draft('x', schema, {'ai_allowed': True}, fail)['status'], 'on_hold')
