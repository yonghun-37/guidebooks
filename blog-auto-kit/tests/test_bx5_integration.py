"""통합 요청에서 발견한 운영·출력 차이를 검증한다."""
import csv
import socket
from pathlib import Path
from types import SimpleNamespace

from course.doctor import doctor
from core.state import Store
from core.publish_actions import status_action
from monetize.sponsor.demo import _tax_csv, RECORDS
from ops.scheduler import generate_schedule
from core.actions import operations_action

KIT = Path(__file__).resolve().parents[1]


def test_doctor_does_not_require_fixed_mock_port(capsys):
    with socket.socket() as occupied:
        occupied.bind(('127.0.0.1', 8767))
        doctor(KIT)
    assert '임시 포트' in capsys.readouterr().out


def test_status_preserves_server_date_and_public_url(tmp_path):
    class Client:
        def request(self, method, path):
            return [{'id': 7, 'status': 'publish', 'date': '2026-10-28T09:00:00',
                     'date_gmt': '2026-10-28T00:00:00', 'link': 'https://example.invalid/p/7'}]
    import json
    status_action(tmp_path, Store(tmp_path), Client(), SimpleNamespace(sample='info', mock=False))
    post = json.loads((tmp_path / 'output/status.json').read_text())['posts'][0]
    assert post['date'] == '2026-10-28T09:00:00'
    assert post['date_gmt'] == '2026-10-28T00:00:00'
    assert post['link'] == 'https://example.invalid/p/7'


def test_tax_export_retains_return_terms_and_costs(tmp_path):
    entries = [{'state': 'contracted', 'records': RECORDS['contracted']},
               {'state': 'settlement_pending', 'records': {'costs': '배송비 5000원'}}]
    path = _tax_csv(tmp_path, '2026-10-27', entries)
    with path.open() as stream:
        row = next(csv.DictReader(stream))
    assert row['return_terms'] == '반납 없음'
    assert row['costs'] == '배송비 5000원'


def test_schedule_examples_only_collect_reports(tmp_path):
    texts = [p.read_text() for p in generate_schedule(tmp_path)]
    texts.append((KIT / 'ops/github-actions.yml').read_text())
    assert all('run --sample' not in text and '--sample</string>' not in text for text in texts)
    assert all('report' in text for text in texts)


def test_audit_template_has_evidence_fields_for_each_check(tmp_path):
    operations_action(tmp_path, Store(tmp_path), SimpleNamespace(ops=False, restore=False, audit=True))
    text = (tmp_path / 'output/launch-checklist.txt').read_text()
    assert text.count('[ ]') == 6
    assert text.count('확인자:') == 6
    assert text.count('근거 파일·주소:') == 6
    assert text.count('보류 이유·다음 확인일:') == 6
