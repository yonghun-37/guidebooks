"""Markdown의 발행 전 점검표를 만든다. 사실·법률 적합성 판정은 사람이 한다."""
import argparse
from collections import Counter
from html.parser import HTMLParser
import re
import unicodedata

from common import cli, kit_path, load_config, save_text
from markdown_tools import IMAGE, LINK, blocks


def plain(text):
    text = IMAGE.sub(lambda m: m[1], text)
    text = LINK.sub(lambda m: m[1], text)
    text = re.sub(r"https?://[^\s\]]+", "", text)
    return re.sub(r"[*`#]", "", text)


class ImageReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.missing = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img" and not dict(attrs).get("alt", "").strip():
            self.missing += 1


def inspect(text, config, affiliate=False):
    rules = config["rules"]
    parsed = blocks(text)
    findings = []

    def add(rule, message, line=None):
        findings.append({"rule": rule, "message": message, "line": line})

    titles = [(value, line) for kind, value, line in parsed if kind == "h1"]
    title = titles[0][0] if titles else ""
    if len(titles) != 1 or not parsed or parsed[0][0] != "h1":
        add("title", "# 제목 하나를 맨 위에 적으세요.")
    length = len(plain(title))
    if not rules["title_min"] <= length <= rules["title_max"]:
        add("title_length", f"제목 {length}자. 기본 범위 {rules['title_min']}~{rules['title_max']}자로 다듬어 보세요.")
    previous, h2 = 1, 0
    for kind, _, line in parsed:
        if kind.startswith("h") and kind[1:].isdigit():
            level = int(kind[1:])
            if level > previous + 1:
                add("headings", "소제목 단계를 건너뛰었어요. ## 다음에 ###을 쓰세요.", line)
            previous = level
            h2 += level == 2
    if h2 < rules["h2_min"]:
        add("headings", f"## 소제목이 {h2}개예요. 기본값 {rules['h2_min']}개 이상으로 질문을 나눠 보세요.")
    body = "\n".join(value for kind, value, _ in parsed if kind not in ("h1", "code"))
    chars = len(plain(body))
    if not rules["body_min"] <= chars <= rules["body_max"]:
        add("body_length", f"본문 {chars}자. 기본 범위 {rules['body_min']}~{rules['body_max']}자예요. 필요한 답부터 채우세요.")
    clean = "\n".join(value for kind, value, _ in parsed if kind != "code")
    images = list(IMAGE.finditer(clean))
    for match in images:
        if not match[1].strip():
            add("image_alt", "이미지의 ![ ] 안에 내용을 설명하는 대체 텍스트를 적으세요.")
    html_images = ImageReader()
    html_images.feed(clean)
    if html_images.missing:
        add("image_alt", f"HTML 이미지 {html_images.missing}개에 대체 텍스트가 없어요.")
    if re.search(r"</?[a-zA-Z][^>]*>", clean):
        add("raw_html", "원시 HTML은 변환할 때 글자로 표시돼요. Markdown 이미지·링크로 바꾸세요.")
    affiliate = affiliate or any(marker.casefold() in clean.casefold() for marker in rules["affiliate_markers"])
    first_body = next((value for kind, value, _ in parsed if kind != "h1"), "")
    # 법은 제목 또는 첫 부분을 허용한다. 키트는 별도 첫 문단을 선택한다.
    disclosed = bool(re.search(r"(?:수수료|원고료|제품|물품|서비스|할인|숙박|식사).*(?:제공받(?:아|았|으며|습니다)|지급받(?:아|았|으며|습니다)|받습니다|제공 받(?:아|았|으며|습니다)|제공됩니다|지급됩니다)", plain(first_body)))
    if affiliate and not disclosed:
        add("disclosure", "제휴 링크가 있어요. 실제 수수료·제공 관계를 본문 첫 문단에 분명히 적으세요. ‘받을 수도’·하단 표시는 통과하지 않아요.")
    seen = []
    for kind, value, line in parsed:
        if kind in ("code", "h1"):
            continue
        for offset, paragraph_line in enumerate(value.splitlines()):
            visible = plain(paragraph_line)
            # URL 안의 숫자·목록 번호와 출처 메모 안 숫자는 주장 숫자로 세지 않는다.
            claim = re.sub(r"\[(?:출처|내 기록):[^\]]*\]", "", visible)
            source = re.search(r"\[출처:\s*(https?://[^\s|\]]+)\s*\|([^|\]]+)\|([^\]]+)\]", paragraph_line)
            source = source and all(part.strip() for part in source.groups())
            record = re.search(r"\[내 기록:([^|\]]+)\|([^\]]+)\]", paragraph_line)
            record = record and all(part.strip() for part in record.groups())
            placeholder = any(word in paragraph_line for word in ("확인 필요", "메모 입력", "URL 입력"))
            if re.search(r"\d", claim) and (not (source or record) or placeholder):
                add("number_source", "숫자가 있는 문장에 같은 줄의 출처 또는 내 기록 메모를 채우세요.", line + offset)
            for sentence in re.split(r"(?<=[.!?。])\s+|\n", visible):
                normalized = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", sentence)).strip()
                if len(normalized) >= rules["repeat_min"]:
                    seen.append(normalized)
            for phrase in rules["cliches"]:
                if phrase in paragraph_line:
                    add("cliche", f"상투 표현 ‘{phrase}’을 구체적인 말로 바꿔 보세요.", line + offset)
    for sentence, count in Counter(seen).items():
        if count > 1:
            add("repeat", f"같은 문장이 {count}번 있어요: {sentence[:70]}")
    experience = False
    for index, (kind, value, _) in enumerate(parsed):
        if kind.startswith("h") and rules["experience_heading"] in value:
            content = []
            for following, paragraph, _ in parsed[index + 1:]:
                if following.startswith("h"):
                    break
                content.append(paragraph)
            if "".join(content).strip() and not re.search(r"확인 필요|직접 입력|여기에|미작성", "".join(content)):
                experience = True
    if not experience:
        add("experience", f"‘## {rules['experience_heading']}’ 아래에 실제 관찰을 적으세요. 경험이 없으면 꾸미지 말고 직접 확인할 일을 남기세요.")
    return {"title": title, "title_chars": length, "body_chars": chars, "affiliate_detected": affiliate, "findings": findings}


def report(result):
    rows = ["# 초안 점검 리포트", "", f"확인할 항목: {len(result['findings'])}개", f"제목: {result['title_chars']}자 / 본문: {result['body_chars']}자(공백 포함)", f"제휴 표시 점검: {'필요' if result['affiliate_detected'] else '자동 탐지 없음 — 실제 관계를 사람이 확인하세요'}", "", "길이·개수·문장 탐지는 키트 기본값(바꿀 수 있음)입니다. 검색 순위·법률 적합성·사실 검증의 합격 판정이 아닙니다.", ""]
    rows += [f"- [{f['rule']}] " + (f"{f['line']}줄: " if f['line'] else "") + f["message"] for f in result["findings"]]
    if not result["findings"]:
        rows.append("자동 점검에서 수정 후보를 찾지 못했어요. 원문·경험·사진 권리·광고 관계·모바일 미리보기를 사람이 확인하세요.")
    rows += ["", "광고 표시 근거: 공정위 추천·보증 심사지침(2026년 10월 조사 기준), 제목 또는 첫 부분. 키트는 본문 첫 문단을 검사합니다.", "https://www.law.go.kr/LSW/admRulInfoR.do?admRulSeq=2100000280130&chrClsCd=010201", "숫자 메모 예: [출처: https://example.invalid/notice | 확인일 | 해당 근거] / [내 기록: 관찰일 | 실제 관찰 내용]", ""]
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft")
    parser.add_argument("--config")
    parser.add_argument("--affiliate", action="store_true", help="제휴 관계를 직접 알리기(짧은 링크 등 누락 보완)")
    parser.add_argument("--output")
    parser.add_argument("--strict", action="store_true", help="수정 후보가 있으면 종료 코드 2")
    args = parser.parse_args()
    result = inspect(kit_path(args.draft).read_text(encoding="utf-8-sig"), load_config(args.config), args.affiliate)
    value = report(result)
    if args.output:
        save_text(kit_path(args.output), value)
    print(value)
    if args.strict and result["findings"]:
        raise SystemExit(2)


if __name__ == "__main__":
    cli(main)
