"""키트가 생성한 HTML과 첫 문단의 실제 경제관계를 확인한다."""
import re
from html.parser import HTMLParser
from content.markdown import render

class TextExtractor(HTMLParser):
    """HTML의 보이는 텍스트를 모은다."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def html_text(value):
    """태그를 제거하고 텍스트를 반환한다."""
    parser = TextExtractor(); parser.feed(value)
    return ' '.join(parser.parts)


def body_text(doc):
    """작성 원문과 최종 HTML을 함께 검사한다."""
    return doc.get('markdown', '') + '\n' + html_text(doc.get('html', ''))


def consistent(doc):
    """원고의 HTML을 금지하고 허용한 렌더러 결과와 정확히 비교한다."""
    markdown = doc.get('markdown', '')
    if re.search(r'<\s*(?:/?[A-Za-z][\w:-]*\b|!--|!DOCTYPE\b)', markdown, re.I):
        return False
    from monetize.affiliate import _mark_links
    expected = _mark_links(render(markdown), {link['url'] for link in doc.get('paid_links', [])
                          if link.get('url') and 'sponsored' in link.get('rel', '').split()})
    return expected == doc.get('html', '')


RELATION_WORDS = {
    'commission': ('수수료',),
    'goods': ('무료 제공', '무료제공', '제품 제공', '제품제공', '상품 제공', '상품제공', '상품 협찬', '제품 협찬'),
    'fee': ('광고비', '원고료', '유료광고', '유료 광고'),
    'loan': ('대여', '빌려', '대여받'),
}


def relation_kinds(relation):
    """등록한 관계의 종류와 상세 내용에서 필요한 표시들을 모은다."""
    kind = str(relation.get('kind', '')).lower()
    details = str(relation.get('details', ''))
    kinds = set()
    aliases = {'affiliate': 'commission', 'commission': 'commission', '수수료': 'commission',
               'goods': 'goods', 'product': 'goods', '제품제공': 'goods',
               'fee': 'fee', 'advertising': 'fee', '광고비': 'fee', 'loan': 'loan', '대여': 'loan'}
    if kind in aliases:
        kinds.add(aliases[kind])
    for name, words in RELATION_WORDS.items():
        if any(word in details for word in words):
            kinds.add(name)
    return kinds


def economic_relations(doc):
    """문서·계약·연결 등록부의 관계를 같은 목록으로 모은다."""
    relations = list(doc.get('commercial_relations', []))
    relations += doc.get('contract', {}).get('commercial_relations', [])
    relations += doc.get('registered_relations', [])
    for link in doc.get('links', []) + doc.get('paid_links', []):
        if link.get('kind') or link.get('details'):
            relations.append(link)
    from gates.links import urls, shopping_url
    if any(shopping_url(url) for url in urls(doc)):
        relations.append({'kind': 'affiliate', 'details': '본문 제휴·쇼핑 링크 수수료 확인'})
    return relations


def _positive_disclosure(kind, value):
    """관계를 부인하거나 이름만 언급한 문장을 실제 수령 표시로 세지 않는다."""
    words = RELATION_WORDS[kind]
    for sentence in re.split(r'[.!?\n]', value):
        for word in words:
            if word not in sentence:
                continue
            if re.search(re.escape(word) + r'.{0,24}(?:받지|지급하지|없|않)', sentence):
                continue
            if re.search(re.escape(word) + r'.{0,30}(?:제공받|지급받|받(?:습니다|아요|았|아|을|게|는다))', sentence):
                return True
    return False


def relation_disclosure_checks(doc):
    """각 경제관계를 첫 문단에서 실제 받는 사실로 공개하게 한다."""
    from gates.checks import result
    relations = economic_relations(doc)
    out = []
    if doc.get('content_type') in ('affiliate', 'sponsor') and not relations:
        return [result('disclosure.D1', 'review', 'commercial_relations',
                       '상업 글의 실제 경제관계 자료가 없습니다.',
                       '수수료·제품 제공·광고비·대여 자료를 등록하세요.', ['BXF-038'], False)]
    opening = doc.get('markdown', '').strip().split('\n\n', 1)[0]
    final_opening = html_text(doc.get('html', '').split('</p>', 1)[0])
    text = body_text(doc)
    required = set()
    for relation in relations:
        kinds = relation_kinds(relation)
        if not kinds:
            out.append(result('disclosure.D1', 'review', 'commercial_relations',
                              '경제관계의 구체적인 내용이 불명확합니다.',
                              '받는 물품·수수료·광고비·대여를 확인하세요.', ['BXF-038'], False))
        required.update(kinds)
        for kind in sorted(kinds):
            words = RELATION_WORDS[kind]
            if not all(_positive_disclosure(kind, value) for value in (opening, final_opening)):
                rule = 'disclosure.D2' if any(word in text for word in words) else 'disclosure.D1'
                out.append(result(rule, 'block', 'commercial_relations',
                                  f'첫 문단에 {words[0]} 관계가 공개되지 않았습니다.',
                                  '실제 받는 관계를 첫 문단에 각각 밝히세요.', ['BXF-035', 'BXF-038']))
    if (len(required) > 1 or len(relations) > 1) and any(row['decision'] != 'pass' for row in out):
        out.append(result('disclosure.D5', 'block', 'commercial_relations',
                          '복수의 경제적 관계 중 일부가 표시되지 않았습니다.',
                          '각 관계를 모두 공개하세요.', ['BXF-038']))
    return out
