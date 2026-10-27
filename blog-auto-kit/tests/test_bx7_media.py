"""실제 형식·공개용 사본·엄격 디코딩의 미디어 회귀 검사."""
import io
import struct
import zlib
from pathlib import Path

import pytest
from PIL import Image, ImageFile

from gates import privacy_exif
from samples.make_images import fake_exif_jpeg
from content.samples import load_sample
from core.state import Store
from wordpress.client import Client
from wordpress.mock_server import running_server
from wordpress.prepare import prepare_draft, remote_assets
from wordpress.publish import publish_draft

XMP = b'<x:xmpmeta xmlns:x="adobe:ns:meta/">GPSLatitude="0,0"</x:xmpmeta>'
ROOT = Path(__file__).resolve().parents[1]


def image_bytes(fmt):
    stream = io.BytesIO()
    Image.new('RGB', (16, 16), (80, 130, 100)).save(stream, format=fmt)
    return stream.getvalue()


def png_chunk(kind, payload):
    return (struct.pack('>I', len(payload)) + kind + payload
            + struct.pack('>I', zlib.crc32(kind + payload) & 0xffffffff))


def with_metadata(fmt, kind):
    data = image_bytes(fmt)
    exif = Image.Exif()
    exif[0x010f] = 'FAKE'
    exif[0x8825] = {1: 'N', 2: (0.0, 0.0, 0.0), 3: 'E', 4: (0.0, 0.0, 0.0)}
    if fmt == 'JPEG':
        payload = (b'http://ns.adobe.com/xap/1.0/\0' + XMP if kind == 'XMP'
                   else exif.tobytes())
        return data[:2] + b'\xff\xe1' + struct.pack('>H', len(payload) + 2) + payload + data[2:]
    payloads = {
        'eXIf': exif.tobytes()[6:],
        'tEXt': b'XML:com.adobe.xmp\0' + XMP,
        'iTXt': b'XML:com.adobe.xmp\0\0\0\0\0' + XMP,
        'zTXt': b'XML:com.adobe.xmp\0\0' + zlib.compress(XMP),
    }
    return data[:-12] + png_chunk(kind.encode(), payloads[kind]) + data[-12:]


def strict_decode(data):
    ImageFile.LOAD_TRUNCATED_IMAGES = False
    with Image.open(io.BytesIO(data)) as im:
        im.verify()
    with Image.open(io.BytesIO(data)) as im:
        im.load()
        return im.size, dict(im.getexif()), dict(im.info)


@pytest.mark.parametrize('fmt,kind', [
    ('JPEG', 'EXIF'), ('JPEG', 'XMP'), ('PNG', 'eXIf'),
    ('PNG', 'tEXt'), ('PNG', 'iTXt'), ('PNG', 'zTXt'),
])
def test_every_supported_metadata_container_is_detected_and_removed(fmt, kind):
    original = with_metadata(fmt, kind)
    strict_decode(original)
    assert privacy_exif.inspect_exif(original), (fmt, kind)
    clean = privacy_exif.strip_exif(original)
    assert privacy_exif.inspect_exif(clean) == []
    size, exif, info = strict_decode(clean)
    assert size == (16, 16)
    assert not exif
    assert not any(key.lower().startswith(('exif', 'xml', 'xmp')) for key in info)
    assert b'GPSLatitude' not in clean


@pytest.mark.parametrize('fmt', ['JPEG', 'PNG'])
def test_format_is_from_bytes_and_clean_images_stay_decodable(fmt):
    data = image_bytes(fmt)
    assert privacy_exif.image_format(data) == fmt
    assert privacy_exif.inspect_exif(data) == []
    assert strict_decode(privacy_exif.strip_exif(data))[0] == (16, 16)


@pytest.mark.parametrize('data', [b'GIF89a', b'RIFFxxxxWEBP', b'<svg/>', b'', b'\xff\xd8'])
def test_unsupported_and_truncated_formats_are_uninspectable(data):
    for operation in (privacy_exif.inspect_exif, privacy_exif.strip_exif):
        with pytest.raises(ValueError):
            operation(data)


@pytest.mark.parametrize('fmt', ['JPEG', 'PNG'])
def test_truncated_or_appended_payload_is_not_silently_accepted(fmt):
    data = image_bytes(fmt)
    for invalid in (data[:-8], data + b'GPSLatitude="0,0"'):
        with pytest.raises(ValueError):
            privacy_exif.inspect_exif(invalid)
        with pytest.raises(ValueError):
            privacy_exif.strip_exif(invalid)


def test_png_bad_crc_is_uninspectable():
    data = bytearray(image_bytes('PNG'))
    data[29] ^= 1
    with pytest.raises(ValueError):
        privacy_exif.inspect_exif(bytes(data))


@pytest.mark.parametrize('data', [None, 'file.jpg'])
def test_non_bytes_cannot_be_reported_clean(data):
    with pytest.raises(ValueError):
        privacy_exif.inspect_exif(data)


def test_demo_has_fake_make_gps_and_xmp_and_both_versions_decode():
    data = fake_exif_jpeg()
    size, exif, _ = strict_decode(data)
    assert size == (16, 16)
    assert exif[0x010f] == 'FAKE'
    with Image.open(io.BytesIO(data)) as im:
        gps = im.getexif().get_ifd(0x8825)
        assert tuple(gps[2]) == (0.0, 0.0, 0.0)
        assert tuple(gps[4]) == (0.0, 0.0, 0.0)
    assert b'GPSLatitude' in data
    clean = privacy_exif.strip_exif(data)
    assert strict_decode(clean)[1] == {}
    assert privacy_exif.inspect_exif(clean) == []
    assert b'FAKE' not in clean and b'GPSLatitude' not in clean


def test_checked_in_demo_is_reproducible_and_strictly_decodes():
    data = (ROOT / 'samples/fake-exif.jpg').read_bytes()
    assert data == fake_exif_jpeg()
    strict_decode(data)
    strict_decode(privacy_exif.strip_exif(data))


@pytest.mark.parametrize('mode', ['approval', 'auto'])
@pytest.mark.parametrize('fmt,kind,filename', [
    ('PNG', 'eXIf', 'photo.png'), ('JPEG', 'EXIF', 'renamed.png'),
    ('JPEG', 'XMP', 'photo.jpg'), ('PNG', 'tEXt', 'photo.png'),
    ('PNG', 'iTXt', 'photo.png'), ('PNG', 'zTXt', 'photo.png'),
])
def test_metadata_never_reaches_unapproved_publication(tmp_path, mode, fmt, kind, filename):
    data = with_metadata(fmt, kind)
    (tmp_path / filename).write_bytes(data)
    doc, store = load_sample('info'), Store(tmp_path)
    doc['media'][0]['path'] = filename
    with running_server(tmp_path, port=0) as url:
        client = Client(url)
        with pytest.raises(ValueError, match='EXIF'):
            prepare_draft(tmp_path, store, client, doc, '2026-10-27')
        with pytest.raises(ValueError):
            publish_draft(tmp_path, store, client, doc, '2026-10-27', mode)
        assert not any(p['status'] in ('future', 'publish')
                       for p in client.request('GET', 'posts'))
        assert client.request('GET', 'media') == []


@pytest.mark.parametrize('fmt,filename,mime', [
    ('JPEG', 'renamed.png', 'image/jpeg'), ('PNG', 'renamed.jpg', 'image/png'),
])
def test_clean_copy_is_uploaded_and_retrievable_from_actual_server(tmp_path, fmt, filename, mime):
    clean = privacy_exif.strip_exif(with_metadata(fmt, 'EXIF' if fmt == 'JPEG' else 'eXIf'))
    (tmp_path / filename).write_bytes(clean)
    doc, store = load_sample('info'), Store(tmp_path)
    doc['media'][0]['path'] = filename
    with running_server(tmp_path, port=0) as url:
        client = Client(url)
        row = prepare_draft(tmp_path, store, client, doc, '2026-10-27')
        media_id = row['prepared']['media'][0]
        uploaded = client.media_bytes(media_id)
        assert uploaded == clean
        assert privacy_exif.inspect_exif(uploaded) == []
        assert strict_decode(uploaded)[0] == (16, 16)
        assert client.request('GET', f'media/{media_id}')['mime_type'] == mime
        assert next((tmp_path / 'private/public-media').iterdir()).read_bytes() == uploaded
    assert (tmp_path / filename).read_bytes() == clean


@pytest.mark.parametrize('fmt,kind', [('JPEG', 'XMP'), ('PNG', 'eXIf')])
def test_upload_boundary_also_strips_metadata_without_mutating_source(tmp_path, fmt, kind):
    original = with_metadata(fmt, kind)
    path = tmp_path / 'photo.bin'
    path.write_bytes(original)
    doc = load_sample('info')
    doc['media'][0]['path'] = path.name
    with running_server(tmp_path, port=0) as url:
        client = Client(url)
        media_id = remote_assets(tmp_path, client, doc)['media'][0]
        uploaded = client.media_bytes(media_id)
        assert privacy_exif.inspect_exif(uploaded) == []
        assert b'GPSLatitude' not in uploaded and b'FAKE' not in uploaded
        assert strict_decode(uploaded)[0] == (16, 16)
    assert path.read_bytes() == original
