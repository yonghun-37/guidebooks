"""서버 사진의 바이트가 바뀌면 예약을 회수하는지 확인한다."""
import shutil
from pathlib import Path
import pytest
from content.samples import load_sample
from core.approval import approve_document
from core.state import Store
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft


@pytest.mark.parametrize('scheduled', [False, True])
def test_remote_media_change_requires_upload_and_new_approval(tmp_path, scheduled):
    source = Path(__file__).resolve().parents[1]
    shutil.copytree(source / 'samples', tmp_path / 'samples')
    store, doc = Store(tmp_path), load_sample('info')
    with running_server(tmp_path, port=0) as url:
        client = Client(url)
        row = prepare_draft(tmp_path, store, client, doc, '2026-10-27')
        approve_document(tmp_path, store, doc, '서윤', '2026-10-27')
        if scheduled:
            publish_draft(tmp_path, store, client, doc, '2026-10-27')
        (tmp_path / 'private/mock-wp/media/1.bin').write_bytes(b'modified server image')
        with pytest.raises(ValueError, match='서버 사진 변경'):
            publish_draft(tmp_path, store, client, doc, '2026-10-27')
        assert client.request('GET', f"posts/{row['post_id']}")['status'] == 'draft'
        assert not store.get('posts', 'info').get('approval')
        updated = prepare_draft(tmp_path, store, client, doc, '2026-10-27')
        assert updated['post_id'] == row['post_id']
        approve_document(tmp_path, store, doc, '서윤', '2026-10-27')
        assert publish_draft(tmp_path, store, client, doc, '2026-10-27')['status'] == 'future'
