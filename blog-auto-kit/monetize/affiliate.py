"""제휴 링크와 경제적 이해관계를 기록한다."""
import csv
import html
from pathlib import Path

COUPANG = '이 게시물은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.'
NAVER = '이 포스팅은 네이버 쇼핑 커넥트 활동의 일환으로, 판매 발생 시 수수료를 제공받습니다.'


def register_link(store, record):
    """수동 또는 모의 링크를 등록한다."""
    if not record.get('id') or not record.get('url'):
        raise ValueError('링크 ID와 주소가 필요합니다')
    if store.get('links', record['id']) is not None:
        raise ValueError('중복 링크 ID입니다')
    store.put('links', record['id'], dict(record))
    return dict(record)


def _mark_links(text, urls):
    """등록된 주소와 일치하는 링크에만 속성을 추가한다."""
    import re
    def mark(match):
        tag = match.group(0)
        href = re.search(r"\bhref\s*=\s*(['\"])(.*?)\1", tag, re.I)
        if not href or html.unescape(href.group(2)) not in urls:
            return tag
        rel = re.search(r"\brel\s*=\s*(['\"])(.*?)\1", tag, re.I)
        if rel:
            values = rel.group(2).split()
            if 'sponsored' not in values: values.append('sponsored')
            return tag[:rel.start(2)] + ' '.join(values) + tag[rel.end(2):]
        return tag[:-1] + ' rel="sponsored">'
    return re.sub(r'<a\b[^>]*>', mark, text, flags=re.I)


def prepare_affiliate(root, store, doc):
    """제휴 문구를 첫 문단에 넣고 링크 대장을 내보낸다."""
    links = store.all('links')
    path = Path(root) / 'output' / 'affiliate' / 'links.csv'
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in links for key in row}) or ['id', 'url']
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(links)
    relations = doc.get('commercial_relations', [])
    disclosures = []
    for relation in relations:
        program = relation.get('program', '').lower()
        if '쿠팡' in program or 'coupang' in program: disclosures.append(COUPANG)
        elif '네이버' in program or 'naver' in program: disclosures.append(NAVER)
        else:
            disclosures.append('광고 관계: ' + ' / '.join(str(relation.get(k, '')) for k in ('kind', 'brand', 'details') if relation.get(k)))
    result = dict(doc)
    prefix = ' '.join(dict.fromkeys(disclosures))
    result['markdown'] = prefix + '\n\n' + doc.get('markdown', '') if prefix else doc.get('markdown', '')
    result['html'] = ('<p>' + html.escape(prefix) + '</p>' if prefix else '') + doc.get('html', '')
    result['html'] = _mark_links(result['html'], {row['url'] for row in links})
    result['links'] = [{'id': row['id'], 'url': row['url'], 'rel': 'sponsored', 'check': '수동 확인 필요'} for row in links]
    result['paid_links'] = result['links']
    result['registry'] = path.relative_to(Path(root)).as_posix()
    return result


def mock_search(query):
    """가상의 검색 결과를 반환한다."""
    return [{'title': query, 'url': 'https://example.invalid/product'}]


def mock_deeplink(url):
    """실제 수익이 발생하지 않는 모의 링크를 반환한다."""
    return 'https://example.invalid/affiliate?target=' + html.escape(url, quote=True)


def live_coupang(*args, **kwargs):
    """공식 서명 근거 확인 전 실연결을 차단한다."""
    raise NotImplementedError('현행 자격과 서명 근거 확인 전 live API는 비활성입니다')
