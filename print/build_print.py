"""產生列印用 HTML：QR 卡（厚紙 A4）與裝盒對照表。再用 print/to_pdf.js 轉成 PDF。"""
import segno, io, os
BASE = "https://molicatalice-cyber.github.io/Christmas-/"
HERE = os.path.dirname(os.path.abspath(__file__))
RED, GREEN, INK, CREAM, GOLD = "#a34245", "#4f7f5c", "#5a1a20", "#fbefe6", "#e9bf4f"

def qr(slug):
    q = segno.make(BASE + slug + "/", error="m")
    buf = io.BytesIO()
    q.save(buf, kind="svg", dark=INK, light=None, border=1, omitsize=True, xmldecl=False, svgns=True, nl=False)
    return buf.getvalue().decode()

# (日期, 網址, 卡片上的字)
QR_CARDS = [
    (1, "song", "十二月的背景音樂"), (4, "luck", "刮刮樂"), (7, "red", "找找看"),
    (9, "quiz", "聖誕冷知識"), (13, "tree", "來佈置聖誕樹"), (17, "listen", "三十秒"),
    (20, "catch", "接禮物"), (24, "xmas", "聖誕快樂"),
]
# 每一格放什麼
DAYS = {
    1: ("QR", "歌單"), 2: ("糖", "維生素C糖"), 3: ("糖", "GODIVA\n（12/19 到期那顆）"), 4: ("QR", "刮刮樂"),
    5: ("糖", "Hi-Chew"), 6: ("卡", "遊戲卡 A"), 7: ("QR", "找找看"), 8: ("糖", "鹽烤椰子太妃"),
    9: ("QR", "聖誕冷知識"), 10: ("糖", "金莎"), 11: ("卡", "食譜卡"), 12: ("糖", "香料太妃"),
    13: ("QR", "佈置聖誕樹"), 14: ("糖", "葡萄軟糖"), 15: ("物", "維尼吊飾"), 16: ("糖", "薑糖\n＋一顆別的糖"),
    17: ("QR", "三十秒"), 18: ("糖", "Andes 薄荷巧克力"), 19: ("卡", "遊戲卡 B"), 20: ("QR", "接禮物"),
    21: ("糖", "蘋果薑糖\n＋一顆別的糖"), 22: ("物", "蜂蠟蠟燭\n＋冬至摺卡"), 23: ("糖", "GODIVA\n（超商那顆）"),
    24: ("QR", "聖誕快樂\n＋手寫紙條"),
}
# 封面上數字的位置（正面看）
LEFT = [[2, 5, 9], [6, 8, 1], [11, 3, 7], [12, 10, 4]]
RIGHT = [[20, 18, 22], [13, 14, 19], [21, 23, 16], [17, 15, 24]]

HEAD = f"""<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><style>
@font-face {{ font-family: H; src: url("file://{HERE}/fonts/jf-openhuninn-2.1.ttf"); }}
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: H, sans-serif; color: {INK}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 210mm; height: 297mm; position: relative; page-break-after: always; overflow: hidden; }}
.ruler {{ position: absolute; bottom: 12mm; left: 55mm; width: 100mm; border-top: .3mm solid #999; border-left: .3mm solid #999; border-right: .3mm solid #999; height: 2mm; font-size: 7pt; color: #999; text-align: center; line-height: 4mm; }}
.note {{ position: absolute; top: 14mm; left: 0; right: 0; text-align: center; font-size: 9pt; color: #999; }}
"""

def qr_sheet():
    css = f"""
.grid {{ position: absolute; left: 30mm; top: 40mm; width: 150mm; display: grid; grid-template-columns: repeat(3, 50mm); grid-auto-rows: 50mm; }}
.card {{ outline: .2mm dashed #bbb; background: {CREAM}; position: relative; }}
.frame {{ position: absolute; inset: 2.2mm; border: .7mm solid var(--c); border-radius: 3.5mm; }}
.num {{ position: absolute; top: -.2mm; left: -.2mm; min-width: 9.5mm; height: 9.5mm; padding: 0 1.5mm; border-radius: 3mm 0 3mm 0; background: var(--c); color: {CREAM}; font-size: 15pt; line-height: 9.5mm; text-align: center; }}
.qr {{ position: absolute; left: 50%; top: 6.5mm; width: 27mm; height: 27mm; transform: translateX(-50%); }}
.qr svg {{ width: 100%; height: 100%; display: block; }}
.t {{ position: absolute; left: 0; right: 0; bottom: 5.2mm; text-align: center; font-size: 10.5pt; line-height: 1; letter-spacing: .08em; color: var(--c); }}
.star {{ position: absolute; top: 1.2mm; right: 2mm; font-size: 10pt; color: {GOLD}; }}
.wide {{ grid-column: span 2; }}
.wide .half {{ position: absolute; top: 0; bottom: 0; width: 50mm; padding: 5mm 4.5mm; }}
.wide .l {{ left: 0; }} .wide .r {{ left: 50mm; border-left: .2mm dotted #ccc; }}
.pray {{ font-size: 7.6pt; line-height: 1.75; text-align: center; margin: 0; }}
.r h3 {{ margin: 0 0 1mm; font-size: 12pt; color: {RED}; font-weight: normal; letter-spacing: .1em; }}
.r p {{ margin: 0; font-size: 6.6pt; line-height: 1.55; }}
.r .q {{ position: absolute; right: 3.5mm; bottom: 3.5mm; width: 19mm; height: 19mm; }}
.r .q svg {{ width: 100%; height: 100%; }}
.r .ql {{ position: absolute; left: 4.5mm; bottom: 4.5mm; width: 21mm; font-size: 6.6pt; line-height: 1.5; color: {GREEN}; }}
"""
    cards = ""
    for i, (d, slug, title) in enumerate(QR_CARDS):
        c = RED if i % 2 == 0 else GREEN
        cards += f'<div class="card" style="--c:{c}"><div class="frame"><div class="num">{d}</div><div class="star">✦</div></div><div class="qr">{qr(slug)}</div><div class="t">{title}</div></div>'
    cards += '<div class="card" style="outline:none;background:none"></div>'
    cards += f"""<div class="card wide" style="--c:{RED}">
<div class="half l"><p class="pray">願這一小盞火<br>陪最長的夜坐一會兒<br><br>願走了一整年的身體<br>今晚睡得很沉<br><br>願光一天一天回來的路上<br>我們都平安</p></div>
<div class="half r"><h3>冬至</h3><p>一年裡夜最長的一天。<br>從明天起，白天會一點一點長回來。</p>
<p style="margin-top:1.6mm;color:#8a5a5e">蜂蠟蠟燭｜第一次請點到表面整圈融化；離開前記得熄掉。</p>
<div class="ql">掃這裡<br>我唸給你聽 →</div><div class="q">{qr("candle")}</div></div></div>"""
    return HEAD + css + f"""</style></head><body><div class="page">
<div class="note">QR 卡｜厚紙 A4，請用「實際大小 / 100%」列印｜沿虛線裁切，每張 5 × 5 cm；最下面那張 10 × 5 cm，字朝內對摺</div>
<div class="grid">{cards}</div><div class="ruler">10 cm</div></div></body></html>"""

def guide():
    colors = {"QR": GREEN, "糖": RED, "卡": "#b98a1e", "物": "#6a5acd"}
    css = f"""
h1 {{ font-size: 17pt; font-weight: normal; margin: 0; text-align: center; padding-top: 13mm; }}
.sub {{ text-align: center; font-size: 9.5pt; color: #777; margin: 1.5mm 0 6mm; }}
.boxes {{ display: flex; justify-content: center; gap: 7mm; }}
.box h2 {{ font-size: 11pt; font-weight: normal; text-align: center; margin: 0 0 2mm; }}
.g {{ display: grid; grid-template-columns: repeat(3, 29mm); grid-auto-rows: 29mm; border: .5mm solid {INK}; }}
.c {{ border: .2mm solid {INK}; padding: 1.5mm; position: relative; }}
.c b {{ font-size: 19pt; font-weight: normal; color: var(--k); line-height: 1; }}
.c i {{ position: absolute; top: 1.8mm; right: 1.8mm; font-style: normal; font-size: 8pt; color: #fff; background: var(--k); border-radius: 1.5mm; padding: .3mm 1.6mm; }}
.c span {{ display: block; margin-top: 1.6mm; font-size: 8.6pt; line-height: 1.35; white-space: pre-line; }}
table {{ margin: 7mm auto 0; border-collapse: collapse; font-size: 9pt; }}
td {{ padding: .9mm 3mm; border-bottom: .2mm solid #ddd; white-space: nowrap; }} td.n {{ text-align: right; color: {RED}; }}
.cols {{ display: flex; justify-content: center; gap: 10mm; }}
"""
    def box(rows, title):
        cells = "".join(f'<div class="c" style="--k:{colors[DAYS[n][0]]}"><b>{n}</b><i>{DAYS[n][0]}</i><span>{DAYS[n][1]}</span></div>' for r in rows for n in r)
        return f'<div class="box"><h2>{title}</h2><div class="g">{cells}</div></div>'
    def page(title, sub, a, b):
        return f'<div class="page"><h1>{title}</h1><div class="sub">{sub}</div><div class="boxes">{a}{b}</div>__EXTRA__</div>'
    def tbl(ns):
        return "<table>" + "".join(f'<tr><td class="n">{n}</td><td>{DAYS[n][0]}</td><td>{DAYS[n][1].replace(chr(10), " ")}</td></tr>' for n in ns) + "</table>"
    lst = f'<div class="cols">{tbl(range(1, 13))}{tbl(range(13, 25))}</div>'
    front = page("裝盒對照表｜從正面看", "跟封面圖同一個方向。從正面（貼封面那一面）放東西時看這張。", box(LEFT, "左盒"), box(RIGHT, "右盒")).replace("__EXTRA__", lst)
    mir = lambda rows: [r[::-1] for r in rows]
    back = page("裝盒對照表｜從背面看（左右相反）", "把盒子翻到背面放東西時看這張。位置已經幫你左右鏡射好了，照著放就對。", box(mir(RIGHT), "右盒（翻過來後在左手邊）"), box(mir(LEFT), "左盒（翻過來後在右手邊）")).replace("__EXTRA__", "")
    return HEAD + css + "</style></head><body>" + front + back + "</body></html>"

os.makedirs(f"{HERE}/out", exist_ok=True)
open(f"{HERE}/out/qr_cards.html", "w", encoding="utf-8").write(qr_sheet())
open(f"{HERE}/out/packing_guide.html", "w", encoding="utf-8").write(guide())
