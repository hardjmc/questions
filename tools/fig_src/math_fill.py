from fig_all import *   # plt, np, PF, fig, new_ax, save, txt, dot, circle, arc, INK/RED/BLUE/GREY
from matplotlib.patches import Rectangle, Polygon

LIGHT = '#dfe8f5'


# ───────────── 共用:盒狀圖 ─────────────
def boxplot(qid, groups, lo, hi, major, minor, xlabel, w=6.4):
    n = len(groups)
    f, ax = plt.subplots(figsize=(w, 1.5 + 0.95 * n), dpi=200)
    for v in np.arange(lo, hi + 1e-9, minor):
        ax.axvline(v, color='#e4e4e4', lw=0.8, zorder=0)
    for v in np.arange(lo, hi + 1e-9, major):
        ax.axvline(v, color='#c8c8c8', lw=0.9, zorder=0)
    for k, (name, (mn, q1, md, q3, mx)) in enumerate(groups):
        y = n - k
        bh = 0.28
        ax.add_patch(Rectangle((q1, y - bh), q3 - q1, 2 * bh, fc=LIGHT, ec=BLUE, lw=1.8, zorder=2))
        ax.plot([md, md], [y - bh, y + bh], color=BLUE, lw=2.2, zorder=3)
        ax.plot([mn, q1], [y, y], color=INK, lw=1.6, zorder=2)
        ax.plot([q3, mx], [y, y], color=INK, lw=1.6, zorder=2)
        for v in (mn, mx):
            ax.plot([v, v], [y - bh * 0.6, y + bh * 0.6], color=INK, lw=1.6, zorder=2)
        if name:
            ax.text(lo - (hi - lo) * 0.03, y, name, fontproperties=PF, fontsize=14, ha='right', va='center', color=INK)
    ax.set_xlim(lo, hi)
    ax.set_ylim(0.4, n + 0.6)
    ax.set_yticks([])
    ax.set_xticks(np.arange(lo, hi + 1e-9, major))
    ax.set_xticks(np.arange(lo, hi + 1e-9, minor), minor=True)
    for lab in ax.get_xticklabels():
        lab.set_fontproperties(PF); lab.set_fontsize(13)
    for s in ('left', 'right', 'top'):
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.3)
    ax.tick_params(axis='x', width=1.2, length=6)
    ax.tick_params(axis='x', which='minor', width=1.0, length=3.5)
    ax.set_xlabel(xlabel, fontproperties=PF, fontsize=13)
    save(f, qid)


@fig(31100)
def f31100():
    boxplot(31100, [('', (35, 55, 70, 80, 95))], 30, 100, 10, 5, '成績(分)')

@fig(31101)
def f31101():
    boxplot(31101, [('', (2, 5, 7, 11, 16))], 0, 18, 2, 1, '每週運動時數(小時)')

@fig(31102)
def f31102():
    boxplot(31102, [('', (20, 40, 55, 70, 110))], 10, 120, 10, 5, '一分鐘跳繩次數(次)')

@fig(31104)
def f31104():
    boxplot(31104, [('', (2, 6, 8, 10, 24))], 0, 26, 2, 1, '等車時間(分鐘)')

@fig(31106)
def f31106():
    boxplot(31106, [('甲班', (40, 55, 65, 75, 90)), ('乙班', (45, 60, 75, 85, 95))], 30, 100, 10, 5, '成績(分)')

@fig(31107)
def f31107():
    boxplot(31107, [('甲組', (20, 30, 40, 60, 70)), ('乙組', (10, 35, 45, 50, 80))], 0, 90, 10, 5, '')

@fig(31108)
def f31108():
    boxplot(31108, [('甲班', (35, 55, 70, 80, 90)), ('乙班', (45, 50, 60, 65, 95))], 30, 100, 10, 5, '英語成績(分)')

@fig(31113)
def f31113():
    boxplot(31113, [('前測', (20, 35, 45, 60, 85)), ('後測', (30, 60, 70, 80, 95))], 10, 100, 10, 5, '成績(分)')

@fig(31114)
def f31114():
    boxplot(31114, [('', (8, 30, 34, 60, 80))], 0, 90, 10, 2, '')

@fig(31115)
def f31115():
    boxplot(31115, [('甲組', (30, 45, 55, 70, 80)), ('乙組', (15, 50, 55, 60, 95)), ('丙組', (35, 45, 60, 65, 75))], 10, 100, 10, 5, '')

@fig(31119)
def f31119():
    boxplot(31119, [('甲班', (35, 50, 60, 75, 95)), ('乙班', (45, 55, 65, 70, 85))], 30, 100, 10, 5, '數學成績(分)')


@fig(31110)
def f31110():
    f, ax = plt.subplots(figsize=(6.2, 3.0), dpi=200)
    cnt = {1: 1, 2: 2, 3: 3, 4: 1, 5: 2, 6: 1, 7: 1, 8: 1}
    for v, c in cnt.items():
        for k in range(c):
            ax.plot([v], [0.5 + k], 'o', ms=13, color=BLUE)
    ax.set_xlim(-0.3, 9.3)
    ax.set_ylim(0, 3.1)
    ax.set_yticks([])
    ax.set_xticks(range(0, 10))
    for lab in ax.get_xticklabels():
        lab.set_fontproperties(PF); lab.set_fontsize(13)
    for s in ('left', 'right', 'top'):
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.3)
    ax.set_xlabel('一週閱讀時數(小時)', fontproperties=PF, fontsize=13)
    save(f, 31110)


# ───────────── 相似形 ─────────────
def poly(ax, pts, color=INK, lw=1.6, close=True, **kw):
    xs = [p[0] for p in pts] + ([pts[0][0]] if close else [])
    ys = [p[1] for p in pts] + ([pts[0][1]] if close else [])
    ax.plot(xs, ys, color=color, lw=lw, **kw)

def seg(ax, P, Q, color=INK, lw=1.6, **kw):
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=color, lw=lw, **kw)

def mid(P, Q):
    return ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)

def angarc(ax, V, P, Q, r, color=RED, lw=1.4):
    a0 = np.degrees(np.arctan2(P[1] - V[1], P[0] - V[0]))
    a1 = np.degrees(np.arctan2(Q[1] - V[1], Q[0] - V[0]))
    d = (a1 - a0) % 360
    if d > 180:
        a0, a1, d = a1, a0, 360 - d
    arc(ax, V[0], V[1], r, a0, a0 + d, color=color, lw=lw)
    return np.radians(a0 + d / 2)

def anglab(ax, V, P, Q, r, s, rl=None, color=RED, fs=13):
    m = angarc(ax, V, P, Q, r, color=color)
    rl = rl or r * 1.9
    txt(ax, V[0] + rl * np.cos(m), V[1] + rl * np.sin(m), s, color=color, fs=fs, ha='center', va='center')

def rightmark(ax, V, P, Q, s=0.25, color=INK):
    u = np.array(P) - np.array(V); u = u / np.linalg.norm(u) * s
    w = np.array(Q) - np.array(V); w = w / np.linalg.norm(w) * s
    V = np.array(V)
    poly(ax, [V + u, V + u + w, V + w], color=color, lw=1.2, close=False)

def lab(ax, P, s, dx=0, dy=0, fs=14, color=INK):
    txt(ax, P[0] + dx, P[1] + dy, s, color=color, fs=fs, ha='center', va='center')


@fig(31122)
def f31122():
    f, ax = new_ax(6.4, 3.6)
    base = [(0, 0), (6, 0), (6 + 9 * np.cos(np.radians(78)), 9 * np.sin(np.radians(78))), (-0.8, 5.2)]
    s1, s2 = 0.26, 0.26 * 10 / 6
    P1 = [(x * s1, y * s1) for x, y in base]
    P2 = [(x * s2 + 3.6, y * s2) for x, y in base]
    poly(ax, P1, lw=1.7); poly(ax, P2, lw=1.7)
    for P, names in ((P1, 'ABCD'), (P2, 'EFGH')):
        off = [(-0.15, -0.18), (0.15, -0.18), (0.18, 0.12), (-0.2, 0.08)]
        for p, nm, (dx, dy) in zip(P, names, off):
            lab(ax, p, nm, dx, dy)
    lab(ax, mid(P1[0], P1[1]), '6', 0, -0.25, color=BLUE)
    lab(ax, mid(P1[1], P1[2]), '9', 0.25, 0, color=BLUE)
    lab(ax, mid(P2[0], P2[1]), '10', 0, -0.25, color=BLUE)
    lab(ax, mid(P2[1], P2[2]), '?', 0.27, 0, color=RED, fs=15)
    ax.set_xlim(-0.6, 7.0)
    save(f, 31122)


@fig(31124)
def f31124():
    f, ax = new_ax(6.0, 4.0)
    th = np.linspace(0, 2 * np.pi, 200)
    ax0 = -2 * np.sqrt(3)
    ax.fill(ax0 + 0.9 * np.cos(th), 2.0 * np.sin(th), color='#d6e6f7', zorder=0)
    ax.plot(ax0 + 0.9 * np.cos(th), 2.0 * np.sin(th), color=BLUE, lw=1.3)
    txt(ax, ax0, 0, '池塘', color=BLUE, fs=13, ha='center', va='center')
    O, A, B, C, D = (0, 0), (ax0, 2.0), (ax0, -2.0), (np.sqrt(3) / 2, -0.5), (np.sqrt(3) / 2, 0.5)
    seg(ax, A, C); seg(ax, B, D); seg(ax, C, D)
    for P, s, dx, dy in ((O, 'O', -0.05, -0.32), (A, 'A', -0.25, 0.2), (B, 'B', -0.25, -0.22), (C, 'C', 0.25, -0.15), (D, 'D', 0.25, 0.15)):
        ax.plot(*P, 'o', ms=4, color=INK); lab(ax, P, s, dx, dy)
    lab(ax, mid(A, O), '40', 0.1, 0.3, color=RED)
    lab(ax, mid(O, C), '10', 0.05, -0.32, color=RED, fs=13)
    lab(ax, mid(C, D), '8', 0.25, 0, color=RED, fs=13)
    save(f, 31124)


@fig(31126)
def f31126():
    f, ax = new_ax(6.0, 3.4)
    C, A, B = (0, 0), (6, 0), (0, 3)
    D, E, F = (2, 0), (2, 2), (0, 2)
    poly(ax, [A, B, C])
    poly(ax, [C, D, E, F], color=BLUE, lw=1.6)
    rightmark(ax, C, A, B, 0.22)
    for P, s, dx, dy in ((A, 'A', 0.22, -0.1), (B, 'B', -0.22, 0.12), (C, 'C', -0.22, -0.2), (D, 'D', 0, -0.28), (E, 'E', 0.18, 0.2), (F, 'F', -0.25, 0)):
        lab(ax, P, s, dx, dy)
    lab(ax, (4.2, 0), '', 0, 0)
    txt(ax, 4.2, -0.32, 'AC = 6', color=RED, fs=13, ha='center', va='center')
    txt(ax, -0.75, 1.0, 'BC = 3', color=RED, fs=13, ha='center', va='center', rotation=90)
    save(f, 31126)


@fig(31128)
def f31128():
    f, ax = new_ax(6.0, 3.8)
    B, C = (0, 0), (9, 0)
    A = (6 * np.cos(np.radians(60)), 6 * np.sin(np.radians(60)))
    D = (4, 0)
    poly(ax, [A, B, C]); seg(ax, A, D)
    angarc(ax, A, B, D, 0.7); angarc(ax, C, B, A, 1.0)
    for P, s, dx, dy in ((A, 'A', 0, 0.3), (B, 'B', -0.3, -0.15), (C, 'C', 0.3, -0.15), (D, 'D', 0, -0.35)):
        lab(ax, P, s, dx, dy)
    lab(ax, mid(A, B), '6', -0.35, 0.1, color=BLUE)
    lab(ax, mid(B, D), '4', 0, -0.35, color=BLUE)
    save(f, 31128)


@fig(31130)
def f31130():
    f, ax = new_ax(6.0, 3.4)
    B, C, A, D = (0, 0), (10, 0), (2, 5), (6, 5)
    E = (A[0] + (B[0] - A[0]) / 3, A[1] + (B[1] - A[1]) / 3)
    F = (D[0] + (C[0] - D[0]) / 3, D[1] + (C[1] - D[1]) / 3)
    poly(ax, [A, B, C, D]); seg(ax, E, F, color=BLUE)
    for P, s, dx, dy in ((A, 'A', -0.2, 0.3), (D, 'D', 0.2, 0.3), (B, 'B', -0.3, -0.2), (C, 'C', 0.3, -0.2), (E, 'E', -0.4, 0), (F, 'F', 0.4, 0)):
        lab(ax, P, s, dx, dy)
    lab(ax, mid(A, D), '4', 0, 0.35, color=RED)
    lab(ax, mid(B, C), '10', 0, -0.4, color=RED)
    save(f, 31130)


@fig(31133)
def f31133():
    f, ax = new_ax(6.0, 4.0)
    A, B, C = (3, 6), (0, 0), (9, 0)
    D, E = (2, 4), (5, 4)
    O = (3.75, 3.0)  # BE 與 CD 交點:B + t(E−B), t=0.75
    poly(ax, [A, B, C]); seg(ax, D, E); seg(ax, B, E, color=BLUE); seg(ax, C, D, color=BLUE)
    for P, s, dx, dy in ((A, 'A', 0, 0.35), (B, 'B', -0.3, -0.2), (C, 'C', 0.3, -0.2), (D, 'D', -0.35, 0.05), (E, 'E', 0.35, 0.05), (O, 'O', 0, -0.4)):
        lab(ax, P, s, dx, dy)
    save(f, 31133)


@fig(31135)
def f31135():
    f, ax = new_ax(6.0, 3.8)
    A, B = (0, 0), (2, 0)
    C = (2 * np.cos(np.radians(36)), 2 * np.sin(np.radians(36)))
    t = np.sqrt(5) - 1
    D = (t * np.cos(np.radians(36)), t * np.sin(np.radians(36)))
    poly(ax, [A, B, C]); seg(ax, B, D, color=BLUE)
    anglab(ax, A, B, C, 0.28, '36°', rl=0.48)
    for P, s, dx, dy in ((A, 'A', -0.1, -0.06), (B, 'B', 0.1, -0.06), (C, 'C', 0.06, 0.08), (D, 'D', -0.08, 0.08)):
        lab(ax, P, s, dx, dy)
    lab(ax, mid(A, B), 'AB = 2', 0, -0.1, color=RED)
    lab(ax, mid(A, C), 'AC = 2', -0.2, 0.1, color=RED)
    save(f, 31135)


@fig(31136)
def f31136():
    f, ax = new_ax(6.0, 4.4)
    B, A, D, C = (0, 0), (0, 6), (8, 0), (8, 3)
    P = (16 / 3, 2)
    seg(ax, (-0.8, 0), (8.8, 0), lw=1.4)
    for x in np.arange(-0.6, 8.8, 0.5):
        seg(ax, (x, 0), (x - 0.3, -0.3), color=GREY, lw=0.9)
    seg(ax, B, A, lw=3); seg(ax, D, C, lw=3)
    seg(ax, A, D, color=BLUE); seg(ax, C, B, color=BLUE)
    for Pt, s, dx, dy in ((A, 'A', -0.35, 0.1), (B, 'B', -0.3, -0.5), (C, 'C', 0.35, 0.1), (D, 'D', 0.3, -0.5), (P, 'P', 0, 0.45)):
        lab(ax, Pt, s, dx, dy)
    ax.plot(*P, 'o', ms=4, color=INK)
    txt(ax, -0.45, 3, '6 公尺', color=RED, fs=13, ha='right', va='center')
    txt(ax, 8.45, 1.5, '3 公尺', color=RED, fs=13, ha='left', va='center')
    txt(ax, 4, -0.75, '8 公尺', color=RED, fs=13, ha='center', va='center')
    save(f, 31136)


# ───────────── 圓的性質 ─────────────
def onc(deg, r=1.0, c=(0, 0)):
    return (c[0] + r * np.cos(np.radians(deg)), c[1] + r * np.sin(np.radians(deg)))

def plab(ax, deg, s, r=1.14, fs=14):
    p = onc(deg, r)
    lab(ax, p, s, fs=fs)


@fig(31137)
def f31137():
    f, ax = new_ax(4.8, 4.0)
    circle(ax, 0, 0, 1)
    A, B, C, D = onc(170), onc(250), onc(350), onc(90)
    poly(ax, [A, B, C, D], color=BLUE)
    dot(ax, 0, 0, 'O', dx=0.05, dy=-0.12)
    for d, s in ((170, 'A'), (250, 'B'), (350, 'C'), (90, 'D')):
        plab(ax, d, s)
    anglab(ax, A, B, D, 0.2, '100°', rl=0.42)
    anglab(ax, C, B, D, 0.2, '?', rl=0.38, fs=15)
    save(f, 31137)


@fig(31138)
def f31138():
    f, ax = new_ax(4.8, 4.0)
    circle(ax, 0, 0, 1)
    A, B, C, D = onc(235), onc(305), onc(60), onc(130)
    for X in (C, D):
        seg(ax, X, A, color=BLUE); seg(ax, X, B, color=BLUE)
    seg(ax, A, B)
    for d, s in ((235, 'A'), (305, 'B'), (60, 'C'), (130, 'D')):
        plab(ax, d, s)
    anglab(ax, C, A, B, 0.3, '35°', rl=0.5)
    anglab(ax, D, A, B, 0.3, '?', rl=0.45, fs=15)
    save(f, 31138)


@fig(31141)
def f31141():
    f, ax = new_ax(4.8, 4.0)
    circle(ax, 0, 0, 1)
    A, B, C, D = onc(180), onc(0), onc(112), onc(235)
    seg(ax, A, B); seg(ax, B, C, color=BLUE); seg(ax, D, B, color=BLUE); seg(ax, D, C, color=BLUE)
    dot(ax, 0, 0, 'O', dx=-0.04, dy=0.07)
    for d, s in ((180, 'A'), (0, 'B'), (112, 'C'), (235, 'D')):
        plab(ax, d, s)
    anglab(ax, B, A, C, 0.32, '34°', rl=0.55)
    anglab(ax, D, B, C, 0.25, '?', rl=0.42, fs=15)
    save(f, 31141)


@fig(31142)
def f31142():
    f, ax = new_ax(4.8, 4.0)
    circle(ax, 0, 0, 1)
    A, B, C, O = onc(205), onc(335), onc(90), (0, 0)
    seg(ax, O, A); seg(ax, O, B); seg(ax, A, B)
    seg(ax, C, A, color=BLUE); seg(ax, C, B, color=BLUE)
    ax.plot(0, 0, 'o', ms=4, color=INK); lab(ax, O, 'O', 0, 0.13)
    for d, s in ((205, 'A'), (335, 'B'), (90, 'C')):
        plab(ax, d, s)
    anglab(ax, A, O, B, 0.3, '25°', rl=0.52, fs=12)
    anglab(ax, C, A, B, 0.25, '?', rl=0.42, fs=15)
    save(f, 31142)


@fig(31143)
def f31143():
    f, ax = new_ax(5.2, 4.0)
    circle(ax, 0, 0, 1)
    A, B, C, D, O = onc(90), onc(200), onc(275), onc(350), (0, 0)
    poly(ax, [A, B, C, D], color=BLUE)
    v = np.array(C) - np.array(B); E = tuple(np.array(C) + v / np.linalg.norm(v) * 0.75)
    seg(ax, C, E, color=BLUE)
    seg(ax, O, B); seg(ax, O, D)
    ax.plot(0, 0, 'o', ms=4, color=INK); lab(ax, O, 'O', 0, 0.14)
    for d, s in ((90, 'A'), (200, 'B'), (275, 'C'), (350, 'D')):
        plab(ax, d, s)
    lab(ax, E, 'E', 0.1, -0.12)
    anglab(ax, C, D, E, 0.2, '75°', rl=0.42, fs=12)
    anglab(ax, O, B, D, 0.15, '?', rl=0.3, fs=14)
    save(f, 31143)


@fig(31145)
def f31145():
    f, ax = new_ax(5.6, 4.2)
    t = [2, 5, 4, 4]  # A,B,C,D 的切線段長
    lo, hi = 0.1, 10
    for _ in range(80):
        r = (lo + hi) / 2
        s = sum(np.arctan(r / x) for x in t)
        lo, hi = (r, hi) if s < np.pi else (lo, r)
    circle(ax, 0, 0, r)
    th = 200.0
    V = []
    for x in t:
        a = np.degrees(np.arctan(r / x))
        cen = 180 - 2 * a
        V.append(onc(th + cen / 2, np.hypot(r, x)))
        th += cen
    poly(ax, V, color=BLUE)
    ax.plot(0, 0, 'o', ms=4, color=INK); lab(ax, (0, 0), 'O', 0.45, 0.3)
    names = 'ABCD'
    for P, s in zip(V, names):
        u = np.array(P) / np.linalg.norm(P)
        lab(ax, tuple(np.array(P) + u * 0.45), s)
    for i, s in ((0, '7'), (1, '9'), (2, '8')):
        P, Q = V[i], V[(i + 1) % 4]
        m = np.array(mid(P, Q)); u = m / np.linalg.norm(m)
        lab(ax, tuple(m + u * 0.4), s, color=RED)
    save(f, 31145)


@fig(31147)
def f31147():
    f, ax = new_ax(4.8, 4.0)
    circle(ax, 0, 0, 1)
    A, B, C, D = onc(150), onc(50), onc(-60), onc(-110)
    seg(ax, A, C, color=BLUE); seg(ax, B, D, color=BLUE); seg(ax, B, C)
    # 交點 P
    a1, a2 = np.array(A), np.array(C); b1, b2 = np.array(B), np.array(D)
    M = np.array([a2 - a1, b1 - b2]).T
    s = np.linalg.solve(M, b1 - a1)
    P = tuple(a1 + s[0] * (a2 - a1))
    ax.plot(*P, 'o', ms=4, color=INK)
    for d, nm in ((150, 'A'), (50, 'B'), (-60, 'C'), (-110, 'D')):
        plab(ax, d, nm)
    lab(ax, P, 'P', -0.16, -0.05)
    anglab(ax, B, C, D, 0.32, '25°', rl=0.52, fs=12)
    anglab(ax, P, A, B, 0.13, '?', rl=0.27, fs=14)
    save(f, 31147)


@fig(31148)
def f31148():
    f, ax = new_ax(6.0, 3.4)
    th = np.linspace(0, np.pi, 200)
    ax.plot(5 * np.cos(th), 5 * np.sin(th), color=INK, lw=1.6)
    seg(ax, (-5, 0), (5, 0))
    s = 2 * np.sqrt(5)
    poly(ax, [(-s / 2, 0), (s / 2, 0), (s / 2, s), (-s / 2, s)], color=BLUE, lw=1.8)
    ax.plot(0, 0, 'o', ms=4, color=INK); lab(ax, (0, 0), 'O', 0, -0.45)
    save(f, 31148)


@fig(31149)
def f31149():
    f, ax = new_ax(5.6, 4.0)
    O, P = (0, 0), (6, 0)
    A, B = onc(60, 3), onc(-60, 3)
    th = np.radians(np.linspace(-60, 60, 80))
    xs = list(3 * np.cos(th)) + [P[0]]
    ys = list(3 * np.sin(th)) + [P[1]]
    ax.fill(xs, ys, color='#f6d3cf', zorder=0)
    circle(ax, 0, 0, 3)
    seg(ax, P, A, color=BLUE); seg(ax, P, B, color=BLUE)
    ax.plot(0, 0, 'o', ms=4, color=INK); lab(ax, O, 'O', -0.35, 0)
    lab(ax, A, 'A', 0.05, 0.35); lab(ax, B, 'B', 0.05, -0.35); lab(ax, P, 'P', 0.35, 0)
    anglab(ax, P, A, B, 0.9, '60°', rl=1.45, fs=13)
    save(f, 31149)


# ───────────── 幾何證明 ─────────────
@fig(31151)
def f31151():
    f, ax = new_ax(5.6, 4.0)
    O = (0, 0)
    ang = 2 * np.degrees(np.arctan2(4, 3))
    A_ = (7, 0); B_ = onc(ang, 6.2)
    P = (3, 4); D = (3, 0)
    u = np.array(onc(ang)); E = tuple(u * np.dot(u, np.array(P)))
    seg(ax, O, A_); seg(ax, O, B_)
    seg(ax, O, onc(np.degrees(np.arctan2(4, 3)), 6.5), color=GREY, lw=1.3, ls='--')
    seg(ax, P, D, color=BLUE); seg(ax, P, E, color=BLUE); seg(ax, O, P, color=INK, lw=1.3)
    rightmark(ax, D, O, P, 0.3); rightmark(ax, E, O, P, 0.3)
    arc(ax, 0, 0, 0.8, 0, np.degrees(np.arctan2(4, 3)))
    arc(ax, 0, 0, 0.95, np.degrees(np.arctan2(4, 3)), ang)
    for Pt, s, dx, dy in ((O, 'O', -0.3, -0.2), (A_, 'A', 0.3, 0), (B_, 'B', -0.15, 0.3), (P, 'P', 0.3, 0.15), (D, 'D', 0, -0.35), (E, 'E', -0.35, 0.05)):
        lab(ax, Pt, s, dx, dy)
    lab(ax, mid(P, D), '4', 0.3, 0, color=RED)
    lab(ax, mid(O, P), '5', 0.3, -0.25, color=RED)
    save(f, 31151)


@fig(31154)
def f31154():
    f, ax = new_ax(6.0, 3.6)
    B, C, A = (0, 0), (10, 0), (3.6, 4.8)
    E, D = (6.8, 2.4), (5, 0)
    poly(ax, [A, B, C]); seg(ax, A, D)
    Ext = (E[0] + 0.45 * 3, E[1] + 0.45 * 4)
    seg(ax, D, Ext, color=BLUE)
    rightmark(ax, E, C, Ext, 0.3, color=BLUE)
    for X in (mid(A, E), mid(E, C)):
        v = np.array(C) - np.array(A); n = np.array([-v[1], v[0]]) / np.linalg.norm(v) * 0.15
        seg(ax, tuple(np.array(X) - n), tuple(np.array(X) + n), color=RED, lw=1.4)
    for Pt, s, dx, dy in ((A, 'A', -0.1, 0.35), (B, 'B', -0.3, -0.2), (C, 'C', 0.3, -0.2), (D, 'D', 0, -0.4), (E, 'E', -0.05, 0.45)):
        lab(ax, Pt, s, dx, dy)
    lab(ax, mid(A, B), 'AB = 6', -0.85, 0.15, color=RED)
    lab(ax, mid(B, C), 'BC = 10', 2.9, -0.4, color=RED)
    lab(ax, (5.9, 4.15), 'AC = 8', 0, 0, color=RED)
    save(f, 31154)


@fig(31156)
def f31156():
    f, ax = new_ax(4.8, 4.0)
    A, B, C, O = onc(100), onc(200), onc(340), (0, 0)
    poly(ax, [A, B, C])
    seg(ax, O, B, color=BLUE); seg(ax, O, C, color=BLUE)
    ax.plot(0, 0, 'o', ms=4, color=INK); lab(ax, O, 'O', 0, 0.13)
    plab(ax, 100, 'A'); plab(ax, 200, 'B'); plab(ax, 340, 'C')
    anglab(ax, B, C, O, 0.38, '20°', rl=0.6, fs=12)
    anglab(ax, A, B, C, 0.2, '?', rl=0.36, fs=15)
    save(f, 31156)


@fig(31157)
def f31157():
    f, ax = new_ax(6.0, 3.6)
    C, B, A, D = (0, 0), (9, 0), (0, 3 * np.sqrt(3)), (3, 0)
    poly(ax, [A, B, C]); seg(ax, A, D, color=BLUE)
    rightmark(ax, C, B, A, 0.35)
    angarc(ax, A, C, D, 0.8); angarc(ax, A, D, B, 1.0)
    for Pt, s, dx, dy in ((A, 'A', -0.3, 0.2), (B, 'B', 0.35, -0.15), (C, 'C', -0.35, -0.2), (D, 'D', 0, -0.4)):
        lab(ax, Pt, s, dx, dy)
    lab(ax, mid(C, D), '3', 0, -0.4, color=RED)
    save(f, 31157)


@fig(31159)
def f31159():
    f, ax = new_ax(6.0, 3.4)
    C, A = (0, 0), (6, 0)
    B = (0, 6 * np.tan(np.radians(25)))
    M = mid(A, B)
    poly(ax, [A, B, C]); seg(ax, C, M, color=BLUE)
    rightmark(ax, C, A, B, 0.25)
    anglab(ax, A, B, C, 0.9, '25°', rl=1.35, fs=13)
    anglab(ax, M, B, C, 0.3, '?', rl=0.5, fs=15)
    for Pt, s, dx, dy in ((A, 'A', 0.3, -0.1), (B, 'B', -0.25, 0.2), (C, 'C', -0.3, -0.2), (M, 'M', 0.2, 0.25)):
        lab(ax, Pt, s, dx, dy)
    save(f, 31159)


@fig(31160)
def f31160():
    f, ax = new_ax(6.4, 3.4)
    ang = np.radians(78)
    B, C = (0, 0), (10, 0)
    A = (5 * np.cos(ang), 5 * np.sin(ang))
    D = (A[0] + 10, A[1]); E = (A[0] + 5, A[1])
    poly(ax, [A, B, C, D]); seg(ax, B, E, color=BLUE); seg(ax, C, E, color=BLUE)
    for V, P, Q, r in ((B, A, E, 0.8), (B, E, C, 1.0), (C, B, E, 0.8), (C, E, D, 1.0)):
        angarc(ax, V, P, Q, r)
    for Pt, s, dx, dy in ((A, 'A', -0.3, 0.25), (B, 'B', -0.3, -0.25), (C, 'C', 0.3, -0.25), (D, 'D', 0.3, 0.25), (E, 'E', 0, 0.35)):
        lab(ax, Pt, s, dx, dy)
    lab(ax, mid(A, B), '5', -0.4, 0, color=RED)
    save(f, 31160)


@fig(31161)
def f31161():
    f, ax = new_ax(6.0, 3.6)
    A, B, C, D = (0, 4), (0, 0), (4, 0), (4, 4)
    E = (4 + 2 * np.sqrt(3), 2)
    poly(ax, [A, B, C, D]); poly(ax, [C, E, D])
    seg(ax, A, E, color=BLUE); seg(ax, B, E, color=BLUE)
    anglab(ax, E, A, B, 1.1, '?', rl=1.5, fs=15)
    for Pt, s, dx, dy in ((A, 'A', -0.3, 0.2), (B, 'B', -0.3, -0.2), (C, 'C', 0.05, -0.35), (D, 'D', 0.05, 0.35), (E, 'E', 0.35, 0)):
        lab(ax, Pt, s, dx, dy)
    save(f, 31161)


@fig(31162)
def f31162():
    f, ax = new_ax(5.6, 4.2)
    B, C = (0, 0), (7, 0)
    A = (5.5, np.sqrt(33.75))
    I = ((7 * A[0] + 8 * C[0]) / 21, (7 * A[1]) / 21)
    t = I[1] / A[1]
    D = (A[0] * t, I[1]); E = (C[0] + (A[0] - C[0]) * t, I[1])
    poly(ax, [A, B, C]); seg(ax, D, E, color=BLUE)
    ax.plot(*I, 'o', ms=4, color=INK)
    for Pt, s, dx, dy in ((A, 'A', 0, 0.35), (B, 'B', -0.3, -0.2), (C, 'C', 0.3, -0.2), (D, 'D', -0.35, 0.05), (E, 'E', 0.35, 0.05), (I, 'I', 0, 0.3)):
        lab(ax, Pt, s, dx, dy)
    lab(ax, mid(A, B), 'AB = 8', -0.8, 0.15, color=RED)
    lab(ax, mid(A, C), 'AC = 6', 0.8, 0.1, color=RED)
    lab(ax, mid(B, C), 'BC = 7', 0, -0.4, color=RED)
    save(f, 31162)


# ───────────── 立體圖形 ─────────────
def net(ax, cells, labels=None, x0=0.0, y0=0.0, s=1.0, color=INK, fill='#eef3fb'):
    for k, (c, r) in enumerate(cells):
        x, y = x0 + c * s, y0 - r * s
        ax.add_patch(Rectangle((x, y - s), s, s, fc=fill, ec=color, lw=1.6))
        if labels:
            txt(ax, x + s / 2, y - s / 2, labels[k], fs=16, ha='center', va='center')


@fig(31163)
def f31163():
    f, ax = new_ax(5.4, 3.6)
    cells = [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2)]
    net(ax, cells, ['1', '2', '3', '4', '5', '6'])
    ax.set_xlim(-0.2, 4.2); ax.set_ylim(-3.2, 0.2)
    save(f, 31163)


@fig(31164)
def f31164():
    f, ax = new_ax(4.6, 3.6)
    grid = [[3, 1, None], [2, 2, 1], [1, None, 2]]
    for r in range(3):
        for c in range(3):
            v = grid[r][c]
            ax.add_patch(Rectangle((c, 2 - r), 1, 1, fc=('#eef3fb' if v else 'white'), ec=INK, lw=1.6))
            if v:
                txt(ax, c + 0.5, 2.5 - r, str(v), fs=17, ha='center', va='center')
    txt(ax, 1.5, 3.3, '俯視圖', fs=13, ha='center', va='center')
    ax.set_xlim(-0.8, 3.8); ax.set_ylim(-0.2, 3.6)
    save(f, 31164)


NETS = [  # 依選項順序:0 1-4-1、1 3-3、2 不能摺(田字)、3 2-2-2
    [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (4, 1)],
    [(0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (3, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],
]
def netopt(i):
    f, ax = new_ax(4.6, 3.0)
    net(ax, NETS[i])
    ax.set_xlim(-0.3, 5.3); ax.set_ylim(-3.3, 0.3)
    save(f, 31167 * 10 + i)

for _i in range(4):
    fig(31167 * 10 + _i)(lambda _i=_i: netopt(_i))


@fig(31169)
def f31169():
    f, ax = new_ax(6.0, 4.4)
    L = [(0, 0), (6, 0), (6, 2), (3, 2), (3, 5), (0, 5)]
    d = np.array([1.6, 1.2])
    Lb = [tuple(np.array(p) + d) for p in L]
    ax.add_patch(Polygon(L, closed=True, fc='#eef3fb', ec=INK, lw=1.7))
    # 可見的後方稜
    for i, j in ((1, 2), (2, 3), (3, 4), (4, 5)):
        seg(ax, Lb[i], Lb[j])
    seg(ax, Lb[5], Lb[0], ls='--', lw=1.2, color=GREY); seg(ax, Lb[0], Lb[1], ls='--', lw=1.2, color=GREY)
    for k in (1, 2, 3, 4, 5):
        seg(ax, L[k], Lb[k])
    seg(ax, L[0], Lb[0], ls='--', lw=1.2, color=GREY)
    for P, Q, s, dx, dy in ((L[0], L[1], '6', 0, -0.35), (L[1], L[2], '2', 0.3, -0.25), (L[2], L[3], '3', 0, -0.3),
                            (L[3], L[4], '3', -0.3, 0), (L[4], L[5], '3', -0.3, 0.35), (L[5], L[0], '5', -0.35, 0)):
        lab(ax, mid(P, Q), s, dx, dy, color=RED)
    lab(ax, mid(L[1], Lb[1]), '4', 0.4, -0.15, color=RED)
    save(f, 31169)


@fig(31172)
def f31172():
    f, ax = new_ax(5.6, 4.2)
    P1, P2, P3, P4 = (0, 0), (6, 0), (8.2, 1.6), (2.2, 1.6)
    V = (4.1, 5.0)
    seg(ax, P1, P2); seg(ax, P2, P3)
    seg(ax, P3, P4, ls='--', color=GREY, lw=1.2); seg(ax, P4, P1, ls='--', color=GREY, lw=1.2)
    seg(ax, V, P4, ls='--', color=GREY, lw=1.2)
    for P in (P1, P2, P3):
        seg(ax, V, P, color=BLUE)
    lab(ax, mid(P1, P2), '6', 0, -0.4, color=RED)
    lab(ax, mid(V, P2), '5', 0.4, 0.05, color=RED)
    save(f, 31172)


@fig(31173)
def f31173():
    f, ax = new_ax(6.0, 3.4)
    A, B, C = (0, 0), (5, 0), (1.8, 2.4)
    seg(ax, (-1.2, 0), (0, 0), color=GREY, lw=1.3, ls='-.'); seg(ax, (5, 0), (6.4, 0), color=GREY, lw=1.3, ls='-.')
    txt(ax, -1.2, 0.15, '旋轉軸', fs=12, color=GREY)
    ax.add_patch(Polygon([A, B, C], closed=True, fc='#eef3fb', ec=INK, lw=1.7))
    rightmark(ax, C, A, B, 0.28)
    th = np.linspace(np.radians(200), np.radians(500), 80)
    ax.plot(6.0 + 0.18 * np.cos(th), 0.55 * np.sin(th), color=RED, lw=1.4)
    ax.annotate('', xy=(6.0 + 0.18 * np.cos(th[-1]), 0.55 * np.sin(th[-1])), xytext=(6.0 + 0.18 * np.cos(th[-4]), 0.55 * np.sin(th[-4])),
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.4))
    for Pt, s, dx, dy in ((A, 'A', -0.2, -0.35), (B, 'B', 0.15, -0.35), (C, 'C', 0, 0.3)):
        lab(ax, Pt, s, dx, dy)
    lab(ax, mid(A, C), '3', -0.3, 0.15, color=RED)
    lab(ax, mid(B, C), '4', 0.3, 0.2, color=RED)
    save(f, 31173)


@fig(31175)
def f31175():
    f, ax = new_ax(5.0, 4.0)
    s = 4.0; d = np.array([1.8, 1.4])
    F = [np.array(p, float) for p in [(0, 0), (s, 0), (s, s), (0, s)]]
    Bk = [p + d for p in F]
    poly(ax, [tuple(p) for p in F])
    seg(ax, tuple(Bk[1]), tuple(Bk[2])); seg(ax, tuple(Bk[2]), tuple(Bk[3]))
    seg(ax, tuple(Bk[3]), tuple(Bk[0]), ls='--', color=GREY, lw=1.2); seg(ax, tuple(Bk[0]), tuple(Bk[1]), ls='--', color=GREY, lw=1.2)
    for k in (1, 2, 3):
        seg(ax, tuple(F[k]), tuple(Bk[k]))
    seg(ax, tuple(F[0]), tuple(Bk[0]), ls='--', color=GREY, lw=1.2)
    V = F[2]
    m1 = (V + F[1]) / 2; m2 = (V + F[3]) / 2; m3 = V + d / 2
    ax.add_patch(Polygon([tuple(V), tuple(m1), tuple(m3)], closed=True, fc='#f6d3cf', ec='none'))
    ax.add_patch(Polygon([tuple(V), tuple(m2), tuple(m3)], closed=True, fc='#f6d3cf', ec='none'))
    ax.add_patch(Polygon([tuple(V), tuple(m1), tuple(m2)], closed=True, fc='#f6d3cf', ec='none'))
    poly(ax, [tuple(m1), tuple(m2), tuple(m3)], color=RED, lw=1.8)
    for m in (m1, m2, m3):
        ax.plot(*m, 'o', ms=4.5, color=RED)
    save(f, 31175)


# ───────────── 二次函數 ─────────────
def grid_axes(ax, x0, x1, y0, y1):
    for x in range(x0, x1 + 1):
        ax.plot([x, x], [y0, y1], color='#e2e2e2', lw=0.8, zorder=0)
    for y in range(y0, y1 + 1):
        ax.plot([x0, x1], [y, y], color='#e2e2e2', lw=0.8, zorder=0)
    ax.annotate('', xy=(x1 + 0.4, 0), xytext=(x0 - 0.2, 0), arrowprops=dict(arrowstyle='->', color=INK, lw=1.3))
    ax.annotate('', xy=(0, y1 + 0.4), xytext=(0, y0 - 0.2), arrowprops=dict(arrowstyle='->', color=INK, lw=1.3))
    txt(ax, x1 + 0.45, -0.1, 'x', fs=14, va='top')
    txt(ax, 0.15, y1 + 0.35, 'y', fs=14)
    for x in range(x0, x1 + 1):
        if x != 0:
            txt(ax, x, -0.18, str(x).replace('-', '−'), fs=12, ha='center', va='top')
    for y in range(y0, y1 + 1):
        if y != 0:
            txt(ax, -0.15, y, str(y).replace('-', '−'), fs=12, ha='right', va='center')
    txt(ax, -0.15, -0.18, 'O', fs=12, ha='right', va='top')


@fig(31176)
def f31176():
    f, ax = new_ax(5.4, 4.2)
    grid_axes(ax, -4, 2, -3, 3)
    x = np.linspace(-3.3, 1.3, 200)
    ax.plot(x, -(x + 1) ** 2 + 2, color=BLUE, lw=2)
    for P in ((-1, 2), (0, 1)):
        ax.plot(*P, 'o', ms=5, color=BLUE)
    ax.set_xlim(-4.6, 2.8); ax.set_ylim(-3.4, 3.7)
    save(f, 31176)


@fig(31178)
def f31178():
    f, ax = new_ax(5.0, 4.4)
    grid_axes(ax, -2, 4, -2, 5)
    x = np.linspace(-1.9, 3.9, 200)
    ax.plot(x, -x ** 2 + 2 * x + 3, color=BLUE, lw=2)
    for P in ((-1, 0), (3, 0), (1, 4), (0, 3)):
        ax.plot(*P, 'o', ms=5, color=BLUE)
    ax.set_xlim(-2.6, 4.8); ax.set_ylim(-2.4, 5.7)
    save(f, 31178)


@fig(31181)
def f31181():
    f, ax = new_ax(6.0, 3.6)
    x = np.linspace(-5, 5, 200)
    ax.plot(x, 5 - x ** 2 / 5, color=INK, lw=2)
    seg(ax, (-6, 0), (6, 0), lw=1.4)
    seg(ax, (0, -0.5), (0, 5), color=GREY, lw=1.2, ls='--')
    ax.add_patch(Rectangle((0.5, 0), 3, 1.9, fc='#eef3fb', ec=BLUE, lw=1.6))
    txt(ax, 2.0, 0.95, '貨車', fs=13, ha='center', va='center', color=BLUE)
    # 地面寬度
    ax.annotate('', xy=(-5, -1.0), xytext=(5, -1.0), arrowprops=dict(arrowstyle='<->', color=RED, lw=1.2))
    txt(ax, -2.5, -1.35, '10 公尺', fs=13, ha='center', va='center', color=RED)
    txt(ax, -0.2, 5.25, '最高點離地 5 公尺', fs=13, ha='center', va='bottom', color=RED)
    # 車寬與距中線
    ax.annotate('', xy=(0.5, 2.35), xytext=(3.5, 2.35), arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.1))
    txt(ax, 2.0, 2.6, '3 公尺', fs=12, ha='center', va='bottom', color=BLUE)
    seg(ax, (0.5, 0), (0.5, -0.5), color=BLUE, lw=1.0)
    ax.annotate('', xy=(0, -0.4), xytext=(0.5, -0.4), arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.0, shrinkA=0, shrinkB=0))
    txt(ax, 0.7, -0.45, '0.5 公尺', fs=12, ha='left', va='center', color=BLUE)
    ax.set_xlim(-6.2, 6.2); ax.set_ylim(-1.6, 6.2)
    save(f, 31181)
