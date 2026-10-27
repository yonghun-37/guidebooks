"""제품의 분류 자료와 명시적 거절 조건을 검사한다."""
from gates.checks import result
from gates.body import body_text

def product_checks(doc):
    """제품별 금지와 자료 부족을 구분한다."""
    out = []
    if doc.get('commercial_relations') and not doc.get('product_records'):
        out.append(result('product_rules.P1', 'review', 'product_records', '상업 글의 제품 분류 자료가 없습니다.', '제품의 모델과 용도를 확인하세요.', ['BXF-044'], False))
    for product in doc.get('product_records', []):
        typ = product.get('product_type', ''); use = product.get('intended_use', '')
        missing = [k for k in ('product_type', 'intended_use', 'model', 'maker') if not product.get(k)]
        if missing:
            out.append(result('product_rules.P1', 'review', 'product_records', '제품 분류 정보가 부족합니다.', '모델과 업체, 용도를 확인하세요.', ['BXF-044'], False))
        if doc.get('commercial_relations') and any(w in typ for w in ('조제유', '조제분유', '영아용 조제식')):
            out.append(result('product_rules.P2', 'block', 'product_type', '조제유류 판매촉진은 거절합니다.', '협찬 또는 제휴를 거절하세요.', ['BXF-041', 'BXF-042']))
        checks = ('certification_scheme', 'recall_check', 'ad_review_scope')
        if any(not product.get(k) or product.get(k) in ('unknown', '미확인') for k in checks):
            out.append(result('product_rules.P3', 'review', 'product_records', '인증·리콜·광고 자료가 부족합니다.', '해당 모델의 자료를 확인하세요.', ['BXF-044'], False))
        if '리콜 확인' in str(product.get('recall_check', '')):
            out.append(result('product_rules.P3', 'block', 'recall_check', '해당 모델의 리콜이 확인되었습니다.', '사용과 홍보를 중단하세요.', ['BXF-097']))
        if (any(x in typ + use for x in ('낮잠 이불', '낮잠이불', '수면 베개', '수면베개', '범퍼')) or (any(x in use for x in ('수면', '잠자리', '낮잠')) and any(x in typ for x in ('베개', '이불', '쿠션')))):
            out.append(result('product_rules.P7', 'block', 'intended_use', '안전 수면 원칙과 충돌합니다.', '협찬을 거절하세요.', ['BXF-050']))
        text = body_text(doc)
        forbidden = any(w in text for w in ('질병을 치료', '질환을 치료', '치료합니다', '완치', '의약품과 같은'))
        if '화장품' in typ and forbidden:
            out.append(result('product_rules.P4', 'block', 'markdown', '화장품의 치료·의약품 오인 표현입니다.', '금지 표현을 삭제하세요.', ['BXF-045']))
        elif '화장품' in typ and product.get('ad_review_scope') in ('unknown', '미확인', ''):
            out.append(result('product_rules.P4', 'review', 'ad_review_scope', '화장품 광고 자료가 부족합니다.', '허용 범위와 안전 자료를 확인하세요.', ['BXF-046'], False))
        if '의료기기' in typ and doc.get('commercial_relations'):
            if not doc.get('comparison_only'):
                out.append(result('product_rules.P5', 'block', 'product_type', '의료기기 체험담 광고를 차단합니다.', '광고를 거절하세요.', ['BXF-047']))
            elif product.get('ad_review_scope') in ('unknown', '미확인', ''):
                out.append(result('product_rules.P5', 'review', 'ad_review_scope', '의료기기 광고 심의 범위가 불명확합니다.', '품목과 매체별 심의를 확인하세요.', ['BXF-048'], False))
        if '건강기능식품' in typ:
            if forbidden:
                out.append(result('product_rules.P6', 'block', 'markdown', '질병 치료 효능 표현입니다.', '금지 표현을 제거하세요.', ['BXF-049']))
            elif product.get('ad_review_scope') in ('unknown', '미확인', ''):
                out.append(result('product_rules.P6', 'review', 'ad_review_scope', '기능과 광고 심의 자료가 부족합니다.', '대상 연령과 심의를 확인하세요.', ['BXF-049'], False))
    for item in out:
        item['classification'] = ('자료 보류' if item['decision'] == 'review' else ('프로젝트 거절' if item['rule_id'] == 'product_rules.P7' else '법적 금지'))
    return out
