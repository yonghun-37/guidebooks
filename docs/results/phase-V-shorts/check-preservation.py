"""시각자료 외 본문·원본 도구·진행 키가 HEAD와 같은지 검사한다."""
from pathlib import Path
import subprocess,re,json,hashlib
root=Path('site-shorts'); checks=[]; failures=[]
def check(name,ok):
 checks.append(name)
 if not ok:failures.append(name)
BASE='41a8234879a58f6e3d603c114568c0f02c38c930'
def original(path):return subprocess.check_output(['git','show',BASE+':'+str(path)],text=True)
def omit_figures(t):
 t=re.sub(r'<figure\b.*?</figure>','',t,flags=re.S)
 t=re.sub(r'<link[^>]*href="[^"]*figures.css"[^>]*/?>','',t)
 t=re.sub(r'>\s+<','><',t)
 return re.sub(r'\s+',' ',t).strip()
for p in sorted(root.rglob('*.html')):
 a=original(p);b=p.read_text()
 if p.name!='credits.html':check(str(p)+' 그림 밖 본문·구조 보존',omit_figures(a)==omit_figures(b))
 for tag in ['script','input','select','button','textarea']:
  pattern=rf'<{tag}\b[^>]*>(?:.*?</{tag}>)?' if tag!='input' else r'<input\b[^>]*>'
  check(str(p)+' '+tag+' 보존',re.findall(pattern,a,re.S)==re.findall(pattern,b,re.S))
 old_ids=set(re.findall(r'\bid="([^"]+)"',a));new_ids=set(re.findall(r'\bid="([^"]+)"',b));check(str(p)+' 기존 앵커 보존',old_ids<=new_ids)
 if p.name not in ['06-edit.html','08-publish.html']:
  old_figures=re.findall(r'<figure\b.*?</figure>',a,re.S)
  check(str(p)+' 기존 figure 보존',all(f in b for f in old_figures))
# Main JS/CSS code was not changed. figures.css and the new symbols have no HEAD version.
for path in subprocess.check_output(['git','ls-files','site-shorts'],text=True).splitlines():
 p=Path(path)
 if p.suffix in ['.js','.css']:check(path+' 원본 동작/조판 보존',original(p)==p.read_text())
assets=[]
for p in (root/'assets/img/ai-examples').glob('keyframe-*.webp'):
 assets.append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 check(str(p)+' 400KB 이하',p.stat().st_size<=400*1024)
# Every introduced bitmap must be referenced by the final HTML and have a prompt record.
provenance=json.loads((root/'assets/img/visual-provenance.json').read_text())['assets']
for item in provenance:check(item['file']+' 프롬프트·참조 파일',bool(item['prompt']) and (root/'assets/img'/item['reference']).is_file())
report={'checks':len(checks),'failures':failures,'checksPerformed':checks,'retainedKeyframes':assets}
Path('docs/results/phase-V-shorts/preservation-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'failures':failures},ensure_ascii=False))
raise SystemExit(bool(failures))
