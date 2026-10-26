"""승인을 콘텐츠·파일·대상·공개범위·AI·시각에 결합한다."""
from datetime import timedelta
from common import digest, hashed, now, timestamp, save_json, read_json
from pathlib import Path

def binding(run):
    output = Path(run['output'])
    documents = [output / 'draft.json', output / 'config.json']
    files = {p.relative_to(output).as_posix(): digest(p) for p in [*map(Path, run['files']), *documents]}
    return hashed({'content': run['draft'], 'files': files, 'target': run['target'], 'flow': run['flow'], 'live': run['live'], 'publish_at': run.get('publish_at'), 'urls': run.get('hosting', {}).get('urls', []), 'cost': run.get('generation_cost')})

def approve(run, actor='local'):
    if run['status'] != 'waiting_approval' or not run.get('gate_passed'):
        raise ValueError('관문을 통과한 승인 대기 실행만 승인할 수 있습니다.')
    if binding(run) != run['binding']:
        raise ValueError('승인 대상 파일이 바뀌었습니다. 새 실행으로 검수하세요.')
    record = {'binding': run['binding'], 'actor': actor, 'approved_at': now().isoformat(), 'expires_at': (now() + timedelta(hours=run['config']['review']['approval_expiry_hours'])).isoformat()}
    save_json(Path(run['output']) / 'APPROVED.json', record)
    run['approval'] = record

def require_approval(run):
    if binding(run) != run['binding']:
        raise ValueError('승인/관문 이후 콘텐츠·파일·대상이 바뀌었습니다.')
    if run['config']['mode'] == 'approval':
        record = run.get('approval', {})
        path = Path(run['output']) / 'APPROVED.json'
        if not path.is_file() or read_json(path) != record or record.get('binding') != run['binding'] or timestamp(record['expires_at']) <= now():
            raise ValueError('승인이 없거나 만료·변경되었습니다. 다시 승인하세요.')
