import os,json,shutil,subprocess,tempfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
PYTHON=ROOT/'starter-kit/.venv/bin/python'
results=[]
with tempfile.TemporaryDirectory(prefix='phase9b-clean-') as temp:
 kit=Path(temp)/'starter-kit';shutil.copytree(ROOT/'starter-kit',kit,ignore=shutil.ignore_patterns('.venv','.cache','.pytest_cache','__pycache__','output','hosting','.env','config.yaml'))
 block=Path(temp)/'block';block.mkdir();(block/'sitecustomize.py').write_text('import socket\ndef blocked(*a,**k):\n raise AssertionError("network blocked for phase9b check")\nsocket.socket.connect=blocked\nsocket.create_connection=blocked\n')
 env=os.environ.copy();env['PYTHONPATH']=str(block)
 for name in list(env):
  if name.startswith(('IG_','LLM_')):env.pop(name,None)
 def run(args,expected,rc=0):
  proc=subprocess.run([str(PYTHON),*args],cwd=kit,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
  assert proc.returncode==rc,(args,proc.stdout)
  assert expected in proc.stdout,(expected,proc.stdout)
  results.append({'command':'python '+' '.join(args),'exit':proc.returncode,'output':proc.stdout.replace(str(kit),'<KIT>'),'expected':expected})
 run(['run_pipeline.py','--offline','--output','output/first-post'],'검수 대기:')
 out=kit/'output/first-post';original=(out/'copy.json').read_bytes()
 run(['write_copy.py','output/first-post/news.json','--mode','prompt','--template','cards','--output','output/first-post/copy.json'],'웹 채팅에 붙여 넣을 프롬프트:')
 assert original==(out/'copy.json').read_bytes()
 copy=json.loads(original);copy['scenes'][1]['body']='검증용 가상 요점';copy['scenes'][1]['points']=['검증용 가상 요점']
 (out/'copy.json').write_text(json.dumps(copy,ensure_ascii=False))
 run(['write_copy.py','output/first-post/news.json','--validate','--output','output/first-post/copy.json'],'구조 검증 OK:')
 run(['run_pipeline.py','render','output/first-post'],'검수 대기:')
 assert len(list((out/'cards').glob('*.png')))==5
 assert len(list((out/'cards').glob('*.jpg')))==5
 from PIL import Image
 assert Image.open(out/'cards/card-01.png').size==(1080,1350)
 # 동봉 파일 생성·형식 검증만 한다. 실제 사실/권리 승인 대신 검증 fixture만 체크한다.
 review=out/'REVIEW.md';review.write_text(review.read_text().replace('- [ ]','- [x]'))
 run(['run_pipeline.py','approve','output/first-post'],'"mode": "dry-run"')
 assert (out/'APPROVED.json').is_file()
 copy['scenes'][1]['points']=['수정한 검증용 가상 요점'];copy['scenes'][1]['body']='수정한 검증용 가상 요점';(out/'copy.json').write_text(json.dumps(copy,ensure_ascii=False))
 run(['publish.py','output/first-post'],'검수 대상이 바뀌었거나 없습니다',1)
 run(['run_pipeline.py','render','output/first-post'],'검수 대기:')
 assert not (out/'APPROVED.json').exists()
 # 대표 오류 문안 형식을 실제 발생시키고 남아 있는 파일에서 재개한다.
 good=(out/'copy.json').read_text();(out/'copy.json').write_text('{')
 run(['run_pipeline.py','render','output/first-post'],'오류:',1)
 (out/'copy.json').write_text(good)
 run(['run_pipeline.py','render','output/first-post'],'검수 대기:')
 import imageio_ffmpeg
 ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
 probe=subprocess.run([ffmpeg,'-i',str(out/'reel.mp4')],capture_output=True,text=True)
 metadata=probe.stderr
 assert '1080x1920' in metadata and '24 fps' in metadata and '00:00:20.00' in metadata
 silence=subprocess.run([ffmpeg,'-i',str(out/'reel.mp4'),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True)
 assert 'max_volume: -91.0 dB' in silence.stderr or 'max_volume: -inf' in silence.stderr
 assert json.loads((out/'reel-info.json').read_text())['audio']==['silent']
 results.append({'check':'예제 출력과 승인 무효화','cards_png':5,'cards_jpeg':5,'card_size':[1080,1350],'video_size':[1080,1920],'fps':24,'duration':20,'audio':'silent AAC (max_volume -91dB or less)','changed_approval_blocked':True,'render_clears_approval':True,'invalid_json_resume':True,'prompt_preserves_copy':True})
Path(ROOT/'docs/results/phase-9b/walkthrough-check.json').write_text(json.dumps({'environment':'Linux / Python 3.11.15 / 기존 설치 환경 / 깨끗한 키트 복사본 / 네트워크 차단','checks':results},ensure_ascii=False,indent=2)+'\n')
print('walkthrough checks:',len(results))
