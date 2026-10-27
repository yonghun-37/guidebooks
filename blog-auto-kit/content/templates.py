"""사람이 승인한 틀과 구조화 데이터로 만든 최종본을 다시 증명한다."""
import copy
import json
import re
from pathlib import Path
from string import Template
from content.markdown import render
from content.template_schema import check_schema, validate_data
from core.hashes import digest
from gates.links import allowed_domains, allowed_url, urls


def template_files(root, ident):
    if not isinstance(ident, str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,39}', ident):
        raise ValueError('틀 ID 형식 오류')
    base = Path(root) / 'content/templates'
    paths = base / (ident + '.md'), base / (ident + '.schema.json')
    if any(not path.resolve().is_relative_to(base.resolve()) for path in paths):
        raise ValueError('틀 경로 오류')
    return paths


def template_material(root, ident):
    markdown, schema_path = template_files(root, ident)
    raw, rules = markdown.read_bytes(), schema_path.read_bytes()
    schema = json.loads(rules)
    check_schema(schema)
    template = Template(raw.decode('utf-8'))
    if not template.is_valid() or set(template.get_identifiers()) != set(schema['properties']):
        raise ValueError('틀의 빈칸과 데이터 규칙의 칸이 다릅니다')
    return template, schema, {'template_hash': digest(raw), 'schema_hash': digest(rules)}


def approve_template(root, store, ident, reviewer, today):
    """승인 명령만 기록을 만든다. 생성·발행 명령은 스스로 승인하지 않는다."""
    if not reviewer.strip():
        raise ValueError('틀 검토자 이름이 필요합니다')
    _, _, hashes = template_material(root, ident)
    record = dict(hashes, id=ident, reviewer=reviewer, date=today)
    store.put('runs', 'template-approval:' + ident, record)
    return record


def template_document(root, ident, data, today, config_path=None):
    """공개할 모든 문장·제목·설명은 고정 틀과 코드에서만 만든다."""
    template, schema, _ = template_material(root, ident)
    validate_data(schema, data, allowed_domains(root, config_path))
    markdown = template.substitute(data)
    doc = {'content_id': ident, 'content_type': 'info', 'title': '이번 달 도서관 그림책 주제 목록',
           'description': '정해진 공공 자료 칸으로 만든 가상 그림책 주제 목록', 'author': '서윤(가상)',
           'as_of': today, 'markdown': markdown, 'html': render(markdown),
           'risk_flags': [], 'source_notes': [{'id': 'library', 'url': data['source_url'],
               'official': True, 'country': 'KR', 'checked_on': today, 'age_range': data['age_band'],
               'license': '링크 안내·가상 편집 목록', 'claims': []}],
           'experience': '', 'experience_by': '', 'photos': [], 'media': [],
           'commercial_relations': [], 'product_records': [], 'contract': {'ai_allowed': False},
           'emergency_topics': [], 'authoring_path': 'approved_template',
           'template_id': ident, 'template_data': copy.deepcopy(data)}
    return doc


def template_errors(root, store, doc, config_path=None):
    """발행 직전 현재 파일·승인·데이터·최종 바이트를 다시 확인한다."""
    if root is None or store is None or doc.get('authoring_path') != 'approved_template':
        return ['승인 틀로 만든 글이 아닙니다']
    try:
        ident = doc['template_id']
        _, _, hashes = template_material(root, ident)
        approval = store.get('runs', 'template-approval:' + ident, {})
        if not approval.get('reviewer') or any(approval.get(k) != v for k, v in hashes.items()):
            return ['틀·데이터 규칙의 현재 해시에 대한 사람 승인이 없습니다']
        expected = template_document(root, ident, doc['template_data'], doc['as_of'], config_path)
        if any(doc.get(k, '').encode('utf-8') != expected[k].encode('utf-8')
               for k in ('markdown', 'html', 'title', 'description')) or doc != expected:
            return ['최종본이 승인 틀과 데이터의 렌더 결과와 다릅니다']
        if any(not allowed_url(url, allowed_domains(root, config_path)) for url in urls(doc)):
            return ['본문에 허용 밖 URL이 있습니다']
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return ['틀 파일·데이터·설정 검증 실패']
    return []
