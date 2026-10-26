import copy
import pytest
import check
from common import load_config


def rules(text, affiliate=False, config=None):
    return [f["rule"] for f in check.inspect(text, config or load_config(), affiliate)["findings"]]


def test_shipped_sample():
    from common import ROOT
    assert rules((ROOT / "samples/article.md").read_text()) == []


@pytest.mark.parametrize("text, expected", [
    ("본문만", "title"),
    ("# 짧음", "title_length"),
    ("# 제목\n\n# 또 제목", "title"),
    ("# 제목\n\n#### 단계", "headings"),
    ("# 제목\n\n짧은 본문", "body_length"),
    ("# 제목\n\n![](picture.png)", "image_alt"),
    ('# 제목\n\n<img src="x">', "image_alt"),
    ("# 제목\n\n신청 기간은 30일입니다.", "number_source"),
    ("# 제목\n\n이 문장은 반복되며 지울 필요가 있습니다. 이 문장은 반복되며 지울 필요가 있습니다.", "repeat"),
    ("# 제목\n\n현대 사회에서 알아보도록 하겠습니다.", "cliche"),
    ("# 제목\n\n## 내 경험\n\n[직접 입력]", "experience"),
    ("# 제목\n\n## 내 경험\n\n## 다음 절", "experience"),
])
def test_each_warning(text, expected):
    assert expected in rules(text)


@pytest.mark.parametrize("note", [
    "[출처: https://example.invalid/notice | 오늘 | 공고 문장 확인]",
    "[내 기록: 어제 | 내가 센 항목]"
])
def test_source_note_on_same_line(note):
    assert "number_source" not in rules("# 제목\n\n3개를 확인했어요. " + note)


@pytest.mark.parametrize("note", ["[출처: URL 입력]", "[출처: https://x.invalid | 확인 필요 | 내용]", "[내 기록: | ]", "[내 기록: 오늘]"])
def test_empty_or_placeholder_source(note):
    assert "number_source" in rules("# 제목\n\n금액은 500원이에요. " + note)


def test_url_and_code_numbers_are_not_claims():
    assert "number_source" not in rules("# 제목\n\n[원문](https://example.invalid/2026/10)\n\n```\n10\n```")
    assert "number_source" in rules("# 제목\n\n3개예요.\n\n[출처: https://x.invalid | 오늘 | 설명]")


@pytest.mark.parametrize("url", ["https://link.coupang.com/a/test", "https://shop.invalid/?aff=abc", "https://naver.me/xyz"])
def test_affiliate_needs_first_paragraph(url):
    body = f"# 제목\n\n상품을 소개해요.\n\n[구매]({url})\n\n수수료를 제공받습니다."
    assert "disclosure" in rules(body)
    good = f"# 제목\n\n이 글의 링크로 구매하면 수수료를 제공받습니다.\n\n[구매]({url})"
    assert "disclosure" not in rules(good)


@pytest.mark.parametrize("text", ["수수료를 받을 수도 있습니다.", "광고가 아닙니다.", "수수료를 받지 않습니다.", "수수료를 제공받지 않습니다.", "제품을 제공받는 글이 아닙니다.", "수수료를 제공받을 수 있습니다."])
def test_vague_or_negative_disclosure(text):
    assert "disclosure" in rules("# 제목\n\n" + text, affiliate=True)


def test_comments_cannot_supply_disclosure_or_experience():
    text = "# 제목\n\n<!-- 수수료를 제공받습니다. -->\n\n본문\n\n<!-- ## 내 경험\n관찰했어요. -->"
    assert {"disclosure", "experience"} <= set(rules(text, True))


def test_config_changes_editorial_thresholds():
    config = copy.deepcopy(load_config())
    config["rules"].update(title_min=1, title_max=100, body_min=1, body_max=10000, h2_min=1)
    assert "title_length" not in rules("# 제목", config=config)
    assert "키트 기본값(바꿀 수 있음)" in check.report(check.inspect("# 제목", config))


def test_fenced_examples_do_not_trigger_image_or_affiliate_checks():
    text = "# 예시\n\n```\n![](missing.png)\nhttps://affiliate.invalid\n```"
    assert "image_alt" not in rules(text)
    assert "disclosure" not in rules(text)


def test_line_numbers_survive_multiline_comments():
    result = check.inspect("<!--\n설명\n-->\n# 제목\n\n123원입니다.", load_config())
    assert next(f for f in result["findings"] if f["rule"] == "number_source")["line"] == 6
