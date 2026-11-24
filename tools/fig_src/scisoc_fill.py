from fig_all import *   # plt, np, PF, fig, new_ax, save, txt, dot, circle, arc, INK/RED/BLUE/GREY
from matplotlib.patches import Rectangle, Ellipse, Polygon, FancyBboxPatch


def _tube(ax, x, plant, foil, label):
    """一支試管:x 為中心;plant 是否放水蘊草;foil 是否包鋁箔。"""
    w, top, bot = 0.7, 4.2, 0.9
    # 液面
    ax.add_patch(Rectangle((x - w / 2, bot), w, 2.6, facecolor='#fbf3c8', edgecolor='none', zorder=1))
    ax.plot([x - w / 2, x - w / 2], [top, bot], color=INK, lw=1.6, zorder=4)
    ax.plot([x + w / 2, x + w / 2], [top, bot], color=INK, lw=1.6, zorder=4)
    th = np.linspace(np.pi, 2 * np.pi, 50)
    ax.plot(x + w / 2 * np.cos(th), bot + w / 2 * np.sin(th) * 0.9, color=INK, lw=1.6, zorder=4)
    ax.plot([x - w / 2, x + w / 2], [bot + 2.6, bot + 2.6], color=BLUE, lw=1.2, ls='--', zorder=3)
    # 橡皮塞
    ax.add_patch(Rectangle((x - w / 2 - 0.05, top), w + 0.1, 0.35, facecolor='#777777', edgecolor=INK, lw=1.2, zorder=5))
    if plant:
        stem_x = np.array([0, 0.05, -0.04, 0.03, 0])
        ys = np.linspace(0.8, 3.2, 5)
        ax.plot(x + stem_x, ys, color='#2f7d32', lw=2.0, zorder=2)
        for yy in np.linspace(1.0, 3.1, 7):
            ax.plot([x, x - 0.22], [yy, yy + 0.16], color='#2f7d32', lw=1.6, zorder=2)
            ax.plot([x, x + 0.22], [yy, yy + 0.16], color='#2f7d32', lw=1.6, zorder=2)
    if foil:
        ax.add_patch(Rectangle((x - w / 2 - 0.08, 0.35), w + 0.16, 4.0, facecolor='#bdbdbd',
                               edgecolor=INK, lw=1.4, hatch='///', zorder=6))
        txt(ax, x, 2.4, '鋁\n箔', fs=12, ha='center', va='center', zorder=7,
            bbox=dict(facecolor='white', edgecolor='none', pad=1))
    txt(ax, x, -0.25, label, fs=15, ha='center', va='center')
    txt(ax, x, -0.95, '有水蘊草' if plant else '無水蘊草', fs=12, ha='center', va='center')


@fig(41211)
def f41211():
    f, ax = new_ax(7.0, 4.6)
    xs = [1.0, 3.0, 5.0, 7.0]
    for x, (p, fo, lab) in zip(xs, [(True, False, '甲'), (True, True, '乙'), (False, False, '丙'), (False, True, '丁')]):
        _tube(ax, x, p, fo, lab)
    # 燈
    lx, ly = 4.0, 6.0
    circle(ax, lx, ly, 0.35, color=INK, lw=1.5)
    ax.add_patch(Rectangle((lx - 0.18, ly + 0.33), 0.36, 0.3, facecolor='#777777', edgecolor=INK, lw=1.2))
    for xe in xs:
        sx, sy = lx, ly - 0.4
        ex, ey = xe, 4.75
        ax.annotate('', xy=(sx + (ex - sx) * 0.85, sy + (ey - sy) * 0.85), xytext=(sx + (ex - sx) * 0.2, sy + (ey - sy) * 0.2),
                    arrowprops=dict(arrowstyle='->', color='#e0a000', lw=1.5))
    txt(ax, lx + 0.55, ly, '光源', fs=13, va='center')
    txt(ax, 8.0, 2.2, '含 BTB 的\n水溶液', fs=12, va='center')
    ax.set_xlim(0.0, 9.6)
    ax.set_ylim(-1.3, 6.8)
    save(f, 41211)


@fig(41212)
def f41212():
    f, ax = new_ax(6.6, 4.0)
    L, R = 0.0, 8.0
    # 上表皮
    ax.add_patch(Rectangle((L, 4.35), R - L, 0.12, facecolor='#dddddd', edgecolor=INK, lw=1.0))  # 角質層
    for x in np.arange(L, R, 0.8):
        ax.add_patch(Rectangle((x, 3.75), 0.8, 0.6, facecolor='white', edgecolor=INK, lw=1.3))
    # 柵狀組織
    for x in np.arange(L + 0.05, R - 0.3, 0.42):
        ax.add_patch(FancyBboxPatch((x + 0.03, 2.35), 0.32, 1.3, boxstyle='round,pad=0,rounding_size=0.12',
                                    facecolor='white', edgecolor=INK, lw=1.3))
        for yy in np.linspace(2.5, 3.5, 5):
            ax.add_patch(Ellipse((x + 0.19 + (0.06 if int(yy * 10) % 2 else -0.06), yy), 0.12, 0.08,
                                 facecolor='#2f7d32', edgecolor='none'))
    # 海綿組織(排列鬆散)
    rng = np.random.default_rng(7)
    pts = [(0.4, 1.9), (1.2, 1.55), (2.0, 1.95), (2.7, 1.4), (3.5, 1.85), (5.1, 1.9), (5.9, 1.45),
           (6.7, 1.95), (7.5, 1.5), (0.6, 1.05), (1.9, 0.95), (6.4, 1.0), (7.4, 0.95), (3.1, 0.95)]
    for (x, y) in pts:
        ax.add_patch(Ellipse((x, y), 0.62, 0.42, angle=rng.uniform(-30, 30), facecolor='white', edgecolor=INK, lw=1.3))
        for k in range(2):
            ax.add_patch(Ellipse((x + rng.uniform(-0.15, 0.15), y + rng.uniform(-0.08, 0.08)), 0.11, 0.07,
                                 facecolor='#2f7d32', edgecolor='none'))
    # 葉脈(維管束)
    circle(ax, 4.3, 1.45, 0.55, color=INK, lw=1.4)
    for (dx, dy) in [(-0.2, 0.2), (0.15, 0.25), (0.0, -0.05), (-0.22, -0.25), (0.2, -0.2)]:
        circle(ax, 4.3 + dx, 1.45 + dy, 0.12, color=INK, lw=1.0)
    # 下表皮 + 氣孔
    for x in np.arange(L, R, 0.8):
        if abs(x - 2.4) < 0.01:
            continue
        ax.add_patch(Rectangle((x, 0.2), 0.8, 0.45, facecolor='white', edgecolor=INK, lw=1.3))
    ax.add_patch(Ellipse((2.62, 0.42), 0.36, 0.42, facecolor='white', edgecolor=INK, lw=1.3))
    ax.add_patch(Ellipse((2.98, 0.42), 0.36, 0.42, facecolor='white', edgecolor=INK, lw=1.3))
    for cx in (2.62, 2.98):
        ax.add_patch(Ellipse((cx, 0.42), 0.09, 0.06, facecolor='#2f7d32', edgecolor='none'))
    # 標示
    def lab(xy, xt, s):
        ax.annotate('', xy=xy, xytext=xt, arrowprops=dict(arrowstyle='-', color=RED, lw=1.3))
        txt(ax, xt[0] + 0.12, xt[1], s, color=RED, fs=15, va='center')
    lab((7.6, 4.05), (8.6, 4.05), '甲')
    lab((7.55, 3.0), (8.6, 3.0), '乙')
    lab((7.75, 1.6), (8.6, 1.75), '丙')
    lab((2.95, 0.3), (3.8, -0.35), '丁')
    ax.set_xlim(-0.2, 9.3)
    ax.set_ylim(-0.7, 4.7)
    save(f, 41212)


def _industry(qid):
    f, ax = plt.subplots(figsize=(6.2, 4.0), dpi=200)
    years = ['1970 年', '1995 年', '2020 年']
    p1 = [55, 25, 6]
    p2 = [20, 35, 30]
    p3 = [25, 40, 64]
    x = np.arange(3)
    w = 0.5
    c1, c2, c3 = '#9fc98f', '#7aa6dc', '#f2c27a'
    b1 = ax.bar(x, p1, w, color=c1, edgecolor=INK, lw=1.2, label='第一級產業')
    b2 = ax.bar(x, p2, w, bottom=p1, color=c2, edgecolor=INK, lw=1.2, label='第二級產業')
    bot3 = [a + b for a, b in zip(p1, p2)]
    b3 = ax.bar(x, p3, w, bottom=bot3, color=c3, edgecolor=INK, lw=1.2, label='第三級產業')
    for i in range(3):
        for v, b in ((p1[i], 0), (p2[i], p1[i]), (p3[i], bot3[i])):
            ax.text(x[i], b + v / 2, f'{v}%', ha='center', va='center', fontsize=12, fontproperties=PF, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontproperties=PF, fontsize=13)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_yticklabels(['0', '20', '40', '60', '80', '100'], fontproperties=PF, fontsize=12)
    ax.set_ylabel('占就業人口比例(%)', fontproperties=PF, fontsize=13)
    ax.set_ylim(0, 100)
    ax.set_xlim(-0.5, 3.6)
    ax.set_title('某國(虛構)各級產業就業人口比例', fontproperties=PF, fontsize=14)
    ax.legend(handles=[b3, b2, b1], prop=PF, fontsize=12, loc='center right', frameon=False)
    for t in ax.get_legend().get_texts():
        t.set_fontproperties(PF); t.set_fontsize(12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    save(f, qid)


@fig(51108)
def f51108():
    _industry(51108)


@fig(51109)
def f51109():
    _industry(51109)


@fig(51110)
def f51110():
    _industry(51110)
