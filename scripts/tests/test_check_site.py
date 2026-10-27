"""작은 실제 사이트 fixture로 배포 경로와 품질 게이트 회귀를 검증한다."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'check_site.py'
spec = importlib.util.spec_from_file_location('check_site', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

BLOCKS = ('question', 'figure', 'principle', 'simulator', 'case', 'workshop', 'story', 'summary', 'quiz')
QUIZ = '''<div data-quiz>{questions}<p data-quiz-score></p><button data-quiz-reset>다시</button></div>'''
QUESTION = '''<div data-question data-explanation="이용 근거를 확인합니다."><h3>무엇을 확인하나요?</h3><button data-correct="true">이용 근거</button><button data-correct="false">사진 크기만</button><p data-feedback></p></div>'''


class CheckSiteTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.write('site/assets/catalog.js', 'window.ReelsCatalog = Object.freeze([{"chapter":2,"slug":"02-test","id":"figure"}]);')
        self.write('research/SOURCES.md', '<a id="s001"></a>\n### S001. 공식 자료')
        self.write('site/glossary.html', '<article id="rss" data-glossary-entry>RSS 피드</article>')
        for chapter in range(2, 15):
            body = ''.join(f'<section data-block="{block}" id="{block}"></section>' for block in BLOCKS)
            body += QUIZ.format(questions=QUESTION * 3)
            self.write(f'site/chapters/{chapter:02}-test.html', body)
        self.write('site/chapters/05b-ai-tools.html', body)
        self.write('site/practice/00-start.html', '<input data-practice-check="0:start">')
        self.write('site/practice/e2e.html', '<input data-practice-check="0:start">')
        self.write('shelf/index.html', '<a href="reels/chapters/02-test.html#figure">시작</a>')
        self.write('site/index.html', '<a href="../index.html">책장</a>')

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def check(self):
        with patch.object(checker, 'ROOT', self.root):
            return checker.check()

    def assert_error(self, fragment):
        self.assertTrue(any(fragment in error for error in self.check()['errors']), self.check()['errors'])

    def test_valid_fixture_and_deployed_cross_book_paths(self):
        self.write('shelf/progress/index.html', '<a href="../reels/">교과서</a><a href="../">책장</a>')
        self.assertEqual(self.check()['errors'], [])
        self.assertEqual(checker.check(root=self.root)['errors'], [])

    def test_blog_samples_use_blog_deployment_and_b_sources(self):
        self.write('research-blog/SOURCES.md', '## B023. 미디어 검수')
        self.write('site-blog/index.html', '<a href="chapters/02-revenue.html">수익</a>')
        self.write('site-blog/assets/catalog.js', 'Object.freeze([]);')
        body = ''.join(f'<section data-block="{block}" id="{block}"></section>' for block in BLOCKS)
        body += QUIZ.format(questions=QUESTION * 3)
        body += '<a href="#source-b023">[B023]</a><p id="source-b023">공식 검수</p>'
        chapter = self.write('site-blog/chapters/02-revenue.html', body)
        self.write('site-blog/chapters/pending.html', '<main>준비중</main>')
        self.write('site-blog/practice/07-publish.html', '<input data-practice-check="7:url">')
        self.write('shelf/index.html', '<a href="blog/">블로그</a>')
        result = checker.check(root=self.root, site='site-blog')
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['theory_chapters'], 1)
        self.assertEqual(result['practice_steps'], 1)
        chapter.write_text(body.replace('B023', 'B999'))
        self.assertTrue(any('미등록 출처 B999' in error for error in checker.check(root=self.root, site='site-blog')['errors']))

    def test_missing_file_and_encoded_same_page_anchor(self):
        self.write('site/drafts/sample.html', '<a href="no.html">없음</a><a href="#%EB%AA%A9%EC%B0%A8">앵커</a>')
        self.assert_error('없는 파일 no.html')
        self.assert_error('없는 앵커 #%EB%AA%A9%EC%B0%A8')
        self.write('site/drafts/sample.html', '<h1 id="목차">목차</h1><a href="?view=1#%EB%AA%A9%EC%B0%A8">앵커</a>')
        self.assertEqual(self.check()['errors'], [])

    def test_blog_advanced_registry_and_external_url_are_distinct(self):
        self.write('research-blog/SOURCES.md', '## B023. 자료')
        self.write('research-blog-advanced/SOURCES.md', '## BX001. 심화 자료')
        self.write('shelf/index.html', '<a href="blog/">블로그</a>')
        page = self.write('site-blog/index.html', '<a href="https://example.invalid/?bbsId=BS074#L107">코드</a><p>[BX001]</p>')
        self.assertEqual(checker.check(root=self.root, site='site-blog')['errors'], [])
        page.write_text('<p>[BX999]</p>')
        self.assertTrue(any('미등록 출처 BX999' in e for e in checker.check(root=self.root, site='site-blog')['errors']))

    def test_malformed_or_outside_reference_is_reported_without_crash(self):
        for href in ('http://[bad', '../../../escape.html', '/reels/'):
            with self.subTest(href=href):
                self.write('shelf/index.html', f'<a href="{href}">이동</a>')
                self.assertTrue(self.check()['errors'])

    def test_malformed_image_reference_is_reported_without_crash(self):
        self.write('site/drafts/sample.html', '<img src="http://[bad" alt="카드 예시">')
        self.assert_error('잘못된 참조')

    def test_unknown_footnote_source_and_glossary_key(self):
        self.write('site/drafts/sample.html', '<a href="#source-s999" aria-label="출처 S999">[S999]</a><p id="source-s999">[S999]</p><a data-term="unknown">용어</a>')
        self.assert_error('미등록 출처 S999')
        self.assert_error('미등록 용어 unknown')
        self.write('site/drafts/sample.html', '<a href="#source-s001">[S001]</a><p id="source-s001">[S001]</p><a data-term="rss">RSS</a>')
        self.assertEqual(self.check()['errors'], [])

    def test_missing_or_reordered_chapter_block(self):
        path = self.root / 'site/chapters/02-test.html'
        original = path.read_text()
        path.write_text(original.replace('data-block="question"', 'data-block="other"'))
        self.assert_error('9단계 블록')
        path.write_text(original.replace('data-block="question"', 'data-block="figure"', 1).replace('data-block="figure" id="figure"', 'data-block="question" id="figure"', 1))
        self.assert_error('9단계 블록')

    def test_ai_tools_chapter_is_required_and_checked(self):
        path = self.root / 'site/chapters/05b-ai-tools.html'
        original = path.read_text()
        path.write_text(original.replace('data-block="question"', 'data-block="other"'))
        self.assert_error('9단계 블록')
        path.unlink()
        self.assert_error('이론')

    def test_catalog_distinguishes_plan_15_from_lab_16_by_slug(self):
        (self.root / 'site/chapters/14-test.html').rename(self.root / 'site/chapters/14-plan.html')
        plan = self.root / 'site/chapters/14-plan.html'
        plan.write_text(plan.read_text() + '<section id="planner-sim"></section>')
        self.write('site/lab.html', '<section id="month-scenario"></section>')
        self.write('site/assets/catalog.js', 'Object.freeze([{"chapter":15,"slug":"14-plan","id":"planner-sim"},{"chapter":16,"slug":"lab","id":"month-scenario"}]);')
        self.assertEqual(self.check()['errors'], [])

    def test_catalog_checks_practice_tools_in_the_practice_folder(self):
        self.write('site/practice/09-records.html', '<section id="care-log"></section>')
        self.write('site/assets/catalog.js', 'Object.freeze([{"chapter":9,"slug":"09-records","id":"care-log","track":"practice"}]);')
        self.assertEqual(self.check()['errors'], [])
        (self.root / 'site/practice/09-records.html').unlink()
        self.assert_error('없는 도구 09-records#care-log')

    def test_bad_quiz_options_explanation_and_question_count(self):
        for question in (QUESTION.replace('true', 'false'), QUESTION.replace('data-explanation="이용 근거를 확인합니다."', 'data-explanation=""'), QUESTION.replace('<button data-correct="false">사진 크기만</button>', ''), QUESTION.replace('이용 근거</button>', ' </button>')):
            with self.subTest(question=question):
                self.write('site/practice/01-test.html', QUIZ.format(questions=question))
                self.assert_error('퀴즈')
        self.write('site/practice/01-test.html', QUIZ.format(questions=QUESTION))
        self.assertEqual(self.check()['errors'], [])
        self.write('site/chapters/02-test.html', ''.join(f'<section data-block="{b}" id="{b}"></section>' for b in BLOCKS) + QUIZ.format(questions=QUESTION))
        self.assert_error('퀴즈')

    def test_chapter_one_needs_three_questions_without_nine_block_requirement(self):
        self.write('site/chapters/01-map.html', QUIZ.format(questions=QUESTION))
        self.assert_error('퀴즈 문항 수 1')
        self.write('site/chapters/01-map.html', QUIZ.format(questions=QUESTION * 3))
        self.assertEqual(self.check()['errors'], [])

    def test_image_requires_useful_alt_or_explicit_decoration(self):
        self.write('site/picture.svg', '<svg/>')
        for attrs in ('', 'alt=""', 'alt="   "', 'alt="image"', 'alt="picture.svg"'):
            with self.subTest(attrs=attrs):
                self.write('site/drafts/sample.html', f'<img src="../picture.svg" {attrs}>')
                self.assert_error('대체 텍스트')
        for attrs in ('alt="" role="presentation"', 'alt="" aria-hidden="true"', 'alt="카드 생성 전후 비교"'):
            with self.subTest(attrs=attrs):
                self.write('site/drafts/sample.html', f'<img src="../picture.svg" {attrs}>')
                self.assertEqual(self.check()['errors'], [])

    def test_fact_pending_counts_elements_only(self):
        self.write('site/drafts/sample.html', '<!-- fact-pending --><p>fact-pending은 검사 이름입니다.</p><script>"fact-pending"</script>')
        self.assertEqual(self.check()['errors'], [])
        self.write('site/drafts/sample.html', '<p class="note fact-pending">확인 필요</p><p data-fact-pending>확인 필요</p>')
        self.assert_error('fact-pending')
        self.assertEqual(self.check()['fact_pending'], 2)

    def test_duplicate_practice_key_and_e2e_set_mismatch(self):
        self.write('site/practice/01-next.html', '<input data-practice-check="0:start">')
        self.assert_error('중복 실습 진행 키')
        self.write('site/practice/01-next.html', '<input data-practice-check="1:next">')
        self.assert_error('E2E 진행 키 불일치')
        self.write('site/practice/e2e.html', '<input data-practice-check="0:start"><input data-practice-check="1:next">')
        self.assertEqual(self.check()['errors'], [])

    def test_deployment_bytes_include_unreferenced_assets_and_sample_mapping(self):
        self.write('site/assets/extra.bin', '1234567')
        self.write('starter-kit/samples/card.png', '12345')
        self.write('starter-kit/samples/copy.json', 'not deployed')
        self.write('shelf/progress/index.html', '<a href="samples/card.png">그림</a>')
        result = self.check()
        self.assertEqual(result['errors'], [])
        size = result['deployment_bytes']
        self.assertEqual(size['site'], sum(p.stat().st_size for p in (self.root / 'site').rglob('*') if p.is_file()))
        self.assertEqual(size['samples'], 5)
        self.assertEqual(size['total'], size['site'] + size['shelf'] + 5)
        self.assertGreaterEqual(size['by_extension']['.bin'], 7)

    def test_cli_returns_failure_and_saves_report(self):
        self.write('site/drafts/sample.html', '<a href="missing.html">이동</a>')
        report = self.root / 'report.json'
        result = subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), '--output', str(report)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout), json.loads(report.read_text()))
        self.assertIn('없는 파일 missing.html', '\n'.join(json.loads(result.stdout)['errors']))


class ShortsSiteTests(unittest.TestCase):
    setUp = CheckSiteTests.setUp
    write = CheckSiteTests.write

    def test_shorts_mode_checks_deployed_links_and_y_sources(self):
        self.write('research-shorts/SOURCES.md', '| <a id="y001"></a>Y001 | 공식 자료 |')
        self.write('site-shorts/index.html', '<a href="chapters/02-revenue.html#figure">샘플</a>')
        body = ''.join(f'<section data-block="{b}" id="{b}"></section>' for b in BLOCKS)
        body += QUIZ.format(questions=QUESTION * 3)
        self.write('site-shorts/chapters/02-revenue.html', body + '<p id="source-y001">[Y001]</p>')
        self.write('shelf/index.html', '<a href="shorts/">쇼츠</a>')
        result = checker.check(root=self.root, site='site-shorts')
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['theory_chapters'], 1)
        self.write('site-shorts/index.html', '<p>[Y999]</p><a href="missing.html">없음</a>')
        errors = checker.check(root=self.root, site='site-shorts')['errors']
        self.assertTrue(any('미등록 출처 Y999' in e for e in errors))
        self.assertTrue(any('없는 파일 missing.html' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
