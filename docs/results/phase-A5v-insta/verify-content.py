"""A5v-insta 그림·출처·실제 출력 대조. 저장소 루트에서 실행한다."""
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter
from decimal import Decimal
import json, re, subprocess, xml.etree.ElementTree as ET

ROOT = Path.cwd()
DEST = ROOT / 'docs/results/phase-A5v-insta'
class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.nodes=[]; self.feed(text)
    def handle_starttag(self, tag, attrs): self.nodes.append((tag, dict(attrs)))
    def handle_startendtag(self, tag, attrs): self.handle_starttag(tag, attrs)

errors, pages = [], []
sources = set(re.findall(r'^### (A\d+)\.', (ROOT/'research-advanced/SOURCES.md').read_text(), re.M))
credits = (ROOT/'site/credits.html').read_text()
for p in sorted((ROOT/'site/advanced').glob('*.html')):
    text=p.read_text(); tags=Tags(text).nodes
    ids=Counter(a['id'] for _,a in tags if 'id' in a)
    for id,count in ids.items():
        if count>1: errors.append(f'{p.name}: duplicate id {id}')
    for ref in re.findall(r'\[(A\d+)\]',text):
        if ref not in sources or 'source-'+ref.lower() not in ids or f'id="{ref.lower()}"' not in credits:
            errors.append(f'{p.name}: source {ref}')
    figures=re.findall(r'<figure\b.*?</figure>',text,re.S)
    for figure in figures:
        if not re.search(r'<figcaption\b[^>]*>.+?</figcaption>',figure,re.S):errors.append(f'{p.name}: missing caption')
        for fragment in re.findall(r'<svg\b.*?</svg>',figure,re.S):
            try: ET.fromstring(fragment)
            except ET.ParseError as exc: errors.append(f'{p.name}: SVG syntax {exc}')
    for tag,a in tags:
        if tag=='svg' and (a.get('role')!='img' or not(a.get('aria-label') or a.get('aria-labelledby'))):errors.append(f'{p.name}: SVG name')
        if tag=='img':
            if not a.get('alt') or not a.get('width') or not a.get('height') or a.get('loading')!='lazy':errors.append(f'{p.name}: img attributes')
            path=p.parent/a['src']
            if path.suffix=='.webp' and path.stat().st_size>400000:errors.append(f'{p.name}: raster too large')
    # Compare explanatory p elements, excluding figure captions and SVG descriptions.
    old=subprocess.check_output(['git','show',f'HEAD:{p.relative_to(ROOT)}'],text=True)
    pchars=lambda s:sum(len(re.sub(r'\s|<[^>]*>','',v)) for v in re.findall(r'<p\b[^>]*>(.*?)</p>',s,re.S))
    pages.append({'file':p.name,'figures':len(figures),'svg':sum(tag=='svg' for tag,_ in tags),'paragraph_chars_before':pchars(old),'paragraph_chars_after':pchars(text)})
fixtures=ROOT/'site/advanced/examples'
normal=json.loads((fixtures/'auto-gates.json').read_text());exc=json.loads((fixtures/'exception-gates.json').read_text())
assert all(item['passed'] for item in normal.values())
assert exc['policy']=={'passed':False,'reasons':['검토 단어: 신청']}
assert json.loads((fixtures/'approval-notification.json').read_text())['status']=='waiting_approval'
assert json.loads((fixtures/'daily-report.json').read_text())['spend']['total']==0
model=json.loads((ROOT/'research-advanced/cost-model.json').read_text())
low,high=[r for r in model['scenarios'] if r['scenario'].startswith('instagram-')]
assert Decimal(low['monthly_30_usd'])==Decimal('.02400')
assert Decimal(high['monthly_30_usd'])+Decimal('.50')*30==Decimal('16.49250')
# The private source output is optional for later reruns; the current run verifies exact JSON copies.
meta=json.loads((DEST/'mock-evidence.json').read_text());work=Path(meta['work'])
if work.exists():
    for label in ['auto','approval','exception']:
        run=work/'private'/label/meta['runs'][label]['id']
        for name in (['notification.json'] if label=='approval' else ['gates.json','notification.json']):
            original=json.loads((run/name).read_text());original.pop('binding',None)
            assert original==json.loads((fixtures/f'{label}-{name}').read_text())
report={'pages':pages,'figures':sum(p['figures'] for p in pages),'svg':sum(p['svg'] for p in pages),'source_output_compared':work.exists(),'paragraph_chars_before':sum(p['paragraph_chars_before'] for p in pages),'paragraph_chars_after':sum(p['paragraph_chars_after'] for p in pages),'errors':errors}
(DEST/'content-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
