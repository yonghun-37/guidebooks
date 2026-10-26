#!/usr/bin/env python3
"""빌드 없는 사이트의 내부 경로·앵커·도구 목록·실습 진행 키를 검사한다."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.nodes = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


def check():
    pages = {p: Page(p) for folder in ('site', 'shelf') for p in (ROOT / folder).rglob('*.html')}
    ids = {p: {a['id'] for _, a in page.nodes if 'id' in a} for p, page in pages.items()}
    errors, references = [], 0
    for path, page in pages.items():
        label = str(path.relative_to(ROOT))
        for id_, count in Counter(a['id'] for _, a in page.nodes if 'id' in a).items():
            if count > 1:
                errors.append(f'{label}: 중복 ID {id_}')
        for _, attrs in page.nodes:
            for key in ('href', 'src', 'poster'):
                if not attrs.get(key):
                    continue
                href = attrs[key]
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                references += 1
                if href.startswith('/'):
                    errors.append(f'{label}: 상대 경로 필요 {href}')
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                # Pages에서 shelf/가 루트이고 site/는 reels/ 아래에 놓인다.
                if path.is_relative_to(ROOT / 'shelf') and url.path:
                    logical = Path('/pages') / path.relative_to(ROOT / 'shelf').parent / unquote(url.path)
                    logical = logical.resolve().relative_to('/pages')
                    if logical.parts[:1] == ('reels',):
                        target = ROOT / 'site' / Path(*logical.parts[1:])
                    elif logical.parts[:2] == ('progress', 'samples'):
                        target = ROOT / 'starter-kit/samples' / logical.name
                if target.is_dir():
                    target /= 'index.html'
                if not target.is_file():
                    errors.append(f'{label}: 없는 파일 {href}')
                elif url.fragment and target in ids and unquote(url.fragment) not in ids[target]:
                    errors.append(f'{label}: 없는 앵커 {href}')
    catalog_text = (ROOT / 'site/assets/catalog.js').read_text()
    catalog = json.loads(catalog_text.split('Object.freeze(', 1)[1].rsplit(');', 1)[0])
    for tool in catalog:
        path = ROOT / 'site' / (f'chapters/{tool["slug"]}.html' if tool['chapter'] != 15 else 'lab.html')
        if tool['id'] not in ids.get(path, set()):
            errors.append(f'도구 목록: 없는 도구 {tool["slug"]}#{tool["id"]}')
    steps = {a['data-practice-check'] for p, page in pages.items() if p.parent.name == 'practice' and p.name != 'e2e.html' for _, a in page.nodes if 'data-practice-check' in a}
    e2e = {a['data-practice-check'] for _, a in pages[ROOT / 'site/practice/e2e.html'].nodes if 'data-practice-check' in a}
    if steps != e2e or len(steps) != 35:
        errors.append('실습 단계와 E2E 진행 키 불일치')
    return dict(html_pages=len(pages), internal_references=references, catalog_entries=len(catalog), practice_steps=len(steps), errors=errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check()
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end='')
    raise SystemExit(bool(result['errors']))
