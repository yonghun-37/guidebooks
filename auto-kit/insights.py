"""지표를 long-form CSV로 저장. missing과 0을 구별한다."""
import argparse
import csv
from pathlib import Path
from common import now, cli, load_config, kit_path
from state import Store
from transport import HTTP

UNITS = {'views': '회', 'engagedViews': '회', 'reach': '계정', 'saved': '회', 'shares': '회', 'estimatedMinutesWatched': '분', 'averageViewDuration': '초'}

def collect(store, run, *, live=False, http=None, session=None, start=None, end=None):
    collected = now().isoformat()
    day = now().date().isoformat()
    metrics = ['views', 'reach', 'saved', 'shares'] if run['flow'] == 'insta' else ['views', 'engagedViews', 'estimatedMinutesWatched']
    values = []
    if not live:
        values = [(day, metric, 12 if metric == 'views' else (0 if metric in ('saved', 'engagedViews') else None)) for metric in metrics]
    elif run['flow'] == 'insta':
        from ops.tokens import instagram_token
        token = instagram_token(run['config'])['access_token']
        base = f"https://graph.instagram.com/{run['config']['instagram']['api_version']}"
        # 지원되지 않는 한 metric이 전체 수집을 막지 않도록 각각 조회한다.
        for metric in metrics:
            raw = (http or HTTP()).json('GET', base + '/' + run['result']['id'] + '/insights', params={'metric': metric}, headers={'Authorization': 'Bearer ' + token})
            data = raw.get('data', [])
            point = data[0].get('values', []) if data else []
            value = point[-1].get('value') if point else (data[0].get('total_value', {}).get('value') if data else None)
            values.append((day, metric, value))
    else:
        from ops.tokens import google_session
        session = session or google_session(run['config'], analytics=True)
        response = session.request('GET', 'https://youtubeanalytics.googleapis.com/v2/reports', params={'ids': 'channel==MINE', 'startDate': start or day, 'endDate': end or day, 'metrics': ','.join(metrics), 'dimensions': 'day', 'filters': 'video==' + run['result']['id']}, timeout=60, allow_redirects=False)
        if response.status_code != 200:
            raise ValueError('YouTube Analytics 권한·지표 조합을 확인하세요.')
        data = response.json()
        names = [column['name'] for column in data.get('columnHeaders', [])]
        for row in data.get('rows', []):
            point = dict(zip(names, row))
            values.extend((point['day'], metric, point.get(metric)) for metric in metrics)
        if not values:
            values = [(end or day, metric, None) for metric in metrics]
    rows = []
    for date, metric, value in values:
        if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool)):
            value = None
        row = {'run_id': run['id'], 'flow': run['flow'], 'media_id': run.get('result', {}).get('id', 'dry-run'), 'date': date, 'metric': metric, 'value': '' if value is None else value, 'unit': UNITS[metric], 'availability': 'missing' if value is None else 'available', 'collected_at': collected, 'mock': not live}
        rows.append(row)
        store.db.execute('INSERT OR REPLACE INTO metrics VALUES(?,?,?,?,?,?)', (run['id'], metric, value, UNITS[metric], date, collected))
    path = Path(run['output']) / 'insights.csv'
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    return {'csv': str(path), 'rows': len(rows), 'mock': not live, 'note': 'Instagram 최대 48시간 지연·YouTube 마지막 준비 날짜. 빈 값은 0이 아님.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('id'); parser.add_argument('--state', default='private/state'); parser.add_argument('--live', action='store_true'); parser.add_argument('--start'); parser.add_argument('--end')
    args = parser.parse_args(); store = Store(kit_path(args.state)); run = store.get(args.id)
    if args.live and (not run['live'] or not run.get('result', {}).get('id')):
        raise ValueError('실제 게시 ID가 있는 live 실행만 지표를 조회할 수 있습니다.')
    collect(store, run, live=args.live, start=args.start, end=args.end)
    print('지표 CSV 저장 완료. missing은 나중에 다시 조회하세요.')

if __name__ == '__main__': cli(main)
