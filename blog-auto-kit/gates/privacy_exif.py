"""JPEG의 EXIF 세그먼트를 검사하고 제거한다."""
def _segments(data: bytes):
    """JPEG 헤더 세그먼트를 엄격하게 순회한다."""
    if not data.startswith(b'\xff\xd8'):
        raise ValueError('JPEG 파일이 아닙니다')
    pos = 2
    while pos < len(data):
        if data[pos] != 255 or pos + 1 >= len(data):
            raise ValueError('손상된 JPEG 세그먼트')
        start = pos
        while pos < len(data) and data[pos] == 255:
            pos += 1
        if pos >= len(data):
            raise ValueError('잘린 JPEG 마커')
        marker = data[pos]; pos += 1
        if marker in (0xD9, 0xDA):
            yield marker, data[start:]
            return
        if marker in (0x01, *range(0xD0, 0xD8)):
            yield marker, data[start:pos]
            continue
        if pos + 2 > len(data):
            raise ValueError('잘린 JPEG 길이')
        length = int.from_bytes(data[pos:pos+2], 'big')
        if length < 2 or pos + length > len(data):
            raise ValueError('잘린 JPEG 세그먼트')
        yield marker, data[start:pos+length]
        pos += length
    raise ValueError('JPEG 종료 마커가 없습니다')

def inspect_exif(data: bytes) -> list:
    """EXIF 존재 여부를 반환한다."""
    return ['EXIF 위치·기기 정보 확인 필요'] if any(m == 0xE1 and b'Exif\x00\x00' in s[:16] for m, s in _segments(data)) else []

def strip_exif(data: bytes) -> bytes:
    """EXIF APP1 세그먼트만 제거한다."""
    return b'\xff\xd8' + b''.join(s for m, s in _segments(data) if not (m == 0xE1 and b'Exif\x00\x00' in s[:16]))
