"""배포 HTML이 공통 응급 데이터에서 어긋나거나 빠지면 게이트 실패."""
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('baby_emergency', ROOT / 'scripts/build_baby_emergency.py')
baby = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baby)


class BabyEmergencyTests(unittest.TestCase):
    def test_every_deployed_host_matches_source(self):
        self.assertEqual(baby.build(check=True), [])
        rows = baby.data()
        briefing = (ROOT / 'research-baby/BRIEFING.md').read_text().split('## ④')[1].split('## ⑤')[0]
        for row in rows:
            self.assertIn('**' + row['text'] + '**', briefing)
        for name in ['chapters/07-hospital.html', 'practice/06-emergency.html', 'print/emergency.html']:
            source = (baby.SITE / name).read_text()
            for row in rows:
                self.assertIn(f'data-emergency-id="{row["id"]}"', source)
                self.assertIn(row['text'], source)
            self.assertIn(baby.FEVER_NOTE, source)
            self.assertIn(baby.ASK, source)

    def test_html_drift_and_missing_message_fail_without_overwriting(self):
        for transform in [lambda s: s.replace('38.0℃', '39.0℃'), lambda s: re.sub(r'<p class="emergency-message".*?</p>', '', s, count=1)]:
            with self.subTest(transform=transform), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                site = root / 'site-baby'
                (site / 'assets').mkdir(parents=True)
                (site / 'assets/emergency-data.js').write_text((baby.SITE / 'assets/emergency-data.js').read_text())
                page = site / 'emergency.html'
                with patch.object(baby, 'ROOT', root), patch.object(baby, 'SITE', site):
                    page.write_text('<div data-emergency="" data-emergency-full></div>')
                    baby.build()
                    changed = transform(page.read_text())
                    page.write_text(changed)
                    self.assertEqual(baby.build(check=True), ['site-baby/emergency.html'])
                    self.assertEqual(page.read_text(), changed)
                    baby.build()
                    self.assertEqual(baby.build(check=True), [])

    def test_data_edit_requires_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / 'site-baby'
            (site / 'assets').mkdir(parents=True)
            data = site / 'assets/emergency-data.js'
            data.write_text((baby.SITE / 'assets/emergency-data.js').read_text())
            with patch.object(baby, 'ROOT', root), patch.object(baby, 'SITE', site):
                (site / 'emergency.html').write_text('<div data-emergency="" data-emergency-full></div>')
                baby.build()
                data.write_text(data.read_text().replace('38.0℃', '39.0℃'))
                self.assertTrue(baby.build(check=True))

    def test_direct_care_pages_include_full_box(self):
        pages = ['chapters/02-feeding', 'chapters/03-sleep', 'chapters/04-crying', 'chapters/05-diapers', 'chapters/06-body', 'chapters/08-growth', 'practice/02-diaper', 'practice/03-feeding', 'practice/04-sleep', 'practice/05-bath', 'practice/06-emergency', 'practice/09-records', 'practice/10-play']
        for page in pages:
            self.assertIn('data-emergency-full', (baby.SITE / (page+'.html')).read_text(), page)
