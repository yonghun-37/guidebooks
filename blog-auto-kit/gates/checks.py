"""건강·개인정보·상업 표시의 검토 항목을 생성한다."""
import json
import re
from pathlib import Path
from gates.risk import is_health, content_text, IDENTIFICATION, MEDICINE
from gates.privacy_exif import inspect_exif
from gates.body import body_text, html_text

EMERGENCY = json.loads((Path(__file__).resolve().parents[1] / 'samples/emergency.json').read_text(encoding='utf-8'))['items']

def result(rule, decision, field, reason, action, evidence, human=False):
    """공통 관문 결과 형식을 만든다."""
    return {'rule_id': rule, 'decision': decision, 'evidence_ids': evidence, 'matched_field': field,
            'reason_ko': reason, 'next_action_ko': action, 'human_resolvable': human}

def health_checks(doc):
    """건강 주장의 출처와 고정 응급 문구를 확인한다."""
    out = []; text = body_text(doc); all_text = content_text(doc)
    if is_health(doc):
        out.append(result('health_safety.H1', 'review', 'risk_flags', '건강·안전 주제는 사람 검토가 필요합니다.', '의료 근거와 문맥을 확인하세요.', ['BXF-091'], True))
        sources = doc.get('source_notes', [])
        if not sources or any(not s.get('official') or not s.get('age_range') or not s.get('checked_on') or not s.get('country') or not s.get('claims') for s in sources):
            out.append(result('health_safety.H2', 'review', 'source_notes', '공식 출처·월령·기준일이 부족합니다.', '공식 자료를 보완하세요.', ['BX077'], False))
        if any(x in all_text for x in ('집에서 지켜봐도', '해열제 용량', '아스피린', '아세트아미노펜', '이부프로펜')) or MEDICINE.search(all_text):
            out.append(result('health_safety.H3', 'block', 'markdown', '약이나 자가 관찰 판정이 포함되어 있습니다.', '해당 문장을 제거하세요.', ['NB-SICK-06']))
    topics = set(doc.get('emergency_topics', []))
    subject = all_text
    for word, topic in (('발열', 'fever'), ('황달', 'jaundice'), ('구토', 'vomit'), ('배꼽', 'navel'), ('저체온', 'cold'), ('발진', 'rash'), ('호흡', 'breathing'), ('수유', 'feeding'), ('부모 위기', 'parent'), ('울음', 'cry')):
        if word in subject:
            topics.add(topic)
    if is_health(doc) and not topics:
        out.append(result('health_safety.H4', 'review', 'markdown', '건강 글의 공통 응급 문구 적용 여부를 확인해야 합니다.', '해당 응급 신호가 있으면 공통 문구를 그대로 넣고 사람이 검토하세요.', ['BXF-091'], True))
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
    text = content_text(doc)
    sensitive = r'(?:아이\s*생일|아이\s*실명|어린이집|병원명|집\s*주소|생활\s*위치)\s*[:：]\s*\S+'
    if re.search(sensitive, text):
        out.append(result('child_privacy.C2', 'block', 'markdown', '아이의 식별 정보가 포함되어 있습니다.', '식별 정보를 제거하세요.', ['BXF-054']))
    elif IDENTIFICATION.search(text):
        out.append(result('child_privacy.C2', 'review', 'document', '아이 이름·병원·어린이집 등 식별 의심 표현이 있습니다.', '사람이 문맥과 결합 식별 가능성을 확인하고 제거하세요.', ['BXF-054'], True))
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
        if candidate.is_relative_to(base) and candidate.is_file():
            try:
                exif = bool(inspect_exif(candidate.read_bytes()))
            except ValueError:
                out.append(result('child_privacy.C2', 'review', 'media.path', '실제 형식의 이미지 파일을 검사할 수 없습니다.', '이미지를 다시 확인하세요.', ['BXF-054'], False))
        if m.get('exif') or m.get('gps') or exif:
            out.append(result('child_privacy.C2', 'block', 'media', '위치 또는 EXIF 정보가 남아 있습니다.', '메타데이터를 제거하고 다시 검사하세요.', ['BXF-054']))
    return out

def disclosure_checks(doc):
    """관계 표시와 실제 경험의 출처를 점검한다."""
    out = []; relations = doc.get('commercial_relations', []); text = doc.get('markdown', '')
    from gates.body import relation_disclosure_checks
    out.extend(relation_disclosure_checks(doc))
    if relations and any(m.get('independent_reuse') or m.get('photo_recommendation') for m in doc.get('media', [])):
        out.append(result('disclosure.D3', 'review', 'media', '독립 사용되는 사진의 표시 여부를 확인해야 합니다.', '사진 표시 또는 예외를 확인하세요.', ['BXF-037'], False))
    needs = doc.get('content_type') == 'sponsor' or (relations and not doc.get('comparison_only'))
    if needs and (not doc.get('experience') or doc.get('experience_by') != 'human'):
        out.append(result('disclosure.D4', 'block', 'experience', '실제 경험은 사람이 작성해야 합니다.', '사람의 경험을 직접 입력하세요.', ['BXF-039']))
    return out
