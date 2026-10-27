"""JPEG·PNG의 위치 메타데이터를 검사하고 공개용 사본을 만든다.

컨테이너를 검사하며 픽셀의 실제 디코딩과 얼굴·배경의 식별 정보는 별도 확인한다.
"""
import binascii

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
PNG_METADATA = {b'eXIf', b'tEXt', b'iTXt', b'zTXt'}


def image_format(data: bytes) -> str:
    """확장자 대신 매직바이트로 지원 형식을 확인한다."""
    if isinstance(data, bytes):
        if data.startswith(b'\xff\xd8'):
            return 'JPEG'
        if data.startswith(PNG_SIGNATURE):
            return 'PNG'
    raise ValueError('검사 가능한 JPEG·PNG 파일이 아닙니다')


def _scan_end(data, pos):
    """바이트 스터핑·재시작 마커를 건너뛰고 다음 JPEG 세그먼트를 찾는다."""
    while pos < len(data):
        if data[pos] != 255:
            pos += 1
            continue
        next_pos = pos + 1
        while next_pos < len(data) and data[next_pos] == 255:
            next_pos += 1
        if next_pos >= len(data):
            raise ValueError('잘린 JPEG 영상 데이터')
        if data[next_pos] == 0 or 0xD0 <= data[next_pos] <= 0xD7:
            pos = next_pos + 1
            continue
        break
    return pos


def _jpeg_length(data, pos):
    """현재 JPEG 세그먼트의 선언 길이와 파일 경계를 대조한다."""
    if pos + 2 > len(data):
        raise ValueError('잘린 JPEG 길이')
    length = int.from_bytes(data[pos:pos + 2], 'big')
    if length < 2 or pos + length > len(data):
        raise ValueError('잘린 JPEG 세그먼트')
    return length


def _jpeg_segments(data):
    """스캔 사이의 APP1까지 검사하고 EOI 뒤의 미검사 데이터는 거절한다."""
    pos = 2
    frame = scan = False
    while pos < len(data):
        start = pos
        if data[pos] != 255:
            raise ValueError('손상된 JPEG 마커')
        while pos < len(data) and data[pos] == 255:
            pos += 1
        if pos >= len(data):
            raise ValueError('잘린 JPEG 마커')
        marker = data[pos]
        pos += 1
        if marker == 0xD9:
            if pos != len(data) or not frame or not scan:
                raise ValueError('JPEG 종료 또는 영상 데이터가 불명확합니다')
            yield marker, data[start:pos]
            return
        if marker in (0, 0xD8, *range(0xD0, 0xD8)):
            raise ValueError('잘못된 JPEG 마커')
        if marker == 0x01:
            yield marker, data[start:pos]
            continue
        length = _jpeg_length(data, pos)
        payload = data[pos + 2:pos + length]
        if marker in (0xC0, 0xC1, 0xC2):
            if len(payload) < 6 or not int.from_bytes(payload[1:3], 'big') or not int.from_bytes(payload[3:5], 'big'):
                raise ValueError('JPEG 영상 크기를 확인할 수 없습니다')
            frame = True
        yield marker, data[start:pos + length]
        pos += length
        if marker == 0xDA:
            if not frame or not payload or length != 6 + 2 * payload[0]:
                raise ValueError('JPEG 스캔 헤더를 확인할 수 없습니다')
            scan, start = True, pos
            pos = _scan_end(data, pos)
            yield 0, data[start:pos]
    raise ValueError('JPEG 종료 마커가 없습니다')


def _png_chunks(data):
    """PNG 청크 길이·CRC·필수 구조와 종료 위치를 검사한다."""
    pos = 8
    seen = set()
    while pos + 12 <= len(data):
        length = int.from_bytes(data[pos:pos + 4], 'big')
        kind = data[pos + 4:pos + 8]
        end = pos + length + 12
        if end > len(data) or not kind.isalpha():
            raise ValueError('손상된 PNG 청크')
        payload = data[pos + 8:end - 4]
        crc = int.from_bytes(data[end - 4:end], 'big')
        if binascii.crc32(kind + payload) & 0xffffffff != crc:
            raise ValueError('PNG CRC가 일치하지 않습니다')
        if not seen and kind != b'IHDR':
            raise ValueError('PNG 헤더가 없습니다')
        if kind == b'IHDR':
            if seen or length != 13 or not int.from_bytes(payload[:4], 'big') or not int.from_bytes(payload[4:8], 'big'):
                raise ValueError('PNG 영상 크기를 확인할 수 없습니다')
        seen.add(kind)
        yield kind, data[pos:end]
        pos = end
        if kind == b'IEND':
            if length or pos != len(data) or b'IDAT' not in seen:
                raise ValueError('PNG 종료 또는 영상 데이터가 불명확합니다')
            return
    raise ValueError('PNG 종료 청크가 없습니다')


def _parts(data):
    fmt = image_format(data)
    if fmt == 'JPEG':
        return b'\xff\xd8', [(m == 0xE1, raw) for m, raw in _jpeg_segments(data)]
    return PNG_SIGNATURE, [(kind in PNG_METADATA, raw) for kind, raw in _png_chunks(data)]


def inspect_exif(data: bytes) -> list:
    """EXIF·XMP를 담을 수 있는 APP1/PNG 텍스트 청크를 알린다."""
    _, parts = _parts(data)
    return ['EXIF·XMP·텍스트 위치 메타데이터 확인 필요'] if any(meta for meta, _ in parts) else []


def strip_exif(data: bytes) -> bytes:
    """JPEG APP1과 PNG EXIF·텍스트를 제거한 같은 형식의 사본을 반환한다."""
    signature, parts = _parts(data)
    clean = signature + b''.join(raw for metadata, raw in parts if not metadata)
    if inspect_exif(clean):
        raise ValueError('공개용 사본에 메타데이터가 남아 있습니다')
    return clean
