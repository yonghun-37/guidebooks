"""카드 줌/팬·전환·자막 등장·진행 막대 + 선택적 사용자 음원 → 세로 MP4."""
import argparse
from pathlib import Path
import shutil
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw

from audio import prepare_audio
from common import cli, load_config, read_json, save_json
from render_cards import plain, text_box
from write_copy import validate_copy


def ffmpeg_exe():
    return shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()


def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def encode(command, output):
    result = subprocess.run([ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", *command],
                            cwd=output, capture_output=True, text=True)
    if result.returncode:
        raise ValueError("영상 생성 실패: " + result.stderr[-1500:])


def make_reel(copy, config, cards, output):
    validate_copy(copy)
    if len(cards) != len(copy["scenes"]):
        raise ValueError("장면 수와 카드 수가 다릅니다.")
    if not 15 <= float(config["reel"]["duration"]) <= 30:
        raise ValueError("릴스 duration은 15~30초로 설정하세요.")
    output = Path(output).resolve()
    frames = output / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    # 재렌더링할 때 이전 음원이나 장면 파일을 검수표에 섞지 않는다.
    for old in frames.glob("*"):
        if old.is_file():
            old.unlink()
    audio_dir = output / "audio"
    if audio_dir.exists():
        # 사용자가 이 폴더의 파일을 입력으로 지정했을 수 있으므로 입력 준비 뒤 정리한다.
        old_audio = set(audio_dir.glob("*"))
    else:
        old_audio = set()
    audio = prepare_audio(copy, config, output)
    for old in old_audio - set(audio.values()):
        if old.is_file():
            old.unlink()
    fps = 24
    total_frames = round(float(config["reel"]["duration"]) * fps)
    duration = total_frames / fps
    c = config["colors"]
    accent = c["accent"].replace("#", "0x")
    playlist, subtitles, timing = [], [], []
    for index, (card, scene) in enumerate(zip(cards, copy["scenes"], strict=True)):
        start = round(index * total_frames / len(cards))
        end = round((index+1) * total_frames / len(cards))
        count = end - start
        seconds = count / fps
        stem = f"scene-{index+1:02d}"
        frame = Image.new("RGB", (1080, 1920), c["foreground"])
        with Image.open(card) as image:
            frame.paste(image.resize((960, 1200), Image.Resampling.LANCZOS), (60, 170))
        draw = ImageDraw.Draw(frame)
        text_box(draw, copy["account_name"], (90, 70, 900, 70), config, 28, "white")
        text_box(draw, "읽고 · 확인하고 · 직접 만들기", (90, 1730, 900, 65), config, 25, "white")
        frame.save(frames / f"{stem}.png")
        caption = Image.new("RGBA", (900, 260), (0, 0, 0, 0))
        text_box(ImageDraw.Draw(caption), plain(scene["subtitle"]), (0, 0, 900, 250), config, 44, "white")
        caption.save(frames / f"{stem}-caption.png")
        # 자막은 카드 줌과 분리해 고정 안전 영역에 나타난다. 장면 경계는 짧은 페이드다.
        filters = (
            f"[0:v]zoompan=z='1.025+0.025*on/{max(count-1,1)}':"
            f"x='(iw-iw/zoom)*on/{max(count-1,1)}':y='(ih-ih/zoom)/2':d=1:s=1080x1920:fps={fps}[zoom];"
            "[1:v]format=rgba,fade=t=in:st=0:d=0.45:alpha=1[caption];"
            "[zoom][caption]overlay=x=90:y='1450+55*max(0,1-t/0.45)':shortest=1,"
            "drawbox=x=90:y=1810:w=900:h=8:color=0x71827D:t=fill[base];"
            f"color=c={accent}:s=900x8:r={fps},format=rgba[bar];"
            f"color=c=0x71827D:s=900x8:r={fps}[track];"
            f"[track][bar]overlay=x='-900+900*({start/fps}+t)/{duration}':y=0:shortest=1[progress];"
            "[base][progress]overlay=x=90:y=1810:shortest=1,"
            f"fade=t=in:st=0:d=0.18,fade=t=out:st={seconds-0.18:.6f}:d=0.18,format=yuv420p[v]"
        )
        encode(["-loop", "1", "-framerate", str(fps), "-i", f"frames/{stem}.png",
                "-loop", "1", "-framerate", str(fps), "-i", f"frames/{stem}-caption.png",
                "-filter_complex_threads", "1", "-filter_complex", filters, "-map", "[v]",
                "-frames:v", str(count), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "27",
                "-threads", "2", "-video_track_timescale", "12288", f"frames/{stem}.mp4"], output)
        playlist.append(f"file 'frames/{stem}.mp4'")
        subtitles.append(f"{index+1}\n{timestamp(start/fps)} --> {timestamp(end/fps)}\n{plain(scene['subtitle'])}\n")
        timing.append({"scene": index+1, "start": start/fps, "end": end/fps})
    (output / "frames.txt").write_text("\n".join(playlist) + "\n", encoding="utf-8")
    (output / "subtitles.srt").write_text("\n".join(subtitles), encoding="utf-8")
    command = ["-f", "concat", "-safe", "0", "-i", "frames.txt"]
    if audio:
        chains, labels = [], []
        for index, (kind, path) in enumerate(audio.items(), 1):
            command += ["-i", str(path)]
            volume = 0.18 if kind == "music" else 1.0
            label = f"a{index}"
            chains.append(f"[{index}:a]apad,atrim=duration={duration},asetpts=PTS-STARTPTS,volume={volume}[{label}]")
            labels.append(f"[{label}]")
        chains.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.95[audio]")
        command += ["-filter_complex", ";".join(chains), "-map", "0:v", "-map", "[audio]"]
    else:
        command += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a"]
    command += ["-t", str(duration), "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-ar", "48000",
                "-ac", "2", "-movflags", "+faststart", "reel.mp4"]
    encode(command, output)
    save_json(output / "reel-info.json", {"duration": duration, "size": [1080, 1920], "fps": fps,
                                        "tts": config["reel"]["tts"], "audio": list(audio) or ["silent"],
                                        "audio_files": [p.relative_to(output).as_posix() for p in audio.values()],
                                        "motion": ["zoom-pan", "scene-fade", "caption-entry", "progress-bar"],
                                        "timing": timing, "subtitles": "burned-in + subtitles.srt"})
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
