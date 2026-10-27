"""통합된 책의 실제 인용/도구 계약과 재생성 결과를 확인한다."""
import importlib.util
import re
from pathlib import Path
import contextlib
import io
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('baby_appendices',ROOT/'scripts/build_baby_appendices.py')
baby=importlib.util.module_from_spec(spec)
spec.loader.exec_module(baby)

class BabyIntegrationTests(unittest.TestCase):
 def test_credits_are_exactly_the_cited_sources(self):
  text=(baby.SITE/'credits.html').read_text()
  self.assertEqual(set(re.findall(r'id="(n\d{3})"',text)),{s.lower() for s in baby.cited()})
  self.assertTrue(baby.cited() <= baby.sources().keys())
  for sid in baby.cited():
   self.assertIn(baby.markdown(baby.sources()[sid]['적용·한계'].replace('Hermes','보조 조사').replace('Codex','직접 확인')),text)

 def test_no_pending_routes_or_local_source_copies(self):
  for p in baby.SITE.rglob('*.html'):
   self.assertNotEqual(p.name,'pending.html')
   text=p.read_text()
   self.assertNotIn('pending.html',text)
   self.assertNotIn('출처 원문',text)
   if p.name!='credits.html': self.assertNotRegex(text,r'id="n\d{3}"')

 def test_all_tools_are_originals_and_registered_once(self):
  keys=[]
  for number,slug,tid,title,desc,track in baby.TOOLS:
   folder='practice' if track=='practice' else 'chapters'
   source=(baby.SITE/folder/(slug+'.html')).read_text()
   self.assertIn('id="'+tid+'"',source)
   self.assertTrue(desc)
   keys.append((folder,slug,tid))
  self.assertEqual(len(keys),len(set(keys)))

 def test_glossary_covers_requested_candidates(self):
  names={row[1] for row in baby.TERMS}
  self.assertTrue({'혼합수유','유축','조유','영아산통','영아돌연사증후군','태변','이행변','백분위','터미타임','선별검사','6가 혼합백신','바우처','소급','수리','뒤보기','리콜','달력 월령','CSV'} <= names)
  self.assertTrue(30<=len(names)<=45)

 def test_rebuild_is_byte_identical(self):
  with tempfile.TemporaryDirectory() as directory:
   site=Path(directory)/'site-baby'
   shutil.copytree(baby.SITE,site)
   paths=[site/n for n in ['credits.html','glossary.html','lab.html','assets/catalog.js']]
   before={p:p.read_bytes() for p in paths}
   with patch.object(baby,'SITE',site), contextlib.redirect_stdout(io.StringIO()):
    baby.build()
   self.assertEqual(before,{p:p.read_bytes() for p in paths})

if __name__=='__main__':unittest.main()
