"""API 없는 규칙 기반 문안 후보. JSON을 사람이 편집한 뒤 렌더링한다."""
import argparse
from pathlib import Path

from common import cli, read_json, save_json


def write_copy(news, config):
    synthetic = news["synthetic"]
    label = "합성 데이터 · 실제 뉴스 아님" if synthetic else "출처 대조 전 · 문안 초안"
    scenes = [{"title": "한 장씩 만드는\n오늘의 연습", "body": "소재를 고르고, 핵심을 적고,\n사람이 확인합니다.\n이 카드부터 직접 만들어 보세요.",
               "subtitle": "합성 피드로 카드와 릴스를 만드는 연습입니다." if synthetic else "RSS에서 고른 소재입니다. 게시 전 원문과 이용 조건을 확인하세요.",
               "source": "동봉 합성 피드" if synthetic else "RSS 후보 묶음"}]
    for article in news["articles"]:
        summary = article["summary"] or "[직접 편집] 원출처를 읽고 확인한 핵심을 적으세요."
        # 후보 추출만 수행한다. 인명·수치·조건을 임의로 바꾸거나 새로운 사실을 만들지 않는다.
        scenes.append({"title": article["title"], "body": summary,
                       "subtitle": article["title"], "source": article["link"],
                       "published": article["published"]})
    caption = label + "\n" + "\n".join(a["title"] + "\n" + a["link"] for a in news["articles"])
    return {"synthetic": synthetic, "label": label, "account_name": config["account_name"],
            "caption": caption, "is_ai_generated": config["publish"]["is_ai_generated"],
            "editing_note": "규칙 기반 후보입니다. copy.json의 title/body/subtitle/caption을 사람이 검토·편집하세요.",
            "scenes": scenes}


def main():
    from common import load_config
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("news", type=Path)
    parser.add_argument("--config")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    save_json(args.output, write_copy(read_json(args.news), load_config(args.config)))
    print(args.output)


if __name__ == "__main__":
    cli(main)
