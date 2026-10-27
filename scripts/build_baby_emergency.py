#!/usr/bin/env python3
"""공통 JS 데이터에서 배포 HTML의 응급 안내 생성. --check는 어긋나면 실패한다."""
import argparse
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site-baby'
HOST = re.compile(r'<div\b(?P<attrs>[^>]*\bdata-emergency="[^"]*"[^>]*)>(?P<body>.*?)</div>', re.S)
FEVER_NOTE = '측정 부위에 따라 값과 정확도가 달라요. 겨드랑이에서 38℃가 될 때까지 기다리는 뜻은 아니에요. 아기가 뜨겁거나 평소와 다르면 잰 부위·값을 알려 바로 의료진에게 문의하세요.'
ASK = '목록이 모든 응급 상황을 담지는 않아요. 심하게 아파 보이거나 급격히 달라지면 즉시 도움을 요청하세요. 그 밖의 걱정되는 변화는 오늘 소아과에 연락하세요. 증상이 겹치면 위의 긴급한 행동부터 따르세요.'


def data():
    source = (SITE / 'assets/emergency-data.js').read_text()
    return json.loads(re.search(r'const rows = (\[.*?\]);', source, re.S)[1])


def render(match, page):
    rows = data()
    prefix = '../' if page.parent != SITE else ''
    def ref(sid):
        return f'<sup class="footnote-ref"><a href="{prefix}credits.html#{sid.lower()}">[{sid}]</a></sup>'
    def item(row):
        result = f'<p class="emergency-message" data-emergency-id="{row["id"]}">{html.escape(row["text"])}'+''.join(map(ref, row['sources']))+'</p>'
        if row['id'] == 'fever':
            result += f'<p class="small emergency-measurement">{FEVER_NOTE}{ref("N001")}</p>'
        return result
    attrs = match['attrs']
    full = 'data-emergency-full' in attrs
    attrs = re.sub(r'\sclass="[^"]*"', '', attrs)
    attrs += ' class="emergency-grid"' if full else ' class="emergency-inline"'
    if full:
        body = ''.join(f'<section class="emergency-tier {tier}"><h3><b>{num}</b> {label}</h3>'+''.join(item(r) for r in rows if r['tier'] == tier)+'</section>' for tier, num, label in [('call', '①', '119'), ('urgent', '②', '즉시 진료')])
        body += f'<section class="emergency-tier ask"><h3><b>③</b> 오늘 소아과에 묻기</h3><p>{ASK}{ref("N001")}{ref("N090")}</p><p class="small">안전 여부를 판정하는 표가 아닙니다. 숨·반응 이상은 119에 연락하세요.</p></section>'
    else:
        ids = re.search(r'data-emergency="([^"]*)"', attrs)[1].split(',')
        unknown = set(ids) - {r['id'] for r in rows}
        if unknown:
            raise ValueError(f'{page}: 알 수 없는 응급 ID {unknown}')
        body = ''.join(f'<p class="emergency-label">{"119" if r["tier"] == "call" else "즉시 진료"}</p>'+item(r) for r in rows if r['id'] in ids)
    return f'<div{attrs}>{body}</div>'


def build(check=False):
    mismatches = []
    for page in sorted(SITE.rglob('*.html')):
        source = page.read_text()
        result = HOST.sub(lambda m: render(m, page), source)
        if result != source:
            mismatches.append(str(page.relative_to(ROOT)))
            if not check:
                page.write_text(result)
    return mismatches


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    mismatches = build(args.check)
    if args.check and mismatches:
        parser.exit(1, '응급 데이터와 HTML 불일치:\n'+'\n'.join(mismatches)+'\n')
    print(f'응급 정적 HTML: {"일치" if args.check else "생성"} ({len(mismatches)}쪽 변경)')
