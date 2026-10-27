"""자유 문장을 표현하지 못하는 닫힌 JSON Schema 부분집합만 검증한다."""
from urllib.parse import urlsplit


def check_schema(schema):
    """알 수 없는 키워드·중첩·자유 문자열은 승인 단계부터 거절한다."""
    keys = {'$schema', 'type', 'additionalProperties', 'required', 'properties'}
    if (not isinstance(schema, dict) or set(schema) - keys or schema.get('type') != 'object'
            or schema.get('additionalProperties') is not False):
        raise ValueError('틀 데이터 규칙은 닫힌 객체여야 합니다')
    props, required = schema.get('properties'), schema.get('required')
    if (not isinstance(props, dict) or not props or not isinstance(required, list)
            or any(not isinstance(k, str) or not k.isidentifier() for k in props)
            or any(not isinstance(k, str) for k in required)
            or set(required) != set(props) or len(required) != len(props)):
        raise ValueError('틀의 모든 칸을 필수 항목으로 정하세요')
    for rule in props.values():
        check_scalar(rule)


def check_scalar(rule):
    """문자열은 짧은 열거값, 정수는 유한 구간으로 제한한다."""
    keys = {'type', 'enum', 'minLength', 'maxLength', 'minimum', 'maximum', 'format'}
    if not isinstance(rule, dict) or set(rule) - keys:
        raise ValueError('지원하지 않는 데이터 규칙입니다')
    if rule.get('type') == 'string':
        values = rule.get('enum')
        low, high = rule.get('minLength'), rule.get('maxLength')
        if (not isinstance(values, list) or not values or type(low) is not int
                or type(high) is not int or not 1 <= low <= high <= 200
                or any(not isinstance(v, str) or not low <= len(v) <= high or '\n' in v
                       or '\r' in v for v in values)):
            raise ValueError('자유 문장 칸 금지 → 길이 제한과 열거값을 정하세요')
        if rule.get('format') not in (None, 'uri'):
            raise ValueError('지원하지 않는 문자열 형식입니다')
    elif rule.get('type') == 'integer':
        low, high = rule.get('minimum'), rule.get('maximum')
        if type(low) is not int or type(high) is not int or low > high:
            raise ValueError('정수 칸에 최소·최대값이 필요합니다')
        values = rule.get('enum', [])
        if not isinstance(values, list) or ('enum' in rule and not values) or any(
                type(v) is not int or not low <= v <= high for v in values):
            raise ValueError('정수 열거값에 불리언·구간 밖 값은 쓸 수 없습니다')
    else:
        raise ValueError('틀은 열거 문자열·구간 정수 칸만 지원합니다')


def validate_data(schema, data, allowed_domains):
    """필드·타입·길이·열거값·URL 도메인을 렌더 전에 확인한다."""
    from gates.links import allowed_url
    check_schema(schema)
    if not isinstance(data, dict) or set(data) != set(schema['properties']):
        raise ValueError('틀 데이터의 정해진 칸만 채우세요')
    for key, rule in schema['properties'].items():
        value = data[key]
        if rule['type'] == 'string':
            if (not isinstance(value, str) or not rule['minLength'] <= len(value) <= rule['maxLength']
                    or value not in rule['enum']):
                raise ValueError(key + ': 허용된 짧은 열거값이 아닙니다')
            if rule.get('format') == 'uri' and not allowed_url(value, allowed_domains):
                raise ValueError(key + ': 허용 기관의 HTTPS URL만 쓰세요')
        elif type(value) is not int or not rule['minimum'] <= value <= rule['maximum']:
            raise ValueError(key + ': 정수 구간을 벗어났습니다')
        if 'enum' in rule and value not in rule['enum']:
            raise ValueError(key + ': 허용 밖 값입니다')
