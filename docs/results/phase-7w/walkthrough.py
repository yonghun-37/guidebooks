#!/usr/bin/env python3
"""깨끗한 임시 키트: README 설치와 실습 2~6의 실제 CLI·출력 대조.
실제 채팅/게시/계정 접속 없음. 검수 체크 처리는 검증용 fixture에만 한다.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[3]
DEST=Path(__file__).resolve().parent
PYTHON=os.environ.get('WALKTHROUGH_PYTHON',str((ROOT/'starter-kit/.venv/bin/python').resolve()))
results=[]
with tempfile.TemporaryDirectory(prefix='ai-insta-7w-clean-') as temp:
    kit=Path(temp)/'starter-kit'
    shutil.copytree(ROOT/'starter-kit',kit,ignore=shutil.ignore_patterns('.venv','.cache','.pytest_cache','__pycache__','output','hosting','.env','config.yaml'))
    env=os.environ.copy()
    for name in ('IG_ACCESS_TOKEN','IG_USER_ID','IG_API_VERSION','LLM_BASE_URL','LLM_API_KEY','LLM_MODEL'):
        env.pop(name,None)
    def run(args,expected=None):
        process=subprocess.run(args,cwd=kit,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
        results.append(dict(command=' '.join(str(a) for a in args).replace(str(kit),'<KIT>'),returncode=process.returncode,output=process.stdout.replace(str(kit),'<KIT>'),expected=expected))
        assert process.returncode==0,process.stdout
        if expected:
            assert expected in process.stdout,(expected,process.stdout)
    run([PYTHON,'-m','venv','.venv'])
    python=kit/'.venv/bin/python'
    run([str(python),'-m','pip','install','--cache-dir','.cache/pip','-r','requirements.txt'])
    # 설치 뒤 CLI의 네트워크를 통째로 차단한다. 외부 API 성공을 흉내 내지 않는다.
    block=Path(temp)/'network-block';block.mkdir()
    (block/'sitecustomize.py').write_text('import socket\ndef blocked(*a,**k):\n raise AssertionError("walkthrough external network blocked")\nsocket.socket.connect=blocked\nsocket.create_connection=blocked\n')
    env['PYTHONPATH']=str(block)
    run([str(python),'--version'],'Python 3.11')
    run([str(python),'run_pipeline.py','--offline','--output','output/first-post'],'검수 대기:')
    output=kit/'output/first-post'
    assert (output/'REVIEW.md').exists() and not (output/'APPROVED.json').exists()
    assert len(list((output/'cards').glob('*.jpg')))==5
    original=(output/'copy.json').read_bytes()
    run([str(python),'write_copy.py','output/first-post/news.json','--mode','prompt','--template','cards','--output','output/first-post/copy.json'],'웹 채팅에 붙여 넣을 프롬프트:')
    assert (output/'prompt.md').exists() and (output/'copy.json').read_bytes()==original
    # 채팅을 호출하지 않고 오프라인 초안을 직접 편집하는 허용 경로를 실행한다.
    copy=json.loads(original)
    copy['scenes'][0]['title']='연습 소재를 내 말로 확인하기'
    (output/'copy.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2)+'\n')
    run([str(python),'write_copy.py','output/first-post/news.json','--validate','--output','output/first-post/copy.json'],'구조 검증 OK: output/first-post/copy.json (사실 확인은 사람이 해야 합니다)')
    for _ in range(2):
        run([str(python),'run_pipeline.py','render','output/first-post'],'검수 대기:')
        assert not (output/'APPROVED.json').exists()
    # 검증 fixture에만 체크한다. 독자 안내에 자동 검수 명령을 제공하지 않는다.
    review=output/'REVIEW.md'
    review.write_text(review.read_text().replace('- [ ]','- [x]'))
    run([str(python),'run_pipeline.py','approve','output/first-post'],'"mode": "dry-run"')
    assert (output/'APPROVED.json').exists()
    run([str(python),'publish.py','output/first-post'],'"mode": "dry-run"')
    run([str(python),'prepare_hosting.py','output/first-post','--dest','hosting/first-post'],'공개 준비 완료: 6개 JPEG/MP4')
    assert sorted(p.suffix for p in (kit/'hosting/first-post').rglob('*') if p.is_file())==['.jpg']*5+['.mp4']
    # 본인 로컬 RSS 경로의 계약도 실제 시험. 내용은 검증용 가상자료이며 공개하지 않는다.
    (kit/'my-feed.xml').write_text('<rss version="2.0"><channel><title>검증 fixture</title><item><title>검증용 예제</title><link>https://example.org/test-only</link><description>실제 뉴스가 아닌 로컬 형식 시험</description><pubDate>2026-10-26</pubDate></item></channel></rss>')
    run([str(python),'run_pipeline.py','--offline','--feed','my-feed.xml','--output','output/my-news'],'검수 대기:')
    actual=json.loads((kit/'output/my-news/news.json').read_text())
    assert actual['synthetic'] is False and actual['articles'][0]['link']=='https://example.org/test-only'
    results.append(dict(check='출력·해시',copy_sha256=hashlib.sha256((output/'copy.json').read_bytes()).hexdigest(),cards=5,mp4_bytes=(output/'reel.mp4').stat().st_size,network_after_install='blocked'))
(DEST/'walkthrough-check.json').write_text(json.dumps(dict(environment='Linux / clean venv / Python 3.11; Windows/macOS 미실행',checks=results),ensure_ascii=False,indent=2)+'\n')
print(f'clean walkthrough: {len(results)} records passed')
