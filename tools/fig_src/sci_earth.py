from fig_all import *   # plt, np, PF, fig, new_ax, save, txt, dot, circle, arc, INK/RED/BLUE/GREY
from matplotlib.patches import Rectangle, Polygon, Wedge, Circle as MC, Ellipse

plt.rcParams['hatch.linewidth'] = 0.9
PATS = ['', '...', '///', '---', '\\\\\\', 'xx']
WB = dict(boxstyle='round,pad=0.15', fc='white', ec='none')
LIGHT = '#dddddd'
SKYB = '#d6e6f7'


def lab(ax, x, y, s, fs=14, color=INK, box=True, **kw):
    kw.setdefault('ha', 'center'); kw.setdefault('va', 'center')
    if box:
        kw['bbox'] = WB
    txt(ax, x, y, s, color=color, fs=fs, **kw)


def arrow(ax, p0, p1, color=INK, lw=1.5, ms=14):
    ax.annotate('', xy=p1, xytext=p0, annotation_clip=False,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=ms, shrinkA=0, shrinkB=0))


def band(ax, x0, x1, y0, y1, pat, clip=None, lo=0, hi=None):
    y0 = max(y0, lo)
    if hi is not None:
        y1 = min(y1, hi)
    if y1 <= y0:
        return None
    r = Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor='white', edgecolor=INK, hatch=pat, lw=0)
    ax.add_patch(r)
    if clip is not None:
        r.set_clip_path(clip)
    return r


def hline_clip(ax, x0, x1, y, clip, top=4):
    if y <= 0 or y >= top:
        return
    l, = ax.plot([x0, x1], [y, y], color=INK, lw=1.3)
    l.set_clip_path(clip)


def compass(ax, x, y, L=0.6, fs=13):
    arrow(ax, (x, y - L / 2), (x, y + L / 2), lw=1.4)
    lab(ax, x, y + L / 2 + 0.22, '北', fs=fs, box=False)


# ═══════════════ 地層 ═══════════════
@fig(41120)
def f41120():
    f, ax = new_ax(6, 4.2)
    H = [(0, 1.3, '甲', 1), (1.3, 2.6, '乙', 2), (2.6, 3.9, '丙', 3)]
    for y0, y1, n, p in H:
        band(ax, 0, 6, y0, y1, PATS[p])
        ax.plot([0, 6], [y1, y1], color=INK, lw=1.3)
    # 火成岩體丁:由底部侵入,貫穿甲、乙,頂端止於丙的底面
    dk = Polygon([(2.4, 0), (3.6, 0), (3.3, 1.3), (3.2, 2.6), (2.7, 2.6), (2.6, 1.3)],
                 closed=True, facecolor='#f3d5d3', edgecolor=INK, hatch='++', lw=1.4, zorder=3)
    ax.add_patch(dk)
    ax.add_patch(Rectangle((0, 0), 6, 3.9, fill=False, ec=INK, lw=1.5))
    lab(ax, 1.0, 0.65, '甲'); lab(ax, 1.0, 1.95, '乙'); lab(ax, 1.0, 3.25, '丙')
    lab(ax, 2.95, 1.2, '丁', color=RED)
    save(f, 41120)


@fig(41121)
def f41121():
    f, ax = new_ax(6.4, 4.4)
    fx0, fx1 = 2.4, 3.2      # 斷層線 (2.4,0)-(3.2,3)
    left = Polygon([(0, 0), (fx0, 0), (fx1, 3), (0, 3)], closed=True, visible=False)
    right = Polygon([(fx0, 0), (6, 0), (6, 3), (fx1, 3)], closed=True, visible=False)
    ax.add_patch(left); ax.add_patch(right)
    names = {0: '甲', 1: '乙', 2: '丙'}
    pat = {-1: PATS[5], 0: PATS[1], 1: PATS[2], 2: PATS[3]}
    # 左塊(上盤)相對上移 0.5
    for k in (-1, 0, 1, 2):
        band(ax, 0, 6, k + 0.5, k + 1.5, pat[k], clip=left, hi=3)
        hline_clip(ax, 0, 6, k + 1.5, left, top=3)
    for k in (0, 1, 2):
        band(ax, 0, 6, k, k + 1, pat[k], clip=right)
        hline_clip(ax, 0, 6, k + 1, right)
    # 侵蝕面以上的丁
    band(ax, 0, 6, 3, 3.8, PATS[4])
    ax.plot([0, 6], [3, 3], color=INK, lw=1.8)
    ax.plot([fx0, fx1], [0, 3], color=INK, lw=2.4)
    # 岩脈戊:貫穿全部(含丁)
    ax.add_patch(Polygon([(4.55, 0), (5.0, 0), (5.05, 3.8), (4.65, 3.8)], closed=True,
                         facecolor='#f3d5d3', edgecolor=INK, hatch='++', lw=1.4, zorder=3))
    ax.add_patch(Rectangle((0, 0), 6, 3.8, fill=False, ec=INK, lw=1.5))
    for k in (0, 1, 2):
        lab(ax, 1.0, min(k + 1.0, 2.72), names[k], fs=13)
        lab(ax, 3.9, k + 0.5, names[k])
    lab(ax, 2.0, 3.4, '丁')
    lab(ax, fx0 + 0.25, 0.45, 'F', color=BLUE)
    lab(ax, 4.82, 2.0, '戊', color=RED)
    save(f, 41121)


@fig(41122)
def f41122():
    f, ax = new_ax(6.4, 4)
    xs = np.linspace(0, 6, 300)
    wav = 0.75 * np.sin(2 * np.pi * (xs - 0.6) / 4.2)
    box = Rectangle((0, 0), 6, 4, visible=False); ax.add_patch(box)
    bounds = [-2, -1, 0, 1, 2, 3, 4, 5]
    for i in range(len(bounds) - 1):
        p = ax.fill_between(xs, np.clip(bounds[i] + 0.9 + wav, 0, 4), np.clip(bounds[i + 1] + 0.9 + wav, 0, 4), facecolor='white',
                            edgecolor=INK, hatch=PATS[1 + i % 4], lw=0)
        p.set_clip_path(box)
        yy = bounds[i + 1] + 0.9 + wav
        yy = np.where((yy > 0) & (yy < 4), yy, np.nan)
        ax.plot(xs, yy, color=INK, lw=1.3)
    ax.add_patch(Rectangle((0, 0), 6, 4, fill=False, ec=INK, lw=1.5))
    lab(ax, 3.0, -0.35, '地表以下的岩層剖面', fs=12, box=False)
    save(f, 41122)


def fault_fig(qid, shift):
    f, ax = new_ax(6.4, 4.4)
    fx0, fx1 = 2.2, 3.8      # 斷層面向左下傾斜,左塊為上盤
    left = Polygon([(0, 0), (fx0, 0), (fx1, 4), (0, 4)], closed=True, visible=False)
    right = Polygon([(fx0, 0), (6, 0), (6, 4), (fx1, 4)], closed=True, visible=False)
    ax.add_patch(left); ax.add_patch(right)
    pat = {-1: PATS[5], 0: PATS[1], 1: PATS[2], 2: PATS[3], 3: PATS[4], 4: '++'}
    for k in range(-1, 5):
        band(ax, 0, 6, k + shift, k + 1 + shift, pat[k], clip=left, hi=4)
        hline_clip(ax, 0, 6, k + 1 + shift, left)
    for k in range(0, 4):
        band(ax, 0, 6, k, k + 1, pat[k], clip=right)
        hline_clip(ax, 0, 6, k + 1, right)
    ax.plot([fx0, fx1], [0, 4], color=RED, lw=2.6)
    ax.add_patch(Rectangle((0, 0), 6, 4, fill=False, ec=INK, lw=1.5))
    lab(ax, 3.45, 3.55, '斷層面', color=RED, fs=12, ha='left')
    save(f, qid)


@fig(41123)
def f41123():
    fault_fig(41123, -0.6)      # 上盤下移:正斷層


@fig(41124)
def f41124():
    fault_fig(41124, 0.6)       # 上盤上移:逆斷層


@fig(41125)
def f41125():
    f, ax = new_ax(6.4, 4.4)
    xs = np.linspace(0, 6, 300)
    ero = 2.4 + 0.12 * np.sin(xs * 2.3) + 0.06 * np.sin(xs * 5.1)
    low = Polygon(np.vstack([np.c_[xs, ero], [[6, 0], [0, 0]]]), closed=True, visible=False)
    ax.add_patch(low)
    cs = [-3, 1.6, 3.0, 6]
    pats = [PATS[1], PATS[2], PATS[3]]
    for i in range(3):
        p = ax.fill_between(xs, np.clip(cs[i] - 0.3 * xs, 0, ero), np.clip(cs[i + 1] - 0.3 * xs, 0, ero), facecolor='white', edgecolor=INK,
                            hatch=pats[i], lw=0)
        p.set_clip_path(low)
        if i < 2:
            yy = cs[i + 1] - 0.3 * xs
            ax.plot(xs, np.where((yy > 0) & (yy < ero), yy, np.nan), color=INK, lw=1.3)
    ax.fill_between(xs, ero, 3.2, facecolor='white', edgecolor=INK, hatch=PATS[4], lw=0)
    ax.fill_between(xs, 3.2, 4.0, facecolor='white', edgecolor=INK, hatch='++', lw=0)
    ax.plot(xs, ero, color=INK, lw=2.0)
    ax.plot([0, 6], [3.2, 3.2], color=INK, lw=1.3)
    ax.add_patch(Rectangle((0, 0), 6, 4, fill=False, ec=INK, lw=1.5))
    lab(ax, 0.8, 0.6, '甲'); lab(ax, 3.0, 1.35, '乙'); lab(ax, 5.2, 1.85, '丙')
    lab(ax, 3.0, 2.82, '丁'); lab(ax, 3.0, 3.6, '戊')
    save(f, 41125)


@fig(41135)
def f41135():
    f, ax = new_ax(6, 4.4)
    cols = [(0.6, '甲地', [('A', '●', PATS[1]), ('B', '▲', PATS[2]), ('C', '★', PATS[3])]),
            (3.6, '乙地', [('D', '▲', PATS[2]), ('E', '★', PATS[3]), ('F', '', PATS[4])])]
    for x0, name, layers in cols:
        for i, (n, sym, pt) in enumerate(layers):
            ax.add_patch(Rectangle((x0, i), 1.6, 1, facecolor='white', edgecolor=INK, hatch=pt, lw=1.4))
            if sym:
                for dx in (0.45, 1.15):
                    lab(ax, x0 + dx, i + 0.5, sym, fs=14)
            lab(ax, x0 + 1.95, i + 0.5, n, fs=14, box=False)
        lab(ax, x0 + 0.8, 3.35, name, fs=14, box=False)
    ax.plot([-0.2, 6.2], [-0.02, -0.02], color='white', lw=0.5)
    save(f, 41135)


# ═══════════════ 岩石循環 ═══════════════
def rock_cycle(qid):
    f, ax = new_ax(6.4, 4.4)
    N = {'岩漿': (0, 2.0), '火成岩': (-2.6, 0.5), '沉積物': (-1.5, -1.6), '沉積岩': (1.5, -1.6), '變質岩': (2.6, 0.5)}
    for k, (x, y) in N.items():
        txt(ax, x, y, k, fs=14, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.35', fc='white', ec=INK, lw=1.4))
    E = [('岩漿', '火成岩', '甲', (-0.35, 0.3)), ('沉積物', '沉積岩', '乙', (0, -0.32)),
         ('沉積岩', '變質岩', '丙', (0.38, -0.2)), ('變質岩', '岩漿', '丁', (0.35, 0.3)),
         ('火成岩', '沉積物', '戊', (-0.38, -0.2))]
    for a, b, n, (ox, oy) in E:
        pa, pb = np.array(N[a]), np.array(N[b])
        d = (pb - pa) / np.linalg.norm(pb - pa)
        s, e = pa + d * 0.75, pb - d * 0.75
        arrow(ax, tuple(s), tuple(e), color=BLUE, lw=1.6)
        m = (s + e) / 2
        lab(ax, m[0] + ox, m[1] + oy, n, color=RED, fs=14, box=False)
    ax.set_xlim(-3.4, 3.4); ax.set_ylim(-2.1, 2.4)
    save(f, qid)


@fig(41126)
def f41126():
    rock_cycle(41126)


@fig(41127)
def f41127():
    rock_cycle(41127)


# ═══════════════ 天氣圖 ═══════════════
def ell(ax, cx, cy, rx, ry, color=INK, lw=1.4, ls='-'):
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(cx + rx * np.cos(t), cy + ry * np.sin(t), color=color, lw=lw, ls=ls)


@fig(41128)
def f41128():
    f, ax = new_ax(6.4, 4.2)
    vals = [1004, 1008, 1012, 1016]
    for k, v in zip(range(1, 5), vals):
        c, r = -0.5 * k, 0.3 + 1.0 * k
        ell(ax, c, 0, r, 0.65 * r)
        # 數值標在左上方
        th = np.radians(128)
        lab(ax, c + r * np.cos(th), 0.65 * r * np.sin(th), str(v), fs=11)
    lab(ax, -0.5, 0, '低', color=RED, fs=16, box=False)
    pts = {'甲': (1.55, 0), '乙': (-4.05, 0), '丙': (-1.25, 1.81), '丁': (-1.25, -1.81)}
    for n, (x, y) in pts.items():
        ax.plot([x], [y], 'o', color=BLUE, ms=5)
        lab(ax, x + 0.3, y + 0.25, n, fs=13)
    compass(ax, 2.6, 1.6)
    save(f, 41128)


def hl_map(qid):
    f, ax = new_ax(6.4, 3.8)
    Hc, Lc = (-2.2, 0.6), (2.2, -0.6)
    for (cx, cy), vals, ch in [(Hc, [1020, 1016], '高'), (Lc, [1004, 1008], '低')]:
        for r, v in zip([1.0, 1.9], vals):
            ell(ax, cx, cy, r, 0.85 * r)
            th = np.radians(125)
            lab(ax, cx + r * np.cos(th), cy + 0.85 * r * np.sin(th), str(v), fs=11)
        lab(ax, cx, cy, ch, color=RED, fs=16, box=False)
    for n, (x, y) in {'甲': (Lc[0] + 1.45, Lc[1]), '乙': (Hc[0], Hc[1] - 1.23)}.items():
        ax.plot([x], [y], 'o', color=BLUE, ms=5)
        lab(ax, x - 0.3 if n == '乙' else x, y if n == '乙' else y - 0.3, n, fs=13)
    compass(ax, 4.0, 1.5)
    save(f, qid)


@fig(41129)
def f41129():
    hl_map(41129)


@fig(41130)
def f41130():
    hl_map(41130)


def front(ax, pts, kind, size=0.17, spacing=0.7, lw=2.0, bw=False):
    pts = np.asarray(pts, float)
    seg = np.diff(pts, axis=0); L = np.hypot(seg[:, 0], seg[:, 1]); cum = np.r_[0, np.cumsum(L)]
    cc = INK if bw else BLUE
    wc = INK if bw else RED
    lc = {'cold': cc, 'warm': wc, 'stat': INK, 'occl': INK if bw else '#7b3fa0'}[kind]
    ax.plot(pts[:, 0], pts[:, 1], color=lc, lw=lw)

    def at(s):
        i = int(np.clip(np.searchsorted(cum, s) - 1, 0, len(L) - 1))
        t = (s - cum[i]) / L[i]
        d = seg[i] / L[i]
        return pts[i] + t * seg[i], d

    def tri(p, d, n, c):
        ax.fill(*np.array([p - d * size, p + d * size, p + n * size * 1.6]).T, color=c, lw=0)

    def semi(p, d, n, c):
        th = np.linspace(0, np.pi, 30)
        q = np.array([p + size * (np.cos(t) * d + np.sin(t) * n) for t in th])
        ax.fill(q[:, 0], q[:, 1], color=c, lw=0)

    for k, s in enumerate(np.arange(spacing / 2, cum[-1] - size, spacing)):
        p, d = at(s)
        n = np.array([-d[1], d[0]])
        if kind == 'cold':
            tri(p, d, n, cc)
        elif kind == 'warm':
            semi(p, d, n, wc)
        elif kind == 'stat':
            tri(p, d, n, cc) if k % 2 == 0 else semi(p, d, -n, wc)
        else:
            oc = INK if bw else '#7b3fa0'
            tri(p, d, n, oc) if k % 2 == 0 else semi(p, d, n, oc)


@fig(41131)
def f41131():
    f, ax = new_ax(5.6, 4.2)
    t = np.linspace(0, 1, 60)
    xs = 1.6 - 3.2 * t + 0.25 * np.sin(np.pi * t)
    ys = 2.0 - 4.0 * t
    front(ax, np.c_[xs, ys], 'cold', size=0.2, spacing=0.75)
    for n, (x, y) in {'甲': (1.5, -0.9), '乙': (-1.5, 0.9)}.items():
        ax.plot([x], [y], 'o', color=INK, ms=6)
        lab(ax, x + 0.3, y + 0.25, n, fs=14, box=False)
    compass(ax, 2.6, 1.5)
    ax.plot([-2.6, 3.2], [-2.1, -2.1], color='white', lw=0.5)
    save(f, 41131)


@fig(41132)
def f41132():
    f, ax = new_ax(6.4, 3.4)
    items = [('甲', 'cold', 0, 1.6), ('乙', 'stat', 3.6, 1.6), ('丙', 'warm', 0, 0), ('丁', 'occl', 3.6, 0)]
    for n, kind, x0, y0 in items:
        xs = np.linspace(x0 + 0.5, x0 + 2.9, 30)
        front(ax, np.c_[xs, np.full_like(xs, y0)], kind, size=0.2, spacing=0.6, bw=True)
        lab(ax, x0 + 0.1, y0, n, fs=14, box=False)
    ax.plot([0, 6.6], [-0.6, -0.6], color='white', lw=0.5)
    ax.plot([0, 6.6], [2.2, 2.2], color='white', lw=0.5)
    save(f, 41132)


@fig(41133)
def f41133():
    f, ax = new_ax(6.4, 4.4)
    # 等壓線(低壓)
    for r in (0.9, 1.9, 2.9):
        ell(ax, -0.3, 0.2, r * 1.15, r * 0.8, color=GREY, lw=1.2)
    xs = np.linspace(0.05, 3.3, 60)
    wf = np.c_[xs, -0.28 * xs - 0.05 * xs ** 2 + 0.0]
    front(ax, wf, 'warm', size=0.18, spacing=0.7)
    t = np.linspace(0, 1, 60)
    cf = np.c_[-0.05 - 1.7 * t + 0.3 * np.sin(np.pi * t), -0.05 - 2.6 * t]
    front(ax, cf, 'cold', size=0.18, spacing=0.7)
    lab(ax, -0.3, 0.45, '低', color=RED, fs=16, box=False)
    for n, (x, y) in {'甲': (1.0, -1.6), '乙': (-2.4, -1.2), '丙': (2.4, 0.5)}.items():
        ax.plot([x], [y], 'o', color=INK, ms=6)
        lab(ax, x + 0.3, y + 0.25, n, fs=14, box=False)
    compass(ax, 3.4, 1.6)
    save(f, 41133)


@fig(41134)
def f41134():
    f, ax = new_ax(6.0, 4.2)
    cx = 5.0
    for r, v in zip([6.5, 5.0, 3.5, 2.0], [1000, 1004, 1008, 1012]):
        a = min(np.degrees(np.arcsin(min(2.2 / r, 1))), 70)
        th = np.radians(np.linspace(180 - a, 180 + a, 120))
        ax.plot(cx + r * np.cos(th), r * np.sin(th), color=INK, lw=1.4)
        lab(ax, cx + r * np.cos(th[0]), r * np.sin(th[0]) + 0.25, str(v), fs=11, box=False)
    pts = {'甲': (cx + 2.75 * np.cos(np.radians(150)), 2.75 * np.sin(np.radians(150))),
           '乙': (cx + 5.75 * np.cos(np.radians(170)), 5.75 * np.sin(np.radians(170))),
           '丙': (cx + 4.25 * np.cos(np.radians(197)), 4.25 * np.sin(np.radians(197)))}
    for n, (x, y) in pts.items():
        ax.plot([x], [y], 'o', color=BLUE, ms=5)
        lab(ax, x + 0.28, y + 0.2, n, fs=13, box=False)
    save(f, 41134)


# ═══════════════ 板塊 ═══════════════
@fig(41136)
def f41136():
    f, ax = new_ax(6.4, 3.8)
    xs = np.linspace(-3.2, 3.2, 200)
    top = 0.55 * np.exp(-(xs / 0.9) ** 2) - 0.05 * np.abs(xs)
    ax.fill_between(xs, top, 1.3, color=SKYB, lw=0)
    lab(ax, -2.4, 0.95, '海水', fs=12, box=False, color=BLUE)
    for side in (-1, 1):
        m = (xs * side) > 0.12
        ax.fill_between(xs[m], top[m] - 0.7, top[m], facecolor='white', edgecolor=INK, hatch='...', lw=0)
        ax.plot(xs[m], top[m], color=INK, lw=1.5)
        ax.plot(xs[m], top[m] - 0.7, color=INK, lw=1.5)
        arrow(ax, (side * 1.5, 0.4), (side * 2.7, 0.4), lw=2.0)
    ax.plot([0.12, 0.12], [-0.2, 0.5], color=INK, lw=1.2); ax.plot([-0.12, -0.12], [-0.2, 0.5], color=INK, lw=1.2)
    for dx in (-0.45, 0, 0.45):
        arrow(ax, (dx * 1.4, -1.9), (dx * 0.25, -0.75), color=RED, lw=1.8)
    lab(ax, 0.9, -1.75, '岩漿', color=RED, fs=12, box=False)
    lab(ax, -2.0, -1.75, '地函', fs=12, box=False)
    ax.set_xlim(-3.3, 3.3); ax.set_ylim(-2.0, 1.4)
    save(f, 41136)


@fig(41137)
def f41137():
    f, ax = new_ax(6.6, 4.2)
    xs = np.linspace(-3.5, 4.0, 300)
    surf = np.where(np.abs(xs + 1) < 0.5, -0.35 * (1 - np.abs(xs + 1) / 0.5), 0) + np.where(xs > 0.5, 0.25, 0) * np.clip((xs - 0.5) / 0.5, 0, 1)
    ax.plot(xs, surf, color=INK, lw=1.8)
    lab(ax, -1.0, -0.62, '海溝', fs=12, box=False)
    lab(ax, -2.6, 0.45, '甲側', fs=14, box=False)
    lab(ax, 2.8, 0.75, '乙側', fs=14, box=False)
    rng = np.random.default_rng(7)
    for _ in range(26):
        x = rng.uniform(-0.8, 3.6)
        d = min(-0.25 - 0.72 * (x + 0.8) + rng.normal(0, 0.18), -0.4)
        ax.plot([x], [d], 'o', color=INK, ms=4)
    # 深度尺
    ax.plot([-3.4, -3.4], [0, -3.0], color=INK, lw=1.2)
    for k in range(4):
        ax.plot([-3.4, -3.3], [-k, -k], color=INK, lw=1.2)
        lab(ax, -3.55, -k, str(100 * k), fs=11, box=False, ha='right')
    lab(ax, -2.6, -3.3, '深度(公里)', fs=11, box=False)
    save(f, 41137)


@fig(41138)
def f41138():
    f, ax = new_ax(6.6, 3.4)
    xs = np.linspace(-4, 4, 300)
    sea = 0.6 * np.exp(-(xs / 0.8) ** 2)
    ax.fill_between(xs, sea, 1.4, color=SKYB, lw=0)
    ax.fill_between(xs, -0.6, sea, facecolor='white', edgecolor=INK, hatch='...', lw=0)
    ax.plot(xs, sea, color=INK, lw=1.6)
    lab(ax, 1.0, 1.0, '中洋脊', fs=12, box=False)
    ax.plot([-4, 4], [-0.9, -0.9], color=INK, lw=1.3)
    for d in (-80, -40, 0, 40, 80):
        x = d / 20
        ax.plot([x, x], [-0.9, -0.8], color=INK, lw=1.3)
        lab(ax, x, -1.2, f'{abs(d)}', fs=11, box=False)
        age = {0: '0', 40: '200萬年', 80: '400萬年'}[abs(d)]
        ax.plot([x], [sea[np.argmin(abs(xs - x))]], 'o', color=RED, ms=5)
        lab(ax, x, sea[np.argmin(abs(xs - x))] + 0.32, age, fs=11, color=RED)
    lab(ax, 0, -1.6, '與中洋脊的距離(公里)', fs=11, box=False)
    lab(ax, -3.3, 1.15, '岩石年齡', fs=11, box=False, color=RED)
    ax.plot([0, 0.1], [1.9, 1.9], color='white', lw=0.5)
    ax.plot([0, 0.1], [-2.1, -2.1], color='white', lw=0.5)
    save(f, 41138)


# ═══════════════ 日地月 ═══════════════
def body(ax, cx, cy, r, sun_ang, lit='white', dark='#8a8a8a'):
    ax.add_patch(MC((cx, cy), r, facecolor=lit, edgecolor=INK, lw=1.3, zorder=3))
    ax.add_patch(Wedge((cx, cy), r, sun_ang + 90, sun_ang + 270, facecolor=dark, edgecolor=INK, lw=1.3, zorder=4))


def sunlight(ax, side, ys, x0, L=1.0):
    for y in ys:
        if side == 'right':
            arrow(ax, (x0 + L, y), (x0, y), color='#d89a00', lw=1.6)
        else:
            arrow(ax, (x0 - L, y), (x0, y), color='#d89a00', lw=1.6)
    xm = x0 + L / 2 if side == 'right' else x0 - L / 2
    lab(ax, xm, max(ys) + 0.4, '太陽光', fs=12, box=False, color='#b07800')


def moon_orbit(qid, labels, sun_side='right', R=2.4):
    f, ax = new_ax(6.4, 4.6)
    sa = 0 if sun_side == 'right' else 180
    circle(ax, 0, 0, R, color=GREY, lw=1.2)
    ax.lines[-1].set_linestyle('--')
    for a in (22.5, 202.5):
        p0 = (R * np.cos(np.radians(a - 8)), R * np.sin(np.radians(a - 8)))
        p1 = (R * np.cos(np.radians(a + 8)), R * np.sin(np.radians(a + 8)))
        arrow(ax, p0, p1, color=BLUE, lw=1.8, ms=16)
    body(ax, 0, 0, 0.5, sa)
    lab(ax, 0, -0.85, '地球', fs=12, box=False)
    for a, n in labels.items():
        cx, cy = R * np.cos(np.radians(a)), R * np.sin(np.radians(a))
        body(ax, cx, cy, 0.22, sa)
        lab(ax, (R + 0.55) * np.cos(np.radians(a)), (R + 0.55) * np.sin(np.radians(a)), n, fs=14, box=False)
    if sun_side == 'right':
        sunlight(ax, 'right', [-1.6, -0.5, 0.6, 1.7], 3.6)
    else:
        sunlight(ax, 'left', [-1.6, -0.5, 0.6, 1.7], -3.6)
    save(f, qid)


@fig(41139)
def f41139():
    moon_orbit(41139, {0: '甲', 90: '乙', 180: '丙', 270: '丁'})


@fig(41140)
def f41140():
    moon_orbit(41140, {315: '甲', 225: '乙', 135: '丙', 45: '丁'})


@fig(41141)
def f41141():
    moon_orbit(41141, {270: '甲', 0: '乙', 90: '丙', 180: '丁'})


@fig(41143)
def f41143():
    moon_orbit(41143, {90: '月球'}, sun_side='left')


@fig(41142)
def f41142():
    f, ax = new_ax(6.4, 3.6)
    ax.add_patch(Ellipse((0, 0), 2 * 1.45, 2 * 1.08, facecolor=SKYB, edgecolor=BLUE, lw=1.4))
    ax.add_patch(MC((0, 0), 0.95, facecolor='white', edgecolor=INK, lw=1.4))
    lab(ax, 0, -0.3, '地球', fs=12, box=False)
    pts = {'A': (1.45, 0, 0.3, 0), 'B': (0, 1.08, 0, 0.3), 'C': (-1.45, 0, -0.3, 0), 'D': (0, -1.08, 0, -0.3)}
    for n, (x, y, dx, dy) in pts.items():
        ax.plot([x], [y], 'o', color=INK, ms=5)
        lab(ax, x + dx, y + dy, n, fs=14, box=False)
    ax.add_patch(MC((4.2, 0), 0.35, facecolor=LIGHT, edgecolor=INK, lw=1.3))
    lab(ax, 4.2, -0.65, '月球', fs=12, box=False)
    arc(ax, 0, 0, 0.6, 40, 140, color=BLUE, lw=1.6)
    arrow(ax, (0.6 * np.cos(np.radians(130)), 0.6 * np.sin(np.radians(130))),
          (0.6 * np.cos(np.radians(150)), 0.6 * np.sin(np.radians(150))), color=BLUE, lw=1.6)
    lab(ax, 0, 0.42, '自轉', fs=11, box=False, color=BLUE)
    save(f, 41142)


def earth_side(qid, s, lats, R=1.6):
    """s=+1 北極偏向太陽(右方);s=-1 北極背向太陽。lats: [(緯度, 標籤, 是否畫點)]"""
    f, ax = new_ax(6.4, 4.4)
    ax.add_patch(MC((0, 0), R, facecolor='white', edgecolor=INK, lw=1.5, zorder=1))
    ax.add_patch(Wedge((0, 0), R, 90, 270, facecolor='#bdbdbd', edgecolor=INK, lw=1.5, zorder=2))
    P = np.radians(90 - s * 23.5)
    ax.plot([-(R + 0.45) * np.cos(P), (R + 0.45) * np.cos(P)], [-(R + 0.45) * np.sin(P), (R + 0.45) * np.sin(P)],
            color=INK, lw=1.4, zorder=5)
    lab(ax, (R + 0.7) * np.cos(P), (R + 0.7) * np.sin(P), '北極', fs=12, box=False)
    for phi, n, style in lats:
        ar = np.radians(phi - s * 23.5)
        al = np.radians(180 - phi - s * 23.5)
        p1 = np.array([R * np.cos(ar), R * np.sin(ar)])
        p2 = np.array([R * np.cos(al), R * np.sin(al)])
        ax.plot(*np.c_[p1, p2], color=BLUE if style else INK, lw=1.3, ls='--' if style else '-', zorder=5)
        d = (p2 - p1) / np.linalg.norm(p2 - p1)
        q = p2 + d * 0.15
        lab(ax, q[0] - 0.1, q[1], n, fs=12 if not style else 14, box=False, ha='right', zorder=6)
    sunlight(ax, 'right', [-1.2, -0.4, 0.4, 1.2], 2.4, L=1.3)
    return f, ax


@fig(41144)
def f41144():
    f, ax = earth_side(0, 1, [(23.5, '北回歸線', False), (0, '赤道', False), (-23.5, '南回歸線', False)])
    R = 1.6
    arrow(ax, (3.0, 0.0), (R + 0.02, 0.0), color=RED, lw=2.2)
    save(f, 41144)


@fig(41145)
def f41145():
    f, ax = earth_side(0, 1, [(70, '甲', True), (0, '乙', True), (-30, '丙', True), (-70, '丁', True)])
    save(f, 41145)


@fig(41152)
def f41152():
    f, ax = earth_side(0, -1, [(25, '甲', True), (0, '乙', True), (-25, '丙', True)])
    save(f, 41152)


@fig(41146)
def f41146():
    f, ax = new_ax(6.6, 3.8)
    a, b = 3.0, 1.35
    ell(ax, 0, 0, a, b, color=GREY, lw=1.3)
    ax.add_patch(MC((0, 0), 0.38, facecolor='#ffd257', edgecolor='#c08a00', lw=1.3))
    lab(ax, 0, 0, '太陽', fs=11, box=False)
    tilt = np.radians(23.5)
    u = np.array([np.sin(tilt), np.cos(tilt)])
    pos = {'甲': (a, 0, 0.62, -0.1), '乙': (0, b, 0.6, 0.18), '丙': (-a, 0, -0.62, -0.1), '丁': (0, -b, 0.6, -0.2)}
    for n, (x, y, dx, dy) in pos.items():
        ax.add_patch(MC((x, y), 0.25, facecolor='white', edgecolor=BLUE, lw=1.4, zorder=3))
        ax.plot([x - 0.42 * u[0], x + 0.42 * u[0]], [y - 0.42 * u[1], y + 0.42 * u[1]], color=INK, lw=1.4, zorder=4)
        lab(ax, x + 0.5 * u[0], y + 0.52 * u[1] + 0.06, 'N', fs=11, box=False)
        lab(ax, x + dx, y + dy, n, fs=14, box=False)
    for ang in (45, 225):
        t0, t1 = np.radians(ang - 7), np.radians(ang + 7)
        arrow(ax, (a * np.cos(t0), b * np.sin(t0)), (a * np.cos(t1), b * np.sin(t1)), color=BLUE, lw=1.8, ms=16)
    save(f, 41146)


def shadow_fig(qid, shadows, compass_north=True, rose=None, pole_lab=(0.0, -0.4)):
    f, ax = new_ax(6.0, 4.0)
    for (x, y, n) in shadows:
        ax.plot([0, x], [0, y], color=INK, lw=3.0, solid_capstyle='round')
        r = np.hypot(x, y)
        lab(ax, x + 0.3 * x / r, y + 0.3 * y / r, n, fs=13, box=False)
    ax.plot([0], [0], 'o', color=RED, ms=9, zorder=5, clip_on=False)
    lab(ax, pole_lab[0], pole_lab[1], '竹竿', fs=12, box=False)
    if compass_north:
        compass(ax, 2.6, -0.6)
    if rose:
        cx, cy = rose
        for (dx, dy, n) in [(0, 1, '甲'), (1, 0, '乙'), (0, -1, '丙'), (-1, 0, '丁')]:
            arrow(ax, (cx, cy), (cx + 0.75 * dx, cy + 0.75 * dy), color=BLUE, lw=1.6)
            lab(ax, cx + 1.0 * dx, cy + 1.0 * dy, n, fs=13, box=False, color=BLUE)
    return f, ax


@fig(41147)
def f41147():
    f, ax = shadow_fig(41147, [(1.8, 1.3, '甲'), (-1.8, 1.3, '乙'), (0, 1.0, '丙')])
    ax.plot([-2.6, 3.0], [-1.25, -1.25], color='white', lw=0.5)
    save(f, 41147)


@fig(41148)
def f41148():
    f, ax = shadow_fig(41148, [(1.3, 1.8, '9時'), (1.0, 0, '12時'), (1.3, -1.8, '15時')],
                       compass_north=False, rose=(-2.6, 0), pole_lab=(-0.55, 0))
    save(f, 41148)


@fig(41149)
def f41149():
    f, ax = new_ax(6.6, 4.0)
    R, k = 3.0, 0.32
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(R * np.cos(t), k * R * np.sin(t), color=INK, lw=1.4)
    phi = np.radians(25)
    for dec, n in [(23.44, '丙'), (0, '乙'), (-23.44, '甲')]:
        d = np.radians(dec)
        H = np.radians(np.linspace(-180, 180, 721))
        e = -np.cos(d) * np.sin(H)
        nn = np.sin(d) * np.cos(phi) - np.cos(d) * np.cos(H) * np.sin(phi)
        u = np.sin(d) * np.sin(phi) + np.cos(d) * np.cos(H) * np.cos(phi)
        m = u >= 0
        X, Y = R * e[m], R * (k * nn[m] + u[m])
        o = np.argsort(H[m])
        col = RED if n == '丙' else BLUE
        ax.plot(X[o], Y[o], color=col, lw=1.8)
        Xo, Yo = X[o], Y[o]
        # 日出、日落點(地平面上)與運行方向箭頭
        for j in (0, -1):
            ax.plot([Xo[j]], [Yo[j]], 'o', color=col, ms=6, zorder=5, clip_on=False)
        jm = int(len(Xo) * 0.3)
        arrow(ax, (Xo[jm - 6], Yo[jm - 6]), (Xo[jm], Yo[jm]), color=col, lw=1.6, ms=16)
        i = int(np.argmin(np.abs(Xo + 0.3 * R) + 10 * (Xo > 0)))   # 標在軌跡上(西半邊),白底
        lab(ax, Xo[i], Yo[i], n, fs=14, box=True, color=col)
    for s, (x, y) in {'東': (R + 0.35, 0), '西': (-R - 0.35, 0), '南': (0, -k * R - 0.35), '北': (0, k * R - 0.3)}.items():
        lab(ax, x, y, s, fs=13, box=False)
    ax.plot([0], [0], 'o', color=INK, ms=5)
    lab(ax, 0.25, -0.22, 'O', fs=12, box=False)
    save(f, 41149)


@fig(41150)
def f41150():
    f, ax = new_ax(6.4, 3.8)
    R = 2.6
    ax.plot([-R - 0.3, R + 0.3], [0, 0], color=INK, lw=1.6)
    arc(ax, 0, 0, R, 0, 180, color=GREY, lw=1.2)
    ax.lines[-1].set_linestyle('--')
    lab(ax, -R - 0.55, 0, '南', fs=13, box=False)
    lab(ax, R + 0.55, 0, '北', fs=13, box=False)
    ax.plot([0, 0], [0, R], color=GREY, lw=1.0, ls=':')
    lab(ax, 0, R + 0.25, '天頂', fs=12, box=False)
    a = np.radians(41.5)
    sx, sy = -R * np.cos(a), R * np.sin(a)
    ax.plot([0, sx], [0, sy], color=RED, lw=1.6)
    ax.add_patch(MC((sx, sy), 0.22, facecolor='#ffd257', edgecolor='#c08a00', lw=1.3, zorder=4))
    lab(ax, sx - 0.55, sy + 0.2, '太陽', fs=12, box=False)
    arc(ax, 0, 0, 0.8, 180 - 41.5, 180, color=RED, lw=1.4)
    lab(ax, -1.25, 0.35, '41.5°', fs=12, box=False, color=RED)
    ax.plot([0], [0], 'o', color=INK, ms=5)
    lab(ax, 0.3, -0.3, '觀測者', fs=11, box=False)
    save(f, 41150)


@fig(41151)
def f41151():
    f, ax = new_ax(6.4, 4.0)
    R = 1.5
    ax.add_patch(MC((0, 0), R, facecolor='white', edgecolor=INK, lw=1.5))
    ax.add_patch(Wedge((0, 0), R, 90, 270, facecolor='#bdbdbd', edgecolor=INK, lw=1.5))
    ax.plot([0], [0], 'o', color=INK, ms=4, zorder=5)
    lab(ax, 0.35, 0.18, '北極', fs=11, box=False)
    arc(ax, 0, 0, 0.75, 200, 330, color=BLUE, lw=1.6)
    arrow(ax, (0.75 * np.cos(np.radians(320)), 0.75 * np.sin(np.radians(320))),
          (0.75 * np.cos(np.radians(340)), 0.75 * np.sin(np.radians(340))), color=BLUE, lw=1.6)
    for n, (x, y, dx, dy) in {'甲': (0, R, 0, 0.3), '乙': (-R, 0, -0.3, 0), '丙': (0, -R, 0, -0.3), '丁': (R, 0, 0.3, 0)}.items():
        ax.plot([x], [y], 'o', color=RED, ms=6, zorder=6)
        lab(ax, x + dx, y + dy, n, fs=14, box=False)
    sunlight(ax, 'right', [-1.0, -0.3, 0.4, 1.1], 2.3, L=1.2)
    save(f, 41151)


@fig(41153)
def f41153():
    f, ax = new_ax(6.0, 3.6)
    ax.plot([-2.8, 2.8], [-1.5, -1.5], color=INK, lw=1.6)
    for s, x in (('東', -2.4), ('南', 0), ('西', 2.4)):
        lab(ax, x, -1.85, s, fs=13, box=False)
    r = 0.8
    ax.add_patch(MC((0, 0.4), r, facecolor='#f5e08a', edgecolor=INK, lw=1.4))
    ax.add_patch(Wedge((0, 0.4), r, -90, 90, facecolor='#6b6b6b', edgecolor=INK, lw=1.4))
    lab(ax, 0, 1.55, '(面向南方觀察)', fs=12, box=False)
    save(f, 41153)


@fig(41154)
def f41154():
    f, ax = new_ax(6.6, 3.2)
    S, rs = (-4.0, 0), 0.9
    M, rm = (0, 0), 0.3
    E, re = (2.0, 0), 0.8
    for (x1, y1), (x2, y2) in [((-4, 0.9), (0, 0.3)), ((-4, -0.9), (0, -0.3))]:
        sl = (y2 - y1) / (x2 - x1)
        ax.plot([x1, 1.25], [y1, y1 + sl * (1.25 - x1)], color=INK, lw=1.0)
    for (x1, y1), (x2, y2) in [((-4, 0.9), (0, -0.3)), ((-4, -0.9), (0, 0.3))]:
        sl = (y2 - y1) / (x2 - x1)
        ax.plot([x1, 1.3], [y1, y1 + sl * (1.3 - x1)], color=GREY, lw=1.0, ls='--')
    ax.fill([0, 2.0, 0], [0.3, 0, -0.3], color='#555555', alpha=0.45, lw=0)
    ax.add_patch(MC(S, rs, facecolor='#ffd257', edgecolor='#c08a00', lw=1.4, zorder=3))
    ax.add_patch(MC(E, re, facecolor='white', edgecolor=INK, lw=1.4, zorder=2))
    ax.add_patch(MC(M, rm, facecolor=LIGHT, edgecolor=INK, lw=1.3, zorder=3))
    lab(ax, -4.0, -1.25, '太陽', fs=12, box=False)
    lab(ax, 0, -0.65, '月球', fs=12, box=False)
    lab(ax, 2.0, -1.15, '地球', fs=12, box=False)
    # 甲:本影落在地表處;乙:半影區地表;丙:地球背面
    ax.plot([1.2], [0], 'o', color=RED, ms=5, zorder=6); lab(ax, 1.45, 0.08, '甲', fs=13, color=RED, box=False)
    yb = 0.45; xb = 2.0 - np.sqrt(re ** 2 - yb ** 2)
    ax.plot([xb], [yb], 'o', color=RED, ms=5, zorder=6); lab(ax, xb + 0.05, yb + 0.35, '乙', fs=13, color=RED, box=False)
    ax.plot([2.8], [0], 'o', color=RED, ms=5, zorder=6); lab(ax, 3.1, 0.0, '丙', fs=13, color=RED, box=False)
    ax.plot([0, 0.1], [2.0, 2.0], color='white', lw=0.5)
    ax.plot([0, 0.1], [-2.0, -2.0], color='white', lw=0.5)
    save(f, 41154)
