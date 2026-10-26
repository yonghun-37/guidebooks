"""Pillow 자막·자체 타이틀과 pip ffmpeg로 만드는 세로 영상."""
from html import escape
from pathlib import Path
import re
import shutil
import subprocess

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageOps

from common import save_json, digest
from write_script import validate

WIDTH, HEIGHT, FPS = 1080, 1920, 30
PHOTO = {".jpg", ".jpeg", ".png", ".webp"}
CLIP = {".mp4", ".mov", ".mkv", ".webm"}
AUDIO = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}


def ffmpeg(args, cwd=None):
    result = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", *args],
                            cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise ValueError("영상 처리 실패. 손상 파일·지원 형식·음성 트랙·저장 공간을 확인하세요.\n" + result.stderr[-1200:])
    return result


def probe(path):
    result = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-i", str(path)],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
    info = result.stderr
    duration = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", info)
    if not duration:
        raise ValueError(f"미디어 길이를 읽을 수 없습니다: {Path(path).name}")
    h, m, s = map(float, duration.groups())
    video = re.search(r"Video: (\w+).*? (\d{2,5})x(\d{2,5}).*? ([\d.]+) fps", info)
    audio = re.search(r"Audio: (\w+)", info)
    return {"duration": h * 3600 + m * 60 + s,
            "video_codec": video[1] if video else None,
            "size": [int(video[2]), int(video[3])] if video else None,
            "fps": float(video[4]) if video else None, "audio_codec": audio[1] if audio else None}


def wrap(text, font, width):
    lines, line = [], ""
    for char in text:
        if char == "\n":
            lines.append(line or " ")
            line = ""
            continue
        if font.getlength(line + char) > width and line:
            lines.append(line.rstrip())
            line = ""
        line += char
    if line.strip():
        lines.append(line.strip())
    return lines or [" "]


def timestamp(frame):
    milliseconds = round(frame * 1000 / FPS)
    return f"{milliseconds // 3600000:02d}:{milliseconds // 60000 % 60:02d}:{milliseconds // 1000 % 60:02d},{milliseconds % 1000:03d}"


def write_preview(output, timeline, settings, audio):
    rows = "".join(f'<tr><td><button type="button" disabled data-start="{t["start"]}" data-end="{t["end"]}">{i + 1}. {escape(t["title"])}</button></td><td>{t["start"]:g}–{t["end"]:g}초</td><td>{escape(t["subtitle"])}</td></tr>' for i, t in enumerate(timeline))
    audio_html = "".join(f'<label>{"본인 녹음" if kind == "narration" else "배경음 원본"}<audio controls preload="metadata" src="{path}"></audio></label>' for kind, path in audio.items())
    guide = f'left:{settings["safe_left"] / WIDTH * 100}%;right:{settings["safe_right"] / WIDTH * 100}%;top:{settings["safe_top"] / HEIGHT * 100}%;bottom:{settings["safe_bottom"] / HEIGHT * 100}%'
    (output / "preview.html").write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>도윤의 쇼츠 작업실</title>
<style>*{box-sizing:border-box}body{margin:0;background:#faf4eb;color:#322230;font-family:system-ui,sans-serif;line-height:1.65}main{max-width:1000px;margin:auto;padding:24px}h1{font-size:clamp(1.6rem,5vw,2.4rem)}.layout{display:flex;flex-wrap:wrap;gap:24px}.viewer{position:relative;width:min(100%,300px);flex-shrink:0;align-self:flex-start}video{display:block;width:100%;border-radius:16px;background:#221b26}.guide{position:absolute;border:2px dashed #ffcb71;pointer-events:none}section{flex:1;min-width:0}button{padding:10px;margin:3px;border:1px solid #7e3e57;border-radius:8px;background:#fff;color:#322230;cursor:pointer}button:focus-visible,input:focus-visible{outline:3px solid #b7491f;outline-offset:3px}table{border-collapse:collapse;width:100%;font-size:.9rem}td,th{padding:6px;text-align:left;overflow-wrap:anywhere;border-bottom:1px solid #cdbfc5}td:nth-child(2){white-space:nowrap}audio{display:block;width:100%}p{overflow-wrap:anywhere}label{display:block;margin:12px 0}.status{font-weight:bold}@media(max-width:700px){.layout{display:block}.viewer{margin:0 auto 24px}button{max-width:100%;overflow-wrap:anywhere}td:nth-child(2){white-space:nowrap;font-size:.85rem}}</style>
<main><h1>도윤의 쇼츠 작업실</h1><p>서진: 첫 화면을 멈춰 보고, 장면을 골라 반복해 보세요. 자막이 읽히고 말이 끝나는지 확인해요.</p><div class="layout"><div class="viewer"><video id="video" controls playsinline preload="auto" src="short.mp4"></video><div id="guide" class="guide" style="''' + guide + '''" hidden></div></div><section><h2>한 장면씩 확인해요</h2><button id="back" type="button" disabled>이전 프레임</button><button id="next" type="button" disabled>다음 프레임</button><label><input id="loop" type="checkbox"> 고른 장면 반복</label><label><input id="safe" type="checkbox"> 연습용 안전 영역 보기</label><p id="status" class="status" role="status">영상 재생 버튼을 한 번 누른 뒤 장면을 골라요.</p><p>안전 영역은 이 키트의 시작값이에요. 실제 업로드 화면에서 가려짐을 다시 확인하세요.</p><table><thead><tr><th>장면 선택</th><th>시간</th><th>자막</th></tr></thead><tbody>''' + rows + '''</tbody></table><h2>소리를 따로 들어요</h2>''' + (audio_html or '<p>녹음이 없어 무음이에요. 영상의 소리를 켜도 말소리는 나오지 않아요.</p>') + '''<p>따로 듣고 위 완성 영상을 함께 들어 보세요. 음악이 말을 덮으면 설정의 music_gain을 낮추고 다시 출력해요.</p><p>수정은 script.json과 config.yaml에서 하고 render 명령을 실행하세요. 검수 체크는 REVIEW.md에서 기록해요.</p></section></div></main>
<script>const v=document.querySelector('#video'),s=document.querySelector('#status');let start=0,end=0,ready=false;v.addEventListener('timeupdate',()=>{if(!ready&&v.currentTime>0&&v.seekable.length&&v.seekable.end(0)>0){ready=true;document.querySelectorAll('button').forEach(b=>b.disabled=false);s.textContent='장면 버튼을 누르면 그 시작에서 멈춰요.'}});document.querySelectorAll('[data-start]').forEach(b=>b.addEventListener('click',()=>{v.pause();start=+b.dataset.start;end=+b.dataset.end;v.currentTime=start;s.textContent=b.textContent+' · 재생 버튼으로 확인하세요.'}));for(const [id,d] of [['back',-1],['next',1]])document.getElementById(id).addEventListener('click',()=>{v.pause();v.currentTime=Math.max(0,Math.min(v.duration||0,v.currentTime+d/30));s.textContent=v.currentTime.toFixed(3)+'초에서 정지했어요.'});document.querySelector('#safe').addEventListener('change',e=>{document.querySelector('#guide').hidden=!e.target.checked});v.addEventListener('timeupdate',()=>{if(!v.paused&&document.querySelector('#loop').checked&&end>start&&v.currentTime>=end){v.currentTime=start;v.play().catch(()=>{})}});v.addEventListener('ended',()=>{if(document.querySelector('#loop').checked&&end>start&&end>=v.duration){v.currentTime=start;v.play().catch(()=>{})}});</script></html>''', encoding="utf-8")


def render(script, config, output):
    validate(script)
    output = Path(output).resolve()
    settings = config["video"]
    frames_dir = output / "frames"
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(parents=True)
    font = ImageFont.truetype(config["font"], settings["caption_size"])
    title_font = ImageFont.truetype(config["font"], 70)
    small = ImageFont.truetype(config["font"], 36)
    for face in (font, title_font, small):
        face.set_variation_by_axes([500])
    caption_width = WIDTH - settings["safe_left"] - settings["safe_right"]
    total_frames = sum(round(s["duration"] * FPS) for s in script["scenes"])
    duration = total_frames / FPS
    audio, warnings = {}, []
    for kind in ("narration", "music"):
        source = settings.get(kind)
        if source:
            source = Path(source)
            if source.suffix.lower() not in AUDIO or not source.is_file():
                raise ValueError(f"{kind}: 지원하는 로컬 음성 파일을 지정하세요.")
            info = probe(source)
            if not info["audio_codec"]:
                raise ValueError(f"{kind}에 음성 트랙이 없습니다.")
            if kind == "narration":
                if info["duration"] > duration + 1 / FPS:
                    raise ValueError("녹음이 영상보다 깁니다. 말을 자르지 않도록 장면 duration을 늘리세요.")
                if info["duration"] < duration - 1:
                    warnings.append("녹음 뒤 남는 구간은 무음입니다. 자막과 말의 시점을 확인하세요.")
            target = output / "audio" / (kind + source.suffix.lower())
            target.parent.mkdir(exist_ok=True)
            if source.resolve() != target.resolve():
                shutil.copyfile(source, target)
            audio[kind] = target.relative_to(output).as_posix()
    inputs = []
    if settings.get("scenes_dir"):
        folder = Path(settings["scenes_dir"])
        if not folder.is_dir():
            raise ValueError("scenes_dir는 폴더여야 합니다.")
        inputs = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in PHOTO | CLIP)
        if not inputs:
            raise ValueError("장면 폴더에 지원하는 사진·클립이 없습니다.")
        if len(inputs) != len(script["scenes"]):
            raise ValueError("사진·클립 수와 scenes 수를 맞추세요. 파일명 순서로 사용합니다.")
    rights_files = []
    if settings.get("music"):
        evidence = output / "music-license.txt"
        shutil.copyfile(config["rights"]["music"]["evidence"], evidence)
        rights_files.append(evidence.name)
        attribution = config["rights"]["music"].get("attribution", "")
        if attribution and attribution not in script["description"]:
            raise ValueError("필요한 음악 표시문구 attribution을 script.json의 description에도 넣으세요. [Y016]")
    timeline, cues, playlist, source_info = [], [], [], []
    start = 0
    for i, scene in enumerate(script["scenes"]):
        stem = f"scene-{i + 1:02d}"
        count = round(scene["duration"] * FPS)
        source = inputs[i] if inputs else None
        base = frames_dir / f"{stem}.png"
        if source and source.suffix.lower() in PHOTO:
            with Image.open(source) as raw:
                ImageOps.fit(ImageOps.exif_transpose(raw).convert("RGB"), (WIDTH, HEIGHT)).save(base)
        elif not source:
            image = Image.new("RGB", (WIDTH, HEIGHT), "#302134")
            draw = ImageDraw.Draw(image)
            draw.rounded_rectangle((80, 300, 1000, 1250), radius=50, fill="#6e3651")
            draw.ellipse((650, 380, 900, 630), fill="#ed9469")
            draw.text((120, 730), "직접 만드는 쇼츠", font=small, fill="#ffd7ac")
            lines = wrap(scene["title"], title_font, 810)
            if len(lines) > 3:
                raise ValueError("장면 title이 너무 깁니다. 짧게 줄이세요.")
            for j, line in enumerate(lines):
                draw.text((120, 820 + j * 100), line, font=title_font, fill="white")
            draw.text((120, 1150), f"도윤의 연습 · {i + 1}/{len(script['scenes'])}", font=small, fill="white")
            image.save(base)
        if source:
            source_info.append({"name": source.name, "sha256": digest(source)})
        lines = wrap(scene["subtitle"], font, caption_width - 40)
        groups = [lines[n:n + 2] for n in range(0, len(lines), 2)]
        if len(groups) > count:
            raise ValueError("장면 길이에 비해 자막이 너무 많습니다.")
        args = ["-stream_loop", "-1", "-i", str(source)] if source and source.suffix.lower() in CLIP else ["-loop", "1", "-framerate", str(FPS), "-i", str(base)]
        chain = [f"[0:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,crop={WIDTH}:{HEIGHT},setsar=1,fps={FPS},setpts=PTS-STARTPTS[base]"]
        for j, group in enumerate(groups):
            a, b = round(j * count / len(groups)), round((j + 1) * count / len(groups))
            caption = Image.new("RGBA", (caption_width, (settings["caption_size"] + 18) * len(group) + 28), (0, 0, 0, 210))
            draw = ImageDraw.Draw(caption)
            for n, line in enumerate(group):
                draw.text((20, 4 + n * (settings["caption_size"] + 18)), line, font=font, fill="white")
            caption_path = frames_dir / f"{stem}-caption-{j}.png"
            caption.save(caption_path)
            args += ["-loop", "1", "-framerate", str(FPS), "-i", str(caption_path)]
            previous = "base" if j == 0 else f"v{j}"
            y = HEIGHT - settings["safe_bottom"] - caption.height
            if y < settings["safe_top"]:
                raise ValueError("자막이 안전 영역을 넘습니다. 크기·여백을 줄이세요.")
            chain.append(f"[{previous}][{j + 1}:v]overlay=x={settings['safe_left']}:y={y}:enable='gte(n,{a})*lt(n,{b})'[v{j + 1}]")
            cues.append(f"{len(cues) + 1}\n{timestamp(start + a)} --> {timestamp(start + b)}\n" + "\n".join(group) + "\n")
        ffmpeg(args + ["-filter_complex_threads", "1", "-filter_complex", ";".join(chain), "-map", f"[v{len(groups)}]", "-an", "-frames:v", str(count), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26", "-threads", "2", "-r", str(FPS), f"frames/{stem}.mp4"], output)
        timeline.append({"title": scene["title"], "start": start / FPS, "end": (start + count) / FPS, "subtitle": scene["subtitle"], "source": source.name if source else "자체 타이틀"})
        playlist.append(f"file 'frames/{stem}.mp4'")
        start += count
    (output / "frames.txt").write_text("\n".join(playlist) + "\n", encoding="utf-8")
    (output / "subtitles.srt").write_text("\n".join(cues), encoding="utf-8")
    args = ["-f", "concat", "-safe", "0", "-i", "frames.txt"]
    if audio:
        chains, labels = [], []
        for i, (kind, path) in enumerate(audio.items(), 1):
            args += ["-i", path]
            gain = settings["music_gain"] if kind == "music" else 1
            chains.append(f"[{i}:a]apad,atrim=duration={duration},asetpts=PTS-STARTPTS,volume={gain}[a{i}]")
            labels.append(f"[a{i}]")
        chains.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.95:latency=1[audio]")
        args += ["-filter_complex_threads", "1", "-filter_complex", ";".join(chains), "-map", "0:v", "-map", "[audio]"]
    else:
        args += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a"]
    ffmpeg(args + ["-t", str(duration), "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "short.mp4"], output)
    actual = probe(output / "short.mp4")
    if actual["size"] != [WIDTH, HEIGHT] or actual["fps"] != FPS or actual["video_codec"] != "h264" or actual["audio_codec"] != "aac" or abs(actual["duration"] - duration) > 0.1 or actual["duration"] > 180:
        raise ValueError("출력 규격 검사 실패: 영상을 다시 생성하세요.")
    save_json(output / "video-info.json", {**actual, "timeline": timeline, "audio": audio or {"silent": True}, "warnings": warnings,
                                          "sources": source_info, "caption_source": "script.json (대본 기반, 음성 인식 없음)", "caption_size": settings["caption_size"], "rights_files": rights_files})
    write_preview(output, timeline, settings, audio)
    return output / "short.mp4"
