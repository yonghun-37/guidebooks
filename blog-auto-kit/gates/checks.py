"""건강·개인정보·상업 표시의 검토 항목을 생성한다."""
import json
import re
from pathlib import Path
from gates.risk import is_health
from gates.privacy_exif import inspect_exif
from gates.body import body_text, html_text

EMERGENCY = json.loads((Path(__file__).resolve().parents[1] / 'samples/emergency.json').read_text(encoding='utf-8'))['items']

def result(rule, decision, field, reason, action, evidence, human=False):
    """공통 관문 결과 형식을 만든다."""
    return {'rule_id': rule, 'decision': decision, 'evidence_ids': evidence, 'matched_field': field,
            'reason_ko': reason, 'next_action_ko': action, 'human_resolvable': human}

def health_checks(doc):
    """건강 주장의 출처와 고정 응급 문구를 확인한다."""
    out = []; text = body_text(doc)
    if is_health(doc) or any(x in text for x in ('해열제', '아세트아미노펜', '이부프로펜')):
        out.append(result('health_safety.H1', 'review', 'risk_flags', '건강·안전 주제는 사람 검토가 필요합니다.', '의료 근거와 문맥을 확인하세요.', ['BXF-091'], True))
        sources = doc.get('source_notes', [])
        if not sources or any(not s.get('official') or not s.get('age_range') or not s.get('checked_on') or not s.get('country') or not s.get('claims') for s in sources):
            out.append(result('health_safety.H2', 'review', 'source_notes', '공식 출처·월령·기준일이 부족합니다.', '공식 자료를 보완하세요.', ['BX077'], False))
        if any(x in text for x in ('집에서 지켜봐도', '해열제 용량', '아세트아미노펜', '이부프로펜', 'mg 복용')) or re.search(r'\d+(?:\.\d+)?\s*(?:mg|밀리그램|ml|밀리리터)\s*(?:을|를)?\s*(?:먹|복용|투여)', text, re.I):
            out.append(result('health_safety.H3', 'block', 'markdown', '약이나 자가 관찰 판정이 포함되어 있습니다.', '해당 문장을 제거하세요.', ['NB-SICK-06']))
    topics = set(doc.get('emergency_topics', []))
    subject = doc.get('title', '') + ' ' + doc.get('description', '')
    for word, topic in (('발열', 'fever'), ('황달', 'jaundice'), ('구토', 'vomit'), ('배꼽', 'navel'), ('저체온', 'cold'), ('발진', 'rash'), ('호흡', 'breathing'), ('수유', 'feeding'), ('부모 위기', 'parent'), ('울음', 'cry')):
        if word in subject:
            topics.add(topic)
    for topic in sorted(topics):
        row = next((r for r in EMERGENCY if r['id'] == topic), None)
        if row is None or row['text'] not in text:
            out.append(result('health_safety.H4', 'block', 'emergency_topics', '응급 문구가 없거나 원문과 다릅니다.', '공통 문구와 출처를 그대로 넣으세요.', row['sources'] if row else []))
    if topics and any(w in text for w in ('며칠 기다', '하루 기다', '모두 나타나면', '모두 나타날 때', '둘 다 나타나면')):
        out.append(result('health_safety.H4', 'block', 'markdown', '응급 신호를 기다리거나 함께 나타나야 한다고 완화했습니다.', '완화 문장을 제거하세요.', ['N001']))
    if doc.get('generation_status') in ('refused', 'truncated', 'invalid') or doc.get('claims_match_sources') is False:
        out.append(result('health_safety.H5', 'review', 'generation_status', '초안이 잘렸거나 주장과 근거가 일치하지 않습니다.', '초안과 근거를 다시 확인하세요.', ['BXF-087'], False))
    return out

def privacy_checks(doc, root=None):
    """사진과 경험의 공개 범위를 점검한다."""
    out = []; media = doc.get('media', [])
    if doc.get('photos') or doc.get('experience') or any(m.get('child_photo') for m in media):
        out.append(result('child_privacy.C1', 'review', 'media', '아이 사진 또는 경험은 사람 확인이 필요합니다.', '공개 범위를 직접 검토하세요.', ['BXF-052', 'BXF-091'], True))
    text = body_text(doc)
    sensitive = r'(?:아이\s*생일|아이\s*실명|어린이집|병원명|집\s*주소|생활\s*위치)\s*[:：]\s*\S+'
    if re.search(sensitive, text):
        out.append(result('child_privacy.C2', 'block', 'markdown', '아이의 식별 정보가 포함되어 있습니다.', '식별 정보를 제거하세요.', ['BXF-054']))
    form = doc.get('contact_form')
    if form and (form.get('data_minimized') is not True or form.get('notice_matches') is not True):
        out.append(result('child_privacy.C4', 'review', 'contact_form', '문의 양식의 수집·고지 범위가 불명확합니다.', '수집을 중지하고 고지와 항목을 확인하세요.', ['BXF-056'], False))
    for m in media:
        if m.get('child_photo') and not m.get('permissions'):
            out.append(result('child_privacy.C3', 'review', 'media.permissions', '사진 공개 권한이 불명확합니다.', '동의와 공개 범위를 확인하세요.', ['BXF-052'], False))
        path = Path(m.get('path', ''))
        base = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[1]
        candidate = (base / path).resolve()
        exif = False
        if not candidate.is_relative_to(base) or not candidate.is_file():
            out.append(result('child_privacy.C2', 'review', 'media.path', '미디어 경로를 확인할 수 없습니다.', '키트 안의 실제 파일을 확인하세요.', ['BXF-054'], False))
        if candidate.is_relative_to(base) and candidate.is_file() and candidate.suffix.lower() in ('.jpg', '.jpeg'):
            try:
                exif = bool(inspect_exif(candidate.read_bytes()))
            except ValueError:
                out.append(result('child_privacy.C2', 'review', 'media.path', 'JPEG 파일을 검사할 수 없습니다.', '이미지를 다시 확인하세요.', ['BXF-054'], False))
        if m.get('exif') or m.get('gps') or exif:
            out.append(result('child_privacy.C2', 'block', 'media', '위치 또는 EXIF 정보가 남아 있습니다.', '메타데이터를 제거하고 다시 검사하세요.', ['BXF-054']))
    return out

def disclosure_checks(doc):
    """관계 표시와 실제 경험의 출처를 점검한다."""
    out = []; relations = doc.get('commercial_relations', []); text = doc.get('markdown', '')
    opening = doc.get('title', '') + ' ' + text.split('\n\n', 1)[0]
    final_opening = doc.get('title', '') + ' ' + html_text(doc.get('html', '').split('</p>', 1)[0])
    for rel in relations:
        kind = rel.get('kind', '')
        words = ('수수료', '제휴') if kind == 'affiliate' else ('협찬', '무료 제공', '무료제공', '광고비', '유료광고')
        if not any(w in opening for w in words) or not any(w in final_opening for w in words):
            rule = 'disclosure.D2' if any(w in text for w in words) else 'disclosure.D1'
            out.append(result(rule, 'block', 'commercial_relations', '경제적 관계가 첫부분에 표시되지 않았습니다.', '실제 관계를 첫부분에 밝히세요.', ['BXF-035', 'BXF-038']))
    kinds = {r.get('kind') for r in relations}
    if len(kinds) > 1 and any(r['rule_id'] in ('disclosure.D1', 'disclosure.D2') for r in out):
        out.append(result('disclosure.D5', 'block', 'commercial_relations', '복수의 경제적 관계 중 일부가 표시되지 않았습니다.', '각 관계를 모두 공개하세요.', ['BXF-038']))
    if relations and any(m.get('independent_reuse') or m.get('photo_recommendation') for m in doc.get('media', [])):
        out.append(result('disclosure.D3', 'review', 'media', '독립 사용되는 사진의 표시 여부를 확인해야 합니다.', '사진 표시 또는 예외를 확인하세요.', ['BXF-037'], False))
    needs = doc.get('content_type') == 'sponsor' or (relations and not doc.get('comparison_only'))
    if needs and (not doc.get('experience') or doc.get('experience_by') != 'human'):
        out.append(result('disclosure.D4', 'block', 'experience', '실제 경험은 사람이 작성해야 합니다.', '사람의 경험을 직접 입력하세요.', ['BXF-039']))
    return out
