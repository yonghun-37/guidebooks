#!/usr/bin/env python3
"""확정 STYLE-GUIDE 3·5절 검사. 표준 라이브러리만 사용한다.

python3 scripts/style_lint.py site/chapters/0*.html
python3 scripts/style_lint.py site/chapters/[0-9]*.html site/practice/[0-9]*.html \
    --baseline docs/results/phase-9/baseline.json --output /tmp/lint.json

학습자 텍스트는 main(없으면 body)에서 추출한다. 출처 각주·참조 번호·내비·
script/style/template/noscript·hidden은 제외하고 접힌 FAQ/OS 탭의 내용은 포함한다.
HTML 속성·주석은 검사하지 않는다. 글자 수는 유니코드 공백을 뺀 문자 수다.
반환값: 0 통과, 1 문체 기준 위반, 2 입력/기준선 오류. JSON은 위반 시에도 출력한다.
--write-baseline은 최초 스냅샷을 쓰며 기존 파일을 덮어쓰지 않는다.
"""
import argparse
from collections import Counter
from dataclasses import dataclass, field
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
METRIC = 'learner-main-non-whitespace-v1'
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
BLOCKS = set('article aside blockquote br caption dd details div dl dt fieldset figcaption figure h1 h2 h3 h4 h5 h6 hr li main ol p pre section summary table tbody td th thead tr ul'.split())
SKIP_TAGS = {'script', 'style', 'template', 'noscript', 'nav', 'footer'}
SKIP_CLASSES = {'source-notes', 'footnote-ref', 'footnotes', 'draft-sources', 'draft-cite'}
FORBIDDEN = [
    ('지급자', r'지급자'),
    ('대가', r'(?<![가-힣])대가(?=$|[^가-힣]|[는를가로에의도만])'),
    ('장부', r'장부'), ('현금 잔액', r'현금\s*잔액'), ('적격·적격성', r'적격(?:성)?'),
    ('키트 계약', r'(?:로컬\s*)?키트\s*계약'), ('실측 아님', r'실측\s*아님'),
    ('시간 배분 예시', r'시간\s*배분\s*예시'), ('탐색 후보', r'탐색\s*후보'),
    ('성공 화면 면책', r'성공\s*화면을\s*본\s*것으로\s*서술하지\s*않'),
    ('독립 확인 면책', r'독립\s*확인을\s*완료하지\s*못'),
    ('공식 본문 면책', r'공식\s*본문을\s*확보하지\s*못'),
    ('재열람 차단 면책', r'재열람이\s*차단'),
]
# 사실표의 ID 계열만 잡아 UTF-8, ISO-8601 등 일반 기술 표기를 오인하지 않는다.
FACT_PREFIXES = ('AI ALG API ASSET AUTO CRAFT ECON ETHIC EXPL GAP GLOBAL GROW '
                 'KCASE LABEL LAW LEARN META METRIC NEWS NOCODE PRAC PRICE REV '
                 'RISK SEC TAX VIDEO XPLAT YT').split()
INTERNAL = [
    ('7r·7v', r'(?<![A-Za-z0-9])7[rv](?![A-Za-z0-9])'),
    ('Phase', r'(?<![A-Za-z])phase'), ('Hermes', r'hermes'),
    ('원응답', r'원응답'), ('조사자', r'조사자'),
    ('사실 ID', r'(?<![A-Za-z0-9])(?:R2(?:-[A-Z]+)?|' + '|'.join(FACT_PREFIXES) + r')-[A-Z0-9-]*'),
]
CAVEATS = [('미확인', r'미확인'), ('단정할 수 없', r'단정할\s*수\s*없'), ('별개', r'별개')]


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.stack = [self.root]
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append((data, self.getpos()[0]))


def find(node, tag):
    if node.tag == tag:
        return node
    for child in node.children:
        if isinstance(child, Node):
            found = find(child, tag)
            if found is not None:
                return found
    return None


def plain(node):
    return ''.join(plain(child) if isinstance(child, Node) else child[0]
                   for child in node.children)


def check_box(node):
    classes = set(node.attrs.get('class', '').split())
    if 'data-check-points' in node.attrs or classes & {'check-points', 'draft-check'}:
        return True
    # 기존 note 등도 상자의 첫 라벨이 같으면 인식한다.
    if node.tag in {'aside', 'div', 'section'}:
        first = next((child for child in node.children
                      if isinstance(child, Node) or child[0].strip()), None)
        return (isinstance(first, Node) and first.tag in {'strong', 'h2', 'h3', 'h4'}
                and plain(first).strip() == '확인할 점')
    return False


def extract(source):
    root = Document(source).root
    main = find(root, 'main') or find(root, 'body')
    if main is None:
        raise ValueError('main 또는 body가 없습니다')
    parts, lines, inside = [], [], []

    def append(text, line, in_check):
        parts.append(text)
        lines.extend([line] * len(text))
        inside.extend([in_check] * len(text))

    def walk(node, in_check=False):
        attrs = node.attrs
        classes = set(attrs.get('class', '').split())
        # hidden인 OS 패널도 학습자가 탭으로 읽을 텍스트이므로 포함한다.
        hidden = 'hidden' in attrs and 'data-os-panel' not in attrs
        if ((node.tag in SKIP_TAGS and 'data-axis-nav' not in attrs) or classes & SKIP_CLASSES or hidden
                or attrs.get('role') in {'doc-endnotes', 'doc-footnote', 'doc-noteref'}
                or 'data-site-header' in attrs or 'data-book-sidebar' in attrs
                or 'data-mobile-outline' in attrs):
            append('\n', 0, False)
            return
        in_check = in_check or check_box(node)
        if node.tag in BLOCKS:
            append('\n', 0, in_check)
        for child in node.children:
            if isinstance(child, Node):
                walk(child, in_check)
            else:
                text, line = child
                # 원문 행 번호를 각 문자에 대응시킨다.
                for chunk in text.splitlines(keepends=True):
                    append(chunk, line, in_check)
                    line += chunk.count('\n')
        if node.tag in BLOCKS:
            append('\n', 0, in_check)

    walk(main)
    return ''.join(parts), lines, inside, root


def hits(text, lines, rules, ignore_case=False):
    found = []
    for rule, pattern in rules:
        for match in re.finditer(pattern, text, re.I if ignore_case else 0):
            found.append({'rule': rule, 'text': match.group(), 'line': lines[match.start()],
                          'context': re.sub(r'\s+', ' ', text[max(0, match.start()-24):match.end()+36]).strip()})
    return sorted(found, key=lambda hit: (hit['line'], hit['rule']))


def path_key(path):
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def analyze(path, baseline=None):
    source = path.read_text(encoding='utf-8')
    text, lines, inside, root = extract(source)
    outside = ''.join(' ' if is_inside else char for char, is_inside in zip(text, inside))
    inside_text = ''.join(char if is_inside else ' ' for char, is_inside in zip(text, inside))
    body = find(root, 'body')
    track = ('practice' if body and 'data-practice' in body.attrs else
             'theory' if body and 'data-chapter' in body.attrs else 'other')
    groups = {'forbidden': hits(text, lines, FORBIDDEN),
              'internal': hits(text, lines, INTERNAL[:3], True)
                          + hits(text, lines, INTERNAL[3:]),
              'caveats_outside': hits(outside, lines, CAVEATS),
              'caveats_inside': hits(inside_text, lines, CAVEATS)}
    counts = {name: len(found) for name, found in groups.items()}
    char_count = len(re.sub(r'\s', '', text))
    key = path_key(path)
    baseline_chars = None
    ratio = None
    if baseline is not None:
        if key not in baseline['files']:
            raise ValueError(f'기준선에 파일이 없습니다: {key}')
        baseline_chars = baseline['files'][key]['char_count']
        if not isinstance(baseline_chars, int) or isinstance(baseline_chars, bool) or baseline_chars <= 0:
            raise ValueError(f'기준선 글자 수가 유효하지 않습니다: {key}')
        ratio = round(char_count / baseline_chars, 6)
    checks = {'forbidden_zero': not counts['forbidden'], 'internal_zero': not counts['internal'],
              'caveats_at_most_two': counts['caveats_outside'] <= 2,
              'theory_length_at_most_70_percent':
                  char_count * 10 <= baseline_chars * 7 if track == 'theory' and baseline_chars else None}
    return {'path': key, 'track': track, 'char_count': char_count,
            'baseline_char_count': baseline_chars, 'ratio': ratio,
            'counts': counts, 'matches': groups, 'checks': checks,
            'passed': all(value is not False for value in checks.values()),
            'sha256': hashlib.sha256(source.encode('utf-8')).hexdigest()}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('html', nargs='+', type=Path, help='검사할 HTML 파일들')
    parser.add_argument('--baseline', type=Path, help='개편 전 글자 수 JSON')
    parser.add_argument('--write-baseline', type=Path, help='최초 기준선 생성 (기존 파일 덮어쓰기 금지)')
    parser.add_argument('--output', type=Path, help='보고서 JSON 경로 (생략하면 표준 출력)')
    args = parser.parse_args()
    try:
        paths = list(dict.fromkeys(path.resolve() for path in args.html))
        if args.write_baseline and (args.baseline or args.write_baseline.exists()):
            raise ValueError('--write-baseline은 --baseline과 함께 쓰거나 기존 파일에 쓸 수 없습니다')
        if args.output and args.output.resolve() in set(paths + [p.resolve() for p in (args.baseline, args.write_baseline) if p]):
            raise ValueError('보고서 경로가 입력 HTML/기준선과 같습니다')
        baseline = json.loads(args.baseline.read_text(encoding='utf-8')) if args.baseline else None
        if baseline is not None and (not isinstance(baseline, dict) or baseline.get('metric') != METRIC or not isinstance(baseline.get('files'), dict)):
            raise ValueError('기준선 형식 또는 글자 수 집계 방식이 다릅니다')
        results = [analyze(path, baseline) for path in paths]
        if args.write_baseline:
            if args.write_baseline.resolve() in paths:
                raise ValueError('기준선 경로가 입력 HTML과 같습니다')
            write_json(args.write_baseline, {'version': 1, 'metric': METRIC, 'files': {
                row['path']: {key: row[key] for key in ('track', 'char_count', 'sha256')} for row in results}})
        totals = Counter()
        for row in results:
            totals.update(row['counts'])
        report = {'version': 1, 'metric': METRIC, 'baseline': path_key(args.baseline) if args.baseline else None,
                  'summary': {'files': len(results), 'passed': sum(row['passed'] for row in results),
                              'failed': sum(not row['passed'] for row in results),
                              'char_count': sum(row['char_count'] for row in results), 'counts': dict(totals)},
                  'files': results}
        if args.output:
            write_json(args.output, report)
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        return int(any(not row['passed'] for row in results))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'style_lint: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
