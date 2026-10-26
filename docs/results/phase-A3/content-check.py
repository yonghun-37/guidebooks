"""심화편 A출처·FAQ·퀴즈·그림 접근성 추가 검사. 표준 check_site의 S출처 검사 보완."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re

ROOT = Path(__file__).resolve().parents[3]

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.nodes = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

errors, results, all_sources = [], [], set()
sources = set(re.findall(r'^### (A\d+)\.', (ROOT / 'research-advanced/SOURCES.md').read_text(), re.M))
credits = (ROOT / 'site/credits.html').read_text()
for file in sorted((ROOT / 'site/advanced').glob('*.html')):
    source = file.read_text()
    nodes = Page(source).nodes
    ids = {attrs['id'] for _, attrs in nodes if 'id' in attrs}
    citations = set(re.findall(r'\[(A\d+)\]', source))
    all_sources.update(citations)
    quiz_count = sum('data-question' in attrs for _, attrs in nodes)
    faq_count = sum(tag == 'details' and attrs.get('id', '').startswith('faq-') for tag, attrs in nodes)
    if file.name != 'e2e.html':
        if quiz_count != 3:
            errors.append(f'{file.name}: quiz {quiz_count}, expected 3')
        if faq_count != 5:
            errors.append(f'{file.name}: FAQ {faq_count}, expected 5')
    for citation in citations:
        if citation not in sources:
            errors.append(f'{file.name}: unknown source {citation}')
        if 'source-' + citation.lower() not in ids:
            errors.append(f'{file.name}: missing source footnote {citation}')
        if f'id="{citation.lower()}"' not in credits:
            errors.append(f'credits: missing {citation}')
    for tag, attrs in nodes:
        if tag == 'svg' and not attrs.get('aria-label') and not attrs.get('aria-labelledby'):
            errors.append(f'{file.name}: unnamed SVG')
        if tag == 'img' and (not attrs.get('width') or not attrs.get('height') or attrs.get('loading') != 'lazy'):
            errors.append(f'{file.name}: image attributes')
    results.append({'file': str(file.relative_to(ROOT)), 'citations': len(citations), 'faq': faq_count, 'quiz': quiz_count})
report = {'files': results, 'unique_A_sources': len(all_sources), 'errors': errors}
(ROOT / 'docs/results/phase-A3/content-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'pages': len(results), 'A_sources': len(all_sources), 'errors': errors}, ensure_ascii=False))
raise SystemExit(bool(errors))
