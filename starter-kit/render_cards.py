"""표지·번호 본문·출처 마무리를 1080×1350 PNG/JPEG로 렌더링한다."""
import argparse
from functools import lru_cache
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont, ImageOps

from common import cli, load_config, read_json
from write_copy import validate_copy

THEMES = {
    "forest": {"background": "#F5F3EA", "foreground": "#153B33", "accent": "#167858"},
    "ink": {"background": "#F0F2F5", "foreground": "#182B4A", "accent": "#3459BE"},
    "coral": {"background": "#FFF2E8", "foreground": "#462C32", "accent": "#BA423A"},
}


@lru_cache(maxsize=128)
def font(path, size, weight=500):
    face = ImageFont.truetype(path, size)
    try:
        axes = face.get_variation_axes()
        face.set_variation_by_axes([min(axis["maximum"], max(axis["minimum"], weight))
                                    if axis["name"] == b"Weight" else axis["default"] for axis in axes])
    except OSError:
        pass
    return face


def plain(text):
    return text.replace("**", "")


def rich_lines(draw, text, face, width):
    """강조 상태를 보존해 단어 우선 줄바꿈한다. 긴 단어·URL은 글자 단위로 나눈다."""
    lines, line, length, strong = [], [], 0, False
    for token in re.split(r"(\*\*|\n|[^\S\n]+)", text):
        if token == "**":
            strong = not strong
            continue
        if token == "\n":
            lines.append(line)
            line, length = [], 0
            continue
        if not token:
            continue
        token_width = draw.textlength(token, font=face)
        if length + token_width > width and line:
            lines.append(line)
            line, length = [], 0
        if not line and token.isspace():
            continue
        for char in token:
            char_width = draw.textlength(char, font=face)
            if length + char_width > width and line:
                lines.append(line)
                line, length = [], 0
            line.append((char, strong))
            length += char_width
    if line:
        lines.append(line)
    return lines


def wrap(draw, text, face, width):
    return ["".join(char for char, _ in line) for line in rich_lines(draw, text, face, width)]


def text_box(draw, text, box, config, size, color, accent=None, weight=500):
    x, top, width, height = box
    minimum = min(size, 24)
    for current in range(size, minimum - 1, -2):
        face = font(config["font"], current, weight)
        lines = rich_lines(draw, text, face, width)
        spacing = round(current * 1.45)
        if len(lines) * spacing <= height:
            y = top
            for line in lines:
                left = x
                # 같은 강조 상태를 묶어 자간/커닝을 일정하게 유지한다.
                runs = []
                for char, strong in line:
                    if runs and runs[-1][1] == strong:
                        runs[-1] = (runs[-1][0] + char, strong)
                    else:
                        runs.append((char, strong))
                for value, strong in runs:
                    draw.text((left, y), value, font=face, fill=(accent or color) if strong else color)
                    left += draw.textlength(value, font=face)
                y += spacing
            return
    raise ValueError("글이 영역을 넘칩니다. copy.json 문안을 줄이고 다시 렌더링하세요.")


def image_slot(canvas, scene, box, config):
    x, y, width, height = box
    colors = config["colors"]
    if scene.get("image"):
        if "://" in scene["image"]:
            raise ValueError("image에는 사용자 제공 로컬 파일만 지정하세요.")
        path = Path(scene["image"])
        path = Path(config.get("asset_root", ".")) / path
        with Image.open(path) as supplied:
            tile = ImageOps.fit(ImageOps.exif_transpose(supplied).convert("RGB"), (width, height))
    else:
        tile = Image.new("RGB", (width, height), colors["accent"])
        draw = ImageDraw.Draw(tile)
        # 자체 제작한 기하 패턴. 사건 사진이나 AI 증거 사진을 흉내 내지 않는다.
        for offset in range(-height, width + height, 84):
            draw.line((offset, height, offset + height, 0), fill=colors["foreground"], width=2)
        radius = min(height, width) // 2
        cx, cy = width * 3 // 4, height // 2
        draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), fill=colors["background"])
        draw.ellipse((cx-radius//2, cy-radius//2, cx+radius//2, cy+radius//2), fill=colors["accent"])
    canvas.paste(tile, (x, y))


def render_cards(copy, config, output):
    validate_copy(copy)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    c = config["colors"]
    paths = []
    for i, scene in enumerate(copy["scenes"], 1):
        closing = scene["layout"] == "closing"
        bg, fg = (c["foreground"], c["background"]) if closing else (c["background"], c["foreground"])
        image = Image.new("RGB", (1080, 1350), bg)
        draw = ImageDraw.Draw(image)
        draw.ellipse((72, 76, 94, 98), fill=fg if closing else c["accent"])
        text_box(draw, copy["account_name"], (112, 60, 760, 64), config, 28, fg)
        draw.line((72, 145, 1008, 145), fill=fg, width=2)
        layout = scene["layout"]
        if layout == "cover":
            text_box(draw, "LIFE NEWS / 신청 전 체크", (72, 184, 900, 60), config, 25, c["accent"])
            text_box(draw, scene["title"], (66, 268, 940, 350), config, 100, fg, c["accent"], 750)
            text_box(draw, scene["body"], (76, 628, 900, 130), config, 34, fg, c["accent"])
            image_slot(image, scene, (72, 818, 936, 330), config)
            draw = ImageDraw.Draw(image)
            text_box(draw, "넘겨서 읽기  →", (72, 1180, 880, 60), config, 27, c["accent"])
        elif layout == "body":
            text_box(draw, f"BRIEF / {i-1:02d}", (72, 180, 900, 55), config, 25, c["accent"])
            text_box(draw, scene["title"], (72, 250, 936, 190), config, 56, fg, c["accent"], 700)
            image_slot(image, scene, (72, 486, 936, 194), config)
            draw = ImageDraw.Draw(image)
            points = scene["points"]
            row_height = min(180, 430 // len(points))
            for number, point in enumerate(points, 1):
                y = 730 + (number-1) * row_height
                draw.rounded_rectangle((72, y+12, 128, y+68), radius=14, fill=c["accent"])
                draw.text((87, y+17), str(number), font=font(config["font"], 27, 700), fill="white")
                text_box(draw, point, (156, y, 838, row_height-12), config, 35, fg, c["accent"])
            text_box(draw, "출처  " + scene["source"], (72, 1178, 936, 70), config, 22, fg)
        else:
            text_box(draw, "SAVE / 신청 전에 다시 확인", (72, 188, 936, 60), config, 25, fg)
            text_box(draw, scene["title"], (66, 298, 940, 320), config, 90, fg, "#E4D891", 750)
            text_box(draw, scene["body"], (76, 670, 900, 170), config, 39, fg, "#E4D891")
            draw.line((72, 895, 1008, 895), fill=fg, width=2)
            text_box(draw, "SOURCE / 원출처", (72, 930, 936, 50), config, 24, fg)
            text_box(draw, scene["source"], (72, 1000, 936, 175), config, 25, fg)
            text_box(draw, copy["account_name"], (72, 1186, 936, 55), config, 29, fg)
        draw.line((72, 1260, 1008, 1260), fill=fg, width=1)
        if copy["synthetic"]:
            draw.text((72, 1280), copy["label"], font=font(config["font"], 18), fill=fg)
        draw.text((900, 1280), f"{i:02d} / {len(copy['scenes']):02d}", font=font(config["font"], 19), fill=fg)
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
