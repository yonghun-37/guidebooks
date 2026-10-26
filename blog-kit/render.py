"""Markdown을 편집기용 HTML과 모바일 미리보기로 만든다. 원시 HTML은 글자로 표시한다."""
import argparse
from html import escape
from urllib.parse import urlsplit, unquote

import check
from common import cli, kit_path, load_config, save_json, save_text
from markdown_tools import map_images, html_fragment, safe_url
from review import digest, template

STYLE = """*{box-sizing:border-box}body{margin:0;background:#f2f5f3;color:#1c3028;font:17px/1.8 system-ui,sans-serif}main{max-width:420px;margin:24px auto;background:white;padding:22px;overflow-wrap:anywhere}h1{font-size:1.65rem;line-height:1.4}h2{font-size:1.3rem;margin-top:2em}img{display:block;width:100%;max-width:100%;height:auto}a{color:#176453}blockquote{margin:1em 0;border-left:4px solid #24785d;padding-left:14px}pre{white-space:pre-wrap;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccd7d0;padding:6px}.table-scroll{overflow-x:auto}p{margin:1em 0}@media(max-width:420px){main{margin:0;width:100%;padding:18px}}"""


def render(draft, output, config=None, affiliate=False):
    draft, output = kit_path(draft), kit_path(output)
    config = config or load_config()
    text = draft.read_text(encoding="utf-8-sig")
    assets = {}

    def image_path(match):
        alt, url = match[1], match[2]
        safe_url(url, True)
        if urlsplit(url).scheme or url.startswith("#"):
            return match[0]
        if urlsplit(url).query or urlsplit(url).fragment:
            raise ValueError("로컬 이미지 경로에는 쿼리·앵커를 넣지 마세요.")
        path = (draft.parent / unquote(url)).resolve()
        if not path.is_relative_to(draft.parent.resolve()) or path.suffix.lower() not in (".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"):
            raise ValueError("이미지는 초안 폴더 안의 SVG·PNG·JPEG·WebP·GIF 파일로 준비하세요.")
        name = "assets/" + digest(path)[:16] + path.suffix.lower()
        assets[name] = path.read_bytes()
        return f"![{alt}]({name})"

    normalized = map_images(text, image_path)
    fragment = html_fragment(normalized)
    result = check.inspect(normalized, config, affiliate)
    title = result["title"] or "내 글 미리보기"
    preview = f'<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><style>{STYLE}</style></head><body><main>{fragment}</main></body></html>\n'
    output.mkdir(parents=True, exist_ok=True)
    (output / "APPROVED.json").unlink(missing_ok=True)
    save_text(output / "draft.md", normalized)
    save_text(output / "editor.html", fragment)
    save_text(output / "preview.html", preview)
    save_text(output / "report.md", check.report(result))
    save_text(output / "REVIEW.md", template())
    save_json(output / "config.snapshot.json", config)
    for name, data in assets.items():
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    names = ["draft.md", "editor.html", "preview.html", "report.md", "config.snapshot.json", *assets]
    save_json(output / "render.json", {"title": title, "synthetic": "가상 연습용" in text, "affiliate": affiliate, "files": {name: digest(output / name) for name in names}})
    print(f"HTML 생성 완료: {output / 'editor.html'}")
    print(f"검수 대기: {output / 'REVIEW.md'}")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft")
    parser.add_argument("--output", default="output/article")
    parser.add_argument("--config")
    parser.add_argument("--affiliate", action="store_true")
    args = parser.parse_args()
    render(args.draft, args.output, load_config(args.config), args.affiliate)


if __name__ == "__main__":
    cli(main)
