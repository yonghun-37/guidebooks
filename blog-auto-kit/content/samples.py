"""가상 블로그 샘플과 별도의 사람 메모를 읽는다."""
import copy
import json
from pathlib import Path
from content.markdown import render

ROOT = Path(__file__).resolve().parents[1] / 'samples'

def load_sample(name: str) -> dict:
    """허용된 네 편의 샘플을 읽는다."""
    if name not in ('info', 'play', 'affiliate', 'sponsor'):
        raise ValueError('알 수 없는 샘플')
    doc = json.loads((ROOT / (name + '.json')).read_text(encoding='utf-8'))
    doc['markdown'] = (ROOT / (name + '.md')).read_text(encoding='utf-8')
    doc['html'] = render(doc['markdown'])
    return doc

def with_human_notes(doc: dict) -> dict:
    """가상 시연용 사람 메모를 복사본에 명시적으로 적용한다."""
    result = copy.deepcopy(doc)
    path = ROOT / (result['content_id'] + '-human.txt')
    if path.exists():
        result['experience'] = path.read_text(encoding='utf-8').strip()
        result['experience_by'] = 'human'
        result['markdown'] += '\n\n' + result['experience']
        result['html'] = render(result['markdown'])
    return result
