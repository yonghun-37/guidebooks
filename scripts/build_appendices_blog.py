"""BlogBook 원본 도구·프롬프트·용어 요청·실제 B 인용을 모은다. 외부 패키지 불필요."""
import html
import json
import re
import shutil
import zipfile
from pathlib import Path
from build_appendices import Document, nodes, text, has_class, TermLinks

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site-blog'
E = html.escape


def shell(slug, title, intro, content, scripts=''):
    attr = 'data-chapter' if slug in {'lab', 'glossary'} else 'data-appendix'
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)} | BlogBook</title><meta name="description" content="AI로 쓰는 블로그 수익화 입문서의 도구와 자료입니다."><link rel="icon" href="data:,"><link rel="stylesheet" href="assets/book.css"><link rel="stylesheet" href="assets/blog.css"><script defer src="assets/catalog.js"></script><script defer src="assets/book.js"></script><script defer src="assets/common.js"></script>{scripts}</head>
<body {attr}="{slug}"><a class="skip-link" href="#main">본문으로 건너뛰기</a><header data-site-header><a href="index.html">BlogBook</a></header><main id="main" class="appendix-main"><p class="kicker" data-chapter-kicker>BlogBook · 도구와 자료</p><h1 data-chapter-title>{E(title)}</h1><p class="lead">{intro}</p>
{content}
<nav data-chapter-pager aria-label="이전·다음 장"></nav></main><footer data-site-footer></footer></body></html>\n'''


def sources():
    result = {}
    for sid, title, body in re.findall(r'## (B\d{3})\. (.*?)\n(.*?)(?=\n<a id=|\Z)', (ROOT/'research-blog/SOURCES.md').read_text(), re.S):
        url = re.search(r'^- URL: \[.*?\]\((.*?)\)', body, re.M)
        if not url:
            raise ValueError(sid)
        publisher = re.search(r'^- 발행 주체: (.*)', body, re.M)
        date = re.search(r'^- 게시·갱신·시행: (.*)', body, re.M)
        result[sid] = dict(title=title, url=url[1], publisher=publisher[1], date=date[1])
    return result


def catalog():
    entries = []
    for path in sorted((SITE/'chapters').glob('[0-9]*.html')):
        doc = Document(path.read_text()).root
        for tool in nodes(doc):
            if not has_class(tool, 'simulator') or tool.tag == 'section' and tool.attrs.get('data-block'):
                continue
            heading = next((n for n in nodes(tool) if n.tag in ('h2', 'h3')), None)
            entries.append(dict(chapter=int(path.name[:2]), slug=path.stem, id=tool.attrs['id'], title=tool.attrs.get('aria-label') or text(heading).strip(), section='simulator'))
    assert len(entries) == 13, entries
    (SITE/'assets/catalog.js').write_text('// scripts/build_appendices.py --site site-blog  · 원본에서 생성\nwindow.BlogCatalog = Object.freeze('+json.dumps(entries, ensure_ascii=False, indent=2)+');\n')
    return entries


def lab(entries):
    options = ''.join(f'<option value="{t["slug"]}:{t["id"]}">{t["chapter"]}장 · {E(t["title"])}</option>' for t in entries)
    links = ''.join(f'<li><a href="chapters/{t["slug"]}.html#{t["id"]}">{t["chapter"]}장 · {E(t["title"])}</a></li>' for t in entries)
    first = entries[0]
    content = f'''<p>Tab으로 도구에 들어가고 방향키·Enter·Space로 조작하세요. 계산·비교·시간표의 가정은 원본과 같습니다. 입력은 현재 화면에서만 쓰며, 수입·검색 순위를 예측하지 않습니다.</p>
<label for="sim-picker">해 볼 도구 · 전체 {len(entries)}개</label><select id="sim-picker" class="url-field">{options}</select>
<p><a id="sim-original" href="chapters/{first['slug']}.html#{first['id']}">원본 장에서 전체 설명 읽기 →</a></p>
<iframe class="book-frame" id="sim-frame" title="{E(first['title'])}" src="chapters/{first['slug']}.html?embed={first['id']}"></iframe>
<details class="home-section"><summary>원본 도구 전체 목록</summary><ol>{links}</ol></details><noscript><p>도구를 바꾸려면 위 목록에서 원본을 여세요.</p></noscript>'''
    (SITE/'lab.html').write_text(shell('lab', '블로그 실험실', '13개 장의 도구를 한곳에서 골라 직접 바꿔 보세요.', content, '<script defer src="assets/lab.js"></script>'))


def prompts():
    content = '''<p>먼저 본인 자료로 빈칸을 채우고 ChatGPT·Gemini·Claude의 대화창에 넣으세요. 받은 답은 원문·사진·내 메모와 대조합니다. 프롬프트는 AI에게 맡길 일·자료·출력 모양을 적은 요청문입니다.</p>
<nav class="route-ribbon" aria-label="작업별 프롬프트"><a href="#info">정보 글</a><a href="#review">실사용 후기</a><a href="#trip">여행 기록</a><a href="#human">교정</a><a href="#practice">제목·개요·초안</a><a href="#image">이미지</a><a href="#repeat">반복·분석·계획</a></nav>
<p>요청문은 해당 장의 원본과 같습니다. 자료 속 전화번호·계좌·타인의 개인정보는 지운 뒤 넣으세요.</p>'''
    count = 0
    groups = [
        ('info', '정보·지원 제도 글', 'chapters/06-writing.html', 'info', ['근거표·개요 준비', '검수한 자료로 초안 쓰기'], '청년 지원금 무조건 받는 법을 알아서 써 줘.', '대상·기간·지역을 원문에서 확인하고 근거표에 넣습니다. 없는 혜택은 만들지 않습니다.'),
        ('review', '실제 사용한 생활 가전 후기', 'chapters/06-writing.html', 'review', ['내 관찰 정리', '관계 표시와 후기 초안'], '써 보지 않은 제습기를 한 달 쓴 것처럼 칭찬해 줘.', '직접 관찰·미측정·공식 사양을 나눕니다. 단점과 제공 관계도 남깁니다.'),
        ('trip', '당일치기 여행 기록', 'chapters/06-writing.html', 'trip', ['사진·동선 정리', '내 표현으로 여행 글'], '인기 여행지에 다녀온 감동 후기를 만들어 줘.', '사진에 있는 장면·내 선택 이유만 씁니다. 없던 방문과 감정은 넣지 않습니다.'),
        ('human', '원뜻을 지키는 교정', 'chapters/06-writing.html', 'human', ['수정 전·후·이유 받기'], '전문가처럼 확신에 차게 다 고쳐 줘.', '수치·고유명사·경험은 유지하고 긴 문장과 반복만 줄입니다.'),
        ('practice', '자료표 → 제목·개요 → 초안', 'practice/04-draft.html', None, ['정보 글 재료', '후기 재료', '여행 재료', '제목·개요', '초안'], '지원금 정보를 검색해서 바로 완성해 줘.', '공식 자료와 내 메모를 먼저 채우고 개요를 고릅니다. 초안의 모든 주장을 다시 대조합니다.'),
        ('image', '썸네일 배경과 이미지 기록', 'practice/05-images.html', None, ['글자 없는 삽화 배경', '권리·AI 역할 기록'], '내가 지원금을 받은 증거 사진과 공식 도장을 만들어 줘.', '개념을 설명하는 삽화를 만들고 제목은 편집기의 텍스트로 넣습니다. 실제 신청 증거로 쓰지 않습니다.'),
    ]
    for id_, title, filename, section_id, labels, bad, good in groups:
        doc = Document((SITE/filename).read_text()).root
        section = next(n for n in nodes(doc) if n.attrs.get('id') == section_id) if section_id else doc
        pres = [n for n in nodes(section) if n.tag == 'pre']
        assert len(pres) == len(labels), (filename, len(pres))
        content += f'<section class="home-section prompt-group" id="{id_}"><h2>{title}</h2><p><a href="{filename}'+(f'#{section_id}' if section_id else '')+'">입력·출력·사용법을 원본에서 읽기 →</a></p>'
        for i, (pre, label) in enumerate(zip(pres, labels), 1):
            count += 1
            content += f'<h3>{E(label)}</h3><div class="code-box" data-prompt-origin="{filename}#{pre.attrs.get("id", section_id or "main")}" data-prompt-index="{i-1}"><pre><code>{E(text(pre))}</code></pre></div>'
        content += f'<figure class="blog-figure"><div class="prompt-compare"><div><h3>나쁜 요청</h3><p>{E(bad)}</p></div><div><h3>좋은 요청의 기준</h3><p>{E(good)}</p></div></div><figcaption>내 자료·제약·출력 모양을 지정하면 사람이 확인할 자리가 남습니다.</figcaption></figure></section>'
    content += '<section class="home-section" id="repeat"><h2>반복·분석·정책·30일 계획</h2><p>첫 글을 낸 뒤에는 본인 기록을 넣어 다음 글의 틀과 계획을 만드세요. 정책 판단과 사실 확인은 원문에서 마칩니다.</p>'
    for filename, id_, title in [('10-automation','template-prompt','글쓰기 양식'), ('11-analytics','analysis-prompt','숫자 읽기'), ('12-policy','policy-prompt','표시·권리 질문'), ('13-plan','plan-prompt','30일 계획')]:
        doc = Document((SITE/f'chapters/{filename}.html').read_text()).root
        node = next(n for n in nodes(doc) if n.attrs.get('id') == id_)
        code = next((n for n in nodes(node) if n.tag == 'code'), node)
        count += 1
        content += f'<h3>{title}</h3><p><a href="chapters/{filename}.html#{id_}">원본과 사용법 →</a></p><div class="code-box" data-prompt-origin="chapters/{filename}.html#{id_}"><pre><code>{E(text(code))}</code></pre></div>'
    content += '</section><p><a href="practice/04-draft.html">실습 4에서 자료를 채우며 시작하기 →</a> · <a href="ai-models.html">어떤 도구를 얼마에 쓰나 →</a></p>'
    (SITE/'prompts.html').write_text(shell('prompts', '프롬프트 모음', '정보 글·실사용 후기·여행 기록을 내 자료로 완성하는 요청문입니다.', content))
    return count


# 인계 표의 서로 다른 표 형식은 여기서만 해석한다. 같은 ID는 첫 정의를 유지한다.
B5_IDS = dict(zip(['프롬프트','대체 텍스트','소유확인','속성','사이트맵','색인','드라이런','터미널','경로','가상환경','Markdown','JSON','API','OAuth','토큰','애플리케이션 비밀번호'], ['prompt','alt-text','ownership','property','sitemap','indexing','dry-run','terminal','path','venv','markdown','json','api','oauth','token','application-password']))


def glossary(pages):
    terms = {}
    def add(id_, name, desc, page):
        terms.setdefault(id_, dict(id=id_, name=name, description=desc, page=page))
    for id_, name, desc in [('uv','순방문자(UV)','정한 기간 안에서 중복을 뺀 방문자입니다. 일별 합과 월 순방문자를 구별합니다.'), ('pv','페이지뷰(PV)','페이지가 열린 횟수입니다. 광고 보고서의 집계 정의도 확인합니다.'), ('rpm','페이지 RPM','같은 기간의 예상 광고수입을 광고 페이지뷰로 나누고 1,000을 곱한 값입니다.')]:
        add(id_, name, desc, 'chapters/02-revenue.html#principle')
    for phase in ['B4a','B4b','B4c','B5']:
        for line in (ROOT/f'docs/results/phase-{phase}-glossary.md').read_text().splitlines():
            if not line.startswith('|'): continue
            f = [x.strip() for x in line.split('|')[1:-1]]
            if len(f)<3 or f[0].startswith('-'): continue
            if phase == 'B4a':
                m = re.search(r'`([\w-]+)`',f[0]); loc = re.search(r'(\d+)장 #([\w-]+)',f[2])
                if not m or not loc: continue
                id_,name,desc=m[1],f[0].split(' `')[0],f[1]
                slug=next((SITE/'chapters').glob(f'{int(loc[1]):02d}-*.html')).name
                page=f'chapters/{slug}#{loc[2]}'
            elif phase == 'B4b':
                if not re.fullmatch(r'[a-z-]+',f[0]): continue
                id_,name,desc,page=f[0],f[1],f[2],'chapters/'+f[3].strip('`')
            elif phase == 'B4c':
                if not re.fullmatch(r'[a-z-]+',f[0]): continue
                id_,name,desc=f[:3]; page=re.search(r'`([^`]+)`',f[3])[1]
            else:
                if f[0] not in B5_IDS: continue
                id_,name,desc=B5_IDS[f[0]],f[0],f[1]
                num=int(re.search(r'실습 (\d+)',f[2])[1]); page='practice/'+next((SITE/'practice').glob(f'{num:02d}-*.html')).name
                if id_ == 'token': name='인증 토큰'
            add(id_,name,desc,page)
    add('ai-token','AI 사용량 토큰','AI가 글을 처리할 때 나누는 조각입니다. 글자 수와 같지 않으며, 입력과 출력 단가가 다릅니다. 인증용 비밀값과 구분합니다.','ai-models.html#billing')
    # 원본의 이전 용어 링크를 풀고, 첫 본문 사용에만 일치하는 data-term을 만든다.
    link_terms = {t['name']: dict(t) for t in terms.values()}
    for name in ['순방문자(UV)','페이지뷰(PV)']:
        t=link_terms.pop(name);link_terms['UV' if name.startswith('순') else 'PV']=t
    for p in pages:
        source=re.sub(r'<a [^>]*\bdata-term="[^"]*"[^>]*>(.*?)</a>',r'\1',(p).read_text(),flags=re.S)
        linker=TermLinks(source,link_terms,p,site=SITE,label=lambda path: path.stem)
        for start,end,replacement in reversed(linker.edits): source=source[:start]+replacement+source[end:]
        p.write_text(source)
    cards=''
    for t in sorted(terms.values(),key=lambda t:t['name'].lower()):
        cards+=f'<article class="glossary-entry" id="{t["id"]}" data-glossary-entry data-search="{E(t["name"]+" "+t["id"]+" "+t["description"],quote=True)}"><h2>{E(t["name"])}</h2><p>{E(t["description"])}</p><p><a href="{t["page"]}">본문에서 예와 함께 읽기 →</a></p></article>'
    content='<label for="term-search">용어·뜻 검색</label><input class="url-field" id="term-search" type="search" placeholder="예: 색인, API, 토큰"><p id="term-count" role="status"></p><div class="glossary-grid">'+cards+'</div><noscript><p>브라우저의 찾기로 용어를 찾으세요.</p></noscript>'
    (SITE/'glossary.html').write_text(shell('glossary','용어집','처음 만나는 말의 뜻과 예시를 함께 읽습니다.',content,'<script defer src="assets/glossary.js"></script>'))
    return len(terms)


def page_label(path):
    if path.startswith('chapters/'):
        return f'이론 {int(Path(path).name[:2])}장'
    if path.startswith('practice/'):
        name=Path(path).stem
        return f'실습 {int(name[:2])}' if name[:2].isdigit() else '한 편 완성 체크리스트'
    return {'prompts.html':'프롬프트 모음','ai-models.html':'모델·사용처·비용'}[path]


def credits(pages):
    source_map=sources(); cited={}
    for p in pages:
        doc=Document(p.read_text()).root
        for n in nodes(doc):
            if n.tag!='a': continue
            m=re.search(r'#source-(b\d{3})$',n.attrs.get('href',''),re.I)
            if m:
                sid=m[1].upper(); assert sid in source_map,sid
                cited.setdefault(sid,set()).add(p.relative_to(SITE).as_posix())
    entries=''
    for sid,paths in sorted(cited.items()):
        s={k: re.sub(r'Hermes\d*[^ ·]*', '', v).replace('**','').strip(' ·') for k,v in source_map[sid].items()}
        backlinks=' · '.join(f'<a href="{p}#source-{sid.lower()}">{E(page_label(p))}</a>' for p in sorted(paths))
        entries+=f'<li class="source-entry" id="source-{sid.lower()}"><h3>[{sid}] <a href="{E(s["url"],quote=True)}">{E(s["title"])}</a></h3><p>{E(s["publisher"])} · {E(s["date"])}</p><p>인용 위치: {backlinks}</p></li>'
    content=f'''<p>2026년 10월 조사 기준. 이론·실습·부록에서 실제 인용한 B번호 {len(cited)}개만 모았습니다. 번호가 빠진 곳은 현재 본문에서 인용하지 않은 자료입니다. A는 공식 기관·사업자, B는 독립 조사·튜토리얼, C는 개인 경험 자료입니다.</p><ul class="source-list">{entries}</ul>
<section class="home-section" id="production"><h2>제작과 예시</h2><p>수아·태오와 블로그 ‘퇴근 후 생활 정보’는 가상입니다. 계산 도구는 공개한 가정에 따른 연습입니다. 가상 수익·경험을 실제 성과로 옮겨 쓰지 마세요.</p><p>HTML·CSS·JavaScript와 SVG 도식은 이 저장소에서 작성했습니다. 참고 사이트에서는 학습 구조와 이동 방식만 참고했습니다. 글꼴은 Pretendard, SIL Open Font License입니다. <a href="assets/licenses/Pretendard-OFL.txt">동봉 라이선스</a></p><p>AI 생성 예시: <a href="assets/img/ai-examples/support-desk.webp">준비물 책상</a>·<a href="assets/img/ai-examples/weekend-river.webp">주말 강변</a>은 <a href="chapters/07-images.html#generate">7장의 실제 프롬프트</a>, <a href="practice/images/support-background.webp">썸네일 배경</a>은 <a href="practice/05-images.html#image-prompt">실습 5의 요청문</a>과 함께 읽으세요. 내장 이미지 생성 기능으로 제작한 설명용 삽화이며 실제 체험의 증거 사진이 아닙니다.</p><p>키트 샘플은 <a href="samples/blog-kit/preview.html">동봉 미리보기</a>에서 읽습니다. 샘플을 그대로 실제 체험담으로 게시하지 마세요.</p></section>
<section class="home-section"><h2>기록과 확인 범위</h2><p>테마·실습 체크·공개 주소·작업 메모는 이 브라우저에만 저장합니다. 실습의 <a href="practice/e2e.html">전체 체크리스트</a>에서 진행·주소·메모를 삭제할 수 있습니다. 서버로 전송하지 않습니다.</p><p>계정별 최신 화면·생성 한도·심사·정산은 공식 안내와 본인 계정에서 확인하세요. 이 책의 화면 도식은 실제 서비스 화면 캡처가 아닙니다.</p></section>'''
    (SITE/'credits.html').write_text(shell('credits','출처·크레딧','주장의 원문과 인용 위치, 예시 제작 방식을 확인합니다.',content))
    return len(cited)


def samples():
    """허용 목록의 공개 키트 파일만 배포한다. 비밀값·실행 산출물은 읽지 않는다."""
    kit=ROOT/'blog-kit'
    out=SITE/'samples/blog-kit';out.mkdir(parents=True,exist_ok=True)
    for name in ['preview.html','draft.md','report.md']:
        source=(kit/'samples/rendered'/name).read_text()
        if name.endswith('.html'):
            source=source.replace('<title>', '<link rel="icon" href="data:,"><title>',1)
        (out/name).write_text(source)
    shutil.copyfile(kit/'README.md',out/'README.md')
    shutil.copytree(kit/'samples/rendered/assets',out/'assets',dirs_exist_ok=True)
    files=set(kit.glob('*.py')) | set(kit.glob('*.md'))
    files |= {kit/name for name in ['.env.example','.gitignore','config.example.json','requirements-dev.txt','pytest.ini']}
    files |= set((kit/'tests').glob('*.py'))
    files |= {p for p in (kit/'samples').rglob('*') if p.is_file() and p.suffix in {'.md','.html','.json','.svg'}}
    with zipfile.ZipFile(out/'blog-kit.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            info=zipfile.ZipInfo('blog-kit/'+path.relative_to(kit).as_posix(),date_time=(2026,10,26,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            archive.writestr(info,path.read_bytes())


def build():
    samples();entries=catalog();lab(entries);prompt_count=prompts()
    pages=sorted((SITE/'chapters').glob('[0-9]*.html'))+sorted(p for p in (SITE/'practice').glob('*.html') if p.stem!='pending')+[SITE/'prompts.html',SITE/'ai-models.html']
    terms=glossary(pages);citations=credits(pages)
    print(f'BlogBook 도구 {len(entries)}개, 프롬프트 {prompt_count}개, 용어 {terms}개, 인용 출처 {citations}개')
