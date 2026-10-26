"""담당 장의 자원·앵커·외부 페이지에서 오는 앵커를 검사합니다."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.refs = [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.refs.append(attrs[key])


files = sorted(Path('site/chapters').glob('0[1-4]-*.html'))
owned = {path.resolve() for path in files}
errors, checked, incoming = [], 0, 0
for path in Path('site').rglob('*.html'):
    doc = Document(path.read_text())
    if path.resolve() in owned:
        errors.extend({'path': str(path), 'duplicate': id_}
                      for id_, count in Counter(doc.ids).items() if count > 1)
    for ref in doc.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
        is_owned = path.resolve() in owned
        is_incoming = target in owned and bool(url.fragment)
        if not is_owned and not is_incoming:
            continue
        checked += is_owned
        incoming += is_incoming
        if not target.exists():
            errors.append({'path': str(path), 'reference': ref, 'error': 'missing file'})
        elif url.fragment and target.suffix == '.html':
            if unquote(url.fragment) not in Document(target.read_text()).ids:
                errors.append({'path': str(path), 'reference': ref, 'error': 'missing anchor'})
report = {'files': len(files), 'local_references': checked,
          'incoming_anchored_references': incoming, 'errors': errors}
Path('docs/results/phase-9a/static-check.json').write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(bool(errors))
