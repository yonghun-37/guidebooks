"""실제 등록 없이 예약 실행용 예시 파일을 만든다."""
from pathlib import Path


def generate_schedule(root) -> list:
    """키트 경로 자리표시자를 포함한 운영체제별 예시를 저장한다."""
    directory = Path(root) / 'output/schedules'; directory.mkdir(parents=True, exist_ok=True)
    files = {
        'cron.txt': '# <KIT>을 실제 키트 경로로 바꾼 뒤 직접 등록하세요.\n0 9 * * * cd "<KIT>" && "<KIT>/.venv/bin/python" blog.py report\n',
        'launchd.plist': '<?xml version="1.0" encoding="UTF-8"?>\n<plist version="1.0"><dict><key>Label</key><string>example.blog</string><key>WorkingDirectory</key><string>&lt;KIT&gt;</string><key>ProgramArguments</key><array><string>&lt;KIT&gt;/.venv/bin/python</string><string>blog.py</string><string>report</string></array><key>StartCalendarInterval</key><dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict></dict></plist>\n<!-- <KIT>을 실제 경로로 변경 후 직접 등록 -->\n',
        'windows.txt': 'PowerShell에서 <KIT>을 실제 경로로 바꾼 뒤 직접 등록하세요.\n'
                       'schtasks /Create /SC DAILY /ST 09:00 /TN "BlogAutoKit" '
                       '/TR \'"<KIT>\\.venv\\Scripts\\python.exe" "<KIT>\\blog.py" report\'\n'
                       'schtasks /Query /TN "BlogAutoKit"\n'
                       'schtasks /Delete /TN "BlogAutoKit"\n'}
    paths = []
    for name, text in files.items():
        path = directory / name; path.write_text(text, encoding='utf-8', newline='\n'); paths.append(path)
    return paths
