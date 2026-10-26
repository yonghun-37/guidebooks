"""Pillow 대체 렌더러로 1080×1350 PNG와 게시용 JPEG를 생성한다."""
import argparse
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import cli, load_config, read_json


@lru_cache(maxsize=64)
def font(path, size):
    face = ImageFont.truetype(path, size)
    try:
        # 동봉 가변 폰트의 기본값(Thin) 대신 읽기 쉬운 중간 굵기를 쓴다.
        axes = face.get_variation_axes()
        face.set_variation_by_axes([min(axis["maximum"], max(axis["minimum"], 500))
                                    if axis["name"] == b"Weight" else axis["default"] for axis in axes])
    except OSError:
        pass  # 사용자가 선택한 일반 고정 굵기 폰트
    return face


def wrap(draw, text, face, width):
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            candidate = (line + " " + word).strip()
            if line and draw.textlength(candidate, font=face) > width:
                lines.append(line.rstrip())
                line = ""
            if draw.textlength(word, font=face) > width:
                for char in word:
                    if line and draw.textlength(line + char, font=face) > width:
                        lines.append(line)
                        line = ""
                    line += char
            else:
                line = (line + " " + word).strip()
        lines.append(line.rstrip())
    return lines


def text_box(draw, text, box, config, size, color):
    x, y, width, height = box
    for current in range(size, 23, -2):
        face = font(config["font"], current)
        lines = wrap(draw, text, face, width)
        spacing = round(current * 1.5)
        if len(lines) * spacing <= height:
            for line in lines:
                draw.text((x, y), line, font=face, fill=color)
                y += spacing
            return
    raise ValueError("글이 영역을 넘칩니다. copy.json 문안을 줄이고 다시 렌더링하세요.")


def render_cards(copy, config, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    colors = config["colors"]
    paths = []
    for i, scene in enumerate(copy["scenes"], 1):
        image = Image.new("RGB", (1080, 1350), colors["background"])
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 1080, 24), fill=colors["accent"])
        text_box(draw, copy["account_name"], (80, 75, 920, 80), config, 30, colors["foreground"])
        draw.rounded_rectangle((80, 185, 1000, 265), radius=18, fill=colors["foreground"])
        text_box(draw, copy["label"], (108, 195, 860, 65), config, 30, "white")
        text_box(draw, scene["title"], (80, 330, 920, 330), config, 68, colors["foreground"])
        draw.rectangle((80, 710, 200, 720), fill=colors["accent"])
        text_box(draw, scene["body"], (80, 765, 920, 340), config, 42, colors["foreground"])
        text_box(draw, "출처: " + scene["source"], (80, 1150, 920, 90), config, 24, colors["foreground"])
        draw.text((80, 1270), "REELSBOOK / 연습하고 검수하기", font=font(config["font"], 22), fill=colors["accent"])
        draw.text((890, 1270), f"{i:02d} / {len(copy['scenes']):02d}", font=font(config["font"], 22), fill=colors["foreground"])
        path = output / f"card-{i:02d}.png"
        image.save(path)
        image.save(path.with_suffix(".jpg"), quality=92)
        paths.append(path)
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("copy", type=Path)
    parser.add_argument("--config")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    for path in render_cards(read_json(args.copy), load_config(args.config), args.output):
        print(path)


if __name__ == "__main__":
    cli(main)
