from fig_all import *   # 提供 plt, np, PF(中文字型), fig 裝飾器, new_ax(w,h,equal), save(f, qid), txt(ax,x,y,s,...), dot, circle, arc, INK/RED/BLUE/GREY 顏色
# 英語看圖題 21100–21139(eng_pics)。
# 21100–21129:聽力「辨識句意」,每題 4 張選項圖 @fig(題號*10+選項索引)。
# 21130–21139:看圖閱讀,題幹圖 @fig(題號)。
# 直接執行本檔(PYTHONPATH 指向 tools/)會輸出 out/eng_pics.json。
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, Circle, Ellipse
import json, os

YEL, ORG, GRN, BRN = '#f2b600', '#e8862a', '#3a9a4a', '#a86b32'
LBLUE, LGREY, CREAM = '#dfe9f5', '#e4e4e4', '#fff4cc'


# ───────────────────────── 共用小圖元 ─────────────────────────
def card():
    f, ax = new_ax(3.2, 2.4)
    ax.set_xlim(0, 4); ax.set_ylim(0, 3)
    ax.add_patch(FancyBboxPatch((0.05, 0.05), 3.9, 2.9, boxstyle='round,pad=0,rounding_size=0.15',
                                fc='white', ec=GREY, lw=1.2))
    return f, ax


def line(ax, xs, ys, color=INK, lw=2, **kw):
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle='round', **kw)


def clock(ax, h, m, cx=2, cy=1.5, r=1.22):
    ax.add_patch(Circle((cx, cy), r, fc='white', ec=INK, lw=2.6))
    for i in range(60):
        a = np.radians(90 - 6 * i); big = i % 5 == 0
        r0 = r * (0.85 if big else 0.92)
        line(ax, [cx + r0 * np.cos(a), cx + 0.96 * r * np.cos(a)], [cy + r0 * np.sin(a), cy + 0.96 * r * np.sin(a)],
             lw=1.8 if big else 0.8)
    for n in range(1, 13):
        a = np.radians(90 - 30 * n)
        txt(ax, cx + 0.68 * r * np.cos(a), cy + 0.68 * r * np.sin(a), str(n), fs=11, ha='center', va='center', zorder=6,
            bbox=dict(boxstyle='square,pad=0.05', fc='white', ec='none', alpha=0.75))
    ah = np.radians(90 - 30 * ((h % 12) + m / 60)); am = np.radians(90 - 6 * m)
    line(ax, [cx, cx + 0.45 * r * np.cos(ah)], [cy, cy + 0.45 * r * np.sin(ah)], lw=5)
    line(ax, [cx, cx + 0.8 * r * np.cos(am)], [cy, cy + 0.8 * r * np.sin(am)], color=BLUE, lw=3)
    ax.add_patch(Circle((cx, cy), 0.06, fc=INK, ec=INK, zorder=5))


def small_clock(ax, cx, cy, r=0.26):
    ax.add_patch(Circle((cx, cy), r, fc='white', ec=INK, lw=2, zorder=3))
    for k in range(12):
        a = np.radians(30 * k)
        line(ax, [cx + 0.78 * r * np.cos(a), cx + 0.92 * r * np.cos(a)], [cy + 0.78 * r * np.sin(a), cy + 0.92 * r * np.sin(a)], lw=1, zorder=4)
    line(ax, [cx, cx], [cy, cy + 0.7 * r], lw=1.6, zorder=4)
    line(ax, [cx, cx + 0.5 * r], [cy, cy], lw=2.2, zorder=4)


def sun(ax, cx, cy, s=1.0):
    ax.add_patch(Circle((cx, cy), 0.3 * s, fc=YEL, ec=ORG, lw=1.8, zorder=3))
    for k in range(8):
        a = k * np.pi / 4
        line(ax, [cx + 0.4 * s * np.cos(a), cx + 0.56 * s * np.cos(a)], [cy + 0.4 * s * np.sin(a), cy + 0.56 * s * np.sin(a)],
             color=ORG, lw=2.6)


def cloud(ax, cx, cy, s=1.0, fc='#dfe3e8'):
    cs = [(-0.36, -0.06, 0.26), (-0.02, 0.1, 0.34), (0.34, -0.04, 0.27), (0.0, -0.14, 0.26)]
    for dx, dy, r in cs:
        ax.add_patch(Circle((cx + dx * s, cy + dy * s), r * s, fc='none', ec=INK, lw=3.2, zorder=2))
    for dx, dy, r in cs:
        ax.add_patch(Circle((cx + dx * s, cy + dy * s), r * s, fc=fc, ec='none', zorder=2.5))


def flake(ax, x, y, r):
    for k in range(3):
        a = np.radians(90 + 60 * k)
        line(ax, [x - r * np.cos(a), x + r * np.cos(a)], [y - r * np.sin(a), y + r * np.sin(a)], color=BLUE, lw=2, zorder=3)


def weather(ax, kind, cx, cy, s=1.0):
    if kind == 'sun':
        sun(ax, cx, cy, s)
    elif kind == 'cloud':
        cloud(ax, cx, cy, s)
    elif kind == 'rain':
        cloud(ax, cx, cy + 0.2 * s, s)
        for dx in (-0.32, 0.0, 0.32):
            line(ax, [cx + dx * s, cx + (dx - 0.1) * s], [cy - 0.25 * s, cy - 0.55 * s], color=BLUE, lw=2.6)
    elif kind == 'snow':
        cloud(ax, cx, cy + 0.2 * s, s)
        for dx, dy in ((-0.34, -0.36), (0.0, -0.5), (0.34, -0.36)):
            flake(ax, cx + dx * s, cy + dy * s, 0.11 * s)


def tag(ax, cx, cy, text, w=1.5, h=0.7, fs=18):
    x0, x1, y0, y1, p = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2, 0.28
    ax.add_patch(Polygon([(x0, cy), (x0 + p, y1), (x1, y1), (x1, y0), (x0 + p, y0)], closed=True, fc=CREAM, ec=INK, lw=2, zorder=3))
    ax.add_patch(Circle((x0 + p * 0.7, cy), 0.055, fc='white', ec=INK, lw=1.4, zorder=4))
    txt(ax, cx + p / 2, cy, text, fs=fs, ha='center', va='center', zorder=5)


def tshirt(ax, cx, cy, s=1.0):
    pts = [(-0.25, 0.55), (-0.62, 0.42), (-0.88, 0.1), (-0.66, -0.06), (-0.45, 0.1), (-0.45, -0.6), (0.45, -0.6),
           (0.45, 0.1), (0.66, -0.06), (0.88, 0.1), (0.62, 0.42), (0.25, 0.55), (0.0, 0.38)]
    ax.add_patch(Polygon([(cx + x * s, cy + y * s) for x, y in pts], closed=True, fc=LBLUE, ec=INK, lw=2))


def pen(ax, cx, cy, s=1.0):
    ax.add_patch(Rectangle((cx - 0.75 * s, cy - 0.08 * s), 1.25 * s, 0.16 * s, fc=BLUE, ec=INK, lw=1.6))
    ax.add_patch(Polygon([(cx + 0.5 * s, cy - 0.08 * s), (cx + 0.5 * s, cy + 0.08 * s), (cx + 0.75 * s, cy)], closed=True, fc='white', ec=INK, lw=1.6))
    line(ax, [cx - 0.6 * s, cx - 0.2 * s], [cy + 0.13 * s, cy + 0.13 * s], lw=2)   # 筆夾


def notebook(ax, cx, cy, s=1.0):
    w, h = 0.8 * s, 1.0 * s
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fc='#cfe8d4', ec=INK, lw=1.8))
    for k in range(5):
        y = cy - h / 2 + (k + 0.6) * h / 5.2
        ax.add_patch(Circle((cx - w / 2, y), 0.045 * s, fc='white', ec=INK, lw=1.2, zorder=3))
    for k in range(3):
        y = cy + 0.25 * s - k * 0.2 * s
        line(ax, [cx - w / 2 + 0.15 * s, cx + w / 2 - 0.12 * s], [y, y], color=GREY, lw=1.2)


def floor(ax, y=0.35):
    line(ax, [0.2, 3.8], [y, y], color=GREY, lw=1.6)


def table(ax, x0, x1, top, y0=0.35):
    ax.add_patch(Rectangle((x0, top - 0.1), x1 - x0, 0.1, fc=BRN, ec=INK, lw=1.6))
    for x in (x0 + 0.1, x1 - 0.18):
        ax.add_patch(Rectangle((x, y0), 0.08, top - 0.1 - y0, fc=BRN, ec=INK, lw=1.4))


def chair(ax, x0, x1, seat, back_top, y0=0.35):
    ax.add_patch(Rectangle((x0, seat - 0.08), x1 - x0, 0.08, fc=BRN, ec=INK, lw=1.6))
    ax.add_patch(Rectangle((x1 - 0.08, seat), 0.08, back_top - seat, fc=BRN, ec=INK, lw=1.4))
    for x in (x0, x1 - 0.08):
        ax.add_patch(Rectangle((x, y0), 0.08, seat - 0.08 - y0, fc=BRN, ec=INK, lw=1.4))


def ball(ax, x, y, r=0.2):
    ax.add_patch(Circle((x, y), r, fc=RED, ec=INK, lw=1.6, zorder=4))
    arc(ax, x, y, r * 0.65, 110, 200, color='white', lw=1.6)


def box(ax, x0, y0, w, h, alpha=1.0):
    ax.add_patch(Rectangle((x0, y0), w, h, fc='#e9cfa6', ec=INK, lw=2, zorder=2, alpha=alpha))
    line(ax, [x0 + 0.12, x0 + w - 0.12], [y0 + h - 0.12, y0 + h - 0.12], color=BRN, lw=1.2, zorder=2)


def flat_book(ax, cx, y0, w=0.9, h=0.24):
    ax.add_patch(Rectangle((cx - w / 2, y0), w, h, fc=BLUE, ec=INK, lw=1.6, zorder=3))
    line(ax, [cx - w / 2 + 0.06, cx + w / 2 - 0.06], [y0 + h * 0.45, y0 + h * 0.45], color='white', lw=1.2, zorder=4)


def cup(ax, cx, y0, h=0.5):
    w0, w1 = 0.3, 0.38
    ax.add_patch(Polygon([(cx - w0 / 2, y0), (cx + w0 / 2, y0), (cx + w1 / 2, y0 + h), (cx - w1 / 2, y0 + h)], closed=True,
                         fc='#f6d2d0', ec=INK, lw=1.8, zorder=3))
    ax.add_patch(Ellipse((cx + w1 / 2 + 0.03, y0 + h * 0.55), 0.18, 0.26, fc='none', ec=INK, lw=1.8, zorder=2))


def upright_book(ax, cx, y0, w=0.32, h=0.75, fc=BLUE):
    ax.add_patch(Rectangle((cx - w / 2, y0), w, h, fc=fc, ec=INK, lw=1.6, zorder=3))
    for dy in (0.15, h - 0.15):
        line(ax, [cx - w / 2 + 0.05, cx + w / 2 - 0.05], [y0 + dy, y0 + dy], color='white', lw=1.2, zorder=4)


def lamp(ax, cx, y0):
    ax.add_patch(Ellipse((cx, y0 + 0.04), 0.5, 0.1, fc=INK, ec=INK, zorder=3))
    line(ax, [cx, cx], [y0 + 0.05, y0 + 0.85], lw=2.4)
    ax.add_patch(Polygon([(cx - 0.2, y0 + 1.15), (cx + 0.2, y0 + 1.15), (cx + 0.35, y0 + 0.8), (cx - 0.35, y0 + 0.8)], closed=True,
                         fc=YEL, ec=INK, lw=1.8, zorder=3))


def pencil(ax, cx, y0, h=1.6, w=0.2):
    ax.add_patch(Rectangle((cx - w / 2, y0 + 0.12), w, h - 0.42, fc=YEL, ec=INK, lw=1.4))
    ax.add_patch(Rectangle((cx - w / 2, y0), w, 0.12, fc='#f3a6b8', ec=INK, lw=1.4))
    top = y0 + h - 0.3
    ax.add_patch(Polygon([(cx - w / 2, top), (cx + w / 2, top), (cx, top + 0.3)], closed=True, fc='#f3dcb5', ec=INK, lw=1.4))
    ax.add_patch(Polygon([(cx - w / 6, top + 0.2), (cx + w / 6, top + 0.2), (cx, top + 0.3)], closed=True, fc=INK, ec=INK, lw=1))


def carton(ax, x0, y0, cols, rows=2, eggs=None):
    eggs = cols * rows if eggs is None else eggs
    c = 0.34
    ax.add_patch(FancyBboxPatch((x0, y0), cols * c + 0.08, rows * c + 0.08, boxstyle='round,pad=0,rounding_size=0.06',
                                fc='#d9d2c5', ec=INK, lw=1.8))
    k = 0
    for r in range(rows):
        for q in range(cols):
            ax.add_patch(Ellipse((x0 + 0.04 + c * (q + 0.5), y0 + 0.04 + c * (r + 0.5)), 0.26, 0.3,
                                 fc='#fffaf0', ec=INK, lw=1.4, zorder=3))
            k += 1


def door(ax, x0, x1, top, y0=0.35):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, top - y0, fc='#e3c9a0', ec=INK, lw=2))
    ax.add_patch(Circle((x1 - 0.13, (y0 + top) / 2), 0.045, fc=INK, ec=INK))


def window(ax, x0, x1, y0, y1):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=LBLUE, ec=INK, lw=2))
    line(ax, [(x0 + x1) / 2] * 2, [y0, y1], lw=1.6)
    line(ax, [x0, x1], [(y0 + y1) / 2] * 2, lw=1.6)


def road(ax, xs, ys):
    ax.plot(xs, ys, color='#d6d6d6', lw=16, solid_capstyle='butt', zorder=1)


def path_arrow(ax, pts):
    xs, ys = zip(*pts)
    ax.plot(xs[:-1], ys[:-1], color=RED, lw=3, solid_joinstyle='round', zorder=3)
    ax.annotate('', xy=pts[-1], xytext=pts[-2], arrowprops=dict(arrowstyle='-|>,head_length=0.6,head_width=0.35', color=RED, lw=3), zorder=3)


def start_dot(ax, x, y):
    ax.add_patch(Circle((x, y), 0.09, fc=BLUE, ec=BLUE, zorder=4))
    txt(ax, x + 0.18, y - 0.02, 'START', fs=11, color=BLUE, va='center')


def traffic_light(ax, x, y):
    ax.add_patch(Rectangle((x - 0.09, y - 0.22), 0.18, 0.44, fc=INK, ec=INK, zorder=4))
    for dy, c in ((0.13, RED), (0, YEL), (-0.13, GRN)):
        ax.add_patch(Circle((x, y + dy), 0.05, fc=c, ec='none', zorder=5))
    line(ax, [x, x], [y - 0.22, y - 0.45], lw=2)


def shop(ax, cx, cy):
    ax.add_patch(Rectangle((cx - 0.42, cy - 0.28), 0.84, 0.42, fc='#fde3e1', ec=INK, lw=1.8, zorder=3))
    ax.add_patch(Polygon([(cx - 0.5, cy + 0.14), (cx + 0.5, cy + 0.14), (cx + 0.38, cy + 0.36), (cx - 0.38, cy + 0.36)], closed=True,
                         fc=RED, ec=INK, lw=1.6, zorder=3))
    txt(ax, cx, cy - 0.07, 'SHOP', fs=11, ha='center', va='center', zorder=4)


def tree(ax, cx, cy):
    ax.add_patch(Rectangle((cx - 0.05, cy - 0.3), 0.1, 0.25, fc=BRN, ec=INK, lw=1.2))
    ax.add_patch(Circle((cx, cy + 0.05), 0.22, fc='#8fcf8f', ec=INK, lw=1.6))


def school(ax, cx, cy, k=1.0):
    _school(ax, cx, cy, k)


def _school(ax, cx, cy, k):
    P = lambda x, y: (cx + x * k, cy + y * k)
    ax.add_patch(Rectangle(P(-0.3, -0.3), 0.6 * k, 0.38 * k, fc='#f1e3c3', ec=INK, lw=1.6, zorder=3))
    ax.add_patch(Polygon([P(-0.36, 0.08), P(0.36, 0.08), P(0, 0.28)], closed=True, fc=BRN, ec=INK, lw=1.4, zorder=3))
    line(ax, [cx, cx], [cy + 0.28 * k, cy + 0.5 * k], lw=1.4)
    ax.add_patch(Polygon([P(0, 0.5), P(0.18, 0.44), P(0, 0.38)], closed=True, fc=RED, ec='none', zorder=3))
    ax.add_patch(Rectangle(P(-0.07, -0.3), 0.14 * k, 0.2 * k, fc=BRN, ec=INK, lw=1, zorder=4))


def compass_n(ax, x, y):
    ax.annotate('', xy=(x, y + 0.3), xytext=(x, y - 0.25), arrowprops=dict(arrowstyle='-|>', color=INK, lw=2))
    txt(ax, x, y + 0.42, 'N', fs=13, ha='center', va='center')


def thermo(ax, cx, val, lo, hi, major, minor, y0=0.62, y1=2.45):
    tw = 0.2
    ax.add_patch(FancyBboxPatch((cx - tw / 2, y0 - 0.1), tw, y1 - y0 + 0.28, boxstyle='round,pad=0,rounding_size=0.1',
                                fc='white', ec=INK, lw=1.8, zorder=2))
    ax.add_patch(Circle((cx, y0 - 0.2), 0.19, fc=RED, ec=INK, lw=1.8, zorder=3))
    yv = y0 + (val - lo) / (hi - lo) * (y1 - y0)
    ax.add_patch(Rectangle((cx - 0.05, y0 - 0.2), 0.1, yv - y0 + 0.2, fc=RED, ec='none', zorder=4))
    for v in range(lo, hi + 1, minor):
        y = y0 + (v - lo) / (hi - lo) * (y1 - y0); big = (v - lo) % major == 0
        line(ax, [cx + tw / 2 + 0.02, cx + tw / 2 + (0.2 if big else 0.11)], [y, y], lw=1.4 if big else 0.9)
        if big:
            txt(ax, cx + tw / 2 + 0.27, y, str(v), fs=11, va='center')
    txt(ax, cx - 0.32, y1 + 0.05, '°C', fs=11, ha='center', va='center')


def bus(ax, cx, cy):
    ax.add_patch(FancyBboxPatch((cx - 1.3, cy - 0.35), 2.6, 1.0, boxstyle='round,pad=0,rounding_size=0.15', fc=YEL, ec=INK, lw=2))
    for k in range(5):
        ax.add_patch(Rectangle((cx - 1.15 + k * 0.42, cy + 0.15), 0.32, 0.32, fc=LBLUE, ec=INK, lw=1.4))
    ax.add_patch(Rectangle((cx + 0.95, cy - 0.22), 0.25, 0.69, fc=LBLUE, ec=INK, lw=1.4))
    for x in (cx - 0.75, cx + 0.6):
        ax.add_patch(Circle((x, cy - 0.38), 0.2, fc=INK, ec=INK))
        ax.add_patch(Circle((x, cy - 0.38), 0.07, fc='white', ec='none', zorder=3))


def car(ax, cx, cy):
    ax.add_patch(Polygon([(cx - 0.55, cy + 0.12), (cx - 0.3, cy + 0.55), (cx + 0.35, cy + 0.55), (cx + 0.65, cy + 0.12)], closed=True,
                         fc=RED, ec=INK, lw=2))
    ax.add_patch(Polygon([(cx - 0.4, cy + 0.15), (cx - 0.24, cy + 0.45), (cx + 0.0, cy + 0.45), (cx + 0.0, cy + 0.15)], closed=True,
                         fc=LBLUE, ec=INK, lw=1.2, zorder=3))
    ax.add_patch(Polygon([(cx + 0.08, cy + 0.15), (cx + 0.08, cy + 0.45), (cx + 0.3, cy + 0.45), (cx + 0.5, cy + 0.15)], closed=True,
                         fc=LBLUE, ec=INK, lw=1.2, zorder=3))
    ax.add_patch(FancyBboxPatch((cx - 1.0, cy - 0.3), 2.0, 0.45, boxstyle='round,pad=0,rounding_size=0.1', fc=RED, ec=INK, lw=2, zorder=2))
    for x in (cx - 0.55, cx + 0.55):
        ax.add_patch(Circle((x, cy - 0.32), 0.2, fc=INK, ec=INK, zorder=3))
        ax.add_patch(Circle((x, cy - 0.32), 0.07, fc='white', ec='none', zorder=4))


def bike(ax, cx, cy):
    rw = 0.42
    for x in (cx - 0.65, cx + 0.65):
        ax.add_patch(Circle((x, cy - 0.15), rw, fc='none', ec=INK, lw=2.4))
        ax.add_patch(Circle((x, cy - 0.15), 0.04, fc=INK, ec=INK))
    bb = (cx - 0.05, cy - 0.15); seat = (cx - 0.25, cy + 0.5); head = (cx + 0.45, cy + 0.45)
    line(ax, [cx - 0.65, bb[0], head[0] - 0.05, seat[0] + 0.05, cx - 0.65], [cy - 0.15, bb[1], head[1] - 0.12, seat[1] - 0.12, cy - 0.15], color=GRN, lw=2.6)
    line(ax, [bb[0], seat[0]], [bb[1], seat[1]], color=GRN, lw=2.6)
    line(ax, [cx + 0.65, head[0]], [cy - 0.15, head[1] + 0.05], color=GRN, lw=2.6)
    line(ax, [seat[0] - 0.15, seat[0] + 0.15], [seat[1] + 0.03, seat[1] + 0.03], lw=4)
    line(ax, [head[0] - 0.05, head[0] + 0.2], [head[1] + 0.08, head[1] + 0.12], lw=3)


def train(ax, cx, cy):
    line(ax, [0.2, 3.8], [cy - 0.55, cy - 0.55], lw=2.4)
    for x in np.arange(0.35, 3.8, 0.3):
        line(ax, [x, x], [cy - 0.55, cy - 0.66], lw=1.6)
    for k, x0 in enumerate((cx - 1.65, cx + 0.05)):
        w = 1.6
        ax.add_patch(FancyBboxPatch((x0, cy - 0.42), w, 0.95, boxstyle='round,pad=0,rounding_size=0.12', fc='#e9eef2', ec=INK, lw=2))
        ax.add_patch(Rectangle((x0, cy - 0.2), w, 0.1, fc=BLUE, ec='none', zorder=3))
        for j in range(3):
            ax.add_patch(Rectangle((x0 + 0.15 + j * 0.48, cy + 0.08), 0.34, 0.3, fc=LBLUE, ec=INK, lw=1.2, zorder=3))
        for x in (x0 + 0.35, x0 + w - 0.35):
            ax.add_patch(Circle((x, cy - 0.45), 0.09, fc=INK, ec=INK, zorder=3))
    line(ax, [cx - 0.05, cx + 0.05], [cy, cy], lw=3)


def mini_bars(ax, labels, vals, title):
    line(ax, [0.5, 3.7], [0.62, 0.62], lw=1.8)
    line(ax, [0.5, 0.5], [0.62, 2.55], lw=1.8)
    txt(ax, 0.6, 2.7, title, fs=12, va='center')
    for k, (lab, v) in enumerate(zip(labels, vals)):
        x = 1.15 + k * 0.95
        ax.add_patch(Rectangle((x - 0.28, 0.62), 0.56, v, fc=BLUE, ec=INK, lw=1.4))
        txt(ax, x, 0.38, lab, fs=12, ha='center', va='center')


def week(ax, marks, style='circle'):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    w, x0, y0, h = 0.545, 0.0925, 0.75, 1.5
    txt(ax, 2.0, 2.6, 'This Week', fs=13, ha='center', va='center')
    for k, d in enumerate(days):
        x = x0 + k * w
        closed = style == 'x' and d.upper() in marks
        ax.add_patch(Rectangle((x, y0), w, h, fc=LGREY if closed else 'white', ec=INK, lw=1.3))
        ax.add_patch(Rectangle((x, y0 + h - 0.38), w, 0.38, fc='#f0d9a8', ec=INK, lw=1.3))
        txt(ax, x + w / 2, y0 + h - 0.19, d, fs=11, ha='center', va='center')
        if style == 'circle' and d.upper() in marks:
            ax.add_patch(Ellipse((x + w / 2, y0 + 0.55), 0.42, 0.58, fc='none', ec=RED, lw=2.6))
            ax.add_patch(Circle((x + w / 2, y0 + 0.55), 0.06, fc=RED, ec=RED))
        if closed:
            line(ax, [x + 0.1, x + w - 0.1], [y0 + 0.25, y0 + 0.85], color=RED, lw=2.6)
            line(ax, [x + 0.1, x + w - 0.1], [y0 + 0.85, y0 + 0.25], color=RED, lw=2.6)


# ───────────────────────── 選項圖的畫法 ─────────────────────────
def D_clock(h, m):
    return lambda ax: clock(ax, h, m)


def D_weather(kind):
    return lambda ax: weather(ax, kind, 2.0, 1.5, 1.7)


def D_ampm(a, p):
    def d(ax):
        line(ax, [2, 2], [0.25, 2.75], color=GREY, lw=1.4)
        txt(ax, 1.0, 2.55, 'AM', fs=14, ha='center', va='center')
        txt(ax, 3.0, 2.55, 'PM', fs=14, ha='center', va='center')
        weather(ax, a, 1.0, 1.25, 1.15)
        weather(ax, p, 3.0, 1.25, 1.15)
    return d


def D_wtemp(kind, t):
    def d(ax):
        weather(ax, kind, 1.3, 1.5, 1.4)
        txt(ax, 3.0, 1.45, t, fs=22, ha='center', va='center')
    return d


def D_shirt(price):
    def d(ax):
        tshirt(ax, 1.15, 1.5, 1.05)
        tag(ax, 2.95, 1.5, price, w=1.55)
    return d


def D_pen_nb(p_pen, p_nb):
    def d(ax):
        pen(ax, 1.05, 2.05, 0.95)
        notebook(ax, 3.0, 2.0, 0.9)
        tag(ax, 1.05, 0.8, p_pen, w=1.35, h=0.6, fs=16)
        tag(ax, 3.0, 0.8, p_nb, w=1.35, h=0.6, fs=16)
    return d


def D_sale(old, new):
    def d(ax):
        # 蛋糕
        ax.add_patch(Rectangle((0.4, 0.85), 1.1, 0.75, fc='#f6d2d0', ec=INK, lw=1.8))
        line(ax, [0.4, 1.5], [1.2, 1.2], color='#c0605a', lw=2)
        ax.add_patch(Rectangle((0.4, 1.6), 1.1, 0.12, fc='white', ec=INK, lw=1.4))
        ax.add_patch(Circle((0.95, 1.86), 0.12, fc=RED, ec=INK, lw=1.2))
        # 價格牌
        ax.add_patch(FancyBboxPatch((1.95, 0.55), 1.7, 1.9, boxstyle='round,pad=0,rounding_size=0.12', fc=CREAM, ec=INK, lw=2))
        txt(ax, 2.8, 2.0, old, fs=17, color=GREY, ha='center', va='center')
        line(ax, [2.35, 3.25], [1.88, 2.12], color=RED, lw=2.4)
        ax.annotate('', xy=(2.8, 1.45), xytext=(2.8, 1.75), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.6))
        txt(ax, 2.8, 1.05, new, fs=22, ha='center', va='center')
    return d


def D_table_ball(where):
    pos = {'under_table': (1.35, 0.56), 'on_table': (1.35, 1.52), 'under_chair': (3.08, 0.56), 'on_chair': (3.0, 1.08)}
    def d(ax):
        floor(ax)
        table(ax, 0.4, 2.3, 1.32)
        chair(ax, 2.7, 3.5, 0.88, 1.75)
        ball(ax, *pos[where])
    return d


def D_stack(order):
    # order:從下到上;'cup_side' 表示杯子在箱子旁的地上
    def d(ax):
        floor(ax)
        y = 0.35
        for it in order:
            if it == 'box':
                box(ax, 1.4, y, 1.2, 0.75); y += 0.75
            elif it == 'book':
                flat_book(ax, 2.0, y); y += 0.24
            elif it == 'cup':
                cup(ax, 2.0, y); y += 0.5
            elif it == 'cup_side':
                cup(ax, 3.1, 0.35)
    return d


def D_wall_clock(where):
    pos = {'above_door': (1.3, 2.42), 'above_window': (2.8, 2.25), 'left_door': (0.5, 1.45), 'right_window': (3.55, 1.45)}
    def d(ax):
        floor(ax)
        door(ax, 0.9, 1.7, 2.0)
        window(ax, 2.4, 3.2, 1.05, 1.85)
        small_clock(ax, *pos[where])
    return d


def D_balls_box(n_in, n_on, n_side):
    def d(ax):
        floor(ax)
        box(ax, 1.1, 0.35, 1.8, 1.0, alpha=0.55)
        xs = {1: [2.0], 2: [1.6, 2.4], 3: [1.5, 2.0, 2.5]}
        for x in xs.get(n_in, []):
            ball(ax, x, 0.6)
        for x in xs.get(n_on, []):
            ball(ax, x, 1.56)
        for k in range(n_side):
            ball(ax, 3.35, 0.56 + 0.42 * k)
    return d


def D_desk_row(order):
    def d(ax):
        floor(ax)
        table(ax, 0.3, 3.7, 1.0)
        for x, it in zip((0.95, 2.0, 3.05), order):
            {'cup': lambda x: cup(ax, x - 0.03, 1.0), 'book': lambda x: upright_book(ax, x, 1.0),
             'lamp': lambda x: lamp(ax, x, 1.0)}[it](x)
    return d


def D_cups_books(nc, nb):
    def d(ax):
        floor(ax)
        table(ax, 0.3, 3.7, 1.0)
        items = ['c'] * nc + ['b'] * nb
        step = 0.56
        x0 = 2.0 - step * (len(items) - 1) / 2
        for k, it in enumerate(items):
            x = x0 + k * step
            if it == 'c':
                cup(ax, x - 0.03, 1.0)
            else:
                upright_book(ax, x, 1.0, fc=GRN)
    return d


def D_pencils(n):
    def d(ax):
        step = 0.55
        x0 = 2.0 - step * (n - 1) / 2
        for k in range(n):
            pencil(ax, x0 + k * step, 0.6)
    return d


def D_eggs(n_cartons, cols):
    def d(ax):
        wbox = cols * 0.34 + 0.08
        gap = 0.12
        tot = n_cartons * wbox + (n_cartons - 1) * gap
        x0 = 2.0 - tot / 2
        for k in range(n_cartons):
            carton(ax, x0 + k * (wbox + gap), 1.1, cols)
    return d


def D_route(turn_at, side):
    def d(ax):
        road(ax, [2, 2], [0.15, 2.85])
        for y in (1.15, 2.15):
            road(ax, [0.2, 3.8], [y, y])
        y = (1.15, 2.15)[turn_at - 1]
        x = 0.45 if side == 'L' else 3.55
        start_dot(ax, 2, 0.35)
        path_arrow(ax, [(2, 0.35), (2, y), (x, y)])
    return d


def D_north(where):
    # 學校標籤一律放在圖示正下方(四個選項一致,不因方位改變標示位置)
    pos = {'N': (1.9, 2.45), 'S': (1.9, 0.8), 'E': (3.2, 1.55), 'W': (0.75, 1.55)}
    def d(ax):
        compass_n(ax, 3.6, 2.35)
        tree(ax, 1.9, 1.55)
        txt(ax, 2.18, 1.5, 'Park', fs=12, va='center')
        x, y = pos[where]
        school(ax, x, y, 0.8)
        txt(ax, x, y - 0.42, 'School', fs=12, ha='center', va='center')
    return d


def D_turn_shop(turn, shop_side):
    def d(ax):
        road(ax, [2, 2], [0.15, 1.5])
        road(ax, [0.2, 3.8], [1.5, 1.5])
        traffic_light(ax, 2.35, 2.05)
        start_dot(ax, 2, 0.35)
        x_end = 3.55 if turn == 'R' else 0.45
        path_arrow(ax, [(2, 0.35), (2, 1.5), (x_end, 1.5)])
        sx = 3.3 if turn == 'R' else 0.7
        sy = 2.25 if shop_side == 'up' else 0.82
        shop(ax, sx, sy)
    return d


def D_floor(fl):
    def d(ax):
        x0, x1, y0, fh = 1.1, 2.9, 0.35, 0.58
        for k in range(4):
            y = y0 + k * fh
            hi = (k + 1 == fl)
            ax.add_patch(Rectangle((x0, y), x1 - x0, fh, fc='#fbd7d4' if hi else 'white', ec=INK, lw=1.8))
            txt(ax, x0 - 0.35, y + fh / 2, f'{k + 1}F', fs=13, ha='center', va='center')
            for j in range(2):
                ax.add_patch(Rectangle((x0 + 0.2 + j * 0.45, y + 0.15), 0.3, 0.28, fc=LBLUE, ec=INK, lw=1.2))
        # 電梯
        ax.add_patch(Rectangle((x1 - 0.45, y0), 0.45, 4 * fh, fc=LGREY, ec=INK, lw=1.4))
        ax.annotate('', xy=(x1 - 0.22, y0 + 4 * fh - 0.15), xytext=(x1 - 0.22, y0 + 0.15),
                    arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.6))
        ym = y0 + (fl - 0.5) * fh
        ax.annotate('', xy=(x1 + 0.05, ym), xytext=(x1 + 0.6, ym), arrowprops=dict(arrowstyle='-|>', color=RED, lw=2.6))
    return d


def D_cal(month, day):
    def d(ax):
        ax.add_patch(Rectangle((1.05, 0.35), 1.9, 2.3, fc='white', ec=INK, lw=2))
        ax.add_patch(Rectangle((1.05, 2.0), 1.9, 0.65, fc=RED, ec=INK, lw=2))
        txt(ax, 2.0, 2.32, month, fs=17, color='white', ha='center', va='center')
        txt(ax, 2.0, 1.15, str(day), fs=40, ha='center', va='center')
        for x in (1.45, 2.55):
            ax.add_patch(Rectangle((x - 0.04, 2.5), 0.08, 0.3, fc=GREY, ec=INK, lw=1))
    return d


def D_week(marks, style):
    return lambda ax: week(ax, marks, style)


def D_thermo(v):
    return lambda ax: thermo(ax, 1.85, v, 0, 50, 10, 2)


def D_two_thermo(a, b):
    def d(ax):
        for cx, v, lab in ((1.0, a, '8:00'), (2.85, b, '12:00')):
            thermo(ax, cx, v, 0, 20, 5, 1, y0=0.92, y1=2.5)
            txt(ax, cx + 0.15, 0.36, lab, fs=12, ha='center', va='center')
    return d


def D_trans(kind):
    fn = {'bus': bus, 'car': car, 'bike': bike, 'train': train}[kind]
    return lambda ax: fn(ax, 2.0, 1.5)


def D_bars(labels, vals, title):
    return lambda ax: mini_bars(ax, labels, vals, title)


# ───────────────────────── 聽力辨識句意 30 題 ─────────────────────────
P = '請選出與聽到內容相符的圖。'
LIST = [
    dict(id=21100, g=7, d=1, ans=2, s="I get up at seven thirty every morning.",
         o=[("時鐘指著 7 點 30 分", D_clock(7, 30)), ("時鐘指著 7 點 15 分", D_clock(7, 15)),
            ("時鐘指著 6 點 30 分", D_clock(6, 30)), ("時鐘指著 8 點 30 分", D_clock(8, 30))],
         e="seven thirty 是 7 點 30 分,長針指 6、短針在 7 和 8 中間。7 點 15 分長針指 3;6 點 30 分和 8 點 30 分是小時聽錯。"),
    dict(id=21101, g=9, d=3, ans=0, s="The movie starts at a quarter to nine.",
         o=[("時鐘指著 8 點 45 分", D_clock(8, 45)), ("時鐘指著 9 點 15 分", D_clock(9, 15)),
            ("時鐘指著 9 點 45 分", D_clock(9, 45)), ("時鐘指著 8 點 15 分", D_clock(8, 15))],
         e="a quarter to nine 是「差 15 分 9 點」,也就是 8 點 45 分,長針指 9、短針接近 9。9 點 15 分是 a quarter past nine;9 點 45 分是 a quarter to ten;8 點 15 分是 a quarter past eight。"),
    dict(id=21102, g=8, d=2, ans=3, s="The train left at ten past four.",
         o=[("時鐘指著 4 點 10 分", D_clock(4, 10)), ("時鐘指著 4 點 50 分", D_clock(4, 50)),
            ("時鐘指著 10 點 20 分", D_clock(10, 20)), ("時鐘指著 3 點 50 分", D_clock(3, 50))],
         e="ten past four 是 4 點過 10 分,即 4 點 10 分,長針指 2、短針剛過 4。4 點 50 分是 ten to five;3 點 50 分是 ten to four;10 點 20 分是把長短針看反了。"),
    dict(id=21103, g=7, d=1, ans=1, s="It will be rainy tomorrow.",
         o=[("雲下面有雨滴(下雨)", D_weather('rain')), ("太陽(晴天)", D_weather('sun')),
            ("雲下面有雪花(下雪)", D_weather('snow')), ("只有雲(陰天)", D_weather('cloud'))],
         e="rainy 是下雨的,要選雲下面有雨滴的圖。太陽是 sunny,雪花是 snowy,只有雲是 cloudy。"),
    dict(id=21104, g=8, d=2, ans=1, s="It was sunny in the morning, but it rained in the afternoon.",
         o=[("上午(AM)晴天,下午(PM)下雨", D_ampm('sun', 'rain')), ("上午(AM)下雨,下午(PM)晴天", D_ampm('rain', 'sun')),
            ("上午(AM)晴天,下午(PM)陰天", D_ampm('sun', 'cloud')), ("上午(AM)陰天,下午(PM)下雨", D_ampm('cloud', 'rain'))],
         e="上午 sunny(晴天)、下午 rained(下雨),所以 AM 是太陽、PM 是雨。上下午顛倒的不對;下午只是陰天、或上午是陰天的,都和內容不符。"),
    dict(id=21105, g=8, d=2, ans=3, s="It's snowing now, and it's minus five degrees outside.",
         o=[("下雪,溫度 -5°C", D_wtemp('snow', '-5°C')), ("下雪,溫度 5°C", D_wtemp('snow', '5°C')),
            ("晴天,溫度 -5°C", D_wtemp('sun', '-5°C')), ("下雨,溫度 -5°C", D_wtemp('rain', '-5°C'))],
         e="snowing 是下雪,minus five degrees 是零下 5 度,要選雪花和 -5°C 的圖。5°C 少了 minus(零下);晴天或下雨的天氣都不符。"),
    dict(id=21106, g=7, d=1, ans=0, s="This T-shirt is two hundred and fifty dollars.",
         o=[("T 恤價格牌 $250", D_shirt('$250')), ("T 恤價格牌 $215", D_shirt('$215')),
            ("T 恤價格牌 $205", D_shirt('$205')), ("T 恤價格牌 $150", D_shirt('$150'))],
         e="two hundred and fifty 是 250。215 是 two hundred and fifteen,205 是 two hundred and five,150 是 one hundred and fifty。"),
    dict(id=21107, g=8, d=2, ans=2, s="The pen is thirty dollars, and the notebook is fifty dollars.",
         o=[("筆 $30,筆記本 $50", D_pen_nb('$30', '$50')), ("筆 $50,筆記本 $30", D_pen_nb('$50', '$30')),
            ("筆 $30,筆記本 $15", D_pen_nb('$30', '$15')), ("筆 $13,筆記本 $50", D_pen_nb('$13', '$50'))],
         e="筆是 thirty（30 元）、筆記本是 fifty（50 元）。兩個價格對調的不對;fifteen 是 15、thirteen 是 13,要注意 -teen 和 -ty 的發音差別。"),
    dict(id=21108, g=9, d=3, ans=3, s="The cake was eighty dollars, but now it's twenty dollars off.",
         o=[("蛋糕原價 $80,現價 $60", D_sale('$80', '$60')), ("蛋糕原價 $80,現價 $20", D_sale('$80', '$20')),
            ("蛋糕原價 $100,現價 $80", D_sale('$100', '$80')), ("蛋糕原價 $80,現價 $100", D_sale('$80', '$100'))],
         e="原價 eighty（80 元）,twenty dollars off 是「便宜 20 元」,現價 80 - 20 = 60 元。現價 20 元是把 off 誤當成售價;原價 100 元不符;現價 100 元是把折扣加上去了。"),
    dict(id=21109, g=7, d=1, ans=1, s="The ball is under the table.",
         o=[("球在桌子下面", D_table_ball('under_table')), ("球在桌子上", D_table_ball('on_table')),
            ("球在椅子下面", D_table_ball('under_chair')), ("球在椅子上", D_table_ball('on_chair'))],
         e="under the table 是在桌子下面。球在桌上是 on the table;在椅子下面或椅子上,地點都不對。"),
    dict(id=21110, g=8, d=2, ans=2, s="The cup is on the book, and the book is on the box.",
         o=[("由下往上依序是箱子、書、杯子", D_stack(['box', 'book', 'cup'])),
            ("由下往上依序是箱子、杯子、書", D_stack(['box', 'cup', 'book'])),
            ("由下往上依序是書、箱子、杯子", D_stack(['book', 'box', 'cup'])),
            ("書放在箱子上,杯子在箱子旁的地上", D_stack(['box', 'book', 'cup_side']))],
         e="杯子在書上、書在箱子上,所以由下往上是箱子、書、杯子。書在杯子上、箱子在書上都把順序弄反了;杯子放在地上也不符合 on the book。"),
    dict(id=21111, g=8, d=2, ans=0, s="There's a clock above the door.",
         o=[("時鐘掛在門的上方", D_wall_clock('above_door')), ("時鐘掛在窗戶上方", D_wall_clock('above_window')),
            ("時鐘掛在門的左邊", D_wall_clock('left_door')), ("時鐘掛在窗戶右邊", D_wall_clock('right_window'))],
         e="above the door 是在門的上方。掛在窗戶上方是 above the window;在門左邊、窗戶右邊都是 next to,不是 above。"),
    dict(id=21112, g=7, d=2, ans=0, s="There are two balls in the box and one ball on the box.",
         o=[("箱子裡有 2 顆球,箱子上有 1 顆球", D_balls_box(2, 1, 0)), ("箱子裡有 1 顆球,箱子上有 2 顆球", D_balls_box(1, 2, 0)),
            ("箱子裡有 2 顆球,箱子旁邊有 1 顆球", D_balls_box(2, 0, 1)), ("箱子裡有 3 顆球", D_balls_box(3, 0, 0))],
         e="in the box 是在箱子裡面(2 顆),on the box 是在箱子上面(1 顆)。數量對調的不對;球在箱子旁邊是 next to;3 顆都在箱子裡也不符。"),
    dict(id=21113, g=8, d=2, ans=2, s="The book is between the cup and the lamp.",
         o=[("桌上由左到右是杯子、書、檯燈", D_desk_row(['cup', 'book', 'lamp'])), ("桌上由左到右是書、杯子、檯燈", D_desk_row(['book', 'cup', 'lamp'])),
            ("桌上由左到右是杯子、檯燈、書", D_desk_row(['cup', 'lamp', 'book'])), ("桌上由左到右是書、檯燈、杯子", D_desk_row(['book', 'lamp', 'cup']))],
         e="between the cup and the lamp 是書在杯子和檯燈中間。其他三張圖中間的都不是書(分別是杯子或檯燈),書都在最旁邊。"),
    dict(id=21114, g=7, d=2, ans=1, s="There are three cups and two books on the table.",
         o=[("桌上有 3 個杯子和 2 本書", D_cups_books(3, 2)), ("桌上有 2 個杯子和 3 本書", D_cups_books(2, 3)),
            ("桌上有 3 個杯子和 3 本書", D_cups_books(3, 3)), ("桌上有 2 個杯子和 2 本書", D_cups_books(2, 2))],
         e="three cups 是 3 個杯子,two books 是 2 本書。數量對調、或杯子和書數量相同的圖都不對。"),
    dict(id=21115, g=8, d=2, ans=3, s="I had four pencils, but I lost one of them.",
         o=[("3 枝鉛筆", D_pencils(3)), ("4 枝鉛筆", D_pencils(4)), ("5 枝鉛筆", D_pencils(5)), ("2 枝鉛筆", D_pencils(2))],
         e="原本有 4 枝,lost one(弄丟 1 枝),現在剩 4 - 1 = 3 枝。4 枝是沒有扣掉弄丟的;5 枝是誤加;2 枝是多扣了。"),
    dict(id=21116, g=8, d=2, ans=0, s="I bought two boxes of eggs. There are six eggs in each box.",
         o=[("2 盒蛋,每盒 6 顆", D_eggs(2, 3)), ("1 盒蛋,每盒 6 顆", D_eggs(1, 3)),
            ("2 盒蛋,每盒 4 顆", D_eggs(2, 2)), ("3 盒蛋,每盒 6 顆", D_eggs(3, 3))],
         e="two boxes 是 2 盒,six eggs in each box 是每盒 6 顆。只有 1 盒、每盒 4 顆或 3 盒都和內容不符。"),
    dict(id=21117, g=8, d=2, ans=2, s="Go straight and turn left at the second corner.",
         o=[("直走,在第二個路口左轉", D_route(2, 'L')), ("直走,在第二個路口右轉", D_route(2, 'R')),
            ("直走,在第一個路口左轉", D_route(1, 'L')), ("直走,在第一個路口右轉", D_route(1, 'R'))],
         e="go straight 直走,turn left at the second corner 在第二個路口左轉。右轉的方向錯;在第一個路口轉彎則是路口錯。"),
    dict(id=21118, g=8, d=2, ans=3, s="The school is north of the park.",
         o=[("學校在公園的北邊", D_north('N')), ("學校在公園的南邊", D_north('S')),
            ("學校在公園的東邊", D_north('E')), ("學校在公園的西邊", D_north('W'))],
         e="north of the park 是在公園的北邊;圖上 N 箭頭指向上方,所以學校要在公園上方。在下方是南邊(south),右邊是東邊(east),左邊是西邊(west)。"),
    dict(id=21119, g=9, d=3, ans=1, s="Turn right at the traffic light, and the shop will be on your left.",
         o=[("在紅綠燈右轉,商店在右轉後道路的左側", D_turn_shop('R', 'up')),
            ("在紅綠燈右轉,商店在右轉後道路的右側", D_turn_shop('R', 'down')),
            ("在紅綠燈左轉,商店在左轉後道路的左側", D_turn_shop('L', 'down')),
            ("在紅綠燈左轉,商店在左轉後道路的右側", D_turn_shop('L', 'up'))],
         e="先在紅綠燈右轉;右轉後面向圖的右方前進,這時「左手邊」是道路的上側,所以商店要在右轉那段路的上方。商店在下方是 on your right;左轉的兩張圖則是轉彎方向錯。"),
    dict(id=21120, g=7, d=1, ans=0, s="Take the elevator up to the third floor.",
         o=[("箭頭指著 3 樓(3F)", D_floor(3)), ("箭頭指著 2 樓(2F)", D_floor(2)),
            ("箭頭指著 4 樓(4F)", D_floor(4)), ("箭頭指著 1 樓(1F)", D_floor(1))],
         e="the third floor 是 3 樓(3F)。second 是 2 樓,fourth 是 4 樓,first 是 1 樓。"),
    dict(id=21121, g=7, d=1, ans=3, s="My birthday is on May twentieth.",
         o=[("日曆:MAY 20", D_cal('MAY', 20)), ("日曆:MAY 12", D_cal('MAY', 12)),
            ("日曆:MAY 21", D_cal('MAY', 21)), ("日曆:MARCH 20", D_cal('MARCH', 20))],
         e="May twentieth 是 5 月 20 日。12 日是 twelfth,21 日是 twenty-first;MARCH 是 3 月,月份不對。"),
    dict(id=21122, g=9, d=3, ans=2, s="Today is Tuesday. Our school trip is the day after tomorrow.",
         o=[("一週日曆圈起星期四(Thu)", D_week(['THU'], 'circle')), ("一週日曆圈起星期三(Wed)", D_week(['WED'], 'circle')),
            ("一週日曆圈起星期五(Fri)", D_week(['FRI'], 'circle')), ("一週日曆圈起星期二(Tue)", D_week(['TUE'], 'circle'))],
         e="今天星期二,the day after tomorrow(後天)是星期四,要圈 Thu。星期三是 tomorrow(明天);星期五是大後天;星期二是今天。"),
    dict(id=21123, g=8, d=2, ans=1, s="The shop is open from Monday to Friday.",
         o=[("星期六、日打叉(星期一到五營業)", D_week(['SAT', 'SUN'], 'x')), ("只有星期日打叉(星期一到六營業)", D_week(['SUN'], 'x')),
            ("星期一、六、日打叉(星期二到五營業)", D_week(['MON', 'SAT', 'SUN'], 'x')), ("星期五、六、日打叉(星期一到四營業)", D_week(['FRI', 'SAT', 'SUN'], 'x'))],
         e="from Monday to Friday 是星期一到星期五營業,所以只有星期六、日不開(打叉)。星期六也營業、星期一或星期五沒營業的圖都不對。"),
    dict(id=21124, g=8, d=2, ans=3, s="It's thirty-two degrees today. It's very hot.",
         o=[("溫度計指在 32°C", D_thermo(32)), ("溫度計指在 23°C", D_thermo(23)),
            ("溫度計指在 12°C", D_thermo(12)), ("溫度計指在 42°C", D_thermo(42))],
         e="thirty-two 是 32 度,溫度計紅柱在 30 再往上兩小格。23 是 twenty-three(數字顛倒);12 是 twelve;42 是 forty-two。"),
    dict(id=21125, g=9, d=3, ans=2, s="It was ten degrees at eight in the morning. At noon, it was five degrees warmer.",
         o=[("8:00 為 10°C,12:00 為 15°C", D_two_thermo(10, 15)), ("8:00 為 10°C,12:00 為 5°C", D_two_thermo(10, 5)),
            ("8:00 為 15°C,12:00 為 10°C", D_two_thermo(15, 10)), ("8:00 為 5°C,12:00 為 10°C", D_two_thermo(5, 10))],
         e="早上 8 點是 10 度,中午 five degrees warmer(暖 5 度)是 10 + 5 = 15 度。中午 5 度是把 warmer 當成「變成 5 度」或變冷;8 點 15 度、中午 10 度是變冷;8 點 5 度的起點溫度不對。"),
    dict(id=21126, g=7, d=1, ans=2, s="I go to school by bus every day.",
         o=[("公車", D_trans('bus')), ("腳踏車", D_trans('bike')), ("汽車", D_trans('car')), ("火車/捷運", D_trans('train'))],
         e="by bus 是搭公車。腳踏車是 by bike,汽車是 by car,火車/捷運是 by train / by MRT。"),
    dict(id=21127, g=8, d=2, ans=0, s="My father usually drives to work, but today he is taking the MRT.",
         o=[("捷運列車", D_trans('train')), ("汽車", D_trans('car')), ("公車", D_trans('bus')), ("腳踏車", D_trans('bike'))],
         e="爸爸平常開車(usually drives),但今天(today)搭捷運(taking the MRT),問的是今天,所以選捷運列車。汽車是平常的交通方式;公車、腳踏車都沒提到。"),
    dict(id=21128, g=9, d=3, ans=1, s="Tom is taller than Ben, but Ben is taller than Sam.",
         o=[("身高長條圖:Tom 最高、Ben 第二、Sam 最矮", D_bars(['Tom', 'Ben', 'Sam'], [1.75, 1.25, 0.8], 'Height')),
            ("身高長條圖:Ben 最高、Tom 第二、Sam 最矮", D_bars(['Tom', 'Ben', 'Sam'], [1.25, 1.75, 0.8], 'Height')),
            ("身高長條圖:Tom 最高、Sam 第二、Ben 最矮", D_bars(['Tom', 'Ben', 'Sam'], [1.75, 0.8, 1.25], 'Height')),
            ("身高長條圖:Sam 最高、Tom 第二、Ben 最矮", D_bars(['Tom', 'Ben', 'Sam'], [1.25, 0.8, 1.75], 'Height'))],
         e="Tom 比 Ben 高,Ben 又比 Sam 高,所以由高到矮是 Tom、Ben、Sam。Ben 最高的圖違反第一句;Sam 比 Ben 高的兩張圖違反第二句。"),
    dict(id=21129, g=8, d=2, ans=3, s="We sold the most books on Wednesday and the fewest on Monday.",
         o=[("賣書長條圖:星期三最多、星期一最少", D_bars(['Mon', 'Tue', 'Wed'], [0.8, 1.25, 1.75], 'Books sold')),
            ("賣書長條圖:星期一最多、星期三最少", D_bars(['Mon', 'Tue', 'Wed'], [1.75, 1.25, 0.8], 'Books sold')),
            ("賣書長條圖:星期二最多、星期一最少", D_bars(['Mon', 'Tue', 'Wed'], [0.8, 1.75, 1.25], 'Books sold')),
            ("賣書長條圖:星期三最多、星期二最少", D_bars(['Mon', 'Tue', 'Wed'], [1.25, 0.8, 1.75], 'Books sold'))],
         e="the most 在 Wednesday(星期三最多),the fewest 在 Monday(星期一最少)。最多、最少顛倒的不對;星期二最多或星期二最少的圖也都不符。"),
]


def ordered(q):
    o = list(q['o'])
    c = o.pop(0)
    o.insert(q['ans'], c)
    return o


def _reg(qid, k, draw):
    @fig(qid * 10 + k)
    def _f():
        f, ax = card()
        draw(ax)
        save(f, qid * 10 + k)


for _q in LIST:
    for _k, (_desc, _draw) in enumerate(ordered(_q)):
        _reg(_q['id'], _k, _draw)


# ───────────────────────── 看圖閱讀 10 題(題幹圖) ─────────────────────────
def board(w=6.0, h=4.0):
    f, ax = new_ax(w, h)
    ax.set_xlim(0, w); ax.set_ylim(0, h)
    return f, ax


def panel(ax, x0, y0, w, h, fc='white', lw=2.2):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle='round,pad=0,rounding_size=0.15', fc=fc, ec=INK, lw=lw))


def grid_table(ax, x0, y_top, colw, rowh, rows, header_fc='#f0d9a8', fs=13):
    y = y_top
    for r, row in enumerate(rows):
        x = x0
        for c, cell in enumerate(row):
            ax.add_patch(Rectangle((x, y - rowh), colw[c], rowh, fc=header_fc if r == 0 else 'white', ec=INK, lw=1.4))
            txt(ax, x + colw[c] / 2, y - rowh / 2, cell, fs=fs, ha='center', va='center')
            x += colw[c]
        y -= rowh


@fig(21130)
def f21130():
    f, ax = board(6.0, 4.0)
    panel(ax, 0.1, 0.1, 5.8, 3.8)
    ax.add_patch(Rectangle((0.1, 3.15), 5.8, 0.75, fc=BLUE, ec=INK, lw=2.2))
    txt(ax, 3.0, 3.52, 'Bus 307  Park Station → Sunny Junior High', fs=15, color='white', ha='center', va='center')
    txt(ax, 3.0, 2.82, 'Leaves Park Station at:', fs=14, ha='center', va='center')
    for k, t in enumerate(['7:05', '7:20', '7:35', '7:50', '8:05']):
        x = 0.75 + k * 1.12
        ax.add_patch(FancyBboxPatch((x - 0.45, 1.75), 0.9, 0.6, boxstyle='round,pad=0,rounding_size=0.08', fc=CREAM, ec=INK, lw=1.6))
        txt(ax, x, 2.05, t, fs=15, ha='center', va='center')
    txt(ax, 3.0, 1.15, 'The trip to Sunny Junior High takes 25 minutes.', fs=13, ha='center', va='center')
    txt(ax, 3.0, 0.6, 'Every day except Sunday', fs=12, color=GREY, ha='center', va='center')
    save(f, 21130)


@fig(21131)
def f21131():
    f, ax = board(5.6, 4.0)
    panel(ax, 0.1, 0.1, 5.4, 3.8, fc='#fffaf0')
    txt(ax, 2.8, 3.4, 'DRINKS MENU', fs=18, ha='center', va='center')
    line(ax, [0.6, 5.0], [3.0, 3.0], lw=1.6)
    items = [('Black Tea', '$25'), ('Green Tea', '$30'), ('Milk Tea', '$45'), ('Lemon Juice', '$40')]
    for k, (n, p) in enumerate(items):
        y = 2.55 - k * 0.58
        txt(ax, 0.8, y, n, fs=15, va='center')
        ax.plot([2.6, 4.0], [y - 0.08, y - 0.08], color=GREY, lw=1.2, ls=(0, (1, 3)))
        txt(ax, 4.75, y, p, fs=15, ha='right', va='center')
    save(f, 21131)


@fig(21132)
def f21132():
    f, ax = plt.subplots(figsize=(5.6, 3.8), dpi=200)
    names = ['Amy', 'Ben', 'Cindy', 'David']; hrs = [6, 4, 9, 4]
    ax.bar(names, hrs, width=0.55, color=BLUE, edgecolor=INK, lw=1.4, zorder=3)
    ax.set_ylim(0, 10); ax.set_yticks(range(0, 11, 2))
    ax.grid(axis='y', color=LGREY, lw=1, zorder=0)
    ax.set_title('Hours of Reading Last Week', fontproperties=PF, fontsize=15, color=INK)
    ax.set_ylabel('Hours', fontproperties=PF, fontsize=13, color=INK)
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontproperties(PF); lab.set_fontsize(13)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    for sp in ('left', 'bottom'):
        ax.spines[sp].set_linewidth(1.4)
    save(f, 21132)


@fig(21133)
def f21133():
    f, ax = board(5.6, 4.0)
    panel(ax, 0.3, 0.6, 5.0, 3.2, fc='white', lw=3)
    ax.add_patch(Rectangle((2.6, 0.1), 0.4, 0.5, fc=GREY, ec=INK, lw=1.6))
    # 禁止游泳符號
    cx, cy, r = 1.35, 2.2, 0.75
    ax.add_patch(Circle((cx, cy), r, fc='white', ec=RED, lw=5, zorder=3))
    for k in range(3):
        xs = np.linspace(cx - 0.5, cx + 0.5, 40)
        line(ax, xs, cy - 0.25 + 0.2 * k + 0.06 * np.sin(xs * 14), color=BLUE, lw=2.4, zorder=3)
    line(ax, [cx - r * 0.7, cx + r * 0.7], [cy + r * 0.7, cy - r * 0.7], color=RED, lw=5, zorder=4)
    txt(ax, 3.55, 2.55, 'NO', fs=24, color=RED, ha='center', va='center')
    txt(ax, 3.55, 1.95, 'SWIMMING', fs=19, color=RED, ha='center', va='center')
    txt(ax, 2.8, 1.0, 'after 6 p.m.', fs=20, ha='center', va='center')
    save(f, 21133)


@fig(21134)
def f21134():
    f, ax = board(6.0, 3.8)
    panel(ax, 0.1, 0.1, 5.8, 3.6, fc='#fffaf0')
    txt(ax, 3.0, 3.25, 'City Library  Opening Hours', fs=17, ha='center', va='center')
    grid_table(ax, 0.3, 2.85, [2.4, 3.0], 0.6,
               [['Day', 'Hours'], ['Monday – Friday', '9:00 a.m. – 9:00 p.m.'],
                ['Saturday', '9:00 a.m. – 5:00 p.m.'], ['Sunday', 'Closed']], fs=14)
    save(f, 21134)


@fig(21135)
def f21135():
    f, ax = board(6.4, 3.4)
    panel(ax, 0.1, 0.1, 6.2, 3.2)
    txt(ax, 3.2, 2.9, 'Weather Forecast for Next Week', fs=16, ha='center', va='center')
    data = [('Mon', 'sun', 28), ('Tue', 'cloud', 26), ('Wed', 'rain', 22), ('Thu', 'rain', 20), ('Fri', 'sun', 27)]
    for k, (d, w, t) in enumerate(data):
        x = 0.8 + k * 1.2
        txt(ax, x, 2.35, d, fs=14, ha='center', va='center')
        weather(ax, w, x, 1.45, 0.85)
        txt(ax, x, 0.5, f'{t}°C', fs=14, ha='center', va='center')
    save(f, 21135)


@fig(21136)
def f21136():
    f, ax = board(6.2, 3.6)
    panel(ax, 0.1, 0.1, 6.0, 3.4, fc='#fffaf0')
    txt(ax, 3.1, 3.1, 'Train Timetable (Southbound)', fs=16, ha='center', va='center')
    grid_table(ax, 0.4, 2.75, [1.35, 1.45, 1.45, 1.15], 0.6,
               [['Train', 'Taipei', 'Taichung', 'Tainan'], ['121', '8:00', '9:05', '10:10'],
                ['135', '8:30', '10:15', '11:40'], ['152', '9:10', '10:00', '10:50']], fs=14)
    save(f, 21136)


@fig(21137)
def f21137():
    f, ax = board(5.6, 4.0)
    panel(ax, 0.1, 0.1, 5.4, 3.8, fc='#f3f7fc')
    txt(ax, 2.8, 3.4, 'CITY BOOK FAIR', fs=20, color=BLUE, ha='center', va='center')
    txt(ax, 2.8, 2.85, 'December 12–14   City Hall', fs=14, ha='center', va='center')
    line(ax, [0.6, 5.0], [2.5, 2.5], lw=1.4, color=GREY)
    txt(ax, 2.8, 2.15, 'Tickets', fs=15, ha='center', va='center')
    for k, (a, b) in enumerate([('Adults', '$100'), ('Students', '$60'), ('Children under 6', 'Free')]):
        y = 1.6 - k * 0.5
        txt(ax, 0.9, y, a, fs=14, va='center')
        txt(ax, 4.7, y, b, fs=14, ha='right', va='center')
    save(f, 21137)


@fig(21138)
def f21138():
    f, ax = plt.subplots(figsize=(5.6, 3.8), dpi=200)
    yrs = ['2022', '2023', '2024', '2025']; v = [30, 45, 40, 50]
    ax.bar(yrs, v, width=0.55, color=GRN, edgecolor=INK, lw=1.4, zorder=3)
    ax.set_ylim(0, 60); ax.set_yticks(range(0, 61, 10))
    ax.grid(axis='y', color=LGREY, lw=1, zorder=0)
    ax.set_title('Visitors to Sunshine Zoo', fontproperties=PF, fontsize=15, color=INK)
    ax.set_ylabel('Visitors (thousands)', fontproperties=PF, fontsize=13, color=INK)
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontproperties(PF); lab.set_fontsize(13)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    for sp in ('left', 'bottom'):
        ax.spines[sp].set_linewidth(1.4)
    save(f, 21138)


@fig(21139)
def f21139():
    f, ax = board(6.0, 3.8)
    panel(ax, 0.1, 0.1, 5.8, 3.6, fc='white')
    ax.add_patch(Rectangle((0.1, 2.75), 5.8, 0.95, fc=RED, ec=INK, lw=2.2))
    txt(ax, 3.0, 3.35, 'TODAY ONLY!', fs=15, color='white', ha='center', va='center')
    txt(ax, 3.0, 2.98, 'Everything 20% OFF', fs=17, color='white', ha='center', va='center')
    tshirt(ax, 1.15, 1.65, 0.75)
    tag(ax, 2.35, 1.0, '$300', w=1.25, h=0.55, fs=15)
    # 帽子
    th = np.linspace(0, np.pi, 50)
    ax.fill(4.1 + 0.5 * np.cos(th), 1.5 + 0.5 * np.sin(th), fc='#cfe8d4', ec=INK, lw=2)
    line(ax, [3.6, 5.05], [1.5, 1.5], lw=4)
    tag(ax, 4.6, 1.0, '$200', w=1.25, h=0.55, fs=15)
    txt(ax, 3.0, 0.35, 'Prices on the tags are before the sale.', fs=12, color=GREY, ha='center', va='center')
    save(f, 21139)


READ = [
    dict(id=21130, g=7, unit='wh- 疑問詞問句', d=3, ans=1,
         q="Look at the bus timetable. Amy takes Bus 307 at Park Station, and she has to arrive at Sunny Junior High by 7:50. Which is the latest bus she can take?",
         o=["The 7:05 bus.", "The 7:20 bus.", "The 7:35 bus.", "The 7:50 bus."],
         e="時刻表顯示公車 7:05、7:20、7:35、7:50、8:05 從 Park Station 出發,車程 25 分鐘。7:20 的車 7:45 到校,趕得上 7:50;7:35 的車 8:00 才到,來不及;7:50 那班更晚。7:05 雖然趕得上,但不是「最晚」能搭的一班,所以答案是 7:20。"),
    dict(id=21131, g=8, unit='比較級與最高級', d=1, ans=2,
         q="Look at the menu. Milk tea is ______ drink on the menu.",
         o=["cheaper", "the cheapest", "the most expensive", "more expensive"],
         e="菜單上 Milk Tea 45 元,比紅茶 25 元、綠茶 30 元、檸檬汁 40 元都貴,是最貴的,用最高級 the most expensive。它不是最便宜的(最便宜是紅茶);cheaper、more expensive 是比較級,後面沒有比較對象,也不能接在空格裡修飾 drink。"),
    dict(id=21132, g=8, unit='比較級與最高級', d=2, ans=0,
         q="Look at the chart. Which sentence is true?",
         o=["Ben read as long as David.", "Amy read longer than Cindy.", "David read the longest of the four.", "Cindy read fewer hours than Ben."],
         e="圖中 Amy 6 小時、Ben 4 小時、Cindy 9 小時、David 4 小時。Ben 和 David 都是 4 小時,所以 as long as(一樣久)正確。Amy 6 小時比 Cindy 9 小時少;讀最久的是 Cindy 不是 David;Cindy 9 小時比 Ben 多,不是 fewer。"),
    dict(id=21133, g=8, unit='助動詞 can/must/should', d=1, ans=3,
         q="Look at the sign. Which is true?",
         o=["You can swim here at 7 p.m.", "You must swim here after 6 p.m.", "You can't swim here before 6 p.m.", "You can swim here at 5 p.m."],
         e="告示寫 NO SWIMMING after 6 p.m.,表示晚上 6 點以後禁止游泳,6 點以前可以,所以下午 5 點可以游(can swim at 5 p.m.)。晚上 7 點已經過了 6 點,不能游;告示沒有規定「必須」游泳;6 點以前並沒有禁止。"),
    dict(id=21134, g=8, unit='連接詞與介系詞', d=2, ans=1,
         q="Look at the sign. When can Ken go to the library?",
         o=["At 8 p.m. on Saturday.", "At 7 p.m. on Wednesday.", "At 10 a.m. on Sunday.", "At 8 a.m. on Monday."],
         e="圖書館星期一到五 9:00 a.m.–9:00 p.m. 開放,星期六 9:00 a.m.–5:00 p.m.,星期日休館。星期三晚上 7 點在開放時間內。星期六晚上 8 點已過 5 點閉館;星期日不開;星期一早上 8 點還沒到 9 點開館。"),
    dict(id=21135, g=8, unit='未來式 will 與 be going to', d=1, ans=0,
         q="Look at the weather forecast. What will the weather be like on Tuesday?",
         o=["It will be cloudy.", "It will be sunny.", "It will be rainy.", "It will be snowy."],
         e="氣象預報中 Tue(星期二)的圖示是雲,26°C,所以會是陰天 cloudy。晴天是星期一和星期五,下雨是星期三和星期四;整週都沒有下雪。"),
    dict(id=21136, g=7, unit='wh- 疑問詞問句', d=3, ans=2,
         q="Look at the timetable. Tom gets to Taipei Station at 8:20. He wants to arrive in Tainan as early as possible. Which train should he take?",
         o=["Train 121.", "Train 135.", "Train 152.", "He can't take any train to Tainan."],
         e="Tom 8:20 才到台北站,8:00 開的 121 次已經開走了。剩下 135 次(8:30 開,11:40 到台南)和 152 次(9:10 開,10:50 到台南),152 次雖然較晚出發但較早到台南,所以搭 152 次。還有車可搭,所以「不能搭任何火車」不對。"),
    dict(id=21137, g=7, unit='wh- 疑問詞問句', d=3, ans=3,
         q="Look at the poster. Mr. Lin goes to the book fair with his son and his daughter. His son is a 13-year-old student, and his daughter is 4 years old. How much do they pay in all?",
         o=["$200.", "$220.", "$260.", "$160."],
         e="票價:大人 100 元、學生 60 元、6 歲以下兒童免費。林先生 100 元,13 歲的兒子是學生 60 元,4 歲的女兒免費,共 100 + 60 = 160 元。220 元是把女兒也算成學生票;260 元是把兒子算成大人票;200 元是兩張大人票。"),
    dict(id=21138, g=8, unit='過去式(規則與不規則)', d=2, ans=0,
         q="Look at the chart. Which sentence is true?",
         o=["The zoo had more visitors in 2023 than in 2024.", "The zoo had the most visitors in 2023.",
            "The zoo had fewer visitors in 2025 than in 2024.", "The zoo had the same number of visitors in 2022 and 2024."],
         e="圖中遊客人數:2022 年 3 萬、2023 年 4.5 萬、2024 年 4 萬、2025 年 5 萬。2023 年(4.5 萬)比 2024 年(4 萬)多,正確。最多的是 2025 年不是 2023 年;2025 年比 2024 年多,不是 fewer;2022 年和 2024 年人數不同。"),
    dict(id=21139, g=7, unit='be 動詞與一般動詞現在式', d=3, ans=2,
         q="Look at the sign. Kevin buys one T-shirt and one cap today. How much does he pay?",
         o=["$440.", "$480.", "$400.", "$500."],
         e="價格牌是特價前的價錢:T 恤 300 元、帽子 200 元,共 500 元;今天全部 20% OFF(打八折),500 × 0.8 = 400 元。500 元是沒有打折;440 元是只有 T 恤打折(240 + 200);480 元是 600 打八折,算成兩件 T 恤。"),
]


import re
_CJK = r'[\u3000-\u9fff\uff00-\uffef]'


def zh(t):
    # 中文語境下改用全形標點
    for a, b in ((',', '\uff0c'), (';', '\uff1b'), (':', '\uff1a'), ('(', '\uff08'), (')', '\uff09')):
        t = re.sub(r'(?<=%s)\s*%s\s*' % (_CJK, re.escape(a)), b, t)
        t = re.sub(r'\s*%s\s*(?=%s)' % (re.escape(a), _CJK), b, t)
    t = re.sub(r',\s*', '\uff0c', t)
    t = re.sub(r';\s*', '\uff1b', t)
    t = re.sub(r'\uff08([^()\uff08\uff09]*)\)', '\uff08\\1\uff09', t)
    return t


def build():
    out = []
    for q in LIST:
        o = ordered(q)
        out.append({"id": q['id'], "subject": "英語", "grade": q['g'], "unit": "聽力測驗",
                    "listening": {"script": q['s'], "prompt": P},
                    "stem": "【聽力】" + P + "\n(聽力原文)" + q['s'],
                    "options": [zh(d) for d, _ in o], "answerIndex": q['ans'],
                    "explanation": zh(q['e']), "difficulty": q['d'], "optionFigs": True})
    for q in READ:
        out.append({"id": q['id'], "subject": "英語", "grade": q['g'], "unit": q['unit'],
                    "stem": "看圖回答問題：" + q['q'], "options": q['o'], "answerIndex": q['ans'],
                    "explanation": zh(q['e']), "difficulty": q['d'], "fig": True})
    return out


if __name__ == '__main__':
    p = '/private/tmp/claude-501/-Volumes-FIRECUDA-2T-AI-hs-exam-countdown/237b96d6-dfad-4a39-bcc5-579fabeb0bea/scratchpad/bank15/out/eng_pics.json'
    data = build()
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    import collections
    print(len(data), collections.Counter(q['answerIndex'] for q in data), collections.Counter(q['difficulty'] for q in data))
