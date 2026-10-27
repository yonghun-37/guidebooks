"""담당 장의 본문 명령·출력·발췌를 깨끗한 키트 복사본과 대조한다."""
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHAPTERS = {'A7':'07-ads', 'A8':'08-affiliate', 'A10':'10-analytics',
            'A11':'11-operations', 'A12':'12-policy', 'E2E':'e2e'}
PYTHON = os.environ.get('BX4B_PYTHON', '/tmp/bx4b-venv/bin/python')
class Blocks(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.items=[]; self.current=None; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in ('samp','code') and any(k in a for k in ('data-source','data-expected','data-run')):
            self.current={'tag':tag, 'attrs':a, 'text':''}
    def handle_data(self, data):
        if self.current is not None: self.current['text']+=data
    def handle_endtag(self, tag):
        if self.current and tag==self.current['tag']:
            self.items.append(self.current); self.current=None

def run(kit, command):
    args=shlex.split(command)
    assert args[0]=='python',command
    result=subprocess.run([PYTHON,*args[1:]],cwd=kit,capture_output=True,text=True,
        env={**os.environ,'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8'},timeout=60)
    assert result.returncode==0,(command,result.stdout,result.stderr)
    return result.stdout

records=[]
with tempfile.TemporaryDirectory(prefix='bx4b-manuscript-') as folder:
    kit=Path(folder)/'blog-auto-kit'
    shutil.copytree(ROOT/'blog-auto-kit',kit,ignore=shutil.ignore_patterns('.venv','__pycache__','.env','output','private','config.toml'))
    for chapter,slug in CHAPTERS.items():
        expected=json.loads((kit/f'course/expected/{chapter}/outputs.json').read_text())
        blocks=Blocks((ROOT/f'site-blog/advanced/{slug}.html').read_text()).items
        allowed=set(re.findall(r'`(python [^`]+)`',(kit/'course/commands.md').read_text()))
        allowed.update(f'python course.py {action} {chapter}' for action in ('start','check'))
        for block in blocks:
            if 'data-run' not in block['attrs']: continue
            for line in block['text'].splitlines():
                if line.startswith('python '): assert line in allowed,(chapter,line,'commands.md 밖 명령')
        shown={b['attrs']['data-expected']:b['text'].strip() for b in blocks if 'data-expected' in b['attrs']}
        for command,row in expected.items():
            assert shown[f'{chapter}|{command}']==row['stdout'].strip(),(chapter,command,'본문 성공 문구 불일치')
        sources=0
        for b in blocks:
            if 'data-source' not in b['attrs']: continue
            name,start,end=b['attrs']['data-source'].rsplit(':',2)
            start,end=int(start),int(end)
            assert end-start+1<=25
            actual='\n'.join((kit/name).read_text().splitlines()[start-1:end])
            assert actual==b['text'],(chapter,name,'코드 발췌 불일치')
            sources+=1
        start=run(kit,f'python course.py start {chapter}')
        outputs=[]
        for command,row in expected.items():
            actual=run(kit,command)
            assert actual==row['stdout'],(chapter,command,'실제 stdout 불일치')
            outputs.append({'command':command,'stdout':actual,'expected_match':True})
        check=run(kit,f'python course.py check {chapter}')
        records.append({'chapter':chapter,'start':start,'commands':outputs,'check':check,'source_excerpts':sources})
        print(chapter,'본문·expected·실행 stdout·발췌·check 일치',flush=True)
        if chapter=='A8':
            run(kit,'python course.py start A8')
            config=kit/'config.toml'
            config.write_text((kit/'config.example.toml').read_text().replace('today = "2026-10-27"','today = "2026-10-28"'))
            run(kit,'python blog.py affiliate --sample affiliate')
            assert '2026-10-28' in (kit/'output/affiliate/links.csv').read_text()
            run(kit,'python course.py start A8')
            run(kit,'python blog.py affiliate --sample affiliate')
            run(kit,'python blog.py gate --sample affiliate')
            run(kit,'python course.py check A8')
            records.append({'A8_change':'clock.today 변경 후 checked_on 2026-10-28, 복원 후 check 통과'})
    before=(kit/'output/scenarios.json').read_bytes()
    config=kit/'config.toml'
    shutil.copyfile(kit/'config.example.toml',config)
    text=config.read_text().replace('today = "2026-10-27"','today = "2026-10-28"')
    config.write_text(text)
    run(kit,'python blog.py run --scenarios')
    assert (kit/'output/scenarios.json').read_bytes()==before
    run(kit,'python course.py start E2E')
    run(kit,'python blog.py run --scenarios')
    run(kit,'python course.py check E2E')
    records.append({'E2E_change':'clock.today 변경 후 시나리오 JSON 바이트 동일, 복원 후 check 통과'})
(ROOT/'docs/results/phase-BX4b/commands.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
