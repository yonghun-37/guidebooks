"""구조화된 초안 응답을 안전하게 처리한다."""
import json


def _matches(value, schema):
    """지원하는 JSON 스키마의 구조와 필수 필드를 확인한다."""
    types = {'object': dict, 'array': list, 'string': str, 'integer': int,
             'number': (int, float), 'boolean': bool, 'null': type(None)}
    kind = schema.get('type')
    if kind in types and (not isinstance(value, types[kind]) or
                          kind in ('integer', 'number') and isinstance(value, bool)):
        return False
    if 'enum' in schema and value not in schema['enum']:
        return False
    if isinstance(value, dict):
        properties = schema.get('properties', {})
        if any(key not in value for key in schema.get('required', [])):
            return False
        if schema.get('additionalProperties') is False and any(key not in properties for key in value):
            return False
        return all(_matches(item, properties[key]) for key, item in value.items() if key in properties)
    if isinstance(value, list) and 'items' in schema:
        return all(_matches(item, schema['items']) for item in value)
    return True


def draft(prompt, schema, contract, transport):
    """계약 허용을 확인한 뒤 주입된 전송 함수로 초안을 요청한다."""
    if contract.get('ai_allowed') is not True:
        return {'status': 'on_hold', 'reason': 'AI 사용 허용 미확인: 사람 작성 가능'}
    request = {'model': 'gpt-6-luna', 'input': prompt, 'text': {'format': {
        'type': 'json_schema', 'name': 'draft', 'strict': True, 'schema': schema}}}
    try:
        response = transport(request)
        if response.get('status') != 'completed':
            return {'status': 'on_hold', 'reason': '응답 미완성'}
        contents = [c for item in response.get('output', []) for c in item.get('content', [])]
        if any(c.get('type') == 'refusal' for c in contents):
            return {'status': 'on_hold', 'reason': '응답 거절'}
        text = next(c['text'] for c in contents if c.get('type') == 'output_text')
        data = json.loads(text)
        if not isinstance(data, dict) or not _matches(data, schema):
            raise ValueError('객체가 아님')
        return {'status': 'ready', 'data': data}
    except (KeyError, StopIteration, ValueError, TypeError, OSError):
        return {'status': 'on_hold', 'reason': '응답 해석 실패'}
