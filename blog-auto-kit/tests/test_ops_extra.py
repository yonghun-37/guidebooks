"""결정적 백업, 안전한 복구와 알림을 검증한다."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from core.state import Store
from ops.backup import backup, restore
from ops.notifications import notify
from ops.scheduler import generate_schedule

class OpsExtraTests(unittest.TestCase):
    def test_backup_is_deterministic_and_excludes_secrets(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); Store(root).put('posts', 'a', {'value': 1})
            (root / 'config.example.toml').write_text('x = 1\n')
            (root / '.env').write_text('SECRET=do-not-copy')
            archive = backup(root); first = archive.read_bytes()
            self.assertEqual(first, backup(root).read_bytes())
            with zipfile.ZipFile(archive) as z:
                self.assertIn('state.sql', z.namelist())
                self.assertFalse(any('.env' in name for name in z.namelist()))
                self.assertNotIn(b'do-not-copy', b''.join(z.read(n) for n in z.namelist()))

    def test_invalid_zip_preserves_existing_state(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); store = Store(root); store.put('posts', 'a', {'value': 1})
            (root / 'config.example.toml').write_text('x=1')
            bad = root / 'bad.zip'
            with zipfile.ZipFile(bad, 'w') as z:
                z.writestr('../escape', 'bad'); z.writestr('state.sql', 'broken')
            with self.assertRaises(ValueError): restore(root, bad)
            self.assertEqual(store.get('posts', 'a'), {'value': 1})
            self.assertFalse((root.parent / 'escape').exists())

    def test_dry_notification_and_live_validation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); calls = []
            data = notify(root, 'gate_review', '2026-10-27', secrets={'token':'private-value'})
            self.assertFalse(data['live']); self.assertNotIn('private-value', (root / 'output/notifications.json').read_text())
            with self.assertRaises(ValueError):
                notify(root, 'gate_review', '2026-10-27', live=True, transport=calls.append, secrets={'url':'https://evil.example/x'})
            self.assertEqual(calls, [])

    def test_schedules_are_relative_and_not_registered(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); paths = generate_schedule(root)
            self.assertGreaterEqual(len(paths), 3)
            for path in paths:
                self.assertNotIn(d, path.read_text())
                self.assertIn('<KIT>', path.read_text())

    def test_restore_failure_rolls_back_all_files(self):
        from unittest.mock import patch
        import os
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); store = Store(root); store.put('posts', 'a', {'value': 1})
            (root / 'config.example.toml').write_text('x=1')
            archive = backup(root); store.put('posts', 'a', {'value': 2})
            (root / 'config.example.toml').write_text('x=2')
            real_replace = os.replace; calls = []
            def fail_once(src, dest):
                calls.append((src, dest))
                if len(calls) == 3: raise OSError('simulated failure')
                return real_replace(src, dest)
            with patch('ops.backup.os.replace', side_effect=fail_once):
                with self.assertRaises(OSError): restore(root, archive)
            self.assertEqual(store.get('posts', 'a'), {'value': 2})
            self.assertEqual((root / 'config.example.toml').read_text(), 'x=2')

    def test_live_notification_uses_injected_transport_without_storing_url(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); calls = []
            url = 'https://discord.com/api/webhooks/123/private-token'
            data = notify(root, 'review', '2026-10-27', live=True,
                          transport=lambda address, body: calls.append((address, body)), secrets={'url':url})
            self.assertTrue(data['live']); self.assertEqual(calls[0][0], url)
            self.assertNotIn('private-token', (root / 'output/notifications.json').read_text())

    def test_bad_sql_and_missing_config_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); store = Store(root); store.put('posts', 'a', {'value': 1})
            for contents in ({'state.sql':'bad SQL', 'config.example.toml':'x=1'}, {'state.sql':'BEGIN; COMMIT;'}):
                path = root / 'bad.zip'
                with zipfile.ZipFile(path, 'w') as z:
                    for name, value in contents.items(): z.writestr(name, value)
                with self.assertRaises(ValueError): restore(root, path)
                self.assertEqual(store.get('posts', 'a'), {'value': 1})

    def test_secret_directories_are_not_backed_up(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); Store(root); (root / 'config.example.toml').write_text('x=1')
            secret = root / 'private/mock-wp/.env.private'; secret.mkdir(parents=True)
            (secret / 'token').write_text('hidden')
            with zipfile.ZipFile(backup(root)) as z:
                self.assertFalse(any('.env' in item for item in z.namelist()))

    def test_telegram_payload_contains_chat_id_without_saving_it(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); calls = []
            notify(root, 'review', '2026-10-27', live=True,
                   transport=lambda url, body: calls.append(body),
                   secrets={'url':'https://api.telegram.org/botTOKEN/sendMessage', 'chat_id':'private-chat'})
            self.assertEqual(calls[0]['chat_id'], 'private-chat')
            self.assertNotIn('private-chat', (root / 'output/notifications.json').read_text())
