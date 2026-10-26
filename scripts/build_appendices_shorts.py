"""ShortsBook 원본 도구·용어 인계·실제 인용을 정적 부록으로 모은다."""
import html
import json
import re
from pathlib import Path
import build_appendices as shared
from build_appendices import Document, nodes, text, has_class

ROOT = Path(__file__).resolve().parents[1]
E = html.escape


def catalog(site):
    entries = []
    for path in sorted((site / 'chapters').glob('*.html')):
        doc = Document(path.read_text()).root
        body = next((n for n in nodes(doc) if n.tag == 'body'), None)
        if not body or not body.attrs.get('data-chapter-number'):
            continue
        for section in nodes(doc):
            kind = section.attrs.get('data-block')
            if kind not in ('figure', 'simulator'):
                continue
            tools = [n for n in nodes(section) if has_class(n, 'simulator') and n.attrs.get('id')] or [section]
            for tool in tools:
                heading = next((n for n in nodes(tool) if n.tag in ('h2', 'h3')), None)
                if heading is None:
                    heading = next(n for n in nodes(section) if n.tag in ('h2', 'h3'))
                entries.append(dict(chapter=int(body.attrs['data-chapter-number']), slug=path.stem,
                                    id=tool.attrs['id'], title=text(heading).strip(), section=section.attrs['id']))
    return sorted(entries, key=lambda item: item['chapter'])


def cited_sources(site, pages):
    cited = {}
    for path in pages:
        doc = Document(path.read_text()).root
        heading = next((n for n in nodes(doc) if n.tag == 'h1'), None)
        label = text(heading).strip() if heading else path.stem
        used = {m[1].upper() for n in nodes(doc) if n.tag == 'a'
                for m in [re.search(r'#source-(y\d{3})$', n.attrs.get('href', ''), re.I)] if m}
        for sid in sorted(used):
            cited.setdefault(sid, []).append((path.relative_to(site).as_posix(), label))
    return cited


def shell(slug, title, intro, content, scripts=''):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)} | ShortsBook</title><link rel="icon" href="data:,"><link rel="stylesheet" href="assets/book.css"><link rel="stylesheet" href="assets/shorts.css"><script src="assets/book.js" defer></script><script src="assets/sim/common.js" defer></script>{scripts}</head>
<body data-chapter="{slug}"><a class="skip-link" href="#main">본문으로 건너뛰기</a><header data-site-header><a href="index.html">ShortsBook</a></header><main id="main" class="appendix-main"><p class="kicker">ShortsBook / 도구와 자료</p><h1>{E(title)}</h1><p class="lead">{intro}</p>{content}<nav data-chapter-pager aria-label="이전·다음 장"></nav></main><footer data-site-footer></footer></body></html>\n'''


# 같은 뜻의 인계 표기는 같은 항목으로 합친다. 인증 토큰과 AI 비용 단위는 분리한다.
ALIASES = {
    '출력·내보내기': ['출력', '내보내기'], 'Content ID 소유권 주장': ['Content ID 소유권 주장', 'Content ID 주장'],
    '화면에 구운 자막': ['화면에 구운 자막', '번인 자막'], 'fps·프레임': ['fps', '프레임'],
    'OAuth·토큰': ['OAuth', '토큰'], '모델 / 서비스': ['모델', '서비스'],
    '기준 그림 / 참조 이미지': ['기준 그림', '참조 이미지', '기준 이미지'],
    '토큰 / MTok': ['MTok'],
}
IDS = dict(zip(
    ['쇼츠','편집 프로젝트','MP4','출력','훅','대본','자막','내레이션','TTS','트랙','뮤트','솔로','Content ID 소유권 주장','저작권 위반 경고','저작자 표시','안전 영역','컷','재생 헤드','화면에 구운 자막','SRT','해상도','fps','코덱','비트레이트','템플릿','메타데이터','일부 공개','비공개 잠금','유효 조회수','평균 조회율','시청 지속률 곡선','양산형 콘텐츠','시간 예산','드라이런','재개 가능 업로드','청크','토큰','샷','기준 이미지','크레딧','타임라인','프레임','OAuth','모델','서비스','이미지→영상','MTok','구독료 배분액'],
    ['shorts','project','mp4','export','hook','script','captions','narration','tts','track','mute','solo','content-id','copyright-strike','attribution','safe-area','cut','playhead','burn-in','srt','resolution','fps','codec','bitrate','template','metadata','unlisted','private-lock','engaged-views','average-percentage','retention','inauthentic','time-budget','dry-run','resumable-upload','chunk','auth-token','shot','reference-image','credits','timeline','frame','oauth','model','service','image-to-video','mtok','allocated-cost']))


def glossary(site, pages):
    terms, canonical = {}, {}
    for phase in ('a', 'b', 'c', 'k', 'p', 'ai'):
        for line in (ROOT / f'docs/results/phase-Y4{phase}-glossary.md').read_text().splitlines():
            fields = [f.strip() for f in line.split('|')[1:-1]]
            if not line.startswith('|') or not fields or fields[0] in ('용어', '제안 ID') or fields[0].startswith('---'):
                continue
            name, description = fields[1:3] if phase == 'b' else fields[:2]
            if name in ('번인 자막',): name = '화면에 구운 자막'
            if name == 'Content ID 주장': name = 'Content ID 소유권 주장'
            if name in ('기준 이미지', '기준 그림 / 참조 이미지'): name = '기준 그림 / 참조 이미지'
            for alias in ALIASES.get(name, [name]):
                primary = {'내보내기':'출력','참조 이미지':'기준 이미지','기준 그림':'기준 이미지','Content ID 주장':'Content ID 소유권 주장','번인 자막':'화면에 구운 자막'}.get(alias, alias)
                id_ = IDS[primary]
                if id_ not in canonical:
                    canonical[id_] = dict(id=id_, name=primary, description=description)
                terms[alias] = canonical[id_]
    # 결합 요청의 서로 다른 개념을 각각 설명한다.
    for id_, description in {
        'fps':'1초에 보여 주는 화면 수입니다. 30fps는 1초에 30장입니다.',
        'frame':'영상의 한 장 화면입니다. 프레임 단위로 이동하면 자막의 시작과 끝을 확인하기 쉽습니다.',
        'oauth':'비밀번호를 다른 도구에 넘기지 않고 허용할 작업을 선택하는 로그인 방식입니다.',
        'auth-token':'로그인에서 허용한 권한을 증명하는 비밀 파일입니다. AI 사용량을 세는 토큰과 다릅니다.',
        'model':'AI 결과를 생성하는 엔진입니다. 같은 서비스에서 여러 모델을 고를 수 있습니다.',
        'service':'모델을 사용하는 앱이나 웹사이트입니다. 구독료와 모델 API 요금은 다를 수 있습니다.',
        'mtok':'AI가 글 등을 처리하는 작은 단위인 토큰 100만 개입니다. 글자 수·낭독 초와 다르며 로그인 토큰과도 다릅니다.',
    }.items(): canonical[id_]['description'] = description
    # 공유 파서는 코드·각주·링크·제목을 건드리지 않고 책 전체 첫 사용에만 링크를 넣는다.
    shared.SITE = site
    shared.CHAPTER_NUMBERS = {p.stem: int(re.search(r'data-chapter-number="(\d+)"', p.read_text())[1]) for p in pages if p.parent.name == 'chapters'}
    for path in pages:
        source = re.sub(r'<a [^>]*\bdata-term="[^"]*"[^>]*>(.*?)</a>', r'\1', path.read_text(), flags=re.S)
        linker = shared.TermLinks(source, dict(sorted(terms.items(), key=lambda item: -len(item[0]))), path)
        for start, end, replacement in reversed(linker.edits):
            if path.parent == site:
                replacement = replacement.replace('href="../glossary', 'href="glossary')
            source = source[:start] + replacement + source[end:]
        path.write_text(source)
    entries = []
    for term in sorted(canonical.values(), key=lambda t: t['name'].casefold()):
        backlink = ''
        if term.get('page'):
            path = site / term['page']
            doc = Document(path.read_text()).root
            number = next((n.attrs['data-chapter-number'] for n in nodes(doc) if 'data-chapter-number' in n.attrs), None)
            title = next((text(n) for n in nodes(doc) if n.tag == 'h1'), path.stem)
            label = f'이론 {number}장 · {title}' if number else title
            backlink = f'<p><a href="{term["page"]}">처음 설명한 곳: {E(label)} →</a></p>'
        entries.append(f'<article class="glossary-entry" id="{term["id"]}" data-glossary-entry data-search="{E(term["name"]+" "+term["id"]+" "+term["description"],quote=True)}"><h2>{E(term["name"])}</h2><p>{E(term["description"])}</p>{backlink}</article>')
    content = '<label>용어·설명 검색 <input id="term-search" type="search" placeholder="예: 자막, TTS, 토큰"></label><p id="term-count" role="status"></p><div class="glossary-grid">'+''.join(entries)+'</div><noscript><p>브라우저의 찾기로 전체 용어를 검색하세요.</p></noscript>'
    (site / 'glossary.html').write_text(shell('glossary','용어집','어려운 말은 뜻을 확인하고 처음 나온 장으로 돌아가세요.',content,'<script src="assets/glossary.js" defer></script>'))
    return len(entries)


def credits(site, pages):
    sources = {}
    for line in (ROOT / 'research-shorts/SOURCES.md').read_text().splitlines():
        fields = [f.strip() for f in line.split('|')[1:-1]]
        if not fields or not (sid := re.search(r'\bY\d{3}\b',fields[0])): continue
        link = re.search(r'\[(.*?)\]\((.*?)\)',fields[1])
        if link: sources[sid[0]] = (link[1], link[2], fields[2:6])
    for sid, title, body in re.findall(r'### (Y\d{3})\. (.*?)\n(.*?)(?=\n<a id=|\Z)', (ROOT / 'research-shorts/SOURCES.md').read_text(), re.S):
        meta = dict(re.findall(r'^- ([^:]+): (.*)$', body, re.M))
        sources[sid] = (title, meta['URL'], [meta.get(key, '미표기') for key in ('기관', '게시·갱신일', '접근일', '신뢰도')])
    cited = cited_sources(site, pages)
    entries = []
    for sid, links in sorted(cited.items()):
        title, url, meta = sources[sid]
        meta = [re.sub(r'[（(][^()（）]*Hermes[^()（）]*[)）]', '', value) for value in meta]
        backlink = ' · '.join(f'<a href="{path}#source-{sid.lower()}">{E(label)}</a>' for path,label in links)
        entries.append(f'<li class="source-entry" id="source-{sid.lower()}"><h3>{sid} · <a href="{E(url,quote=True)}">{E(title)}</a></h3><p>기관: {E(meta[0])} · 게시·갱신일: {E(meta[1])}<br>확인일: {E(meta[2])} · 자료 구분: {E(meta[3])}</p><p>인용한 곳: {backlink}</p></li>')
    content = f'''<p>2026년 10월 조사 기준 · 접근일 2026-10-26. 본문에서 실제 연결한 Y번호 {len(entries)}개만 모았습니다. 번호는 원래 조사 목록을 유지해 중간이 비어 있습니다. A는 공식 문서·제공자, B는 업계 참고 자료입니다.</p><section id="sources"><h2>인용 출처</h2><ul class="source-list">{''.join(entries)}</ul></section>
<section class="home-section" id="licenses"><h2>폰트·키트·그림</h2><p>공통 조판·테마·퀴즈는 같은 프로젝트의 ReelsBook 자산을 재사용했습니다. 웹 글꼴은 Pretendard v1.3.9이며 <a href="assets/licenses/Pretendard-OFL.txt">OFL 고지</a>를 따릅니다. 키트 샘플은 자체 타이틀·무음·대본 기반 자막을 넣은 가상 영상입니다. <a href="assets/samples/LICENSE.txt">키트 MIT 고지</a>와 <a href="assets/licenses/NotoSansKR-OFL.txt">샘플 글꼴 Noto Sans KR의 OFL 고지</a>를 제공합니다.</p></section>
<section class="home-section" id="ai-example-credits"><h2>AI 생성 예시와 가상 연습</h2><p>도윤·서진·연습 계정과 계산 입력은 가상입니다. 로봇 기준 그림·고개를 기울인 장면 카드·실습의 종이 로봇은 내장 이미지 생성으로 만든 정지 그림이며 실존 인물·브랜드·로고가 없습니다. <a href="prompts.html#actual-image-prompts">두 그림의 실제 프롬프트·참조 관계</a>와 <a href="practice/05-scenes.html#image">실습 그림의 프롬프트</a>를 읽을 수 있습니다. 도식은 직접 그렸습니다.</p><p>계산·타임라인은 공개한 가정으로 비교하는 연습입니다. 테마·실습 체크·게시 주소는 이 브라우저에 저장하며 서버로 보내지 않습니다. <a href="practice/e2e.html">전체 체크리스트</a>에서 실습 기록을 지울 수 있습니다.</p></section><p><a href="index.html#contents">전체 목차로 →</a></p>'''
    (site / 'credits.html').write_text(shell('credits','출처·크레딧','근거 원문과 인용한 장을 함께 확인합니다.',content))
    return len(entries)


def lab(site, entries):
    links = ''.join(f'<li><a href="chapters/{t["slug"]}.html#{t["id"]}">{t["chapter"]}장 · {E(t["title"])}</a></li>' for t in entries)
    options = ''.join(f'<option value="{t["slug"]}:{t["id"]}">{t["chapter"]}장 · {E(t["title"])}</option>' for t in entries)
    content = f'''<p class="note">모든 장의 그림과 도구 {len(entries)}개입니다. 원본 장의 도구·설명·가정을 그대로 불러옵니다. Tab으로 들어가고 방향키·Enter·Space로 조작하세요. 소리는 재생 버튼을 눌러야 나옵니다.</p><label>실험 선택 <select id="sim-picker">{options}</select></label><p><a id="sim-original" href="chapters/{entries[0]['slug']}.html#{entries[0]['id']}">원본 장에서 전체 맥락 읽기 →</a></p><div class="lab-stage"><iframe class="lab-frame" id="sim-frame" title="선택한 원본 장의 도구" hidden></iframe></div><details class="home-section"><summary>원본 도구 전체 목록 · 직접 열기</summary><ol>{links}</ol></details><noscript><p>위 원본 도구 목록에서 도구와 가정을 읽으세요.</p></noscript>'''
    (site / 'assets/catalog.js').write_text('// 원본 HTML에서 생성. 도구 계산 로직은 복제하지 않습니다.\nwindow.ShortsCatalog = Object.freeze('+json.dumps(entries,ensure_ascii=False,indent=2)+');\n')
    (site / 'lab.html').write_text(shell('lab','영상 실험실','한 번에 한 가지를 바꾸고 원본 장의 가정과 함께 비교하세요.',content,'<script src="assets/catalog.js" defer></script><script src="assets/lab.js" defer></script>'))


def build():
    site = ROOT / 'site-shorts'
    chapters = sorted(p for p in (site / 'chapters').glob('*.html') if p.name != 'coming-soon.html')
    practice = sorted(p for p in (site / 'practice').glob('*.html') if p.name != 'coming-soon.html')
    pages = chapters + practice + [site / 'prompts.html', site / 'ai-models.html']
    entries = catalog(site)
    count = glossary(site, pages)
    sources = credits(site, pages)
    lab(site, entries)
    print(f'ShortsBook: 도구 {len(entries)}개, 용어 {count}개, 실제 인용 출처 {sources}개')
