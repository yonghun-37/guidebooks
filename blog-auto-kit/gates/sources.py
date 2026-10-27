"""숫자 주장을 문장별 출처 메모와 연결해 검사한다."""
import re
from gates.checks import result


def numeric_claims(doc):
    """수치의 출처 ID와 해당 수치가 메모에 있는지 점검한다."""
    text = doc.get('markdown', '')
    text = re.sub(r'https?://\S+', '', text)
    notes = {str(n.get('id')): n for n in doc.get('source_notes', [])}
    out = []
    for paragraph in text.split('\n'):
        parts = re.split(r'(?<=\])\s+|(?<=[.!?。])\s+(?!\[)', paragraph)
        for sentence in parts:
            stripped = re.sub(r'\[[^\]]+\]', '', sentence)
            stripped = re.sub(r'20\d{2}년\s*(?:\d{1,2}월)?\s*(?:조사\s*기준)?', '', stripped)
            numbers = re.findall(r'\d+(?:\.\d+)?', stripped)
            if not numbers:
                continue
            ids = re.findall(r'\[([^\]]+)\]', sentence)
            claims = ' '.join(str(c) for i in ids if i in notes for c in notes[i].get('claims', []))
            normalized = re.sub(r'[^가-힣A-Za-z0-9]', '', stripped)
            matching = any(normalized and normalized in re.sub(r'[^가-힣A-Za-z0-9]', '', str(c)) for i in ids if i in notes for c in notes[i].get('claims', []))
            if not ids or not matching or not all(n in re.findall(r'\d+(?:\.\d+)?', claims) for n in numbers):
                out.append(result('sources.N1', 'review', 'markdown', '숫자 문장에 연결된 근거가 부족합니다.', '같은 문장에 출처 ID를 표시하고 수치와 주장을 출처 메모에 기록하세요.', ids, False))
    return out
