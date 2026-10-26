"""쇼츠 통합 생성기의 원본 재사용·실제 인용 경계를 확인한다."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_appendices_shorts import catalog, cited_sources


def test_catalog_uses_display_number_and_original_tool(tmp_path):
    folder = tmp_path / 'chapters'
    folder.mkdir()
    (folder / '02b-ai-tools.html').write_text('''<body data-chapter-number="3"><h1>AI 도구 지도</h1>
    <section id="simulator" data-block="simulator"><h2>경로 고르기</h2><div class="simulator"><select></select></div></section></body>''')
    assert catalog(tmp_path) == [dict(chapter=3, slug='02b-ai-tools', id='simulator', title='경로 고르기', section='simulator')]


def test_credits_exclude_unused_source_notes_and_merge_backlinks(tmp_path):
    first = tmp_path / 'a.html'
    first.write_text('<h1>첫 장</h1><a href="#source-y001">[Y001]</a><li id="source-y001">사용함</li><li id="source-y002">목록에만 있음</li>')
    second = tmp_path / 'b.html'
    second.write_text('<h1>다음 장</h1><a href="#source-y001">[Y001]</a>')
    assert cited_sources(tmp_path, [first, second]) == {'Y001': [('a.html', '첫 장'), ('b.html', '다음 장')]}


def test_shorts_gate_checks_first_and_inserted_chapters_and_catalog(tmp_path):
    import check_site
    folder = tmp_path / 'site-shorts'
    (folder / 'chapters').mkdir(parents=True)
    (folder / 'assets').mkdir()
    (tmp_path / 'research-shorts').mkdir()
    (tmp_path / 'research-shorts/SOURCES.md').write_text('Y001')
    (folder / 'chapters/01-map.html').write_text('<h1>순서</h1>')
    (folder / 'chapters/02b-ai-tools.html').write_text('<h1>도구</h1>')
    (folder / 'assets/catalog.js').write_text('window.ShortsCatalog = Object.freeze([{"chapter":3,"slug":"02b-ai-tools","id":"missing"}]);')
    result = check_site.check(tmp_path, 'site-shorts')
    assert result['theory_chapters'] == 2
    assert result['catalog_entries'] == 1
    assert any('없는 도구' in error for error in result['errors'])
    assert sum('9단계' in error for error in result['errors']) == 2


def test_shorts_gate_checks_e2e_keys(tmp_path):
    import check_site
    folder = tmp_path / 'site-shorts/practice'
    folder.mkdir(parents=True)
    (tmp_path / 'research-shorts').mkdir()
    (tmp_path / 'research-shorts/SOURCES.md').write_text('Y001')
    (folder / '00-start.html').write_text('<input data-practice-check="0:route">')
    (folder / 'e2e.html').write_text('<input data-practice-check="0:files">')
    assert any('E2E' in error for error in check_site.check(tmp_path, 'site-shorts')['errors'])
