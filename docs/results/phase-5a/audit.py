"""Phase 5a 원고의 사실 ID·출처·명령 산출물 정합성 확인. 저장소 루트에서 실행."""
from pathlib import Path
from html.parser import HTMLParser
import re, json, hashlib
root=Path.cwd()
facts={}
for line in (root/'research/FACT-SHEET.md').read_text().splitlines():
    cells=line.split('|')
    if len(cells)>5 and re.fullmatch(r'[A-Z]+-\d+',cells[1].strip()):
        facts[cells[1].strip()]=set(re.findall(r'\[(S\d+)\]',cells[3]))
source_text=(root/'research/SOURCES.md').read_text()
source_urls={m[1]:m[2] for m in re.finditer(r'### (S\d+)\..*?\n- URL: (\S+)',source_text,re.S)}
class Audit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.facts=[];self.ids=[];self.refs=[];self.external=[];self.blocks=[];self.code=[];self.in_code=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if 'data-block' in a:self.blocks.append(a['data-block'])
        if 'data-fact-id' in a:self.facts.extend(a['data-fact-id'].split())
        if tag=='a':
            href=a.get('href','')
            if href.startswith('#source-'):self.refs.append(href[8:].upper())
            if href.startswith('http'):self.external.append(href)
        if tag=='code':self.in_code=True
    def handle_endtag(self,tag):
        if tag=='code':self.in_code=False
    def handle_data(self,data):
        if self.in_code:self.code.append(data)
rows=[]
for slug in ['02-formats','03-revenue','04-niche','05-sources']:
    page=root/f'site/chapters/{slug}.html';parser=Audit();parser.feed(page.read_text())
    assert len(parser.ids)==len(set(parser.ids))
    assert len(parser.blocks)==9
    expected=set()
    for fid in parser.facts:assert fid in facts;expected |= facts[fid]
    assert set(parser.refs)==expected,(slug,set(parser.refs)^expected)
    assert all(f'source-{sid.lower()}' in parser.ids for sid in expected)
    assert all(url in source_urls.values() for url in parser.external)
    rows.append({'slug':slug,'factIds':sorted(set(parser.facts)),'sources':sorted(expected),'bytes':page.stat().st_size})
news=root/'starter-kit/output/phase-5a/news.json';data=json.loads(news.read_text())
assert data['synthetic'] is True and len(data['articles'])==3
assert all(a['synthetic'] is True for a in data['articles'])
result={'chapters':rows,'starterKit':{'command':'.venv/bin/python fetch_news.py --feed fixtures/sample-feed.xml --output output/phase-5a/news.json','workingDirectory':'starter-kit','synthetic':True,'articles':3,'sha256':hashlib.sha256(news.read_bytes()).hexdigest()},'passed':True}
(root/'docs/results/phase-5a/audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'chapters':len(rows),'factSourceAudit':'pass','syntheticArticles':3}))
