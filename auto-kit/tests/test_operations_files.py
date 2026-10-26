from pathlib import Path
import plistlib
import pytest
from common import load_config
from doctor import diagnose
from schedule.install import generate
from hosting import host
import doctor

@pytest.mark.parametrize('version', [(3, 10, 12), (3, 11, 15), (3, 12, 0)])
def test_doctor_python_minimum(monkeypatch, version):
    monkeypatch.setattr(doctor.sys, 'version_info', version)
    results = diagnose(load_config(), values={})
    assert results[0]['level'] == ('error' if version < (3, 11) else 'ok')
    assert '3.11' in results[0]['message']
    if version < (3, 11):
        assert len(results) == 1
        assert 'mock 준비 완료' not in str(results)

def test_doctor_mock_and_live_missing():
    cfg=load_config()
    results=diagnose(cfg, values={}, live=False)
    assert not [r for r in results if r['level']=='error']
    results=diagnose(cfg, values={}, live=True)
    assert any('공급자' in r['message'] for r in results)
    assert any('상한' in r['message'] for r in results)

@pytest.mark.parametrize('os_name',['windows','macos','cron'])
def test_schedule_files_use_absolute_python_and_mock(tmp_path,os_name):
    result=generate(os_name,'09:17','insta',tmp_path,python='/usr/bin/python3')
    text=Path(result['path']).read_text()
    assert 'tick' in text
    assert 'secret' not in text
    if os_name=='macos':
        plist=plistlib.loads(Path(result['path']).read_bytes())
        assert plist['ProgramArguments'][0]=='/usr/bin/python3'
    assert '--live' not in text

def test_hosting_only_media_and_max_bytes(tmp_path):
    cfg=load_config()
    private=tmp_path/'token.json'; private.write_text('secret')
    with pytest.raises(ValueError): host([private],cfg,'r',tmp_path)
    media=tmp_path/'a.jpg';media.write_bytes(b'x'*10)
    cfg['hosting']['max_bytes_per_run']=9
    with pytest.raises(ValueError): host([media],cfg,'r',tmp_path)
