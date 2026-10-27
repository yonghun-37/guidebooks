"""다른 ID의 동일 내용도 동시에 중복 예약하지 못하게 한다."""
from concurrent.futures import ThreadPoolExecutor
from core.state import Store
from wordpress.quota import reserve_slot


def test_concurrent_content_hash_reservations_have_one_owner(tmp_path):
    store = Store(tmp_path)
    def reserve(ident):
        try:
            reserve_slot(store, 'mock', ident, '2026-10-27', 2, content_digest='same-content')
            return True
        except ValueError:
            return False
    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(reserve, ['one', 'two']))
    assert sum(outcomes) == 1
