"""직접 입력·RSS와 지난 성과로 주제를 고른다. 외부 RSS는 live에서만 읽는다."""
from html import unescape
import math
import re
from xml.etree import ElementTree
from common import kit_path, read_json, hashed
from transport import HTTP

def rss_topics(text):
    if len(text) > 2000000 or '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise ValueError('RSS 크기 또는 XML 선언을 확인하세요.')
    try:
        root = ElementTree.fromstring(text)
    except ElementTree.ParseError:
        raise ValueError('RSS XML을 읽지 못했습니다.') from None
    topics = []
    atom = '{http://www.w3.org/2005/Atom}'
    for item in root.findall('.//item') + root.findall('.//' + atom + 'entry'):
        def value(name, alternate):
            return item.findtext(name) or item.findtext(atom + alternate) or ''
        title = value('title', 'title')
        content = re.sub('<[^>]+>', '', unescape(value('description', 'summary') or item.findtext(atom + 'content') or title))
        link = value('link', 'id')
        element = item.find(atom + 'link')
        if element is not None:
            link = element.get('href', link)
        if title and content:
            topics.append({'title': title, 'text': content, 'url': link, 'entities': [], 'synthetic': False, 'rights_reviewed': False, 'category': 'RSS'})
    return topics

def select_topic(config, store, flow, *, live=False, http=None):
    candidates = []
    for file in config['sources']['files']:
        values = read_json(kit_path(file))
        candidates.extend(values if isinstance(values, list) else [values])
    for entry in config['sources']['rss']:
        options = entry if isinstance(entry,dict) else {'url':entry}
        feed = options['url']
        if '://' in feed:
            if not live:
                raise ValueError('드라이런에서는 RSS XML을 로컬 파일로 저장해 지정하세요.')
            response = (http or HTTP()).request('GET', feed)
            if response.status_code != 200:
                raise ValueError('RSS 응답 상태를 확인하세요.')
            text = response.text
        else:
            text = kit_path(feed).read_text(encoding='utf-8')
        candidates.extend({**topic,'rights_reviewed':options.get('rights_reviewed',False),'entities':options.get('entities',[]),'category':options.get('category','RSS')} for topic in rss_topics(text))
    history = store.runs()
    seen = {r.get('source_hash') for r in history if r['flow'] == flow and r['status'] in ('done', 'dry_run', 'scheduled', 'uncertain')}
    scores = {}
    for row in store.db.execute("SELECT run_id,value FROM metrics WHERE metric IN ('views','engagedViews') AND value IS NOT NULL"):
        run = next((r for r in history if r['id'] == row[0] and r['flow'] == flow), None)
        if run:
            category = run.get('source', {}).get('category', '')
            scores.setdefault(category, []).append(math.log1p(max(0, row[1])))
    ranked = []
    for order, source in enumerate(candidates):
        if not isinstance(source.get('title'), str) or not isinstance(source.get('text'), str) or not source['text'].strip():
            raise ValueError('소스에는 비어 있지 않은 title·text가 필요합니다.')
        fingerprint = hashed(source['text'].strip())
        if fingerprint in seen:
            continue
        previous = scores.get(source.get('category', ''), [])
        performance = sum(previous) / len(previous) if previous else 0
        score = 1 / (1 + order) + config['sources']['performance_weight'] * performance
        ranked.append((score, -order, {**source, 'selection_score': score, 'performance_score': performance, 'source_hash': fingerprint}))
    if not ranked:
        raise ValueError('새 주제가 없습니다. 이미 처리한 소스를 빼고 원문을 추가하세요.')
    return max(ranked, key=lambda item: item[:2])[2]
