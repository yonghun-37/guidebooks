"""설정 오류와 결정적 파일·백업 복구를 검사한다."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.config import load_config
from core.files import write_json
from core.state import Store
from ops.backup import backup, restore


class OperationsTests(unittest.TestCase):
    def test_backup_restores_database_and_media(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            store = Store(root)
            store.put('posts', 'one', {'state': 'draft'})
            write_json(root / 'private/mock-wp/state.json', {'posts': [{'id': 1}]})
            (root / 'config.example.toml').write_text('[clock]\ntoday="2026-10-27"\n')
            path = backup(root)
            original = path.read_bytes()
            self.assertEqual(backup(root).read_bytes(), original)
            store.put('posts', 'one', {'state': 'broken'})
            restore(root, path)
            self.assertEqual(store.get('posts', 'one')['state'], 'draft')
            self.assertEqual((root / 'private/mock-wp/state.json').read_text(),
                             '{\n  "posts": [\n    {\n      "id": 1\n    }\n  ]\n}\n')

    def test_configuration_reports_line_and_fix(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / 'bad.toml'
            path.write_text('[wordpress]\nurl=17\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, '2줄.*url.*고치'):
                load_config(path)


if __name__ == '__main__':
    unittest.main()
