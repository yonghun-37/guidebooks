"""위험 주제는 설정과 관계없이 사람 검토로 분류한다."""
import json
HEALTH = ('건강', '안전', '터미타임', '수면', '수유', '접종', '발열', '황달', '구토', '호흡', 'tummy', 'health', 'safety')

def is_health(doc: dict) -> bool:
    """제목과 설명을 포함한 메타데이터에서 건강 주제를 찾는다."""
    text = json.dumps({k: doc.get(k, '') for k in ('title', 'description', 'markdown', 'html', 'risk_flags', 'emergency_topics')}, ensure_ascii=False).lower()
    return any(word in text for word in HEALTH)

def requires_human(doc: dict) -> bool:
    """고위험 글은 언제나 사람 승인을 요구한다."""
    flags = set(doc.get('risk_flags', []))
    metadata = (doc.get('title', '') + ' ' + doc.get('description', '')).lower()
    flagged = bool(flags.intersection({'child_photo', 'experience', 'sponsor', 'affiliate', 'existing_update', 'update', 'photo', 'commercial'}))
    flagged = flagged or any(word in metadata for word in ('아이 사진', '아이의 사진', '협찬', '제휴', '기존 글 갱신'))
    return bool(flagged or is_health(doc) or doc.get('content_type') in ('affiliate', 'sponsor') or doc.get('commercial_relations') or doc.get('experience') or doc.get('photos') or any(m.get('child_photo') for m in doc.get('media', [])) or doc.get('is_update') or 'update' in doc.get('risk_flags', []))
