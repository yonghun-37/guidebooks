"""실제 로컬 mock HTTP를 이용한 여섯 검증 사례."""
import copy
import json
from pathlib import Path
from content.markdown import render
from core.approval import approve_document
from gates.engine import evaluate
from ops.backup import backup, restore
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft

TODAY = '2026-10-27'


def info(root):
    """복사된 정보 글 자료를 읽는다."""
    doc = json.loads((root / 'samples/info.json').read_text(encoding='utf-8'))
    doc['markdown'] = (root / 'samples/info.md').read_text(encoding='utf-8')
    doc['html'] = render(doc['markdown'])
    return doc


def mock_normal(root, store):
    """초안과 사람 승인 뒤 예약하고 날짜를 넘겨 공개를 확인한다."""
    doc = info(root)
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url); row = prepare_draft(root, store, client, doc, TODAY)
        approve_document(root, store, doc, '가상 검토자', TODAY)
        scheduled = publish_draft(root, store, client, doc, TODAY)
        assert scheduled['status'] == 'future'
    with running_server(root, port=0, today='2026-10-29') as url:
        remote = Client(url).request('GET', f"posts/{row['post_id']}")
        assert remote['status'] == 'publish'
    return 'mock 초안·사람 승인·예약 후 고정 시계 10월 29일 공개 확인'


def _product_doc(root, product):
    """제휴 제품 검사에 쓸 문서를 만든다."""
    doc = info(root)
    doc.update(content_type='affiliate', commercial_relations=[{'kind': 'affiliate', 'program': '가상', 'brand': '가상', 'details': '수수료'}], product_records=[product])
    return doc


def regulated_refusal(root, store):
    """조제유류 판매촉진의 승인 시도를 차단한다."""
    product = {'product_type': '조제유류', 'intended_use': '수유', 'model': '가상 A', 'maker': '가상', 'certification_scheme': '확인', 'recall_check': '확인', 'ad_review_scope': '확인', 'recall_status': 'none_found', 'classification_basis': '가상 품목 자료: 조제유류', 'regulated_category': 'infant_formula'}
    doc = _product_doc(root, product)
    results = evaluate(doc, today=TODAY)
    assert any(r['rule_id'] == 'product_rules.P2' and r['decision'] == 'block' for r in results)
    with running_server(root, port=0) as url:
        try: prepare_draft(root, store, Client(url), doc, TODAY)
        except ValueError: pass
        else: raise AssertionError('규제 제품이 초안 관문을 통과함')
        try: approve_document(root, store, doc, '가상 검토자', TODAY)
        except ValueError: pass
        else: raise AssertionError('규제 제품이 승인됨')
        assert Client(url).request('GET', 'posts') == []
    return '조제유류 판매촉진 차단·사람 승인 거부·서버 글 0개'


def missing_data(root, store):
    """제품 모델·인증 자료 누락을 검토 대기로 구분한다."""
    doc = _product_doc(root, {'product_type': '그림책꽂이', 'intended_use': '정리', 'maker': '가상'})
    results = evaluate(doc, today=TODAY)
    assert any(r['decision'] == 'review' and not r.get('human_resolvable') and r['rule_id'].startswith('product_rules') for r in results)
    with running_server(root, port=0) as url:
        try: prepare_draft(root, store, Client(url), doc, TODAY)
        except ValueError: pass
        else: raise AssertionError('자료 없는 제품을 보류하지 않음')
        assert Client(url).request('GET', 'posts') == []
    return '모델·인증 자료 누락: 제품 관문 검토 대기, 서버 글 0개'


def reapproval(root, store):
    """승인 후 변경을 차단하고 같은 글에 재승인한다."""
    doc = info(root)
    with running_server(root, port=0) as url:
        client = Client(url); row = prepare_draft(root, store, client, doc, TODAY)
        approve_document(root, store, doc, '가상 검토자', TODAY)
        revised = copy.deepcopy(doc)
        revised['markdown'] += '\n\n가상 내용 수정'
        revised['html'] = render(revised['markdown'])
        try: publish_draft(root, store, client, revised, TODAY)
        except ValueError: pass
        else: raise AssertionError('수정 후 재승인 없이 예약됨')
        updated = prepare_draft(root, store, client, revised, TODAY)
        assert row['post_id'] == updated['post_id']
        approve_document(root, store, revised, '가상 검토자', TODAY)
        scheduled = publish_draft(root, store, client, revised, TODAY)
        assert scheduled['status'] == 'future'
    return 'HTML 수정 후 예약 거부·같은 post_id 재승인 후 예약'


class LostResponse(Client):
    """첫 글 생성 응답만 유실시켜 조회 복구를 검사한다."""
    def __init__(self, url):
        super().__init__(url); self.lost = False
    def request(self, method, route, data=None, headers=None):
        response = super().request(method, route, data, headers)
        if method == 'POST' and route == 'posts' and not self.lost:
            self.lost = True
            raise TimeoutError('가상 응답 유실')
        return response


def timeout_no_duplicate(root, store):
    """생성 직후 응답 유실을 조회로 복구하고 중복을 확인한다."""
    doc = info(root)
    with running_server(root, port=0) as url:
        client = LostResponse(url); first = prepare_draft(root, store, client, doc, TODAY)
        second = prepare_draft(root, store, client, doc, TODAY)
        posts = client.request('GET', 'posts')
        assert client.lost and first['post_id'] == second['post_id'] and len(posts) == 1
    return '생성 응답 유실 후 슬러그 조회 복구, 재실행해도 서버 글 1개'


def backup_restore(root, store):
    """DB와 mock 미디어를 변조한 뒤 백업으로 복원한다."""
    with running_server(root, port=0) as url:
        client = Client(url)
        client.upload_media(b'fixed media bytes', 'demo.svg', 'image/svg+xml')
        store.put('posts', 'restore-check', {'value': 'original'})
        media = root / 'private/mock-wp/media/1.bin'; original = media.read_bytes()
        archive = backup(root)
        store.put('posts', 'restore-check', {'value': 'damaged'}); media.write_bytes(b'damaged')
        restore(root, archive)
        assert store.get('posts', 'restore-check') == {'value': 'original'}
        assert media.read_bytes() == original
        assert len(client.request('GET', 'media')) == 1
    return 'SQLite 논리 데이터와 mock 미디어 바이트 복구 확인'


def bypass_attempts(root, store):
    """두 독립 검토의 우회 반례를 실제 HTTP 경로로 묶어 확인한다."""
    from course.bypass_cases import run_bypass_attempts
    return run_bypass_attempts(root, store)
