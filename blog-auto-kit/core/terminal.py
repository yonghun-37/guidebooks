"""명령의 짧은 출력도 저장해 책의 예상 출력과 비교한다."""
import io
from contextlib import redirect_stdout
from core.files import read_json, write_json


def capture_command(root, command, action):
    stream = io.StringIO()
    with redirect_stdout(stream):
        code = action()
    output = stream.getvalue()
    print(output, end='')
    path = root / 'private/terminal.json'
    records = read_json(path) if path.exists() else {}
    records[command] = {'stdout': output, 'returncode': code or 0}
    write_json(path, records)
    return code or 0
