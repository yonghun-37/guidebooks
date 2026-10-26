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
    assert sys.version_info >= (3, 11), 'Python 3.11 이상에서 실행하세요.'
    checked=[]
    with tempfile.TemporaryDirectory() as temporary:
        root=Path(temporary)/'auto-kit'
        shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.venv','__pycache__','.pytest_cache','private','output','.env'))
        def run(*args,expected=0):
            result=subprocess.run([sys.executable,*args],cwd=root,capture_output=True,text=True)
            assert result.returncode==expected,(args,result.stdout,result.stderr)
            checked.append({'command':'python '+' '.join(args),'exit':result.returncode,'stdout':result.stdout.strip()})
            return result.stdout
        assert 'mock 준비 완료' in run('doctor.py')
        assert 'dry_run' in run('pipeline.py','run','--flow','insta','--provider','mock','--mode','auto')
        shorts_text=run('pipeline.py','run','--flow','shorts','--provider','mock','--mode','auto')
        assert 'dry_run' in shorts_text
        shorts_id=re.search(r'[a-f0-9]{12}',shorts_text)[0]
        assert '월급날' in run('pipeline.py','inspect',shorts_id,'--flow','shorts','--artifact','draft')
        assert 'upload' in run('pipeline.py','inspect',shorts_id,'--flow','shorts','--artifact','request-plan')
        text=run('pipeline.py','run','--flow','insta','--provider','mock','--state','private/review-demo')
        identifier=re.search(r'[a-f0-9]{12}',text)[0]
        run('pipeline.py','approve',identifier,'--state','private/review-demo')
        assert 'dry_run' in run('pipeline.py','resume',identifier,'--state','private/review-demo')
        text=run('pipeline.py','run','--flow','insta','--provider','mock','--mode','post_review','--state','private/schedule-demo')
        assert 'scheduled' in text
        scheduled=re.search(r'[a-f0-9]{12}',text)[0]
        assert 'rejected' in run('pipeline.py','reject',scheduled,'--state','private/schedule-demo')
        run('pipeline.py','status');run('pipeline.py','report')
        assert '지표 CSV 저장 완료' in run('insights.py',identifier,'--state','private/review-demo')
        for os_name in ('windows','macos','cron'):
            assert '예약 파일 생성 완료' in run('-m','schedule.install','--os',os_name,'--flow','shorts' if os_name=='macos' else 'insta','--time','09:17')
        for file in ('install-insta-cron.sh','install-shorts-macos.sh'):
            subprocess.run(['sh','-n',str(root/'private/schedule'/file)],check=True)
        run('pipeline.py','tick','--flow','insta','--provider','mock','--mode','auto','--state','private/daily','--daily-at','09:17')
        assert json.loads(run('pipeline.py','tick','--flow','insta','--provider','mock','--mode','auto','--state','private/daily','--daily-at','09:17')) == []
        run('-c',"from common import load_config,save_json; c=load_config(); c['gates']['sensitive_words'].append('신청'); save_json('private/exception-config.json',c)")
        bad=run('pipeline.py','run','--flow','insta','--provider','mock','--mode','auto','--config','private/exception-config.json','--state','private/exception-demo',expected=2)
        old_id=re.search(r'[a-f0-9]{12}',bad)[0]
        assert '신청' in run('pipeline.py','inspect',old_id,'--flow','insta','--artifact','gates','--state','private/exception-demo')
        run('pipeline.py','approve',old_id,'--state','private/exception-demo',expected=1)
        assert 'dry_run' in run('pipeline.py','run','--flow','insta','--provider','mock','--mode','auto','--state','private/exception-fixed')
        assert old_id in json.loads(run('pipeline.py','report','--state','private/exception-demo'))['exceptions']
        assert 'rejected' in run('pipeline.py','reject',old_id,'--state','private/exception-demo')
        assert json.loads(run('pipeline.py','report','--state','private/exception-demo'))['exceptions']==[]
        shutil.copyfile(root/'config.example.json',root/'config.json')
        shutil.copyfile(root/'.env.example',root/'.env')
        assert '[error]' in run('doctor.py','--config','config.json','--live','--flow','insta',expected=1)
        config=json.loads((root/'config.json').read_text(encoding='utf-8-sig'))
        config['sources']['files']=[]
        config['sources']['rss']=[{'url':f'sources/{flow}-feed.xml','flow':flow,'synthetic':True,'rights_reviewed':False,'category':category} for flow,category in [('insta','생활 뉴스'),('shorts','자취 생활')]]
        (root/'config.json').write_text(json.dumps(config,ensure_ascii=False),encoding='utf-8')
        for flow in ('insta','shorts'):
            assert 'dry_run' in run('pipeline.py','run','--flow',flow,'--provider','mock','--mode','auto','--config','config.json','--state','private/rss-demo')
        assert '4 passed' in run('-m','pytest','-q','tests/test_core.py','-k','example_fact')
        run('-c',"from cryptography.fernet import Fernet; from pathlib import Path; p=Path('private/state-encryption.key'); p.parent.mkdir(exist_ok=True); p.write_bytes(Fernet.generate_key()); p.chmod(0o600)")
        assert (root/'private/state-encryption.key').is_file()
    # repo 연구 링크는 원래 위치에서 확인한다. HTML/CSS의 상대 링크도 확인한다.
    links=[]
    class Parser(HTMLParser):
        def handle_starttag(self,tag,attrs):
            values=dict(attrs)
            for name in ('href','src','srcset'):
                if values.get(name):links.append((self.file,values[name]))
    parser=Parser()
    for file in ROOT.rglob('*'):
        if not file.is_file() or any(p in ('.venv','private','__pycache__','.pytest_cache') for p in file.relative_to(ROOT).parts):continue
        if file.suffix=='.md':links.extend((file,target) for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',file.read_text()))
        if file.suffix in ('.html','.svg'):
            parser.file=file;parser.feed(file.read_text())
    bad=[]
    for file,target in links:
        parsed=urlsplit(target)
        if parsed.scheme or not parsed.path or target.startswith('<'):continue
        if not (file.parent/unquote(parsed.path)).exists():bad.append((str(file.relative_to(ROOT)),target))
    assert not bad,bad
    result={'python_version':sys.version.split()[0],'clean_copy_commands':len(checked),'commands':checked,'local_links':len(links),'link_errors':len(bad),'external_calls':0}
    destination=ROOT/'docs/verification/commands.json';destination.parent.mkdir(exist_ok=True,parents=True)
    destination.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'},ensure_ascii=False))

if __name__=='__main__':main()
