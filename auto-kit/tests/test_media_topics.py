from pathlib import Path
from html import escape
import pytest
from PIL import ImageDraw
from common import load_config, read_json, ROOT, hashed
from state import Store
from providers import Provider
from topics import select_topic
from rendering.media import render, probe_media
from rendering import short_base
from pipeline import Pipeline
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


@pytest.mark.parametrize('flow,format,motion,custom', [
    ('insta', 'reel', False, False),
    ('insta', 'carousel', True, False),
    ('insta', 'reel', False, True),
    ('shorts', 'carousel', False, False),
    ('shorts', 'carousel', False, True),
])
def test_flow_display_text_in_real_frames_and_previews(tmp_path, monkeypatch, flow, format, motion, custom):
    config = load_config()
    config['mode'] = 'auto'
    config['instagram']['format'] = format
    config['media']['motion_reel'] = motion
    selected = config['flows'][flow]
    name_key = 'account_name' if flow == 'insta' else 'channel_name'
    if custom:
        selected.update({name_key: '새 이름 <우리 & 함께>',
                         'creator_name': '새 제작자', 'preview_speaker': '<새 안내자>'})
    # Pillow에 실제로 그려지는 문구를 수집해 영상 입력과 카드 양쪽을 검사한다.
    drawn = []
    original_text = ImageDraw.ImageDraw.text
    def capture_text(self, xy, text, *args, **kwargs):
        drawn.append(text)
        return original_text(self, xy, text, *args, **kwargs)
    monkeypatch.setattr(ImageDraw.ImageDraw, 'text', capture_text)
    previews = []
    original_preview = short_base.write_preview
    def capture_preview(output, *args):
        original_preview(output, *args)
        previews.append((output / 'preview.html').read_text(encoding='utf-8'))
    monkeypatch.setattr(short_base, 'write_preview', capture_preview)

    run = Pipeline(config, tmp_path / 'state').run(flow, provider='mock')
    assert run['status'] == 'dry_run', run
    assert selected[name_key] in drawn
    assert any(text.startswith(selected['creator_name'] + '의 연습 · ') for text in drawn)
    previews.append((Path(run['output']) / 'preview.html').read_text(encoding='utf-8'))
    assert len(previews) == 2  # 공통 영상 미리보기와 최종 흐름 미리보기
    for preview in previews:
        assert escape(selected[name_key]) + ' · 미리보기' in preview
        assert escape(selected['preview_speaker']) + ':' in preview
        if custom:
            assert selected[name_key] not in preview  # HTML은 표시 이름을 이스케이프한다.
            assert selected['preview_speaker'] not in preview
    opposite = config['flows']['shorts' if flow == 'insta' else 'insta']
    forbidden = [opposite.get('channel_name', opposite.get('account_name')),
                 opposite['creator_name'], opposite['preview_speaker'], '도윤의 쇼츠 작업실']
    if custom:
        defaults = load_config()['flows'][flow]
        forbidden.extend([defaults[name_key], defaults['creator_name'], defaults['preview_speaker']])
    visible = '\n'.join(drawn + previews)
    assert all(text not in visible for text in forbidden)
