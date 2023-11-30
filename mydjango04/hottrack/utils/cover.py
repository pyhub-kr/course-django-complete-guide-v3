# melon/utils/cover.py

from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont, __version__ as pil_version


# PIL 버전 10부터 변경되는 동작이 있어서, 버전을 체크해줍니다.
PIL_VERSION = tuple(map(int, pil_version.split(".")))


def make_cover_image(cover_url: str, text: str, canvas_size: int = 256) -> Image:
    canvas = Image.new("RGB", (canvas_size, canvas_size), "white")
    draw = ImageDraw.Draw(canvas)

    res = requests.get(cover_url)
    if res.ok:
        cover_image = Image.open(BytesIO(res.content))
        cover_image.thumbnail((canvas_size, canvas_size))
        canvas.paste(cover_image, (0, 0))
    else:
        # 이미지 다운로드에 실패했을 경우, X 표시를 그립니다.
        draw.line((0, 0, canvas_size, canvas_size), fill="red")
        draw.line((0, canvas_size, canvas_size, 0), fill="blue")

    # 사선 스트라이프 패턴 그리기 (회색, 선 굵기 3)
    for i in range(-canvas_size, canvas_size, 10):
        draw.line([(i, 0), (i + canvas_size, canvas_size)], fill="#F0F0F0", width=2)

    # 맑은고딕 (윈도우), 애플고딕(맥) 폰트 사용하기
    trying_font_names = ["malgunsl.ttf", "AppleGothic.ttf"]
    for font_name in trying_font_names:
        try:
            font = ImageFont.truetype(font=font_name, size=32)
            break
        except IOError:
            continue
    else:
        font = ImageFont.load_default()

    # 텍스트를 그릴 시작 좌표 x, y 좌표 계산하기
    if PIL_VERSION >= (10,):
        x0 = int(canvas.width / 2)
        y0 = int(canvas.height / 2)
        bb_l, bb_t, bb_r, bb_b = draw.textbbox(xy=(0, 0), text=text, font=font)
        x = x0 - (bb_r - bb_l) / 2
        y = y0 - (bb_b - bb_t) / 2
    else:
        text_width, text_height = draw.textsize(text=text, font=font)
        x = (canvas.width - text_width) / 2
        y = (canvas.height - text_height) / 2

    # 지정 좌표, 폰트, 색상으로 텍스트 그리기
    draw.text(xy=(x, y), text=text, fill="black", font=font)

    return canvas
