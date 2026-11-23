from fig_all import *   # 提供 plt, np, PF(中文字型), fig 裝飾器, new_ax(w,h,equal), save(f, qid), txt(ax,x,y,s,...), dot, circle, arc, INK/RED/BLUE/GREY 顏色
from matplotlib.patches import Ellipse, Rectangle, Polygon, FancyBboxPatch
plt.rcParams['axes.unicode_minus'] = False
LGREY = '#dddddd'


def P(size):
    p = PF.copy()
    p.set_size(size)
    return p


def graph(w=6.0, h=4.0):
    f, ax = plt.subplots(figsize=(w, h), dpi=200)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(1.3)
        ax.spines[s].set_color(INK)
    return f, ax


def finish(ax, xl, yl, grid=True):
    if grid:
        ax.grid(color=LGREY, lw=0.8)
        ax.set_axisbelow(True)
    ax.set_xlabel(xl, fontproperties=P(13), color=INK)
    ax.set_ylabel(yl, fontproperties=P(13), color=INK)
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontproperties(P(12))
    ax.tick_params(colors=INK, width=1.1)


def ray(ax, p0, p1, color=INK, lw=1.6, ls='-', arrow=True, frac=0.55):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, ls=ls)
    if arrow:
        mx = p0[0] + (p1[0] - p0[0]) * frac
        my = p0[1] + (p1[1] - p0[1]) * frac
        dx = (p1[0] - p0[0]) * 0.01
        dy = (p1[1] - p0[1]) * 0.01
        ax.annotate('', xy=(mx + dx, my + dy), xytext=(mx - dx, my - dy),
                    arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=16))


def farrow(ax, p0, p1, color=RED, lw=2.0):
    ax.annotate('', xy=p1, xytext=p0, arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=18))


def hatch_line(ax, x0, y0, x1, y1, side=(0, -1), n=14, L=0.18, color=INK):
    ax.plot([x0, x1], [y0, y1], color=color, lw=2.4)
    for t in np.linspace(0, 1, n):
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        ax.plot([x, x + side[0] * L + (L * 0.6 if side[1] else 0)],
                [y, y + side[1] * L + (L * 0.6 if side[0] else 0)], color=color, lw=1.0)


def conv_lens(ax, x=0, h=3.0):
    ax.add_patch(Ellipse((x, 0), 0.32, h, fill=False, color=INK, lw=1.6))


def axis_line(ax, x0, x1):
    ax.plot([x0, x1], [0, 0], color=INK, lw=1.2, ls=(0, (6, 3)))


def focus_marks(ax, f, labels2=True, fs=13):
    for s in (-1, 1):
        dot(ax, s * f, 0, 'F', dx=-0.12, dy=-0.42, fs=fs)
        if labels2:
            dot(ax, s * 2 * f, 0, '2F', dx=-0.22, dy=-0.42, fs=fs)


def obj_arrow(ax, x, h, color=BLUE):
    ax.annotate('', xy=(x, h), xytext=(x, 0), arrowprops=dict(arrowstyle='-|>', color=color, lw=2.2, mutation_scale=18))


def wave_panel(ax, amp, ncyc, title=None, divx=8, divy=4):
    ax.set_xlim(0, divx)
    ax.set_ylim(-divy, divy)
    ax.set_xticks(range(divx + 1))
    ax.set_yticks(range(-divy, divy + 1))
    ax.grid(color=LGREY, lw=0.8)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_color(INK)
        s.set_linewidth(1.2)
    x = np.linspace(0, divx, 800)
    ax.plot(x, amp * np.sin(2 * np.pi * ncyc * x / divx), color=BLUE, lw=1.8)
    if title:
        ax.set_title(title, fontproperties=P(14), color=INK)


# ───────────────────────── 光與透鏡 ─────────────────────────
@fig(41020)
def f41020():
    f, ax = new_ax(6, 3.4)
    hatch_line(ax, -3.2, 0, 3.2, 0, side=(0, -1), n=22)
    ax.plot([0, 0], [-0.1, 2.2], color=GREY, lw=1.3, ls='--')
    txt(ax, 0.1, 2.05, '法線', color=GREY, fs=12)
    a = np.radians(30)
    p0 = (-2.8 * np.cos(a), 2.8 * np.sin(a))
    ray(ax, p0, (0, 0), color=RED, lw=1.8)
    arc(ax, 0, 0, 0.9, 150, 180, color=INK, lw=1.3)
    txt(ax, -1.45, 0.17, '30°', fs=13)
    txt(ax, -3.1, 1.5, '入射光', color=RED, fs=13)
    txt(ax, 2.2, -0.62, '平面鏡', fs=13)
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-0.8, 2.3)
    save(f, 41020)


@fig(41021)
def f41021():
    f, ax = new_ax(6, 4.2)
    ax.add_patch(Rectangle((-3, -2.6), 6, 2.6, color='#e6eef8', zorder=0))
    ax.plot([-3, 3], [0, 0], color=INK, lw=1.6)
    ax.plot([0, 0], [-2.5, 2.4], color=GREY, lw=1.3, ls='--')
    txt(ax, -2.9, 1.9, '空氣', fs=13)
    txt(ax, -2.9, -2.3, '水', fs=13)
    ray(ax, (-2.2, 2.2), (0, 0), color=RED, lw=1.8)
    L = 2.4
    cand = {'甲': 60, '乙': 45, '丙': 25, '丁': -25}
    for lab, ang in cand.items():
        a = np.radians(ang)
        p1 = (L * np.sin(a), -L * np.cos(a))
        ray(ax, (0, 0), p1, color=INK, lw=1.5)
        txt(ax, p1[0] + (0.08 if ang > 0 else -0.35), p1[1] - 0.28, lab, fs=14)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2.8, 2.4)
    save(f, 41021)


@fig(41022)
def f41022():
    f, ax = new_ax(6.4, 3.2)
    axis_line(ax, -5.4, 5.4)
    conv_lens(ax, 0, 3.0)
    focus_marks(ax, 2)
    obj_arrow(ax, -3, 1.0)
    txt(ax, -3.35, 1.15, '物體', color=BLUE, fs=13)
    txt(ax, 0.25, 1.35, '凸透鏡', fs=13)
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-1.7, 1.7)
    save(f, 41022)


@fig(41023)
def f41023():
    f, ax = new_ax(6.4, 3.6)
    axis_line(ax, -4.6, 4.8)
    conv_lens(ax, 0, 3.4)
    for s in (-1, 1):
        dot(ax, s * 2, 0, 'F', dx=-0.12, dy=-0.45)
    ray(ax, (-4, -1), (0, 1), color=RED, lw=1.8, frac=0.28)
    ends = {'甲': (4, -1), '乙': (4, 3), '丙': (4, 0), '丁': (4, 1)}
    for lab, p1 in ends.items():
        ray(ax, (0, 1), p1, color=INK, lw=1.5, frac=0.75)
        txt(ax, p1[0] + 0.15, p1[1] + (0.12 if lab == '丙' else -0.12), lab, fs=14)
    ax.set_xlim(-4.7, 4.9)
    ax.set_ylim(-1.9, 3.2)
    save(f, 41023)


@fig(41024)
def f41024():
    f, ax = new_ax(6.4, 3.2)
    ax.add_patch(Rectangle((-1, -1.3), 2, 2.6, facecolor='#eeeeee', edgecolor=INK, lw=1.6))
    txt(ax, -0.18, -0.15, '?', fs=22)
    for y in (0.7, 0, -0.7):
        ray(ax, (-3.6, y), (-1, y), color=RED, lw=1.6)
        # 出射光:看起來像從盒子左側 (-2,0) 發散出來
        d = np.array([1 - (-2), y])
        d = d / np.linalg.norm(d)
        ray(ax, (1, y), (3.6, y + 2.6 * d[1] / d[0]), color=RED, lw=1.6)
    ax.set_xlim(-3.7, 3.7)
    ax.set_ylim(-1.6, 1.6)
    save(f, 41024)


@fig(41025)
def f41025():
    f, ax = plt.subplots(figsize=(6.4, 3.6), dpi=200)
    ax.set_aspect('equal')
    ax.set_xlim(-5, 8)
    ax.set_ylim(-3, 2)
    ax.set_xticks(range(-5, 9))
    ax.set_yticks(range(-3, 3))
    ax.grid(color='#cccccc', lw=0.8)
    ax.tick_params(length=0, labelbottom=False, labelleft=False)
    for s in ax.spines.values():
        s.set_color('#cccccc')
    ax.plot([-5, 8], [0, 0], color=INK, lw=1.3)
    ax.add_patch(Ellipse((0, 0), 0.3, 3.8, fill=False, color=INK, lw=1.6))
    for s in (-1, 1):
        dot(ax, s * 2, 0, 'F', dx=-0.15, dy=-0.5)
    obj_arrow(ax, -3, 1.0)
    txt(ax, -3.9, 1.15, '物體', color=BLUE, fs=12)
    save(f, 41025)


@fig(41026)
def f41026():
    f, ax = plt.subplots(figsize=(6.0, 4.5), dpi=200)
    ax.set_aspect('equal')
    ax.set_xlim(-6, 2)
    ax.set_ylim(-2, 4)
    ax.set_xticks(range(-6, 3))
    ax.set_yticks(range(-2, 5))
    ax.grid(color='#cccccc', lw=0.8)
    ax.tick_params(length=0, labelbottom=False, labelleft=False)
    for s in ax.spines.values():
        s.set_color('#cccccc')
    ax.plot([0, 0], [1, 3], color=INK, lw=3)
    for y in np.linspace(1, 3, 9):
        ax.plot([0, 0.2], [y, y + 0.14], color=INK, lw=1)
    txt(ax, 0.3, 1.8, '平面鏡', fs=12)
    ax.plot([-2], [0], 'o', ms=8, color=RED)
    txt(ax, -2.2, -0.55, 'E(眼睛)', color=RED, fs=12)
    for lab, (x, y) in {'A': (-1, 3), 'B': (-4, 2), 'C': (-1, -1), 'D': (-3, 1)}.items():
        dot(ax, x, y, lab, dx=0.1, dy=0.1, color=BLUE, fs=14)
    save(f, 41026)


@fig(41027)
def f41027():
    f, ax = new_ax(5.6, 3.8)
    hatch_line(ax, 0, 0, 4.8, 0, side=(0, -1), n=18)
    hatch_line(ax, 0, 0, 0, 3.0, side=(-1, 0), n=12)
    a = np.radians(40)
    hit = (2.6, 0)
    p0 = (hit[0] + 2.4 * np.cos(a), 2.4 * np.sin(a))
    ray(ax, p0, hit, color=RED, lw=1.8)
    arc(ax, hit[0], 0, 0.7, 0, 40, color=INK, lw=1.3)
    txt(ax, hit[0] + 0.78, 0.18, '40°', fs=13)
    txt(ax, 3.6, 1.75, '入射光', color=RED, fs=13)
    txt(ax, 3.4, -0.6, '鏡 1', fs=13)
    txt(ax, -0.75, 2.4, '鏡 2', fs=13)
    ax.set_xlim(-0.9, 5.0)
    ax.set_ylim(-0.8, 3.1)
    save(f, 41027)


# ───────────────────────── 波動與聲音 ─────────────────────────
@fig(41028)
def f41028():
    f, ax = graph(6.4, 3.4)
    x = np.linspace(0, 20, 600)
    ax.plot(x, 3 * np.sin(2 * np.pi * x / 8), color=BLUE, lw=1.8)
    ax.axhline(0, color=INK, lw=1.0)
    ax.set_xlim(0, 20.5)
    ax.set_ylim(-4, 4)
    ax.set_xticks(range(0, 21, 2))
    ax.set_yticks(range(-4, 5, 1))
    finish(ax, '位置(cm)', '位移(cm)')
    save(f, 41028)


@fig(41029)
def f41029():
    f, ax = graph(6.4, 3.4)
    x = np.linspace(0, 50, 600)
    ax.plot(x, 5 * np.sin(2 * np.pi * x / 20), color=BLUE, lw=1.8)
    ax.axhline(0, color=INK, lw=1.0)
    ax.set_xlim(0, 51)
    ax.set_ylim(-7, 7)
    ax.set_xticks(range(0, 51, 5))
    ax.set_yticks(range(-6, 7, 2))
    finish(ax, '位置(cm)', '位移(cm)')
    save(f, 41029)


@fig(41030)
def f41030():
    f, axs = plt.subplots(1, 2, figsize=(6.4, 3.0), dpi=200)
    wave_panel(axs[0], 3, 4, '甲')
    wave_panel(axs[1], 1.5, 4, '乙')
    f.tight_layout()
    save(f, 41030)


@fig(41031)
def f41031():
    f, axs = plt.subplots(2, 2, figsize=(6.4, 4.4), dpi=200)
    spec = [('甲', 2, 3), ('乙', 1, 6), ('丙', 3.5, 2), ('丁', 2.5, 4)]
    for a, (t, amp, n) in zip(axs.flat, spec):
        wave_panel(a, amp, n, t)
    f.tight_layout()
    save(f, 41031)


@fig(41032)
def f41032():
    f, ax = graph(6.4, 3.4)
    t = np.linspace(0, 1.2, 600)
    ax.plot(t, 2 * np.sin(2 * np.pi * t / 0.4), color=BLUE, lw=1.8)
    ax.axhline(0, color=INK, lw=1.0)
    ax.set_xlim(0, 1.22)
    ax.set_ylim(-3, 3)
    ax.set_xticks([round(0.1 * i, 1) for i in range(13)])
    ax.set_xticklabels(['0' if i == 0 else (f'{0.1 * i:.1f}' if i % 2 == 0 else '') for i in range(13)])
    ax.set_yticks(range(-3, 4))
    finish(ax, '時間(s)', '位移(cm)')
    save(f, 41032)


@fig(41033)
def f41033():
    f, axs = plt.subplots(1, 2, figsize=(7.0, 3.2), dpi=200)
    for a in axs:
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
        a.axhline(0, color=INK, lw=1.0)
    x = np.linspace(0, 10, 500)
    axs[0].plot(x, 2 * np.sin(2 * np.pi * x / 4), color=BLUE, lw=1.8)
    axs[0].set_xlim(0, 10.2)
    axs[0].set_ylim(-3, 3)
    axs[0].set_xticks(range(0, 11, 1))
    axs[0].set_xticklabels([str(i) if i % 2 == 0 else '' for i in range(11)])
    axs[0].set_yticks([-2, 0, 2])
    finish(axs[0], '位置(m)', '位移(cm)')
    axs[0].set_title('(一)某時刻的波形', fontproperties=P(13))
    t = np.linspace(0, 1.5, 500)
    axs[1].plot(t, 2 * np.sin(2 * np.pi * t / 0.5), color=RED, lw=1.8)
    axs[1].set_xlim(0, 1.53)
    axs[1].set_ylim(-3, 3)
    axs[1].set_xticks([0.25 * i for i in range(7)])
    axs[1].set_xticklabels(['0', '', '0.5', '', '1.0', '', '1.5'])
    axs[1].set_yticks([-2, 0, 2])
    finish(axs[1], '時間(s)', '位移(cm)')
    axs[1].set_title('(二)某點的振動', fontproperties=P(13))
    f.tight_layout()
    save(f, 41033)


@fig(41034)
def f41034():
    f, ax = graph(6.4, 3.0)
    t = np.linspace(0, 0.5, 3000)

    def pulse(t0, a):
        return a * np.exp(-((t - t0) / 0.006) ** 2) * np.sin(2 * np.pi * (t - t0) / 0.006)
    y = pulse(0.0, 3.0) + pulse(0.12, 1.0) + pulse(0.40, 1.8)
    ax.plot(t, y, color=BLUE, lw=1.4)
    ax.set_xlim(-0.012, 0.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xticks([0.04 * i for i in range(13)])
    ax.set_xticklabels(['0' if i == 0 else (f'{0.04 * i:.2f}' if i % 2 == 0 else '') for i in range(13)])
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    finish(ax, '時間(s)', '')
    ax.grid(axis='y', visible=False)
    save(f, 41034)


@fig(41035)
def f41035():
    f, ax = new_ax(6.6, 2.6)
    k = 2 * np.pi / 20
    for u in np.arange(1, 59.01, 1.0):
        x = u - 1.8 * np.sin(k * (u - 5))
        ax.plot([x, x], [1.0, 2.6], color=BLUE, lw=1.3)
    ax.plot([0, 60], [0.6, 0.6], color=INK, lw=1.4)
    for c in range(0, 61):
        hgt = 0.35 if c % 10 == 0 else (0.25 if c % 5 == 0 else 0.13)
        ax.plot([c, c], [0.6, 0.6 - hgt], color=INK, lw=0.9)
        if c % 10 == 0:
            txt(ax, c, -0.1, str(c), fs=12, ha='center', va='top')
    txt(ax, 61.2, 0.2, 'cm', fs=12)
    ax.set_xlim(-2, 65)
    ax.set_ylim(-0.9, 2.8)
    ax.set_aspect(6)
    save(f, 41035)


# ───────────────────────── 力與運動 ─────────────────────────
@fig(41036)
def f41036():
    f, ax = graph(5.6, 3.8)
    ax.plot([0, 6], [0, 24], color=BLUE, lw=2)
    ax.set_xlim(0, 6.2)
    ax.set_ylim(0, 26)
    ax.set_xticks(range(0, 7))
    ax.set_yticks(range(0, 25, 4))
    finish(ax, '時間(s)', '位置(m)')
    save(f, 41036)


@fig(41037)
def f41037():
    f, ax = graph(5.8, 3.8)
    ax.plot([0, 2, 5, 7], [0, 6, 6, 14], color=BLUE, lw=2)
    ax.set_xlim(0, 7.3)
    ax.set_ylim(0, 16)
    ax.set_xticks(range(0, 8))
    ax.set_yticks(range(0, 17, 2))
    finish(ax, '時間(s)', '位置(m)')
    save(f, 41037)


@fig(41038)
def f41038():
    f, ax = graph(5.8, 3.6)
    ax.plot([0, 4, 8], [0, 12, 12], color=BLUE, lw=2)
    ax.set_xlim(0, 8.3)
    ax.set_ylim(0, 15)
    ax.set_xticks(range(0, 9))
    ax.set_yticks(range(0, 16, 3))
    finish(ax, '時間(s)', '速度(m/s)')
    save(f, 41038)


@fig(41039)
def f41039():
    f, ax = graph(6.0, 3.6)
    ts = [0, 2, 4, 7, 9]
    vs = [0, 2, 8, 8, 0]
    ax.plot(ts, vs, color=BLUE, lw=2)
    for lab, (a, b) in zip('甲乙丙丁', zip(range(4), range(1, 5))):
        xm = (ts[a] + ts[b]) / 2
        ym = (vs[a] + vs[b]) / 2
        off = {'甲': (0.15, 0.9), '乙': (-0.7, 0.6), '丙': (-0.2, 0.7), '丁': (0.25, 0.4)}[lab]
        txt(ax, xm + off[0], ym + off[1], lab, color=RED, fs=14)
    ax.set_xlim(0, 9.5)
    ax.set_ylim(0, 10.5)
    ax.set_xticks(range(0, 10))
    ax.set_yticks(range(0, 11, 2))
    finish(ax, '時間(s)', '速度(m/s)')
    save(f, 41039)


@fig(41040)
def f41040():
    f, ax = new_ax(6.4, 2.8)
    ax.plot([-4, 4], [0, 0], color=INK, lw=1.6)
    ax.add_patch(Rectangle((-1, 0), 2, 1.4, facecolor='#eeeeee', edgecolor=INK, lw=1.6))
    farrow(ax, (1, 1.0), (3.4, 1.0))
    txt(ax, 2.0, 1.15, '8 N', color=RED, fs=13)
    farrow(ax, (1, 0.4), (1.9, 0.4))
    txt(ax, 2.0, 0.28, '2 N', color=RED, fs=13)
    farrow(ax, (-1, 0.7), (-2.6, 0.7))
    txt(ax, -2.45, 0.86, '3 N', color=RED, fs=13)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.3, 1.8)
    save(f, 41040)


@fig(41041)
def f41041():
    f, ax = new_ax(6.0, 3.8)
    th = np.radians(30)
    ax.add_patch(Polygon([(0, 0), (6, 0), (6, 6 * np.tan(th))], closed=True, facecolor='#f2f2f2', edgecolor=INK, lw=1.6))
    u = np.array([np.cos(th), np.sin(th)])
    n = np.array([-np.sin(th), np.cos(th)])
    base = 3.2 * u
    w, h = 1.2, 0.8
    corners = [base - u * w / 2, base + u * w / 2, base + u * w / 2 + n * h, base - u * w / 2 + n * h]
    ax.add_patch(Polygon(corners, closed=True, facecolor='#dfe8f5', edgecolor=INK, lw=1.6))
    c = base + n * h / 2
    L = 1.3
    dirs = {'甲': u, '乙': np.array([0, -1]), '丙': n, '丁': -u}
    for lab, d in dirs.items():
        e = c + d * (L + 0.4 if lab in '甲丁' else L)
        farrow(ax, tuple(c), tuple(e), color=INK, lw=1.6)
        lp = e + d * 0.3
        txt(ax, lp[0] - 0.15, lp[1] - 0.15, lab, fs=14)
    arc(ax, 0, 0, 0.9, 0, 30, color=INK, lw=1.2)
    txt(ax, 1.0, 0.12, '30°', fs=12)
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.3, 4.3)
    save(f, 41041)


@fig(41042)
def f41042():
    f, ax = graph(6.0, 3.8)
    ax.plot([0, 14], [10, 10], color=BLUE, lw=2)
    ax.plot([0, 12], [0, 24], color=RED, lw=2)
    txt(ax, 12.4, 10.6, '甲', color=BLUE, fs=14)
    txt(ax, 12.2, 22.5, '乙', color=RED, fs=14)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 26)
    ax.set_xticks(range(0, 15, 2))
    ax.set_yticks(range(0, 27, 4))
    finish(ax, '時間(s)', '速度(m/s)')
    save(f, 41042)


@fig(41043)
def f41043():
    f, ax = graph(5.6, 3.8)
    ax.plot([0, 4], [0, 8], color=BLUE, lw=2)
    ax.plot([0, 4], [0, 16], color=RED, lw=2)
    txt(ax, 3.55, 6.0, 'A', color=BLUE, fs=14)
    txt(ax, 1.65, 7.5, 'B', color=RED, fs=14)
    ax.set_xlim(0, 4.2)
    ax.set_ylim(0, 10)
    ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])
    ax.set_xticklabels(['0', '', '1', '', '2', '', '3', '', '4'])
    ax.set_yticks(range(0, 11, 2))
    finish(ax, '加速度(m/s²)', '外力(N)')
    save(f, 41043)


# ───────────────────────── 功與能量 ─────────────────────────
def hang_weight(ax, x, ytop, label, w=0.7, h=0.6, color='#dfe8f5'):
    ax.plot([x, x], [ytop, ytop - 0.4], color=INK, lw=1.3)
    ax.add_patch(Rectangle((x - w / 2, ytop - 0.4 - h), w, h, facecolor=color, edgecolor=INK, lw=1.5))
    txt(ax, x, ytop - 0.4 - h / 2, label, fs=12, ha='center', va='center')


def fulcrum(ax, x, y):
    ax.add_patch(Polygon([(x, y), (x - 0.35, y - 0.6), (x + 0.35, y - 0.6)], closed=True, facecolor='#999999', edgecolor=INK, lw=1.3))


@fig(41044)
def f41044():
    f, ax = new_ax(6.0, 3.0)
    ax.plot([-3, 3], [0, 0], color=INK, lw=4)
    fulcrum(ax, 0, -0.04)
    hang_weight(ax, -1.25, 0, '6 公斤重', w=1.4)
    hang_weight(ax, 2.5, 0, '?', w=0.8)
    for x0, x1, s in [(-1.25, 0, '20 cm'), (0, 2.5, '40 cm')]:
        ax.annotate('', xy=(x0, 0.35), xytext=(x1, 0.35), arrowprops=dict(arrowstyle='<->', color=INK, lw=1.1))
        txt(ax, (x0 + x1) / 2, 0.45, s, fs=12, ha='center')
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-1.3, 0.9)
    save(f, 41044)


@fig(41045)
def f41045():
    f, ax = new_ax(6.4, 3.2)
    ax.add_patch(Rectangle((-4.6, -0.12), 9.2, 0.24, facecolor='#f2e6cc', edgecolor=INK, lw=1.5))
    for i in range(-4, 5):
        ax.plot([i], [0], 'o', ms=4.5, color=INK, mfc='white')
        if i != 0:
            txt(ax, i, 0.22, str(abs(i)), fs=11, ha='center')
    fulcrum(ax, 0, -0.13)

    def stack(x, n):
        ax.plot([x, x], [0, -0.45], color=INK, lw=1.2)
        for k in range(n):
            ax.add_patch(Rectangle((x - 0.25, -0.45 - 0.42 * (k + 1)), 0.5, 0.38, facecolor='#dfe8f5', edgecolor=INK, lw=1.3))
    stack(-3, 2)
    stack(-2, 1)
    ax.plot([2.5], [-1.0], alpha=0)
    txt(ax, 2.6, -1.2, '掛 4 個?', color=RED, fs=13, ha='center')
    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-1.5, 0.6)
    save(f, 41045)


def pulley(ax, cx, cy, r=0.45):
    circle(ax, cx, cy, r, color=INK, lw=1.6)
    ax.plot([cx], [cy], 'o', ms=3.5, color=INK)


@fig(41046)
def f41046():
    f, ax = new_ax(6.4, 4.0)
    for x0 in (-3.4, 0.8):
        ax.plot([x0, x0 + 2.6], [4, 4], color=INK, lw=2.4)
        for t in np.linspace(x0, x0 + 2.6, 12):
            ax.plot([t, t + 0.15], [4, 4.18], color=INK, lw=0.9)
    # 甲:定滑輪
    cx, cy, r = -2.1, 3.0, 0.45
    ax.plot([cx, cx], [4, cy], color=INK, lw=1.4)
    pulley(ax, cx, cy, r)
    ax.plot([cx - r, cx - r], [cy, 1.0], color=INK, lw=1.3)
    ax.add_patch(Rectangle((cx - r - 0.4, 0.3), 0.8, 0.7, facecolor='#dfe8f5', edgecolor=INK, lw=1.4))
    txt(ax, cx - r, 0.65, '40 N', fs=11, ha='center', va='center')
    ax.plot([cx + r, cx + r], [cy, 1.2], color=INK, lw=1.3)
    farrow(ax, (cx + r, 1.2), (cx + r, 0.5))
    txt(ax, cx + r + 0.12, 0.6, 'F甲', color=RED, fs=13)
    txt(ax, -2.35, -0.35, '甲', fs=14)
    # 乙:動滑輪
    cx, cy = 2.1, 1.7
    ax.plot([cx - r, cx - r], [4, cy], color=INK, lw=1.3)
    ax.plot([cx + r, cx + r], [cy, 3.3], color=INK, lw=1.3)
    farrow(ax, (cx + r, 3.25), (cx + r, 3.85))
    txt(ax, cx + r + 0.12, 3.35, 'F乙', color=RED, fs=13)
    pulley(ax, cx, cy, r)
    ax.plot([cx, cx], [cy, 1.0], color=INK, lw=1.4)
    ax.add_patch(Rectangle((cx - 0.4, 0.3), 0.8, 0.7, facecolor='#dfe8f5', edgecolor=INK, lw=1.4))
    txt(ax, cx, 0.65, '40 N', fs=11, ha='center', va='center')
    txt(ax, 1.85, -0.35, '乙', fs=14)
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-0.5, 4.3)
    save(f, 41046)


@fig(41047)
def f41047():
    f, ax = new_ax(5.4, 4.2)
    ax.plot([-1.6, 2.6], [4.2, 4.2], color=INK, lw=2.4)
    for t in np.linspace(-1.6, 2.6, 16):
        ax.plot([t, t + 0.15], [4.2, 4.38], color=INK, lw=0.9)
    r = 0.45
    fx, fy = 1.0, 3.4      # 定滑輪
    mx, my = 0.1, 1.7      # 動滑輪(右緣 x=0.55 與定滑輪左緣 x=0.55 同一直線)
    ax.plot([fx, fx], [4.2, fy], color=INK, lw=1.4)
    pulley(ax, fx, fy, r)
    ax.plot([mx - r, mx - r], [4.2, my], color=INK, lw=1.3)           # 固定端
    ax.plot([mx + r, mx + r], [my, fy], color=INK, lw=1.3)            # 往上繞定滑輪
    th = np.linspace(0, np.pi, 40)
    ax.plot(fx + r * np.cos(np.pi - th), fy + r * np.sin(np.pi - th), color=INK, lw=1.3)
    ax.plot([fx + r, fx + r], [fy, 1.3], color=INK, lw=1.3)
    farrow(ax, (fx + r, 1.3), (fx + r, 0.6))
    txt(ax, fx + r + 0.12, 0.7, 'F', color=RED, fs=14)
    pulley(ax, mx, my, r)
    ax.plot([mx, mx], [my, 0.95], color=INK, lw=1.4)
    ax.add_patch(Rectangle((mx - 0.5, 0.25), 1.0, 0.7, facecolor='#dfe8f5', edgecolor=INK, lw=1.4))
    txt(ax, mx, 0.6, '60 N', fs=12, ha='center', va='center')
    ax.set_xlim(-1.7, 2.7)
    ax.set_ylim(0.0, 4.5)
    save(f, 41047)


@fig(41048)
def f41048():
    f, ax = new_ax(6.4, 3.6)
    pts = [(0, 10), (4, 2), (7, 6), (10.5, 0.6)]
    xs, ys = [], []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        t = np.linspace(0, 1, 80)
        xs += list(x0 + (x1 - x0) * t)
        ys += list(y0 + (y1 - y0) * (1 - np.cos(np.pi * t)) / 2)
    ax.plot(xs, ys, color=INK, lw=2)
    ax.plot([-1.2, 11], [0, 0], color=INK, lw=1.4)
    for lab, (x, y) in zip('ABC', pts[:3]):
        ax.plot([x], [y], 'o', ms=6, color=BLUE)
        txt(ax, x - 0.15, y + 0.6, lab, color=BLUE, fs=14)
        ax.plot([x, x], [0, y], color=GREY, lw=1.1, ls='--')
        txt(ax, x + 0.15, y / 2 - 0.4, f'{y} m', fs=12)
    ax.add_patch(Rectangle((-0.4, 10.0), 0.8, 0.45, facecolor='#d0342c', edgecolor=INK, lw=1))
    ax.set_xlim(-1.2, 11)
    ax.set_ylim(-0.5, 11.6)
    ax.set_aspect(0.55)
    save(f, 41048)


@fig(41049)
def f41049():
    f, ax = new_ax(6.6, 2.8)
    for ox, L, lab in [(0, 3.0, '甲'), (4.0, 6.0, '乙')]:
        h = 1.5
        b = np.sqrt(L ** 2 - h ** 2)
        ax.add_patch(Polygon([(ox, 0), (ox + b, 0), (ox + b, h)], closed=True, facecolor='#f2f2f2', edgecolor=INK, lw=1.6))
        ang = np.arctan2(h, b)
        mx, my = ox + b / 2, h / 2
        txt(ax, mx - 0.5 * np.sin(ang) - 0.5, my + 0.35, f'{L:g} m', fs=12)
        txt(ax, ox + b + 0.12, h / 2 - 0.1, '1.5 m', fs=12)
        txt(ax, ox + b / 2 - 0.1, -0.55, lab, fs=14)
    ax.set_xlim(-0.2, 10.4)
    ax.set_ylim(-0.75, 2.2)
    save(f, 41049)


@fig(41050)
def f41050():
    f, ax = new_ax(6.4, 2.8)
    ax.add_patch(Rectangle((0, 0), 100, 3, facecolor='#f2e6cc', edgecolor=INK, lw=1.5))
    for c in range(0, 101, 10):
        ax.plot([c, c], [3, 2.0], color=INK, lw=0.9)
        txt(ax, c, 3.6, str(c), fs=11, ha='center')
    ax.add_patch(Polygon([(40, 0), (36, -7), (44, -7)], closed=True, facecolor='#999999', edgecolor=INK, lw=1.3))
    ax.plot([0.8, 0.8], [0, -5], color=INK, lw=1.3)
    ax.add_patch(Rectangle((-5, -12), 11.6, 7, facecolor='#dfe8f5', edgecolor=INK, lw=1.4))
    txt(ax, 0.8, -8.6, 'W', fs=13, ha='center', va='center')
    txt(ax, 105, 3.6, 'cm', fs=11)
    ax.set_xlim(-6, 112)
    ax.set_ylim(-13, 7)
    ax.set_aspect(1.4)
    save(f, 41050)


@fig(41051)
def f41051():
    f, ax = new_ax(6.0, 3.8)
    L = 4.0
    ax.plot([-1.2, 1.2], [0, 0], color=INK, lw=2.4)
    for t in np.linspace(-1.2, 1.2, 9):
        ax.plot([t, t + 0.15], [0, 0.18], color=INK, lw=0.9)
    th = np.radians(np.linspace(-44, 44, 100))
    ax.plot(L * np.sin(th), -L * np.cos(th), color=GREY, lw=1.1, ls='--')
    ang = {'A': -40, 'B': -25, 'C': 0, 'D': 15, 'E': 25}
    hcm = {k: 100 * (1 - np.cos(np.radians(v))) for k, v in ang.items()}
    for k, v in ang.items():
        a = np.radians(v)
        x, y = L * np.sin(a), -L * np.cos(a)
        if k == 'A':
            ax.plot([0, x], [0, y], color=INK, lw=1.3)
            ax.plot([x], [y], 'o', ms=12, color=BLUE)
        else:
            ax.plot([x], [y], 'o', ms=5, color=INK)
        lab = k if k == 'C' else f'{k}({hcm[k]:.0f} cm)'
        if v < 0:
            txt(ax, x - 0.25, y - 0.05, lab, fs=12, ha='right', va='center')
        elif v == 0:
            txt(ax, x, y - 0.3, lab, fs=12, ha='center', va='top')
        elif k == 'D':
            txt(ax, x + 0.1, y - 0.25, lab, fs=12, ha='center', va='top')
        else:
            txt(ax, x + 0.25, y + 0.05, lab, fs=12, ha='left', va='center')
    ax.set_xlim(-5.4, 5.4)
    ax.set_ylim(-4.8, 0.3)
    save(f, 41051)


# ───────────────────────── 溫度與熱 ─────────────────────────
@fig(41052)
def f41052():
    f, ax = graph(6.0, 3.8)
    t = [0, 2, 6, 14, 20]
    T = [-20, 0, 0, 100, 100]
    ax.plot(t, T, color=BLUE, lw=2)
    labs = {'甲': (0.5, -5), '乙': (3.8, 6), '丙': (8.0, 52), '丁': (16.8, 106)}
    for k, (x, y) in labs.items():
        txt(ax, x, y, k, color=RED, fs=14)
    ax.set_xlim(0, 20.5)
    ax.set_ylim(-30, 120)
    ax.set_xticks(range(0, 21, 2))
    ax.set_yticks(range(-20, 121, 20))
    finish(ax, '加熱時間(min)', '溫度(°C)')
    save(f, 41052)


@fig(41053)
def f41053():
    f, ax = graph(6.0, 3.8)
    ax.plot([0, 4, 10, 14], [20, 80, 80, 140], color=BLUE, lw=2)
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 160)
    ax.set_xticks(range(0, 15, 1))
    ax.set_xticklabels([str(i) if i % 2 == 0 else '' for i in range(15)])
    ax.set_yticks(range(0, 161, 20))
    finish(ax, '加熱時間(min)', '溫度(°C)')
    save(f, 41053)


@fig(41054)
def f41054():
    f, ax = graph(5.8, 3.8)
    ax.plot([0, 5], [20, 40], color=BLUE, lw=2)
    ax.plot([0, 5], [20, 60], color=RED, lw=2)
    txt(ax, 5.1, 39, '甲', color=BLUE, fs=14)
    txt(ax, 5.1, 59, '乙', color=RED, fs=14)
    ax.set_xlim(0, 5.6)
    ax.set_ylim(0, 70)
    ax.set_xticks(range(0, 6))
    ax.set_yticks(range(0, 71, 10))
    finish(ax, '加熱時間(min)', '溫度(°C)')
    save(f, 41054)


@fig(41055)
def f41055():
    f, ax = graph(5.8, 3.8)
    ax.plot([0, 6], [20, 50], color=BLUE, lw=2)
    ax.plot([0, 5], [20, 60], color=RED, lw=2)
    txt(ax, 6.05, 48, '水 200 g', color=BLUE, fs=12)
    txt(ax, 4.0, 63, '液體 X 250 g', color=RED, fs=12)
    ax.set_xlim(0, 7.6)
    ax.set_ylim(0, 70)
    ax.set_xticks(range(0, 8))
    ax.set_yticks(range(0, 71, 10))
    finish(ax, '加熱時間(min)', '溫度(°C)')
    save(f, 41055)


@fig(41056)
def f41056():
    f, ax = graph(5.8, 3.8)
    t = np.linspace(0, 10, 300)
    ax.plot(t, 40 + 40 * np.exp(-t / 1.8), color=RED, lw=2)
    ax.plot(t, 40 - 20 * np.exp(-t / 1.8), color=BLUE, lw=2)
    txt(ax, 0.3, 80, '熱水', color=RED, fs=13)
    txt(ax, 0.3, 12, '冷水', color=BLUE, fs=13)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 90)
    ax.set_xticks(range(0, 11, 2))
    ax.set_yticks(range(0, 91, 10))
    finish(ax, '時間(min)', '溫度(°C)')
    save(f, 41056)


@fig(41057)
def f41057():
    f, ax = new_ax(6.0, 2.6)
    lo, hi = -10, 5
    ax.add_patch(FancyBboxPatch((lo - 3, -0.35), hi - lo + 5, 0.7, boxstyle='round,pad=0,rounding_size=0.35',
                                facecolor='white', edgecolor=INK, lw=1.4))
    circle(ax, lo - 4.2, 0, 1.1, color=INK, lw=1.4)
    th = np.linspace(0, 2 * np.pi, 100)
    ax.fill(lo - 4.2 + 0.9 * np.cos(th), 0.9 * np.sin(th), color=RED)
    ax.add_patch(Rectangle((lo - 4.2, -0.15), -4 - (lo - 4.2), 0.3, color=RED))
    for c in range(lo, hi + 1):
        hgt = 0.9 if c % 10 == 0 else (0.65 if c % 5 == 0 else 0.4)
        ax.plot([c, c], [0.35, 0.35 + hgt], color=INK, lw=1.3)
        if c % 5 == 0:
            txt(ax, c, 1.45, str(c), fs=15, ha='center')
    txt(ax, hi + 2.2, 1.45, '°C', fs=15)
    ax.set_xlim(lo - 5.6, hi + 4)
    ax.set_ylim(-1.5, 2.4)
    ax.set_aspect(2.2)
    save(f, 41057)


@fig(41058)
def f41058():
    f, ax = graph(5.8, 3.8)
    ax.plot([0, 3000], [20, 80], color=BLUE, lw=2)
    ax.plot([0, 3000], [20, 50], color=RED, lw=2)
    txt(ax, 2450, 74, '甲(100 g)', color=BLUE, fs=12, ha='right')
    txt(ax, 3000, 43, '乙(200 g)', color=RED, fs=12, ha='right', va='top')
    ax.set_xlim(0, 3100)
    ax.set_ylim(0, 90)
    ax.set_xticks(range(0, 3001, 500))
    ax.set_yticks(range(0, 91, 10))
    finish(ax, '吸收的熱量(cal)', '溫度(°C)')
    save(f, 41058)


@fig(41059)
def f41059():
    f, ax = new_ax(6.0, 2.6)
    ax.add_patch(Rectangle((-0.8, -1.2), 0.8, 2.6, facecolor='#cccccc', edgecolor=INK, lw=1.4))
    ax.add_patch(Rectangle((0, 0.2), 5.0, 0.4, facecolor='#f0c9a8', edgecolor=INK, lw=1.4))
    ax.add_patch(Rectangle((0, -0.2), 5.0, 0.4, facecolor='#c9ced6', edgecolor=INK, lw=1.4))
    txt(ax, 5.2, 0.4, '銅', fs=13, va='center')
    txt(ax, 5.2, 0.0, '鐵', fs=13, va='center')
    txt(ax, -0.75, 1.6, '固定端', fs=12)
    ax.set_xlim(-1.0, 6.0)
    ax.set_ylim(-1.3, 2.0)
    save(f, 41059)
