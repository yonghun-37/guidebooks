"""WordPress 일부 응답과 고정 JSON 상태를 구성한다."""
from datetime import datetime
from core.files import read_json, write_json


def load_state(root):
    path = root / 'private/mock-wp/state.json'
    return read_json(path) if path.exists() else {key: [] for key in (
        'posts', 'media', 'categories', 'tags')}


def save_state(root, state):
    write_json(root / 'private/mock-wp/state.json', state)


def select_rows(state, kind, ident, query, now):
    rows = state[kind]
    for row in rows if kind == 'posts' else []:
        if row['status'] == 'future' and row['date'] <= now:
            row['status'] = 'publish'
    if ident:
        return next((row for row in rows if row['id'] == ident), None)
    return [row for row in rows if (
        ('slug' not in query or row.get('slug') == query['slug'][0]) and
        ('search' not in query or query['search'][0] in row.get('name', '')) and
        ('status' not in query or row.get('status') in query['status'][0].split(',')))]


def upsert_post(state, data, ident, now):
    if data.get('status', 'draft') not in ('draft', 'future', 'publish'):
        raise ValueError('rest_invalid_param')
    if 'date' in data:
        datetime.fromisoformat(data['date'])
    rows = state['posts']
    row = next((item for item in rows if item['id'] == ident), None)
    if ident and row is None:
        raise ValueError('rest_post_invalid_id')
    if row is None:
        ident = max((item['id'] for item in rows), default=0) + 1
        row = {'id': ident, 'status': 'draft', 'date': now, 'slug': ''}
        rows.append(row)
    if 'slug' in data or not row['slug']:
        base = data.get('slug') or f'post-{ident}'
        slug, index = base, 2
        while any(item['id'] != ident and item['slug'] == slug for item in rows):
            slug, index = f'{base}-{index}', index + 1
        row['slug'] = slug
    row.update({key: value for key, value in data.items() if key != 'slug'})
    row['link'] = f'http://mock.local/?p={ident}'
    return row
