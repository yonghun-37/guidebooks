"""자동 발행은 허용 조건을 모두 확인했을 때만 연다."""
import json
import re

HEALTH = ('건강', '안전', '터미타임', '수면', '수유', '접종', '발열', '황달', '구토', '호흡',
          '저체온', '발진', '응급', 'tummy', 'health', 'safety', '해열제', '아스피린',
          '아세트아미노펜', '이부프로펜', '약 이름', '복용', '투약', '의약품')
MEDICINE = re.compile(r'(?:[가-힣A-Za-z]+(?:프로펜|아미노펜|마이신|실린|프라졸|스타틴)|\d+(?:\.\d+)?\s*(?:mg|ml|밀리그램|밀리리터|정|포)(?=$|[^A-Za-z가-힣]|을|를|씩|으로))', re.I)
IDENTIFICATION = re.compile(r'(?:아이(?:의)?\s*(?:이름|실명|생일)|이름은|병원(?:명|은|에)|[가-힣]+병원|[가-힣]+어린이집|다니는\s*어린이집|어린이집(?:은|의)|집\s*주소|생활\s*위치)')
SIGNALS = ('아이 사진', '아이의 사진', '아이 얼굴', '협찬', '제휴', '수수료', '제품 제공',
           '무료 제공', '상품 무료제공', '광고비', '대여', '기존 글', '갱신', '업데이트')


def content_text(doc):
    """제목·설명·본문·경험·이미지 설명/속성을 같은 범위로 읽는다."""
    keys = ('title', 'description', 'markdown', 'html', 'experience', 'photos', 'media',
            'risk_flags', 'emergency_topics')
    return json.dumps({k: doc.get(k, '') for k in keys}, ensure_ascii=False).lower()


def is_health(doc: dict) -> bool:
    """약 검사도 보조 신호이며 의료 의미를 완전히 판별하지는 않는다."""
    text = content_text(doc)
    return any(word in text for word in HEALTH) or bool(MEDICINE.search(text))


def may_auto_publish(doc: dict, results: list, record: dict) -> bool:
    """허용 유형·전부 pass·위험 신호 없음·서버 신규 확인을 모두 요구한다."""
    allowed = record.get('auto_allowed_types', [])
    if doc.get('content_type') not in ('info', 'play') or doc.get('content_type') not in allowed:
        return False
    if not results or any(row.get('decision') != 'pass' for row in results):
        return False
    if record.get('server_checked') is not True or record.get('server_new_confirmed') is not True or record.get('is_update'):
        return False
    text = content_text(doc)
    if is_health(doc) or IDENTIFICATION.search(text) or any(word in text for word in SIGNALS):
        return False
    if any(doc.get(key) for key in ('experience', 'photos', 'commercial_relations', 'registered_relations', 'product_records', 'paid_links', 'links', 'is_update', 'risk_flags')):
        return False
    if doc.get('contract', {}).get('commercial_relations'):
        return False
    # 이미지 내용의 안전은 코드가 판별하지 않는다. 직접 제작한 삽화만 허용한다.
    for media in doc.get('media', []):
        if media.get('child_photo') is not False or media.get('kind') != 'illustration' or media.get('permissions') != '직접 제작':
            return False
    return True


def requires_human(doc: dict) -> bool:
    """기존 호출자의 표시용 보수 판정. 발행 판단에는 사용하지 않는다."""
    return not may_auto_publish(doc, [{'decision': 'pass'}], {
        'auto_allowed_types': ['info', 'play'], 'server_checked': True,
        'server_new_confirmed': True, 'is_update': False})
