#!/usr/bin/env python3
"""원고·연구·인계 표에서 실험실 목록/용어집/출처를 갱신한다. 외부 패키지 불필요."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from style_lint import Document, Node

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
CHAPTERS = sorted((SITE / 'chapters').glob('[0-9][0-9]-*.html'))
PAGES = CHAPTERS + sorted((SITE / 'practice').glob('*.html'))
E = html.escape


def nodes(node):
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from nodes(child)


def text(node):
    return ''.join(text(c) if isinstance(c, Node) else c[0] for c in node.children)


def has_class(node, name):
    return name in node.attrs.get('class', '').split()


def shell(slug, title, intro, content, scripts=''):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} | ReelsBook</title><link rel="icon" href="data:,"><link rel="stylesheet" href="assets/book.css"><script src="assets/book.js" defer></script>{scripts}</head>
<body data-chapter="{slug}"><a class="skip-link" href="#main">본문으로 건너뛰기</a><header data-site-header><a href="index.html">ReelsBook</a></header>
<main id="main" class="appendix-main"><p class="kicker" data-chapter-kicker>(이론) ReelsBook / 부록</p><h1 data-chapter-title>(이론) {title}</h1><p class="lead">{intro}</p>
{content}
<nav data-chapter-pager aria-label="이전·다음 장"></nav></main><footer data-site-footer></footer></body></html>\n'''


def catalog():
    entries = []
    for p in CHAPTERS:
        # JS 연결 방식을 추측하지 않고 현재 HTML의 학습 블록을 읽는다.
        doc = Document(p.read_text()).root
        for section in nodes(doc):
            if section.attrs.get('data-block') not in ('figure', 'simulator'):
                continue
            tool = next((n for n in nodes(section) if has_class(n, 'simulator')), section)
            heading = next(n for n in nodes(tool) if n.tag in ('h2', 'h3'))
            title = text(heading)
            if section.attrs['data-block'] == 'figure':
                title = ' · '.join(text(n) for card in nodes(section) if has_class(card, 'axis-card')
                                   for n in nodes(card) if n.tag == 'strong') or title
            entries.append(dict(chapter=int(p.name[:2]), slug=p.stem,
                                id=tool.attrs['id'], title=title, section=section.attrs['id']))
    entries.append(dict(chapter=15,slug='lab',id='month-scenario',title='내 계정 한 달 시나리오',section='month-scenario'))
    (SITE/'assets/catalog.js').write_text('// scripts/build_appendices.py가 현재 원본 HTML에서 생성. 계산/HTML 복제 없음.\nwindow.ReelsCatalog = Object.freeze('+json.dumps(entries,ensure_ascii=False,indent=2)+');\n')
    return entries


class TermLinks(HTMLParser):
    """본문의 첫 일반 텍스트에만 용어 링크를 넣고 코드·각주·기존 링크는 보존한다."""
    def __init__(self, source, terms, path):
        super().__init__(convert_charrefs=False)
        self.terms, self.path = terms, path
        self.stack, self.edits = [], []
        self.offsets = [0]
        for line in source.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append((tag, dict(attrs)))

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not any(tag == 'main' for tag, _ in self.stack):
            return
        if any(tag in {'a','code','pre','script','style','aside','nav','footer','h1','h2','h3','h4','button','option'}
               or 'hidden' in attrs for tag, attrs in self.stack):
            return
        line, column = self.getpos()
        base = self.offsets[line-1] + column
        occupied = []
        for name, term in self.terms.items():
            if 'first' in term:
                continue
            match = re.search(r'(?<![A-Za-z])'+re.escape(name)+r'(?![A-Za-z])', data)
            if not match or any(match.start() < end and match.end() > start for start, end in occupied):
                continue
            occupied.append(match.span())
            number = int(self.path.name[:2]) if self.path.name[:2].isdigit() else None
            first = f'(이론) {number}장' if self.path.parent.name == 'chapters' else f'(실습) {number}' if number is not None else '(실습) 전체 진행표'
            term.update(first=first, page=str(self.path.relative_to(SITE)))
            label = match[0]
            replacement = f'<a href="../glossary.html#{term["id"]}" data-term="{term["id"]}" data-term-description="{E(term["description"], quote=True)}">{label}</a>'
            self.edits.append((base+match.start(), base+match.end(), replacement))
        self.edits.sort()


def glossary():
    terms = {'파이프라인':dict(id='pipeline',description='앞 작업의 결과를 다음 작업의 입력으로 이어 주는 흐름.')}
    b_ids = dict(zip(['프롬프트','JSON','템플릿','렌더링','프레임','TTS','SRT','드라이런','해시','노코드','커넥터'],['prompt','json','template','rendering','frame','tts','srt','dry-run','hash','no-code','connector']))
    for phase in 'abc':
        for line in (ROOT/f'docs/results/phase-5{phase}-glossary.md').read_text().splitlines():
            if not line.startswith('|'): continue
            fields = [f.strip() for f in line.split('|')[1:-1]]
            if len(fields)!=4 or not re.match(r'\d',fields[2]): continue
            name = fields[0].split(' (`')[0]
            if phase=='b': id_ = b_ids[name]
            else: id_ = re.search(r'`([^`]+)`', fields[0])[1]
            if name not in terms: terms[name]=dict(id=id_,description=fields[1])
    categories = {
        '플랫폼':['캐러셀','알고리즘','교차 게시'], '수익':['니치','브랜디드 콘텐츠','제휴 마케팅','현금 잔액'],
        '제작':['프롬프트','JSON','템플릿','렌더링','프레임','TTS','SRT'],
        '자동화':['파이프라인','API','RSS','드라이런','해시','노코드','커넥터','컨테이너','액세스 토큰','2단계 인증'],
        '법':['인용','공정 이용','공공누리'], '세금':['원천징수'], '지표':['조회','도달','인사이트']}
    for category,names in categories.items():
        for name in names: terms[name]['category']=category
    # 개편에서 없앤 말은 제거하고 현재 쓰는 쉬운 이름으로 맞춘다.
    terms.pop('현금 잔액')
    for old, new, description in [
        ('프롬프트', '지시문', 'AI에게 작업 목적·자료·지켜야 할 조건·결과 형식을 알려 주는 문장.'),
        ('브랜디드 콘텐츠', '협찬', '브랜드의 돈·제품·서비스 등을 받고 콘텐츠를 만드는 일.'),
        ('제휴 마케팅', '제휴 링크', '링크를 거친 인정 구매 등에 따라 수수료를 받는 방식.'),
    ]:
        terms[new] = terms.pop(old)
        terms[new]['description'] = description
    terms['원천징수']['description'] = '돈을 보내는 쪽이 세금을 미리 떼어 납부하는 방식. 최종 세금과 다를 수 있습니다.'
    terms['RSS']['description'] = '새 글의 제목·링크·짧은 설명 등을 모아 받는 피드 형식. 이용 권리는 따로 확인합니다.'
    for p in PAGES:
        source = p.read_text()
        # 첫 사용 링크를 다시 계산하므로 반복 실행해도 같은 결과가 나온다.
        source = re.sub(r'<a [^>]*\bdata-term="[^"]*"[^>]*>(.*?)</a>', r'\1', source, flags=re.S)
        linker = TermLinks(source, terms, p)
        for start, end, replacement in reversed(linker.edits):
            source = source[:start] + replacement + source[end:]
        p.write_text(source)
    terms = {name: term for name, term in terms.items() if 'first' in term}
    korean={'API':'에이피아이','RSS':'알에스에스','JSON':'제이슨','TTS':'티티에스','SRT':'에스알티','2단계 인증':'이단계 인증'}
    entries=[]
    for name,t in sorted(terms.items(),key=lambda item:korean.get(item[0],item[0])):
        entries.append(f'''<article class="glossary-entry" id="{t['id']}" data-glossary-entry data-category="{t['category']}" data-search="{E(name+' '+t['id']+' '+t['description'],quote=True)}"><p class="small">{t['category']}</p><h2>{E(name)}</h2><p>{E(t['description'])}</p><p><a href="{t['page']}">처음 나온 {t['first']} →</a></p></article>''')
    content='''<div class="filter-row"><label>용어·설명 검색 <input id="term-search" type="search" placeholder="예: 드라이런, API, 지시문"></label><label>분류 <select id="term-category"><option value="">전체</option>'''+''.join(f'<option>{c}</option>' for c in categories)+'''</select></label></div><p id="term-count" role="status">모든 용어를 가나다순으로 표시합니다. 영문 약어는 한국어 발음 순서입니다.</p><div class="glossary-grid">'''+''.join(entries)+'''</div><noscript><p>검색은 자바스크립트가 필요합니다. 브라우저의 찾기 기능으로 전체 목록을 검색할 수 있습니다.</p></noscript>'''
    (SITE/'glossary.html').write_text(shell('glossary','용어집','처음 만나는 말은 쉬운 설명과 처음 나온 장으로 연결합니다.',content,'<script src="assets/glossary.js" defer></script>'))
    return len(terms)


def credits():
    sources={sid:(title,dict(re.findall(r'^- ([^:]+): (.*)$',body,re.M))) for sid,title,body in re.findall(r'### (S\d+)\. (.*?)\n(.*?)(?=\n<a id=|\Z)',(ROOT/'research/SOURCES.md').read_text(),re.S)}
    cited={}
    for p in PAGES:
        doc = Document(p.read_text()).root
        note = next((n for n in nodes(doc) if has_class(n, 'source-notes')), None)
        if note is None:
            continue
        referenced = {n.attrs.get('href', '')[1:] for n in nodes(doc)
                      if n.tag == 'a' and n.attrs.get('href', '').startswith('#source-')}
        for item in nodes(note):
            if item.tag != 'li':
                continue
            anchors = {n.attrs['id'] for n in nodes(item) if 'id' in n.attrs}
            used = anchors & referenced
            if not used:
                continue
            for sid in sorted(set(re.findall(r'\bS\d{3}\b', text(item)))):
                assert sid in sources, sid
                track = '실습' if p.parent.name == 'practice' else '이론'
                label = f'({track}) {int(p.name[:2])}' if p.name[:2].isdigit() else f'({track}) 전체 진행표'
                cited.setdefault(sid, []).append((str(p.relative_to(SITE).with_suffix('')), sorted(used)[0], label))
    entries=[]
    for sid,links in sorted(cited.items()):
        title,meta=sources[sid]
        data=''.join(f'<div><dt>{label}</dt><dd>{E(meta.get(key,"미상"))}</dd></div>' for label,key in [('기관','기관'),('게시·갱신일','게시·갱신일'),('확인일(조사 접근일)','접근일'),('신뢰도 등급','신뢰도')])
        backlink=' · '.join(f'<a href="{slug}.html#{anchor}">{n} 각주</a>' for slug,anchor,n in links)
        entries.append(f'<li class="source-entry" id="{sid.lower()}"><h3>{sid} · <a href="{E(meta["URL"],quote=True)}">{E(title)}</a></h3><dl class="source-meta">{data}</dl><p>사용한 내용과 확인할 점은 연결된 본문 각주에서 읽으세요.</p><p>인용한 장: {backlink}</p></li>')
    content=f'''<p class="note warning">2026년 10월 조사 기준, 정책은 바뀔 수 있습니다. 확인일은 2026-10-26입니다. 내 계정의 이용 조건은 앱에서 확인하고, 개별 법·세무 문제는 전문가에게 문의하세요.</p>
<nav class="related-links" aria-label="크레딧 절"><a href="#sources">인용 출처</a><a href="#licenses">폰트·도구</a><a href="#disclosure">가상·합성 고지</a><a href="#updates">업데이트 기록</a></nav>
<section id="sources" class="chapter-block"><h2>본문에서 인용한 출처 {len(entries)}개</h2><p>A: 공식 문서·법령·정부·제작자, B: 언론·업계 조사, C: 개인·블로그. 등급 A도 최신성·한국 적용을 보증하지 않습니다. 날짜 미상을 접근일로 바꾸지 않았습니다. 번호는 연구 목록의 원래 번호여서 중간 번호가 빠질 수 있습니다.</p><ul class="source-list">{''.join(entries)}</ul></section>
<section id="licenses" class="chapter-block"><h2>폰트·도구 라이선스</h2><p>라이선스 링크 확인: 2026-10-26. 연구의 정책 출처 목록과 별도로 제공하는 제작 크레딧입니다. 사용한 구성요소의 원문 조건을 따릅니다.</p>
<ul><li>웹 본문: Pretendard Variable v1.3.9, Kil Hyung-jin, SIL OFL 1.1. <a href="https://github.com/orioncactus/pretendard/blob/v1.3.9/LICENSE">원문 라이선스</a>. 고정 버전 CDN을 사용하며 연결이 안 되면 시스템 폰트로 표시합니다.</li>
<li>샘플 이미지: Google Fonts / Adobe의 Noto Sans KR, SIL OFL 1.1. <a href="assets/licenses/NotoSansKR-OFL.txt">동봉 저작권·라이선스 전문</a>. 카드에는 이 글꼴로 렌더링한 픽셀이 포함됩니다.</li>
<li>스타터 키트 원본 코드·합성 피드·생성 샘플: MIT, Guidebooks contributors. <a href="assets/img/samples/LICENSE.txt">원문과 적용 범위</a>. 교과서 전체의 권리로 확대하지 않습니다.</li>
<li>카드 렌더링: <a href="https://pillow.readthedocs.io/en/stable/about.html#license">Pillow, MIT-CMU 라이선스 고지</a>. 설정: <a href="https://github.com/yaml/pyyaml/blob/main/LICENSE">PyYAML, MIT</a>.</li>
<li>영상 도구: <a href="https://github.com/imageio/imageio-ffmpeg/blob/main/LICENSE">imageio-ffmpeg 래퍼, BSD 2-Clause</a>. FFmpeg 실행 파일은 래퍼와 별도 라이선스이며 빌드에 따라 LGPL/GPL이 적용됩니다. <a href="https://ffmpeg.org/legal.html">FFmpeg 공식 설명</a>. 실행 파일을 이 사이트에 재배포하지 않습니다.</li>
<li>브라우저 검증: <a href="https://github.com/microsoft/playwright/blob/main/LICENSE">Playwright, Apache 2.0</a>. 사이트 실행에 필요한 라이브러리는 아닙니다. 본문·도식·CSS·JS는 새로 작성했으며 참고 사이트에서는 학습 구조와 UX 패턴만 참고했습니다.</li></ul></section>
<section id="disclosure" class="chapter-block"><h2>가상 인물·합성 데이터 고지</h2><p>하린·정 선배·하린의 계정과 실습 수치는 가상입니다. 예제 피드·카드·영상은 synthetic=true 자료로 만든 교육용 샘플이며 실제 뉴스 보도가 아닙니다. 표지 영상은 무음이며 한글 자막이 화면에 포함됩니다. 별도 자막 파일도 제공합니다.</p><p>계산 도구와 시간 계획은 공개한 가정에 따른 연습이며 수익·추천·성장 예측이 아닙니다. 실제 사례는 인용 범위 안에서만 다룹니다. 실제 Instagram 계정 로그인·게시·유료 API 호출을 검증한 교재가 아닙니다.</p><p>테마·완료 체크·실습 진행 및 본인이 입력한 게시물 주소·14장 변경 입력은 이 브라우저의 localStorage에 저장합니다. 서버로 전송하지 않습니다. 실습 E2E와 실험실에서 해당 입력을 삭제할 수 있고 저장 차단 시 계산·읽기는 계속 됩니다.</p></section>
<section id="updates" class="chapter-block"><h2>업데이트 기록</h2><dl><dt>2026-10-26 · 문체 개편</dt><dd>이론 1~14장과 실습 0~10·전체 진행표를 질문과 직답 중심으로 개편하고, 현재 도구·용어·본문 인용 출처를 맞췄습니다.</dd><dt>2026-10-26 · 실습편 추가</dt><dd>이론/실습 두 트랙과 실습 0~10·E2E 진행 기록을 추가했습니다. 미확인 앱 메뉴는 공식 도움말과 확인 공백을 표시합니다. 공개 URL 준비·로컬 토큰 설정을 키트에 추가했으며 실제 로그인·게시를 검증하지 않았습니다.</dd><dt>2026-10-26 · 부록 통합</dt><dd>2~14장 공통 상태·메타·이동 통합, 15장 실험실, 16장 용어집, 인용 출처와 표지 샘플을 추가했습니다. 1장 대기 문장을 조사 근거와 미확인 범위로 대체했습니다.</dd><dt>2026-10-26 · 앞선 제작·집필</dt><dd>오프라인 스타터 키트와 1~14장 원고·모형, 초기·확장 조사 기록을 통합 기반으로 사용했습니다. 세부 검증은 저장소 docs/results의 단계별 결과 기록을 따릅니다.</dd></dl></section>'''
    (SITE/'credits.html').write_text(shell('credits','출처·크레딧','근거를 찾을 수 있고, 확인하지 못한 범위도 읽을 수 있도록.',content))
    return len(entries)


def lab(entries):
    fallback=''.join(f'<li><a href="chapters/{s["slug"]}.html#{s["id"]}">{s["chapter"]}장 · {E(s["title"])}</a></li>' for s in entries if s['chapter']!=15)
    content='''<p class="note">장별 그림과 입력 도구를 한곳에서 골라 만져 보세요. 원본 장의 도구와 가정 설명을 그대로 불러옵니다. Tab으로 입력에 들어가고 방향키·Enter·Space로 조작합니다.</p><nav class="tool-shortcuts" aria-label="새로 만져 볼 도구"><a href="chapters/03-revenue.html#ledger-sim">돈의 네 갈래</a><a href="chapters/07-cards.html#ch7-sim">문안 카드 편집</a><a href="chapters/08-reels.html#ch8-sim">릴스 타임라인</a><a href="chapters/10-publishing.html#publishing-sim">게시 단계</a><a href="chapters/12-safety.html#safety-sim">증거 검수</a></nav><div class="filter-row"><label>실험 선택 <select id="sim-picker"><option value="month-scenario">15장 · 내 계정 한 달 시나리오</option></select></label></div><p><a id="sim-original" href="chapters/14-plan.html#simulator">원본 장에서 전체 맥락 읽기 →</a></p><div class="lab-stage"><iframe class="lab-frame" id="sim-frame" title="선택한 원본 장의 시뮬레이터" hidden></iframe>
<section id="month-scenario" class="simulator" aria-labelledby="month-title"><div class="sim-heading"><h2 id="month-title">내 계정 한 달 시나리오</h2><span class="model-badge">교육용 가정 모형</span></div><div class="sim-body"><p>수익 경로와 독자를 점검한 뒤, 14장에서 바꾼 시간 계획을 읽어 보세요.</p><div class="month-grid"><article class="month-card"><h3>4장 · 내 기획 점검</h3><p>독자·소개·제안 질문에 빠진 항목을 찾습니다.</p><a href="chapters/04-niche.html#niche-sim">기획 점검 열기</a></article><article class="month-card"><h3>3장 · 돈의 네 갈래</h3><p>돈이 들어오는 경로를 골라 비용을 뺀 금액을 계산합니다.</p><a href="chapters/03-revenue.html#ledger-sim">돈의 흐름 열기</a></article><article class="month-card"><h3>14장 · 30일 계획</h3><p data-month-plan>1독자·소개·제안 질문에 빠진 항목을 찾습니다.</p><a href="chapters/14-plan.html#planner-sim">계획 바꾸기</a></article><article class="month-card"><h3>가정을 읽는 법</h3><p>3·4장 입력은 저장하지 않습니다. 14장 시간 계획은 직접 바꾼 입력만 이어 봅니다. 계획한 시간은 실제 완료 기록이 아닙니다. 빈칸·무효 입력은 0으로 추정하지 않습니다.</p><button type="button" data-refresh-month>저장한 입력 다시 읽기</button><button type="button" data-clear-month>저장한 시간 계획·이전 입력 삭제</button><p data-month-storage role="status"></p></article></div></div><p class="sim-assumptions">초기 예시값은 가져오지 않고, 독자가 변경한 14장 입력과 계산 결과만 이어 씁니다. 브라우저를 바꾸거나 저장을 차단하면 전달되지 않을 수 있습니다. 삭제는 테마·완료 체크를 지우지 않습니다.</p></section></div>
<details class="home-section"><summary>원본 도구 전체 목록 · 직접 열기</summary><ol>'''+fallback+'''</ol></details><noscript><p class="note">선택·요약은 자바스크립트가 필요합니다. 위 원본 도구 목록에서 각 장의 본문과 가정을 읽으세요.</p></noscript>'''
    scripts='<link rel="stylesheet" href="assets/interactions.css"><script src="assets/catalog.js" defer></script><script src="assets/sim/common.js" defer></script><script src="assets/lab.js" defer></script>'
    (SITE/'lab.html').write_text(shell('lab','자동화 실험실','한 번에 하나씩 바꾸고, 결과보다 가정을 먼저 읽어 보세요.',content,scripts))


if __name__ == '__main__':
    entries=catalog()
    print(f'도구 {len(entries)}개, 용어 {glossary()}개, 인용 출처 {credits()}개')
    lab(entries)
