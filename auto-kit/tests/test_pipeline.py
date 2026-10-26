from pathlib import Path
import copy
import pytest
from common import load_config, read_json
from pipeline import Pipeline
from state import Store

@pytest.mark.parametrize('flow', ['insta', 'shorts'])
def test_mock_full_flow(tmp_path, flow):
    cfg = load_config(); cfg['mode'] = 'auto'
    p = Pipeline(cfg, tmp_path)
    result = p.run(flow, provider='mock')
    assert result['status'] == 'dry_run', result
    assert all(step in result['steps'] for step in ['topic','draft','render','host','gates','publish','insights'])
    assert read_json(tmp_path / result['id'] / 'request-plan.json')['network_calls'] == 0
    assert (tmp_path / 'dashboard.html').exists()
    assert (tmp_path / result['id'] / 'insights.csv').exists()

def test_approval_binding_and_dry_cannot_go_live(tmp_path):
    p = Pipeline(load_config(), tmp_path)
    run = p.run('insta')
    assert run['status'] == 'waiting_approval'
    p.approve(run['id'])
    with pytest.raises(ValueError): p.resume(run['id'], live=True)
    file = Path(run['files'][0])
    file.write_bytes(file.read_bytes() + b'changed')
    result = p.resume(run['id'])
    assert result['status'] == 'exception'
    assert 'publish' not in result['steps']

def test_resume_skips_successful_generation(tmp_path, monkeypatch):
    cfg = load_config(); cfg['mode'] = 'auto'
    p = Pipeline(cfg, tmp_path)
    original = p.render
    monkeypatch.setattr(p, 'render', lambda *a: (_ for _ in ()).throw(ValueError('렌더 실패')))
    run = p.run('insta')
    assert run['status'] == 'failed' and 'draft' in run['steps']
    calls = len(p.store.calls())
    monkeypatch.setattr(p, 'render', original)
    result = p.resume(run['id'])
    assert result['status'] == 'dry_run'
    assert len(p.store.calls()) == calls

def test_duplicate_blocks_before_publish(tmp_path):
    cfg = load_config(); cfg['mode'] = 'auto'
    p = Pipeline(cfg, tmp_path)
    first = p.run('insta')
    # 주제 선택 재사용을 강제해 콘텐츠 해시 방어도 별도로 검증한다.
    p.select = lambda *a, **k: first['source']
    second = p.run('insta')
    assert second['status'] == 'exception'
    assert 'publish' not in second['steps']

def test_post_review_insta_delay_and_reject(tmp_path):
    cfg = load_config(); cfg['mode'] = 'post_review'
    p = Pipeline(cfg, tmp_path)
    run = p.run('insta')
    assert run['status'] == 'scheduled'
    assert 'publish' not in run['steps']
    p.reject(run['id'])
    assert p.resume(run['id'])['status'] == 'rejected'

def test_live_requires_credentials_and_non_mock(tmp_path):
    p = Pipeline(load_config(), tmp_path)
    with pytest.raises(ValueError): p.run('insta', live=True, provider='mock')

def test_quality_failure_queue_contains_reasons(tmp_path, monkeypatch):
    cfg = load_config(); cfg['mode'] = 'auto'; cfg['gates']['blocked_words'] = ['책']
    p = Pipeline(cfg, tmp_path)
    run = p.run('insta')
    assert run['status'] == 'exception'
    assert any('책' in r for r in run['gates']['policy']['reasons'])
    assert (tmp_path / run['id'] / 'notification.json').exists()
