from fig_all import *   # plt, np, PF, fig, new_ax, save, txt, dot, circle, arc, INK/RED/BLUE/GREY

LETTERS = '甲乙丙丁'


# ───────────────────────── 共用工具 ─────────────────────────
def grid(ax, lons, lats, lonlab, latlab, lw=1.2, hl=None):
    """經緯線網格(示意)。lons/lats 為繪圖座標;lonlab/latlab 為標籤。hl:要加粗的 (kind,value)。"""
    x0, x1, y0, y1 = min(lons), max(lons), min(lats), max(lats)
    for x, s in zip(lons, lonlab):
        bold = hl and ('lon', x) in hl
        ax.plot([x, x], [y0, y1], color=(RED if bold else GREY), lw=(2.0 if bold else lw))
        txt(ax, x, y0 - 0.06 * (y1 - y0), s, fs=11, ha='center', va='top')
    for y, s in zip(lats, latlab):
        bold = hl and ('lat', y) in hl
        ax.plot([x0, x1], [y, y], color=(RED if bold else GREY), lw=(2.0 if bold else lw))
        txt(ax, x0 - 0.03 * (x1 - x0), y, s, fs=11, ha='right', va='center')


def pt(ax, x, y, s, dx=0.0, dy=0.0, color=BLUE, fs=14, ha='left', va='bottom'):
    ax.plot([x], [y], 'o', ms=7, color=color)
    txt(ax, x + dx, y + dy, s, color=color, fs=fs, ha=ha, va=va)


def north(ax, x, y, L=1.0, fs=12):
    ax.annotate('', xy=(x, y + L), xytext=(x, y), annotation_clip=False, arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.5))
    txt(ax, x, y + L * 1.08, '北', fs=fs, ha='center', va='bottom')


def style(ax):
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontproperties(PF); lab.set_fontsize(11)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


def climate(ax, temp, rain, rmax=500, tmin=-10, tmax=35, title=None):
    m = np.arange(1, 13)
    ax.bar(m, rain, color='#9db7e0', edgecolor=BLUE, lw=1.0, width=0.7)
    ax.set_ylim(0, rmax); ax.set_xlim(0.4, 12.6)
    ax.set_xticks(m); ax.set_xticklabels([str(i) for i in m])
    ax.set_ylabel('降雨量(毫米)', fontproperties=PF, fontsize=11)
    ax.set_xlabel('月', fontproperties=PF, fontsize=11)
    ax2 = ax.twinx()
    ax2.plot(m, temp, color=RED, lw=2.0, marker='o', ms=4)
    ax2.set_ylim(tmin, tmax)
    ax2.set_ylabel('氣溫(°C)', fontproperties=PF, fontsize=11)
    for lab in ax2.get_yticklabels():
        lab.set_fontproperties(PF); lab.set_fontsize(11)
    style(ax)
    ax2.spines['top'].set_visible(False)
    if title:
        ax.set_title(title, fontproperties=PF, fontsize=13)
    return ax2


def timeline(ax, years, labels, x0, x1, segs=None, pts=None, up=True):
    """years:繪圖用年份;labels:每個刻度上方文字;segs:[(a,b,字)];pts:[(year,字)]"""
    ax.plot([x0, x1], [0, 0], color=INK, lw=2.0)
    ax.annotate('', xy=(x1 + (x1 - x0) * 0.03, 0), xytext=(x1, 0),
                annotation_clip=False, arrowprops=dict(arrowstyle='-|>', color=INK, lw=2.0))
    for y, s in zip(years, labels):
        ax.plot([y, y], [-0.12, 0.12], color=INK, lw=2.0)
        txt(ax, y, 0.22, s, fs=12, ha='center', va='bottom')
    for a, b, s in (segs or []):
        ax.annotate('', xy=(a, -0.45), xytext=(b, -0.45),
                    annotation_clip=False, arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.4))
        txt(ax, (a + b) / 2, -0.6, s, color=BLUE, fs=14, ha='center', va='top')
    for y, s in (pts or []):
        ax.plot([y], [0], 'o', ms=8, color=BLUE)
        txt(ax, y, -0.3, s, color=BLUE, fs=14, ha='center', va='top')


def contour_map(ax, X, Y, Z, levels, label_levels=None, fs=11, manual=False):
    cs = ax.contour(X, Y, Z, levels=levels, colors=INK, linewidths=1.3)
    if label_levels is None:
        label_levels = levels
    lab = ax.clabel(cs, levels=label_levels, fmt='%d', fontsize=fs, inline=True, manual=manual)
    for t in lab:
        t.set_fontproperties(PF); t.set_fontsize(fs)
    return cs


# ───────────────────────── 51030 座標判讀 ─────────────────────────
@fig(51030)
def f51030():
    f, ax = new_ax(5.6, 4.2)
    xs = [-2, -1, 0, 1, 2]; ys = [-2, -1, 0, 1, 2]
    grid(ax, xs, ys, ['40°W', '20°W', '0°', '20°E', '40°E'], ['40°S', '20°S', '0°', '20°N', '40°N'])
    pt(ax, -1, -1, '甲', 0.08, 0.06)
    pt(ax, -1, 1, '乙', 0.08, 0.06)
    pt(ax, 1, -1, '丙', 0.08, 0.06)
    pt(ax, 1, 1, '丁', 0.08, 0.06)
    save(f, 51030)


# ───────────────────────── 51031 相對方位 ─────────────────────────
@fig(51031)
def f51031():
    f, ax = new_ax(5.6, 4.2)
    xs = [0, 1, 2, 3, 4]; ys = [0, 1, 2, 3, 4]
    grid(ax, xs, ys, ['100°E', '110°E', '120°E', '130°E', '140°E'], ['0°', '10°N', '20°N', '30°N', '40°N'])
    pt(ax, 1, 3, '甲', 0.1, 0.08)
    pt(ax, 3, 1, '乙', 0.1, 0.08)
    save(f, 51031)


# ───────────────────────── 51032 日出先後 ─────────────────────────
@fig(51032)
def f51032():
    f, ax = new_ax(6.0, 3.2)
    xs = [0, 1, 2, 3, 4, 5]; ys = [0, 1.3, 2.6]
    grid(ax, xs, ys, ['75°E', '90°E', '105°E', '120°E', '135°E', '150°E'], ['10°N', '20°N', '30°N'])
    for x, s in zip([1, 2, 3, 4], ['乙', '丙', '甲', '丁']):
        pt(ax, x, 1.3, s, 0.08, 0.08)
    save(f, 51032)


# ───────────────────────── 51033 時差 ─────────────────────────
@fig(51033)
def f51033():
    f, ax = new_ax(6.4, 3.0)
    lons = [-90, -60, -30, 0, 30, 60, 90, 120, 150]
    xs = [l / 30 for l in lons]
    lab = ['90°W', '60°W', '30°W', '0°', '30°E', '60°E', '90°E', '120°E', '150°E']
    grid(ax, xs, [0, 2.2, 4.4], lab, ['20°S', '0°', '20°N'])
    pt(ax, 120 / 30, 3.2, '甲', 0.1, 0.05)
    pt(ax, -60 / 30, 1.2, '乙', 0.1, 0.05)
    save(f, 51033)


# ───────────────────────── 51034 換日線 ─────────────────────────
@fig(51034)
def f51034():
    f, ax = new_ax(6.0, 3.4)
    xs = [0, 1, 2, 3, 4]
    grid(ax, xs, [0, 1, 2], ['160°E', '170°E', '180°', '170°W', '160°W'], ['10°S', '0°', '10°N'],
         hl=[('lon', 2)])
    pt(ax, 1, 1.3, '甲', -0.1, 0.08, ha='right')
    pt(ax, 3, 1.3, '乙', 0.1, 0.08)
    ax.annotate('', xy=(1.15, 1.3), xytext=(2.85, 1.3),
                annotation_clip=False, arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.6, linestyle='--'))
    txt(ax, 2.5, 0.75, '船隻航向', fs=12, ha='center')
    save(f, 51034)


# ───────────────────────── 51035 飛航時間 ─────────────────────────
@fig(51035)
def f51035():
    f, ax = new_ax(6.2, 3.2)
    lons = [-15, 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150]
    xs = [l / 15 for l in lons]
    lab = ['' if l not in (0, 45, 90, 135) else (f'{l}°E' if l else '0°') for l in lons]
    grid(ax, xs, [0, 2.6, 5.2], lab, ['20°N', '40°N', '60°N'])
    pt(ax, 9, 1.9, '甲', 0.15, 0.05)
    pt(ax, 0, 4.4, '乙', 0.15, 0.05)
    ax.annotate('', xy=(0.25, 4.35), xytext=(8.8, 2.0),
                annotation_clip=False, arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.6, linestyle='--', connectionstyle='arc3,rad=0.25'))
    txt(ax, 6.2, 4.75, '航線', color=RED, fs=12, ha='center')
    save(f, 51035)


# ───────────────────────── 51036 經緯度與距離 ─────────────────────────
@fig(51036)
def f51036():
    f, ax = new_ax(6.0, 4.0)
    xs = [0, 1, 2, 3, 4, 5, 6, 7, 8]; ys = [0, 1, 2, 3, 4, 5, 6]
    grid(ax, xs, ys, ['0°', '10°E', '20°E', '30°E', '40°E', '50°E', '60°E', '70°E', '80°E'],
         ['0°', '10°N', '20°N', '30°N', '40°N', '50°N', '60°N'])
    for (a, b, s1, s2, col) in [((2, 6), (3, 6), '甲', '乙', RED), ((4, 0), (5, 0), '丙', '丁', BLUE)]:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=3)
        pt(ax, *a, s1, -0.05, 0.1, color=col, ha='right')
        pt(ax, *b, s2, 0.05, 0.1, color=col)
    ax.plot([6.5, 6.5], [2, 3], color='#2e8b57', lw=3)
    pt(ax, 6.5, 2, '戊', 0.1, -0.05, color='#2e8b57', va='top')
    pt(ax, 6.5, 3, '己', 0.1, 0.05, color='#2e8b57')
    save(f, 51036)


# ───────────────────────── 51037 等高線疏密與坡度 ─────────────────────────
def hill37(x, y):
    a = np.where(x > 0, 0.8, 5.0)
    return 460 * np.exp(-(y ** 2) / 4.5 - (x ** 2) / a)


@fig(51037)
def f51037():
    f, ax = new_ax(6.0, 4.4)
    X, Y = np.meshgrid(np.linspace(-6, 3.2, 400), np.linspace(-4.2, 4.2, 400))
    contour_map(ax, X, Y, hill37(X, Y), [100, 200, 300, 400])
    ax.plot([0], [0], '^', ms=9, color=INK)
    # 四條路線都從 100 公尺等高線出發,直線登頂
    for (dx, dy), s in zip([(-1, 0), (1, 0), (0, 1), (0, -1)], ['甲', '乙', '丙', '丁']):
        r = np.linspace(0.01, 8, 4000)
        z = hill37(dx * r, dy * r)
        r0 = r[np.argmin(np.abs(z - 100))]
        sx, sy = dx * r0, dy * r0
        ax.plot([sx, 0], [sy, 0], color=RED, lw=1.6, ls='--')
        ax.plot([sx], [sy], 'o', color=RED, ms=6)
        off = {'甲': (-0.25, 0, 'right', 'center'), '乙': (0.25, 0, 'left', 'center'),
               '丙': (0, 0.2, 'center', 'bottom'), '丁': (0, -0.2, 'center', 'top')}[s]
        txt(ax, sx + off[0], sy + off[1], s, color=RED, fs=14, ha=off[2], va=off[3])
    north(ax, 2.9, 2.6, 1.0)
    txt(ax, -6, -4.2, '單位:公尺', fs=11)
    save(f, 51037)


# ───────────────────────── 51038 山谷與山脊 ─────────────────────────
@fig(51038)
def f51038():
    f, ax = new_ax(6.4, 4.2)
    X, Y = np.meshgrid(np.linspace(-4.6, 4.6, 400), np.linspace(0, 6, 400))
    Z = 40 * Y - 30 * np.cos(X) + 60
    lv = [80, 120, 160, 200, 240, 280]
    contour_map(ax, X, Y, Z, lv, manual=[(np.pi / 2, (z - 60) / 40) for z in lv])
    P = {'甲': (-np.pi, 3.0), '乙': (-np.pi / 2, 4.6), '丙': (0, 3.0), '丁': (np.pi, 3.0)}
    for s, (x, y) in P.items():
        ax.plot([x], [y], 'o', color=RED, ms=7)
        txt(ax, x + 0.15, y + 0.12, s, color=RED, fs=14)
    north(ax, 5.1, 4.4, 1.0)
    txt(ax, -4.6, -0.55, '單位:公尺', fs=11)
    ax.set_xlim(-4.7, 5.6)
    save(f, 51038)


# ───────────────────────── 51039 河流流向 ─────────────────────────
@fig(51039)
def f51039():
    f, ax = new_ax(5.4, 4.6)
    X, Y = np.meshgrid(np.linspace(-3, 3, 400), np.linspace(-3, 3, 400))
    U = (X + Y) / np.sqrt(2); V = (X - Y) / np.sqrt(2)
    Z = 200 + 45 * U + 70 * np.sqrt(V ** 2 + 0.15)
    contour_map(ax, X, Y, Z, [100, 150, 200, 250, 300, 350, 400])
    t = np.linspace(-2.9, 2.9, 50)
    ax.plot(t, t, color=BLUE, lw=2.4)
    txt(ax, -1.25, -2.2, '河流', color=BLUE, fs=12)
    north(ax, 3.4, 1.4, 1.0)
    txt(ax, -3.0, -3.55, '單位:公尺', fs=11)
    save(f, 51039)


# ───────────────────────── 51040 剖面配對 ─────────────────────────
def terr40(x, y):
    return 520 * np.exp(-((x - 2.2) ** 2 + y ** 2) / 1.6) + 330 * np.exp(-((x - 5.8) ** 2 + (y - 0.2) ** 2) / 1.8)


@fig(51040)
def f51040():
    f = plt.figure(figsize=(8.0, 4.0), dpi=200)
    ax = f.add_axes([0.0, 0.05, 0.48, 0.9]); ax.set_aspect('equal'); ax.axis('off')
    X, Y = np.meshgrid(np.linspace(0, 8, 400), np.linspace(-3, 3, 400))
    contour_map(ax, X, Y, terr40(X, Y), [100, 200, 300, 400, 500], fs=10)
    ax.plot([0.3, 7.7], [0, 0], color=RED, lw=1.6)
    txt(ax, 0.15, 0, 'A', color=RED, fs=13, ha='right', va='center')
    txt(ax, 7.85, 0, 'B', color=RED, fs=13, ha='left', va='center')
    txt(ax, 0, -3.3, '單位:公尺', fs=10, va='top')
    xs = np.linspace(0.3, 7.7, 200)
    true = terr40(xs, 0 * xs)
    mirror = true[::-1]
    single = 520 * np.exp(-((xs - 4.0) ** 2) / 3.0)
    equal = 430 * np.exp(-((xs - 2.2) ** 2) / 1.6) + 430 * np.exp(-((xs - 5.8) ** 2) / 1.8)
    profiles = [mirror, single, equal, true]           # 正解放在「丁」
    for i, (pr, s) in enumerate(zip(profiles, LETTERS)):
        r, c = divmod(i, 2)
        a = f.add_axes([0.54 + c * 0.24, 0.55 - r * 0.47, 0.2, 0.32])
        a.fill_between(xs, 0, pr, color='#e8e1d0')
        a.plot(xs, pr, color=INK, lw=1.5)
        a.set_ylim(0, 600); a.set_xlim(0.3, 7.7)
        a.set_xticks([]); a.set_yticks([0, 300, 600])
        a.set_yticklabels(['0', '300', '600'])
        style(a)
        a.set_title(f'({s})', fontproperties=PF, fontsize=12)
        a.text(0.3, -90, 'A', fontsize=11, ha='center', va='top')
        a.text(7.7, -90, 'B', fontsize=11, ha='center', va='top')
    save(f, 51040)


# ───────────────────────── 51041 山頂高度 ─────────────────────────
def hill41(x, y):
    return 470 * np.exp(-(x ** 2) / 6 - (y ** 2) / 3)


@fig(51041)
def f51041():
    f, ax = new_ax(5.8, 4.0)
    X, Y = np.meshgrid(np.linspace(-4.5, 4.5, 400), np.linspace(-3, 3, 400))
    contour_map(ax, X, Y, hill41(X, Y), [100, 200, 300, 400], label_levels=[100, 300])
    ax.plot([0], [0], '^', ms=10, color=RED)
    txt(ax, 0.2, 0.05, '山頂', color=RED, fs=12)
    txt(ax, -4.5, -3.3, '單位:公尺', fs=11, va='top')
    save(f, 51041)


# ───────────────────────── 51042 比例尺+等高線 ─────────────────────────
def hill42(x, y):
    return 530 * np.exp(-(x ** 2 + y ** 2) / 9.0)


@fig(51042)
def f51042():
    f, ax = new_ax(5.6, 4.4)
    X, Y = np.meshgrid(np.linspace(-4.2, 4.2, 400), np.linspace(-3.4, 3.4, 400))
    contour_map(ax, X, Y, hill42(X, Y), [200, 250, 300, 350, 400, 450, 500], label_levels=[200, 400])
    # 甲在 250 等高線、乙在 450 等高線(都在 30° 方向上)
    d = np.array([np.cos(np.radians(140)), np.sin(np.radians(140))])
    for h, s in [(250, '甲'), (450, '乙')]:
        r = 3.0 * np.sqrt(np.log(530 / h))
        x, y = r * d
        ax.plot([x], [y], 'o', color=RED, ms=7)
        txt(ax, x - 0.15, y + 0.12, s, color=RED, fs=14, ha='right', va='bottom')
    ax.plot([0], [0], '^', ms=9, color=INK)
    txt(ax, 2.6, -3.4, '單位:公尺', fs=11)
    save(f, 51042)


# ───────────────────────── 51043 鞍部 ─────────────────────────
@fig(51043)
def f51043():
    f, ax = new_ax(6.2, 3.8)
    X, Y = np.meshgrid(np.linspace(-4.2, 4.2, 400), np.linspace(-2.6, 2.6, 400))
    Z = 400 * np.exp(-((X + 1.6) ** 2 + Y ** 2) / 1.5) + 380 * np.exp(-((X - 1.6) ** 2 + Y ** 2) / 1.5)
    contour_map(ax, X, Y, Z, [100, 150, 200, 250, 300, 350], label_levels=[100, 200, 300])
    P = {'甲': (0, 0), '乙': (-1.6, 0.0), '丙': (0, 2.1), '丁': (3.3, -1.3)}
    for s, (x, y) in P.items():
        ax.plot([x], [y], 'o', color=RED, ms=7)
        if s == '乙':
            txt(ax, x - 0.12, y + 0.1, s, color=RED, fs=14, ha='right')
        else:
            txt(ax, x + 0.12, y + 0.1, s, color=RED, fs=14)
    txt(ax, -4.2, -2.9, '單位:公尺', fs=11, va='top')
    save(f, 51043)


# ───────────────────────── 51044 方格與線段比例尺 ─────────────────────────
def square_grid(ax, nx, ny):
    for i in range(nx + 1):
        ax.plot([i, i], [0, ny], color=GREY, lw=1.0)
    for j in range(ny + 1):
        ax.plot([0, nx], [j, j], color=GREY, lw=1.0)


@fig(51044)
def f51044():
    f, ax = new_ax(6.0, 3.8)
    square_grid(ax, 8, 4)
    pt(ax, 1, 2, '甲', -0.12, 0.1, color=RED, ha='right')
    pt(ax, 7, 2, '乙', 0.12, 0.1, color=RED)
    # 線段比例尺:兩格 = 1 公里
    y = -0.7
    ax.plot([0, 2], [y, y], color=INK, lw=2.4)
    for xx in (0, 1, 2):
        ax.plot([xx, xx], [y - 0.12, y + 0.12], color=INK, lw=1.6)
    txt(ax, 0, y - 0.2, '0', fs=11, ha='center', va='top')
    txt(ax, 2, y - 0.2, '1 公里', fs=11, ha='center', va='top')
    north(ax, 8.5, 2.6, 1.0)
    save(f, 51044)


# ───────────────────────── 51045 線段比例尺→數字比例尺 ─────────────────────────
@fig(51045)
def f51045():
    f, ax = new_ax(6.0, 2.0)
    for i in range(3):
        ax.fill_between([i, i + 1], 0, 0.25, color=(INK if i % 2 == 0 else 'white'), edgecolor=INK, lw=1.4)
    ax.plot([0, 3, 3, 0, 0], [0, 0, 0.25, 0.25, 0], color=INK, lw=1.4)
    for i, s in enumerate(['0', '2', '4', '6 公里']):
        txt(ax, i, 0.38, s, fs=12, ha='center', va='bottom')
    ax.annotate('', xy=(0, -0.25), xytext=(1, -0.25), annotation_clip=False, arrowprops=dict(arrowstyle='<->', color=RED, lw=1.4))
    txt(ax, 0.5, -0.38, '圖上長 1 公分', color=RED, fs=12, ha='center', va='top')
    ax.set_xlim(-0.4, 3.6); ax.set_ylim(-0.9, 0.8)
    save(f, 51045)


# ───────────────────────── 51046 斜向距離 ─────────────────────────
@fig(51046)
def f51046():
    f, ax = new_ax(5.6, 4.2)
    square_grid(ax, 6, 5)
    pt(ax, 1, 0.5 + 0.5, '甲', -0.12, -0.1, color=RED, ha='right', va='top')
    pt(ax, 4, 5, '乙', 0.12, 0.05, color=RED)
    ax.plot([1, 4], [1, 5], color=RED, lw=1.6, ls='--')
    txt(ax, 0, -0.25, '每一小方格邊長:圖上 1 公分   比例尺 1:50,000', fs=11, va='top')
    save(f, 51046)


# ───────────────────────── 51047 面積換算 ─────────────────────────
@fig(51047)
def f51047():
    f, ax = new_ax(5.4, 3.6)
    ax.plot([0, 4, 4, 0, 0], [0, 0, 3, 3, 0], color=BLUE, lw=2.0)
    ax.fill_between([0, 4], 0, 3, color='#dce6f5')
    txt(ax, 2, 1.5, '保護區', color=BLUE, fs=14, ha='center', va='center')
    ax.annotate('', xy=(0, -0.3), xytext=(4, -0.3), annotation_clip=False, arrowprops=dict(arrowstyle='<->', color=INK, lw=1.3))
    txt(ax, 2, -0.42, '圖上 4 公分', fs=12, ha='center', va='top')
    ax.annotate('', xy=(4.3, 0), xytext=(4.3, 3), annotation_clip=False, arrowprops=dict(arrowstyle='<->', color=INK, lw=1.3))
    txt(ax, 4.42, 1.5, '圖上\n3 公分', fs=12, va='center')
    txt(ax, 0, 3.25, '比例尺 1:50,000', fs=12)
    ax.set_xlim(-0.3, 5.4)
    save(f, 51047)


# ───────────────────────── 51048 颱風路徑 ─────────────────────────
@fig(51048)
def f51048():
    f, ax = new_ax(6.0, 4.4)
    xs = [118, 120, 122, 124, 126, 128, 130]; ys = [16, 18, 20, 22, 24, 26]
    grid(ax, xs, ys, [f'{v}°E' for v in xs], [f'{v}°N' for v in ys])
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((121.0, 23.7), 1.3, 3.2, angle=-15, facecolor='#ddd', edgecolor=INK, lw=1.2))
    txt(ax, 121.0, 23.7, '臺灣', fs=11, ha='center', va='center')
    track = [(129.2, 17.0), (127.0, 19.2), (124.6, 21.4), (122.8, 23.0)]
    tx, ty = zip(*track)
    ax.plot(tx, ty, color=RED, lw=1.6, ls='--')
    for (x, y), s in zip(track, ['甲', '', '', '乙']):
        ax.plot([x], [y], 'o', ms=9, mfc='white', mec=RED, mew=2)
        if s:
            txt(ax, x + 0.4, y + 0.3, s, color=RED, fs=14, va='bottom')
    save(f, 51048)


# ───────────────────────── 51049 臺灣東西剖面 ─────────────────────────
@fig(51049)
def f51049():
    f, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200)
    x = np.linspace(0, 150, 600)
    h = np.interp(x, [0, 35, 55, 70, 85, 100, 108, 113, 117, 125, 132, 140, 145, 150],
                  [0, 30, 150, 800, 2000, 3300, 2500, 1300, 250, 300, 1300, 1100, 0, 0])
    ax.fill_between(x, 0, h, color='#e8e1d0')
    ax.plot(x, h, color=INK, lw=1.6)
    ax.axhline(0, color=BLUE, lw=1.2)
    for xx, s in [(20, '甲'), (100, '乙'), (121, '丙'), (132, '丁')]:
        yy = np.interp(xx, x, h)
        ax.plot([xx], [yy], 'o', color=RED, ms=6)
        txt(ax, xx, yy + 150, s, color=RED, fs=14, ha='center', va='bottom')
    ax.set_xlim(0, 150); ax.set_ylim(0, 4000)
    ax.set_xticks([0, 50, 100, 150]); ax.set_xticklabels(['0', '50', '100', '150'])
    ax.set_xlabel('水平距離(公里)', fontproperties=PF, fontsize=11)
    ax.set_ylabel('海拔(公尺)', fontproperties=PF, fontsize=11)
    txt(ax, 2, 3700, '西', fs=13)
    txt(ax, 148, 3700, '東', fs=13, ha='right')
    style(ax)
    save(f, 51049)


# ───────────────────────── 51050 / 51051 臺灣氣候圖 ─────────────────────────
KHH_T = [19.3, 20.3, 22.6, 25.5, 27.7, 28.8, 29.4, 28.9, 28.6, 27.4, 24.7, 21.1]
KHH_R = [15, 15, 31, 71, 175, 414, 381, 441, 264, 48, 19, 15]
KEE_T = [16.2, 16.4, 18.1, 21.4, 24.7, 27.4, 29.6, 29.3, 27.4, 24.3, 21.4, 18.0]
KEE_R = [342, 377, 330, 245, 291, 302, 151, 210, 375, 400, 391, 337]


@fig(51050)
def f51050():
    f, ax = plt.subplots(figsize=(5.6, 3.8), dpi=200)
    climate(ax, KHH_T, KHH_R, rmax=500, tmin=0, tmax=35)
    save(f, 51050)


@fig(51051)
def f51051():
    f, axs = plt.subplots(1, 2, figsize=(8.4, 3.6), dpi=200)
    climate(axs[0], KEE_T, KEE_R, rmax=500, tmin=0, tmax=35, title='甲站')
    climate(axs[1], KHH_T, KHH_R, rmax=500, tmin=0, tmax=35, title='乙站')
    f.tight_layout(w_pad=2.5)
    save(f, 51051)


# ───────────────────────── 51052 臺灣周邊島嶼 ─────────────────────────
@fig(51052)
def f51052():
    f, ax = new_ax(5.6, 4.6)
    xs = [116, 117, 118, 119, 120, 121, 122, 123, 124]; ys = [21, 22, 23, 24, 25, 26, 27]
    grid(ax, xs, ys, [f'{v}°E' for v in xs], [f'{v}°N' for v in ys])
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((120.95, 23.7), 1.1, 3.4, angle=-15, facecolor='#ddd', edgecolor=INK, lw=1.2))
    txt(ax, 120.95, 23.9, '臺灣\n本島', fs=11, ha='center', va='center')
    for (x, y), s in zip([(120.0, 26.2), (119.6, 23.6), (118.4, 24.4), (121.55, 22.05)], LETTERS):
        pt(ax, x, y, s, 0.1, 0.05, color=RED)
    save(f, 51052)


# ───────────────────────── 51053 氣候帶緯度 ─────────────────────────
@fig(51053)
def f51053():
    f, ax = new_ax(5.4, 4.4)
    lats = [66.5, 23.5, 0, -23.5, -66.5]
    ax.plot([0, 8, 8, 0, 0], [-90, -90, 90, 90, -90], color=INK, lw=1.4)
    for la in lats:
        ax.plot([0, 8], [la, la], color=(INK if la == 0 else GREY), lw=1.4, ls=('-' if la == 0 else '--'))
        s = '0°' if la == 0 else f'{abs(la)}°{"N" if la > 0 else "S"}'
        txt(ax, -0.15, la, s, fs=11, ha='right', va='center')
    for (x, la), s in zip([(1.5, 10), (4.0, 72), (6.2, 35), (2.8, -42)], LETTERS):
        pt(ax, x, la, s, 0.15, 1.5, color=RED)
    ax.set_xlim(-1.6, 8.3)
    ax.set_aspect(9.9 / 180 * 0.65)
    save(f, 51053)


# ───────────────────────── 51054–51057 世界氣候圖 ─────────────────────────
@fig(51054)
def f51054():
    f, ax = plt.subplots(figsize=(5.6, 3.8), dpi=200)
    climate(ax, [26.5, 27.1, 27.5, 27.9, 28.3, 28.3, 27.9, 27.9, 27.6, 27.6, 27.0, 26.5],
            [240, 160, 185, 180, 170, 160, 160, 175, 170, 195, 255, 290], rmax=400, tmin=-10, tmax=35)
    save(f, 51054)


@fig(51055)
def f51055():
    f, ax = plt.subplots(figsize=(5.6, 3.8), dpi=200)
    climate(ax, [24.5, 23.5, 21.5, 18, 14.5, 11.5, 11, 12, 14, 17, 20.5, 23],
            [100, 115, 115, 90, 80, 60, 60, 65, 75, 115, 105, 100], rmax=300, tmin=-10, tmax=35)
    save(f, 51055)


@fig(51056)
def f51056():
    f, ax = plt.subplots(figsize=(5.6, 3.8), dpi=200)
    climate(ax, [8.5, 9.5, 11.5, 14, 18, 22.5, 25.5, 25.5, 22, 17.5, 12.5, 9.5],
            [80, 75, 70, 65, 45, 20, 10, 25, 70, 115, 115, 90], rmax=300, tmin=-10, tmax=35)
    save(f, 51056)


@fig(51057)
def f51057():
    f, ax = plt.subplots(figsize=(5.8, 3.8), dpi=200)
    m = np.arange(1, 13)
    a = [4.5, 5, 7, 9, 12, 14.5, 16.5, 16.5, 14.5, 11.5, 7.5, 5.5]
    b = [-15, -12.5, -5, 5, 12.5, 17.5, 20, 18.5, 12, 4, -5, -12]
    ax.plot(m, a, color=BLUE, lw=2.0, marker='o', ms=4)
    ax.plot(m, b, color=RED, lw=2.0, marker='s', ms=4)
    txt(ax, 12.2, a[-1], '甲', color=BLUE, fs=13, va='center')
    txt(ax, 12.2, b[-1], '乙', color=RED, fs=13, va='center')
    ax.axhline(0, color=GREY, lw=1.0)
    ax.set_xticks(m); ax.set_xticklabels([str(i) for i in m])
    ax.set_xlim(0.5, 12.9); ax.set_ylim(-20, 25)
    ax.set_xlabel('月', fontproperties=PF, fontsize=11)
    ax.set_ylabel('月均溫(°C)', fontproperties=PF, fontsize=11)
    style(ax)
    save(f, 51057)


# ───────────────────────── 臺灣史 ─────────────────────────
@fig(51058)
def f51058():
    f, ax = new_ax(6.6, 2.4, equal=False)
    ys = [1683, 1858, 1885, 1895]
    xs = [0, 3.2, 5.6, 7.2]
    timeline(ax, xs, ['1683\n清朝領臺', '1858\n天津條約', '1885\n臺灣建省', '1895\n馬關條約'], -0.3, 8.6,
             segs=[(0, 3.2, '甲'), (3.2, 5.6, '乙'), (5.6, 7.2, '丙'), (7.2, 8.6, '丁')])
    ax.set_ylim(-1.1, 1.2)
    save(f, 51058)


@fig(51059)
def f51059():
    f, ax = plt.subplots(figsize=(5.8, 3.8), dpi=200)
    yrs = [1868, 1872, 1876, 1880, 1884, 1888, 1892, 1895]
    a = [10, 25, 45, 60, 65, 70, 80, 85]
    b = [30, 35, 40, 35, 30, 28, 30, 25]
    ax.plot(yrs, a, color=RED, lw=2.0, marker='o', ms=4)
    ax.plot(yrs, b, color=BLUE, lw=2.0, marker='s', ms=4)
    txt(ax, 1895.6, a[-1], '甲', color=RED, fs=13, va='center')
    txt(ax, 1895.6, b[-1], '乙', color=BLUE, fs=13, va='center')
    ax.set_xticks([1868, 1876, 1884, 1892]); ax.set_xticklabels(['1868', '1876', '1884', '1892'])
    ax.set_xlim(1866, 1898); ax.set_ylim(0, 100)
    ax.set_xlabel('年', fontproperties=PF, fontsize=11)
    ax.set_ylabel('出口值(相對指數,示意)', fontproperties=PF, fontsize=11)
    style(ax)
    save(f, 51059)


@fig(51060)
def f51060():
    f, ax = plt.subplots(figsize=(5.8, 3.8), dpi=200)
    yrs = [1905, 1915, 1920, 1925, 1930, 1935, 1940]
    pop = [304, 348, 366, 399, 459, 521, 587]
    ax.bar(yrs, pop, width=3.2, color='#9db7e0', edgecolor=BLUE, lw=1.0)
    for x, p in zip(yrs, pop):
        txt(ax, x, p + 8, str(p), fs=11, ha='center', va='bottom')
    ax.set_xticks(yrs); ax.set_xticklabels([str(y) for y in yrs])
    ax.set_ylim(0, 700)
    ax.set_xlabel('年(人口普查)', fontproperties=PF, fontsize=11)
    ax.set_ylabel('臺灣總人口(萬人)', fontproperties=PF, fontsize=11)
    style(ax)
    save(f, 51060)


@fig(51061)
def f51061():
    f, ax = new_ax(6.6, 2.4, equal=False)
    xs = [0, 3.0, 5.4, 7.2]
    timeline(ax, xs, ['1895', '1919', '1937', '1945'], -0.3, 7.8,
             segs=[(0, 3.0, '甲'), (3.0, 5.4, '乙'), (5.4, 7.2, '丙')])
    ax.set_ylim(-1.1, 0.9)
    save(f, 51061)


@fig(51062)
def f51062():
    f, ax = new_ax(6.6, 2.4, equal=False)
    xs = [0, 2.5, 5.0, 7.5]
    timeline(ax, xs, ['1895\n馬關條約', '1915\n西來庵事件', '?', '1937\n中日戰爭爆發'], -0.4, 8.2)
    ax.plot([5.0], [0], 'o', ms=9, color=RED)
    txt(ax, 5.0, -0.3, '某事件', color=RED, fs=13, ha='center', va='top')
    ax.set_ylim(-0.9, 1.2)
    save(f, 51062)


@fig(51063)
def f51063():
    f, ax = plt.subplots(figsize=(5.8, 3.8), dpi=200)
    yrs = [1920, 1930, 1935, 1940, 1943]
    r = [25, 33, 42, 58, 71]
    ax.plot(yrs, r, color=RED, lw=2.0, marker='o', ms=5)
    for x, v in zip(yrs, r):
        txt(ax, x - 0.5, v + 1, f'約 {v}%', fs=11, ha='right', va='bottom')
    ax.set_xticks(yrs); ax.set_xticklabels([str(y) for y in yrs])
    ax.set_xlim(1912, 1946); ax.set_ylim(0, 90)
    ax.set_xlabel('年', fontproperties=PF, fontsize=11)
    ax.set_ylabel('臺灣學齡兒童就學率(%)', fontproperties=PF, fontsize=11)
    style(ax)
    save(f, 51063)


# ───────────────────────── 世界史 ─────────────────────────
@fig(51064)
def f51064():
    f, ax = new_ax(6.4, 2.0, equal=False)
    xs = [0, 1.4, 5.0, 6.8]
    timeline(ax, xs, ['1776', '1789', '1871', '1914'], -0.4, 7.4,
             pts=list(zip(xs, LETTERS)))
    ax.set_ylim(-0.9, 0.8)
    save(f, 51064)


@fig(51065)
def f51065():
    f, ax = plt.subplots(figsize=(5.8, 3.8), dpi=200)
    yrs = [1700, 1750, 1775, 1800, 1830, 1850, 1870]
    v = [3, 5, 9, 15, 30, 55, 110]
    ax.plot(yrs, v, color=INK, lw=2.0, marker='o', ms=5)
    ax.set_xticks([1700, 1750, 1800, 1850]); ax.set_xticklabels(['1700', '1750', '1800', '1850'])
    ax.set_xlim(1690, 1880); ax.set_ylim(0, 120)
    ax.set_xlabel('年', fontproperties=PF, fontsize=11)
    ax.set_ylabel('英國煤產量(百萬噸,約數)', fontproperties=PF, fontsize=11)
    style(ax)
    save(f, 51065)


@fig(51066)
def f51066():
    f, ax = plt.subplots(figsize=(5.8, 3.8), dpi=200)
    yrs = list(range(1928, 1939))
    v = [4.2, 3.2, 8.7, 15.9, 23.6, 24.9, 21.7, 20.1, 16.9, 14.3, 19.0]
    ax.plot(yrs, v, color=RED, lw=2.0, marker='o', ms=4)
    ax.set_xticks(yrs[::2]); ax.set_xticklabels([str(y) for y in yrs[::2]])
    ax.set_ylim(0, 30)
    ax.set_xlabel('年', fontproperties=PF, fontsize=11)
    ax.set_ylabel('美國失業率(%)', fontproperties=PF, fontsize=11)
    style(ax)
    save(f, 51066)


@fig(51067)
def f51067():
    f, ax = new_ax(6.6, 2.4, equal=False)
    xs = [0, 2.6, 5.3, 6.9]
    timeline(ax, xs, ['1945\n二戰結束', '1961\n柏林圍牆建立', '1989\n圍牆倒塌', '1991\n蘇聯解體'], -0.3, 8.4,
             segs=[(0, 2.6, '甲'), (2.6, 5.3, '乙'), (5.3, 6.9, '丙'), (6.9, 8.4, '丁')])
    ax.set_ylim(-1.1, 1.2)
    save(f, 51067)


@fig(51068)
def f51068():
    f, ax = plt.subplots(figsize=(5.8, 3.8), dpi=200)
    yrs = [1800, 1850, 1900, 1927, 1950, 1960, 1975, 1987, 1999, 2011, 2022]
    v = [1.0, 1.26, 1.65, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    ax.plot(yrs, v, color=BLUE, lw=2.0, marker='o', ms=4)
    ax.set_xticks([1800, 1850, 1900, 1950, 2000]); ax.set_xticklabels(['1800', '1850', '1900', '1950', '2000'])
    ax.set_ylim(0, 9)
    ax.set_xlabel('年', fontproperties=PF, fontsize=11)
    ax.set_ylabel('世界人口(十億人,約數)', fontproperties=PF, fontsize=11)
    style(ax)
    save(f, 51068)


@fig(51069)
def f51069():
    f, ax = new_ax(6.6, 2.4, equal=False)
    xs = [0, 1.2, 6.2, 8.0]
    timeline(ax, xs, ['1914', '1918', '1939', '1945'], -0.3, 9.0,
             segs=[(0, 1.2, '甲'), (1.2, 6.2, '乙'), (6.2, 8.0, '丙'), (8.0, 9.0, '丁')])
    ax.set_ylim(-1.1, 0.9)
    save(f, 51069)
