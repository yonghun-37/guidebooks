"""A5r에서 재현한 운영 변형. 실제 외부 API는 사용하지 않는다."""
import copy
from datetime import timedelta
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from common import ROOT, load_config, now, read_json, save_json, timestamp
from pipeline import Pipeline
from providers import Provider
from state import Store


def test_recovered_font_failure_clears_current_error_preserves_history(tmp_path):
    cfg = load_config(); cfg['mode'] = 'auto'
    font = tmp_path / 'font.ttf'; cfg['media']['font'] = str(font)
    p = Pipeline(cfg, tmp_path / 'state')
    failed = p.run('insta', provider='mock')
    assert failed['status'] == 'failed' and failed['failed_step'] == 'render'
    output = Path(failed['output'])
    before = [(output / f).read_bytes() for f in ('source.json', 'draft.json')]
    font.write_bytes((ROOT / 'assets/fonts/NotoSansKR.ttf').read_bytes())
    recovered = p.resume(failed['id'])
    assert recovered['status'] == 'dry_run'
    assert 'reason' not in recovered and 'failed_step' not in recovered
    assert [(output / f).read_bytes() for f in ('source.json', 'draft.json')] == before
    assert p.store.db.execute("SELECT count(*) FROM events WHERE run_id=? AND status='failed'", (failed['id'],)).fetchone()[0] == 1


def test_explicit_result_flow_and_utf8_under_ascii_locale(tmp_path):
    cfg = load_config(); cfg['mode'] = 'auto'
    p = Pipeline(cfg, tmp_path)
    insta = p.run('insta')
    # 결과 조회 검증은 이미 생성한 문안을 이용하고 영상 인코딩은 반복하지 않는다.
    shorts = copy.deepcopy(insta); shorts['id'] = '123456abcdef'; shorts['flow'] = 'shorts'
    shorts['output'] = str(tmp_path / shorts['id'])
    save_json(Path(shorts['output']) / 'draft.json', {'title': '월급날 네 칸'})
    p.store.save(shorts)
    env = {**os.environ, 'LC_ALL': 'C', 'PYTHONUTF8': '0', 'PYTHONCOERCECLOCALE': '0', 'PYTHONIOENCODING': 'utf-8'}
    command = [sys.executable, 'pipeline.py', 'inspect', shorts['id'], '--flow', 'shorts', '--artifact', 'draft', '--state', str(tmp_path)]
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)['title'] == '월급날 네 칸'
    command[3] = insta['id']
    wrong = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
    assert wrong.returncode == 1 and '흐름' in wrong.stdout.decode('utf-8')


def test_explicit_token_import_replaces_private_precedence(tmp_path, monkeypatch, capsys):
    import ops.tokens as tokens
    cfg = load_config(); path = tmp_path / 'token.json'; cfg['ops']['instagram_token_file'] = str(path)
    save_json(path, {'access_token': 'old-fake', 'issued_at': (now()-timedelta(days=70)).isoformat(), 'expires_at': (now()-timedelta(days=10)).isoformat()})
    values = {'IG_ACCESS_TOKEN': 'new-fake', 'IG_TOKEN_ISSUED_AT': now().isoformat(), 'IG_TOKEN_EXPIRES_AT': (now()+timedelta(days=60)).isoformat()}
    monkeypatch.setattr(tokens, 'secrets', lambda: values)
    with pytest.raises(ValueError, match='만료'):
        tokens.instagram_token(cfg)
    tokens.import_instagram(cfg)
    assert tokens.instagram_token(cfg)['access_token'] == 'new-fake'
    assert path.stat().st_mode & 0o777 == 0o600
    assert 'fake' not in capsys.readouterr().out
    before = path.read_bytes(); values['IG_TOKEN_EXPIRES_AT'] = 'invalid'
    with pytest.raises(ValueError): tokens.import_instagram(cfg)
    assert path.read_bytes() == before


def test_inspect_result_reads_stored_publish_response(tmp_path):
    cfg = load_config(); cfg['mode'] = 'auto'
    p = Pipeline(cfg, tmp_path); run = p.run('insta')
    assert p.inspect(run['id'], 'insta', 'result') == run['result']


def test_inspect_youtube_result_with_status_is_json_not_run_summary(tmp_path):
    p = Pipeline(load_config(), tmp_path)
    run = {'id': '123456abcdef', 'flow': 'shorts', 'status': 'done',
           'created_at': now().isoformat(), 'source_hash': 'fixture',
           'result': {'id': 'video-fixture', 'status': {'privacyStatus': 'private'},
                      'requested_status': {'privacyStatus': 'private'}}}
    p.store.save(run)
    result = subprocess.run([sys.executable, 'pipeline.py', 'inspect', run['id'],
                             '--flow', 'shorts', '--artifact', 'result', '--state', str(tmp_path)],
                            cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout) == run['result']


@pytest.mark.parametrize('flow', ['insta', 'shorts'])
def test_post_review_clock_includes_generation_time(tmp_path, monkeypatch, flow):
    import pipeline as module
    started = now()
    clock = [started]; monkeypatch.setattr(module, 'now', lambda: clock[0])
    cfg = load_config(); cfg['mode'] = 'post_review'
    p = Pipeline(cfg, tmp_path); original = p.render
    def slow_render(*args):
        clock[0] += timedelta(minutes=3)
        return original(*args)
    p.render = slow_render
    run = p.run(flow)
    assert run['status'] == 'scheduled', run.get('reason')
    assert timestamp(run['publish_at']) == timestamp(run['created_at']) + timedelta(hours=2)
    assert timestamp(run['publish_at']) - clock[0] == timedelta(hours=1, minutes=57)


@pytest.mark.parametrize('count', [2, 3, 5])
def test_owned_asset_count_controls_draft_and_render_input(tmp_path, count):
    from PIL import Image
    from rendering.media import render
    cfg = load_config(); folder = tmp_path / 'photos'; folder.mkdir()
    for i in range(count): Image.new('RGB', (100, 100), '#276050').save(folder / f'{i}.jpg')
    cfg['media']['scenes_dir'] = str(folder)
    provider = Provider(cfg, Store(tmp_path / 'state'), 'owned', mock=True)
    source = read_json(ROOT / 'sources/sample.json')[0]
    draft = provider.draft(source, 'insta')
    assert len(draft['scenes']) == count
    assert len(render(draft, cfg, tmp_path / 'output', 'insta', provider)) == count


def test_owned_count_retries_before_media_and_includes_count_in_request(tmp_path):
    cfg = load_config(); cfg['providers']['llm'] = 'openai'
    folder = tmp_path / 'photos'; folder.mkdir()
    for i in range(3): (folder / f'{i}.jpg').write_bytes(b'owned')
    cfg['media']['scenes_dir'] = str(folder)
    source = read_json(ROOT / 'sources/sample.json')[0]; calls = []
    def invoke(kind, payload, model):
        calls.append(payload)
        draft = Provider.mock_draft(source, 'insta')
        if len(calls) > 1: draft['scenes'] = draft['scenes'][:3]
        return {'value': draft, 'usage': {'input_tokens': 5, 'output_tokens': 5}}
    draft = Provider(cfg, Store(tmp_path / 'state'), 'r', invoke=invoke).draft(source, 'insta')
    assert len(draft['scenes']) == 3 and len(calls) == 2
    assert all(c['scene_count'] == 3 for c in calls)


def test_doctor_checks_hosting_credentials_and_destination():
    from doctor import diagnose
    cfg = load_config(); cfg['hosting'].update(adapter='pages', base_url='https://user.github.io/media')
    rows = diagnose(cfg, {}, live=True, flow='insta')
    assert any(r['level'] == 'error' and 'PAGES_TOKEN' in r['message'] for r in rows)
    assert any(r['level'] == 'error' and 'pages_repository' in r['message'] for r in rows)


def test_corrected_exception_is_closed_without_deleting_history(tmp_path):
    from ops.report import report
    cfg = load_config(); cfg['mode'] = 'auto'; cfg['gates']['sensitive_words'].append('신청')
    p = Pipeline(cfg, tmp_path / 'bad'); bad = p.run('insta')
    assert bad['status'] == 'exception'
    with pytest.raises(ValueError): p.approve(bad['id'])
    assert p.resume(bad['id'])['status'] == 'exception'
    fixed = load_config(); fixed['mode'] = 'auto'
    good = Pipeline(fixed, tmp_path / 'fixed').run('insta')
    assert good['status'] == 'dry_run'
    assert report(p.store, cfg)['exceptions'] == [bad['id']]
    p.reject(bad['id'])
    assert report(p.store, cfg)['exceptions'] == []
    assert p.store.get(bad['id'])['gates']['policy']['passed'] is False
