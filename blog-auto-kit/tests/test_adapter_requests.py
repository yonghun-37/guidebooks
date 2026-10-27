"""분석 API 요청의 주소·기간·지표와 실패 상태를 확인한다."""
from analytics.adapters import fetch_ga4, fetch_gsc


def test_requests_use_official_paths_and_keep_quota():
    seen = []
    def transport(request):
        seen.append(request)
        return {'rows': [], 'propertyQuota': {'tokensPerDay': {'remaining': 123}}}
    ga = fetch_ga4('123', '2026-10-01', '2026-10-27', transport)
    fetch_gsc('sc-domain:example.invalid', '2026-10-01', '2026-10-27', transport)
    assert seen[0]['url'].endswith('/v1beta/properties/123:runReport')
    assert seen[0]['body']['returnPropertyQuota'] is True
    assert ga['quota']['tokensPerDay']['remaining'] == 123
    assert 'sc-domain%3Aexample.invalid/searchAnalytics/query' in seen[1]['url']
    assert seen[1]['body']['dataState'] == 'final'


def test_transport_error_is_held_instead_of_zero():
    def failed(request):
        raise OSError('simulated')
    result = fetch_ga4('123', '2026-10-01', '2026-10-27', failed)
    assert result['status'] == 'on_hold'
    assert result['rows'] == []
