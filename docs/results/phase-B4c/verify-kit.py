"""본문 명령을 깨끗한 임시 복사본에서 재현. 인증·전송·예약 등록은 금지한다."""
from pathlib import Path
import json, os, shutil, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[3]
records=[]
with tempfile.TemporaryDirectory(prefix='blog-b4c-') as folder:
    target=Path(folder)/'blog-kit'
    shutil.copytree(ROOT/'blog-kit',target,ignore=shutil.ignore_patterns('.venv','__pycache__','.env','auth','output','config.json','.pytest_cache'))
    # sitecustomize가 복사본의 모든 Python socket 연결을 막는다.
    (target/'sitecustomize.py').write_text("import socket\ndef blocked(*a, **k):\n    raise RuntimeError('B4c 검증은 오프라인입니다')\nsocket.socket.connect=blocked\nsocket.create_connection=blocked\n")
    env=dict(os.environ,PYTHONPATH=str(target))
    def run(*args,expect):
        process=subprocess.run(['python3',*args],cwd=target,env=env,capture_output=True,text=True)
        assert process.returncode==0,(args,process.stderr,process.stdout)
        for text in expect: assert text in process.stdout,(args,text,process.stdout)
        output=process.stdout.replace(str(target),'<TEMP>/blog-kit')
        records.append({'command':'python '+' '.join(args),'expected':expect,'exit':process.returncode,'output':output})
    run('check.py','samples/article.md','--output','output/practice/report.md','--strict',expect=['확인할 항목: 0개','제목: 27자 / 본문: 1369자'])
    run('render.py','samples/article.md','--output','output/practice/article',expect=['HTML 생성 완료:','검수 대기:'])
    run('daily.py','--date','2026-10-26',expect=['작성 대기:'])
    daily=target/'output/daily/2026-10-26'
    shutil.copy(target/'samples/article.md',daily/'draft.md')
    shutil.copy(target/'samples/support-check.svg',daily/'support-check.svg')
    run('daily.py','--date','2026-10-26','--resume',expect=['검수 대기:'])
    # 승인 명령의 입력 조건만 연습 자료에서 모사. 실제 경험·정책 검증의 기록이 아니다.
    review=target/'output/practice/article/REVIEW.md'
    review.write_text(review.read_text().replace('- [ ]','- [x]'))
    run('review.py','output/practice/article','--approve',expect=['사람 승인 기록 완료.'])
    run('publish.py','output/practice/article','--platform','blogger',expect=['"mode": "dry-run"','"state": "draft"','isDraft=true'])
    run('publish.py','output/practice/article','--platform','wordpress',expect=['"status": "draft"'])
    run('publish.py','output/practice/article','--platform','naver',expect=['편집기에 붙여 넣기:'])
    run('publish.py','output/practice/article','--platform','tistory',expect=['편집기에 붙여 넣기:'])
    run('schedule_setup.py','--os','windows','--time','20:30',expect=['안내만 생성했습니다.','BlogBookDaily'])
    run('schedule_setup.py','--os','macos','--time','20:30',expect=['안내만 생성했습니다.','30 20 * * *'])
    assert not (target/'.env').exists()
    assert not list(target.rglob('LIVE_ATTEMPT.json'))
(ROOT/'docs/results/phase-B4c/kit-check.json').write_text(json.dumps({'commands':records,'scope':'Linux 임시 복사본·네트워크 차단·승인은 연습 입력 모사. live·OS 등록 미실행.'},ensure_ascii=False,indent=2))
print(f'본문 키트 명령 {len(records)}개 재현 성공; 네트워크 차단, live·실제 예약 등록 없음')
