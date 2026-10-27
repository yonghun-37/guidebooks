"""실제 HTTP 왕복과 승인·중복 방지 동작을 검사한다."""
import copy
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.state import Store
from wordpress.client import Client, WPError
from wordpress.mock_server import running_server


class WordPressTests(unittest.TestCase):
    def test_authentication_and_slug_collision(self):
        with TemporaryDirectory() as folder, running_server(Path(folder), port=0) as url:
            client = Client(url)
            first = client.request('POST', 'posts', {'slug': 'same', 'status': 'draft'})
            second = client.request('POST', 'posts', {'slug': 'same', 'status': 'future',
                                                       'date': '2026-10-28T09:00:00'})
            self.assertEqual((first['slug'], second['slug']), ('same', 'same-2'))
            self.assertEqual(len(client.find_slug('same')), 1)
            with self.assertRaises(WPError) as caught:
                Client(url, password='bad').request('GET', 'posts')
            self.assertEqual(caught.exception.body['data']['status'], 401)
            self.assertEqual(caught.exception.body['code'], 'incorrect_password')

    def test_media_taxonomy_and_publication_status(self):
        with TemporaryDirectory() as folder, running_server(Path(folder), port=0) as url:
            client = Client(url)
            self.assertEqual(client.ensure_term('categories', '놀이'), 1)
            self.assertEqual(client.ensure_term('categories', '놀이'), 1)
            media = client.upload_media(b'<svg/>', 'drawing.svg', 'image/svg+xml')
            post = client.request('POST', 'posts', {'slug': 'test', 'status': 'draft',
                                                  'featured_media': media['id']})
            result = client.request('POST', f"posts/{post['id']}", {'status': 'publish'})
            self.assertEqual(result['status'], 'publish')
            self.assertEqual(client.request('GET', f"posts/{post['id']}")['id'], post['id'])

    def test_store_preserves_unique_run_lock(self):
        with TemporaryDirectory() as folder:
            store = Store(Path(folder))
            self.assertTrue(store.claim('one', {'state': 'sending'}))
            self.assertFalse(Store(Path(folder)).claim('one', {'state': 'sending'}))


if __name__ == '__main__':
    unittest.main()
