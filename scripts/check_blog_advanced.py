#!/usr/bin/env python3
"""심화편의 명령·실제 출력·파일:줄 발췌를 대조한다.

--check는 파일을 변경하지 않는 게이트다. --extract는 HTML에서 읽은 명령을
JSON으로 저장한다. --replay는 빈 복사본·새 venv에서 기본 경로를 순서대로 실행한다.
바꿔 보기의 수동 편집·선택 실연결 명령은 기본 경로와 구분해 추출한다.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

from check_site import Page

ROOT = Path(__file__).resolve().parents[1]


def section_id(element):
    while element:
        if element.tag == 'section' and 'chapter-block' in element.attrs.get('class', '').split():
            return element.attrs.get('id', '')
        element = element.parent
    return ''


def check(root=ROOT):
    root = Path(root)
    kit = root / 'blog-auto-kit'
    canonical = {}
    for chapter, unix, windows in re.findall(
            r'^\| (A\d+|E2E) \| `([^`]+)` \| `([^`]+)` \|$',
            (kit / 'course/commands.md').read_text(), re.M):
        if unix != windows:
            raise ValueError(f'{chapter}: commands.md의 공통 명령 불일치')
        canonical.setdefault(chapter, []).append(unix)
    errors, chapters = [], []
    if 'python blog.py status --costs' not in canonical.get('A4', []):
        errors.append('A4: 비용 기록 읽기 명령 누락')
    if 'python blog.py template approve library --by 서윤' not in canonical.get('A3', []):
        errors.append('A3: 글 틀 승인 명령 누락')
    scenario_output = json.loads((kit / 'course/expected/E2E/outputs.json').read_text())
    scenario_text = scenario_output.get('python blog.py run --scenarios', {}).get('stdout', '')
    if '✔ 통과: bypass_attempts' not in scenario_text:
        errors.append('E2E: 우회 시도 묶음 성공 출력 누락')
    files = sorted((root / 'site-blog/advanced').glob('*.html'))
    if len(files) != 14:
        errors.append(f'심화 장 수 {len(files)}: 14개 필요')
    for path in files:
        chapter = 'E2E' if path.stem == 'e2e' else 'A' + str(int(path.name[:2]))
        page = Page(path)
        commands, primary, shown, sources = [], [], {}, 0
        for element in page.elements:
            attrs = element.attrs
            if element.tag == 'code' and not element.text.strip():
                errors.append(f'{chapter}: 빈 코드 예시')
            if element.tag == 'code' and 'data-run' in attrs:
                commands.append({'os': attrs['data-run'], 'section': section_id(element),
                                 'text': element.text, 'course': attrs.get('data-course') == chapter})
                if attrs.get('data-course') == chapter and attrs['data-run'] in ('common', 'unix'):
                    primary.extend(element.text.strip().splitlines())
            if 'data-expected' in attrs:
                key = attrs['data-expected']
                if key in shown:
                    errors.append(f'{chapter}: 성공 출력 중복 {key}')
                shown[key] = element.text.strip('\n')
            if 'data-source' in attrs:
                sources += 1
                try:
                    name, first, last = attrs['data-source'].rsplit(':', 2)
                    first, last = int(first), int(last)
                    source = (kit / name).resolve()
                    if not source.is_relative_to(kit.resolve()) or not 1 <= first <= last <= first + 24:
                        raise ValueError('파일 경로 또는 25줄 제한')
                    lines = source.read_text().splitlines()
                    if last > len(lines) or element.text != '\n'.join(lines[first-1:last]):
                        raise ValueError('실제 파일 줄과 다름')
                except (OSError, ValueError) as error:
                    errors.append(f'{chapter}: 발췌 {attrs["data-source"]}: {error}')
        expected_commands = canonical.get(chapter, [])
        allowed = {line for rows in canonical.values() for line in rows}
        allowed.update(f'python course.py {action} {name}' for name in canonical for action in ('start', 'check'))
        allowed.add('python blog.py run --sample library')
        allowed.update(('python course.py reset', 'python --version', 'python3.11 --version',
                        'python3.11 -m venv .venv', 'source .venv/bin/activate', 'pwd', 'ls',
                        'py -3.11 --version', 'py -3.11 -m venv .venv', 'Get-Location', 'Get-ChildItem',
                        r'.\.venv\Scripts\Activate.ps1', r'.venv\Scripts\Activate.ps1',
                        'cp config.example.toml config.toml', 'Copy-Item config.example.toml config.toml'))
        for block in commands:
            for line in block['text'].strip().splitlines():
                if line not in allowed:
                    errors.append(f'{chapter}: commands.md·준비/복원 명령 밖: {line}')
        if primary != expected_commands:
            errors.append(f'{chapter}: 본문 기본 명령·순서가 commands.md와 다름: {primary}')
        checkpoint = [line for b in commands if b['os'] in ('common', 'unix') and b['section'] == 'checkpoint'
                      for line in b['text'].strip().splitlines()]
        if expected_commands and checkpoint != [f'python course.py start {chapter}', *expected_commands,
                                                 f'python course.py check {chapter}']:
            errors.append(f'{chapter}: 체크포인트 복원 명령·순서 불일치')
        # 기본 경로 표시를 떼어 검사를 우회하거나, 실행하지 않는 성공 문구를 붙이지 못한다.
        visible = [line for b in commands if b['os'] in ('common', 'unix')
                   and b['section'] not in ('change', 'checkpoint')
                   for line in b['text'].splitlines()
                   if (line.startswith('python blog.py ') or line.startswith('python course.py '))
                   and line != f'python course.py start {chapter}']
        if visible != primary:
            errors.append(f'{chapter}: 기본 명령 표시 누락·중복')
        expected = {} if chapter == 'A0' else json.loads(
            (kit / f'course/expected/{chapter}/outputs.json').read_text())
        required_keys = {f'{chapter}|{command}' for command in expected_commands}
        if set(shown) != required_keys or set(expected) != set(expected_commands):
            errors.append(f'{chapter}: 성공 출력 또는 expected 명령 누락·추가')
        for command, result in expected.items():
            if shown.get(f'{chapter}|{command}') != result['stdout'].rstrip('\n'):
                errors.append(f'{chapter}: 성공 출력 불일치 {command}')
        read = next((e for e in page.elements if e.attrs.get('id') == 'read'), None)
        if not sources or not read or not any(e.tag == 'caption' and '읽는 법' in e.text and e.within(read) for e in page.elements):
            errors.append(f'{chapter}: 실제 발췌 또는 읽는 법 표 없음')
        for tabs in (e for e in page.elements if 'data-os-tabs' in e.attrs):
            panels = [e for e in page.elements if 'data-os-panel' in e.attrs and e.within(tabs)]
            texts = ['\n'.join(e.text for e in page.elements if e.tag == 'code' and e.within(panel)) for panel in panels]
            if len(texts) == 2 and texts[0] == texts[1]:
                errors.append(f'{chapter}: 같은 OS 명령은 공통 블록으로 합치세요')
            elif len(texts) == 2 and all(texts):
                left, right = texts[0].splitlines(), texts[1].splitlines()
                if left[0] == right[0] or left[-1] == right[-1]:
                    errors.append(f'{chapter}: OS 탭의 같은 앞뒤 명령을 공통 블록으로 옮기세요')
        chapters.append({'chapter': chapter, 'file': str(path.relative_to(root)),
                         'primary': primary, 'blocks': commands, 'outputs': len(shown), 'sources': sources})
    return {'chapters': chapters, 'errors': errors}


def replay(root, report):
    if report['errors']:
        raise ValueError('불일치부터 고친 뒤 재현하세요')
    if sys.version_info < (3, 11):
        raise ValueError('재현은 Python 3.11 이상으로 실행하세요')
    with tempfile.TemporaryDirectory(prefix='blog-html-replay-') as directory:
        kit = Path(directory) / 'kit'
        shutil.copytree(root / 'blog-auto-kit', kit, ignore=shutil.ignore_patterns(
            '.env', '.venv', 'private', 'output', 'config.toml', '__pycache__', '.pytest_cache'))
        subprocess.run([sys.executable, '-m', 'venv', str(kit / '.venv')], check=True)
        python = str(kit / '.venv/bin/python')
        env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
        count = 0
        for chapter in report['chapters']:
            name = chapter['chapter']
            if name == 'A0':
                print('A0: 운영계획 장 확인 · 실행 명령 없음', flush=True)
                continue
            # start/check도 HTML에서 추출한 기본 구역의 명령이어야 한다.
            route = []
            for block in chapter['blocks']:
                if block['os'] not in ('common', 'unix'):
                    continue
                for line in block['text'].splitlines():
                    if (block['course'] or
                        block['section'] == 'start' and line == f'python course.py start {name}' or
                        block['section'] == 'checkpoint' and line == f'python course.py check {name}'):
                        route.append(line)
            if route != [f'python course.py start {name}', *chapter['primary'], f'python course.py check {name}']:
                raise ValueError(name + ': HTML 시작·체크 명령 누락 또는 순서 오류')
            for command in route:
                words = shlex.split(command)
                if words[0] != 'python' or words[1] not in ('course.py', 'blog.py'):
                    raise ValueError('재현 허용 명령 밖: ' + command)
                result = subprocess.run([python, *words[1:]], cwd=kit, env=env,
                                        text=True, capture_output=True, timeout=90)
                print('$ ' + command + '\n' + result.stdout, end='', flush=True)
                if result.returncode:
                    raise ValueError(command + '\n' + result.stderr)
                expected = json.loads((kit / f'course/expected/{name}/outputs.json').read_text())
                if command in expected and result.stdout != expected[command]['stdout']:
                    raise ValueError('실제 stdout 불일치: ' + command)
                count += 1
        print(f'HTML 추출 명령 클린룸: {count}개 성공 / 불일치 0', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--extract', type=Path)
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    try:
        report = check()
        if args.extract:
            args.extract.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        if report['errors']:
            for error in report['errors']:
                print('✖ ' + error)
            return 1
        print(f'본문↔키트: {len(report["chapters"])}장 / 명령 {sum(len(c["primary"]) for c in report["chapters"])} / 출력 {sum(c["outputs"] for c in report["chapters"])} / 발췌 {sum(c["sources"] for c in report["chapters"])} / 불일치 0', flush=True)
        if args.replay:
            replay(ROOT, report)
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print('✖ ' + str(error))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
