"""AI 부록에서 생성량 토큰과 로그인 토큰을 구분하고 루트 링크를 보존한다."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_appendices as builder


class ReelsAppendicesTests(unittest.TestCase):
    def test_model_token_is_not_attached_to_login_token(self):
        terms = {'토큰': dict(id='token', description='AI가 사용량을 세는 단위.')}
        linker = builder.TermLinks('<main><p>토큰이 있으면 게시합니다.</p></main>', terms,
                                   builder.SITE / 'chapters/09-pipeline.html')
        self.assertEqual(linker.edits, [])
        self.assertNotIn('first', terms['토큰'])

    def test_model_appendix_links_to_root_glossary(self):
        terms = {'토큰': dict(id='token', description='AI가 사용량을 세는 단위.')}
        linker = builder.TermLinks('<main><p>토큰은 글자 수와 다릅니다.</p></main>', terms,
                                   builder.SITE / 'ai-models.html')
        self.assertEqual(len(linker.edits), 1)
        self.assertIn('href="glossary.html#token"', linker.edits[0][2])
        self.assertTrue(terms['토큰']['first'].startswith('(부록)'))
