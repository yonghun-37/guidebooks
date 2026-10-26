"""깨끗한 복사본에서 문서의 오프라인 명령과 로컬 링크를 확인한다."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[1]

def main():
    checked=[]
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary)/'auto-kit'
        shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.venv','__pycache__','.pytest_cache','private','output','.env'))
        def run(*args,expected=0):
            result=subprocess.run([sys.executable,*args],cwd=root,capture_output=True,text=True)
            assert result.returncode==expected,(args,result.stdout,result.stderr)
            checked.append({'command':'python '+' '.join(args),'exit':result.returncode})
            return result.stdout
        assert 'mock 준비 완료' in run('doctor.py')
        assert 'dry_run' in run('pipeline.py','run','--flow','insta','--provider','mock','--mode','auto')
        assert 'dry_run' in run('pipeline.py','run','--flow','shorts','--provider','mock','--mode','auto')
        text=run('pipeline.py','run','--flow','insta','--provider','mock','--state','private/review-demo')
        identifier=re.search(r'[a-f0-9]{12}',text)[0]
        run('pipeline.py','approve',identifier,'--state','private/review-demo')
        assert 'dry_run' in run('pipeline.py','resume',identifier,'--state','private/review-demo')
        run('pipeline.py','status');run('pipeline.py','report')
        run('insights.py',identifier,'--state','private/review-demo')
        for os_name in ('windows','macos','cron'):
            assert '예약 파일 생성 완료' in run('-m','schedule.install','--os',os_name,'--flow','insta','--time','09:17')
        for file in ('install-insta-cron.sh','install-insta-macos.sh'):
            subprocess.run(['sh','-n',str(root/'private/schedule'/file)],check=True)
        run('pipeline.py','tick','--flow','insta','--provider','mock','--mode','auto','--state','private/daily','--daily-at','00:00')
        run('pipeline.py','tick','--flow','insta','--provider','mock','--mode','auto','--state','private/daily','--daily-at','00:00')
        assert 'error' in run('doctor.py','--live','--flow','insta',expected=1)
    # repo 연구 링크는 원래 위치에서 확인한다. HTML/CSS의 상대 링크도 확인한다.
    links=[]
    class Parser(HTMLParser):
        def handle_starttag(self,tag,attrs):
            values=dict(attrs)
            for name in ('href','src','srcset'):
                if values.get(name):links.append((self.file,values[name]))
    parser=Parser()
    for file in ROOT.rglob('*'):
        if not file.is_file() or any(p in ('private','__pycache__','.pytest_cache') for p in file.relative_to(ROOT).parts):continue
        if file.suffix=='.md':links.extend((file,target) for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',file.read_text()))
        if file.suffix in ('.html','.svg'):
            parser.file=file;parser.feed(file.read_text())
    bad=[]
    for file,target in links:
        parsed=urlsplit(target)
        if parsed.scheme or not parsed.path or target.startswith('<'):continue
        if not (file.parent/unquote(parsed.path)).exists():bad.append((str(file.relative_to(ROOT)),target))
    assert not bad,bad
    result={'clean_copy_commands':len(checked),'commands':checked,'local_links':len(links),'link_errors':len(bad),'external_calls':0}
    destination=ROOT/'docs/verification/commands.json';destination.parent.mkdir(exist_ok=True,parents=True)
    destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'},ensure_ascii=False))

if __name__=='__main__':main()
