"""대표 해설의 자체 도식 3장. 키트 루트에서 실행하며 기존 렌더러에 넘긴다."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
INK, BG = '#263344', '#faf6ed'
COLORS = ['#e6a289', '#b6cbb5', '#afc6dc', '#e5c77a']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('input/money-scenes'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    def font(size, weight=600):
        face = ImageFont.truetype(str(ROOT / 'assets/fonts/NotoSansKR.ttf'), size)
        face.set_variation_by_axes([weight])
        return face
    for scene in range(3):
        im = Image.new('RGB', (1080, 1920), BG)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((80, 150, 920, 215), 28, fill='#eae4d7')
        d.text((112, 159), '자취생 10분 생존법 · 가상 채널', font=font(32), fill=INK)
        headlines = [('월급날,','돈을 네 칸으로'), ('나갈 돈과','모을 돈을 나눠요'), ('새 통장 대신','내 메모부터')]
        for j, line in enumerate(headlines[scene]):
            d.text((85, 285 + 114*j), line, font=font(82, 750), fill=INK)
        d.text((90, 545), ['돈의 용도를 먼저 적어 봐요', '금액은 내 상황을 보고 정해요', '오늘 쓸 곳만 적어도 시작이에요'][scene], font=font(37), fill='#586270')
        names = ['월세', '생활비', '비상금', '목표']
        hints = ['나갈 돈', '평소 쓸 돈', '예상 못 한 지출', '모으고 싶은 것']
        for i, name in enumerate(names):
            x, y = 90 + (i % 2)*430, 675 + (i // 2)*320
            d.rounded_rectangle((x, y+10, x+390, y+290), 26, fill='#e8e1d3')
            d.rounded_rectangle((x, y, x+390, y+280), 26, fill=COLORS[i], outline=INK, width=2)
            # 작은 집, 장보기 가방, 비상 파우치, 목표 깃발: 자체 도형.
            cx, cy = x+195, y+92
            if i == 0:
                d.polygon([(cx-48,cy-8),(cx,cy-50),(cx+48,cy-8)], fill=INK)
                d.rectangle((cx-36,cy-8,cx+36,cy+35), fill=INK)
                d.rectangle((cx-9,cy+7,cx+9,cy+35), fill=BG)
            elif i == 1:
                d.rounded_rectangle((cx-42,cy-16,cx+42,cy+39),10, fill=INK)
                d.arc((cx-21,cy-47,cx+21,cy+4),180,360,fill=INK,width=7)
            elif i == 2:
                d.rounded_rectangle((cx-48,cy-32,cx+48,cy+34),14,fill=INK)
                d.line((cx-27,cy-12,cx+27,cy-12),fill=BG,width=5)
                d.ellipse((cx+20,cy-17,cx+30,cy-7),fill=BG)
            else:
                d.line((cx-27,cy-45,cx-27,cy+38),fill=INK,width=7)
                d.polygon([(cx-23,cy-43),(cx+46,cy-29),(cx-23,cy-5)],fill=INK)
            d.text((x+34,y+151), name, font=font(54,750), fill=INK)
            d.text((x+34,y+221), hints[i], font=font(29), fill=INK)
        d.line((90,1585,900,1585),fill='#d4ccbd',width=2)
        d.text((90,1630),'금액·비율·절약 효과를 정한 예가 아닙니다',font=font(28,400),fill='#586270')
        d.text((90,1680),'네 칸은 설명용 분류 · 직접 만든 메모 도식',font=font(28,400),fill='#586270')
        d.text((90,1770),f'{scene+1:02d} / 03',font=font(28),fill=INK)
        im.save(args.output / f'{scene+1:02d}.png')
    print(f'장면 도식 3장 생성 완료: {args.output}')


if __name__ == '__main__':
    main()
