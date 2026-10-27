"""배포 파일과 함수 길이·모듈 설명·기존 키트 독립성을 검사한다."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'private', 'output', '.venv', '__pycache__', '.pytest_cache'}


def source_files():
    return [p for p in ROOT.rglob('*') if p.is_file() and not SKIP.intersection(p.relative_to(ROOT).parts)
            and p.suffix in ('.py', '.md', '.json', '.toml', '.yml', '.txt', '.lock', '.ini', '.svg')]


def test_every_delivered_text_file_has_at_most_200_lines():
    too_long = [(p.relative_to(ROOT), len(p.read_bytes().splitlines())) for p in source_files()
                if len(p.read_bytes().splitlines()) > 200]
    assert too_long == []


def test_python_functions_and_module_descriptions():
    for path in source_files():
        if path.suffix != '.py':
            continue
        tree = ast.parse(path.read_text(encoding='utf-8'))
        assert ast.get_docstring(tree), path
        assert any('\uac00' <= ch <= '\ud7a3' for ch in ast.get_docstring(tree)), path
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                assert node.end_lineno - node.lineno + 1 <= 40, (path, node.name)
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [n.name for n in node.names] + [getattr(node, 'module', '') or '']
                assert all('blog_kit' not in name and 'auto_kit' not in name for name in names)
