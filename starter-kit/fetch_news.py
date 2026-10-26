"""RSS 제목·링크·짧은 요약만 수집. 기사 본문 페이지는 요청하지 않는다."""
import argparse
from html import unescape
import re
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from pathlib import Path

from common import cli, load_config, save_json


def clean(text, limit):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", text or ""))).strip()[:limit]


def fetch(sources, *, offline=True):
    articles = []
    seen = set()
    synthetic_flags = []
    for source in sources:
        remote = str(source).startswith(("http://", "https://"))
        if remote and offline:
            raise ValueError("오프라인에서는 URL을 읽지 않습니다. 로컬 피드를 쓰거나 --online을 명시하세요.")
        if remote:
            with urlopen(source, timeout=20) as response:
                data = response.read(2_000_001)
        else:
            data = Path(source).read_bytes()
        if len(data) > 2_000_000 or b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
            raise ValueError("피드가 너무 크거나 허용하지 않는 XML 선언을 포함합니다.")
        try:
            channel = ET.fromstring(data).find("channel")
        except ET.ParseError as error:
            raise ValueError("RSS XML 형식을 확인하세요.") from error
        if channel is None:
            raise ValueError("RSS 2.0의 channel/item 형식이 필요합니다. Atom은 지원하지 않습니다.")
        synthetic = channel.findtext("synthetic") == "true"
        synthetic_flags.append(synthetic)
        for item in channel.findall("item"):
            title = clean(item.findtext("title"), 120)
            link = clean(item.findtext("link"), 1000)
            if not title or not link.startswith(("https://", "http://")) or link in seen:
                continue
            seen.add(link)
            articles.append({"title": title, "link": link,
                             "summary": clean(item.findtext("description"), 240),
                             "published": clean(item.findtext("pubDate"), 80),
                             "synthetic": synthetic})
    if not articles:
        raise ValueError("제목과 HTTP(S) 링크가 있는 RSS 항목이 없습니다.")
    return {"synthetic": any(synthetic_flags), "articles": articles[:3],
            "notice": "합성 데이터 포함 · 실제 뉴스 아님" if any(synthetic_flags) else "RSS 후보 · 원문 대조와 이용 허락 확인 필요"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config")
    parser.add_argument("--feed", action="append", help="로컬 RSS 경로 또는 --online과 함께 URL")
    parser.add_argument("--online", action="store_true", help="명시한 RSS URL만 네트워크로 읽기")
    parser.add_argument("--output", type=Path, default=Path("output/news.json"))
    args = parser.parse_args()
    save_json(args.output, fetch(args.feed or load_config(args.config)["rss"], offline=not args.online))
    print(args.output)


if __name__ == "__main__":
    cli(main)
