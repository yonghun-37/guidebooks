"""키·네트워크 없이 공개 가능한 작은 샘플만 내보낸다."""
from pathlib import Path
import json
import shutil
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import ROOT, load_config, save_json
from pipeline import Pipeline

def main():
    target=ROOT/'samples';target.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        config=load_config();config['mode']='auto';p=Pipeline(config,Path(temporary)/'state')
        ids={}
        for flow in ('insta','shorts'):
            run=p.run(flow,provider='mock')
            if run['status']!='dry_run':raise ValueError('샘플 관문 실패: '+run['status'])
            ids[run['id']]=flow
            directory=target/flow;directory.mkdir(exist_ok=True)
            for name in ('draft.json','gates.json','request-plan.json','notification.json','insights.csv','preview.html','subtitles.srt','short.mp4'):
                path=Path(run['output'])/name
                if path.is_file():shutil.copyfile(path,directory/name)
            if flow=='insta':
                shutil.copytree(Path(run['output'])/'cards',directory/'cards',dirs_exist_ok=True)
            save_json(directory/'result.json',{'status':run['status'],'flow':flow,'steps':run['steps'],'mock':True,'network_calls':0,'generation_cost_usd':run['generation_cost']})
        html=(p.store.root/'dashboard.html').read_text()
        for identifier,flow in ids.items():html=html.replace(identifier+'/preview.html',flow+'/preview.html')
        (target/'dashboard.html').write_text(html)
    total=sum(f.stat().st_size for f in target.rglob('*') if f.is_file())
    if total>10000000:raise ValueError('samples가 10MB를 넘었습니다.')
    print(f'mock 샘플 생성 완료 · {total:,} bytes · 외부 호출 0')

if __name__=='__main__':main()
