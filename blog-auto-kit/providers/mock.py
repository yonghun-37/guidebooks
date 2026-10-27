"""네트워크 없이 샘플 초안을 만든다."""
from content.samples import load_sample


def draft_sample(name, today):
    """샘플의 경험과 사진을 비운 초안을 반환한다."""
    doc = dict(load_sample(name))
    doc.update(as_of=today, experience='', experience_by='', photos=[])
    return doc
