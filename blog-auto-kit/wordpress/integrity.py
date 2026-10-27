"""승인한 초안과 서버의 편집용 내용을 비교한다."""
from core.hashes import approval_hash, digest


def recent_documents(store, doc):
    """다른 공개·예약 글의 원문만 모은다."""
    return [row['doc'] for row in store.all('posts') if row.get('id') != doc['content_id'] and row.get('status') in ('future', 'publish') and row.get('doc')]


def require_draft_match(root, doc, row):
    """현재 원고와 이미지가 실제 준비한 초안과 같은지 확인한다."""
    if row.get('draft_hash') != approval_hash(root, doc):
        raise ValueError('준비한 초안이 변경됨 → publish --prepare를 다시 실행하세요')


def _raw(value):
    """WordPress 편집 응답과 mock의 문자열을 공통 형태로 읽는다."""
    return value.get('raw') if isinstance(value, dict) else value


def verify_remote(client, row):
    """서버 원고의 내용과 분류 및 대표 미디어를 확인한다."""
    remote = client.request('GET', f"posts/{row['post_id']}?context=edit")
    expected = row['snapshot']
    for key in ('slug', 'title', 'content', 'excerpt'):
        if _raw(remote.get(key)) != expected.get(key):
            raise ValueError('서버 원고 변경 → 초안을 다시 준비하고 승인하세요')
    for key in ('categories', 'tags', 'featured_media'):
        if remote.get(key) != expected.get(key):
            raise ValueError('서버 분류 또는 미디어 변경 → 초안을 다시 준비하세요')
    for ident, expected_hash in row.get('prepared', {}).get('media_hashes', {}).items():
        if digest(client.media_bytes(int(ident))) != expected_hash:
            raise ValueError('서버 사진 변경 → 미디어를 다시 준비하고 승인하세요')
    return remote
