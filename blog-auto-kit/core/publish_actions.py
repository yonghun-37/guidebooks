"""초안 저장·사람 승인·예약과 공개 확인 명령을 실행한다."""
from core.approval import inspect_document, require_ready, approve_document
from core.files import write_json
from core.workflow import read_document, wordpress_connection
from core.sponsor_flow import record_sponsor_approval, record_sponsor_remote
from wordpress.prepare import prepare_draft
from wordpress.publish import publish_draft, check_remote_status


def gate_action(root, store, args):
    doc = read_document(root, args.sample)
    results = inspect_document(root, doc, today=args.today, store=store)
    if args.approve:
        approval = approve_document(root, store, doc, args.approve, args.today)
        if doc['content_type'] == 'sponsor':
            record_sponsor_approval(root, store, approval, args.today)
        print('✔ 통과: 현재 최종본 사람 승인 · ' + approval['hash'][:12])
    else:
        require_ready(results)
        waiting = any(row['decision'] == 'review' for row in results)
        print('✔ 통과: 자동 검사 완료' + (' · 사람 검토 대기' if waiting else ''))
    print('output/gates/' + args.sample + '.txt')


def wordpress_action(root, store, config, args):
    if args.command == 'status' and getattr(args, 'costs', False):
        from decimal import Decimal
        print('✔ 통과: 비용 기록 읽기 · 예약과 확정은 같은 실행의 상태입니다')
        for row in store.all('costs'):
            amount = Decimal(row['micro_usd']) / Decimal(1000000)
            print(f"{row['run_id']} | {row['date']} | {row['status']} | {amount:.6f} USD")
        if not store.all('costs'):
            print('비용 기록 없음')
        return
    with wordpress_connection(root, config, args.live, args.today,
                              getattr(args, 'advance_days', 0)) as client:
        if client is None:
            write_json(root / 'output/request-plan.json', {'operation': args.command,
                       'sample': args.sample, 'dry_run': True})
            print('✔ 통과: 드라이런 요청 계획\noutput/request-plan.json')
            return
        if args.command == 'status':
            return status_action(root, store, client, args)
        doc = read_document(root, args.sample)
        if args.prepare:
            row = prepare_draft(root, store, client, doc, args.today,
                                config.get('publishing', {}).get('auto_allowed_types', []))
            row['daily_limit'] = config.get('publishing', {}).get('daily_limit', 2)
            store.put('posts', doc['content_id'], row)
        else:
            row = publish_draft(root, store, client, doc, args.today,
                                config.get('publishing', {}).get('mode', 'approval'))
            if doc['content_type'] == 'sponsor':
                record_sponsor_remote(root, store, row, args.today)
        print(f"✔ 통과: WordPress post_id={row['post_id']} · {row['status']}")
        print('private/state.sqlite3')


def status_action(root, store, client, args):
    remote = client.request('GET', 'posts?status=draft,future,publish')
    row = store.get('posts', args.sample)
    if row and row.get('post_id'):
        row = check_remote_status(store, client, row)
        if args.sample == 'sponsor':
            record_sponsor_remote(root, store, row, args.today)
    write_json(root / 'output/status.json', {'post_count': len(remote),
               'posts': [{key: r.get(key, '') for key in ('id', 'status', 'date', 'date_gmt', 'link')}
                         for r in remote]})
    print('✔ 통과: mock REST 연결' if args.mock else '✔ 통과: 서버 상태 재조회')
    print('output/status.json')
