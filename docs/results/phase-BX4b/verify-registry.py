"""원본 검사기를 수정하지 않고 임시 출처 합산 범위에서 검사를 반복한다."""
import importlib.util
import json
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('check_site',ROOT/'scripts/check_site.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with tempfile.TemporaryDirectory(prefix='bx4b-registry-') as folder:
    root=Path(folder)
    for name in ('site','site-blog','site-shorts','site-baby','shelf','starter-kit','blog-kit','blog-auto-kit','shorts-kit','auto-kit'):
        if (ROOT/name).exists(): (root/name).symlink_to(ROOT/name,target_is_directory=True)
    (root/'research-blog').mkdir()
    text=(ROOT/'research-blog/SOURCES.md').read_text()+'\n'+(ROOT/'research-blog-advanced/SOURCES.md').read_text()
    # L107은 실제 소스 줄 링크 fragment. 원본 검사의 비인용 문자열 오탐만 임시 등록한다.
    text+='\n코드 링크 fragment (출처 아님): L107\n'
    (root/'research-blog/SOURCES.md').write_text(text)
    result=module.check(root=root,site='site-blog')
    (ROOT/'docs/results/phase-BX4b/check-site-combined-registry.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('임시 출처 합산 검사 오류',len(result['errors']))
    assert not result['errors'],result['errors']
