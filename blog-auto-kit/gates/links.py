"""본문·최종 HTML의 URL을 모아 상업 관계와 허용 도메인을 확인한다."""
import html
import re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit

SHOP_DOMAINS = ('coupang.com', 'coupangcdn.com', 'amzn.to', 'amazon.com', 'amazon.co.jp',
                'shopping.naver.com', 'smartstore.naver.com', 'naver.me', '11st.co.kr',
                'gmarket.co.kr', 'auction.co.kr', 'aliexpress.com', 'temu.com')


class URLExtractor(HTMLParser):
    """상대 URL·다른 스킴도 HTML 속성에서 모은다."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src', 'poster', 'action', 'formaction', 'cite', 'data') and value:
                self.found.append(value)
            elif key == 'srcset' and value:
                self.found.extend(item.strip().split()[0] for item in value.split(',') if item.strip())


def urls(doc):
    """마크다운·HTML 속성·일반 텍스트의 모든 링크를 함께 모은다."""
    text = html.unescape(doc.get('markdown', '') + '\n' + doc.get('html', ''))
    parser = URLExtractor()
    parser.feed(text)
    found = re.findall(r'(?i)(?:https?:)?//[^\s<>"\'()\[\]`]+', text)
    found.extend(re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', text))
    found.extend(re.findall(r'^\s*\[[^\]]+\]:\s*<?([^\s>]+)', text, re.M))
    return sorted(set(found + parser.found))


def domain(url):
    """사용자명·포트·대소문자와 도메인을 구별한다."""
    try:
        return (urlsplit(url).hostname or '').lower().rstrip('.')
    except ValueError:
        return ''


def shopping_url(url):
    host = domain(url)
    return any(host == base or host.endswith('.' + base) for base in SHOP_DOMAINS)


def allowed_domains(root, config_path=None):
    """저장된 발행 기록 대신 현재 설정의 정확한 호스트 허용 목록을 읽는다."""
    from core.config import load_config
    if root is None:
        return []
    root = Path(root)
    path = root / (config_path or ('config.toml' if (root / 'config.toml').exists() else 'config.example.toml'))
    if not path.is_file():
        return []
    values = load_config(path).get('publishing', {}).get('auto_allowed_domains', [])
    if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
        raise ValueError('auto_allowed_domains: 허용 도메인 이름 목록을 넣으세요')
    return [v.lower() for v in values]


def allowed_url(url, domains):
    try:
        parts = urlsplit(url)
        return (parts.scheme == 'https' and not parts.username and not parts.password
                and parts.port in (None, 443) and domain(url) in domains
                and not re.search(r'[\s<>"\'`\\]', url) and not shopping_url(url))
    except ValueError:
        return False


def link_checks(doc, root, config_path=None):
    from gates.checks import result
    found = urls(doc)
    out = []
    if any(shopping_url(url) for url in found):
        out.append(result('links.L1', 'review', 'markdown/html',
                          '본문에 제휴·쇼핑 링크가 있습니다.',
                          '실제 경제관계와 표시를 확인하고 사람이 승인하세요.', ['BXF-038'], True))
    domains = allowed_domains(root, config_path)
    if any(not allowed_url(url, domains) for url in found):
        out.append(result('links.L2', 'review', 'markdown/html',
                          '자동 발행 허용 목록 밖의 URL이 있습니다.',
                          '기관 도메인과 실제 링크를 사람이 확인하세요.', [], True))
    return out
