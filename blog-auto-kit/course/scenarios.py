"""서로 독립된 임시 키트에서 운영 시나리오를 실행한다."""
import json
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

KIT_ROOT = Path(__file__).resolve().parents[1]
if str(KIT_ROOT) not in sys.path:
    sys.path.insert(0, str(KIT_ROOT))
from core.state import Store
from course import scenario_cases as cases

NAMES = ('mock_normal', 'regulated_refusal', 'missing_data', 'reapproval', 'timeout_no_duplicate', 'backup_restore', 'bypass_attempts')


def run_scenarios(kit_root: Path) -> dict:
    """각 시나리오를 별도 복사본에서 실행하고 결과를 저장한다."""
    kit_root = Path(kit_root)
    result = {}
    for name in NAMES:
        with TemporaryDirectory(prefix='blog-scenario-') as folder:
            root = Path(folder)
            shutil.copytree(kit_root / 'samples', root / 'samples')
            shutil.copyfile(kit_root / 'config.example.toml', root / 'config.example.toml')
            evidence = getattr(cases, name)(root, Store(root))
            result[name] = {'passed': True, 'evidence': evidence}
    path = kit_root / 'output/scenarios.json'; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return result


def main():
    """일곱 결과를 화면에 표시한다."""
    for name, row in run_scenarios(KIT_ROOT).items():
        print(f"✔ 통과: {name} — {row['evidence']}")


if __name__ == '__main__':
    main()
