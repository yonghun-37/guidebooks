"""Check Phase 8s drafts without changing existing site content.
Run from repository root: python3 docs/results/phase-8s/static_check.py
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/results/phase-8s'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.text, self.blocks = [], [], [], []
        self.skip, self.simulators = 0, 0
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ('style', 'script'):
            self.skip += 1
        if d.get('id'):
            self.ids.append(d['id'])
        self.refs.extend(d[k] for k in ('href', 'src') if k in d)
        if 'data-block' in d:
            self.blocks.append(d['data-block'])
        if 'data-simulator' in d:
            self.simulators += 1
    def handle_endtag(self, tag):
        if tag in ('style', 'script'):
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)

def parse(path):
    p = Page()
    p.feed(path.read_text())
    return p

errors, lengths, checked = [], {}, 0
current = len(''.join(parse(ROOT / 'site/chapters/03-revenue.html').text))
for f in sorted((ROOT / 'site/drafts').glob('*.html')):
    p = parse(f)
    if len(p.ids) != len(set(p.ids)):
        errors.append(f'{f.name}: duplicate IDs')
    if f.name.startswith('ch03-'):
        lengths[f.name] = len(''.join(p.text))
        if lengths[f.name] >= current:
            errors.append(f'{f.name}: not shorter than current chapter')
        if p.blocks != ['question','figure','principle','simulator','case','workshop','story','summary','quiz']:
            errors.append(f'{f.name}: wrong nine blocks')
        if p.simulators != 1:
            errors.append(f'{f.name}: simulator count')
    for raw in p.refs:
        u = urlparse(raw)
        if u.scheme or u.netloc:
            continue
        target = (f.parent / unquote(u.path)).resolve() if u.path else f
        checked += 1
        if not target.exists():
            errors.append(f'{f.name}: missing {raw}')
        elif u.fragment and unquote(u.fragment) not in parse(target).ids:
            errors.append(f'{f.name}: missing anchor {raw}')
for f in [ROOT/'docs/learner-questions.md',ROOT/'docs/style-guide.md',ROOT/'research/monetization-explainer.md']:
    for raw in re.findall(r'\]\(([^)]+)\)', f.read_text()):
        u = urlparse(raw)
        if u.scheme:
            continue
        target = (f.parent/u.path).resolve()
        checked += 1
        if not target.exists():
            errors.append(f'{f.name}: missing {raw}')
        elif u.fragment and target.suffix == '.html' and u.fragment not in parse(target).ids:
            errors.append(f'{f.name}: missing anchor {raw}')
ids = re.findall(r'<a id="(s\d+)"></a>', (ROOT/'research/SOURCES.md').read_text())
if len(ids) != len(set(ids)):
    errors.append('duplicate source IDs')
questions = (ROOT/'docs/learner-questions.md').read_text()
judgments = re.findall(r'\| (답함|부분|안 함) \|',questions)
if len(judgments) != 70:
    errors.append('learner question count must be 70')
protected = json.loads((OUT/'protected-files.json').read_text())
changed = [p for p,h in protected.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest() != h]
result = {'checkedLocalReferences':checked, 'sourceCount':len(ids), 'currentChapterTextCharacters':current,
          'sampleTextCharacters':lengths, 'learnerQuestions':len(judgments),
          'judgments':{s:judgments.count(s) for s in ('답함','부분','안 함')},
          'protectedSiteFiles':len(protected),'existingSiteFilesChangedSinceSnapshot':changed,'errors':errors}
(OUT/'static-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
assert not errors
# A concurrently edited existing site file is reported, never restored.
