"""제품의 자료 부족·금지 광고·프로젝트 거절을 구별한다."""
import re
from gates.checks import result
from gates.body import body_text, economic_relations


def _unknown(value):
    return not value or value in ('unknown', '미확인', '분류 불명')


def _finding(rule, decision, field, reason, action, evidence, classification=None):
    row = result('product_rules.' + rule, decision, field, reason, action, evidence, False)
    row['classification'] = classification or ('자료 보류' if decision == 'review' else '법적 금지')
    return row


def _classified(product):
    return (not any(_unknown(product.get(key)) for key in
            ('product_type', 'intended_use', 'model', 'maker', 'classification_basis'))
            and product.get('regulated_category') in ('other', 'infant_formula'))


def _classification_checks(product, commercial):
    out = []; typ = product.get('product_type', '')
    if not _classified(product):
        out.append(_finding('P1', 'review', 'product_records', '제품 분류 정보나 분류 근거가 부족합니다.',
                   '모델·업체·용도와 품목 분류 근거를 확인하세요.', ['BXF-044', 'BXF-097']))
    if commercial and _classified(product) and product.get('regulated_category') == 'infant_formula':
        out.append(_finding('P2', 'block', 'regulated_category', '조제유류 판매촉진은 거절합니다.',
                   '협찬 또는 제휴를 거절하세요.', ['BXF-041', 'BXF-042']))
    elif commercial and not _classified(product) and any(word in typ for word in ('조제유', '조제분유', '영아용 조제식')):
        out.append(_finding('P2', 'review', 'classification_basis', '조제유류의 법적 분류를 확인해야 합니다.',
                   '제품 이름만으로 확정하지 말고 품목 분류 자료를 확인하세요.', ['BXF-042']))
    return out


def _safety_checks(product):
    out = []; typ = product.get('product_type', ''); use = product.get('intended_use', '')
    if (any(_unknown(product.get(key)) for key in ('certification_scheme', 'recall_check', 'ad_review_scope'))
            or product.get('recall_status') not in ('none_found', 'recalled')):
        out.append(_finding('P3', 'review', 'product_records', '인증·리콜·광고 자료가 부족합니다.',
                   '해당 모델의 자료와 리콜 결과 값을 확인하세요.', ['BXF-044']))
    if product.get('recall_status') == 'recalled':
        out.append(_finding('P3', 'block', 'recall_status', '해당 모델이 리콜 대상으로 확인되었습니다.',
                   '사용과 홍보를 중단하세요.', ['BXF-044'], '프로젝트 거절'))
    if (any(word in typ + use for word in ('낮잠 이불', '낮잠이불', '수면 베개', '수면베개', '범퍼'))
            or (any(word in use for word in ('수면', '잠자리', '낮잠'))
                and any(word in typ for word in ('베개', '이불', '쿠션')))):
        out.append(_finding('P7', 'block', 'intended_use', '안전 수면 원칙과 충돌합니다.',
                   '협찬을 거절하세요.', ['BXF-050'], '프로젝트 거절'))
    return out


def _testimonial(text):
    """직접 사용 표현을 찾으며 명시적인 비사용 설명은 구별한다."""
    text = re.sub(r'(?:사용해\s*본\s*적(?:이)?\s*없\w*|사용하지\s*않\w*|써\s*본\s*적(?:이)?\s*없\w*)', '', text)
    return bool(re.search(r'(?:제가|저는|나는|내가|우리\s*아이|우리\s*아기|직접).{0,50}'
                          r'(?:사용(?:했|한|해|하니|하니까)|써\s*보|써보|썼|써봤|쓰니|써서)|'
                          r'(?:사용해\s*보니|사용해보니|써\s*보니|써봤더니|써봤어요|써봤습니다)', text))


def _disease_claim(text):
    """질병 대상 표현과 효능 주장을 함께 찾는 보조 검사다."""
    disease = r'(?:질병|질환|감기|아토피(?:피부염)?|피부염|비염|알레르기|천식|당뇨|암|염증|폐렴|장염|습진|독감)'
    efficacy = r'(?:예방|치료|완화|낫게|완치)'
    return bool(re.search(disease + r'[^.!?\n]{0,40}' + efficacy, text)
                or re.search(r'의약품과\s*같은|완치', text))


def _advertising_checks(product, text):
    out = []; typ = product.get('product_type', '')
    rule, evidence = ('P4', ['BXF-045']) if '화장품' in typ else ('P6', ['BXF-049']) if '건강기능식품' in typ else ('P5', ['BXF-048']) if '의료기기' in typ else ('P4', ['BXF-044'])
    if _disease_claim(text):
        regulated = _classified(product) and any(word in typ for word in ('화장품', '건강기능식품', '의료기기'))
        general = _classified(product) and any(word in typ for word in ('일반 제품', '일반제품'))
        out.append(_finding(rule, 'block' if regulated or general else 'review', 'markdown',
                   '질병 예방·치료·완화 광고 표현입니다.' if regulated or general else '질병 관련 광고의 제품 분류·허용 문안을 확정할 수 없습니다.',
                   '제품 분류와 허용 문안을 확인하고 광고 문구를 수정하세요.', evidence,
                   '프로젝트 거절' if general else None))
    if '의료기기' in typ and _testimonial(text):
        out.append(_finding('P5', 'block', 'experience', '의료기기 사용자 체험담 광고를 차단합니다.',
                   '사용자 체험담을 광고에 이용하지 마세요.', ['BXF-048']))
    if _unknown(product.get('ad_review_scope')):
        if '의료기기' in typ:
            out.append(_finding('P5', 'review', 'ad_review_scope', '의료기기 광고 심의 범위가 불명확합니다.',
                       '품목과 매체별 심의를 확인하세요.', ['BXF-047']))
        elif '화장품' in typ or '건강기능식품' in typ:
            out.append(_finding(rule, 'review', 'ad_review_scope', '기능과 광고 자료가 부족합니다.',
                       '허용 범위·대상 연령·심의를 확인하세요.', evidence))
    return out


def product_checks(doc):
    """제품 분류 자료와 실제 문안·경험을 함께 확인한다."""
    out = []
    commercial = bool(economic_relations(doc) or doc.get('content_type') in ('affiliate', 'sponsor'))
    text = '\n'.join((doc.get('title', ''), doc.get('description', ''), body_text(doc), doc.get('experience', '')))
    if commercial and not doc.get('product_records'):
        out.append(_finding('P1', 'review', 'product_records', '상업 글의 제품 분류 자료가 없습니다.',
                   '제품의 모델과 용도를 확인하세요.', ['BXF-044']))
    for product in doc.get('product_records', []):
        out.extend(_classification_checks(product, commercial))
        out.extend(_safety_checks(product))
        if commercial:
            out.extend(_advertising_checks(product, text))
    return out
