"""표준 라이브러리로 그림책 PNG와 가짜 EXIF JPEG를 만든다."""
import base64
import binascii
import struct
import zlib
from pathlib import Path

JPEG_BASE = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////2wBDAf//////////////////////////////////////////////////////////////////////////////////////wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAX/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIQAxAAAAF//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABBQJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAwEBPwF//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAgEBPwF//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQAGPwJ//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPyF//9oADAMBAAIAAwAAABD/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oACAEDAQE/EAf/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oACAECAQE/EAf/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oACAEBAAE/EAf/2Q=='


def chunk(kind, data):
    """PNG 청크와 CRC를 구성한다."""
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', binascii.crc32(kind + data) & 0xffffffff)


def draw_books():
    """아이 얼굴이 없는 가상 그림책꽂이를 픽셀로 그린다."""
    width, height = 240, 160
    rows = []
    colors = [(194, 94, 71), (66, 132, 129), (216, 178, 80), (112, 103, 146)]
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            color = (249, 245, 236)
            if 30 <= x < 210 and 105 <= y < 123:
                color = (135, 95, 61)
            for i, shade in enumerate(colors):
                if 45 + i * 35 <= x < 72 + i * 35 and 40 + i * 7 <= y < 105:
                    color = shade
            row.extend(color)
        rows.append(bytes(row))
    header = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header) + chunk(b'IDAT', zlib.compress(b''.join(rows), 9)) + chunk(b'IEND', b'')


def fake_exif_jpeg():
    """제조사 FAKE와 좌표 0,0을 가진 TIFF EXIF를 삽입한다."""
    entry = lambda tag, kind, count, value: struct.pack('<HHI', tag, kind, count) + value
    offset = lambda n: struct.pack('<I', n)
    tiff = b'II' + struct.pack('<HI', 42, 8) + struct.pack('<H', 2)
    tiff += entry(0x010f, 2, 5, offset(38)) + entry(0x8825, 4, 1, offset(44))
    tiff += offset(0) + b'FAKE\0\0' + struct.pack('<H', 4)
    tiff += entry(1, 2, 2, b'N\0\0\0') + entry(2, 5, 3, offset(98))
    tiff += entry(3, 2, 2, b'E\0\0\0') + entry(4, 5, 3, offset(122)) + offset(0)
    tiff += struct.pack('<II', 0, 1) * 6
    payload = b'Exif\0\0' + tiff
    image = base64.b64decode(JPEG_BASE)
    return image[:2] + b'\xff\xe1' + struct.pack('>H', len(payload) + 2) + payload + image[2:]


def main():
    root = Path(__file__).resolve().parent
    (root / 'books.png').write_bytes(draw_books())
    (root / 'fake-exif.jpg').write_bytes(fake_exif_jpeg())
    print('✔ 통과: samples/books.png · samples/fake-exif.jpg')


if __name__ == '__main__':
    main()
