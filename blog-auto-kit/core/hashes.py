"""최종 내용과 이미지 바이트를 승인 해시에 함께 묶는다."""
import hashlib
import re
import unicodedata
from pathlib import Path
from core.files import json_text


def digest(data):
    return hashlib.sha256(data).hexdigest()


def content_hash(doc):
    text = unicodedata.normalize('NFKC', doc.get('html', ''))
    return digest(re.sub(r'\s+', ' ', text).strip().encode('utf-8'))


def approval_hash(root, doc):
    images = {}
    for item in doc.get('media', []):
        path = Path(root) / item['path']
        if not path.is_file():
            raise ValueError('이미지 파일 없음 → media.path를 실제 파일로 고치세요')
        images[item['path']] = digest(path.read_bytes())
    return digest(json_text({'document': doc, 'image_bytes': images}).encode('utf-8'))
