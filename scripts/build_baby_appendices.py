#!/usr/bin/env python3
"""BabyBook의 현재 인용·원본 도구로 출처/용어집/실험실을 재생성한다.

python3 scripts/build_baby_appendices.py
다른 책·연구 원본은 쓰지 않는다. 용어는 본문에서 설명한 뜻만 편집한다.
"""
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site-baby'
# key, 표제어, 짧은 뜻, 원본 장, 근거(파일 형식·가족 계획 용어는 본문 링크만).
TERMS = [
 ('mixed-feeding','혼합수유','모유와 분유 수유를 병행하는 방식입니다.','02-feeding','N089'),
 ('expressing','유축','모유를 짜서 용기에 담는 일입니다.','02-feeding','N014'),
 ('formula-preparation','조유','제품에 표시된 물과 가루의 비율로 분유를 타는 일입니다.','02-feeding','N010 N012'),
 ('feeding-cues','배고픔 신호','아기가 먹고 싶을 때 보이는 움직임 등 수유를 시작할 단서입니다.','02-feeding','N005'),
 ('latch','깊이 물리기','아기가 입을 크게 벌릴 때 유방을 깊이 물도록 돕는 수유 방법입니다.','02-feeding','N005 N016'),
 ('regurgitation','게워냄','수유 뒤 소량의 우유가 흘러나오는 모습입니다. 구토의 색·반복·먹는 상태는 따로 살핍니다.','02-feeding','N060'),
 ('cleaning','세척','젖병과 부품을 분리해 씻고 헹구어 오염물을 없애는 일입니다.','02-feeding','N015'),
 ('sanitizing','소독','세척한 수유 도구의 세균 등을 더 줄이는 과정입니다. 세척을 대신하지 않습니다.','02-feeding','N015'),
 ('sids','영아돌연사증후군','1세 이전 아기가 갑자기 사망했으나 부검·현장·과거 병력 조사로도 원인을 알 수 없는 경우입니다.','03-sleep','N002'),
 ('separate-sleep','같은 방·별도 잠자리','부모와 방을 함께 쓰면서 아기에게 따로 마련한 잠자리에서 재우는 방식입니다.','03-sleep','N002'),
 ('swaddling','속싸개','아기를 감싸는 천입니다. 국내외 안내 차이와 뒤집기 시도를 확인합니다.','03-sleep','N031 N093'),
 ('pacifier','공갈젖꼭지','수유 없이 빨도록 만든 젖꼭지입니다. 신생아 사용에 관한 국내외 안내를 확인합니다.','03-sleep','N031 N020'),
 ('colic','영아산통','다른 면에서는 건강한 아기의 긴 울음 양상을 가리키는 말입니다. 시간만으로 진단하지 않고 다른 원인을 확인합니다.','04-crying','N026'),
 ('meconium','태변','출생 초기에 나오는 검고 끈적한 변입니다.','05-diapers','N102'),
 ('transitional-stool','이행변','태변 이후 수유가 진행되며 색과 양상이 달라지는 중간 단계의 변입니다.','05-diapers','N017 N102'),
 ('wet-diaper','젖은 기저귀','이 책에서는 소변이 있는 기저귀를 뜻합니다. 대변 기록과 구분합니다.','05-diapers','N005'),
 ('jaundice','황달','피부 등이 노랗게 보이는 변화입니다. 색만으로 수치나 원인을 정하지 않습니다.','07-hospital','N003'),
 ('sponge-bath','부분 씻기','아기를 물에 담그지 않고 젖은 천 등으로 닦는 방법입니다.','06-body','N007 N059'),
 ('cord-care','배꼽 관리','남아 있는 배꼽을 깨끗하고 마르게 두고 억지로 떼지 않는 돌봄입니다.','06-body','N007'),
 ('diaper-rash','기저귀 발진','기저귀가 닿는 피부에 생기는 발진입니다. 자주 갈고 부드럽게 씻고 말립니다.','05-diapers','N051'),
 ('temperature-site','체온 측정 부위','체온을 잰 몸의 위치입니다. 값과 함께 시간·기기를 기록합니다.','07-hospital','N001'),
 ('calendar-age','달력 월령','출생일부터 달력의 개월 단위로 센 나이입니다. 한 달을 30일로 바꾸지 않습니다.','09-checkups','N027 N031'),
 ('percentile','백분위','같은 성별·나이 기준에서 측정값의 상대 위치를 나타내는 수치입니다. 합격 점수가 아닙니다.','08-growth','N033'),
 ('growth-chart','성장도표','성별과 정확한 나이에 맞춰 키·체중 등 측정값의 흐름을 보는 자료입니다.','08-growth','N033'),
 ('tummy-time','터미타임','아기가 깨어 있을 때 어른이 곁에서 지켜보며 엎드려 노는 시간입니다.','08-growth','N032 N092'),
 ('screening','선별검사','추가 평가가 필요한지 살피는 검사입니다. 재검 안내는 확진과 구분합니다.','08-growth','N034 N035'),
 ('development','발달 이정표','아기의 움직임·반응 등을 관찰하고 의료진에게 질문하기 위한 안내입니다.','08-growth','N009 N032'),
 ('hexavalent','6가 혼합백신','여섯 감염병의 예방 성분을 함께 담은 백신입니다. B형간염 접종 경로를 기관에 확인합니다.','09-checkups','N027'),
 ('rotavirus','로타 접종','로타바이러스 예방접종입니다. 종류에 따라 접종 횟수가 달라 기록을 대조합니다.','09-checkups','N027'),
 ('infant-checkup','영유아건강검진','정해진 대상 기간에 성장·발달과 돌봄 등을 살피는 건강검진입니다.','09-checkups','N029 N031 N032'),
 ('voucher','바우처','정해진 곳에서 카드 등으로 사용하는 지원입니다. 현금 입금과 나누어 봅니다.','10-benefits','N036'),
 ('retroactive','소급','신청한 달보다 앞선 대상 월부터 급여를 지급하는 것입니다. 기한과 조건을 확인합니다.','10-benefits','N037'),
 ('accepted','수리','신고가 받아들여져 등록 처리된 상태입니다. 제출·접수 상태와 구분합니다.','10-benefits','N042 N098'),
 ('birth-notification','출생통보','병원이 출생 사실을 통보하는 절차입니다. 부모의 출생신고를 대신하지 않습니다.','10-benefits','N044'),
 ('happy-birth','행복출산','출산 관련 지원의 신청을 모아 처리하는 서비스입니다. 항목별 자격·결정은 따로 확인합니다.','10-benefits','N098'),
 ('postpartum','산욕기','출산 뒤 몸이 회복되는 시기입니다. 약 6주라는 설명을 완전 회복의 마감일로 삼지 않습니다.','11-parents','N053'),
 ('shifts','교대 돌봄','한 사람이 쉬는 동안 다른 사람이 아기를 맡도록 시간과 할 일을 나누는 가족 계획입니다.','11-parents',''),
 ('rear-facing','뒤보기','카시트에 앉은 아기가 차량 뒤쪽을 보게 하는 방향입니다.','12-safety','N094'),
 ('recall','리콜','결함 제품을 회수하거나 수리하는 등의 조치입니다. 정확한 모델명으로 조회합니다.','12-safety','N077'),
 ('csv','CSV','표의 각 칸을 쉼표로 구분해 저장하는 텍스트 파일 형식입니다. 이 책에서는 돌봄 기록을 내려받을 때 씁니다.','practice/09-records',''),
]
# chapter, slug, tool id, title, description, track
TOOLS = [
 (1,'01-map','deadline-tool','우리 아기 기한 달력','신고·급여·검진·로타 기한의 참고 날짜를 보고 기관과 대조합니다.','theory'),
 (2,'02-feeding','feeding-tool','수유 관찰 메모','삼킴·기저귀·체중·활력 중 상담 때 확인할 것을 고릅니다.','theory'),
 (3,'03-sleep','sleep-tool','잠자리 점검','빈 별도 잠자리와 졸릴 때 교대할 계획을 점검합니다.','theory'),
 (4,'04-crying','crying-tool','우는 이유 점검 흐름','급한 신호 확인부터 달래기·연락까지 순서를 따라갑니다.','theory'),
 (5,'05-diapers','diaper-note','기저귀 관찰 준비표','진료에 전할 일령·수유·기저귀 변화를 준비합니다.','theory'),
 (6,'06-body','bath-prep','씻기 전 준비표','배꼽 상태·물품·물 온도 확인을 메모합니다.','theory'),
 (7,'07-hospital','contact-card','연락처 카드 만들기','소아과·응급실·야간 기관 연락처를 적고 인쇄합니다.','theory'),
 (8,'08-growth','growth-note','검진 메모 준비표','측정 기록·궁금한 반응·선별검사 결과를 모읍니다.','theory'),
 (9,'09-checkups','calendar-tool','접종·검진 참고 달력','출생일과 B형간염 경로로 표준 시기를 확인합니다.','theory'),
 (10,'10-benefits','benefits-tool','2026 지원금 월별 비교','0~23개월의 현금·보육료·일회 바우처를 구분합니다.','theory'),
 (11,'11-parents','sleep-shifts','교대 수면 시간표','돌봄 가능한 시간을 넣어 휴식 구간과 도움 필요 시간을 봅니다.','theory'),
 (12,'12-safety','home-review','우리 집 안전 점검 메모','카시트·잠자리·접촉·제품에서 오늘 바꿀 일을 적습니다.','theory'),
 (13,'13-hundred-days','next-three-months','다음 석 달 준비 목록','접종·검진 예약과 움직임에 맞춘 환경 점검을 준비합니다.','theory'),
 (8,'08-checkups','schedule-tool','예약 전 참고 일정','접종 경로와 검진 참고 날짜를 보고 실제 전화 예약으로 이어갑니다.','practice'),
 (9,'09-records','care-log','수유·수면·기저귀 기록기','같은 브라우저에 기록하고 요약·CSV·인쇄로 남깁니다.','practice'),
]

def escape(value):
 return html.escape(value, quote=True)

def markdown(value):
 # Original registry fields use links, emphasis and occasional inline code.
 value=escape(value).replace('**','').replace('`','')
 return re.sub(r'\[([^]]+)\]\((https?://[^\s]+)\)',r'<a href="\2">\1</a>',value)

def sources():
 text=(ROOT/'research-baby/SOURCES.md').read_text()
 entries={}
 for sid,body in re.findall(r'^## (N\d{3})\n(.*?)(?=^## |\Z)',text,re.M|re.S):
  fields=dict(re.findall(r'^- ([^:]+): (.*)$',body,re.M))
  entries[sid]=fields
 return entries

def cited():
 ids=set()
 for p in SITE.rglob('*.html'):
  if p.name=='credits.html': continue
  ids.update(re.findall(r'\[(N\d{3})\]',p.read_text()))
 # Dynamic footnotes, including canonical emergency messages, also count.
 for p in (SITE/'assets').glob('*.js'):
  ids.update(re.findall(r'\bN\d{3}\b',p.read_text()))
 return ids

def replace_section(file, start, end, content):
 p=SITE/file;s=p.read_text();a=s.index(start);b=s.index(end,a)
 p.write_text(s[:a]+content+s[b:])

def build():
 entries=sources()
 # Create static glossary first, so its own evidence is part of the citation set.
 cards=[]
 for key,title,definition,chapter,refs in TERMS:
  path=chapter+'.html' if chapter.startswith('practice/') else 'chapters/'+chapter+'.html'
  foot=''.join(f'<sup class="footnote-ref"><a href="credits.html#{sid.lower()}">[{sid}]</a></sup>' for sid in refs.split())
  cards.append(f'<article id="{key}" class="glossary-entry" data-glossary-entry data-search="{escape(title+" "+definition)}"><h2>{escape(title)}</h2><p>{escape(definition)}{foot}</p><a href="{path}">본문에서 읽기 →</a></article>')
 glossary='<section class="chapter-block" id="terms"><h2>낯선 말부터 찾아요</h2><p>돌봄과 신청에 필요한 말입니다. 관련 본문에서 조건과 공식 안내를 함께 읽으세요.</p><label for="term-search">용어 검색</label><input type="search" id="term-search" placeholder="예: 조유, 바우처"><p id="term-count" role="status"></p><div class="glossary-grid">'+''.join(cards)+'</div></section>'
 replace_section('glossary.html','<section ', '<nav data-chapter-pager', glossary)
 p=SITE/'glossary.html';s=p.read_text()
 if 'assets/glossary.js' not in s:s=s.replace('</head>','<script defer src="assets/glossary.js"></script></head>')
 p.write_text(s)
 ids=cited()
 if ids-entries.keys(): raise ValueError(f'원본 미등록 출처: {sorted(ids-entries.keys())}')
 rows=[]
 for sid in sorted(ids):
  fields=entries[sid]
  document=re.fullmatch(r'\[(.*)\]\((https?://.*)\)',fields['문서'])
  title,url=document.groups()
  meta=[]
  for label in ['기관·등급','문서 날짜','확인 위치','확인 상태','적용·한계']:
   value=fields[label]
   # Keep source meaning, dates, limits; editorial tool names are not reader terminology.
   value=value.replace('Hermes','보조 조사').replace('Codex','직접 확인')
   meta.append(f'<p><strong>{label}</strong>: {markdown(value)}</p>')
  rows.append(f'<li id="{sid.lower()}" class="source-entry"><h3>[{sid}] <a href="{escape(url)}">{escape(title)}</a></h3><div class="check-points"><strong>확인할 점</strong>{"".join(meta)}</div></li>')
 replace_section('credits.html','<section class="chapter-block"','<section class="chapter-block"><h2>만든 방식',f'<section class="chapter-block" id="sources"><h2>본문에서 인용한 공식 안내 {len(ids)}개</h2><p>건강 정보는 국내 공식 안내를 우선하고 국외 보완은 본문에 표시했습니다. 아래에는 문서 날짜와 2026년 10월 27일 확인 당시의 적용 범위를 함께 남겼습니다. 각주의 번호로 원문을 찾을 수 있습니다.</p><ol class="credits-list">'+''.join(rows)+'</ol></section>')
 catalog=[];options=[];links=[]
 for number,slug,tid,title,desc,track in TOOLS:
  path=('practice/' if track=='practice' else 'chapters/')+slug+'.html'
  catalog.append(dict(chapter=number,slug=slug,id=tid,title=title,description=desc,section='simulator',track=track,path=path))
  label=('실습 ' if track=='practice' else '')+str(number)+(' · ' if track=='practice' else '장 · ')+title
  options.append(f'<option value="{slug}:{tid}">{escape(label)}</option>')
  links.append(f'<li><h3><a href="{path}#{tid}">{escape(label)} →</a></h3><p>{escape(desc)}</p></li>')
 (SITE/'assets/catalog.js').write_text('/* 원본 도구만 등록한다. scripts/build_baby_appendices.py로 재생성. */\nwindow.BabyCatalog = Object.freeze('+json.dumps(catalog,ensure_ascii=False,indent=2)+');\n')
 replace_section('lab.html','<section class="chapter-block"','<nav data-chapter-pager','<section class="chapter-block" id="tools"><h2>필요한 도구 하나를 골라요</h2><p>진단이나 안전 점수를 만들지 않습니다. 날짜는 기관과 확인하고, 관찰 메모는 상담에 씁니다. 연락처와 돌봄 기록은 같은 브라우저에만 남으며 기기 간에 합쳐지지 않습니다.</p><label for="sim-picker">도구 선택</label><select id="sim-picker">'+''.join(options)+'</select><p id="sim-description"></p><p><a id="sim-original" href="chapters/01-map.html#deadline-tool">원래 장에서 열기 →</a></p><iframe id="sim-frame" class="lab-frame" title="육아 도구" src="chapters/01-map.html?embed=deadline-tool"></iframe></section><section class="chapter-block" id="tool-list"><h2>도구와 바로 가기</h2><ul class="tool-list">'+''.join(links)+'</ul></section>')
 p=SITE/'lab.html';p.write_text(p.read_text().replace('육아 실험실 · 도구 샘플','육아 실험실'))
 print(json.dumps(dict(sources=len(ids),terms=len(TERMS),tools=len(TOOLS)),ensure_ascii=False))

if __name__=='__main__': build()
