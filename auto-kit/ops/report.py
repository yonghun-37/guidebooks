"""토큰/원응답을 제외한 정적 대시보드와 일일 보고."""
from html import escape
from common import now, save_json

def report(store, config):
    runs, spend = store.runs(), store.spend()
    today = now().date().isoformat()
    rows = []
    for run in runs:
        gates = ', '.join(name + (' ✓' if result['passed'] else ' ✕') for name, result in run.get('gates', {}).items())
        metrics = ', '.join(f'{r[0]}={"미준비" if r[1] is None else r[1]} {r[2]}' for r in store.db.execute('SELECT metric,value,unit FROM metrics WHERE run_id=?', (run['id'],)))
        quota=run.get('quota',{})
        used,total=quota.get('usage',quota.get('local_usage')),quota.get('total',quota.get('local_limit'))
        quota_html=f'<meter min="0" max="{total}" value="{used}">{used}/{total}</meter> {used}/{total}' if used is not None and total else '미확인'
        rows.append(f'<tr><td><a href="{run["id"]}/preview.html">{run["id"]}</a></td><td>{escape(run["flow"])}</td><td>{escape(run["status"])}</td><td>{escape(gates)}</td><td>{run.get("generation_cost",0):.6f}</td><td>{quota_html}</td><td>{escape(metrics)}</td></tr>')
    day_ratio = min(1, spend['day'] / config['budget']['daily_usd'])
    month_ratio = min(1, spend['month'] / config['budget']['monthly_usd'])
    chart = f'<svg viewBox="0 0 600 140" role="img" aria-label="일 월 예산 사용"><text x="8" y="24" fill="currentColor">일 ${spend["day"]:.4f} / {config["budget"]["daily_usd"]}</text><rect x="8" y="36" width="580" height="14" fill="#888"/><rect x="8" y="36" width="{580*day_ratio}" height="14" fill="#319a89"/><text x="8" y="88" fill="currentColor">월 ${spend["month"]:.4f} / {config["budget"]["monthly_usd"]}</text><rect x="8" y="100" width="580" height="14" fill="#888"/><rect x="8" y="100" width="{580*month_ratio}" height="14" fill="#db9d4f"/></svg>'
    html = '<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>자동화 운영 대시보드</title><style>:root{color-scheme:light dark}body{font:16px/1.7 system-ui;max-width:1200px;margin:auto;padding:20px}table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #888;text-align:left}a{color:inherit}svg{max-width:600px}.scroll{overflow:auto}</style><h1>자동화 운영 대시보드</h1><p>갱신 ' + today + ' · 비용 USD · 로컬 비공개 문서. mock 지표는 가상값입니다.</p>' + chart + '<p>한도는 조회 당시 스냅샷. YouTube는 사용자가 확인한 로컬 cap이며 Cloud 실시간 총량이 아닙니다.</p><div class="scroll"><table><tr><th>실행/미리보기</th><th>흐름</th><th>상태</th><th>관문</th><th>생성비</th><th>한도 사용/총량</th><th>지표</th></tr>' + ''.join(rows) + '</table></div></html>'
    (store.root / 'dashboard.html').write_text(html, encoding='utf-8')
    summary = {'date': today, 'runs': len([r for r in runs if r['created_at'].startswith(today)]), 'total_runs':len(runs), 'exceptions': [r['id'] for r in runs if r['status'] in ('failed','exception','uncertain')], 'spend': spend}
    save_json(store.root / 'daily-report.json', summary)
    return summary
