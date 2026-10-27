#!/usr/bin/env python3
"""정적 사이트의 배포 경로·본문 구조·출처·퀴즈·접근성·전체 용량을 검사한다.

python3 scripts/check_site.py --site site-blog --output /tmp/blog-site.json
--site 생략 시 기존 ReelsBook 검사를 유지한다. 준비중 공통 안내는 이론 원고로 세지 않는다.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = ('question', 'figure', 'principle', 'simulator', 'case', 'workshop', 'story', 'summary', 'quiz')
VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Element:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent = tag, attrs, parent
        self.text = ''

    def within(self, other):
        parent = self.parent
        while parent is not None:
            if parent is other:
                return True
            parent = parent.parent
        return False


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.nodes, self.elements, self.stack = [], [], []
        self.content = ''
        self.feed(path.read_text(encoding='utf-8'))
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        element = Element(tag, attrs, self.stack[-1] if self.stack else None)
        self.nodes.append((tag, attrs))
        self.elements.append(element)
        if tag not in VOID_TAGS:
            self.stack.append(element)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if not any(item.tag in ('script', 'style') for item in self.stack):
            self.content += data
            for item in self.stack:
                item.text += data


def deployment_files(root):
    """책·서가 원본을 배포 URL에 대응시킨다."""
    files, groups = {}, {}
    for folder, prefix in (('shelf', ''), ('site', 'reels'), ('site-shorts', 'shorts'), ('site-blog', 'blog'), ('site-baby', 'baby')):
        for path in sorted((root / folder).rglob('*')):
            if path.is_file():
                files[str(PurePosixPath(prefix) / path.relative_to(root / folder).as_posix())] = path
                groups[path] = folder
    for path in sorted((root / 'starter-kit/samples').glob('*')):
        if path.is_file() and path.suffix in ('.png', '.mp4'):
            files[f'progress/samples/{path.name}'] = path
            groups[path] = 'samples'
    return files, groups


def resolve_reference(current, relative):
    parts = list(PurePosixPath(current).parent.parts)
    for part in relative.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if not parts:
                raise ValueError('배포 루트 밖 경로')
            parts.pop()
        else:
            parts.append(part)
    return '/'.join(parts)


def quiz_errors(page, theory):
    """book.js의 DOM 계약: 문항·보기·단일 정답·해설·피드백 노드."""
    errors, count = [], 0
    quizzes = [e for e in page.elements if 'data-quiz' in e.attrs]
    if theory and not quizzes:
        errors.append('퀴즈 없음')
    for quiz in quizzes:
        questions = [e for e in page.elements if 'data-question' in e.attrs and e.within(quiz)]
        count += len(questions)
        minimum = 3 if theory else 1
        if not minimum <= len(questions) <= 5:
            errors.append(f'퀴즈 문항 수 {len(questions)} (필요 {minimum}~5)')
        for key in ('data-quiz-score', 'data-quiz-reset'):
            if not any(key in e.attrs and e.within(quiz) for e in page.elements):
                errors.append(f'퀴즈 {key} 없음')
        for index, question in enumerate(questions, 1):
            options = [e for e in page.elements if e.tag == 'button' and 'data-correct' in e.attrs and e.within(question)]
            if (len(options) < 2 or any(not e.text.strip() or e.attrs['data-correct'] not in ('true', 'false') for e in options)
                    or sum(e.attrs['data-correct'] == 'true' for e in options) != 1):
                errors.append(f'퀴즈 {index}: 보기·단일 정답 오류')
            if not (question.attrs.get('data-explanation') or '').strip():
                errors.append(f'퀴즈 {index}: 해설 없음')
            if not any('data-feedback' in e.attrs and e.within(question) for e in page.elements):
                errors.append(f'퀴즈 {index}: 피드백 없음')
    return errors, count


def figure_check(page):
    """그림 개수와 관계없이 캡션·SVG의 접근 가능한 이름을 검사한다."""
    issues = []
    figures = [e for e in page.elements if e.tag == 'figure']
    for index, figure in enumerate(figures, 1):
        children = [e for e in page.elements if e.within(figure)]
        captions = [e for e in children if e.tag == 'figcaption' and e.parent is figure]
        if len(captions) != 1 or not captions[0].text.strip():
            issues.append(f'그림 {index}: 내용 있는 figcaption 1개 필요')
        for svg in (e for e in children if e.tag == 'svg' and e.attrs.get('aria-hidden') != 'true'):
            # 이름이 있는 바깥 SVG 안의 좌표·크롭용 SVG는 그림의 일부다.
            # 독립 이미지로 선언한 경우에는 중첩되어도 이름을 검사한다.
            if svg.attrs.get('role') != 'img' and any(
                    parent.tag == 'svg' and svg.within(parent) for parent in children):
                continue
            title = any(e.tag == 'title' and e.text.strip() and e.within(svg) for e in children)
            if not (title or (svg.attrs.get('aria-label') or '').strip()):
                issues.append(f'그림 {index}: SVG 제목 또는 aria-label 필요')
    return issues


def check(root=None, site='site'):
    if site not in {'site', 'site-shorts', 'site-blog', 'site-baby'}:
        raise ValueError('지원하지 않는 사이트')
    shorts = site == 'site-shorts'
    other_book = site != 'site'
    root = Path(root if root is not None else ROOT).resolve()
    pages = {p: Page(p) for folder in (site, 'shelf') for p in sorted((root / folder).rglob('*.html'))}
    ids = {p: {a['id'] for _, a in page.nodes if 'id' in a} | {a['name'] for tag, a in page.nodes if tag == 'a' and 'name' in a} for p, page in pages.items()}
    deployed, groups = deployment_files(root)
    logical_paths = {path: url for url, path in deployed.items()}
    sources_path = root / {'site': 'research', 'site-shorts': 'research-shorts', 'site-blog': 'research-blog', 'site-baby': 'research-baby'}[site] / 'SOURCES.md'
    source_pattern = r'\b[A-Z]{1,4}\d{3}\b' if other_book else r'^###\s+(S\d{3})\.'
    sources = set(re.findall(source_pattern, sources_path.read_text(encoding='utf-8'), re.MULTILINE)) if sources_path.is_file() else set()
    citation_pattern = (r'\bY\d{3}\b' if shorts else
                        r'\b[A-Z]{1,4}\d{3}\b' if other_book else r'\bS\d{3}\b')
    glossary = pages.get(root / site / 'glossary.html')
    terms = {a['id'] for _, a in glossary.nodes if 'data-glossary-entry' in a and 'id' in a} if glossary else set()
    errors, references, pending, questions, source_refs, term_refs, chapters = [], 0, 0, 0, 0, 0, 0
    if not (root / site / 'index.html').is_file():
        errors.append(f'표지 없음: {site}/index.html')
    if not sources_path.is_file():
        errors.append(f'출처 목록 없음: {sources_path.relative_to(root)}')
    if glossary is None and not other_book:
        errors.append('용어집 없음: site/glossary.html')
    for path, page in pages.items():
        label = str(path.relative_to(root))
        if path.is_relative_to(root / site):
            errors.extend(f'{label}: {issue}' for issue in figure_check(page))
        theory = path.parent == root / site / 'chapters' and ((other_book and re.match(r'\d{2}[a-z]?-', path.name) is not None) or (not other_book and (re.match(r'(0[2-9]|1[0-4])-', path.name) is not None or path.name == '05b-ai-tools.html')))
        # BabyBook N3: a tool sample is not a finished theory manuscript.
        if site == 'site-baby' and any(a.get('data-manuscript') == 'pending' for tag, a in page.nodes if tag == 'body'):
            theory = False
        if theory:
            chapters += 1
            blocks = tuple(a['data-block'] for _, a in page.nodes if 'data-block' in a)
            if blocks != BLOCKS:
                errors.append(f'{label}: 9단계 블록 누락·중복·순서 오류 ({", ".join(blocks)})')
        theory_quiz = path.parent == root / site / 'chapters' and (re.match(r'(0[1-9]|1[0-4])-', path.name) is not None or path.name == '05b-ai-tools.html')
        quiz_issues, question_count = quiz_errors(page, theory if other_book else theory_quiz)
        questions += question_count
        errors.extend(f'{label}: {issue}' for issue in quiz_issues)
        for id_, count in Counter(a['id'] for _, a in page.nodes if 'id' in a).items():
            if count > 1:
                errors.append(f'{label}: 중복 ID {id_}')
        cited = set(re.findall(citation_pattern, page.content))
        for tag, attrs in page.nodes:
            if 'fact-pending' in (attrs.get('class') or '').split() or 'data-fact-pending' in attrs:
                pending += 1
                errors.append(f'{label}: fact-pending 요소 남음')
            if 'data-term' in attrs:
                term = attrs['data-term'] or ''
                term_refs += 1
                if term not in terms:
                    errors.append(f'{label}: 미등록 용어 {term}')
            for value in (attrs.get('id', ''), attrs.get('href', ''), attrs.get('aria-label', '')):
                cited.update(match.upper() for match in re.findall(citation_pattern, value or '', re.IGNORECASE))
            if tag == 'img':
                alt = attrs.get('alt')
                decorative = attrs.get('role') == 'presentation' or attrs.get('aria-hidden') == 'true'
                text = (alt or '').strip()
                generic = text.casefold() in {'image', 'img', 'picture', 'photo', '이미지', '사진', '그림'}
                try:
                    filename = Path(unquote(urlsplit(attrs.get('src') or '').path)).name.casefold()
                except ValueError:
                    filename = ''  # 참조 검사에서 잘못된 URL을 보고한다.
                if alt is None or (not text and not (alt == '' and decorative)) or generic or (text and text.casefold() == filename):
                    errors.append(f'{label}: 이미지 대체 텍스트 필요 ({attrs.get("src", "")})')
            for key in ('href', 'src', 'poster', 'data-retry-tool'):
                if not attrs.get(key):
                    continue
                href = attrs[key]
                try:
                    url = urlsplit(href)
                    if url.scheme or url.netloc:
                        continue
                    references += 1
                    decoded = unquote(url.path)
                    if decoded.startswith('/'):
                        errors.append(f'{label}: 상대 경로 필요 {href}')
                        continue
                    logical = resolve_reference(logical_paths[path], decoded) if decoded else logical_paths[path]
                    index = f'{logical}/index.html' if logical else 'index.html'
                    target = deployed.get(logical) or deployed.get(index)
                    if target is None:
                        errors.append(f'{label}: 없는 파일 {href}')
                    elif url.fragment and target in ids and unquote(url.fragment) not in ids[target]:
                        errors.append(f'{label}: 없는 앵커 {href}')
                except ValueError as exc:
                    errors.append(f'{label}: 잘못된 참조 {href} ({exc})')
        source_refs += len(cited)
        errors.extend(f'{label}: 미등록 출처 {source}' for source in sorted(cited - sources))
    if not other_book and chapters != 14:
        errors.append(f'이론 2~15장 필요 (현재 {chapters}개)')
    catalog = []
    try:
        catalog_path = root / site / 'assets/catalog.js'
        catalog_text = catalog_path.read_text(encoding='utf-8') if catalog_path.exists() or not other_book else 'Object.freeze([]);'
        catalog = json.loads(catalog_text.split('Object.freeze(', 1)[1].rsplit(');', 1)[0])
        if not isinstance(catalog, list):
            raise ValueError('도구 목록은 배열이어야 합니다')
        for tool in catalog:
            folder = 'practice' if tool.get('track') == 'practice' else 'chapters'
            path = root / site / (f'{folder}/{tool["slug"]}.html' if tool['slug'] != 'lab' else 'lab.html')
            if tool['id'] not in ids.get(path, set()):
                errors.append(f'도구 목록: 없는 도구 {tool["slug"]}#{tool["id"]}')
    except (OSError, ValueError, IndexError, KeyError, TypeError) as exc:
        errors.append(f'도구 목록 오류: {exc}')
    original_keys = [a['data-practice-check'] for p, page in pages.items() if p.parent == root / site / 'practice' and p.name != 'e2e.html' for _, a in page.nodes if 'data-practice-check' in a]
    steps = set(original_keys)
    e2e_page = pages.get(root / site / 'practice/e2e.html')
    e2e_keys = [a['data-practice-check'] for _, a in e2e_page.nodes if 'data-practice-check' in a] if e2e_page else []
    for key, count in Counter(original_keys).items():
        if count > 1:
            errors.append(f'중복 실습 진행 키 {key}')
    if (not other_book or e2e_page is not None) and (not steps or None in steps or '' in steps or steps != set(e2e_keys)):
        errors.append('실습 단계와 E2E 진행 키 불일치')
    sizes = dict(site=0, shelf=0, samples=0, **{name: 0 for name in ('site-shorts', 'site-blog', 'site-baby') if (root / name).exists()})
    extensions = Counter()
    for path, group in groups.items():
        size = path.stat().st_size
        sizes[group] += size
        extensions[path.suffix.lower() or '(확장자 없음)'] += size
    sizes.update(total=sum(sizes.values()), files=len(groups), by_extension=dict(sorted(extensions.items())))
    return dict(html_pages=len(pages), internal_references=references, catalog_entries=len(catalog), practice_steps=len(steps), theory_chapters=chapters, quiz_questions=questions, source_references=source_refs, term_references=term_refs, fact_pending=pending, deployment_bytes=sizes, errors=errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--site', choices=('site', 'site-shorts', 'site-blog', 'site-baby'), default='site',
                        help='검사할 책 (기본: site). 책별 출처 목록과 배포 경로로 검사 (BabyBook: research-baby, /baby/)')
    args = parser.parse_args()
    result = check(root=args.root, site=args.site)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
    print(rendered, end='')
    raise SystemExit(bool(result['errors']))
