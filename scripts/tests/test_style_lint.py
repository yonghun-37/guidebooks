"""문체 게이트의 추출 범위·상자 예외·비율·CLI 회귀 검사."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'style_lint.py'
spec = importlib.util.spec_from_file_location('style_lint', SCRIPT)
lint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lint
spec.loader.exec_module(lint)


class StyleLintTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'chapter.html'

    def analyze(self, content, body='data-chapter="test"', baseline=None):
        self.path.write_text(f'<html><body {body}><main>{content}</main></body></html>', encoding='utf-8')
        return lint.analyze(self.path, baseline)

    def test_only_learner_content_including_axis_cards_and_closed_faq(self):
        row = self.analyze('''<script>Hermes</script><style>Phase</style><!-- PRAC-01 -->
          <nav>Hermes</nav><aside class="source-notes">Hermes PRAC-01</aside>
          <p data-fact-id="PRAC-01" title="Hermes">답입니다.<sup class="footnote-ref">[S001]</sup></p>
          <details><summary>질문</summary><p>원응답</p></details>
          <nav data-axis-nav><a href="#axis">탐색 후보</a></nav>
          <p hidden>Phase</p><div data-os-panel hidden>7r</div>''')
        self.assertEqual(row['counts']['internal'], 2)
        self.assertEqual(row['counts']['forbidden'], 1)
        self.assertEqual(row['char_count'], len('답입니다.질문원응답탐색후보7r'))

    def test_inline_markup_does_not_hide_terms(self):
        row = self.analyze('<p>키트 <strong>계약</strong>·미<strong>확인</strong>·PRAC-<b>25</b></p>')
        self.assertEqual(row['counts']['forbidden'], 1)
        self.assertEqual(row['matches']['internal'][0]['text'], 'PRAC-25')
        self.assertEqual(row['counts']['caveats_outside'], 1)

    def test_check_boxes_exempt_caveats_but_never_internal_terms(self):
        row = self.analyze('''<p>미확인 별개 단정할 수 없습니다</p>
          <aside class="check-points"><strong>확인할 점</strong><p>미확인 PRAC-01</p></aside>
          <div class="note"><h3>확인할 점</h3><p>단정할 수 없습니다</p></div>
          <aside class="draft-check"><strong>확인할 점</strong>별개</aside>
          <div data-check-points>미확인</div><p>확인할 점을 읽으세요. 별개</p>''')
        self.assertEqual(row['counts']['caveats_outside'], 4)
        self.assertEqual(row['counts']['caveats_inside'], 4)
        self.assertEqual(row['counts']['internal'], 1)
        self.assertFalse(row['checks']['caveats_at_most_two'])

    def test_caveat_limit_is_two(self):
        row = self.analyze('<p>미확인 별개</p>')
        self.assertTrue(row['passed'])
        self.assertTrue(self.analyze('<p>단정할 수 없습니다</p>')['passed'])

    def test_fact_namespaces_and_ascii_boundaries(self):
        row = self.analyze('<p>API- META-01 PRAC-25 R2-ACC-01 EXPL-08 7r에서 7v PHASE 9 Hermes 원응답 조사자</p>')
        self.assertEqual(row['counts']['internal'], 11)
        row = self.analyze('<p>UTF-8 ISO-8601 MyPhase 17rpm 대가족 기대가 큽니다. 대가를 받습니다.</p>')
        self.assertEqual(row['counts']['internal'], 0)
        self.assertEqual(row['counts']['forbidden'], 1)

    def test_forbidden_table_phrases(self):
        text = ('지급자 대가 장부 현금 잔액 적격성 로컬 키트 계약 실측 아님 시간 배분 예시 탐색 후보 '
                '성공 화면을 본 것으로 서술하지 않습니다 독립 확인을 완료하지 못했다 '
                '공식 본문을 확보하지 못했다 재열람이 차단됐다')
        self.assertEqual(self.analyze(f'<p>{text}</p>')['counts']['forbidden'], 13)

    def test_count_is_stable_across_layout_whitespace_and_reports_source_line(self):
        a = self.analyze('<p>한 줄</p><p>두 줄</p>')
        b = self.analyze('\n  <p>한 줄</p>\n\n <p>두 줄</p>')
        self.assertEqual(a['char_count'], b['char_count'])
        row = self.analyze('\n<p>정상</p>\n<p>Hermes</p>')
        self.assertEqual(row['matches']['internal'][0]['line'], 3)

    def test_baseline_ratio_exact_boundary_and_track(self):
        baseline = {'files': {lint.path_key(self.path): {'char_count': 10}}}
        row = self.analyze('<p>가나다라마바사</p>', baseline=baseline)
        self.assertEqual(row['ratio'], 0.7)
        self.assertTrue(row['passed'])
        self.assertFalse(self.analyze('<p>가나다라마바사아</p>', baseline=baseline)['passed'])
        practice = self.analyze('<p>가나다라마바사아</p>', body='data-practice="test"', baseline=baseline)
        self.assertIsNone(practice['checks']['theory_length_at_most_70_percent'])
        self.assertTrue(practice['passed'])

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.path), *map(str, args)],
                              text=True, capture_output=True)

    def test_cli_snapshot_report_and_overwrite_protection(self):
        self.analyze('<p>Hermes</p>')
        baseline = self.path.with_suffix('.baseline.json')
        report = self.path.with_suffix('.lint.json')
        result = self.run_cli('--write-baseline', baseline, '--output', report)
        self.assertEqual(result.returncode, 1)
        saved = baseline.read_bytes()
        result = self.run_cli('--baseline', baseline, '--output', report)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(report.read_text())['files'][0]['ratio'], 1)
        self.assertEqual(self.run_cli('--write-baseline', baseline).returncode, 2)
        self.assertEqual(baseline.read_bytes(), saved)
        self.assertEqual(self.run_cli('--output', self.path).returncode, 2)

    def test_invalid_or_missing_baseline_fails(self):
        self.analyze('<p>정상</p>')
        baseline = self.path.with_suffix('.json')
        self.assertEqual(self.run_cli('--baseline', baseline).returncode, 2)
        baseline.write_text(json.dumps({'metric': lint.METRIC, 'files': {}}))
        self.assertEqual(self.run_cli('--baseline', baseline).returncode, 2)
        baseline.write_text('{"metric":"other","files":{}}')
        self.assertEqual(self.run_cli('--baseline', baseline).returncode, 2)
        self.assertEqual(self.run_cli().returncode, 0)


if __name__ == '__main__':
    unittest.main()
