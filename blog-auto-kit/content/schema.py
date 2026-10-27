"""네 가지 글의 공통 필드와 출처 구조를 점검한다."""
FIELDS = {'content_id': str, 'content_type': str, 'title': str, 'description': str,
          'markdown': str, 'html': str, 'author': str, 'as_of': str,
          'risk_flags': list, 'source_notes': list, 'experience': str,
          'experience_by': str, 'photos': list, 'media': list,
          'commercial_relations': list, 'product_records': list,
          'contract': dict, 'emergency_topics': list}
SOURCE = ('id', 'url', 'official', 'country', 'checked_on', 'age_range', 'license', 'claims')
PRODUCT = ('product_type', 'intended_use', 'model', 'maker', 'certification_scheme', 'recall_check', 'ad_review_scope', 'recall_status', 'classification_basis', 'regulated_category')

def validate(doc) -> list:
    """필수 필드 오류를 한국어 목록으로 반환한다."""
    if not isinstance(doc, dict):
        return ['문서가 객체가 아닙니다']
    errors = [f'{key}: 필수 형식 오류' for key, typ in FIELDS.items() if not isinstance(doc.get(key), typ)]
    for key in ('content_id', 'title', 'description', 'author', 'as_of'):
        if isinstance(doc.get(key), str) and not doc[key].strip():
            errors.append(f'{key}: 값이 비어 있습니다')
    if doc.get('content_type') not in ('info', 'play', 'affiliate', 'sponsor'):
        errors.append('content_type: 알 수 없는 글 유형')
    for key, fields in (('source_notes', SOURCE), ('product_records', PRODUCT),
                        ('media', ('path', 'alt', 'child_photo', 'permissions')),
                        ('commercial_relations', ('kind', 'program', 'brand', 'details'))):
        for item in doc.get(key, []) if isinstance(doc.get(key), list) else []:
            if not isinstance(item, dict) or any(k not in item for k in fields):
                errors.append(f'{key}: 필수 항목 누락')
    for product in doc.get('product_records', []):
        if isinstance(product, dict) and product.get('recall_status') not in ('none_found', 'recalled', 'unchecked'):
            errors.append('product_records.recall_status: 확인 필요')
    for source in doc.get('source_notes', []):
        if isinstance(source, dict) and not isinstance(source.get('official'), bool):
            errors.append('source_notes.official: 참 또는 거짓이어야 합니다')
    for media in doc.get('media', []):
        if isinstance(media, dict) and not isinstance(media.get('child_photo'), bool):
            errors.append('media.child_photo: 참 또는 거짓이어야 합니다')
    if isinstance(doc.get('contract'), dict) and doc['contract'].get('ai_allowed') not in (True, False, 'unknown'):
        errors.append('contract.ai_allowed: 확인 필요')
    return errors
