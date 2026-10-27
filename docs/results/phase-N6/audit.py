"""통합 이후 연결·응급 문구·내부 용어의 재현 가능한 정적 전수 점검."""
import importlib.util
import json
from pathlib import Path
import posixpath
import re

ROOT=Path(__file__).resolve().parents[3]
SITE=ROOT/'site-baby'
spec=importlib.util.spec_from_file_location('appendices',ROOT/'scripts/build_baby_appendices.py')
baby=importlib.util.module_from_spec(spec);spec.loader.exec_module(baby)
files={p.relative_to(SITE).as_posix():p for folder in ['chapters','practice'] for p in (SITE/folder).glob('*.html')}
edges=set();term_links=0;hosts=0
for key,p in files.items():
 text=p.read_text()
 term_links+=len(re.findall(r' data-term=',text))
 hosts+=len(re.findall(r' data-emergency=',text))
 for href in re.findall(r'href="([^"]+)"',text):
  dst=posixpath.normpath(posixpath.join(posixpath.dirname(key),href.split('#')[0].split('?')[0]))
  if dst in files and dst.split('/')[0]!=key.split('/')[0]:edges.add((key,dst))
missing=[(a,b) for a,b in edges if (b,a) not in edges]
# The canonical seven messages must occur only in their data module.
text=(SITE/'assets/emergency-data.js').read_text()
messages=re.findall(r'"text": "([^"]+)"',text)
duplicates=[]
for p in [*SITE.rglob('*.html'),*(SITE/'assets').glob('*.js')]:
 if p.name=='emergency-data.js':continue
 for message in messages:
  if message in p.read_text():duplicates.append(str(p.relative_to(SITE)))
assert len(messages)==7
assert not missing,missing
assert not duplicates,duplicates
assert len(baby.TERMS)==40 and len(baby.TOOLS)==15
source_ids=baby.cited()
assert source_ids<=baby.sources().keys()
report={
 'html_pages':len(list(SITE.rglob('*.html'))),
 'cross_track_directed_edges':len(edges),'missing_reverse_links':missing,
 'first_use_glossary_links':term_links,'canonical_emergency_messages':len(messages),
 'chapter_practice_emergency_hosts':hosts,'copied_canonical_messages':duplicates,
 'cited_sources':sorted(source_ids),'unused_registry_sources':sorted(baby.sources().keys()-source_ids),
 'glossary_terms':len(baby.TERMS),'original_tools':len(baby.TOOLS),
 'review_scope':'이론 1~13, 실습 0~10/E2E, 표지·출처·용어집·실험실·인쇄 4종을 읽고 설계 8·11절과 비교. 수치 및 장면의 수동 대조 결과는 phase-N6.md에 기록.',
}
(Path(__file__).parent/'consistency-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print({k:v for k,v in report.items() if k not in ['cited_sources','unused_registry_sources','review_scope']})
