"""Claude 검수의 자유 문장 우회 10개를 실제 HTTP 발행 경로에서 막는다."""
import shutil, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from content.samples import load_sample
from content.markdown import render
from core.state import Store
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft
TODAY='2026-10-27'
CASES = [
 '[여기서 구매](https://link.coupang.com/a/abc123)',
 '체온이 38도를 넘으면 알아 두세요.',
 'If baby has a fever, read this.',
 '분유 1회 120ml를 먹여요.',
 '<p style="color:white">숨긴 글</p>',
 '![아이 사진](samples/fake-exif.jpg)',
 '해 열 제 설명',
 '봄이는 2026년 3월 14일에 태어났어요.',
 '서울 마포구 ○○어린이집에 다녀요.',
 '이 매트에서 재우면 질식 걱정이 없어요.',
]
@pytest.mark.parametrize('text', CASES)
def test_no_auto(tmp_path, text):
    shutil.copytree(ROOT/'samples', tmp_path/'samples')
    store = Store(tmp_path)
    doc = load_sample('info')
    doc.update(title='그림책 정리', description='책을 함께 읽는 순서', media=[])
    doc['markdown'] = '그림책을 정리해요.\n\n## 함께 읽기\n\n그림을 보며 이야기를 나눠요.\n\n' + text
    doc['html'] = render(doc['markdown'])
    with running_server(tmp_path, port=0, today=TODAY) as url:
        c = Client(url)
        # 먼저 정상 초안을 저장해 모든 반례에서 실제 draft 한 개를 확인한다.
        baseline = dict(doc, markdown=doc['markdown'][:-len(text)])
        baseline['html'] = render(baseline['markdown'])
        prepare_draft(tmp_path, store, c, baseline, TODAY, ['info'])
        try:
            prepare_draft(tmp_path, store, c, doc, TODAY, ['info'])
            publish_draft(tmp_path, store, c, doc, TODAY, 'auto')
        except ValueError:
            pass
        posts = c.request('GET', 'posts')
        assert len(posts) == 1 and all(p['status'] == 'draft' for p in posts), text
