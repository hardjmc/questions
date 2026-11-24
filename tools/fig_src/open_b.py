from fig_all import *   # plt, np, PF, fig, new_ax, save, txt, dot, circle, arc, INK/RED/BLUE/GREY
from matplotlib.patches import Polygon as MPoly

FS = 14


def L(ax, *pts, color=INK, lw=1.6, ls='-'):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle='round')


def lab(ax, p, s, dx=0.0, dy=0.0, color=INK, fs=FS, pt=True):
    if pt:
        ax.plot([p[0]], [p[1]], 'o', ms=3.5, color=color)
    ax.text(p[0] + dx, p[1] + dy, s, fontsize=fs, color=color, fontproperties=PF, ha='center', va='center')


def mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def tick(ax, p, q, n=1, size=0.16, color=INK):
    """在線段 pq 中點畫 n 條等長記號。"""
    m = np.array(mid(p, q)); d = np.array(q) - np.array(p); d = d / np.linalg.norm(d)
    nrm = np.array([-d[1], d[0]])
    for k in range(n):
        c = m + d * (k - (n - 1) / 2) * size * 0.7
        a = c + nrm * size; b = c - nrm * size
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=1.4)


def rangle(ax, v, p, q, s=0.22, color=INK):
    v = np.array(v, float); u1 = np.array(p) - v; u2 = np.array(q) - v
    u1 = u1 / np.linalg.norm(u1) * s; u2 = u2 / np.linalg.norm(u2) * s
    pts = [v + u1, v + u1 + u2, v + u2]
    ax.plot([x[0] for x in pts], [x[1] for x in pts], color=color, lw=1.2)


def ang(ax, v, p, q, r=0.4, color=RED, label=None, lr=None, fs=FS):
    a0 = np.degrees(np.arctan2(p[1] - v[1], p[0] - v[0]))
    a1 = np.degrees(np.arctan2(q[1] - v[1], q[0] - v[0]))
    if (a1 - a0) % 360 > 180:
        a0, a1 = a1, a0
    if a1 < a0:
        a1 += 360
    arc(ax, v[0], v[1], r, a0, a1, color=color)
    if label:
        am = np.radians((a0 + a1) / 2); rr = lr or r + 0.3
        ax.text(v[0] + rr * np.cos(am), v[1] + rr * np.sin(am), label, fontsize=fs, color=color,
                fontproperties=PF, ha='center', va='center')


def grid(ax, x0, x1, y0, y1):
    for x in range(x0, x1 + 1):
        ax.plot([x, x], [y0, y1], color='#dddddd', lw=0.8, zorder=0)
    for y in range(y0, y1 + 1):
        ax.plot([x0, x1], [y, y], color='#dddddd', lw=0.8, zorder=0)
    ax.annotate('', xy=(x1 + 0.6, 0), xytext=(x0 - 0.3, 0), arrowprops=dict(arrowstyle='->', color=INK, lw=1.3))
    ax.annotate('', xy=(0, y1 + 0.6), xytext=(0, y0 - 0.3), arrowprops=dict(arrowstyle='->', color=INK, lw=1.3))
    txt(ax, x1 + 0.7, -0.15, 'x', fs=FS, va='center')
    txt(ax, 0.15, y1 + 0.6, 'y', fs=FS, va='center')
    txt(ax, -0.45, -0.5, 'O', fs=FS - 1, va='center')
    for x in range(x0 + 1, x1 + 1):
        if x != 0:
            txt(ax, x, -0.5, str(x), fs=11, ha='center', va='center', color=GREY)
    for y in range(y0 + 1, y1 + 1):
        if y != 0:
            txt(ax, -0.4, y, str(y), fs=11, ha='center', va='center', color=GREY)


# 39031 對頂角與平行
@fig(39031)
def f39031():
    f, ax = new_ax(5.2, 3.6)
    A, B, O = (0, 2.4), (4, 0), (2, 1.2)
    C = (3.4, 2.7); D = (2 * O[0] - C[0], 2 * O[1] - C[1])
    L(ax, A, B); L(ax, C, D); L(ax, A, C, color=BLUE); L(ax, D, B, color=BLUE)
    tick(ax, A, O); tick(ax, O, B)
    lab(ax, A, 'A', -0.25, 0.1); lab(ax, B, 'B', 0.25, -0.1); lab(ax, O, 'O', 0.05, -0.32)
    lab(ax, C, 'C', 0.22, 0.12); lab(ax, D, 'D', -0.22, -0.15)
    save(f, 39031)


# 39032 平行四邊形對角線上兩點
@fig(39032)
def f39032():
    f, ax = new_ax(5.6, 3.2)
    A, B, C, D = (1.5, 3), (0, 0), (6, 0), (7.5, 3)
    E = (B[0] + 0.25 * 7.5, 0.75); F = (B[0] + 0.75 * 7.5, 2.25)
    L(ax, A, B, C, D, A); L(ax, B, D)
    L(ax, A, E, C, F, A, color=BLUE)
    tick(ax, B, E); tick(ax, F, D)
    lab(ax, A, 'A', -0.2, 0.25); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15); lab(ax, D, 'D', 0.25, 0.2)
    lab(ax, E, 'E', 0.05, -0.35); lab(ax, F, 'F', -0.05, 0.35)
    save(f, 39032)


# 39033 等腰三角形底邊兩點
@fig(39033)
def f39033():
    f, ax = new_ax(5.0, 3.4)
    A, B, C = (3, 3.4), (0, 0), (6, 0)
    D, E = (1.6, 0), (4.4, 0)
    L(ax, A, B, C, A); L(ax, A, D, color=BLUE); L(ax, A, E, color=BLUE)
    tick(ax, A, B, 2); tick(ax, A, C, 2); tick(ax, B, D); tick(ax, E, C)
    lab(ax, A, 'A', 0, 0.3); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15)
    lab(ax, D, 'D', 0, -0.35); lab(ax, E, 'E', 0, -0.35)
    save(f, 39033)


# 39034 菱形 60°
@fig(39034)
def f39034():
    f, ax = new_ax(5.6, 3.2)
    h = 2 * np.sqrt(3)
    B, C, A, D = (0, 0), (4, 0), (2, h), (6, h)
    E = (2.8, 0); F = (4 + 0.7 * 2, 0.7 * h)
    L(ax, A, B, C, D, A)
    L(ax, A, E, color=BLUE); L(ax, A, F, color=BLUE); L(ax, E, F, color=BLUE)
    ang(ax, B, C, A, r=0.45, label='60°', lr=0.85)
    ang(ax, A, E, F, r=0.55, label='60°', lr=0.95)
    lab(ax, A, 'A', -0.1, 0.3); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.1, -0.35); lab(ax, D, 'D', 0.25, 0.2)
    lab(ax, E, 'E', 0, -0.35); lab(ax, F, 'F', 0.3, -0.05)
    save(f, 39034)


# 39035 直角三角形外心與重心
@fig(39035)
def f39035():
    f, ax = new_ax(5.4, 3.0)
    C, A, B = (0, 0), (0, 2.0), (4.8, 0)
    L(ax, A, B, C, A)
    rangle(ax, C, A, B)
    lab(ax, A, 'A', -0.25, 0.15); lab(ax, B, 'B', 0.25, -0.12); lab(ax, C, 'C', -0.25, -0.15)
    txt(ax, -0.45, 1.0, '5', fs=FS, ha='center', va='center')
    txt(ax, 2.4, -0.35, '12', fs=FS, ha='center', va='center')
    save(f, 39035)


# 39036 內心與平行線
@fig(39036)
def f39036():
    f, ax = new_ax(5.4, 4.0)
    s = 0.62
    A, B, C = (6 * s, np.sqrt(45) * s), (0, 0), (8 * s, 0)
    I = (5 * s, np.sqrt(5) * s)
    D = (2 * s, np.sqrt(5) * s); E = (22 / 3 * s, np.sqrt(5) * s)
    L(ax, A, B, C, A); L(ax, D, E, color=BLUE)
    lab(ax, A, 'A', 0, 0.3); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15)
    lab(ax, D, 'D', -0.3, 0.05); lab(ax, E, 'E', 0.3, 0.05); lab(ax, I, 'I', 0, 0.28)
    txt(ax, 1.6, 2.6, '9', fs=FS, ha='center', va='center')
    txt(ax, 4.85, 2.25, '7', fs=FS, ha='center', va='center')
    save(f, 39036)


# 39037 重心與四邊形面積
@fig(39037)
def f39037():
    f, ax = new_ax(5.4, 3.6)
    A, B, C = (1.5, 4), (0, 0), (6, 0)
    D, E = (3, 0), (3.75, 2)
    G = (2.5, 4 / 3)
    ax.add_patch(MPoly([G, D, C, E], closed=True, fc='#cfe0f7', ec='none'))
    L(ax, A, B, C, A); L(ax, A, D, color=BLUE); L(ax, B, E, color=BLUE)
    tick(ax, B, D); tick(ax, D, C); tick(ax, A, E, 2); tick(ax, E, C, 2)
    lab(ax, A, 'A', 0, 0.3); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15)
    lab(ax, D, 'D', 0, -0.35); lab(ax, E, 'E', 0.28, 0.12); lab(ax, G, 'G', -0.32, 0.12)
    save(f, 39037)


# 39038 尺規作角平分線
@fig(39038)
def f39038():
    f, ax = new_ax(5.4, 3.8)
    O = (0, 0); a = np.radians(64)
    A = (4.6, 0); B = (4.6 * np.cos(a), 4.6 * np.sin(a))
    L(ax, O, A); L(ax, O, B)
    C = (2, 0); D = (2 * np.cos(a), 2 * np.sin(a))
    arc(ax, 0, 0, 2, -8, 72, color=GREY, lw=1.3)
    t = 3.151; P = (t * np.cos(np.radians(32)), t * np.sin(np.radians(32)))
    dc = np.degrees(np.arctan2(P[1] - C[1], P[0] - C[0]))
    dd = np.degrees(np.arctan2(P[1] - D[1], P[0] - D[0]))
    arc(ax, C[0], C[1], 1.8, dc - 14, dc + 14, color=GREY, lw=1.3)
    arc(ax, D[0], D[1], 1.8, dd - 14, dd + 14, color=GREY, lw=1.3)
    R = (4.6 * np.cos(np.radians(32)), 4.6 * np.sin(np.radians(32)))
    L(ax, O, R, color=BLUE)
    lab(ax, O, 'O', -0.25, -0.15); lab(ax, A, 'A', 0.25, -0.1, pt=False); lab(ax, B, 'B', 0.15, 0.22, pt=False)
    lab(ax, C, 'C', 0.05, -0.32); lab(ax, D, 'D', -0.3, 0.05); lab(ax, P, 'P', -0.1, 0.5)
    save(f, 39038)


# 39039 坐標上的中垂線
@fig(39039)
def f39039():
    f, ax = new_ax(5.6, 3.8)
    grid(ax, -1, 7, -1, 5)
    ax.plot([-1, 7], [0, 0], color=BLUE, lw=2.4, zorder=1)
    txt(ax, 2.3, 0.35, '公路 L', color=BLUE, fs=13, va='center')
    lab(ax, (0, 4), 'A(0, 4)', 0.95, 0.25, color=RED)
    lab(ax, (6, 2), 'B(6, 2)', 0.0, 0.38, color=RED)
    save(f, 39039)


# 39040 平行四邊形角平分線
@fig(39040)
def f39040():
    f, ax = new_ax(6.0, 3.0)
    s = 0.42
    a = np.radians(65)
    B = (0, 0); A = (7 * np.cos(a) * s, 7 * np.sin(a) * s); C = (12 * s, 0); D = (A[0] + 12 * s, A[1])
    E = (7 * s, 0); F = (5 * s, 0)
    L(ax, A, B, C, D, A); L(ax, A, E, color=BLUE); L(ax, D, F, color=BLUE)
    lab(ax, A, 'A', -0.15, 0.25); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15); lab(ax, D, 'D', 0.25, 0.2)
    lab(ax, E, 'E', 0.1, -0.32); lab(ax, F, 'F', -0.1, -0.32)
    txt(ax, A[0] / 2 - 0.35, A[1] / 2, '7', fs=FS, ha='center', va='center')
    txt(ax, A[0] + 6 * s, A[1] + 0.28, '12', fs=FS, ha='center', va='center')
    save(f, 39040)


# 39041 矩形沿對角線摺疊
@fig(39041)
def f39041():
    f, ax = new_ax(5.0, 4.2)
    s = 0.5
    A, B, C, D = (0, 6 * s), (0, 0), (8 * s, 0), (8 * s, 6 * s)
    Cp = (2.24 * s, 7.68 * s); E = (1.75 * s, 6 * s)
    L(ax, D, A, B, C); L(ax, C, D, ls='--', color=GREY, lw=1.3)
    L(ax, B, D); L(ax, B, Cp, D, color=BLUE)
    lab(ax, A, 'A', -0.25, 0.1); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15); lab(ax, D, 'D', 0.28, 0.05)
    lab(ax, Cp, "C'", -0.05, 0.28); lab(ax, E, 'E', 0.12, -0.3)
    txt(ax, -0.35, 1.5, '6', fs=FS, ha='center', va='center')
    txt(ax, 2.0, -0.3, '8', fs=FS, ha='center', va='center')
    save(f, 39041)


# 39042 正方形內 45°
@fig(39042)
def f39042():
    f, ax = new_ax(4.4, 3.8)
    s = 0.6
    A, B, C, D = (0, 6 * s), (0, 0), (6 * s, 0), (6 * s, 6 * s)
    E, F = (3 * s, 0), (6 * s, 4 * s)
    L(ax, A, B, C, D, A); L(ax, A, E, color=BLUE); L(ax, A, F, color=BLUE); L(ax, E, F, color=BLUE)
    ang(ax, A, E, F, r=0.6, label='45°', lr=0.95)
    lab(ax, A, 'A', -0.25, 0.15); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15); lab(ax, D, 'D', 0.25, 0.15)
    lab(ax, E, 'E', 0, -0.32); lab(ax, F, 'F', 0.3, 0)
    save(f, 39042)


# 39043 梯子下滑
@fig(39043)
def f39043():
    f, ax = new_ax(5.4, 4.0)
    s = 0.6
    ax.plot([0, 0], [-0.05, 7 * s], color=INK, lw=2.2)
    ax.plot([-0.3, 5 * s], [0, 0], color=INK, lw=2.2)
    for i in range(8):
        y = i * 0.5
        if y < 7 * s:
            ax.plot([-0.22, 0], [y, y + 0.2], color=GREY, lw=1)
    L(ax, (0, 6 * s), (2.5 * s, 0), color=BLUE, lw=2.2)
    L(ax, (0, 5.2 * s), (3.9 * s, 0), color=BLUE, lw=2.0, ls='--')
    txt(ax, 2.0, 1.5, '6.5 m', fs=13, color=BLUE, va='center')
    txt(ax, 1.25 * s, -0.32, '2.5 m', fs=13, ha='center', va='center')
    ax.annotate('', xy=(0.25, 5.2 * s), xytext=(0.25, 6 * s), arrowprops=dict(arrowstyle='->', color=RED, lw=1.4))
    txt(ax, 0.4, 5.6 * s, '下滑 0.8 m', fs=13, color=RED, va='center')
    txt(ax, -0.55, 2.0, '牆', fs=13, ha='center', va='center')
    txt(ax, 2.5, -0.75, '地面', fs=13, ha='center', va='center')
    save(f, 39043)


# 39044 長方體表面最短路徑
@fig(39044)
def f39044():
    f, ax = new_ax(5.6, 3.0)
    s = 0.6
    ox, oy = 4 * s * 0.6, 4 * s * 0.45   # 斜投影(寬 4)
    A = (0, 0); B = (8 * s, 0); C = (B[0] + ox, oy); D = (ox, oy)
    E = (0, 2 * s); F = (B[0], 2 * s); G = (C[0], oy + 2 * s); H = (D[0], oy + 2 * s)
    L(ax, A, B, F, E, A); L(ax, F, G, H, E); L(ax, B, C, G)
    L(ax, A, D, ls='--', color=GREY, lw=1.2); L(ax, D, C, ls='--', color=GREY, lw=1.2); L(ax, D, H, ls='--', color=GREY, lw=1.2)
    lab(ax, A, 'A', -0.22, -0.15, color=RED); lab(ax, B, 'B', 0.05, -0.3); lab(ax, C, 'C', 0.25, -0.05)
    lab(ax, D, 'D', 0.2, -0.22); lab(ax, E, 'E', -0.25, 0.05); lab(ax, F, 'F', -0.25, -0.22)
    lab(ax, G, 'G', 0.22, 0.15, color=RED); lab(ax, H, 'H', -0.1, 0.25)
    txt(ax, 4 * s, -0.35, '8', fs=FS, ha='center', va='center')
    txt(ax, B[0] + ox / 2 + 0.3, oy / 2 - 0.1, '4', fs=FS, ha='center', va='center')
    txt(ax, -0.3, s, '2', fs=FS, ha='center', va='center')
    save(f, 39044)


# 39046 坐標平面上的三角形
@fig(39046)
def f39046():
    f, ax = new_ax(4.6, 4.4)
    grid(ax, -1, 7, -1, 8)
    A, B, C = (1, 1), (5, 3), (3, 7)
    L(ax, A, B, C, A, color=BLUE, lw=1.8)
    lab(ax, A, 'A(1, 1)', 0.2, -0.45, color=RED)
    lab(ax, B, 'B(5, 3)', 1.1, -0.1, color=RED)
    lab(ax, C, 'C(3, 7)', 1.1, 0.2, color=RED)
    save(f, 39046)


# 39047 坐標上的平行四邊形
@fig(39047)
def f39047():
    f, ax = new_ax(5.2, 4.0)
    grid(ax, -1, 8, -1, 6)
    A, B, C = (1, 2), (5, 1), (6, 4)
    L(ax, A, B, C, color=BLUE, lw=1.8)
    lab(ax, A, 'A(1, 2)', -0.4, 0.4, color=RED)
    lab(ax, B, 'B(5, 1)', 0.4, -0.45, color=RED)
    lab(ax, C, 'C(6, 4)', 0.9, 0.3, color=RED)
    save(f, 39047)


# 39048 兩切線
@fig(39048)
def f39048():
    f, ax = new_ax(5.2, 3.4)
    r = 1.5
    O, P = (0, 0), (-2 * r, 0)
    A = (r * np.cos(np.radians(120)), r * np.sin(np.radians(120)))
    B = (A[0], -A[1])
    circle(ax, 0, 0, r)
    L(ax, (P[0] + (A[0] - P[0]) * 1.25, P[1] + (A[1] - P[1]) * 1.25), P,
      (P[0] + (B[0] - P[0]) * 1.25, P[1] + (B[1] - P[1]) * 1.25), color=BLUE)
    L(ax, P, O)
    lab(ax, O, 'O', 0.22, -0.15); lab(ax, P, 'P', -0.28, 0); lab(ax, A, 'A', -0.05, 0.3); lab(ax, B, 'B', -0.05, -0.3)
    save(f, 39048)


# 39049 圓形水管截面
@fig(39049)
def f39049():
    f, ax = new_ax(4.0, 3.6)
    r = 1.3; y0 = -0.5
    th = np.linspace(np.arcsin(y0 / r) - 0, np.pi - np.arcsin(y0 / r), 2)
    t = np.linspace(-np.pi - np.arcsin(y0 / r), np.arcsin(y0 / r), 120)
    xs = list(r * np.cos(t)); ys = list(r * np.sin(t))
    ax.fill(xs, ys, color='#cfe0f7')
    circle(ax, 0, 0, r, lw=1.8)
    w = np.sqrt(r * r - y0 * y0)
    L(ax, (-w, y0), (w, y0), color=BLUE, lw=1.8)
    lab(ax, (0, 0), 'O', 0.2, 0.15)
    txt(ax, 0, y0 + 0.22, '水面寬 24 cm', fs=12, color=BLUE, ha='center', va='center')
    save(f, 39049)


# 39050 直徑與圓內接四邊形
@fig(39050)
def f39050():
    f, ax = new_ax(4.6, 3.4)
    r = 1.5
    def P(d):
        return (r * np.cos(np.radians(d)), r * np.sin(np.radians(d)))
    A, B, C, D = P(180), P(0), P(70), P(130)
    circle(ax, 0, 0, r)
    L(ax, A, B, C, D, A); L(ax, A, C, color=BLUE)
    ang(ax, A, B, C, r=0.5, label='35°', lr=0.82, fs=12)
    lab(ax, (0, 0), 'O', 0, -0.25)
    lab(ax, A, 'A', -0.25, 0); lab(ax, B, 'B', 0.25, 0); lab(ax, C, 'C', 0.2, 0.2); lab(ax, D, 'D', -0.18, 0.22)
    save(f, 39050)


# 39051 切線與直徑延長線
@fig(39051)
def f39051():
    f, ax = new_ax(5.4, 3.2)
    r = 1.5
    O, P, B, A = (0, 0), (-2.5, 0), (-1.5, 0), (1.5, 0)
    C = (-0.9, 1.2)
    circle(ax, 0, 0, r)
    L(ax, P, A); L(ax, P, (P[0] + (C[0] - P[0]) * 1.35, P[1] + (C[1] - P[1]) * 1.35), color=BLUE)
    L(ax, C, B); L(ax, C, A)
    lab(ax, O, 'O', 0, -0.28); lab(ax, P, 'P', -0.25, -0.12); lab(ax, B, 'B', 0.18, -0.25)
    lab(ax, A, 'A', 0.25, -0.12); lab(ax, C, 'C', -0.1, 0.3)
    save(f, 39051)


# 39052 圓心角與圓周角
@fig(39052)
def f39052():
    f, ax = new_ax(4.2, 3.8)
    r = 1.5
    def P(d):
        return (r * np.cos(np.radians(d)), r * np.sin(np.radians(d)))
    A, B, C, D = P(205), P(335), P(100), P(270)
    O = (0, 0)
    circle(ax, 0, 0, r)
    L(ax, A, B); L(ax, O, A); L(ax, O, B)
    L(ax, A, C, B, color=BLUE); L(ax, A, D, B, color=BLUE)
    ang(ax, A, O, B, r=0.45, label='25°', lr=0.72, fs=12)
    lab(ax, O, 'O', 0, 0.25); lab(ax, A, 'A', -0.25, -0.05); lab(ax, B, 'B', 0.25, -0.05)
    lab(ax, C, 'C', 0, 0.25); lab(ax, D, 'D', 0, -0.25)
    save(f, 39052)


# 39053 同心圓
@fig(39053)
def f39053():
    f, ax = new_ax(4.0, 3.8)
    R, r = 1.6, 1.0
    circle(ax, 0, 0, R); circle(ax, 0, 0, r)
    w = np.sqrt(R * R - r * r)
    A, B, P = (-w, -r), (w, -r), (0, -r)
    L(ax, A, B, color=BLUE, lw=1.8)
    lab(ax, (0, 0), 'O', 0, 0.22); lab(ax, A, 'A', -0.22, -0.1); lab(ax, B, 'B', 0.22, -0.1); lab(ax, P, 'P', 0, -0.25)
    txt(ax, 0, -1.95, 'AB = 16', fs=13, color=RED, ha='center', va='center')
    save(f, 39053)


# 39054 路燈與人影
@fig(39054)
def f39054():
    f, ax = new_ax(5.6, 3.4)
    s = 0.6
    ax.plot([-0.3, 7.6 * s], [0, 0], color=INK, lw=2)
    ax.plot([0, 0], [0, 4.8 * s], color=INK, lw=2.4)
    ax.plot([0], [4.8 * s], 'o', ms=10, color='#f2c14e', zorder=5)
    Lp = (0, 4.8 * s)
    ax.plot([4 * s, 4 * s], [0, 1.6 * s], color=BLUE, lw=3)
    ax.plot([4 * s], [1.6 * s + 0.12], 'o', ms=6, color=BLUE)
    L(ax, Lp, (6 * s, 0), color=GREY, lw=1.2, ls='--')
    ax.plot([4 * s, 6 * s], [0, 0], color=RED, lw=3.2)
    txt(ax, 2 * s, -0.3, '4 m', fs=13, ha='center', va='center')
    txt(ax, 5 * s, -0.3, '影子 2 m', fs=13, color=RED, ha='center', va='center')
    txt(ax, 4 * s - 0.45, 0.8 * s, '1.6 m', fs=12, color=BLUE, ha='center', va='center')
    txt(ax, -0.45, 2.4 * s, '路燈', fs=13, ha='center', va='center')
    save(f, 39054)


# 39055 平行線截比例
@fig(39055)
def f39055():
    f, ax = new_ax(5.0, 3.6)
    A, B, C = (2.0, 4.0), (0, 0), (6.0, 0)
    k = 3 / 8
    D = (A[0] + (B[0] - A[0]) * k, A[1] + (B[1] - A[1]) * k)
    E = (A[0] + (C[0] - A[0]) * k, A[1] + (C[1] - A[1]) * k)
    L(ax, A, B, C, A); L(ax, D, E, color=BLUE)
    lab(ax, A, 'A', 0, 0.3); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15)
    lab(ax, D, 'D', -0.3, 0.05); lab(ax, E, 'E', 0.3, 0.05)
    txt(ax, (A[0] + D[0]) / 2 - 0.3, (A[1] + D[1]) / 2 + 0.05, '3', fs=FS, ha='center', va='center')
    txt(ax, (D[0] + B[0]) / 2 - 0.3, (D[1] + B[1]) / 2 + 0.05, '5', fs=FS, ha='center', va='center')
    txt(ax, (D[0] + E[0]) / 2, D[1] + 0.25, '4.5', fs=FS, color=BLUE, ha='center', va='center')
    save(f, 39055)


# 39056 直角三角形斜邊上的高
@fig(39056)
def f39056():
    f, ax = new_ax(5.4, 3.0)
    s = 0.62
    A, B, D, C = (0, 0), (8 * s, 0), (2 * s, 0), (2 * s, 2 * np.sqrt(3) * s)
    L(ax, A, B, C, A); L(ax, C, D, color=BLUE)
    rangle(ax, C, A, B); rangle(ax, D, B, C)
    lab(ax, A, 'A', -0.25, -0.12); lab(ax, B, 'B', 0.25, -0.12); lab(ax, C, 'C', 0, 0.3); lab(ax, D, 'D', 0, -0.3)
    txt(ax, s, -0.3, '2', fs=FS, ha='center', va='center')
    txt(ax, 5 * s, -0.3, '6', fs=FS, ha='center', va='center')
    save(f, 39056)


# 39057 三角形內接正方形
@fig(39057)
def f39057():
    f, ax = new_ax(5.4, 3.8)
    s = 0.42
    B, C, A, H = (0, 0), (12 * s, 0), (4 * s, 8 * s), (4 * s, 0)
    D, E, F, G = (2.4 * s, 4.8 * s), (7.2 * s, 4.8 * s), (7.2 * s, 0), (2.4 * s, 0)
    ax.add_patch(MPoly([D, E, F, G], closed=True, fc='#cfe0f7', ec=BLUE, lw=1.6))
    L(ax, A, B, C, A); L(ax, A, H, ls='--', color=GREY, lw=1.3)
    rangle(ax, H, C, A, s=0.18)
    lab(ax, A, 'A', 0, 0.3); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15)
    lab(ax, D, 'D', -0.28, 0.1); lab(ax, E, 'E', 0.28, 0.1); lab(ax, F, 'F', 0.12, -0.3); lab(ax, G, 'G', -0.12, -0.3)
    lab(ax, H, 'H', 0, -0.3)
    txt(ax, 6 * s, -0.75, 'BC = 12,AH = 8', fs=13, color=RED, ha='center', va='center')
    save(f, 39057)


# 39058 平行四邊形中的相似
@fig(39058)
def f39058():
    f, ax = new_ax(5.6, 3.0)
    A, B, C, D = (1, 3), (0, 0), (6, 0), (7, 3)
    E = (3, 3); F = (2.25, 2.25)
    L(ax, A, B, C, D, A); L(ax, A, C, color=BLUE); L(ax, B, E, color=BLUE)
    lab(ax, A, 'A', -0.2, 0.25); lab(ax, B, 'B', -0.25, -0.15); lab(ax, C, 'C', 0.25, -0.15); lab(ax, D, 'D', 0.25, 0.2)
    lab(ax, E, 'E', 0, 0.3); lab(ax, F, 'F', -0.05, -0.38)
    save(f, 39058)


# 39059 圓錐展開圖
@fig(39059)
def f39059():
    f, ax = new_ax(5.6, 3.4)
    R = 2.4
    O = (0, 0)
    a0, a1 = 30, 150
    th = np.linspace(np.radians(a0), np.radians(a1), 100)
    ax.fill(np.r_[0, R * np.cos(th)], np.r_[0, R * np.sin(th)], color='#cfe0f7')
    ax.plot(R * np.cos(th), R * np.sin(th), color=INK, lw=1.6)
    L(ax, O, (R * np.cos(np.radians(a0)), R * np.sin(np.radians(a0))))
    L(ax, O, (R * np.cos(np.radians(a1)), R * np.sin(np.radians(a1))))
    arc(ax, 0, 0, 0.4, a0, a1)
    txt(ax, 0, 0.62, '120°', fs=13, color=RED, ha='center', va='center')
    txt(ax, 1.25, 0.35, '12', fs=FS, ha='center', va='center')
    circle(ax, 3.2, 1.0, 0.8)
    txt(ax, 3.2, -0.15, '底面', fs=13, ha='center', va='center')
    txt(ax, 0, -0.35, '側面', fs=13, ha='center', va='center')
    save(f, 39059)


# 39060 骰子展開圖
@fig(39060)
def f39060():
    f, ax = new_ax(5.0, 3.6)
    cells = {(1, 2): '3', (0, 1): 'x', (1, 1): '2', (2, 1): '6', (3, 1): 'y', (1, 0): 'z'}
    for (c, r), s in cells.items():
        ax.add_patch(Rectangle((c, r), 1, 1, fill=False, ec=INK, lw=1.6))
        col = RED if s in 'xyz' else INK
        txt(ax, c + 0.5, r + 0.5, s, fs=18, color=col, ha='center', va='center')
    ax.set_xlim(-0.2, 4.2); ax.set_ylim(-0.2, 3.2)
    save(f, 39060)
