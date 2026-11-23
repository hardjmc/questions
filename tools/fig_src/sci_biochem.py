from fig_all import *   # 提供 plt, np, PF(中文字型), fig 裝飾器, new_ax(w,h,equal), save(f, qid), txt(ax,x,y,s,...), dot, circle, arc, INK/RED/BLUE/GREY 顏色
from matplotlib.patches import Ellipse, Rectangle, FancyBboxPatch, Polygon, Circle as MC

GREEN = '#3a8a3a'


def chart(w=6.0, h=4.0):
    f, ax = plt.subplots(figsize=(w, h), dpi=200)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.grid(True, color='#dddddd', lw=0.8)
    ax.set_axisbelow(True)
    return f, ax


def labs(ax, xl, yl, fs=12):
    ax.set_xlabel(xl, fontproperties=PF, fontsize=fs)
    ax.set_ylabel(yl, fontproperties=PF, fontsize=fs)
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_fontproperties(PF)
        t.set_fontsize(11)


def lead(ax, x0, y0, x1, y1, s, fs=13, color=INK, **kw):
    ax.plot([x0, x1], [y0, y1], color=GREY, lw=1.2)
    txt(ax, x1, y1, s, color=color, fs=fs, va='center', **kw)


def ell(ax, x, y, w, h, ang=0, ec=INK, fc='none', lw=1.4):
    ax.add_patch(Ellipse((x, y), w, h, angle=ang, ec=ec, fc=fc, lw=lw))


def box(ax, x, y, w, h, s='', ec=INK, fc='white', fs=13, lw=1.4, color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.08', ec=ec, fc=fc, lw=lw))
    if s:
        txt(ax, x + w / 2, y + h / 2, s, ha='center', va='center', fs=fs, color=color)


def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.5, ms=14):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=ms, shrinkA=0, shrinkB=0))


# ── 41070 植物細胞示意 ──────────────────────────────
def plant_cell(ax, ox, oy, w, h, labels=True):
    ax.add_patch(Rectangle((ox, oy), w, h, ec=INK, fc='none', lw=2.6))            # 細胞壁
    ax.add_patch(Rectangle((ox + 0.12, oy + 0.12), w - 0.24, h - 0.24, ec=INK, fc='none', lw=1.0))  # 細胞膜
    ell(ax, ox + w * 0.58, oy + h * 0.5, w * 0.5, h * 0.62, fc='#eef3fb')       # 液胞
    circle(ax, ox + w * 0.2, oy + h * 0.7, 0.32, lw=1.5)                         # 細胞核
    ax.add_patch(MC((ox + w * 0.2, oy + h * 0.7), 0.1, color=INK))
    for (cx, cy, a) in [(0.18, 0.25, 20), (0.35, 0.12, -10), (0.9, 0.12, 15), (0.9, 0.85, -20), (0.45, 0.88, 10)]:
        ell(ax, ox + w * cx, oy + h * cy, 0.42, 0.2, a, ec=GREEN, fc='#d9eed9', lw=1.3)


@fig(41070)
def f41070():
    f, ax = new_ax(6.0, 3.8)
    plant_cell(ax, 0, 0, 4.0, 2.8)
    lead(ax, 4.0, 1.55, 4.7, 1.7, '甲')
    lead(ax, 4.0 * 0.9 + 0.2, 2.8 * 0.85, 4.7, 2.6, '乙')
    lead(ax, 4.0 * 0.7, 2.8 * 0.45, 4.7, 0.8, '丙')
    lead(ax, 0.8, 2.8 * 0.7, -0.7, 1.4, '丁')
    ax.set_xlim(-1.0, 5.2); ax.set_ylim(-0.2, 3.0)
    save(f, 41070)


# ── 41071 兩種細胞 ──────────────────────────────
@fig(41071)
def f41071():
    f, ax = new_ax(6.4, 3.4)
    # 甲:植物細胞
    plant_cell(ax, 0, 0, 2.6, 2.2)
    txt(ax, 1.3, -0.45, '甲', ha='center', fs=14)
    # 乙:動物細胞
    ell(ax, 4.6, 1.1, 2.6, 2.0, lw=1.2)
    circle(ax, 4.5, 1.2, 0.32, lw=1.5)
    ax.add_patch(MC((4.5, 1.2), 0.1, color=INK))
    txt(ax, 4.6, -0.45, '乙', ha='center', fs=14)
    ax.set_xlim(-0.3, 6.2); ax.set_ylim(-0.7, 2.4)
    save(f, 41071)


# ── 41072 顯微鏡視野(物像在右上方)──────────────
@fig(41072)
def f41072():
    f, ax = new_ax(5.2, 3.6)
    circle(ax, 0, 0, 1.5, lw=1.8)
    ax.plot([-1.5, 1.5], [0, 0], color=GREY, lw=1.0, ls='--')
    ax.plot([0, 0], [-1.5, 1.5], color=GREY, lw=1.0, ls='--')
    ell(ax, 0.75, 0.72, 0.5, 0.34, 20, ec=RED, fc='#f7d9d7', lw=1.6)
    ax.add_patch(MC((0.75, 0.72), 0.07, color=RED))
    txt(ax, 1.75, 0.0, '視野', fs=13, va='center')
    ax.set_xlim(-1.7, 2.4); ax.set_ylim(-1.6, 1.6)
    save(f, 41072)


# ── 41073 視野中一排細胞 ────────────────────────
@fig(41073)
def f41073():
    f, ax = new_ax(5.6, 3.6)
    circle(ax, 0, 0, 1.6, lw=1.8)
    n = 8
    wcell = 3.2 / n
    for i in range(n):
        x = -1.6 + wcell * i
        ax.add_patch(Rectangle((x, -0.18), wcell, 0.36, ec=INK, fc='#eef3fb', lw=1.2))
        ax.add_patch(MC((x + wcell / 2, 0), 0.05, color=INK))
    txt(ax, 0, -2.05, '接目鏡 10×、接物鏡 10×', ha='center', fs=13)
    ax.set_xlim(-2.0, 2.0); ax.set_ylim(-2.3, 1.7)
    save(f, 41073)


# ── 41074 細胞內外氣體濃度 ──────────────────────
@fig(41074)
def f41074():
    f, ax = new_ax(6.0, 3.4)
    ell(ax, 0, 0, 2.6, 1.8, lw=1.6, fc='#eef3fb')
    txt(ax, 0, 0.35, '細胞內', ha='center', fs=13)
    txt(ax, 0, -0.1, '氧氣:2', ha='center', fs=13, color=BLUE)
    txt(ax, 0, -0.5, '二氧化碳:7', ha='center', fs=13, color=RED)
    txt(ax, 2.6, 0.45, '細胞外', ha='center', fs=13)
    txt(ax, 2.6, 0.0, '氧氣:9', ha='center', fs=13, color=BLUE)
    txt(ax, 2.6, -0.4, '二氧化碳:1', ha='center', fs=13, color=RED)
    txt(ax, 0.9, -1.35, '(數字為相對濃度)', ha='center', fs=12, color=GREY)
    ax.set_xlim(-1.5, 3.6); ax.set_ylim(-1.6, 1.0)
    save(f, 41074)


# ── 41075 光照強度與產氧速率 ────────────────────
LUX = np.array([0, 1, 2, 3, 4, 5, 6])
O2R = np.array([-2, 4, 10, 14, 14, 14, 14])


@fig(41075)
def f41075():
    f, ax = chart(6.0, 3.8)
    ax.plot(LUX, O2R, color=BLUE, lw=2, marker='o', ms=5)
    ax.axhline(0, color=INK, lw=1.2)
    ax.set_xticks(LUX); ax.set_yticks(range(-4, 17, 2))
    ax.set_ylim(-4, 16.5)
    labs(ax, '光照強度(千勒克斯)', '氧氣釋放速率(相對值)')
    save(f, 41075)


# ── 41076 密閉溫室 24 小時 CO2 濃度 ─────────────
HRS = np.arange(0, 25, 2)
CO2 = np.array([440, 460, 480, 490, 470, 420, 380, 350, 335, 330, 360, 400, 430])


@fig(41076)
def f41076():
    f, ax = chart(6.4, 3.8)
    ax.plot(HRS, CO2, color=RED, lw=2, marker='o', ms=4)
    ax.set_xticks(range(0, 25, 2))
    ax.set_ylim(300, 510)
    labs(ax, '時刻(時)', '二氧化碳濃度(ppm)')
    save(f, 41076)


# ── 41077 燈距與氣泡數 ──────────────────────────
DIST = np.array([10, 20, 30, 40, 50])
BUB = np.array([60, 34, 18, 9, 4])


@fig(41077)
def f41077():
    f, ax = chart(6.0, 3.8)
    ax.plot(DIST, BUB, color=GREEN, lw=2, marker='o', ms=5)
    for x, y in zip(DIST, BUB):
        txt(ax, x + 1, y + 2.5, str(y), fs=12)
    ax.set_xticks(DIST); ax.set_xlim(5, 55); ax.set_ylim(0, 70)
    labs(ax, '燈泡與水蘊草的距離(公分)', '每分鐘氣泡數(個)')
    save(f, 41077)


# ── 41078 斑葉遮光實驗 ──────────────────────────
@fig(41078)
def f41078():
    f, ax = new_ax(6.0, 3.6)
    th = np.linspace(0, 2 * np.pi, 300)
    X, Y = 2.6 * np.cos(th), 1.3 * np.sin(th)
    ax.fill(X, Y, color='white', ec=INK, lw=1.6)
    # 內部綠色區(邊緣白色無葉綠素)
    ax.fill(2.1 * np.cos(th), 0.85 * np.sin(th), color='#cfe8cf', ec=GREEN, lw=1.2)
    # 遮光鋁箔帶
    ax.add_patch(Rectangle((-0.5, -1.45), 1.0, 2.9, ec=INK, fc='#bbbbbb', lw=1.4, hatch='//', alpha=0.9))
    ax.plot([2.6, 3.2], [0, 0], color=INK, lw=2)   # 葉柄
    txt(ax, -1.4, 0, '甲', ha='center', va='center', fs=14)
    txt(ax, 0, 0, '乙', ha='center', va='center', fs=14, bbox=dict(fc='white', ec='none', pad=1))
    txt(ax, -2.35, -0.05, '丙', ha='center', va='center', fs=13)
    lead(ax, 0.3, 1.2, 1.2, 1.75, '鋁箔(遮光)', fs=12)
    lead(ax, 1.9, -0.95, 2.6, -1.55, '白色部分(無葉綠素)', fs=12)
    lead(ax, 1.4, -0.4, 3.0, -0.75, '綠色部分', fs=12)
    ax.set_xlim(-2.8, 5.6); ax.set_ylim(-1.8, 1.9)
    save(f, 41078)


# ── 41079 兩種酵素活性與溫度 ────────────────────
def enz(t, peak, width):
    return 100 * np.exp(-((t - peak) / width) ** 2)


@fig(41079)
def f41079():
    f, ax = chart(6.0, 3.8)
    t = np.linspace(0, 90, 400)
    a = np.where(t < 37, enz(t, 37, 22), enz(t, 37, 12))
    b = np.where(t < 70, enz(t, 70, 22), enz(t, 70, 9))
    ax.plot(t, a, color=BLUE, lw=2)
    ax.plot(t, b, color=RED, lw=2, ls='--')
    txt(ax, 22, 85, '甲', color=BLUE, fs=14)
    txt(ax, 76, 85, '乙', color=RED, fs=14)
    ax.set_xticks(range(0, 91, 10)); ax.set_ylim(0, 110)
    labs(ax, '溫度(℃)', '酵素活性(相對值)')
    save(f, 41079)


# ── 41080 心臟四腔室示意 ────────────────────────
@fig(41080)
def f41080():
    f, ax = new_ax(5.6, 3.8)
    box(ax, 0, 1.7, 1.6, 1.1, '甲', fs=15)
    box(ax, 1.9, 1.7, 1.6, 1.1, '乙', fs=15)
    box(ax, 0, 0, 1.6, 1.5, '丙', fs=15)
    box(ax, 1.9, 0, 1.6, 1.5, '丁', fs=15)
    txt(ax, 1.75, 3.15, '(心臟正面觀,觀察者面對受測者)', ha='center', fs=12, color=GREY)
    txt(ax, -0.35, 1.4, '受測者\n的右側', ha='right', va='center', fs=12)
    txt(ax, 3.85, 1.4, '受測者\n的左側', ha='left', va='center', fs=12)
    ax.set_xlim(-1.6, 5.1); ax.set_ylim(-0.2, 3.4)
    save(f, 41080)


# ── 41081/41082 血液循環示意 ────────────────────
def circulation(qid):
    f, ax = new_ax(6.0, 4.4)
    box(ax, 0.9, 3.4, 2.2, 0.75, '肺部微血管', fs=13)
    box(ax, 0.9, -0.5, 2.2, 0.75, '全身微血管', fs=13)
    box(ax, 0.6, 1.75, 1.3, 0.55, '右心房', fs=12)
    box(ax, 2.1, 1.75, 1.3, 0.55, '左心房', fs=12)
    box(ax, 0.6, 1.0, 1.3, 0.65, '右心室', fs=12)
    box(ax, 2.1, 1.0, 1.3, 0.65, '左心室', fs=12)
    # A:右心室→肺
    ax.plot([0.6, 0.0, 0.0], [1.3, 1.3, 3.75], color=BLUE, lw=1.8)
    arrow(ax, 0.0, 3.75, 0.88, 3.75, color=BLUE)
    txt(ax, -0.35, 2.6, 'A', fs=15, va='center')
    # B:肺→左心房
    ax.plot([3.1, 4.0, 4.0], [3.75, 3.75, 2.05], color=BLUE, lw=1.8)
    arrow(ax, 4.0, 2.05, 3.42, 2.05, color=BLUE)
    txt(ax, 4.15, 2.9, 'B', fs=15, va='center')
    # C:左心室→全身
    ax.plot([3.4, 4.5, 4.5], [1.3, 1.3, -0.12], color=BLUE, lw=1.8)
    arrow(ax, 4.5, -0.12, 3.12, -0.12, color=BLUE)
    txt(ax, 4.65, 0.6, 'C', fs=15, va='center')
    # D:全身→右心房
    ax.plot([0.9, -0.5, -0.5], [-0.12, -0.12, 2.05], color=BLUE, lw=1.8)
    arrow(ax, -0.5, 2.05, 0.58, 2.05, color=BLUE)
    txt(ax, -0.85, 0.6, 'D', fs=15, va='center')
    ax.set_xlim(-1.1, 5.0); ax.set_ylim(-0.7, 4.3)
    save(f, qid)


@fig(41081)
def f41081():
    circulation(41081)


@fig(41082)
def f41082():
    circulation(41082)


# ── 41083 蒸散作用實驗 ──────────────────────────
TH = np.arange(0, 7)
W_A = np.array([0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0])
W_B = np.array([0, 0.2, 0.3, 0.5, 0.7, 0.8, 1.0])
W_C = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])


@fig(41083)
def f41083():
    f, ax = chart(6.0, 3.8)
    ax.plot(TH, W_A, color=BLUE, lw=2, marker='o', ms=4)
    ax.plot(TH, W_B, color=INK, lw=2, marker='s', ms=4)
    ax.plot(TH, W_C, color=RED, lw=2, marker='^', ms=5)
    txt(ax, 6.1, 12, '甲', color=BLUE, fs=14, va='center')
    txt(ax, 6.1, 0.6, '乙', color=INK, fs=14, va='center')
    txt(ax, 6.1, 3.4, '丙', color=RED, fs=14, va='center')
    ax.set_xticks(TH); ax.set_yticks(range(0, 15, 2)); ax.set_xlim(0, 6.6); ax.set_ylim(0, 13.5)
    labs(ax, '時間(小時)', '水分減少量(毫升)')
    save(f, 41083)


# ── 41084 血管總截面積與血流速率 ────────────────
@fig(41084)
def f41084():
    f, ax = chart(6.4, 3.8)
    # 用分段直觀數值(相對值):甲 小、乙 很大、丙 中
    xs = [0, 0.8, 1.2, 1.8, 2.2, 3.0]
    area = [1, 1.5, 9, 9, 2.5, 2.0]
    speed = [9, 7, 1, 1, 3.5, 4.5]
    ax.plot(xs, area, color=BLUE, lw=2)
    ax.plot(xs, speed, color=RED, lw=2, ls='--')
    txt(ax, 2.35, 1.4, '總截面積', color=BLUE, fs=12)
    txt(ax, 0.05, 9.6, '血流速率', color=RED, fs=12)
    for xv in (1.0, 2.0):
        ax.axvline(xv, color=GREY, lw=1.0, ls=':')
    ax.set_xticks([0.5, 1.5, 2.5]); ax.set_xticklabels(['甲', '乙', '丙'])
    ax.set_yticks([]); ax.set_xlim(0, 3); ax.set_ylim(0, 11)
    labs(ax, '血管種類', '相對值')
    for t in ax.get_xticklabels():
        t.set_fontsize(14)
    save(f, 41084)


# ── 譜系圖工具 ──────────────────────────────────
def person(ax, x, y, male, aff, label=None, s=0.5, qmark=False):
    if male:
        ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, ec=INK, fc=INK if aff else 'white', lw=1.6))
    else:
        ax.add_patch(MC((x, y), s / 2, ec=INK, fc=INK if aff else 'white', lw=1.6))
    if qmark:
        txt(ax, x, y, '?', ha='center', va='center', fs=14, color=RED)
    if label:
        txt(ax, x, y - s / 2 - 0.3, label, ha='center', va='center', fs=12)


def couple(ax, x1, x2, y, kids_x, ky):
    ax.plot([x1, x2], [y, y], color=INK, lw=1.5)
    mx = (x1 + x2) / 2
    ax.plot([mx, mx], [y, (y + ky) / 2], color=INK, lw=1.5)
    ax.plot([min(kids_x), max(kids_x)], [(y + ky) / 2] * 2, color=INK, lw=1.5)
    for k in kids_x:
        ax.plot([k, k], [(y + ky) / 2, ky + 0.25], color=INK, lw=1.5)


def legend_ped(ax, x, y):
    person(ax, x, y, True, False, s=0.36); txt(ax, x + 0.35, y, '正常男性', va='center', fs=12)
    person(ax, x, y - 0.55, False, False, s=0.36); txt(ax, x + 0.35, y - 0.55, '正常女性', va='center', fs=12)
    person(ax, x, y - 1.1, True, True, s=0.36); txt(ax, x + 0.35, y - 1.1, '患病男性', va='center', fs=12)
    person(ax, x, y - 1.65, False, True, s=0.36); txt(ax, x + 0.35, y - 1.65, '患病女性', va='center', fs=12)


@fig(41085)
def f41085():
    f, ax = new_ax(6.0, 3.6)
    person(ax, 0, 2, True, False, '1'); person(ax, 1.6, 2, False, False, '2')
    couple(ax, 0.25, 1.35, 2, [0, 0.8, 1.6], 0.4)
    person(ax, 0, 0.4, True, False, '3'); person(ax, 0.8, 0.4, False, True, '4'); person(ax, 1.6, 0.4, True, False, '5')
    txt(ax, -0.8, 2, 'I', va='center', fs=13); txt(ax, -0.8, 0.4, 'II', va='center', fs=13)
    legend_ped(ax, 3.0, 2.3)
    ax.set_xlim(-1.0, 4.8); ax.set_ylim(-0.3, 2.6)
    save(f, 41085)


@fig(41086)
def f41086():
    f, ax = new_ax(6.0, 3.6)
    person(ax, 0, 2, True, True, '1'); person(ax, 1.6, 2, False, False, '2')
    couple(ax, 0.25, 1.35, 2, [0, 0.8, 1.6], 0.4)
    person(ax, 0, 0.4, False, True, '3'); person(ax, 0.8, 0.4, True, False, '4'); person(ax, 1.6, 0.4, False, False, '5')
    txt(ax, -0.8, 2, 'I', va='center', fs=13); txt(ax, -0.8, 0.4, 'II', va='center', fs=13)
    legend_ped(ax, 3.0, 2.3)
    ax.set_xlim(-1.0, 4.8); ax.set_ylim(-0.3, 2.6)
    save(f, 41086)


@fig(41087)
def f41087():
    f, ax = new_ax(6.4, 4.0)
    person(ax, 0, 3.2, True, False, '1'); person(ax, 1.6, 3.2, False, False, '2')
    couple(ax, 0.25, 1.35, 3.2, [0.4, 1.6], 1.6)
    person(ax, 0.4, 1.6, False, True, '3'); person(ax, 1.6, 1.6, True, False, '4')
    person(ax, 3.0, 1.6, False, True, '5')
    couple(ax, 1.85, 2.75, 1.6, [2.3], 0.0)
    person(ax, 2.3, 0.0, True, False, '6', qmark=True)
    txt(ax, -0.8, 3.2, 'I', va='center', fs=13); txt(ax, -0.8, 1.6, 'II', va='center', fs=13); txt(ax, -0.8, 0.0, 'III', va='center', fs=13)
    legend_ped(ax, 4.0, 3.4)
    ax.set_xlim(-1.0, 5.8); ax.set_ylim(-0.7, 3.6)
    save(f, 41087)


# ── 41088 棋盤方格 ──────────────────────────────
def punnett2(qid, top, left, cells, top_title, left_title):
    f, ax = new_ax(5.4, 3.8)
    cw, ch = 1.4, 0.8
    # 格線
    for k in range(4):
        y = ch - k * ch
        ax.plot([-cw if k > 0 else 0, 2 * cw], [y, y], color=INK, lw=1.5)
    for k in range(4):
        x = -cw + k * cw
        ax.plot([x, x], [ch if k > 0 else 0, -2 * ch], color=INK, lw=1.5)
    for j, g in enumerate(top):
        txt(ax, cw / 2 + j * cw, ch / 2, g, ha='center', va='center', fs=15, color=BLUE)
    for i, g in enumerate(left):
        txt(ax, -cw / 2, -ch / 2 - i * ch, g, ha='center', va='center', fs=15, color=RED)
    for i in range(2):
        for j in range(2):
            txt(ax, cw / 2 + j * cw, -ch / 2 - i * ch, cells[i][j], ha='center', va='center', fs=15)
    txt(ax, cw, ch + 0.35, top_title, ha='center', va='center', fs=12, color=BLUE)
    txt(ax, -cw - 0.2, -ch, left_title, ha='right', va='center', fs=12, color=RED)
    ax.set_xlim(-cw - 1.6, 2 * cw + 0.2); ax.set_ylim(-2 * ch - 0.2, ch + 0.65)
    save(f, qid)


@fig(41088)
def f41088():
    punnett2(41088, ['A', 'a'], ['A', 'a'], [['甲', '乙'], ['丙', '丁']], '父親的精子', '母親的\n卵')


@fig(41089)
def f41089():
    punnett2(41089, ['X', 'Y'], ['X', 'X'], [['甲', '乙'], ['丙', '丁']], '父親的精子', '母親的\n卵')


@fig(41090)
def f41090():
    f, ax = new_ax(5.6, 3.4)
    person(ax, 0, 1.8, True, False, '父'); person(ax, 1.8, 1.8, False, False, '母')
    couple(ax, 0.25, 1.55, 1.8, [0.9], 0.2)
    person(ax, 0.9, 0.2, True, False, '兒子')
    txt(ax, 0, 2.35, 'A 型', ha='center', fs=13, color=BLUE)
    txt(ax, 1.8, 2.35, 'B 型', ha='center', fs=13, color=BLUE)
    txt(ax, 1.3, 0.2, 'O 型', va='center', fs=13, color=BLUE)
    ax.set_xlim(-1.3, 3.6); ax.set_ylim(-0.4, 2.7)
    save(f, 41090)


# ── 食物網 ──────────────────────────────────────
def foodweb(ax, nodes, edges, fs=13):
    for a, b in edges:
        (x0, y0), (x1, y1) = nodes[a], nodes[b]
        v = np.array([x1 - x0, y1 - y0]); d = np.linalg.norm(v); u = v / d
        arrow(ax, x0 + u[0] * 0.35, y0 + u[1] * 0.28, x1 - u[0] * 0.4, y1 - u[1] * 0.3, color=INK, lw=1.4)
    for k, (x, y) in nodes.items():
        txt(ax, x, y, k, ha='center', va='center', fs=fs, bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=BLUE, lw=1.3))


WEB1 = {'草': (2, 0), '兔': (0, 1.3), '鼠': (2, 1.3), '蚱蜢': (4, 1.0), '青蛙': (4, 2.2), '蛇': (3, 3.2), '鷹': (1, 4.0)}
WEB1E = [('草', '兔'), ('草', '鼠'), ('草', '蚱蜢'), ('蚱蜢', '青蛙'), ('鼠', '蛇'), ('青蛙', '蛇'), ('兔', '鷹'), ('鼠', '鷹'), ('蛇', '鷹')]


@fig(41091)
def f41091():
    f, ax = new_ax(5.2, 4.0)
    foodweb(ax, WEB1, WEB1E)
    ax.set_xlim(-0.6, 4.7); ax.set_ylim(-0.4, 4.4)
    save(f, 41091)


@fig(41092)
def f41092():
    f, ax = new_ax(5.2, 4.0)
    foodweb(ax, WEB1, WEB1E)
    ax.set_xlim(-0.6, 4.7); ax.set_ylim(-0.4, 4.4)
    save(f, 41092)


@fig(41093)
def f41093():
    f, ax = new_ax(5.6, 4.0)
    nodes = {'藻類': (2, 0), '浮游動物': (0.5, 1.4), '螺': (3.5, 1.4), '小魚': (0.5, 2.8), '螃蟹': (3.5, 2.8), '白鷺': (2, 4.0)}
    edges = [('藻類', '浮游動物'), ('藻類', '螺'), ('浮游動物', '小魚'), ('螺', '螃蟹'), ('小魚', '白鷺'), ('螃蟹', '白鷺')]
    foodweb(ax, nodes, edges)
    ax.set_xlim(-0.6, 4.4); ax.set_ylim(-0.4, 4.4)
    save(f, 41093)


# ── 41094 族群成長曲線 ──────────────────────────
DAY = np.arange(0, 13)
POP = np.round(500 / (1 + 49 * np.exp(-1.0 * DAY)))


@fig(41094)
def f41094():
    f, ax = chart(6.0, 3.8)
    ax.plot(DAY, POP, color=BLUE, lw=2, marker='o', ms=4)
    ax.set_xticks(DAY); ax.set_yticks(range(0, 601, 100)); ax.set_ylim(0, 600)
    labs(ax, '培養天數(天)', '草履蟲數量(隻/毫升)')
    save(f, 41094)


# ── 41095 掠食者與獵物 ──────────────────────────
@fig(41095)
def f41095():
    f, ax = chart(6.4, 3.8)
    t = np.linspace(0, 20, 400)
    a = 100 + 60 * np.sin(2 * np.pi * t / 10)
    b = 30 + 15 * np.sin(2 * np.pi * (t - 2.5) / 10)
    ax.plot(t, a, color=BLUE, lw=2)
    ax.plot(t, b, color=RED, lw=2, ls='--')
    txt(ax, 2.0, 168, '甲', color=BLUE, fs=14)
    txt(ax, 4.6, 52, '乙', color=RED, fs=14)
    ax.set_xticks(range(0, 21, 2)); ax.set_ylim(0, 185)
    labs(ax, '時間(年)', '族群數量(隻)')
    save(f, 41095)


# ── 溶解度曲線 ──────────────────────────────────
T = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80])
KNO3 = np.array([13, 21, 32, 46, 64, 85, 110, 138, 169])
NACL = np.array([36, 36, 36, 36, 37, 37, 37, 38, 38])


def sol_chart(qid, nacl=True, mark=None):
    f, ax = chart(6.0, 4.2)
    tt = np.linspace(0, 80, 300)
    from numpy.polynomial import polynomial as P
    ax.plot(tt, np.interp(tt, T, KNO3), color=BLUE, lw=2)
    ax.plot(T, KNO3, 'o', color=BLUE, ms=4)
    txt(ax, 62, 150, '硝酸鉀', color=BLUE, fs=13)
    if nacl:
        ax.plot(T, NACL, color=RED, lw=2, ls='--')
        txt(ax, 64, 20, '氯化鈉', color=RED, fs=13)
    ax.set_xticks(range(0, 81, 10)); ax.set_yticks(range(0, 181, 20)); ax.set_xlim(0, 82); ax.set_ylim(0, 180)
    labs(ax, '溫度(℃)', '溶解度(公克/100 公克水)')
    return f, ax


@fig(41096)
def f41096():
    f, ax = sol_chart(41096)
    save(f, 41096)


@fig(41097)
def f41097():
    f, ax = sol_chart(41097, nacl=False)
    for t0, v in ((20, 32), (60, 110)):
        txt(ax, t0 - 3, v + 7, str(v), fs=12, color=BLUE)
    save(f, 41097)


@fig(41098)
def f41098():
    f, ax = sol_chart(41098)
    save(f, 41098)


@fig(41099)
def f41099():
    f, ax = sol_chart(41099, nacl=False)
    txt(ax, 34, 70, '64', fs=12, color=BLUE)
    save(f, 41099)


# ── 41100 粒子模型 ──────────────────────────────
def atom(ax, x, y, kind, r=0.13):
    if kind == 'B':
        ax.add_patch(MC((x, y), r, color=INK))
    else:
        ax.add_patch(MC((x, y), r, ec=INK, fc='white', lw=1.3))


def mol(ax, x, y, kinds, ang=0, r=0.13):
    n = len(kinds)
    if n == 1:
        atom(ax, x, y, kinds[0], r); return
    u = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang))]) * r * 0.95
    for i, k in enumerate(kinds):
        o = (i - (n - 1) / 2) * 2
        atom(ax, x + u[0] * o, y + u[1] * o, k, r)


@fig(41100)
def f41100():
    f, ax = new_ax(6.4, 3.6)
    boxes = [
        ('甲', [('BB', 0.3, 0.3, 20), ('BB', 0.9, 0.5, -30), ('BB', 0.4, 0.95, 60), ('BB', 1.0, 1.05, 0)]),
        ('乙', [('BWB', 0.45, 0.25, 0), ('BWB', 0.45, 1.1, 0), ('BWB', 1.07, 0.68, 90), ('BWB', 0.42, 0.68, 0)]),
        ('丙', [('BB', 0.3, 0.3, 20), ('WW', 0.95, 0.4, -30), ('BB', 0.4, 0.95, 70), ('WW', 1.0, 1.05, 10)]),
        ('丁', [('BW', 0.3, 0.3, 20), ('BW', 0.95, 0.4, -30), ('W', 0.45, 0.95, 0), ('W', 1.05, 1.0, 0)]),
    ]
    for i, (name, ms) in enumerate(boxes):
        ox = i * 1.65
        ax.add_patch(Rectangle((ox, 0), 1.35, 1.35, ec=INK, fc='none', lw=1.4))
        for kinds, x, y, a in ms:
            mol(ax, ox + x, y, list(kinds), a)
        txt(ax, ox + 0.675, -0.3, name, ha='center', va='center', fs=14)
    atom(ax, 1.5, -0.85, 'B'); txt(ax, 1.7, -0.85, 'X 原子', va='center', fs=12)
    atom(ax, 3.3, -0.85, 'W'); txt(ax, 3.5, -0.85, 'Y 原子', va='center', fs=12)
    ax.set_xlim(-0.1, 6.4); ax.set_ylim(-1.1, 1.5)
    save(f, 41100)


# ── 41101 蒸餾裝置 ──────────────────────────────
@fig(41101)
def f41101():
    f, ax = new_ax(6.4, 3.8)
    # 蒸餾瓶(圓底燒瓶)
    th = np.linspace(np.radians(104), np.radians(104) + 2 * np.pi - np.radians(28), 200)
    ax.plot(0.75 * np.cos(th), 0.75 * np.sin(th), color=INK, lw=1.6)
    xs = np.linspace(-0.62, 0.62, 60)
    ax.fill_between(xs, -0.25, -np.sqrt(np.maximum(0.5625 - xs ** 2, 0)), color='#d6e4f5')
    ax.plot([-0.18, -0.18], [0.73, 2.05], color=INK, lw=1.6)          # 瓶頸
    ax.plot([0.18, 0.18], [0.73, 1.52], color=INK, lw=1.6)
    ax.plot([0.18, 0.18], [1.68, 2.05], color=INK, lw=1.6)
    ax.add_patch(Rectangle((-0.24, 2.05), 0.48, 0.2, ec=INK, fc='#888888', lw=1.2))  # 塞子
    # 支管 → 冷凝管內管
    p0 = np.array([0.18, 1.6]); p1 = np.array([4.1, 0.15])
    u = (p1 - p0) / np.linalg.norm(p1 - p0); n = np.array([-u[1], u[0]])
    L = np.linalg.norm(p1 - p0)
    for off in (0.08, -0.08):
        q0, q1 = p0 + n * off, p1 + n * off
        ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color=INK, lw=1.3)
    # 冷凝管外管(封閉)
    s0, s1, w = 0.9, L - 0.75, 0.28
    jac = [p0 + u * s0 + n * w, p0 + u * s1 + n * w, p0 + u * s1 - n * w, p0 + u * s0 - n * w]
    ax.add_patch(Polygon(jac, closed=True, ec=INK, fc='#eef4fb', lw=1.6, zorder=1))
    # 進出水口:乙 在上端(靠蒸餾瓶)上側,甲 在下端(靠錐形瓶)下側
    up = p0 + u * (s0 + 0.35) + n * w
    dn = p0 + u * (s1 - 0.35) - n * w
    ax.plot([up[0], up[0]], [up[1], up[1] + 0.4], color=INK, lw=2.2)
    ax.plot([dn[0], dn[0]], [dn[1], dn[1] - 0.4], color=INK, lw=2.2)
    txt(ax, up[0] + 0.15, up[1] + 0.4, '乙', fs=14, va='center')
    txt(ax, dn[0] + 0.15, dn[1] - 0.42, '甲', fs=14, va='center')
    lead(ax, *(p0 + u * 2.3 + n * w * 0.6), 3.3, 1.65, '冷凝管', fs=12)
    # 溫度計:球部在支管口
    ax.plot([0, 0], [1.6, 2.75], color=RED, lw=1.8)
    ax.add_patch(MC((0, 1.6), 0.07, color=RED))
    lead(ax, 0.03, 2.55, 0.6, 2.6, '溫度計', fs=12)
    # 錐形瓶
    ax.add_patch(Polygon([[3.95, -0.05], [4.25, -0.05], [4.65, -1.05], [3.55, -1.05]], closed=True, ec=INK, fc='none', lw=1.5))
    txt(ax, 4.1, -1.32, '錐形瓶', ha='center', va='center', fs=12)
    # 加熱
    txt(ax, 0, -1.15, '加熱', ha='center', fs=12, color=RED)
    ax.set_xlim(-1.0, 5.0); ax.set_ylim(-1.55, 2.85)
    save(f, 41101)


# ── 41102 開口坩堝加熱鎂帶 ──────────────────────
@fig(41102)
def f41102():
    f, ax = chart(6.0, 3.8)
    t = np.linspace(0, 10, 200)
    up = 3.2 + 0.9 * (1 - np.exp(-t / 2))
    dn = 3.2 - 0.9 * (1 - np.exp(-t / 2))
    flat = np.full_like(t, 3.2)
    ax.plot(t, up, color=BLUE, lw=2); txt(ax, 10.2, up[-1], '甲', color=BLUE, fs=14, va='center')
    ax.plot(t, flat, color=INK, lw=2, ls='-.'); txt(ax, 10.2, 3.2, '乙', fs=14, va='center')
    ax.plot(t, dn, color=RED, lw=2, ls='--'); txt(ax, 10.2, dn[-1], '丙', color=RED, fs=14, va='center')
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 11); ax.set_ylim(1.8, 4.6)
    labs(ax, '加熱時間', '坩堝內固體質量')
    save(f, 41102)


# ── 41103 反應前粒子 ────────────────────────────
@fig(41103)
def f41103():
    f, ax = new_ax(6.0, 3.0)
    ax.add_patch(Rectangle((0, 0), 2.4, 1.8, ec=INK, fc='none', lw=1.5))
    for x, y, a in [(0.4, 0.4, 0), (1.2, 0.3, 30), (2.0, 0.5, -20), (0.6, 1.3, 60)]:
        mol(ax, x, y, ['W', 'W'], a, r=0.12)
    for x, y, a in [(1.6, 1.1, -30), (2.0, 1.5, 10), (0.95, 0.85, 0)]:
        mol(ax, x, y, ['B', 'B'], a, r=0.15)
    txt(ax, 1.2, -0.3, '反應前', ha='center', va='center', fs=13)
    arrow(ax, 2.7, 0.9, 3.5, 0.9, lw=1.8)
    ax.add_patch(Rectangle((3.8, 0), 2.4, 1.8, ec=INK, fc='none', lw=1.5, ls='--'))
    txt(ax, 5.0, 0.9, '?', ha='center', va='center', fs=20, color=RED)
    txt(ax, 5.0, -0.3, '反應後', ha='center', va='center', fs=13)
    atom(ax, 0.6, -0.8, 'W', r=0.12); txt(ax, 0.8, -0.8, '氫原子', va='center', fs=12)
    atom(ax, 2.6, -0.8, 'B', r=0.15); txt(ax, 2.82, -0.8, '氧原子', va='center', fs=12)
    ax.set_xlim(-0.2, 6.4); ax.set_ylim(-1.05, 2.0)
    save(f, 41103)


# ── 41104 銅粉加熱質量 ──────────────────────────
@fig(41104)
def f41104():
    f, ax = chart(6.0, 3.8)
    t = np.array([0, 2, 4, 6, 8, 10, 12])
    m = np.array([4.0, 4.5, 4.8, 4.95, 5.0, 5.0, 5.0])
    ax.plot(t, m, color=BLUE, lw=2, marker='o', ms=4)
    ax.set_xticks(t); ax.set_yticks(np.arange(3.8, 5.31, 0.2)); ax.set_ylim(3.8, 5.3)
    ax.set_yticklabels([f'{v:.1f}' for v in np.arange(3.8, 5.31, 0.2)])
    labs(ax, '加熱時間(分鐘)', '固體質量(公克)')
    save(f, 41104)


# ── 41105 密閉瓶與天平 ──────────────────────────
@fig(41105)
def f41105():
    f, ax = new_ax(5.6, 3.8)
    ax.add_patch(Rectangle((-1.6, -0.3), 3.2, 0.3, ec=INK, fc='#eeeeee', lw=1.5))   # 天平
    ax.add_patch(Rectangle((-1.8, -1.1), 3.6, 0.8, ec=INK, fc='white', lw=1.5))
    ax.add_patch(Rectangle((-0.75, -0.95), 1.5, 0.5, ec=INK, fc='white', lw=1.3))
    txt(ax, 0, -0.7, '120.0 g', ha='center', va='center', fs=13, color=RED)
    # 瓶子
    ax.add_patch(Rectangle((-0.6, 0), 1.2, 1.4, ec=INK, fc='none', lw=1.6))
    ax.add_patch(Rectangle((-0.3, 1.4), 0.6, 0.35, ec=INK, fc='none', lw=1.6))
    ax.add_patch(Rectangle((-0.36, 1.75), 0.72, 0.18, ec=INK, fc=INK, lw=1.2))   # 瓶蓋
    # 小試管(內裝稀鹽酸)
    ax.add_patch(Rectangle((0.05, 0.25), 0.25, 0.95, ec=BLUE, fc='none', lw=1.4, angle=12))
    ax.add_patch(Rectangle((0.05, 0.25), 0.25, 0.55, ec='none', fc='#d6e4f5', angle=12, zorder=0))
    for x in (-0.4, -0.2, -0.35):
        pass
    for (x, y) in [(-0.4, 0.1), (-0.15, 0.12), (-0.3, 0.25)]:
        ax.add_patch(MC((x, y), 0.08, ec=INK, fc='#cccccc', lw=1))
    lead(ax, 0.25, 1.0, 1.1, 1.5, '小試管(稀鹽酸)', fs=12)
    lead(ax, -0.35, 0.2, -1.2, 0.9, '大理石', fs=12, ha='right')
    lead(ax, 0.3, 1.85, 1.1, 2.1, '瓶蓋(密封)', fs=12)
    ax.set_xlim(-2.4, 3.2); ax.set_ylim(-1.3, 2.3)
    save(f, 41105)


# ── 酸鹼滴定 ────────────────────────────────────
def ph_curve(v, veq, ca=0.1, cb=None, va=20.0):
    """以強酸強鹼計算 pH。v、veq 單位 mL;酸濃度 ca(M)。"""
    cb = ca * va / veq
    na, nb = ca * va, cb * v
    tot = (va + v) / 1000
    out = []
    for a, b, tv in zip(np.broadcast_to(na, v.shape), nb, tot):
        d = (a - b) / 1000 / tv
        if abs(d) < 1e-7:
            out.append(7.0)
        elif d > 0:
            out.append(-np.log10(d))
        else:
            out.append(14 + np.log10(-d))
    return np.array(out)


@fig(41106)
def f41106():
    f, ax = chart(6.0, 3.8)
    v = np.linspace(0, 40, 801)
    ax.plot(v, ph_curve(v, 20), color=BLUE, lw=2)
    ax.set_xticks(range(0, 41, 5)); ax.set_yticks(range(0, 15, 2)); ax.set_ylim(0, 14); ax.set_xlim(0, 40)
    labs(ax, '加入氫氧化鈉溶液體積(毫升)', 'pH')
    save(f, 41106)


@fig(41107)
def f41107():
    f, ax = chart(6.0, 3.8)
    v = np.linspace(0, 40, 801)
    p = ph_curve(v, 20)
    ax.plot(v, p, color=BLUE, lw=2)
    for name, vv in (('A', 10), ('B', 20), ('C', 30)):
        pv = ph_curve(np.array([float(vv)]), 20)[0]
        ax.plot([vv], [pv], 'o', color=RED, ms=6)
        txt(ax, vv + 0.8, pv - 1.0 if name != 'A' else pv + 0.5, name, color=RED, fs=14)
    ax.set_xticks(range(0, 41, 5)); ax.set_yticks(range(0, 15, 2)); ax.set_ylim(0, 14); ax.set_xlim(0, 40)
    labs(ax, '加入氫氧化鈉溶液體積(毫升)', 'pH')
    save(f, 41107)


TV = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40])
TEMP = np.array([22.0, 23.4, 24.8, 26.1, 27.4, 28.6, 27.9, 27.2, 26.6])


@fig(41108)
def f41108():
    f, ax = chart(6.0, 3.8)
    ax.plot(TV, TEMP, color=RED, lw=2, marker='o', ms=4)
    ax.set_xticks(TV); ax.set_ylim(21, 30); ax.set_yticks(range(21, 31))
    labs(ax, '加入氫氧化鈉溶液體積(毫升)', '溶液溫度(℃)')
    save(f, 41108)


@fig(41109)
def f41109():
    f, ax = chart(6.0, 3.8)
    v = np.linspace(0, 40, 801)
    ax.plot(v, ph_curve(v, 10, ca=0.05), color=BLUE, lw=2)
    ax.plot(v, ph_curve(v, 20, ca=0.1), color=RED, lw=2, ls='--')
    txt(ax, 11.5, 3.0, '甲', color=BLUE, fs=14)
    txt(ax, 21.5, 3.0, '乙', color=RED, fs=14)
    ax.set_xticks(range(0, 41, 5)); ax.set_yticks(range(0, 15, 2)); ax.set_ylim(0, 14); ax.set_xlim(0, 40)
    labs(ax, '加入氫氧化鈉溶液體積(毫升)', 'pH')
    save(f, 41109)
