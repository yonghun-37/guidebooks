"""블로그 부록 재생성이 원본·인용·공개 키트 파일만 재사용하는지 확인한다."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import build_appendices_blog as builder
from build_appendices import Document, nodes, text


class BlogAppendicesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.tmp.name)
        cls.site=cls.root/'site-blog'
        for directory in ['site-blog','blog-kit','research-blog']:
            shutil.copytree(builder.ROOT/directory,cls.root/directory,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache','.venv'))
        (cls.root/'docs/results').mkdir(parents=True)
        for name in ['B4a','B4b','B4c','B5']:
            path=Path(f'docs/results/phase-{name}-glossary.md')
            shutil.copyfile(builder.ROOT/path,cls.root/path)
        cls.patcher=patch.multiple(builder,ROOT=cls.root,SITE=cls.site)
        cls.patcher.start()
        builder.build()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()
        cls.tmp.cleanup()

    def test_every_tool_uses_a_distinct_original(self):
        tools=json.loads((self.site/'assets/catalog.js').read_text().split('Object.freeze(',1)[1].rsplit(');',1)[0])
        self.assertEqual([t['chapter'] for t in tools],list(range(1,14)))
        for tool in tools:
            doc=Document((self.site/f'chapters/{tool["slug"]}.html').read_text()).root
            self.assertEqual(len([n for n in nodes(doc) if n.attrs.get('id')==tool['id']]),1)
        lab=(self.site/'lab.html').read_text()
        self.assertNotIn('id="revenue-tool"',lab)
        self.assertIn('<iframe',lab)

    def test_prompts_match_their_source(self):
        doc=Document((self.site/'prompts.html').read_text()).root
        boxes=[n for n in nodes(doc) if 'data-prompt-origin' in n.attrs]
        self.assertEqual(len(boxes),18)
        for box in boxes:
            filename,id_=box.attrs['data-prompt-origin'].split('#')
            original=Document((self.site/filename).read_text()).root
            section=next(n for n in nodes(original) if n.attrs.get('id')==id_)
            index=int(box.attrs.get('data-prompt-index','0'))
            if section.tag=='pre': expected=text(section)
            else:
                pres=[n for n in nodes(section) if n.tag=='pre']
                expected=text(pres[index]) if pres else text(next(n for n in nodes(section) if n.tag=='code'))
            self.assertEqual(text(next(n for n in nodes(box) if n.tag=='code')),expected)

    def test_glossary_has_distinct_tokens_and_merged_terms(self):
        doc=Document((self.site/'glossary.html').read_text()).root
        ids=[n.attrs['id'] for n in nodes(doc) if 'data-glossary-entry' in n.attrs]
        self.assertEqual(len(ids),68)
        self.assertEqual(len(ids),len(set(ids)))
        self.assertIn('token',ids)
        self.assertIn('ai-token',ids)
        self.assertIn('mock',ids)
        self.assertIn('assert',ids)
        self.assertIn('id="advanced-tools"', (self.site/'lab.html').read_text())
        self.assertIn('id="advanced-sources"', (self.site/'credits.html').read_text())
        for path in self.site.rglob('*.html'):
            for node in nodes(Document(path.read_text()).root):
                if 'data-term' in node.attrs:
                    self.assertIn(node.attrs['data-term'],ids)
                    self.assertTrue(node.attrs['href'].endswith('#'+node.attrs['data-term']))

    def test_credits_only_collect_actual_footnote_links(self):
        cited=set()
        for directory in ['chapters','practice']:
            for path in (self.site/directory).glob('[0-9]*.html'):
                cited.update(re.findall(r'href="#source-(b\d{3})"',path.read_text()))
        for name in ['prompts','ai-models']:
            cited.update(re.findall(r'href="#source-(b\d{3})"',(self.site/f'{name}.html').read_text()))
        listed=set(re.findall(r'id="source-(b\d{3})"',(self.site/'credits.html').read_text()))
        self.assertEqual(cited,listed)

    def test_rebuild_is_identical_and_zip_contains_exact_public_source(self):
        def snapshot():
            return {p.relative_to(self.site).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in self.site.rglob('*') if p.is_file()}
        before=snapshot()
        builder.build()
        self.assertEqual(before,snapshot())
        with zipfile.ZipFile(self.site/'samples/blog-kit/blog-kit.zip') as archive:
            self.assertIn('blog-kit/README.md',archive.namelist())
            self.assertIn('blog-kit/.env.example',archive.namelist())
            for name in archive.namelist():
                self.assertNotIn('/auth/',name)
                self.assertNotIn('/.env',name.replace('/.env.example','/example'))
                self.assertNotIn('__pycache__',name)
                self.assertEqual(archive.read(name),(self.root/name).read_bytes())
