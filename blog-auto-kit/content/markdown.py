"""마크다운의 작은 부분집합을 안전한 HTML로 바꾼다."""
import html
import re
from urllib.parse import urlsplit


def inline_links(text):
    """HTTPS 주소의 간단한 마크다운 링크만 만든다."""
    def link(match):
        url = html.unescape(match[2])
        if urlsplit(url).scheme != 'https':
            return match[1]
        return '<a href="' + html.escape(url, quote=True) + '">' + match[1] + '</a>'
    return re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)', link, text)

def render(markdown: str) -> str:
    """HTML을 이스케이프하고 제목과 문단을 만든다."""
    out = []
    for block in markdown.strip().split('\n\n'):
        text = inline_links(html.escape(block.strip())).replace('\n', '<br>')
        if text.startswith('## '):
            out.append('<h2>' + text[3:] + '</h2>')
        elif text.startswith('# '):
            out.append('<h1>' + text[2:] + '</h1>')
        elif text:
            out.append('<p>' + text + '</p>')
    return '\n'.join(out)
