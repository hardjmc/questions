from fig_all import *   # plt, np, PF, fig, new_ax, save, txt, dot, circle, arc, INK/RED/BLUE/GREY
from matplotlib.patches import Rectangle, Ellipse

LW = 1.7

# ───────────── 電路元件 ─────────────
def seg(ax, p, q, c=INK, lw=LW):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=c, lw=lw, solid_capstyle='round')

def wire(ax, *pts, c=INK, lw=LW):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=c, lw=lw, solid_joinstyle='miter', solid_capstyle='round')

def jdot(ax, p):
    ax.plot([p[0]], [p[1]], 'o', ms=5.5, color=INK)

def comp(ax, kind, p1, p2, label=None, side=1, plus=1, fs=13, lab_off=0.5, lc=INK):
    """在 p1→p2 線段中央畫元件。kind: R, L(燈泡), A, V, G, bat, swo(開), swc(閉), W(導線)"""
    p1 = np.array(p1, float); p2 = np.array(p2, float)
    d = p2 - p1; u = d / np.linalg.norm(d); n = np.array([-u[1], u[0]])
    m = (p1 + p2) / 2
    P = lambda s, t: m + u * s + n * t
    half = {'L': 0.27, 'A': 0.27, 'V': 0.27, 'G': 0.27, 'bat': 0.09, 'swo': 0.32, 'swc': 0.32, 'R': 0.4, 'W': 0}[kind]
    a, b = m - u * half, m + u * half
    seg(ax, p1, a); seg(ax, b, p2)
    if kind == 'R':
        k = 6
        ss = np.linspace(-half, half, 2 * k + 1)
        ts = [0] + [0.14 * (1 if i % 2 else -1) for i in range(1, 2 * k)] + [0]
        wire(ax, *[P(s, t) for s, t in zip(ss, ts)])
    elif kind == 'L':
        circle(ax, m[0], m[1], 0.27, lw=LW)
        r = 0.27 / np.sqrt(2)
        seg(ax, P(-r, -r), P(r, r), lw=1.4); seg(ax, P(-r, r), P(r, -r), lw=1.4)
    elif kind in ('A', 'V', 'G'):
        circle(ax, m[0], m[1], 0.27, lw=LW)
        ax.text(m[0], m[1], kind, fontsize=14, ha='center', va='center', color=INK, fontweight='bold')
    elif kind == 'bat':
        sl, ss_ = 0.09 * plus, -0.09 * plus
        seg(ax, P(sl, -0.32), P(sl, 0.32), lw=1.8)          # 長線(正極)
        seg(ax, P(ss_, -0.16), P(ss_, 0.16), lw=4.0)        # 短線(負極)
        q = P(sl + 0.2 * plus, 0.36)
        ax.text(q[0], q[1], '+', fontsize=13, ha='center', va='center', color=INK)
    elif kind in ('swo', 'swc'):
        A_, B_ = P(-0.32, 0), P(0.32, 0)
        for X in (A_, B_):
            ax.plot([X[0]], [X[1]], 'o', ms=5, mfc='white', mec=INK, mew=1.4, zorder=5)
        E = B_ if kind == 'swc' else P(0.24, 0.34)
        seg(ax, A_, E)
    if label:
        q = m + n * lab_off * side
        ax.text(q[0], q[1], label, fontsize=fs, ha='center', va='center', color=lc, fontproperties=PF)

def caption(ax, x, y, s, fs=14):
    txt(ax, x, y, s, fs=fs, ha='center', va='center')

def finish(ax, x0, x1, y0, y1):
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)

# ───────────── 磁學元件 ─────────────
def into_page(ax, x, y, r=0.22, c=INK):
    circle(ax, x, y, r, color=c, lw=LW)
    k = r * 0.62
    seg(ax, (x - k, y - k), (x + k, y + k), c=c, lw=1.6); seg(ax, (x - k, y + k), (x + k, y - k), c=c, lw=1.6)

def out_page(ax, x, y, r=0.22, c=INK):
    circle(ax, x, y, r, color=c, lw=LW)
    ax.plot([x], [y], 'o', ms=5, color=c)

def magnet(ax, x0, y0, w, h, left, right, vertical=False, fs=15):
    """長條磁鐵。vertical=True 時 left=下半、right=上半"""
    ax.add_patch(Rectangle((x0, y0), w, h, fill=False, ec=INK, lw=LW))
    if vertical:
        seg(ax, (x0, y0 + h / 2), (x0 + w, y0 + h / 2))
        ax.add_patch(Rectangle((x0, y0), w, h / 2, fc='#f6d5d2' if left == 'N' else '#d6e2f5', ec='none', zorder=0))
        ax.add_patch(Rectangle((x0, y0 + h / 2), w, h / 2, fc='#f6d5d2' if right == 'N' else '#d6e2f5', ec='none', zorder=0))
        txt(ax, x0 + w / 2, y0 + h / 4, left, fs=fs, ha='center', va='center')
        txt(ax, x0 + w / 2, y0 + 3 * h / 4, right, fs=fs, ha='center', va='center')
    else:
        seg(ax, (x0 + w / 2, y0), (x0 + w / 2, y0 + h))
        ax.add_patch(Rectangle((x0, y0), w / 2, h, fc='#f6d5d2' if left == 'N' else '#d6e2f5', ec='none', zorder=0))
        ax.add_patch(Rectangle((x0 + w / 2, y0), w / 2, h, fc='#f6d5d2' if right == 'N' else '#d6e2f5', ec='none', zorder=0))
        txt(ax, x0 + w / 4, y0 + h / 2, left, fs=fs, ha='center', va='center')
        txt(ax, x0 + 3 * w / 4, y0 + h / 2, right, fs=fs, ha='center', va='center')

def pole_block(ax, x0, y0, w, h, s, fs=16):
    ax.add_patch(Rectangle((x0, y0), w, h, fc='#f6d5d2' if s == 'N' else '#d6e2f5', ec=INK, lw=LW))
    txt(ax, x0 + w / 2, y0 + h / 2, s, fs=fs, ha='center', va='center')

def arrow(ax, p, q, c=RED, lw=2.0, ms=16):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=c, lw=lw, mutation_scale=ms))

def solenoid(ax, x0, x1, yc, r=0.5, turns=7, tilt=0.12, cur=None, lw=2.0):
    """螺線管。t 增加時,前側導線往下走。cur='down':電流沿 t 增加(前側向下);'up':相反。回傳兩端引線端點。"""
    T = 2 * np.pi * turns
    t = np.linspace(0, T, turns * 240)
    x = x0 + (x1 - x0) * t / T + tilt * np.sin(t)
    y = yc + r * np.cos(t)
    z = np.sin(t)
    front = z >= 0
    # 分段畫
    idx = np.where(np.diff(front.astype(int)) != 0)[0]
    bounds = [0] + list(idx + 1) + [len(t)]
    for a, b in zip(bounds[:-1], bounds[1:]):
        bb = min(b + 1, len(t))
        if front[a]:
            ax.plot(x[a:bb], y[a:bb], color=INK, lw=lw, zorder=4)
        else:
            ax.plot(x[a:bb], y[a:bb], color=GREY, lw=1.3, zorder=1)
    if cur:
        for k in range(1, turns, 2):
            ta, tb = np.pi / 2 - 0.45 + 2 * np.pi * k, np.pi / 2 + 0.45 + 2 * np.pi * k
            pa = (x0 + (x1 - x0) * ta / T + tilt * np.sin(ta), yc + r * np.cos(ta))
            pb = (x0 + (x1 - x0) * tb / T + tilt * np.sin(tb), yc + r * np.cos(tb))
            if cur == 'up':
                pa, pb = pb, pa
            ax.annotate('', xy=pb, xytext=pa, zorder=6,
                        arrowprops=dict(arrowstyle='-|>', color=RED, lw=2.4, mutation_scale=15))
    return (x0, yc + r), (x1, yc + r)


# ════════════════ 40980 哪一個是並聯 ════════════════
@fig(40980)
def f40980():
    f, ax = new_ax(7.0, 5.0)
    W, H = 3.2, 1.6
    def frame(ox, oy):
        return [(ox, oy), (ox + W, oy), (ox + W, oy + H), (ox, oy + H)]
    # 甲:串聯(兩燈在上邊)
    ox, oy = 0, 3.3
    comp(ax, 'bat', (ox, oy), (ox + W, oy))
    wire(ax, (ox, oy), (ox, oy + H)); wire(ax, (ox + W, oy), (ox + W, oy + H))
    comp(ax, 'L', (ox, oy + H), (ox + W / 2, oy + H)); comp(ax, 'L', (ox + W / 2, oy + H), (ox + W, oy + H))
    caption(ax, ox + W / 2, oy - 0.55, '甲')
    # 乙:串聯(兩燈分在左右兩邊)
    ox, oy = 4.3, 3.3
    comp(ax, 'bat', (ox, oy), (ox + W, oy))
    comp(ax, 'L', (ox, oy), (ox, oy + H)); comp(ax, 'L', (ox + W, oy), (ox + W, oy + H))
    wire(ax, (ox, oy + H), (ox + W, oy + H))
    caption(ax, ox + W / 2, oy - 0.55, '乙')
    # 丙:並聯
    ox, oy = 0, 0
    comp(ax, 'bat', (ox, oy), (ox + W, oy))
    wire(ax, (ox, oy), (ox, oy + H)); wire(ax, (ox + W, oy), (ox + W, oy + H))
    wire(ax, (ox, oy + H), (ox + 0.9, oy + H)); wire(ax, (ox + W - 0.9, oy + H), (ox + W, oy + H))
    wire(ax, (ox + 0.9, oy + H - 0.45), (ox + 0.9, oy + H + 0.45)); wire(ax, (ox + W - 0.9, oy + H - 0.45), (ox + W - 0.9, oy + H + 0.45))
    comp(ax, 'L', (ox + 0.9, oy + H + 0.45), (ox + W - 0.9, oy + H + 0.45))
    comp(ax, 'L', (ox + 0.9, oy + H - 0.45), (ox + W - 0.9, oy + H - 0.45))
    jdot(ax, (ox + 0.9, oy + H)); jdot(ax, (ox + W - 0.9, oy + H))
    caption(ax, ox + W / 2, oy - 0.55, '丙')
    # 丁:串聯含開關
    ox, oy = 4.3, 0
    comp(ax, 'bat', (ox, oy), (ox + W / 2, oy)); comp(ax, 'swc', (ox + W / 2, oy), (ox + W, oy))
    comp(ax, 'L', (ox, oy), (ox, oy + H)); wire(ax, (ox + W, oy), (ox + W, oy + H))
    wire(ax, (ox, oy + H), (ox + W / 2, oy + H)); comp(ax, 'L', (ox + W / 2, oy + H), (ox + W, oy + H))
    caption(ax, ox + W / 2, oy - 0.55, '丁')
    finish(ax, -0.5, 8.0, -0.9, 5.3)
    save(f, 40980)


# ════════════════ 40981 安培計、伏特計接法 ════════════════
@fig(40981)
def f40981():
    f, ax = new_ax(7.0, 5.2)
    W, H = 3.6, 1.3
    def panel(ox, oy, kind, cap):
        comp(ax, 'bat', (ox, oy), (ox + W, oy))
        wire(ax, (ox, oy), (ox, oy + H)); wire(ax, (ox + W, oy), (ox + W, oy + H))
        x1, x2 = ox + 1.6, ox + 2.9
        if kind == 'ok':          # A 串聯、V 並聯在燈泡兩端
            comp(ax, 'A', (ox, oy + H), (x1, oy + H)); comp(ax, 'L', (x1, oy + H), (x2, oy + H), 'L', lab_off=-0.5)
            wire(ax, (x2, oy + H), (ox + W, oy + H))
            wire(ax, (x1, oy + H), (x1, oy + H + 0.6)); wire(ax, (x2, oy + H), (x2, oy + H + 0.6))
            comp(ax, 'V', (x1, oy + H + 0.6), (x2, oy + H + 0.6))
        elif kind == 'swap':      # V 串聯、A 並聯在燈泡兩端
            comp(ax, 'V', (ox, oy + H), (x1, oy + H)); comp(ax, 'L', (x1, oy + H), (x2, oy + H), 'L', lab_off=-0.5)
            wire(ax, (x2, oy + H), (ox + W, oy + H))
            wire(ax, (x1, oy + H), (x1, oy + H + 0.6)); wire(ax, (x2, oy + H), (x2, oy + H + 0.6))
            comp(ax, 'A', (x1, oy + H + 0.6), (x2, oy + H + 0.6))
        elif kind == 'both_series':
            comp(ax, 'A', (ox, oy + H), (x1 - 0.2, oy + H)); comp(ax, 'L', (x1 - 0.2, oy + H), (x2 - 0.2, oy + H), 'L', lab_off=-0.5)
            comp(ax, 'V', (x2 - 0.2, oy + H), (ox + W, oy + H))
        elif kind == 'both_par':
            comp(ax, 'L', (ox, oy + H), (ox + W, oy + H), 'L', lab_off=-0.5)
            x1, x2 = ox + 1.2, ox + 2.4
            for yy, k in ((oy + H + 0.55, 'A'), (oy + H + 1.1, 'V')):
                comp(ax, k, (x1, yy), (x2, yy))
            wire(ax, (x1, oy + H), (x1, oy + H + 1.1)); wire(ax, (x2, oy + H), (x2, oy + H + 1.1))
            jdot(ax, (x1, oy + H + 0.55)); jdot(ax, (x2, oy + H + 0.55))
        if kind != 'both_series':
            jdot(ax, (x1, oy + H)); jdot(ax, (x2, oy + H))
        caption(ax, ox + W / 2, oy - 0.55, cap)
    panel(0, 3.6, 'swap', '甲')
    panel(4.7, 3.6, 'both_series', '乙')
    panel(0, 0, 'both_par', '丙')
    panel(4.7, 0, 'ok', '丁')
    finish(ax, -0.5, 8.8, -0.9, 6.2)
    save(f, 40981)


# ════════════════ 40982 串聯伏特計 ════════════════
@fig(40982)
def f40982():
    f, ax = new_ax(6.0, 3.8)
    W, H = 5.0, 2.2
    comp(ax, 'bat', (0, 0), (W, 0), '6 V', side=-1)
    wire(ax, (0, 0), (0, H)); wire(ax, (W, 0), (W, H))
    comp(ax, 'R', (0, H), (2.4, H), '2 Ω', side=-1)
    comp(ax, 'R', (2.4, H), (W, H), '4 Ω', side=-1)
    wire(ax, (2.4, H), (2.4, H + 0.9)); wire(ax, (W, H), (W, H + 0.9))
    comp(ax, 'V', (2.4, H + 0.9), (W, H + 0.9))
    jdot(ax, (2.4, H)); jdot(ax, (W, H))
    finish(ax, -0.6, 5.6, -0.9, 3.5)
    save(f, 40982)


# ════════════════ 40983 並聯總電流 ════════════════
@fig(40983)
def f40983():
    f, ax = new_ax(6.0, 4.0)
    W = 5.0
    comp(ax, 'bat', (0, 0), (2.5, 0), '12 V', side=-1)
    comp(ax, 'A', (2.5, 0), (W, 0))
    wire(ax, (0, 0), (0, 2.6)); wire(ax, (W, 0), (W, 2.6))
    comp(ax, 'R', (0, 1.4), (W, 1.4), '4 Ω', side=1)
    comp(ax, 'R', (0, 2.6), (W, 2.6), '6 Ω', side=1)
    for p in ((0, 1.4), (W, 1.4)):
        jdot(ax, p)
    finish(ax, -0.6, 5.6, -0.9, 3.3)
    save(f, 40983)


# ════════════════ 圖表共用 ════════════════
def graph(w=5.6, h=4.0, xlabel='', ylabel=''):
    f, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlabel(xlabel, fontproperties=PF, fontsize=13)
    ax.set_ylabel(ylabel, fontproperties=PF, fontsize=13)
    ax.tick_params(labelsize=12, width=1.2)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(1.3)
    ax.grid(True, color='#dddddd', lw=0.8)
    return f, ax


# ════════════════ 40984 I-V 圖求電阻 ════════════════
@fig(40984)
def f40984():
    f, ax = graph(xlabel='電壓(V)', ylabel='電流(A)')
    v = np.array([0, 8]); ax.plot(v, v / 4, color=BLUE, lw=2.2)
    ax.plot([2, 4, 6, 8], [0.5, 1.0, 1.5, 2.0], 'o', color=BLUE, ms=6)
    ax.set_xlim(0, 9); ax.set_ylim(0, 2.5)
    ax.set_xticks(range(0, 10, 1)); ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5])
    save(f, 40984)


# ════════════════ 40985 兩電阻 I-V 圖,串聯 ════════════════
@fig(40985)
def f40985():
    f, ax = graph(xlabel='電壓(V)', ylabel='電流(A)')
    v = np.array([0, 6])
    ax.plot(v, v / 2, color=RED, lw=2.2); ax.plot(v, v / 6, color=BLUE, lw=2.2)
    txt(ax, 5.0, 2.75, '甲', color=RED, fs=14); txt(ax, 6.1, 1.0, '乙', color=BLUE, fs=14)
    ax.set_xlim(0, 7); ax.set_ylim(0, 3.5)
    ax.set_xticks(range(0, 8)); ax.set_yticks([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5])
    save(f, 40985)


# ════════════════ 40986 / 40987 開關與燈泡 ════════════════
def lamp_net(ax):
    W = 5.6
    # 主線:電池 + S1 + L3 在下方
    comp(ax, 'bat', (0, 0), (1.8, 0))
    comp(ax, 'swc', (1.8, 0), (3.6, 0), 'S₁', side=-1, lab_off=0.45)
    comp(ax, 'L', (3.6, 0), (W, 0), 'L₃', side=-1)
    wire(ax, (0, 0), (0, 2.6)); wire(ax, (W, 0), (W, 2.6))
    wire(ax, (0, 1.4), (1.2, 1.4)); wire(ax, (W, 1.4), (W - 1.2, 1.4))
    comp(ax, 'L', (1.2, 1.4), (W - 1.2, 1.4), 'L₁', side=-1)
    comp(ax, 'L', (0, 2.6), (2.8, 2.6), 'L₂', side=1)
    comp(ax, 'swo', (2.8, 2.6), (W, 2.6), 'S₂', side=1, lab_off=0.55)
    jdot(ax, (0, 1.4)); jdot(ax, (W, 1.4))
    finish(ax, -0.6, 6.2, -0.9, 3.4)

@fig(40986)
def f40986():
    f, ax = new_ax(6.0, 3.8); lamp_net(ax); save(f, 40986)

@fig(40987)
def f40987():
    f, ax = new_ax(6.0, 3.8); lamp_net(ax); save(f, 40987)


# ════════════════ 40988 電功率-時間圖 ════════════════
@fig(40988)
def f40988():
    f, ax = graph(xlabel='使用時間(小時)', ylabel='電功率(W)')
    ax.plot([0, 0.5, 0.5, 2.5, 2.5], [1000, 1000, 200, 200, 0], color=BLUE, lw=2.2)
    ax.set_xlim(0, 3); ax.set_ylim(0, 1200)
    ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3]); ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
    save(f, 40988)


# ════════════════ 40989 燈泡電功率(電表讀數) ════════════════
@fig(40989)
def f40989():
    f, ax = new_ax(6.0, 3.8)
    W, H = 5.0, 2.0
    comp(ax, 'bat', (0, 0), (W, 0))
    wire(ax, (0, 0), (0, H)); wire(ax, (W, 0), (W, H))
    comp(ax, 'A', (0, H), (2.2, H), '0.5 A', side=-1, lab_off=0.55)
    comp(ax, 'L', (2.2, H), (W, H), 'L', side=-1)
    wire(ax, (2.2, H), (2.2, H + 0.9)); wire(ax, (W, H), (W, H + 0.9))
    comp(ax, 'V', (2.2, H + 0.9), (W, H + 0.9), '3 V', side=1, lab_off=0.55)
    jdot(ax, (2.2, H)); jdot(ax, (W, H))
    finish(ax, -0.6, 5.6, -0.8, 3.7)
    save(f, 40989)


# ════════════════ 40990 電表接反 ════════════════
@fig(40990)
def f40990():
    f, ax = new_ax(6.0, 3.8)
    W, H = 5.0, 2.0
    comp(ax, 'bat', (0, 0), (W, 0), '3 V', side=-1)
    wire(ax, (0, 0), (0, H)); wire(ax, (W, 0), (W, H))
    comp(ax, 'V', (0, H), (2.2, H))
    comp(ax, 'L', (2.2, H), (W, H), 'L', side=-1)
    wire(ax, (2.2, H), (2.2, H + 0.9)); wire(ax, (W, H), (W, H + 0.9))
    comp(ax, 'A', (2.2, H + 0.9), (W, H + 0.9))
    jdot(ax, (2.2, H)); jdot(ax, (W, H))
    finish(ax, -0.6, 5.6, -0.9, 3.5)
    save(f, 40990)


# ════════════════ 40991 混聯電路 ════════════════
@fig(40991)
def f40991():
    f, ax = new_ax(6.4, 3.8)
    comp(ax, 'bat', (0, 0), (5.6, 0), '12 V', side=-1)
    wire(ax, (0, 0), (0, 1.8))
    comp(ax, 'R', (0, 1.8), (2.2, 1.8), 'R₁=4 Ω', side=-1)
    wire(ax, (2.2, 1.2), (2.2, 2.4)); wire(ax, (4.6, 1.2), (4.6, 2.4))
    comp(ax, 'R', (2.2, 2.4), (4.6, 2.4), '6 Ω', side=1)
    comp(ax, 'R', (2.2, 1.2), (4.6, 1.2), '12 Ω', side=-1)
    wire(ax, (4.6, 1.8), (5.6, 1.8), (5.6, 0))
    jdot(ax, (2.2, 1.8)); jdot(ax, (4.6, 1.8))
    finish(ax, -0.6, 6.2, -0.9, 3.1)
    save(f, 40991)


# ════════════════ 40992 直導線磁場(俯視) ════════════════
@fig(40992)
def f40992():
    f, ax = new_ax(5.6, 3.8)
    out_page(ax, 0, 0, r=0.2, c=RED)
    for r in (0.6, 1.0, 1.4):
        circle(ax, 0, 0, r, color=BLUE, lw=1.4)
    txt(ax, 1.9, 0.6, '導線垂直紙面\n電流流出紙面', fs=13, va='center')
    txt(ax, 1.9, -0.6, '藍線：磁力線\n（俯視圖）', fs=13, va='center', color=BLUE)
    finish(ax, -1.7, 4.4, -1.7, 1.7)
    save(f, 40992)


# ════════════════ 40993 直導線周圍指南針 ════════════════
@fig(40993)
def f40993():
    f, ax = new_ax(5.6, 3.8)
    into_page(ax, 0, 0, r=0.24, c=RED)
    for (x, y, s) in ((0, 1.1, '甲'), (1.1, 0, '乙'), (0, -1.1, '丙'), (-1.1, 0, '丁')):
        ax.plot([x], [y], 'o', ms=7, color=BLUE)
        dx, dy = (0.32, 0) if x >= 0 and y == 0 else ((-0.32, 0) if y == 0 else (0.32, 0))
        txt(ax, x + (0.2 if x >= 0 else -0.5), y + (0.0 if y == 0 else 0), s, fs=14, va='center')
    txt(ax, 1.9, 0.0, '導線垂直紙面\n電流流入紙面', fs=13, va='center')
    finish(ax, -1.7, 4.3, -1.5, 1.5)
    save(f, 40993)


# ════════════════ 40994 螺線管極性 ════════════════
@fig(40994)
def f40994():
    f, ax = new_ax(6.4, 3.4)
    a, b = solenoid(ax, 0, 3.6, 0, cur='up')
    # 引線:電流由右端引線流入,左端引線流出
    wire(ax, a, (a[0], 1.3)); wire(ax, b, (b[0] + 0.12, 1.3))
    arrow(ax, (b[0] + 0.12, 1.35), (b[0] + 0.12, 0.85), c=RED, ms=14)
    arrow(ax, (a[0], 0.85), (a[0], 1.35), c=RED, ms=14)
    ax.text(b[0] + 0.3, 1.1, 'I', color=RED, fontsize=15, style='italic', fontfamily='serif', va='center')
    ax.text(a[0] - 0.35, 1.1, 'I', color=RED, fontsize=15, style='italic', fontfamily='serif', va='center')
    txt(ax, -0.9, 0, '左端', fs=13, va='center'); txt(ax, 4.0, 0, '右端', fs=13, va='center')
    txt(ax, 1.8, -0.95, '深色線：前側導線　淺灰線：後側導線', fs=12, ha='center', va='center')
    txt(ax, 1.8, -1.4, '紅色箭頭：前側導線的電流方向', fs=12, color=RED, ha='center', va='center')
    finish(ax, -1.1, 4.7, -1.65, 1.6)
    save(f, 40994)


# ════════════════ 40995 螺線管外部磁場 ════════════════
@fig(40995)
def f40995():
    f, ax = new_ax(6.4, 3.8)
    a, b = solenoid(ax, 0, 3.6, 0, cur='down')
    wire(ax, a, (a[0], 1.6)); wire(ax, b, (b[0] + 0.12, 1.6))
    arrow(ax, (a[0], 1.55), (a[0], 1.05), c=RED, ms=14)
    arrow(ax, (b[0] + 0.12, 1.05), (b[0] + 0.12, 1.55), c=RED, ms=14)
    ax.text(a[0] - 0.35, 1.3, 'I', color=RED, fontsize=15, style='italic', fontfamily='serif', va='center')
    ax.text(b[0] + 0.3, 1.3, 'I', color=RED, fontsize=15, style='italic', fontfamily='serif', va='center')
    ax.plot([1.9], [1.35], 'o', ms=7, color=BLUE)
    txt(ax, 2.05, 1.35, 'P', fs=14, va='center')
    txt(ax, -0.9, 0, '左端', fs=13, va='center'); txt(ax, 4.0, 0, '右端', fs=13, va='center')
    txt(ax, 1.8, -0.95, '深色線：前側導線　淺灰線：後側導線', fs=12, ha='center', va='center')
    txt(ax, 1.8, -1.4, '紅色箭頭：前側導線的電流方向', fs=12, color=RED, ha='center', va='center')
    finish(ax, -1.1, 4.7, -1.65, 1.9)
    save(f, 40995)


# ════════════════ 40996 電磁鐵實驗圖 ════════════════
@fig(40996)
def f40996():
    f, ax = graph(xlabel='電流(A)', ylabel='吸起迴紋針數(個)')
    i = np.array([0, 0.5, 1.0, 1.5])
    ax.plot(i, 8 * i, 'o-', color=RED, lw=2.0, ms=6)
    i2 = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5])
    ax.plot(i2, 4 * i2, 's-', color=BLUE, lw=2.0, ms=6)
    txt(ax, 1.55, 12.2, '100 匝', color=RED, fs=13); txt(ax, 2.55, 9.4, '50 匝', color=BLUE, fs=13)
    ax.set_xlim(0, 3); ax.set_ylim(0, 14)
    ax.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3]); ax.set_yticks(range(0, 15, 2))
    save(f, 40996)


# ════════════════ 電磁感應小圖 ════════════════
def induction_panel(ax, ox, oy, mpos, left_pole, move, coil_move=False, cap=''):
    """線圈 + 檢流計;磁鐵在右側。mpos:磁鐵左緣 x(相對);move: -1 向左(插入), +1 向右(拔出), 0 靜止"""
    mx = ox + mpos
    right_pole = 'S' if left_pole == 'N' else 'N'
    magnet(ax, mx, oy + 0.95, 1.5, 0.5, left_pole, right_pole, fs=13)
    a, b = solenoid(ax, ox, ox + 1.4, oy + 1.2, r=0.45, turns=5, tilt=0.1, lw=1.8)
    # 引線到檢流計
    wire(ax, a, (ox, oy + 1.9), (ox - 0.35, oy + 1.9), (ox - 0.35, oy), (ox + 0.45, oy))
    wire(ax, b, (ox + 1.4, oy + 1.9), (ox + 1.75, oy + 1.9), (ox + 1.75, oy), (ox + 0.95, oy))
    comp(ax, 'G', (ox + 0.45, oy), (ox + 0.95, oy))
    if move:
        y = oy + 0.62
        x0 = mx + 0.2; x1 = x0 + 0.9 * move
        if move < 0:
            x0, x1 = mx + 1.3, mx + 0.4
        else:
            x0, x1 = mx + 0.4, mx + 1.3
        arrow(ax, (x0, y), (x1, y), c=RED, ms=14)
    else:
        txt(ax, mx + 0.75, oy + 0.55, '靜止', fs=12, ha='center', va='center', color=RED)
    if coil_move:
        arrow(ax, (ox + 0.15, oy + 0.52), (ox + 1.25, oy + 0.52), c=BLUE, ms=14)
    caption(ax, ox + 1.4, oy - 0.55, cap)

@fig(40997)
def f40997():
    f, ax = new_ax(7.4, 4.6)
    induction_panel(ax, 0, 2.9, 1.9, 'N', -1, cap='甲')
    induction_panel(ax, 4.3, 2.9, 0.4, 'N', 0, cap='乙')
    induction_panel(ax, 0, 0, 1.9, 'S', +1, cap='丙')
    induction_panel(ax, 4.3, 0, 2.0, 'N', 0, coil_move=True, cap='丁')
    txt(ax, 4.3, -1.05, '丁：線圈向右移向靜止的磁鐵', fs=12, color=BLUE)
    finish(ax, -0.6, 8.3, -1.25, 5.3)
    save(f, 40997)

@fig(40998)
def f40998():
    f, ax = new_ax(7.4, 4.4)
    induction_panel(ax, 0, 2.9, 1.9, 'N', +1, cap='甲')
    induction_panel(ax, 4.3, 2.9, 1.9, 'S', -1, cap='乙')
    induction_panel(ax, 0, 0, 1.9, 'N', 0, cap='丙')
    induction_panel(ax, 4.3, 0, 1.9, 'S', +1, cap='丁')
    finish(ax, -0.6, 8.3, -0.9, 5.3)
    save(f, 40998)


# ════════════════ 40999 冷次定律(磁鐵落向線圈) ════════════════
@fig(40999)
def f40999():
    f, ax = new_ax(5.6, 4.0)
    ax.add_patch(Ellipse((0, 0), 2.6, 0.8, fill=False, ec=INK, lw=2.4))
    magnet(ax, -0.28, 0.9, 0.56, 1.5, 'N', 'S', vertical=True, fs=14)
    arrow(ax, (0.75, 2.2), (0.75, 1.2), c=RED, ms=16)
    txt(ax, 0.95, 1.65, '向下落', color=RED, fs=13, va='center')
    txt(ax, 1.5, -0.25, '線圈（固定）', fs=13, va='center')
    txt(ax, -2.6, 2.1, '觀察者\n由上往下看', fs=13, va='center', color=BLUE)
    arrow(ax, (-1.6, 1.6), (-1.6, 0.8), c=BLUE, ms=14)
    finish(ax, -2.8, 2.9, -0.7, 2.7)
    save(f, 40999)


# ════════════════ 41000 由磁場方向判斷電流 ════════════════
@fig(41000)
def f41000():
    f, ax = new_ax(5.6, 4.0)
    # 後半圈(上半)
    th = np.linspace(0, np.pi, 100)
    ax.plot(1.1 * np.cos(th), 0.35 * np.sin(th), color=BLUE, lw=1.8, zorder=1)
    ax.plot([0, 0], [-1.6, 1.6], color=INK, lw=3, zorder=2)
    ax.plot([0, 0], [-0.40, -0.27], color='white', lw=5, zorder=2.5)   # 前半圈蓋住導線
    th = np.linspace(np.pi, 2 * np.pi, 100)
    ax.plot(1.1 * np.cos(th), 0.35 * np.sin(th), color=BLUE, lw=1.8, zorder=3)
    arrow(ax, (-0.35, -0.335), (0.25, -0.335), c=BLUE, ms=16)
    ax.annotate('', xy=(-0.75, 0.256), xytext=(-0.3, 0.337), zorder=1,
                arrowprops=dict(arrowstyle='-|>', color=BLUE, lw=2.0, mutation_scale=16))
    txt(ax, 1.25, 0.15, '磁力線', fs=13, color=BLUE)
    txt(ax, 0.15, 1.4, '直導線', fs=13)
    txt(ax, 1.3, -1.0, '（眼睛位於前方\n略高處觀看）', fs=12, color=GREY)
    finish(ax, -2.0, 3.2, -1.7, 1.7)
    save(f, 41000)


# ════════════════ 41001 / 41002 載流導線在磁場中受力 ════════════════
@fig(41001)
def f41001():
    f, ax = new_ax(5.6, 4.0)
    pole_block(ax, -1.2, 1.0, 2.4, 0.6, 'N')
    pole_block(ax, -1.2, -1.6, 2.4, 0.6, 'S')
    into_page(ax, 0, 0, r=0.24, c=RED)
    txt(ax, 1.5, 0.0, '導線垂直紙面\n電流流入紙面', fs=13, va='center')
    finish(ax, -1.6, 3.8, -1.8, 1.8)
    save(f, 41001)

@fig(41002)
def f41002():
    f, ax = new_ax(5.0, 3.4)
    pole_block(ax, -2.2, -0.9, 0.7, 1.8, 'N')
    pole_block(ax, 1.5, -0.9, 0.7, 1.8, 'S')
    out_page(ax, 0, 0, r=0.24, c=RED)
    txt(ax, 0, -1.4, '導線垂直紙面，電流流出紙面', fs=13, ha='center', va='center')
    finish(ax, -2.4, 2.4, -1.8, 1.1)
    save(f, 41002)


# ════════════════ 41003 家用並聯電器 ════════════════
@fig(41003)
def f41003():
    f, ax = new_ax(6.4, 3.8)
    comp(ax, 'W', (0, 0), (0, 0.01)) if False else None
    ax.plot([0], [0])
    # 電源
    circle(ax, 0, 1.3, 0.35, lw=LW)
    ax.plot(np.linspace(-0.2, 0.2, 50), 1.3 + 0.12 * np.sin(np.linspace(0, 2 * np.pi, 50)), color=INK, lw=1.6)
    txt(ax, -0.95, 1.3, '110 V', fs=13, va='center', ha='center')
    wire(ax, (0, 1.65), (0, 2.6), (4.8, 2.6), (4.8, 1.85)); wire(ax, (0, 0.95), (0, 0), (4.8, 0), (4.8, 0.75))
    xs = [1.6, 3.2, 4.8]; names = ['電燈\n220 W', '電鍋\n550 W', '吹風機\n1100 W']
    for x, nm in zip(xs, names):
        wire(ax, (x, 2.6), (x, 1.85)); wire(ax, (x, 0.75), (x, 0))
        ax.add_patch(Rectangle((x - 0.45, 0.75), 0.9, 1.1, fill=False, ec=INK, lw=LW))
        txt(ax, x, 1.3, nm, fs=12, ha='center', va='center')
        if x < 4.8:
            jdot(ax, (x, 2.6)); jdot(ax, (x, 0))
    finish(ax, -1.5, 5.5, -0.3, 2.9)
    save(f, 41003)


# ════════════════ 41004 哪個燈泡最亮 ════════════════
@fig(41004)
def f41004():
    f, ax = new_ax(7.0, 5.0)
    W, H = 3.4, 1.6
    # 甲:兩電池串聯 + 一燈
    ox, oy = 0, 3.6
    comp(ax, 'bat', (ox, oy), (ox + W / 2, oy)); comp(ax, 'bat', (ox + W / 2, oy), (ox + W, oy))
    wire(ax, (ox, oy), (ox, oy + H)); wire(ax, (ox + W, oy), (ox + W, oy + H))
    comp(ax, 'L', (ox, oy + H), (ox + W, oy + H))
    caption(ax, ox + W / 2, oy - 0.55, '甲')
    # 乙:兩電池並聯 + 一燈
    ox, oy = 4.6, 3.6
    xa, xb = ox + 0.8, ox + W - 0.8
    comp(ax, 'bat', (xa, oy), (xb, oy)); comp(ax, 'bat', (xa, oy + 0.75), (xb, oy + 0.75))
    wire(ax, (xa, oy), (xa, oy + 0.75)); wire(ax, (xb, oy), (xb, oy + 0.75))
    wire(ax, (xa, oy + 0.375), (ox, oy + 0.375), (ox, oy + H)); wire(ax, (xb, oy + 0.375), (ox + W, oy + 0.375), (ox + W, oy + H))
    jdot(ax, (xa, oy + 0.375)); jdot(ax, (xb, oy + 0.375))
    comp(ax, 'L', (ox, oy + H), (ox + W, oy + H))
    caption(ax, ox + W / 2, oy - 0.55, '乙')
    # 丙:一電池 + 兩燈串聯
    ox, oy = 0, 0
    comp(ax, 'bat', (ox, oy), (ox + W, oy))
    wire(ax, (ox, oy), (ox, oy + H)); wire(ax, (ox + W, oy), (ox + W, oy + H))
    comp(ax, 'L', (ox, oy + H), (ox + W / 2, oy + H)); comp(ax, 'L', (ox + W / 2, oy + H), (ox + W, oy + H))
    caption(ax, ox + W / 2, oy - 0.55, '丙')
    # 丁:一電池 + 兩燈並聯
    ox, oy = 4.6, 0
    comp(ax, 'bat', (ox, oy), (ox + W, oy))
    wire(ax, (ox, oy), (ox, oy + H + 0.3)); wire(ax, (ox + W, oy), (ox + W, oy + H + 0.3))
    comp(ax, 'L', (ox, oy + H + 0.3), (ox + W, oy + H + 0.3))
    comp(ax, 'L', (ox, oy + H - 0.5), (ox + W, oy + H - 0.5))
    jdot(ax, (ox, oy + H - 0.5)); jdot(ax, (ox + W, oy + H - 0.5))
    caption(ax, ox + W / 2, oy - 0.55, '丁')
    finish(ax, -0.5, 8.5, -0.9, 5.6)
    save(f, 41004)


# ════════════════ 41005 燈泡 I-V 曲線 ════════════════
@fig(41005)
def f41005():
    f, ax = graph(xlabel='電壓(V)', ylabel='電流(A)')
    v = np.linspace(0, 10, 200)
    ax.plot(v, 0.2 * np.sqrt(v / 2), color=RED, lw=2.2)
    for (x, y) in ((2, 0.2), (8, 0.4)):
        ax.plot([x], [y], 'o', color=RED, ms=6)
        ax.plot([x, x], [0, y], '--', color=GREY, lw=1.2); ax.plot([0, x], [y, y], '--', color=GREY, lw=1.2)
    ax.set_xlim(0, 10); ax.set_ylim(0, 0.5)
    ax.set_xticks(range(0, 11, 2)); ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    save(f, 41005)


# ════════════════ 41006 兩電阻 I-V 圖,並聯總功率 ════════════════
@fig(41006)
def f41006():
    f, ax = graph(xlabel='電壓(V)', ylabel='電流(A)')
    v = np.array([0, 8])
    ax.plot(v, v / 5, color=RED, lw=2.2); ax.plot(v, v / 10, color=BLUE, lw=2.2)
    txt(ax, 7.0, 1.5, '乙', color=RED, fs=14); txt(ax, 7.4, 0.62, '甲', color=BLUE, fs=14)
    ax.set_xlim(0, 8); ax.set_ylim(0, 1.6)
    ax.set_xticks(range(0, 9)); ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6])
    save(f, 41006)


# ════════════════ 41007 安培計讀數 ════════════════
@fig(41007)
def f41007():
    f, ax = new_ax(5.6, 4.0)
    ax.add_patch(Rectangle((-2.6, -1.5), 5.2, 3.8, fill=False, ec=INK, lw=LW))
    R = 2.0
    ang = lambda v: np.radians(150 - 120 * v / 3)
    th = np.linspace(ang(0), ang(3), 100)
    ax.plot(R * np.cos(th), R * np.sin(th), color=INK, lw=1.5)
    for k in range(31):
        v = k / 10; a = ang(v)
        L = 0.28 if k % 10 == 0 else (0.2 if k % 5 == 0 else 0.12)
        ax.plot([R * np.cos(a), (R - L) * np.cos(a)], [R * np.sin(a), (R - L) * np.sin(a)], color=INK, lw=1.2 if k % 5 else 1.5)
        if k % 10 == 0:
            ax.text(1.18 * R * np.cos(a), 1.12 * R * np.sin(a), str(k // 10), fontsize=14, ha='center', va='center', color=INK)
    a = ang(2.4)
    ax.plot([0, 1.85 * np.cos(a)], [0, 1.85 * np.sin(a)], color=RED, lw=2.2)
    ax.plot([0], [0], 'o', ms=8, color=INK)
    ax.text(0, 0.65, 'A', fontsize=18, ha='center', va='center', fontweight='bold', color=INK)
    for x, s in ((-1.3, '−'), (0, '0.6'), (1.3, '3')):
        circle(ax, x, -0.9, 0.14, lw=1.4)
        txt(ax, x + 0.22, -0.65, s, fs=13)
    wire(ax, (-1.3, -1.04), (-1.3, -1.9)); wire(ax, (0, -1.04), (0, -1.9))
    txt(ax, 0.3, -1.85, '導線接在「−」與「0.6」兩端', fs=12, color=BLUE)
    finish(ax, -2.8, 4.0, -2.1, 2.5)
    save(f, 41007)


# ════════════════ 41008 短路 ════════════════
@fig(41008)
def f41008():
    f, ax = new_ax(6.0, 3.4)
    W, H = 5.0, 1.8
    comp(ax, 'bat', (0, 0), (W, 0))
    wire(ax, (0, 0), (0, H)); wire(ax, (W, 0), (W, H))
    comp(ax, 'L', (0, H), (2.2, H), 'L₁', side=-1)
    comp(ax, 'L', (2.2, H), (W - 0.6, H), 'L₂', side=-1)
    wire(ax, (W - 0.6, H), (W, H))
    wire(ax, (2.2, H), (2.2, H + 0.8), (W - 0.6, H + 0.8), (W - 0.6, H))
    jdot(ax, (2.2, H)); jdot(ax, (W - 0.6, H))
    txt(ax, 3.0, H + 0.95, '導線', fs=12, color=BLUE)
    finish(ax, -0.6, 5.6, -0.6, 3.2)
    save(f, 41008)


# ════════════════ 41009 開關並聯 ════════════════
@fig(41009)
def f41009():
    f, ax = new_ax(6.0, 3.6)
    W = 5.0
    comp(ax, 'bat', (0, 0), (W, 0))
    wire(ax, (0, 0), (0, 2.0)); wire(ax, (W, 0), (W, 2.0))
    comp(ax, 'L', (2.8, 2.0), (W, 2.0), 'L', side=-1)
    wire(ax, (0, 2.0), (0.6, 2.0))
    wire(ax, (0.6, 1.5), (0.6, 2.5)); wire(ax, (2.2, 1.5), (2.2, 2.5))
    comp(ax, 'swo', (0.6, 2.5), (2.2, 2.5), 'S₁', side=1, lab_off=0.6)
    comp(ax, 'swo', (0.6, 1.5), (2.2, 1.5), 'S₂', side=-1, lab_off=0.4)
    wire(ax, (2.2, 2.0), (2.8, 2.0))
    jdot(ax, (0.6, 2.0)); jdot(ax, (2.2, 2.0))
    finish(ax, -0.6, 5.6, -0.6, 3.3)
    save(f, 41009)


# ════════════════ 41010 三電阻串聯 ════════════════
@fig(41010)
def f41010():
    f, ax = new_ax(6.4, 3.6)
    W, H = 6.0, 1.8
    comp(ax, 'bat', (0, 0), (W, 0), '9 V', side=-1)
    wire(ax, (0, 0), (0, H)); wire(ax, (W, 0), (W, H))
    comp(ax, 'R', (0, H), (2.0, H), '1 Ω', side=-1)
    comp(ax, 'R', (2.0, H), (4.0, H), '2 Ω', side=-1)
    comp(ax, 'R', (4.0, H), (W, H), '3 Ω', side=-1)
    wire(ax, (2.0, H), (2.0, H + 0.9)); wire(ax, (W, H), (W, H + 0.9))
    comp(ax, 'V', (2.0, H + 0.9), (W, H + 0.9))
    jdot(ax, (2.0, H)); jdot(ax, (W, H))
    finish(ax, -0.6, 6.6, -0.9, 3.2)
    save(f, 41010)


# ════════════════ 41011 不同規格燈泡串聯 ════════════════
@fig(41011)
def f41011():
    f, ax = new_ax(6.0, 3.4)
    W, H = 5.0, 1.8
    # 家用交流電源(~ 符號)
    cx = W / 2
    wire(ax, (0, 0), (cx - 0.35, 0)); wire(ax, (cx + 0.35, 0), (W, 0))
    circle(ax, cx, 0, 0.35, lw=LW)
    ax.plot(np.linspace(cx - 0.2, cx + 0.2, 50), 0.12 * np.sin(np.linspace(0, 2 * np.pi, 50)), color=INK, lw=1.6)
    txt(ax, cx, -0.65, '110 V 家用電源', fs=13, ha='center', va='center')
    wire(ax, (0, 0), (0, H)); wire(ax, (W, 0), (W, H))
    comp(ax, 'L', (0, H), (2.5, H), '甲\n110 V 100 W', side=1, lab_off=0.75, fs=12)
    comp(ax, 'L', (2.5, H), (W, H), '乙\n110 V 25 W', side=1, lab_off=0.75, fs=12)
    finish(ax, -0.6, 5.6, -0.9, 3.0)
    save(f, 41011)


# ════════════════ 41012 交流電波形 ════════════════
@fig(41012)
def f41012():
    f, ax = graph(w=6.0, h=3.6, xlabel='時間(秒)', ylabel='電流(A)')
    t = np.linspace(0, 0.08, 400)
    ax.plot(t, 2 * np.sin(2 * np.pi * 25 * t), color=BLUE, lw=2.2)
    ax.axhline(0, color=INK, lw=1.2)
    ax.set_xlim(0, 0.08); ax.set_ylim(-2.5, 2.5)
    ax.set_xticks([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08])
    ax.set_xticklabels(['0', '', '0.02', '', '0.04', '', '0.06', '', '0.08'])
    ax.set_yticks([-2, -1, 0, 1, 2])
    save(f, 41012)


# ════════════════ 41013 條形磁鐵與指南針 ════════════════
@fig(41013)
def f41013():
    f, ax = new_ax(5.6, 3.2)
    magnet(ax, -1.6, -0.35, 3.2, 0.7, 'N', 'S', fs=16)
    ax.plot([0], [1.2], 'o', ms=7, color=BLUE)
    txt(ax, 0.15, 1.2, 'P', fs=14, va='center')
    finish(ax, -2.2, 2.2, -0.8, 1.7)
    save(f, 41013)


# ════════════════ 41014 由電流變化求電阻 ════════════════
@fig(41014)
def f41014():
    f, ax = new_ax(6.0, 3.8)
    W = 5.0
    comp(ax, 'bat', (0, 0), (2.5, 0), '6 V', side=-1)
    comp(ax, 'A', (2.5, 0), (W, 0))
    wire(ax, (0, 0), (0, 2.6)); wire(ax, (W, 0), (W, 2.6))
    comp(ax, 'R', (0, 1.4), (W, 1.4), 'R₁', side=1)
    comp(ax, 'R', (0, 2.6), (2.8, 2.6), 'R₂', side=1)
    comp(ax, 'swo', (2.8, 2.6), (W, 2.6), 'S', side=1, lab_off=0.55)
    jdot(ax, (0, 1.4)); jdot(ax, (W, 1.4))
    finish(ax, -0.6, 5.6, -0.9, 3.3)
    save(f, 41014)
