"""편집한 완성 견본. 기본 실행은 동봉 음성을 재사용하며 네트워크를 쓰지 않는다."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import tempfile
import wave
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'samples' / 'editorial'
INK = '#142d2a'
PAPER = '#f7f4e9'
GREEN = '#166750'
MINT = '#dce9d5'
GOLD = '#efc868'
CORAL = '#d57859'
FPS = 24
W, H = 1080, 1920

# 같은 영상의 단계별 원고. 한 음성 파일 = 한 자막 = 한 장면이다.
CUES = [
    ('월급은 들어왔는데,\n어디에 쓸지 막막한가요?', '월급은 들어왔는데, 어디에 쓸지 막막한가요?', -1),
    ('오늘은 십 분만,\n메모를 네 칸으로 나눠요.', '오늘은 십 분만, 메모를 네 칸으로 나눠요.', -1),
    ('월세와 관리비. 이번 달\n꼭 나갈 돈부터 적어요.', '월세와 관리비. 이번 달 꼭 나갈 돈부터 적어요.', 0),
    ('둘째는 생활비.\n식비와 교통비를 적어요.', '둘째는 생활비. 식비와 교통비를 적어요.', 1),
    ('셋째는 비상금.\n갑자기 필요한 돈이에요.', '셋째는 비상금. 갑자기 필요한 돈이에요.', 2),
    ('마지막은 목표. 여행이나\n이사처럼 이름을 붙여요.', '마지막은 목표. 여행이나 이사처럼 이름을 붙여요.', 3),
    ('정해진 비율은 없어요.\n내 상황에 맞게 채워요.', '정해진 비율은 없어요. 내 상황에 맞게 채워요.', 4),
    ('저장해 두고, 다음 월급날\n네 칸을 채워 보세요.', '저장해 두고, 다음 월급날 네 칸을 채워 보세요.', 4),
]


@lru_cache(maxsize=40)
def font(size, bold=False):
    """--font-dir 또는 NOTO_KR_FONT_DIR로 설치한 Noto Sans CJK KR을 지정한다."""
    directory = Path(os.environ.get('NOTO_KR_FONT_DIR', Path.home()/'.local/share/fonts/noto-cjk-kr'))
    return ImageFont.truetype(str(directory / ('NotoSansCJKkr-Bold.otf' if bold else 'NotoSansCJKkr-Regular.otf')), size)


def text(draw, xy, value, size=42, fill=INK, bold=False, spacing=14):
    draw.multiline_text(xy, value, font=font(size, bold), fill=fill, spacing=spacing)


def roundbox(draw, box, fill, radius=28, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def run(args, **kwargs):
    return subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-y', *map(str, args)], check=True, **kwargs)


def cards():
    target = OUT/'instagram'; target.mkdir(parents=True, exist_ok=True)
    for n in range(4):
        im = Image.new('RGB', (1080, 1350), PAPER); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 1080, 18), fill=GREEN)
        text(d, (76, 70), '출근길 3분 생활 뉴스', 30, GREEN, True)
        text(d, (840, 70), f'{n+1:02d} / 04', 28, GREEN)
        if n == 0:
            roundbox(d, (76, 160, 370, 217), MINT, 16)
            text(d, (95, 170), '신청 전 체크리스트', 27, GREEN, True)
            text(d, (76, 275), '청년 지원금,\n신청 전에\n이것부터 봐요.', 91, bold=True, spacing=12)
            text(d, (80, 668), '공고를 읽을 때는 딱 세 줄부터.', 38)
            for i, label in enumerate(('내가 대상인가요?', '언제까지 내나요?', '무엇을 준비하나요?')):
                y = 800 + i*109
                d.ellipse((80, y, 136, y+56), fill=GREEN)
                text(d, (98, y+6), str(i+1), 31, PAPER, True)
                text(d, (163, y+3), label, 43, bold=True)
        else:
            titles = ('내가 대상인지\n먼저 확인해요.', '마감일은\n달력에 남겨요.', '필요한 서류는\n목록으로 적어요.')
            labels = ('01  대상', '02  기간', '03  서류')
            text(d, (76, 177), labels[n-1], 37, GREEN, True)
            text(d, (76, 264), titles[n-1], 80, bold=True, spacing=16)
            roundbox(d, (76, 548, 1004, 990), '#ffffff', 28)
            if n == 1:
                items = [('나이', '공고에 적힌 기준일도 확인'), ('거주지', '주민등록 등 요구 기준 확인'), ('소득', '어떤 기준으로 계산하는지 확인')]
            elif n == 2:
                items = [('시작일', '접수를 시작하는 날짜'), ('마감일', '마지막 날의 마감 시각까지'), ('내 할 일', '서류 준비할 날을 먼저 정하기')]
            else:
                items = [('서류 이름', '공고의 목록을 그대로 메모'), ('발급 방법', '온라인 발급 여부 확인'), ('제출 방법', '파일 형식과 제출처 확인')]
            for i, (a, b) in enumerate(items):
                y = 594+i*130
                d.line((111, y+110, 965, y+110), fill='#e0e6df', width=2)
                text(d, (110, y), a, 35, GREEN, True)
                text(d, (110, y+49), b, 35)
            end = ('해당 공고의 조건에 하나씩 표시해요.', '저장만 하지 말고 일정도 남겨요.', '저장해 두고 실제 공고와 대조해요.')[n-1]
            text(d, (80, 1055), end, 37, GREEN, True)
        d.line((76, 1180, 1004, 1180), fill='#c5d1c4', width=2)
        text(d, (78, 1205), '가상 공고 · 안내 예시', 30, GREEN, True)
        text(d, (78, 1255), '실제 신청은 해당 기관의 최신 공고에서 확인하세요.', 28)
        for suffix in ('png', 'jpg', 'webp'):
            options = {'quality':91} if suffix != 'png' else {}
            im.save(target/f'instagram-{n+1:02d}.{suffix}', **options)
    caption = '지원금 소식을 봤다면, 신청 버튼보다 공고부터 읽어요.\n① 대상: 나이·거주지·소득 기준 확인\n② 기간: 접수일과 마감 시각을 달력에 기록\n③ 서류: 이름·발급 방법·제출 방법을 목록으로 정리\n저장해 두고 실제 공고와 하나씩 대조해 보세요.\n\n가상 공고를 바탕으로 만든 안내 예시입니다. 특정 지원제도의 대상·금액·일정을 안내하는 게시물이 아닙니다. 실제 신청 전 해당 기관의 최신 공고를 확인하세요.\n#생활정보 #청년지원금 #신청체크리스트'
    (target/'caption.txt').write_text(caption+'\n', encoding='utf-8')


def voice(model_dir):
    """명시적으로 --regenerate-voice를 줄 때만 선택 설치된 로컬 TTS를 부른다."""
    from supertonic import TTS
    from huggingface_hub import snapshot_download
    import numpy as np
    np.random.seed(26)
    snapshot_download('Supertone/supertonic-3', revision='724fb5abbf5502583fb520898d45929e62f02c0b', local_dir=model_dir)
    engine = TTS(model_dir=model_dir, auto_download=False, intra_op_num_threads=4)
    style = engine.get_voice_style('F1')
    target = OUT/'shorts'/'voice'; target.mkdir(parents=True, exist_ok=True)
    for i, (_, narration, _) in enumerate(CUES):
        wav, duration = engine.synthesize(narration, voice_style=style, lang='ko', speed=1.0, total_steps=12)
        engine.save_audio(wav, str(target/f'{i+1:02d}.wav'))
        print(f'한국어 합성음 {i+1}/8 · {float(duration[0]):.2f}초', flush=True)


def video_frame(index, elapsed, duration):
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    text(d, (100, 206), '자취생 10분 생존법', 32, GREEN, True)
    text(d, (100, 280), '월급날 10분', 92, bold=True)
    text(d, (105, 403), '돈이 갈 곳을 네 칸에 적어요.', 43)
    # 직접 그린 메모. 화면 모서리의 앱 버튼과 아래 설명란을 피해 중앙에 둔다.
    roundbox(d, (100, 566, 940, 1295), '#fffefa', 25, '#d4d9ce', 3)
    d.rectangle((100, 594, 940, 601), fill=GOLD)
    cells = [(128, 642, 510, 907), (532, 642, 912, 907), (128, 929, 510, 1266), (532, 929, 912, 1266)]
    active = CUES[index][2]
    names = ['월세', '생활비', '비상금', '목표']
    examples = ['월세 · 관리비', '식비 · 교통비', '갑작스러운 지출', '여행 · 이사']
    for i, box in enumerate(cells):
        selected = active == i or active == 4
        roundbox(d, box, MINT if selected else '#f1f1e8', 19, GREEN if selected else None, 4)
        x, y = box[:2]
        text(d, (x+25, y+21), f'0{i+1}', 29, GREEN)
        text(d, (x+24, y+70), names[i], 61, GREEN if selected else INK, True)
        if selected:
            text(d, (x+24, y+157), examples[i], 31)
            d.line((x+26, y+218, x+335, y+218), fill=GREEN, width=3)
        else:
            d.line((x+26, y+207, x+335, y+207), fill='#cad1c3', width=3)
    if active == -1:
        label = '월급날에 꺼내 보는 메모' if index == 0 else '네 칸이면 시작할 수 있어요'
    elif active == 4:
        label = '금액과 비율은 내 상황에 맞게'
    else:
        label = ['먼저, 빠져나갈 돈', '매일 쓰는 돈', '혹시 모를 지출', '모으고 싶은 이유'][active]
    text(d, (105, 1343), label, 39, GREEN, True)
    # 자막 안전 영역: 좌우 100px, 위 200px, 아래 320px 이상.
    roundbox(d, (86, 1460, 954, 1625), INK, 22)
    sub = CUES[index][0]
    for line_i, line in enumerate(sub.split('\n')):
        f = font(43, True); width = d.textlength(line, font=f)
        d.text(((W-width)/2, 1480+line_i*64), line, font=f, fill='#ffffff')
    text(d, (105, 1676), '한국어 합성음 · 창작 생활비 메모 예시', 26, GREEN)
    # 같은 장면 안에서 읽는 진행만 움직인다. 화면이 자막보다 먼저 넘어가지 않는다.
    d.rounded_rectangle((100, 1758, 940, 1766), radius=4, fill='#d8dfd0')
    progress = (index + min(1, elapsed/duration))/len(CUES)
    d.rounded_rectangle((100, 1758, 100+840*progress, 1766), radius=4, fill=GREEN)
    return im


def stamp(seconds):
    ms = round(seconds*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'


def film():
    target = OUT/'shorts'; target.mkdir(parents=True, exist_ok=True)
    timeline, pcm, start = [], bytearray(), 0.0
    rate = 44100
    for i, (subtitle, narration, active) in enumerate(CUES):
        path = target/'voice'/f'{i+1:02d}.wav'
        with wave.open(str(path)) as w:
            assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, rate)
            body = w.readframes(w.getnframes())
            speech = w.getnframes()/rate
        # 앞에 0.16초, 읽은 뒤 최소 0.30초 여백을 두고 프레임 수로 길이를 맞춘다.
        frames = math.ceil((speech+.46)*FPS)
        duration = frames/FPS
        before = round(.16*rate)
        after = round(duration*rate) - before - len(body)//2
        pcm.extend(b'\0\0'*before + body + b'\0\0'*after)
        timeline.append({'scene':i+1, 'start':round(start, 6), 'end':round(start+duration, 6), 'speech_start':round(start+.16, 6), 'speech_end':round(start+.16+speech, 6), 'frames':frames, 'narration':narration, 'subtitle':subtitle})
        start += duration
    with wave.open(str(target/'narration.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
    (target/'timeline.json').write_text(json.dumps(timeline, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (target/'subtitles.srt').write_text('\n\n'.join(f"{x['scene']}\n{stamp(x['speech_start'])} --> {stamp(x['end'])}\n{x['subtitle']}" for x in timeline)+'\n', encoding='utf-8')
    with tempfile.TemporaryDirectory(prefix='editorial-render-') as temp:
        raw = Path(temp)/'silent.mp4'
        cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', '-pix_fmt', 'yuv420p', str(raw)]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        try:
            for i, row in enumerate(timeline):
                duration = row['frames']/FPS
                base = video_frame(i, 0, duration)
                for frame in range(row['frames']):
                    im = base.copy()
                    d = ImageDraw.Draw(im)
                    progress = (i+frame/row['frames'])/len(CUES)
                    d.rounded_rectangle((100, 1758, 100+840*progress, 1766), radius=4, fill=GREEN)
                    p.stdin.write(im.tobytes())
                video_frame(i, duration/2, duration).save(target/f'scene-{i+1:02d}.webp', quality=86)
                print(f'장면 {i+1}/8 렌더 완료', flush=True)
        finally:
            p.stdin.close()
        if p.wait():
            raise RuntimeError('영상 렌더 실패')
        run(['-i', raw, '-i', target/'narration.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=7', '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', '-t', f'{start:.6f}', target/'payday-four-boxes.mp4'])
    video_frame(1, 0, 1).save(target/'poster.jpg', quality=90)
    (target/'script.txt').write_text('\n\n'.join(x[1] for x in CUES)+'\n', encoding='utf-8')
    run(['-i', target/'narration.wav', '-c:a', 'flac', target/'narration.flac'])
    (target/'narration.wav').unlink()
    manifest = {'title':'월급날 10분, 돈을 네 칸으로 나누기', 'duration_seconds':round(start,6), 'width':W, 'height':H, 'fps':FPS, 'voice':{'engine':'supertonic 1.3.1', 'model':'supertonic-3', 'model_revision':'724fb5abbf5502583fb520898d45929e62f02c0b', 'style':'F1', 'language':'ko', 'steps':12, 'speed':1.0, 'synthetic':True}, 'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [target/'payday-four-boxes.mp4', target/'narration.flac']}}
    (target/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'완성 견본 {start:.3f}초 · 1080×1920 · 한국어 합성음')


def webcopy():
    for site in ('site', 'site-shorts'):
        target = ROOT.parent/site/'assets'/'advanced'/'editorial'; target.mkdir(parents=True, exist_ok=True)
        for path in (OUT/'instagram').glob('*.webp'):
            shutil.copyfile(path, target/path.name)
        for name in ('payday-four-boxes.mp4', 'poster.jpg', 'subtitles.srt'):
            shutil.copyfile(OUT/'shorts'/name, target/name)
        # WebVTT is used by HTML video; burned-in captions remain visible without a track.
        srt = (target/'subtitles.srt').read_text(encoding='utf-8')
        (target/'subtitles.vtt').write_text('WEBVTT\n\n'+srt.replace(',', '.'), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--regenerate-voice', action='store_true', help='선택 설치한 supertonic으로 음성을 새로 생성(모델 없으면 다운로드)')
    parser.add_argument('--model-dir', type=Path, default=Path('/tmp/editorial-supertonic-3'))
    parser.add_argument('--cards-only', action='store_true')
    args = parser.parse_args()
    cards()
    if not args.cards_only:
        if args.regenerate_voice:
            voice(args.model_dir)
        film()
        webcopy()


if __name__ == '__main__':
    main()
