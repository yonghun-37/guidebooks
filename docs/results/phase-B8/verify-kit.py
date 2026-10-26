"""Python 3.11로 깨끗한 원본·ZIP의 pytest 및 README 드라이런 검증."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/results/phase-B8'
assert sys.version_info[:2] == (3, 11), sys.version
work = Path(tempfile.mkdtemp(prefix='blogbook-b8-'))
source = work / 'source/blog-kit'
shutil.copytree(ROOT / 'blog-kit', source, ignore=shutil.ignore_patterns(
    '.venv', '__pycache__', '.pytest_cache', 'output', '.env', 'config.json', 'APPROVED.json'))
archive = ROOT / 'site-blog/samples/blog-kit/blog-kit.zip'
with zipfile.ZipFile(archive) as z:
    z.extractall(work / 'zip')
    zipnames = z.namelist()
forbidden = [n for n in zipnames if any(x in Path(n).parts for x in ('.env', '.venv', '__pycache__', 'APPROVED.json', 'auth'))]
assert not forbidden, forbidden
# 공개 ZIP의 각 파일을 원본과 바이트 비교한다.
for name in zipnames:
    original = ROOT / name
    assert original.is_file(), name
    assert original.read_bytes() == (work / 'zip' / name).read_bytes(), name
runs = []
for label, kit in [('original', source), ('zip', work / 'zip/blog-kit')]:
    def run(args, expected=0):
        proc = subprocess.run([sys.executable, *args], cwd=kit, text=True, capture_output=True)
        runs.append(dict(copy=label, command='python ' + ' '.join(args), exit=proc.returncode,
                         stdout=proc.stdout, stderr=proc.stderr))
        assert proc.returncode == expected, runs[-1]
        return proc.stdout
    test = run(['-m', 'pytest', '-ra'])
    (OUT / f'{label}-pytest.txt').write_text(sys.version + '\n' + test)
    run(['brief.py', '--keyword', '2025 청년내일저축계좌 대상 신청 기간', '--type', '정보',
         '--platform', 'naver', '--notes', 'samples/info-notes.txt', '--output', 'output/practice/brief.md'])
    checked = run(['check.py', 'samples/article.md', '--output', 'output/practice/report.md', '--strict'])
    assert '확인할 항목: 0개' in checked and '27자 / 본문: 1798자' in checked
    run(['render.py', 'samples/article.md', '--output', 'output/practice/article'])
    run(['review.py', 'output/practice/article', '--approve'], expected=1)
    review = kit / 'output/practice/article/REVIEW.md'
    review.write_text(review.read_text().replace('- [ ]', '- [x]'))
    run(['review.py', 'output/practice/article', '--approve'])
    for platform in ['blogger', 'wordpress', 'naver', 'tistory']:
        result = run(['publish.py', 'output/practice/article', '--platform', platform])
        assert 'dry-run' in result if platform in ['blogger', 'wordpress'] else '편집기에 붙여 넣기' in result
    # 입력 메모 파일이 ZIP에도 있고 후기/여행 경로가 동일하게 보존된다.
    for stem in ['info', 'review', 'trip']:
        assert (kit / f'samples/{stem}-notes.txt').read_text()
    run(['daily.py', '--date', '2026-10-26'])
    run(['daily.py', '--date', '2026-10-26'], expected=1)
    for osname in ['windows', 'macos', 'linux']:
        assert '안내만 생성' in run(['schedule_setup.py', '--os', osname, '--time', '20:30'])
(OUT / 'kit-check.json').write_text(json.dumps(dict(
    python=sys.version, zip_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
    zip_files=len(zipnames), byte_matches=len(zipnames), forbidden=forbidden, runs=runs), ensure_ascii=False, indent=2))
print(json.dumps(dict(python=sys.version.split()[0], zip_files=len(zipnames), runs=len(runs), copies=2), ensure_ascii=False))
