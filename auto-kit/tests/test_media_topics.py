from pathlib import Path
import pytest
from common import load_config
from state import Store
from providers import Provider
from topics import select_topic
from rendering.media import render, probe_media
from gates import inspect_media, inspect_text, similarity

def test_topic_uses_performance_and_rss(tmp_path):
    config = load_config()
    config['sources']['files'] = []
    feed = tmp_path / 'feed.xml'
    feed.write_text('<rss><channel><item><title>책 소식</title><description>책을 읽어요.</description><link>https://example.invalid/1</link></item></channel></rss>')
    config['sources']['rss'] = [str(feed)]
    topic = select_topic(config, Store(tmp_path / 'state'), 'insta', live=False)
    assert topic['text'] == '책을 읽어요.'

@pytest.mark.parametrize('flow', ['insta', 'shorts'])
def test_real_local_media_and_gates(tmp_path, flow):
    config, store = load_config(), Store(tmp_path / 'state')
    p = Provider(config, store, 'r', mock=True)
    source = {'title': '가상도서관 소식', 'text': '가상도서관은 책 12권을 소개해요.', 'entities': ['가상도서관']}
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
