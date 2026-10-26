import os, subprocess, json, hashlib, tempfile, shutil, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
TEMP=tempfile.TemporaryDirectory(prefix='ai-insta-9d-clean-')
KIT=Path(TEMP.name)/'starter-kit'
shutil.copytree(ROOT/'starter-kit',KIT,ignore=shutil.ignore_patterns('.venv','.cache','__pycache__','output','hosting','.env'))
subprocess.run([sys.executable,'-m','venv',str(KIT/'.venv')],check=True)
PY=KIT/'.venv/bin/python'
subprocess.run([str(PY),'-m','pip','install','--cache-dir','/tmp/phase9d-pip-cache','-r','requirements.txt'],cwd=KIT,check=True)
OUT=ROOT/'docs/results/phase-9d';records=[]
block=KIT.parent/'network-block';block.mkdir(exist_ok=True)
(block/'sitecustomize.py').write_text('import socket\ndef blocked(*a,**k):\n raise AssertionError("external network blocked")\nsocket.socket.connect=blocked\nsocket.create_connection=blocked\n')
env=os.environ.copy()
for k in ('IG_ACCESS_TOKEN','IG_USER_ID','IG_API_VERSION','LLM_API_KEY','LLM_BASE_URL','LLM_MODEL'):env.pop(k,None)
env['PYTHONPATH']=str(block)
def run(args,expected=None,ok=0):
 p=subprocess.run([str(x) for x in args],cwd=KIT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
 records.append(dict(command=' '.join(str(x) for x in args).replace(str(KIT),'<KIT>'),returncode=p.returncode,output=p.stdout.replace(str(KIT),'<KIT>'),expected=expected))
 (OUT/'walkthrough.json').write_text(json.dumps({'environment':'Linux / Python 3.11 / clean venv; network blocked after pip install','commands':records},ensure_ascii=False,indent=2)+'\n')
 assert p.returncode==ok,p.stdout
 if expected:assert expected in p.stdout,p.stdout
run([PY,'--version'],'Python 3.11')
run([PY,'run_pipeline.py','--offline','--output','output/first-post'],'검수 대기:')
out=KIT/'output/first-post'
assert len(list((out/'cards').glob('*.jpg')))==5 and not (out/'APPROVED.json').exists()
original=(out/'copy.json').read_bytes()
run([PY,'write_copy.py','output/first-post/news.json','--mode','prompt','--template','cards','--output','output/first-post/copy.json'],'웹 채팅에 붙여 넣을 프롬프트:')
assert (out/'copy.json').read_bytes()==original
copy=json.loads(original);copy['scenes'][0]['title']='확인한 내용으로 제목을 고쳐요'
(out/'copy.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2)+'\n')
run([PY,'write_copy.py','output/first-post/news.json','--validate','--output','output/first-post/copy.json'],'구조 검증 OK: output/first-post/copy.json (사실 확인은 사람이 해야 합니다)')
run([PY,'run_pipeline.py','render','output/first-post'],'검수 대기:')
# 선택 녹음 경로의 실행만 확인하는 합성 테스트 톤. 사람 목소리로 표현하지 않는다.
import wave,math,struct
tone=KIT/'test-tone.wav'
with wave.open(str(tone),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000)
 w.writeframes(b''.join(struct.pack('<h',int(1500*math.sin(2*math.pi*440*n/16000))) for n in range(16000*20)))
config=json.loads((out/'config.json').read_text());config['reel']['narration']=str(tone)
(out/'config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2))
run([PY,'run_pipeline.py','render','output/first-post'],'검수 대기:')
import imageio_ffmpeg
ff=imageio_ffmpeg.get_ffmpeg_exe()
media=subprocess.run([ff,'-i',str(out/'reel.mp4'),'-f','null','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
assert media.returncode==0 and 'Audio:' in media.stderr and '1080x1920' in media.stderr,media.stderr[-2000:]
(OUT/'media-check.json').write_text(json.dumps({'cards':5,'card_size':[1080,1350],'video_size':[1080,1920],'duration_seconds':20,'audio_test':'synthetic 440Hz WAV input; audio stream and full decoding checked; human voice quality not tested','ffmpeg_decode_exit':media.returncode},ensure_ascii=False,indent=2)+'\n')
# 웹/계정 게시 없이 합성 fixture의 검수·승인만 시험한다.
r=out/'REVIEW.md';assert r.read_text().count('- [ ]')==6
r.write_text(r.read_text().replace('- [ ]','- [x]'))
run([PY,'run_pipeline.py','approve','output/first-post'],'"mode": "dry-run"')
run([PY,'publish.py','output/first-post'],'"mode": "dry-run"')
run([PY,'prepare_hosting.py','output/first-post','--dest','hosting/first-post'],'공개 준비 완료: 6개 JPEG/MP4')
assert sorted(p.suffix for p in (KIT/'hosting/first-post').rglob('*') if p.is_file())==['.jpg']*5+['.mp4']
run([PY,'publish.py','output/first-post','--base-url','https://example.org/phase9d-fixture'],'"mode": "dry-run"')
(KIT/'my-feed.xml').write_text('<rss version="2.0"><channel><title>검증 전용 가상 자료</title><item><title>새 피드 형식 연습</title><link>https://example.org/test-only</link><description>실제 뉴스가 아닌 검증 fixture</description><pubDate>2026-10-26</pubDate></item></channel></rss>')
run([PY,'run_pipeline.py','--offline','--feed','my-feed.xml','--output','output/my-news'],'검수 대기:')
# 승인 뒤 파일을 고치면 게시를 거부해야 한다.
copy['scenes'][0]['title']='승인 후 변경 fixture'
(out/'copy.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2))
result=subprocess.run([str(PY),'publish.py','output/first-post'],cwd=KIT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
assert result.returncode!=0,result.stdout
records.append({'check':'approved file mutation rejected','returncode':result.returncode,'output':result.stdout.replace(str(KIT),'<KIT>')})
(OUT/'walkthrough.json').write_text(json.dumps({'environment':'Linux / Python 3.11.15 / clean venv; network blocked after successful requirements install','commands':records,'unexecuted':['Windows/macOS installer and OS shells','web chat','real account API calls and --live','hosting upload','token issuance/refresh']},ensure_ascii=False,indent=2)+'\n')
print(f'{len(records)} walkthrough records passed')
TEMP.cleanup()
