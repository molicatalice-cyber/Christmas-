"""把封面圖切成左右兩半，各自置中放在 A4（底色取圖片邊緣色）。每半 18 x 24 cm。"""
import sys
from statistics import median
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

src = Image.open(sys.argv[1]).convert("RGB")
W, H = src.size
halves = {"left": src.crop((0, 0, W // 2, H)), "right": src.crop((W // 2, 0, W, H))}
IMG_W, IMG_H = 180 * mm, 240 * mm
PW, PH = A4

def edge_color(im):
    w, h = im.size
    px = [im.getpixel((x, y)) for x in range(0, w, 7) for y in (2, h - 3)]
    px += [im.getpixel((x, y)) for y in range(0, h, 7) for x in (2, w - 3)]
    px = [p for p in px if p[0] > p[1] + 60]          # 只取紅色系，排除綠色角落與插圖
    return tuple(int(median(c)) for c in zip(*px))

for name, im in halves.items():
    bg = edge_color(im)
    print(name, im.size, bg)
    # PDF
    c = canvas.Canvas(f"print/cover/cover_{name}_A4.pdf", pagesize=A4)
    c.setFillColorRGB(*[v / 255 for v in bg]); c.rect(0, 0, PW, PH, stroke=0, fill=1)
    x, y = (PW - IMG_W) / 2, (PH - IMG_H) / 2
    c.drawImage(ImageReader(im), x, y, IMG_W, IMG_H)
    # 校正尺：10 cm，印出來量一下就知道有沒有被縮放
    light = [min(1, v / 255 + 0.18) for v in bg]
    c.setStrokeColorRGB(*light); c.setFillColorRGB(*light); c.setLineWidth(0.5)
    rx, ry = (PW - 100 * mm) / 2, 13 * mm
    c.line(rx, ry, rx + 100 * mm, ry)
    for t in (0, 100): c.line(rx + t * mm, ry - 1.5 * mm, rx + t * mm, ry + 1.5 * mm)
    c.setFont("Helvetica", 6); c.drawCentredString(PW / 2, ry + 1.5 * mm, "10 cm")
    c.save()
    # JPG 300dpi 備用
    page = Image.new("RGB", (2480, 3508), bg)
    iw, ih = round(180 / 25.4 * 300), round(240 / 25.4 * 300)
    page.paste(im.resize((iw, ih), Image.LANCZOS), ((2480 - iw) // 2, (3508 - ih) // 2))
    page.save(f"print/cover/cover_{name}_A4.jpg", quality=95, dpi=(300, 300))
    page.resize((496, 702)).save(f"/tmp/claude-0/-home-user-Christmas-/69fc4b52-9197-5d60-9cb7-56f52d456d4b/scratchpad/prev_{name}.png")
