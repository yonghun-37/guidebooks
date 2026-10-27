"""로컬에서 고정 시계로 WordPress REST 일부를 흉내 낸다."""
import argparse
import base64
import hmac
import json
import re
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from wordpress.client import MOCK_PASSWORD
from wordpress.mock_data import load_state, save_state, select_rows, upsert_post


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def send_json(self, code, body):
        data = json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=UTF-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def authenticated(self):
        expected = 'Basic ' + base64.b64encode(
            ('mock-user:' + MOCK_PASSWORD).encode()).decode()
        if hmac.compare_digest(self.headers.get('Authorization', ''), expected):
            return True
        self.send_json(401, {'code': 'incorrect_password',
                            'message': 'The provided password is an invalid application password.',
                            'data': {'status': 401}})
        return False

    def do_GET(self):
        self.dispatch(False)

    def do_POST(self):
        self.dispatch(True)

    def dispatch(self, writing):
        if not self.authenticated():
            return
        parts = urlsplit(self.path)
        if not writing and self.read_media_file(parts.path):
            return
        route = parts.path.removeprefix('/wp-json/wp/v2/').strip('/').split('/')
        if route[0] not in ('posts', 'media', 'categories', 'tags'):
            self.send_json(404, {'code': 'rest_no_route', 'message': 'No route.', 'data': {'status': 404}})
            return
        try:
            ident = int(route[1]) if len(route) == 2 else None
            with self.server.state_lock:
                state = load_state(self.server.root)
                if writing:
                    body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                    result = self.write_item(state, route[0], ident, body)
                else:
                    result = select_rows(state, route[0], ident, parse_qs(parts.query),
                                         self.server.today + 'T23:59:59')
                save_state(self.server.root, state)
            if result is None:
                raise ValueError('rest_post_invalid_id')
            self.send_json(201 if writing and ident is None else 200, result)
        except (ValueError, KeyError, TypeError):
            self.send_json(400, {'code': 'rest_invalid_param', 'message': 'Invalid parameter.',
                                'data': {'status': 400}})

    def read_media_file(self, path):
        match = re.fullmatch(r'/wp-content/uploads/(\d+)\.bin', path)
        if not match:
            return False
        file = self.server.root / f'private/mock-wp/media/{int(match[1])}.bin'
        if not file.is_file():
            self.send_json(404, {'code': 'rest_invalid_id', 'message': 'Invalid media.',
                                 'data': {'status': 404}})
            return True
        data = file.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        return True

    def write_item(self, state, kind, ident, body):
        if kind == 'posts':
            return upsert_post(state, json.loads(body), ident, self.server.today + 'T00:00:00')
        rows = state[kind]
        data = json.loads(body) if kind != 'media' else {}
        found = next((row for row in rows if row.get('name') == data.get('name')), None)
        if found and kind != 'media':
            return found
        index = max((row['id'] for row in rows), default=0) + 1
        row = {'id': index, **data}
        if kind == 'media':
            path = self.server.root / f'private/mock-wp/media/{index}.bin'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            row.update({'source_url': f'/wp-content/uploads/{index}.bin',
                        'media_type': 'image', 'mime_type': self.headers['Content-Type']})
        rows.append(row)
        return row

@contextmanager
def running_server(root, port=8767, today='2026-10-27'):
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.state_lock = threading.Lock()
    server.root, server.today = Path(root), today
    worker = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.02}, daemon=True)
    worker.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown()
        worker.join()
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description='A1 mock WordPress(외부 접속 불가)')
    parser.add_argument('--port', type=int, default=8767)
    parser.add_argument('--today', default='2026-10-27')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    server.state_lock = threading.Lock()
    server.root, server.today = Path.cwd(), args.today
    print('✔ 통과: mock WordPress 준비', flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
