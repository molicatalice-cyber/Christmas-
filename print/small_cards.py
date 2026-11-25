"""三張對摺小卡（迷宮、找字、食譜）＋一張蠟燭說明，9.5 x 9.5 cm，一張 A4 是一盒的份量。"""
import random
RED, GREEN, INK = "#a34245", "#4f7f5c", "#5a1a20"

def maze_svg(cols=12, rows=11, cell=6.2, seed=24):
    rnd = random.Random(seed)
    right = [[True] * cols for _ in range(rows)]; down = [[True] * cols for _ in range(rows)]
    seen = {(0, 0)}; stack = [(0, 0)]
    while stack:
        r, c = stack[-1]
        nb = [(r + dr, c + dc) for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)) if 0 <= r + dr < rows and 0 <= c + dc < cols and (r + dr, c + dc) not in seen]
        if not nb: stack.pop(); continue
        nr, nc = rnd.choice(nb)
        if nr == r: right[r][min(c, nc)] = False
        else: down[min(r, nr)][c] = False
        seen.add((nr, nc)); stack.append((nr, nc))
    assert len(seen) == rows * cols          # 每一格都連通，所以一定有解
    W, H = cols * cell, rows * cell; L = [f'M0,0H{W}V{H}H0Z']
    for r in range(rows):
        for c in range(cols):
            if c < cols - 1 and right[r][c]: L.append(f'M{(c+1)*cell:.2f},{r*cell:.2f}v{cell}')
            if r < rows - 1 and down[r][c]: L.append(f'M{c*cell:.2f},{(r+1)*cell:.2f}h{cell}')
    fs = cell * .72
    return (f'<svg viewBox="-0.5 -0.5 {W+1} {H+1}" style="width:{W+1}mm;height:{H+1}mm"><path d="{"".join(L)}" fill="none" stroke="{INK}" stroke-width=".45" stroke-linecap="round"/>'
            f'<text x="{cell/2}" y="{cell*.76}" font-size="{fs}" text-anchor="middle">🦌</text><text x="{W-cell/2}" y="{H-cell*.24}" font-size="{fs}" text-anchor="middle">🛷</text></svg>')

WORDS = ["聖誕老人", "薑餅人", "聖誕樹", "麋鹿", "雪橇", "襪子", "煙囪", "禮物", "鈴鐺", "高鐵", "企鵝"]
DIRS = [(0, 1), (1, 0), (1, 1)]
def count(g, w):
    n = len(g); k = 0
    for r in range(n):
        for c in range(n):
            for dr, dc in DIRS:
                er, ec = r + dr * (len(w) - 1), c + dc * (len(w) - 1)
                if er < n and ec < n and all(g[r + dr * i][c + dc * i] == ch for i, ch in enumerate(w)): k += 1
    return k
def wordsearch(n=9, seed=7):
    pool = sorted(set("".join(WORDS)))
    for attempt in range(seed, seed + 500):
        rnd = random.Random(attempt); g = [[None] * n for _ in range(n)]; ok = True
        for w in WORDS:
            for _ in range(300):
                dr, dc = rnd.choice(DIRS); r = rnd.randrange(n - dr * (len(w) - 1)); c = rnd.randrange(n - dc * (len(w) - 1))
                if all(g[r + dr * i][c + dc * i] in (None, ch) for i, ch in enumerate(w)):
                    for i, ch in enumerate(w): g[r + dr * i][c + dc * i] = ch
                    break
            else: ok = False; break
        if not ok: continue
        for r in range(n):
            for c in range(n):
                if g[r][c] is None: g[r][c] = rnd.choice(pool)
        if all(count(g, w) == 1 for w in WORDS): return g      # 每個詞剛好出現一次
    raise RuntimeError("word search failed")

def small_cards(HEAD):
    g = wordsearch()
    grid = "".join(f"<span>{ch}</span>" for row in g for ch in row)
    css = f"""
.grid {{ position: absolute; left: 10mm; top: 48.5mm; display: grid; grid-template-columns: repeat(2, 95mm); grid-auto-rows: 95mm; }}
.card {{ outline: .2mm dashed #bbb; position: relative; padding: 7mm 7mm 0; text-align: center; }}
.card::before, .card::after {{ content: ""; position: absolute; background: #ccc; }}
.card::before {{ left: 50%; top: 0; width: .2mm; height: 2mm; box-shadow: 0 93mm 0 #ccc; }}
.card::after {{ top: 50%; left: 0; height: .2mm; width: 2mm; box-shadow: 93mm 0 0 #ccc; }}
h2 {{ margin: 0; font-size: 14pt; font-weight: normal; color: {RED}; letter-spacing: .12em; }}
.s {{ margin: 1mm 0 2.5mm; font-size: 7.8pt; color: #6b4a4d; line-height: 1.5; }}
.ws {{ display: inline-grid; grid-template-columns: repeat(9, 6.2mm); grid-auto-rows: 6.2mm; border: .4mm solid {GREEN}; border-radius: 2mm; padding: .8mm; }}
.ws span {{ font-size: 11.5pt; line-height: 6.2mm; }}
.wl {{ margin-top: 2mm; font-size: 7.6pt; color: {GREEN}; line-height: 1.6; }}
.rc {{ text-align: left; font-size: 8.6pt; line-height: 1.6; }}
.rc h3 {{ margin: 2.2mm 0 .6mm; font-size: 9pt; font-weight: normal; color: {GREEN}; letter-spacing: .1em; }}
.rc p {{ margin: 0; }} .rc .dim {{ color: #8a6a6d; font-size: 7.8pt; }}
"""
    maze = f'<div class="card"><h2>麋鹿又迷路了</h2><p class="s">請帶牠走到雪橇那裡。聖誕老人已經在看錶了。</p>{maze_svg()}</div>'
    ws = f'<div class="card"><h2>找字</h2><p class="s">裡面藏了 11 個詞，橫的、直的、斜的都有。<br>企鵝不該在這裡，但牠在。</p><div class="ws">{grid}</div><div class="wl">{"　".join(WORDS[:6])}<br>{"　".join(WORDS[6:])}</div></div>'
    recipe = """<div class="card"><h2>香料熱蘋果汁</h2><p class="s">一杯的份量，十分鐘。</p><div class="rc">
<h3>材料</h3><p>蘋果汁 300 ml（超商那種就可以）<br>肉桂棒 1 支，或肉桂粉撒兩下<br>薑 2 片<br>柳橙或橘子 2 片</p>
<p class="dim">肉桂棒在超市的香料區，長得像樹枝的那個。</p>
<h3>作法</h3><p>全部丟進小鍋，小火煮到邊邊冒小泡泡，<br>不用滾。關火放三分鐘，倒出來喝。</p>
<h3>想換口味</h3><p>蘋果汁換成紅酒，加一匙糖，就是熱紅酒。<br>不喝酒的話，換葡萄汁也很像一回事。</p></div></div>"""
    candle = """<div class="card"><h2>蜂蠟蠟燭的小說明</h2><p class="s">&nbsp;</p><div class="rc" style="margin-top:4mm">
<p>這是一顆蜂蠟做的小蠟燭。</p>
<h3>第一次點</h3><p>請讓表面整圈都融化了再熄。<br>不然它會在中間凹一個洞，之後越燒越深。</p>
<h3>點的時候</h3><p>下面墊個不怕燙的小碟子。<br>人要離開房間的時候，先把它熄掉。</p>
<h3>同一格的 QR 卡</h3><p>點起來之後再掃，剛剛好。</p></div></div>"""
    return HEAD + css + f"""</style></head><body><div class="page">
<div class="note">小卡｜普通紙 A4，請用「實際大小 / 100%」列印｜沿虛線裁成 9.5 × 9.5 cm，字朝內對摺再對摺（邊上的小短線是摺線位置）<br>右下那張蠟燭說明可放可不放，要放就跟蠟燭同一格</div>
<div class="grid">{maze}{ws}{recipe}{candle}</div><div class="ruler">10 cm</div></div></body></html>"""
