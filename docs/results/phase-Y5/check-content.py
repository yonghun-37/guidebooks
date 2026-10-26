"""표시 번호·정적 이동·배포 샘플·JS 구문을 현재 파일에서 대조한다."""
from pathlib import Path
import hashlib,json,re,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from build_appendices import Document,nodes,text
site=ROOT/'site-shorts'
chapters={p.stem:(p,int(re.search(r'data-chapter-number="(\d+)"',p.read_text())[1])) for p in (site/'chapters').glob('*.html') if p.name!='coming-soon.html'}
assert sorted(number for _,number in chapters.values())==list(range(1,16))
checked=0
for path,number in chapters.values():
 source=path.read_text();doc=Document(source).root
 assert re.search(r'data-chapter="'+re.escape(path.stem)+'"',source),path
 assert 'data-chapter-pager' in source,path
 assert '준비중' not in source,path
 for node in nodes(doc):
  if node.tag!='a':continue
  slug=Path(node.attrs.get('href','').split('#')[0]).stem
  reference=re.search(r'(\d+)장',text(node))
  if slug in chapters and reference:
   checked+=1;assert int(reference[1])==chapters[slug][1],(path,slug,reference[1])
 for kicker in re.findall(r'<[^>]*data-chapter-kicker[^>]*>([^<]*)</',source):
  if '/' in kicker:assert kicker.split('/')[-1].strip()==str(number),(path,kicker)
for name in ('short.mp4','preview.html','subtitles.srt'):
 assert (site/'assets/samples'/name).read_bytes()==(ROOT/'shorts-kit/samples'/name).read_bytes()
js=list(site.rglob('*.js'));inline=0
for p in js:subprocess.run(['node','--check',str(p)],check=True,capture_output=True)
with tempfile.TemporaryDirectory(prefix='y5-js-') as temp:
 for path in site.rglob('*.html'):
  for source in re.findall(r'<script\b[^>]*>(.*?)</script>',path.read_text(),re.S):
   if not source.strip():continue
   file=Path(temp)/f'{inline}.js';file.write_text(source);subprocess.run(['node','--check',str(file)],check=True,capture_output=True);inline+=1
result=dict(theory_chapters=len(chapters),numbered_static_links=checked,original_sample_files=3,external_js=len(js),inline_js=inline,errors=[])
(ROOT/'docs/results/phase-Y5/content-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
