"""장별 명령을 해당 기능에 연결하고 생성 경로를 알려 준다."""
from core.files import write_json, write_text
from core.workflow import make_draft, read_document, save_document


def artifact_paths(root, paths):
    for path in paths:
        from pathlib import Path
        print(Path(path).relative_to(root).as_posix())


def content_action(root, store, config, args):
    if args.command == 'topics':
        from content.topics import build_topics
        write_json(root / 'output/topics.json', build_topics(args.today))
        print('✔ 통과: 주제 지도 생성\noutput/topics.json')
    else:
        make_draft(root, store, args.sample, args.today, args.human_notes,
                   config.get('provider', {}))
        print('✔ 통과: 초안 생성 · 경험은 사람 칸\noutput/drafts/' + args.sample + '.json')


def monetize_action(root, store, config, args):
    if args.command == 'pages':
        from monetize.pages import generate_pages
        paths = generate_pages(root, config.get('pages', {}), args.today)
    elif args.command == 'ads':
        from monetize.ads import build_ads
        settings = dict(config.get('ads', {}))
        paths = build_ads(root, settings, args.today)
    elif args.command == 'affiliate':
        from monetize.affiliate import register_link, prepare_affiliate
        if store.get('links', 'nail') is None:
            register_link(store, {'id': 'nail', 'url': 'https://example.invalid/nail',
                                  'program': '쿠팡(모의)', 'price': '표시하지 않음',
                                  'checked_on': args.today, 'check': 'mock 정상'})
        doc = prepare_affiliate(root, store, read_document(root, args.sample))
        save_document(root, doc)
        paths = [root / doc['registry']]
    elif args.command == 'sponsor':
        from monetize.sponsor.demo import run_sponsor_demo, export_reports
        from core.sponsor_flow import settle_sponsor, review_sponsor
        if args.action == 'settle':
            paths = settle_sponsor(root, store, args.today)
        elif args.action == 'review':
            paths = review_sponsor(root, store, args.today)
        elif args.action == 'demo':
            paths = run_sponsor_demo(root, store, args.today)
        else:
            paths = export_reports(root, store, args.today)
    else:
        from analytics.report import build_report
        paths = build_report(root, store, args.today)
    print('✔ 통과: ' + args.command + ' 생성')
    artifact_paths(root, paths)


def operations_action(root, store, args):
    from ops.backup import backup, restore
    if args.ops:
        from ops.notifications import notify
        from ops.scheduler import generate_schedule
        notify(root, 'approval_waiting', args.today)
        paths = generate_schedule(root)
        paths.append(backup(root))
        print('✔ 통과: 알림 드라이런·예약 예시·백업')
        artifact_paths(root, paths)
    elif args.restore:
        restore(root, root / 'output/backups/blog.zip')
        print('✔ 통과: SQLite·mock WordPress·설정 복구')
    elif args.audit:
        fields = '\n  확인자: \n  근거 파일·주소: \n  보류 이유·다음 확인일: \n'
        write_text(root / 'output/launch-checklist.txt',
                   '2026년 10월 조사 기준\n' + ''.join('[ ] ' + label + fields for label in (
                       '출처·저작권·제품 자료', '경제관계 첫부분 표시·실제 경험', '아동 정보·사진 사람 확인',
                       '개인정보 실제 흐름·광고코드 확인', '현물·부가세·사업자등록 국세청126 확인',
                       '육아휴직급여 소득활동 고용센터1350 확인')))
        print('✔ 통과: 출시 전 사람이 확인할 점검표\noutput/launch-checklist.txt')
    else:
        from course.scenarios import run_scenarios
        for name, result in run_scenarios(root).items():
            if not result['passed']:
                raise ValueError(name + ' 실패 → tests/test_scenarios.py를 확인하세요')
            print('✔ 통과: ' + name)
