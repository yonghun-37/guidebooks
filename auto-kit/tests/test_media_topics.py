from pathlib import Path
import pytest
from common import load_config, read_json, ROOT, hashed
from state import Store
from providers import Provider
from topics import select_topic
from rendering.media import render, probe_media
from gates import inspect_media, inspect_text, similarity

def test_topic_uses_performance_and_rss(tmp_path):
    config = load_config()
    config['sources']['files'] = []
    feed = tmp_path / 'feed.xml'
    feed.write_text('<rss><channel><item><title>청년 지원금 신청 전 확인</title><description>공고에서 신청 기간을 확인해요.</description><link>https://example.invalid/1</link></item></channel></rss>')
    config['sources']['rss'] = [str(feed)]
    topic = select_topic(config, Store(tmp_path / 'state'), 'insta', live=False)
    assert topic['text'] == '공고에서 신청 기간을 확인해요.'

@pytest.mark.parametrize('flow', ['insta', 'shorts'])
def test_example_json_and_rss_select_same_flow(tmp_path, flow):
    config = load_config()
    store = Store(tmp_path / 'state')
    direct = select_topic(config, store, flow)
    config['sources']['files'] = []
    config['sources']['rss'] = [
        {'url': f'sources/{name}-feed.xml', 'flow': name, 'synthetic': True,
         'rights_reviewed': False, 'category': category}
        for name, category in [('insta', '생활 뉴스'), ('shorts', '자취 생활')]
    ]
    rss = select_topic(config, store, flow)
    assert rss['title'] == direct['title']
    assert rss['text'] == direct['text']
    assert rss['source_hash'] == hashed(direct['text'].strip())
    assert rss['synthetic'] is True and rss['rights_reviewed'] is False
    assert Provider.mock_draft(rss, flow) == Provider.mock_draft(direct, flow)

def test_sources_without_flow_remain_shared(tmp_path):
    config = load_config()
    config['sources']['files'] = []
    config['sources']['rss'] = ['sources/insta-feed.xml']
    store = Store(tmp_path / 'state')
    assert select_topic(config, store, 'shorts')['title'] == select_topic(config, store, 'insta')['title']

@pytest.mark.parametrize('flow', ['insta', 'shorts'])
def test_real_local_media_and_gates(tmp_path, flow):
    config, store = load_config(), Store(tmp_path / 'state')
    p = Provider(config, store, 'r', mock=True)
    source = next(s for s in read_json(ROOT / 'sources/sample.json') if s['flow'] == flow)
    draft = p.draft(source, flow)
    files = render(draft, config, tmp_path / 'render', flow, p)
    results = inspect_media(files, flow, config['gates'], config['instagram' if flow == 'insta' else 'youtube'])
    assert all(r['passed'] for r in results.values()), results
    assert all(r['passed'] for r in inspect_text(draft, source, [], config['gates']).values())
    if flow == 'shorts':
        info = probe_media(files[0])
        assert info['width'] == 1080 and info['height'] == 1920
        assert -19 <= info['lufs'] <= -13
        assert (tmp_path / 'render/subtitles.srt').is_file()

def test_ngrams_and_missing_ai():
    assert similarity('같은 문장을 되풀이해요', '같은 문장을 되풀이해요') == 1
    assert not inspect_media([], 'shorts', load_config()['gates'], {})['ai']['passed']
