"""관문 결과와 예외 대기열을 파일로 기록한다."""
import json
from pathlib import Path
from difflib import SequenceMatcher
from content.schema import validate
from gates.checks import result, health_checks, privacy_checks, disclosure_checks
from gates.products import product_checks
from gates.body import consistent
from gates.sources import numeric_claims

def evaluate(doc: dict, recent: list = (), today='2026-10-27', daily_count=0, limit=2, root=None, config_path=None) -> list:
    """자료 부족, 고위험, 중복 및 상한을 점검한다."""
    out = []
    errors = validate(doc)
    if errors:
        out.append(result('schema', 'block', 'document', '; '.join(errors), '필수 필드를 수정하세요.', []))
    out.extend(health_checks(doc)); out.extend(privacy_checks(doc, root))
    out.extend(disclosure_checks(doc)); out.extend(product_checks(doc))
    from gates.links import link_checks
    out.extend(link_checks(doc, root, config_path))
    out.extend(numeric_claims(doc))
    if not consistent(doc):
        out.append(result('content.consistency', 'block', 'html', '최종 HTML과 원문이 다릅니다.', '최종 HTML을 다시 생성하고 검토하세요.', []))
    if not any(line.startswith('## ') for line in doc.get('markdown', '').splitlines()):
        out.append(result('seo.S1', 'review', 'markdown', '소제목이 없습니다.', '내용에 맞는 소제목을 넣으세요.', ['BXF-077'], False))
    if (not doc.get('source_notes') or not doc.get('author') or not doc.get('as_of') or not doc.get('title') or not doc.get('description') or any(not m.get('alt') for m in doc.get('media', []))):
        out.append(result('seo.S1', 'review', 'source_notes', '출처·작성자·기준일이 부족합니다.', '자료를 보완하세요.', ['BXF-077'], False))
    if doc.get('post_status') in ('unknown', 'pending'):
        out.append(result('duplicate.U2', 'review', 'post_status', '이전 요청의 결과가 불명확합니다.', '서버에서 기존 글을 조회하세요.', ['BXF-003'], False))
    if any('sponsored' not in link.get('rel', '').split() for link in doc.get('paid_links', [])):
        out.append(result('seo.S2', 'review', 'paid_links', '대가 링크의 속성이 누락되었습니다.', '편집 가능한 링크에 rel=sponsored를 넣으세요.', ['BXF-080'], False))
    if doc.get('spam_intent'):
        out.append(result('seo.S2', 'block', 'spam_intent', '순위 조작 목적의 콘텐츠입니다.', '행위를 중단하세요.', ['BXF-076']))
    if daily_count >= limit:
        out.append(result('seo.S3', 'review', 'daily_count', '설정한 발행 상한에 도달했습니다.', '다음 실행으로 연기하세요.', ['BXF-080'], False))
    text = ' '.join(doc.get('markdown', '').split())
    for old in recent:
        oldtext = ' '.join(old.get('markdown', '').split())
        if text and text == oldtext:
            out.append(result('duplicate.U1', 'block', 'markdown', '기존 글과 같습니다.', '기존 글을 확인하세요.', ['BXF-080']))
        elif text and oldtext and SequenceMatcher(None, text, oldtext).ratio() >= 0.9:
            out.append(result('duplicate.U3', 'review', 'markdown', '기존 글과 매우 비슷합니다.', '새로운 가치를 확인하세요.', ['BXF-080'], False))
    if not out:
        out.append(result('general', 'pass', 'document', '자동 검사에서 차단이나 검토 항목이 없습니다.', '발행 설정을 확인하세요.', []))
    return out

def write_report(root: Path, doc, results) -> None:
    """관문 결과와 해결 대기 목록을 저장한다."""
    output = Path(root) / 'output'; directory = output / 'gates'
    directory.mkdir(parents=True, exist_ok=True)
    ident = doc['content_id']
    if not ident or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in ident):
        raise ValueError('잘못된 content_id')
    (directory / (ident + '.json')).write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    (directory / (ident + '.txt')).write_text('\n'.join(f"{r['decision']} {r['rule_id']}: {r['reason_ko']} {r['next_action_ko']}" for r in results) + '\n', encoding='utf-8', newline='\n')
    queue = output / 'queue.json'
    items = json.loads(queue.read_text(encoding='utf-8')) if queue.exists() else []
    items = [x for x in items if x.get('content_id') != ident]
    items.extend({'content_id': ident, **r} for r in results if r['decision'] != 'pass')
    queue.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
