from pathlib import Path
import pytest
from common import ROOT, load_config, read_json
from markdown_tools import html_fragment
import render
import review


def approve_all(output):
    path = output / "REVIEW.md"
    path.write_text(path.read_text().replace("- [ ]", "- [x]"))
    review.approve(output)


def test_format_and_html_escaping():
    text = '# 제목\n\n## 질문\n\n**답변**과 `코드`\n\n- 하나\n- 둘\n\n1. 먼저\n2. 다음\n\n> 인용\n\n| 항목 | 값 |\n| --- | --- |\n| 이름 | 설명 |\n\n<script>alert(1)</script>'
    html = html_fragment(text)
    for value in ("<h1>", "<h2>", "<strong>", "<code>", "<ul><li>", "<ol><li>", "<blockquote>", "<th>", "&lt;script&gt;"):
        assert value in html
    assert "<script>" not in html
    assert '<a href="https://x.invalid"' in html_fragment("[자료](https://x.invalid)")


@pytest.mark.parametrize("url", ["javascript:alert", "data:image/svg+xml,test", "//evil.invalid/x", "java%73cript:alert", "https://u:p@x.invalid/x"])
def test_unsafe_urls_refused(url):
    with pytest.raises(ValueError):
        html_fragment(f"[링크]({url})")
    with pytest.raises(ValueError):
        html_fragment(f"![설명]({url})")


def test_render_assets_reapproval_and_changed_files(tmp_path):
    out = render.render(ROOT / "samples/article.md", tmp_path / "article")
    assert (out / "assets").is_dir()
    assert "width=device-width" in (out / "preview.html").read_text()
    assert "max-width:420px" in (out / "preview.html").read_text()
    with pytest.raises(ValueError, match="모든 항목"):
        review.approve(out)
    approve_all(out)
    review.require_approval(out)
    (out / "draft.md").write_text("바뀐 내용")
    with pytest.raises(ValueError, match="달라졌"):
        review.require_approval(out)
    render.render(ROOT / "samples/article.md", out)
    assert not (out / "APPROVED.json").exists()
    # 출력 폴더 안의 재작성본도 로컬 이미지와 함께 다시 변환할 수 있다.
    render.render(out / "draft.md", out)


@pytest.mark.parametrize("filename", ["editor.html", "preview.html", "report.md", "REVIEW.md", "config.snapshot.json", "render.json"])
def test_approval_binds_all_deliverables(tmp_path, filename):
    render.render(ROOT / "samples/article.md", tmp_path)
    approve_all(tmp_path)
    with (tmp_path / filename).open("a") as stream:
        stream.write(" ")
    with pytest.raises(ValueError):
        review.require_approval(tmp_path)


def test_refuse_local_image_outside_draft_folder(tmp_path):
    (tmp_path / "outside.svg").write_text("<svg/>")
    folder = tmp_path / "draft"
    folder.mkdir()
    (folder / "article.md").write_text("# 제목\n\n![설명](../outside.svg)")
    with pytest.raises(ValueError, match="초안 폴더"):
        render.render(folder / "article.md", tmp_path / "out")


def test_image_markdown_examples_in_code_and_comments_need_no_file(tmp_path):
    draft = tmp_path / "input.md"
    draft.write_text("# 이미지 쓰는 법\n\n```md\n![설명](missing.svg)\n```\n\n`![설명](also-missing.svg)`\n\n<!-- ![설명](not-a-file.svg) -->")
    render.render(draft, tmp_path / "out")
    html = (tmp_path / "out/editor.html").read_text()
    assert "<img" not in html and "missing.svg" in html
