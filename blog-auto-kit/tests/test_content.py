"""콘텐츠 생성과 스키마의 기본 동작을 검증한다."""
import unittest
from content.samples import load_sample, with_human_notes
from content.markdown import render
from content.schema import validate
from content.topics import build_topics

class ContentTests(unittest.TestCase):
    def test_samples_are_valid_and_notes_are_explicit(self):
        for name in ('info', 'play', 'affiliate', 'sponsor'):
            doc = load_sample(name)
            self.assertEqual(validate(doc), [])
            self.assertEqual(doc['experience'], '')
        self.assertEqual(with_human_notes(load_sample('sponsor'))['experience_by'], 'human')

    def test_markdown_escapes_html(self):
        self.assertNotIn('<script>', render('<script>alert(1)</script>'))

    def test_topics_are_deterministic(self):
        self.assertEqual(build_topics('2026-10-27')['as_of'], '2026-10-27')

    def test_nested_data_and_nonempty_fields_are_validated(self):
        doc = load_sample('info'); doc['source_notes'][0]['official'] = 'yes'
        self.assertTrue(validate(doc))
        doc = load_sample('info'); doc['title'] = ''
        self.assertTrue(validate(doc))
        doc = load_sample('sponsor'); doc['media'][0]['child_photo'] = 'false'
        self.assertTrue(validate(doc))
