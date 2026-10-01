from PIL import Image, ImageDraw

BOYUT = 128
MAVI = (26, 115, 232)


def ciz() -> Image.Image:
    img = Image.new("RGB", (BOYUT, BOYUT), MAVI)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((8, 8, BOYUT - 8, BOYUT - 8), radius=24, fill=MAVI)
    draw.line((36, 66, 56, 86, 92, 44), fill="white", width=12, joint="curve")
    return img


if __name__ == "__main__":
    ciz().save("app.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)])
