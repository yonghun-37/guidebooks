"""HTML 추출 명령을 바꿔 보기의 수동 편집까지 포함해 읽는 순서로 재현한다.

python3.11 docs/results/phase-BX5/verify-reading.py
편집 값은 본문의 바꿔 보기 설명 그대로다. 선택한 Unix 명령은 검사기의 추출 JSON에서만 읽는다.
"""
import json,os,shlex,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
REPORT=Path(__file__).with_name('extracted-commands.json')
records=[]
with tempfile.TemporaryDirectory(prefix='bx5-full-reading-') as folder:
    kit=Path(folder)/'kit'
    shutil.copytree(ROOT/'blog-auto-kit',kit,ignore=shutil.ignore_patterns('.env','.venv','output','private','config.toml','__pycache__','.pytest_cache'))
    subprocess.run([sys.executable,'-m','venv',str(kit/'.venv')],check=True)
    python=str(kit/'.venv/bin/python')
    env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
    original_topics=(kit/'content/topics.py').read_text()
    def config(old,new):
        file=kit/'config.toml'
        if not file.exists():shutil.copyfile(kit/'config.example.toml',file)
        text=file.read_text();assert old in text,(old,text);file.write_text(text.replace(old,new))
    def edit_json(name,key,value):
        file=kit/name;data=json.loads(file.read_text());data[key]=value;file.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    def run(command,expect=0):
        words=shlex.split(command)
        if words[0]=='python':words[0]=python
        if words[0]=='cp':
            shutil.copyfile(kit/words[1],kit/words[2]);stdout='';code=0
        elif words[0]=='source':
            result=subprocess.run(['bash','-c',command],cwd=kit,env=env,text=True,capture_output=True,timeout=90);stdout=result.stdout;code=result.returncode
        else:
            result=subprocess.run(words,cwd=kit,env=env,text=True,capture_output=True,timeout=90);stdout=result.stdout;code=result.returncode
        print('$ '+command+'\n'+stdout,end='',flush=True)
        assert code==expect,(command,code,stdout,getattr(locals().get('result'), 'stderr',''))
        records.append({'command':command,'returncode':code,'stdout':stdout})
    for row in json.loads(REPORT.read_text())['chapters']:
        ch=row['chapter'];print('\n### '+ch,flush=True);change=0
        for block in row['blocks']:
            if block['os'] not in ('common','unix'):continue
            section=block['section'];expected_failure=False
            if section=='change':
                change+=1
                if ch=='A1' and block['text'].strip()=='python blog.py run --sample':config('today = "2026-10-27"','today = "2026-10-28"')
                if ch=='A2':config('editor@example.invalid','hello@example.invalid')
                if ch=='A3':
                    file=kit/'content/topics.py';assert '아이와 책 정리하기' in file.read_text();file.write_text(file.read_text().replace('아이와 책 정리하기','도서관 그림책 빌린 기록 정리하기'))
                if ch=='A4':config('monthly_cap_usd = "1.00"','monthly_cap_usd = "0.00"')
                if ch=='A5':edit_json('output/drafts/play.json','risk_flags',[])
                if ch=='A6' and change==2:
                    edit_json('output/drafts/info.json','description','지원 제도 확인 순서와 문의처');expected_failure=True
                if ch=='A7' and change==2:config('ad_after_h2 = 2','ad_after_h2 = 1')
                if ch=='A8' and change==2:config('today = "2026-10-27"','today = "2026-10-28"')
                if ch=='A9' and block['text'].strip()=='python blog.py publish --sample sponsor':
                    config('mode = "approval"','mode = "auto"');expected_failure=True
                if ch=='A10' and change==2:config('today = "2026-10-27"','today = "2026-10-28"')
                if ch=='A11' and change==2:config('today = "2026-10-27"','today = "2026-10-28"')
                if ch=='A11' and change==3:config('today = "2026-10-28"','today = "2026-10-29"')
                if ch=='A12' and change==1:config('mode = "approval"','mode = "auto"')
                if ch=='E2E':config('today = "2026-10-27"','today = "2026-10-28"')
            if section=='checkpoint' and ch=='A3':(kit/'content/topics.py').write_text(original_topics)
            for command in block['text'].splitlines():run(command,1 if expected_failure else 0)
            if section=='change':
                if ch=='A2':assert 'hello@example.invalid' in (kit/'output/pages/privacy.html').read_text()
                if ch=='A3':assert '도서관 그림책 빌린 기록 정리하기' in (kit/'output/topics.json').read_text()
                if ch=='A5':assert '사람 검토' in (kit/'output/gates/play.txt').read_text()
                if ch=='A7' and change==2:assert '첫째' in (kit/'output/ads/layout.html').read_text()
                if ch=='A8' and change==2:assert '2026-10-28' in (kit/'output/affiliate/links.csv').read_text()
                if ch=='A10' and change==2:assert '2026-10-28' in (kit/'output/analytics/weekly.html').read_text()
                if ch=='A11' and change==3:assert 'today = "2026-10-28"' in (kit/'config.toml').read_text()
        print(ch+' 읽는 순서·변경 후 복원 통과',flush=True)
print(f'전체 읽는 순서: {len(records)} 명령 / 예상한 차단 2 / 체크포인트 13장 통과')
Path(__file__).with_name('reading-order.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
