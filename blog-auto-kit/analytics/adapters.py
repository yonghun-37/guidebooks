"""주입된 전송 함수로 분석 응답을 읽는다."""
from datetime import date
from urllib.parse import quote


def request_report(url, body, transport):
    """OAuth 전송 함수에 요청을 맡기고 실패를 보류한다."""
    try:
        response = transport({'method': 'POST', 'url': url, 'body': body})
        if not isinstance(response, dict) or response.get('error'):
            raise ValueError('API 오류')
        return response, 'empty' if not response.get('rows') else 'ready'
    except (OSError, ValueError, TypeError):
        return {}, 'on_hold'


def check_period(start, end):
    """고정 형식의 집계 기간을 확인한다."""
    if date.fromisoformat(start) > date.fromisoformat(end):
        raise ValueError('집계 기간 오류 → 시작일을 종료일 이전으로 고치세요')


def fetch_ga4(property_id, start, end, transport):
    """GA4 행과 속성 시간대를 반환한다."""
    check_period(start, end)
    ident = str(property_id).removeprefix('properties/')
    body = {'dateRanges': [{'startDate': start, 'endDate': end}],
            'dimensions': [{'name': 'date'}, {'name': 'pagePath'}],
            'metrics': [{'name': name} for name in (
                'activeUsers', 'sessions', 'screenPageViews', 'engagementRate')],
            'returnPropertyQuota': True}
    url = 'https://analyticsdata.googleapis.com/v1beta/properties/' + quote(ident, safe='') + ':runReport'
    response, status = request_report(url, body, transport)
    return {'status': status, 'rows': response.get('rows', []),
            'timezone': response.get('metadata', {}).get('timeZone', '속성 설정 확인'),
            'empty': not bool(response.get('rows')), 'quota': response.get('propertyQuota', {}),
            'note': '빈 행·오류를 방문 0으로 바꾸지 않습니다'}


def fetch_gsc(site, start, end, transport):
    """GSC 행을 태평양 시간 기준과 지연 안내와 함께 반환한다."""
    check_period(start, end)
    body = {'startDate': start, 'endDate': end, 'dimensions': ['date', 'page'],
            'dataState': 'final', 'rowLimit': 1000, 'startRow': 0}
    url = 'https://www.googleapis.com/webmasters/v3/sites/' + quote(site, safe='') + '/searchAnalytics/query'
    response, status = request_report(url, body, transport)
    return {'status': status, 'rows': response.get('rows', []),
            'timezone': 'America/Los_Angeles', 'empty': not bool(response.get('rows')),
            'note': '데이터 반영 지연 가능; 상위 행만 제공하며 빈 행은 방문 0 확정이 아닙니다'}
