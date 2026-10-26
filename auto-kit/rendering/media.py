"""복사한 키트 렌더러를 공통 문안에 연결하고 실제 파일을 검사한다."""
import json
from pathlib import Path
import re
import shutil
import subprocess
from html import escape
import imageio_ffmpeg
from common import kit_path, save_json
from . import cards, short_base

def ffmpeg(args):
    result = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-y', *map(str, args)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise ValueError('ffmpeg 처리 실패. 파일·코덱·폰트·저장 공간을 확인하세요.')
    return result

def probe_media(path):
    """ffprobe가 있으면 JSON, pip ffmpeg만 있으면 기존 키트 parser를 쓴다."""
    executable = shutil.which('ffprobe')
    if executable:
        result = subprocess.run([executable, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], capture_output=True, text=True)
        try:
            raw = json.loads(result.stdout)
            video = next(s for s in raw['streams'] if s['codec_type'] == 'video')
            audio = next(s for s in raw['streams'] if s['codec_type'] == 'audio')
            a, b = map(float, video['r_frame_rate'].split('/'))
            info = {'width': video['width'], 'height': video['height'], 'fps': a/b, 'video_codec': video['codec_name'], 'audio_codec': audio['codec_name'], 'duration': float(raw['format']['duration'])}
        except (ValueError, KeyError, StopIteration):
            raise ValueError('ffprobe에서 영상·음성 규격을 읽지 못했습니다.') from None
        method = 'ffprobe JSON'
    else:
        raw = short_base.probe(path)
        if not raw['size']:
            raise ValueError('미디어에 영상 트랙이 없습니다.')
        info = {'width': raw['size'][0], 'height': raw['size'][1], 'fps': raw['fps'], 'video_codec': raw['video_codec'], 'audio_codec': raw['audio_codec'], 'duration': raw['duration']}
        method = 'pip ffmpeg stderr parser (shorts-kit 재사용)'
    result = ffmpeg(['-i', path, '-vn', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    try:
        measure = json.loads(re.search(r'\{\s*"input_i".*?\}', result.stderr, re.S)[0])
        lufs = float(measure['input_i'])
        if not -100 < lufs < 20:
            lufs = None
    except (TypeError, ValueError):
        lufs = None
    return {**info, 'lufs': lufs, 'probe_method': method}

def render(draft, config, output, flow, provider):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    media = config['media']
    flow_config = config['flows'][flow]
    display = {
        'name': flow_config['account_name' if flow == 'insta' else 'channel_name'],
        'creator_name': flow_config['creator_name'],
        'preview_speaker': flow_config['preview_speaker'],
    }
    font = str(kit_path(media['font']))
    backgrounds = []
    folder = kit_path(media['scenes_dir']) if media.get('scenes_dir') else None
    if folder:
        backgrounds = sorted(p for p in folder.iterdir() if p.suffix.lower() in short_base.PHOTO | short_base.CLIP)
        if len(backgrounds) != len(draft['scenes']):
            raise ValueError('소재 파일 수와 장면 수를 맞추세요. 파일명 순서로 사용합니다.')
    elif media['image_api'] or media['video_api']:
        assets = output / 'assets'
        assets.mkdir(exist_ok=True)
        for i, scene in enumerate(draft['scenes']):
            image_path = assets / f'image-{i:02d}.png'
            if not image_path.exists():
                provider.media('image', scene['title'] + ' — 글자 없는 상징적 일러스트', image_path)
            background = image_path
            if media['video_api']:
                video_path = assets / f'video-{i:02d}.mp4'
                if not video_path.exists():
                    provider.media('video', scene['title'], video_path, image=str(image_path), seconds=5)
                background = video_path
            backgrounds.append(background)
        folder = assets
    files = []
    if flow == 'insta':
        scenes = []
        for i, scene in enumerate(draft['scenes']):
            row = {'layout': 'cover' if i == 0 else ('closing' if i == len(draft['scenes']) - 1 else 'body'), 'title': scene['title'], 'body': scene['text'], 'points': [scene['text']], 'source': '원문 링크는 미리보기·게시 문안에서 확인'}
            if backgrounds and backgrounds[i].suffix.lower() in short_base.PHOTO:
                row['image'] = str(backgrounds[i])
            scenes.append(row)
        copy = {'account_name': display['name'], 'scenes': scenes, 'synthetic': True, 'label': '직접 작성한 예시 문안 · AI 제작 보조' if provider.mock else 'AI 제작 보조 · 원문 확인', 'caption': draft['caption']}
        cards.render_cards(copy, {'font': font, 'colors': cards.THEMES['forest'], 'asset_root': '/'}, output / 'cards')
        files = sorted((output / 'cards').glob('*.jpg'))
    if flow == 'shorts' or media['motion_reel'] or config['instagram']['format'] == 'reel':
        recording = kit_path(media['recording']) if media.get('recording') else output / 'narration.wav'
        if not recording.exists():
            provider.media('tts', draft['narration'], recording, seconds=sum(s['duration'] for s in draft['scenes']))
        duration = short_base.probe(recording)['duration']
        if not 3 <= duration <= (180 if flow == 'shorts' else 900):
            raise ValueError('녹음/TTS 길이가 범위를 벗어났습니다. 음성을 자르지 않고 중단합니다.')
        original_duration = sum(s['duration'] for s in draft['scenes'])
        scale = max(1, duration / original_duration)
        scenes = [{'title': s['title'], 'subtitle': s['text'], 'duration': s['duration'] * scale} for s in draft['scenes']]
        # 생성 이미지/영상이 섞인 폴더는 사용할 파일만 모은다.
        scene_dir = None
        if backgrounds:
            scene_dir = output / 'scene-inputs'
            scene_dir.mkdir(exist_ok=True)
            for previous in scene_dir.iterdir():
                previous.unlink()
            for i, background in enumerate(backgrounds):
                shutil.copyfile(background, scene_dir / (f'{i:02d}' + background.suffix))
        settings = {'caption_size': 48, 'safe_left': 90, 'safe_right': 90, 'safe_top': 250, 'safe_bottom': 320, 'narration': str(recording), 'music': None, 'music_gain': .1, 'scenes_dir': str(scene_dir) if scene_dir else None}
        script = {'scenes': scenes, 'label': 'AI 제작 보조', 'description': draft['caption']}
        video = short_base.render(script, {'font': font, 'video': settings, 'display': display}, output)
        normalized = output / 'normalized.mp4'
        ffmpeg(['-i', video, '-c:v', 'copy', '-af', f"loudnorm=I={media['lufs_target']}:TP=-1.5:LRA=11", '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', normalized])
        normalized.replace(video)
        if flow == 'shorts' or config['instagram']['format'] == 'reel':
            files = [video]
    title = escape(draft['title'])
    preview_title = escape(display['name'] + ' · 미리보기')
    speaker = escape(display['preview_speaker'])
    visuals = ''.join(f'<img alt="카드 {i+1}" src="{p.relative_to(output).as_posix()}">' if p.suffix == '.jpg' else f'<video controls src="{p.name}"></video>' for i, p in enumerate(files))
    (output / 'preview.html').write_text(f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{preview_title}</title><style>:root{{color-scheme:light dark}}body{{font:18px/1.7 system-ui;max-width:1000px;margin:auto;padding:20px}}img,video{{max-width:min(100%,350px);vertical-align:top;margin:8px}}</style><h1>{preview_title}</h1><h2>{title}</h2><p>{speaker}: 계정·채널명과 자막을 확인하세요.</p><p>{escape(draft["caption"])}</p>{visuals}<p>mock 음성은 설명용 신호음입니다. 대본 자막은 장면 시간에 배분하며 음성 정렬을 하지 않습니다.</p></html>', encoding='utf-8')
    save_json(output / 'render-info.json', {'files': [str(p) for p in files], 'flow': flow})
    return files
