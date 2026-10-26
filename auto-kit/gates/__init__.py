"""휴리스틱 관문. 통과가 사실 정확성·권리·플랫폼 허용 보장은 아니다."""
import re
import unicodedata
from pathlib import Path
from PIL import Image

def content_text(draft):
    return '\n'.join([draft['title'], draft['caption'], draft['narration']] + [s['title'] + ' ' + s['text'] for s in draft['scenes']])

def normalized(text):
    return unicodedata.normalize('NFKC', text).casefold()

def grams(text, n):
    text = re.sub(r'\s+', '', normalized(text))
    return {text[i:i+n] for i in range(max(1, len(text) - n + 1))}

def similarity(a, b, n=4):
    a, b = grams(a, n), grams(b, n)
    return len(a & b) / len(a | b) if a | b else 0

def verdict(reasons, **details):
    return {'passed': not reasons, 'reasons': reasons, **details}

def inspect_text(draft, source, recent, config):
    text, original = content_text(draft), source['text'] + ' ' + source.get('title', '')
    numbers = lambda t: set(re.findall(r'(?<!\w)[+-]?\d[\d,]*(?:\.\d+)?%?|\d+(?:\.\d+)?%?', normalized(t)))
    unknown_numbers = sorted(numbers(text) - numbers(original))
    # 라틴 이름/약어, 따옴표 이름, 대표 기관 접미사 + 모델 신고 entities를 함께 검사.
    names = set(re.findall(r'\b[A-Z][A-Za-z]+(?:[- ][A-Z][A-Za-z]+)*\b|[가-힣]{2,}(?:도서관|대학교|연구원|주식회사|위원회|재단)', text))
    names.update(re.findall(r'[“「]([^”」]{2,40})[”」]', text))
    names.update(draft['entities'])
    unknown_names = sorted(name for name in names if normalized(name) not in normalized(original))
    facts = ['원문에 없는 숫자: ' + ', '.join(unknown_numbers)] if unknown_numbers else []
    if unknown_names:
        facts.append('원문에 없는 이름: ' + ', '.join(unknown_names))
    policy = ['검토 단어: ' + word for word in config['blocked_words'] + config['sensitive_words'] if normalized(word) in normalized(text)]
    if len(draft['caption']) > config['max_caption_chars']:
        policy.append('문안 길이 상한 초과')
    scores = [similarity(text, previous, config['ngram']) for previous in recent]
    return {'facts': verdict(facts, method='숫자·이름 문자열 대조(문맥·한국어 인명 누락 가능)'), 'policy': verdict(policy),
            'similarity': verdict(['최근 게시물과 유사도가 높습니다.'] if scores and max(scores) >= config['similarity'] else [], maximum=max(scores, default=0), threshold=config['similarity'])}

def inspect_media(files, flow, config, target, *, probe=None):
    from rendering.media import probe_media
    probe = probe or probe_media
    reasons, details = [], []
    for file in files:
        file = Path(file)
        if file.suffix.lower() in ('.jpg', '.jpeg'):
            with Image.open(file) as image:
                w, h = image.size
                if image.format != 'JPEG' or not 320 <= w <= 1440 or not .8 <= w/h <= 1.91 or file.stat().st_size > config['max_image_bytes']:
                    reasons.append('JPEG 비율·너비·용량 검사 실패')
                details.append({'file': file.name, 'width': w, 'height': h, 'bytes': file.stat().st_size})
        elif file.suffix.lower() == '.mp4':
            info = probe(file)
            details.append({'file': file.name, **info})
            maximum = 180 if flow == 'shorts' else 900
            if info['width'] > info['height'] or info['duration'] < 3 or info['duration'] > maximum or info['video_codec'] != 'h264' or info['audio_codec'] != 'aac' or not 23 <= info['fps'] <= 60 or file.stat().st_size > config['max_video_bytes']:
                reasons.append('영상 비율·길이·코덱·fps·용량 검사 실패')
            lufs = info.get('lufs')
            if lufs is None or not config['lufs_min'] <= lufs <= config['lufs_max']:
                reasons.append('음량 LUFS 기본 범위 밖(무음 포함)')
        else:
            reasons.append('게시용 미디어 형식 불가')
    ai_fields = ('is_ai_generated',) if flow == 'insta' else ('containsSyntheticMedia', 'selfDeclaredMadeForKids')
    return {'specification': verdict(reasons, media=details), 'ai': verdict(['AI·아동용 필드를 Boolean으로 지정하세요.'] if any(type(target.get(key)) is not bool for key in ai_fields) else [])}
