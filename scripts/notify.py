#!/usr/bin/env python3
"""Post a progress message (and optional file attachments) to the ai-insta Discord channel.

Usage: python3 scripts/notify.py "message" [file ...]
Token is read from yh-lab/.env (DISCORD_BOT_TOKEN); it is never printed.
"""
import json, re, sys, uuid
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ENV = Path('/home/yonghun/project/yh-lab/.env')
CHANNEL = '1564065235499880478'


def token():
    for line in ENV.read_text().splitlines():
        m = re.match(r'^\s*(?:export\s+)?DISCORD_BOT_TOKEN\s*=\s*(.*?)\s*$', line)
        if m:
            return m[1].strip('"\'')
    raise SystemExit('DISCORD_BOT_TOKEN missing')


def post(text, files=()):
    files = [Path(f) for f in files]
    payload = {'content': text[:1990], 'allowed_mentions': {'parse': []},
               'attachments': [{'id': i, 'filename': p.name} for i, p in enumerate(files)]}
    b = 'ai-insta-' + uuid.uuid4().hex
    parts = [f'--{b}\r\nContent-Disposition: form-data; name="payload_json"\r\nContent-Type: application/json\r\n\r\n'.encode(),
             json.dumps(payload, ensure_ascii=False).encode(), b'\r\n']
    for i, p in enumerate(files):
        parts += [f'--{b}\r\nContent-Disposition: form-data; name="files[{i}]"; filename="{p.name}"\r\nContent-Type: application/octet-stream\r\n\r\n'.encode(),
                  p.read_bytes(), b'\r\n']
    parts.append(f'--{b}--\r\n'.encode())
    req = Request(f'https://discord.com/api/v10/channels/{CHANNEL}/messages', data=b''.join(parts), method='POST',
                  headers={'Authorization': 'Bot ' + token(), 'User-Agent': 'ai-insta/notify',
                           'Content-Type': 'multipart/form-data; boundary=' + b})
    try:
        with urlopen(req, timeout=30) as r:
            print('sent', r.status, json.load(r).get('id'))
    except HTTPError as e:
        print('discord_error', e.code, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    post(sys.argv[1], sys.argv[2:])
