"""독립된 로컬 mock 운영 시나리오를 검증한다."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from course.scenarios import run_scenarios


@pytest.fixture(scope='module')
def outcomes(tmp_path_factory):
    root = tmp_path_factory.mktemp('scenario-output')
    import shutil
    shutil.copytree(ROOT / 'samples', root / 'samples')
    shutil.copy(ROOT / 'config.example.toml', root / 'config.example.toml')
    result = run_scenarios(root)
    assert json.loads((root / 'output/scenarios.json').read_text(encoding='utf-8')) == result
    return result


@pytest.mark.parametrize('name', ['mock_normal', 'regulated_refusal', 'missing_data', 'reapproval', 'timeout_no_duplicate', 'backup_restore'])
def test_each_scenario_has_success_and_evidence(outcomes, name):
    assert outcomes[name]['passed'] is True
    assert outcomes[name]['evidence']
