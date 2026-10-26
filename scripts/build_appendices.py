#!/usr/bin/env python3
"""원고·연구·인계 표에서 실험실 목록/용어집/출처를 갱신한다. 외부 패키지 불필요."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
CHAPTERS = sorted((SITE / 'chapters').glob('[0-9][0-9]-*.html'))
E = html.escape


def shell(slug, title, intro, content, scripts=''):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} | ReelsBook</title><link rel="icon" href="data:,"><link rel="stylesheet" href="assets/book.css"><script src="assets/book.js" defer></script>{scripts}</head>
<body data-chapter="{slug}"><a class="skip-link" href="#main">본문으로 건너뛰기</a><header data-site-header><a href="index.html">ReelsBook</a></header>
<main id="main" class="appendix-main"><p class="kicker" data-chapter-kicker>ReelsBook / 부록</p><h1 data-chapter-title>{title}</h1><p class="lead">{intro}</p>
{content}
<nav data-chapter-pager aria-label="이전·다음 장"></nav></main><footer data-site-footer></footer></body></html>\n'''


def catalog():
    entries = []
    for p in CHAPTERS:
        text = p.read_text()
        modules = re.findall(r'<script src="\.\./assets/sim/([^"]+)"', text)
        for module in modules:
            for id_ in re.findall(r"ReelsSim.mount\('#([^']+)'", (SITE/'assets/sim'/module).read_text()):
                match = re.search(r'<[^>]+\bid="'+re.escape(id_)+r'"[^>]*>', text)
                assert match, (p, id_)
                section_match = list(re.finditer(r'<section[^>]+id="([^"]+)"',text[:match.start()]))[-1]
                section = section_match[1]
                section_end = text.index('</section>', match.end())
                heading = re.search(r'<h3[^>]*>(.*?)</h3>', text[match.end():section_end], re.S)
                title = heading[1] if heading else re.search(r'<h2[^>]*>(.*?)</h2>', text[section_match.start():match.start()], re.S)[1]
                entries.append(dict(chapter=int(p.name[:2]),slug=p.stem,id=id_,title=html.unescape(re.sub('<[^>]+>','',title)),section=section))
    entries.append(dict(chapter=15,slug='lab',id='month-scenario',title='내 계정 한 달 시나리오',section='month-scenario'))
    (SITE/'assets/catalog.js').write_text('// scripts/build_appendices.py가 원본 장/모듈에서 생성. 계산/HTML 복제 없음.\nwindow.ReelsCatalog = Object.freeze('+json.dumps(entries,ensure_ascii=False,indent=2)+');\n')
    return entries


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
    for p in CHAPTERS:
        def link(match):
            attrs,label = match[1],match[2]
            name = html.unescape(re.sub('<[^>]+>','',label)).strip()
            if name=='공식 API': name='API'
            assert name in terms, (p,name)
            term = terms[name]
            if 'first' not in term: term.update(first=int(p.name[:2]),chapter=p.stem)
            attrs=re.sub(r'href="[^"]*"',f'href="../glossary.html#{term["id"]}"',attrs)
            old=re.search(r'data-term="([^"]*)"',attrs)[1]
            if 'data-term-description=' not in attrs:
                attrs=attrs.replace(f'data-term="{old}"',f'data-term="{term["id"]}" data-term-description="{old}"')
            else: attrs=re.sub(r'data-term="[^"]*"',f'data-term="{term["id"]}"',attrs)
            return '<a '+attrs+'>'+label+'</a>'
        text=re.sub(r'<a ([^>]*\bdata-term="[^"]*"[^>]*)>(.*?)</a>',link,p.read_text(),flags=re.S)
        p.write_text(text)
    korean={'API':'에이피아이','RSS':'알에스에스','JSON':'제이슨','TTS':'티티에스','SRT':'에스알티','2단계 인증':'이단계 인증'}
    entries=[]
    for name,t in sorted(terms.items(),key=lambda item:korean.get(item[0],item[0])):
        assert 'first' in t, name
        entries.append(f'''<article class="glossary-entry" id="{t['id']}" data-glossary-entry data-category="{t['category']}" data-search="{E(name+' '+t['id']+' '+t['description'],quote=True)}"><p class="small">{t['category']}</p><h2>{E(name)}</h2><p>{E(t['description'])}</p><p><a href="chapters/{t['chapter']}.html">처음 나온 {t['first']}장 →</a></p></article>''')
    content='''<div class="filter-row"><label>용어·설명 검색 <input id="term-search" type="search" placeholder="예: 드라이런, API, 현금"></label><label>분류 <select id="term-category"><option value="">전체</option>'''+''.join(f'<option>{c}</option>' for c in categories)+'''</select></label></div><p id="term-count" role="status">모든 용어를 가나다순으로 표시합니다. 영문 약어는 한국어 발음 순서입니다.</p><div class="glossary-grid">'''+''.join(entries)+'''</div><noscript><p>검색은 자바스크립트가 필요합니다. 브라우저의 찾기 기능으로 전체 목록을 검색할 수 있습니다.</p></noscript>'''
    (SITE/'glossary.html').write_text(shell('glossary','용어집','처음 만나는 말은 쉬운 설명과 처음 나온 장으로 연결합니다.',content,'<script src="assets/glossary.js" defer></script>'))
    return len(terms)


def credits():
    sources={sid:(title,dict(re.findall(r'^- ([^:]+): (.*)$',body,re.M))) for sid,title,body in re.findall(r'### (S\d+)\. (.*?)\n(.*?)(?=\n<a id=|\Z)',(ROOT/'research/SOURCES.md').read_text(),re.S)}
    cited={}
    for p in CHAPTERS:
        text=p.read_text()
        notes=re.search(r'<aside class="source-notes".*?</aside>',text,re.S)[0]
        for sid in sorted(set(re.findall(r'\bS\d{3}\b',notes))):
            assert sid in sources,sid
            anchor='source-'+sid.lower()
            if f'id="{anchor}"' not in notes:
                # 1장 묶음 각주는 해당 원문 링크가 들어 있는 실제 li로 연결.
                anchor=next(m[1] for m in re.finditer(r'<li id="([^"]+)">(.*?)</li>',notes,re.S) if sid in m[2])
            cited.setdefault(sid,[]).append((p.stem,anchor,int(p.name[:2])))
    entries=[]
    for sid,links in sorted(cited.items()):
        title,meta=sources[sid]
        data=''.join(f'<div><dt>{label}</dt><dd>{E(meta.get(key,"미상"))}</dd></div>' for label,key in [('기관','기관'),('게시·갱신일','게시·갱신일'),('확인일(조사 접근일)','접근일'),('신뢰도 등급','신뢰도')])
        backlink=' · '.join(f'<a href="chapters/{slug}.html#{anchor}">{n}장 각주</a>' for slug,anchor,n in links)
        entries.append(f'<li class="source-entry" id="{sid.lower()}"><h3>{sid} · <a href="{E(meta["URL"],quote=True)}">{E(title)}</a></h3><dl class="source-meta">{data}</dl><p><strong>확인 범위:</strong> {E(meta.get("확인 범위","기록 없음"))}</p><p>인용한 장: {backlink}</p></li>')
    content=f'''<p class="note warning">2026년 10월 조사 기준, 정책은 바뀔 수 있음. 조사 컷오프·확인일은 2026-10-26입니다. 실제 계정의 현재 자격과 개인별 법·세무 판단을 대신하지 않습니다.</p>
<nav class="related-links" aria-label="크레딧 절"><a href="#sources">인용 출처</a><a href="#licenses">폰트·도구</a><a href="#disclosure">가상·합성 고지</a><a href="#updates">업데이트 기록</a></nav>
<section id="sources" class="chapter-block"><h2>본문에서 인용한 출처 {len(entries)}개</h2><p>A: 공식 문서·법령·정부·제작자, B: 언론·업계 조사, C: 개인·블로그. 등급 A도 최신성·한국 적용을 보증하지 않습니다. ‘Hermes 확인’과 Codex 직접 검증은 다릅니다. 날짜 미상을 접근일로 바꾸지 않았습니다. 번호는 연구 목록의 원래 번호여서 중간 번호가 빠질 수 있습니다.</p><ul class="source-list">{''.join(entries)}</ul></section>
<section id="licenses" class="chapter-block"><h2>폰트·도구 라이선스</h2><p>라이선스 링크 확인: 2026-10-26. 연구의 정책 출처 목록과 별도로 제공하는 제작 크레딧입니다. 사용한 구성요소의 원문 조건을 따릅니다.</p>
<ul><li>웹 본문: Pretendard Variable v1.3.9, Kil Hyung-jin, SIL OFL 1.1. <a href="https://github.com/orioncactus/pretendard/blob/v1.3.9/LICENSE">원문 라이선스</a>. 고정 버전 CDN을 사용하며 연결이 안 되면 시스템 폰트로 표시합니다.</li>
<li>샘플 이미지: Google Fonts / Adobe의 Noto Sans KR, SIL OFL 1.1. <a href="assets/licenses/NotoSansKR-OFL.txt">동봉 저작권·라이선스 전문</a>. 카드에는 이 글꼴로 렌더링한 픽셀이 포함됩니다.</li>
<li>스타터 키트 원본 코드·합성 피드·생성 샘플: MIT, Guidebooks contributors. <a href="assets/img/samples/LICENSE.txt">원문과 적용 범위</a>. 교과서 전체의 권리로 확대하지 않습니다.</li>
<li>카드 렌더링: <a href="https://pillow.readthedocs.io/en/stable/about.html#license">Pillow, MIT-CMU 라이선스 고지</a>. 설정: <a href="https://github.com/yaml/pyyaml/blob/main/LICENSE">PyYAML, MIT</a>.</li>
<li>영상 도구: <a href="https://github.com/imageio/imageio-ffmpeg/blob/main/LICENSE">imageio-ffmpeg 래퍼, BSD 2-Clause</a>. FFmpeg 실행 파일은 래퍼와 별도 라이선스이며 빌드에 따라 LGPL/GPL이 적용됩니다. <a href="https://ffmpeg.org/legal.html">FFmpeg 공식 설명</a>. 실행 파일을 이 사이트에 재배포하지 않습니다.</li>
<li>브라우저 검증: <a href="https://github.com/microsoft/playwright/blob/main/LICENSE">Playwright, Apache 2.0</a>. 사이트 실행에 필요한 라이브러리는 아닙니다. 본문·도식·CSS·JS는 새로 작성했으며 참고 사이트에서는 학습 구조와 UX 패턴만 참고했습니다.</li></ul></section>
<section id="disclosure" class="chapter-block"><h2>가상 인물·합성 데이터 고지</h2><p>하린·정 선배·하린의 계정과 실습 수치는 가상입니다. 예제 피드·카드·영상은 synthetic=true 자료로 만든 교육용 샘플이며 실제 뉴스 보도가 아닙니다. 표지 영상은 무음이며 한글 자막이 화면에 포함됩니다. 별도 자막 파일도 제공합니다.</p><p>성장·니치 점수·장부·30일 일정은 공개한 가정에 따른 연습이며 수익·추천·성장 예측이 아닙니다. 실제 사례는 인용 범위 안에서만 다룹니다. 실제 Instagram 계정 로그인·게시·유료 API 호출을 검증한 교재가 아닙니다.</p><p>테마·완료 체크와 3·4·14장 변경 입력은 이 브라우저의 localStorage에 저장합니다. 서버로 전송하지 않습니다. 실험실에서 입력을 삭제할 수 있고 저장 차단 시 계산·읽기는 계속 됩니다.</p></section>
<section id="updates" class="chapter-block"><h2>업데이트 기록</h2><dl><dt>2026-10-26 · Phase 5d</dt><dd>2~14장 공통 상태·메타·이동 통합, 15장 실험실, 16장 용어집, 인용 출처와 표지 샘플을 추가했습니다. 1장 대기 문장을 조사 근거와 미확인 범위로 대체했습니다.</dd><dt>2026-10-26 · 앞선 제작·집필</dt><dd>오프라인 스타터 키트와 1~14장 원고·모형, 초기·확장 조사 기록을 통합 기반으로 사용했습니다. 세부 검증은 저장소 docs/results의 해당 Phase 기록을 따릅니다.</dd></dl></section>'''
    (SITE/'credits.html').write_text(shell('credits','출처·크레딧','근거를 찾을 수 있고, 확인하지 못한 범위도 읽을 수 있도록.',content))
    return len(entries)


def lab(entries):
    fallback=''.join(f'<li><a href="chapters/{s["slug"]}.html#{s["id"]}">{s["chapter"]}장 · {E(s["title"])}</a></li>' for s in entries if s['chapter']!=15)
    content='''<p class="note">장별 그림과 입력 도구를 한곳에서 골라 만져 보세요. 원본 장의 도구와 가정 설명을 그대로 불러옵니다. Tab으로 입력에 들어가고 방향키·Enter·Space로 조작합니다.</p><div class="filter-row"><label>실험 선택 <select id="sim-picker"><option value="month-scenario">15장 · 내 계정 한 달 시나리오</option></select></label></div><p><a id="sim-original" href="chapters/14-plan.html#simulator">원본 장에서 전체 맥락 읽기 →</a></p><div class="lab-stage"><iframe class="lab-frame" id="sim-frame" title="선택한 원본 장의 시뮬레이터" hidden></iframe>
<section id="month-scenario" class="simulator" aria-labelledby="month-title"><div class="sim-heading"><h2 id="month-title">내 계정 한 달 시나리오</h2><span class="model-badge">교육용 가정 모형</span></div><div class="sim-body"><p>예측 아님 · 니치 자기평가·현금 장부·작업 후보를 모은 요약입니다. 팔로워나 수익 달성 시점을 계산하지 않습니다.</p><div class="month-grid"><article class="month-card"><h3>4장 · 독자와 주당 시간</h3><p data-month-niche>4장 입력을 기다립니다.</p><a href="chapters/04-niche.html#niche-sim">니치·주당 시간 바꾸기</a></article><article class="month-card"><h3>3장 · 같은 기간의 현금 장부</h3><p data-month-ledger>3장 입력을 기다립니다.</p><a href="chapters/03-revenue.html#ledger-sim">장부 바꾸기</a></article><article class="month-card"><h3>14장 · 30일 계획</h3><p data-month-plan>14장 입력을 기다립니다.</p><a href="chapters/14-plan.html#planner-sim">계획 바꾸기</a></article><article class="month-card"><h3>가정을 읽는 법</h3><p>장부의 기간은 독자가 맞춰야 합니다. 주당 시간과 플래너의 활동일·하루 확보 시간을 함께 비교하세요. 계획 배치는 실제 완료가 아닙니다. 빈칸·무효 입력은 0으로 추정하지 않습니다.</p><button type="button" data-refresh-month>저장한 입력 다시 읽기</button><button type="button" data-clear-month>3·4·14장 저장 입력 삭제</button><p data-month-storage role="status"></p></article></div></div><p class="sim-assumptions">초기 예시값은 가져오지 않고, 독자가 변경한 원본 장 입력과 원본 계산 결과만 이어 씁니다. 브라우저를 바꾸거나 저장을 차단하면 전달되지 않을 수 있습니다. 삭제는 테마·완료 체크를 지우지 않습니다.</p></section></div>
<details class="home-section"><summary>원본 도구 전체 목록 · 직접 열기</summary><ol>'''+fallback+'''</ol></details><noscript><p class="note">선택·요약은 자바스크립트가 필요합니다. 위 원본 도구 목록에서 각 장의 본문과 가정을 읽으세요.</p></noscript>'''
    scripts='<script src="assets/catalog.js" defer></script><script src="assets/sim/common.js" defer></script><script src="assets/lab.js" defer></script>'
    (SITE/'lab.html').write_text(shell('lab','자동화 실험실','한 번에 하나씩 바꾸고, 결과보다 가정을 먼저 읽어 보세요.',content,scripts))


if __name__ == '__main__':
    entries=catalog()
    print(f'도구 {len(entries)}개, 용어 {glossary()}개, 인용 출처 {credits()}개')
    lab(entries)
