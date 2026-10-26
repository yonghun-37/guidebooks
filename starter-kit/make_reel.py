"""카드 + 무음 오디오 + 영상 내 자막 → 세로 MP4. 다운로드·TTS API 없음."""
import argparse
from pathlib import Path
import shutil
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw

from common import cli, load_config, read_json, save_json
from render_cards import text_box


def ffmpeg_exe():
    return shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()


def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def make_reel(copy, config, cards, output):
    output = Path(output)
    frames = output / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    duration = float(config["reel"]["duration"])
    per_scene = duration / len(cards)
    playlist, subtitles = [], []
    for i, (card, scene) in enumerate(zip(cards, copy["scenes"], strict=True), 1):
        frame = Image.new("RGB", (1080, 1920), config["colors"]["foreground"])
        with Image.open(card) as image:
            frame.paste(image.resize((960, 1200), Image.Resampling.LANCZOS), (60, 190))
        draw = ImageDraw.Draw(frame)
        text_box(draw, copy["label"], (80, 90, 920, 80), config, 32, "white")
        text_box(draw, scene["subtitle"], (90, 1450, 900, 270), config, 44, "white")
        text_box(draw, "무음 + 자막 / 게시 전 사람 검수", (90, 1750, 900, 70), config, 28, "white")
        name = f"frames/scene-{i:02d}.png"
        frame.save(output / name)
        playlist.extend([f"file '{name}'", f"duration {per_scene:.6f}"])
        subtitles.append(f"{i}\n{timestamp((i-1)*per_scene)} --> {timestamp(i*per_scene)}\n{scene['subtitle']}\n")
    playlist.append(f"file '{name}'")
    (output / "frames.txt").write_text("\n".join(playlist) + "\n", encoding="utf-8")
    (output / "subtitles.srt").write_text("\n".join(subtitles), encoding="utf-8")
    command = [ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
               "-f", "concat", "-safe", "0", "-i", "frames.txt",
               "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(duration),
               "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast",
               "-crf", "25", "-threads", "2", "-c:a", "aac", "-b:a", "64k",
               "-movflags", "+faststart", "reel.mp4"]
    result = subprocess.run(command, cwd=output, capture_output=True, text=True)
    if result.returncode:
        raise ValueError("영상 생성 실패: " + result.stderr[-2000:])
    save_json(output / "reel-info.json", {"duration": duration, "size": [1080, 1920], "fps": 24,
                                        "tts": "silent", "subtitles": "burned-in + subtitles.srt",
                                        "ffmpeg": ffmpeg_exe()})
    return output / "reel.mp4"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("copy", type=Path)
    parser.add_argument("--cards", type=Path, required=True)
    parser.add_argument("--config")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    copy = read_json(args.copy)
    cards = [args.cards / f"card-{i:02d}.png" for i in range(1, len(copy["scenes"]) + 1)]
    print(make_reel(copy, load_config(args.config), cards, args.output))


if __name__ == "__main__":
    cli(main)
