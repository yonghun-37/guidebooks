"""쇼츠 심화 시각자료의 구조·출처·실제 산출물 수치를 검증한다."""
from pathlib import Path
from html.parser import HTMLParser
import json, re
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.figures=[]; self.figure=None; self.svg=None; self.svgs=[]; self.ids=[]; self.refs=[]; self.images=[]; self.in_caption=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and a.get('href','').startswith('#source-'):self.refs.append(a['href'][1:])
        if tag=='figure':self.figure={'id':a.get('id'),'caption':'','visuals':0}
        if tag in ('svg','video','img') and self.figure:self.figure['visuals']+=1
        if tag=='svg':self.svg=a;self.svgs.append(a)
        if tag=='figcaption':self.in_caption=True
        if tag=='img':self.images.append(a)
    def handle_endtag(self,tag):
        if tag=='figcaption':self.in_caption=False
        if tag=='figure':self.figures.append(self.figure);self.figure=None
    def handle_data(self,data):
        if self.figure and self.in_caption:self.figure['caption']+=data
errors=[];pages=[]
for p in sorted((ROOT/'site-shorts/advanced').glob('*.html')):
    s=p.read_text(); parsed=Page();parsed.feed(s)
    for f in parsed.figures:
        if not f['caption'].strip() or not f['visuals']:errors.append(f'{p.name}: figure incomplete {f}')
    if len(parsed.ids)!=len(set(parsed.ids)):errors.append(f'{p.name}: duplicate ids')
    for ref in parsed.refs:
        if ref not in parsed.ids:errors.append(f'{p.name}: missing {ref}')
    for svg in parsed.svgs:
        if svg.get('role')!='img' or not(svg.get('aria-label') or svg.get('aria-labelledby')):errors.append(f'{p.name}: SVG alt missing')
    for img in parsed.images:
        for key in ['alt','loading','width','height']:
            if not img.get(key):errors.append(f'{p.name}: image missing {key}')
    pages.append({'file':p.name,'figures':len(parsed.figures),'svg':len(parsed.svgs),'images':len(parsed.images)})
webps=[{'file':str(p.relative_to(ROOT)),'bytes':p.stat().st_size} for p in (ROOT/'site-shorts/assets/img/advanced').glob('frame-*.webp')]
if len(webps)!=3 or any(p['bytes']>400*1024 for p in webps):errors.append('frame count/size')
g=json.loads((OUT/'mock-gates.json').read_text());fail=json.loads((OUT/'facts-failure.json').read_text())
if not all(v['passed'] for v in g.values()):errors.append('normal gates did not all pass')
if fail['facts']['passed'] or fail['facts']['reasons']!=['원문에 없는 숫자: 99']:errors.append('failed facts mismatch')
if g['specification']['media'][0]['duration']!=36.1:errors.append('duration mismatch')
# Research comparison arithmetic stays independent of the current 2..5 scene schema.
from decimal import Decimal as D
model=json.loads((ROOT/'research-advanced/cost-model.json').read_text())
low=next(x for x in model['scenarios'] if x['scenario']=='shorts-low');high=next(x for x in model['scenarios'] if x['scenario']=='shorts-high')
assert D(low['per_item_usd'])*30==D('.096')
assert D(high['per_item_usd'])*30==D('7.095')
assert (D(high['per_item_usd'])+10*D('.05'))*30==D('22.095')
status_page=(ROOT/'site-shorts/advanced/05-youtube.html').read_text()
if '처음 failed · 재개 때 uncertain' not in status_page or 'failed → Studio 기존 영상 대조' not in status_page:errors.append('upload status distinction missing')
report={'pages':pages,'total_figures':sum(p['figures'] for p in pages),'frames':webps,'actual_gates':list(g),'cost_arithmetic':'passed','errors':errors}
(OUT/'content-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
