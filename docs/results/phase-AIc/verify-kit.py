"""AIc에 보존한 명령을 임시 키트에서 실행. 첫 인자는 새 키트 복사본 경로."""
from pathlib import Path
import subprocess,json,os,html,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[3]
KIT=Path(sys.argv[1]).resolve()
PYTHON=KIT/'.venv/bin/python'
ENV={k:os.environ[k] for k in ['HOME','PATH','LANG'] if k in os.environ}
ENV['PATH']=str(PYTHON.parent)+os.pathsep+ENV.get('PATH','')
results=[]
def run(args,expect=None):
 r=subprocess.run(args,cwd=KIT,env=ENV,text=True,capture_output=True)
 results.append({'command':' '.join(str(a) for a in args),'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 assert r.returncode==0,results[-1]
 if expect:assert expect in r.stdout,results[-1]
 return r

def main():
 for slug in ['03-copy','04-cards','05-reel']:
  old=subprocess.check_output(['git','show','HEAD:site/practice/'+slug+'.html'],cwd=ROOT,text=True)
  new=(ROOT/'site/practice'/f'{slug}.html').read_text()
  commands=[html.unescape(x) for x in re.findall(r'<pre><code>(.*?)</code></pre>',old,re.S) if 'python' in x]
  assert all(c in html.unescape(new) for c in commands),slug
  results.append({'page':slug,'original_command_blocks_preserved':len(commands)})
 run(['python','--version'])
 run(['python','run_pipeline.py','--offline','--output','output/first-post'],'검수 대기:')
 copy=KIT/'output/first-post/copy.json';before=hashlib.sha256(copy.read_bytes()).hexdigest()
 run(['python','write_copy.py','output/first-post/news.json','--mode','prompt','--template','cards','--output','output/first-post/copy.json'],'웹 채팅에 붙여 넣을 프롬프트:')
 assert hashlib.sha256(copy.read_bytes()).hexdigest()==before
 run(['python','write_copy.py','output/first-post/news.json','--validate','--output','output/first-post/copy.json'],'구조 검증 OK: output/first-post/copy.json')
 run(['python','run_pipeline.py','render','output/first-post'],'검수 대기:')
 # Fictional fixture tests the command syntax only; never posted as news.
 (KIT/'my-feed.xml').write_text('''<rss version="2.0"><channel><title>가상 검증 자료</title><item><title>가상 은솔 자료</title><link>https://example.invalid/aic-fixture</link><description>명령 검증용 가상 자료이며 실제 뉴스가 아닙니다.</description><pubDate>2026-10-26</pubDate></item></channel></rss>''')
 (KIT/'config.yaml').write_text((KIT/'config.example.yaml').read_text())
 run(['python','-c',"import yaml;from pathlib import Path;p=Path('config.yaml');c=yaml.safe_load(p.read_text());c['account_name']='AIc 가상 검증 계정';p.write_text(yaml.safe_dump(c,allow_unicode=True))"])
 run(['python','run_pipeline.py','--offline','--config','config.yaml','--feed','my-feed.xml','--output','output/my-news'],'검수 대기:')
 run(['python','write_copy.py','output/my-news/news.json','--mode','prompt','--template','cards','--output','output/my-news/copy.json','--config','config.yaml'],'웹 채팅에 붙여 넣을 프롬프트:')
 assert 'AIc 가상 검증 계정' in (KIT/'output/my-news/prompt.md').read_text()
 run(['python','write_copy.py','output/my-news/news.json','--validate','--output','output/my-news/copy.json'],'구조 검증 OK:')
 run(['python','run_pipeline.py','render','output/my-news'],'검수 대기:')
 run(['python','-c',"from PIL import Image;from pathlib import Path;import json; p=Path('output/first-post');assert len(list((p/'cards').glob('*.png')))==5;assert len(list((p/'cards').glob('*.jpg')))==5;assert all(Image.open(f).size==(1080,1350) for f in (p/'cards').glob('*.png'));q=Path('output/my-news');assert len(list((q/'cards').glob('*.png')))==3;assert json.loads((q/'copy.json').read_text())['account_name']=='AIc 가상 검증 계정';print('카드 수·치수·계정 이름 OK')"])
 # Non-personal tone fixture; verify the exact m4a conversion, not speech quality.
 run(['python','-c',"import imageio_ffmpeg,subprocess; subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-f','lavfi','-i','sine=frequency=440:duration=0.5','-c:a','aac','my-voice.m4a'],check=True)"])
 run(['python','-c',"import imageio_ffmpeg,subprocess; subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-i','my-voice.m4a','-vn','-c:a','pcm_s16le','my-voice.wav'],check=True)"])
 run(['python','-c',"import json;from pathlib import Path;p=Path('output/first-post/config.json');c=json.loads(p.read_text());c['reel']['narration']=str(Path('my-voice.wav').resolve());c['reel']['music']=None;c['reel']['tts']='silent';p.write_text(json.dumps(c,ensure_ascii=False))"])
 run(['python','run_pipeline.py','render','output/first-post'],'검수 대기:')
 run(['python','-c',"import imageio_ffmpeg,subprocess; r=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-i','output/first-post/reel.mp4','-f','null','-'],capture_output=True,text=True);assert r.returncode==0;assert '1080x1920' in r.stderr;assert 'Audio:' in r.stderr;print('MP4 1080x1920·오디오 스트림·끝까지 디코딩 OK')"])

try:main()
finally:
 (ROOT/'docs/results/phase-AIc/kit-check.json').write_text(json.dumps({'temporary_kit':str(KIT),'dependency_setup':'Python 3.11.15 신규 venv에 requirements.txt의 세 고정 버전 pip 설치 성공','platform':'Linux; Windows 명령은 동일 인자를 Linux venv python으로 실행, Windows/macOS 실기기 아님','voice_fixture':'0.5초 사인파, 사람 음성 청취/정렬 검증 아님','results':results},ensure_ascii=False,indent=2))
print('PASS',len(results))
