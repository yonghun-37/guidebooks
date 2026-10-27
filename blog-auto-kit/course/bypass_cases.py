"""무승인 발행과 금지 문안의 우회 시도를 묶어서 실행한다."""
from content.markdown import render
from content.samples import load_sample
from core.approval import approve_document
from monetize.affiliate import COUPANG
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft

TODAY = '2026-10-27'


def attacks(root):
    """건강·식별·제품·숨긴 표시·메타데이터의 검토 반례를 만든다."""
    docs = []
    for text in ('해열제에 관한 설명입니다.', '아스피린에 관한 설명입니다.',
                 '아기 발열에 관한 설명입니다.', '가상 아이의 이름은 테스트봄이이고 병원은 가상병원입니다.'):
        doc = load_sample('info'); doc['markdown'] += '\n\n' + text
        docs.append(doc)
    for typ in ('화장품', '건강기능식품', '의료기기'):
        doc = load_sample('affiliate'); doc['markdown'] = COUPANG + '\n\n' + doc['markdown']
        doc['product_records'][0]['product_type'] = typ
        if typ == '의료기기':
            doc.update(experience='제가 직접 써보니 편했습니다.', experience_by='human', comparison_only=True)
        else:
            doc['markdown'] += '\n\n감기를 예방합니다.'
        docs.append(doc)
    for text in ('제휴 활동 안내입니다.', COUPANG):
        doc = load_sample('affiliate'); doc['markdown'] = text + '\n\n' + doc['markdown']
        docs.append(doc)
    path = root / 'samples/renamed.png'; path.write_bytes((root / 'samples/fake-exif.jpg').read_bytes())
    from samples.make_images import chunk
    png = (root / 'samples/books.png').read_bytes()
    (root / 'samples/metadata.png').write_bytes(png[:33] + chunk(b'eXIf', b'II*\0\x08\0\0\0\0\0\0\0\0\0') + png[33:])
    for name in ('fake-exif.jpg', 'renamed.png', 'metadata.png'):
        doc = load_sample('info'); doc['media'][0]['path'] = 'samples/' + name; docs.append(doc)
    for i, doc in enumerate(docs):
        doc['content_id'] = 'bypass-' + str(i)
        doc['html'] = render(doc['markdown'])
    docs[8]['html'] = docs[8]['html'].replace('<p>', '<p style="display:none">', 1)
    return docs


def run_bypass_attempts(root, store):
    """approval/auto에서 준비·승인·발행 순서를 바꿔도 공개가 없는지 확인한다."""
    count = 0
    with running_server(root, port=0, today=TODAY) as url:
        client = Client(url)
        for doc in attacks(root):
            for mode in ('approval', 'auto'):
                try:
                    prepare_draft(root, store, client, doc, TODAY, ['info', 'play'])
                except ValueError:
                    pass
                # 금지/자료 보류는 승인 시도에도 닫히며, 건강/식별 review는 승인하지 않는다.
                if doc['content_type'] == 'affiliate':
                    try:
                        approve_document(root, store, doc, '가상 검토자', TODAY)
                    except ValueError:
                        pass
                    else:
                        raise AssertionError('금지 문안 승인 우회')
                try:
                    publish_draft(root, store, client, doc, TODAY, mode)
                except ValueError:
                    pass
                count += 1
        posts = client.request('GET', 'posts')
        assert all(row['status'] == 'draft' for row in posts)
    return f'우회 시도 {count}회: 무승인 future/publish 0건; 금지 문안 승인 거부'
