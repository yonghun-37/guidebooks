"""작은 Markdown 부분집합: 제목·문단·목록·인용·표·코드·링크·이미지·강조.

원시 HTML은 이스케이프한다. 외부 이미지/링크를 내려받지 않는다.
"""
from html import escape
import re
from urllib.parse import urlsplit, unquote

COMMENT = re.compile(r"<!--.*?-->", re.S)
IMAGE = re.compile(r"!\[([^\]\n]*)\]\(([^\s)]+)\)")
LINK = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^\s)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def blocks(text):
    lines = COMMENT.sub(lambda match: "\n" * match[0].count("\n"), text).splitlines()
    result, index = [], 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        number = index + 1
        if line.startswith("```"):
            code = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code.append(lines[index])
                index += 1
            result.append(("code", "\n".join(code), number))
            index += 1
            continue
        heading = HEADING.match(line)
        if heading:
            result.append(("h" + str(len(heading[1])), heading[2], number))
        elif re.match(r"^[-*+]\s+", line):
            result.append(("ul", re.sub(r"^[-*+]\s+", "", line), number))
        elif re.match(r"^\d+[.)]\s+", line):
            result.append(("ol", re.sub(r"^\d+[.)]\s+", "", line), number))
        elif line.startswith("> "):
            result.append(("quote", line[2:], number))
        elif line.startswith("|") and line.endswith("|"):
            result.append(("row", line, number))
        else:
            paragraph = [line]
            while index + 1 < len(lines) and lines[index + 1].strip():
                following = lines[index + 1].strip()
                if HEADING.match(following) or re.match(r"^(?:[-*+]\s|\d+[.)]\s|>\s|\||```)", following):
                    break
                index += 1
                paragraph.append(following)
            result.append(("p", "\n".join(paragraph), number))
        index += 1
    return result


def map_images(text, transform):
    pattern = re.compile(r"<!--.*?-->|^```[^\n]*\n.*?(?:^```[^\n]*(?:\n|$)|\Z)|`[^`\n]*`|" + IMAGE.pattern, re.S | re.M)
    def replace(match):
        image = IMAGE.fullmatch(match[0])
        return transform(image) if image else match[0]
    return pattern.sub(replace, text)


def safe_url(value, image=False):
    # 엔티티·퍼센트·제어 문자로 프로토콜 검사를 우회하지 않도록 보수적으로 거절한다.
    decoded = unquote(value)
    if any(ord(c) < 33 or ord(c) == 127 for c in decoded) or "\\" in decoded:
        raise ValueError("링크·이미지 주소에서 공백·제어 문자·역슬래시를 빼세요.")
    parsed = urlsplit(decoded)
    if parsed.scheme:
        if parsed.scheme.lower() not in (("https", "http") if image else ("https", "http", "mailto")):
            raise ValueError("허용하지 않는 링크·이미지 주소 형식입니다.")
        if parsed.scheme.lower() in ("https", "http") and (not parsed.hostname or parsed.username or parsed.password):
            raise ValueError("링크에는 자격증명 없는 웹 주소를 쓰세요.")
    elif decoded.startswith("//") or ":" in decoded.split("/")[0]:
        raise ValueError("링크·이미지에 명확한 웹 주소 또는 상대 경로를 쓰세요.")
    return value


def inline(text):
    pattern = re.compile(r"!\[([^\]\n]*)\]\(([^\s)]+)\)|\[([^\]\n]+)\]\(([^\s)]+)\)|\*\*(.+?)\*\*|`([^`]+)`")
    out, end = [], 0
    for match in pattern.finditer(text):
        out.append(escape(text[end:match.start()]))
        alt, image, label, url, bold, code = match.groups()
        if image is not None:
            out.append(f'<img src="{escape(safe_url(image, True), quote=True)}" alt="{escape(alt, quote=True)}" loading="lazy" style="max-width:100%;height:auto">')
        elif url is not None:
            out.append(f'<a href="{escape(safe_url(url), quote=True)}" rel="noopener noreferrer">{escape(label)}</a>')
        elif bold is not None:
            out.append(f"<strong>{escape(bold)}</strong>")
        else:
            out.append(f"<code>{escape(code)}</code>")
        end = match.end()
    out.append(escape(text[end:]))
    return "".join(out).replace("\n", "<br>\n")


def html_fragment(text):
    parsed = blocks(text)
    out, index = [], 0
    while index < len(parsed):
        kind, value, _ = parsed[index]
        if kind in ("ul", "ol"):
            items = []
            while index < len(parsed) and parsed[index][0] == kind:
                items.append("<li>" + inline(parsed[index][1]) + "</li>")
                index += 1
            out.append(f"<{kind}>" + "".join(items) + f"</{kind}>")
            continue
        if kind == "row":
            rows = []
            while index < len(parsed) and parsed[index][0] == "row":
                cells = [c.strip() for c in parsed[index][1].strip("|").split("|")]
                rows.append(cells)
                index += 1
            header = len(rows) > 1 and all(re.fullmatch(r":?-{3,}:?", c) for c in rows[1])
            table = []
            for row_index, cells in enumerate(rows):
                if header and row_index == 1:
                    continue
                tag = "th" if header and row_index == 0 else "td"
                table.append("<tr>" + "".join(f"<{tag}>" + inline(c) + f"</{tag}>" for c in cells) + "</tr>")
            out.append('<div class="table-scroll"><table>' + "".join(table) + "</table></div>")
            continue
        if kind == "code":
            out.append("<pre><code>" + escape(value) + "</code></pre>")
        else:
            tag = "blockquote" if kind == "quote" else kind
            out.append(f"<{tag}>" + inline(value) + f"</{tag}>")
        index += 1
    return "\n".join(out) + "\n"
