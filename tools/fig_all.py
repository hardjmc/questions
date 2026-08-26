#!/usr/bin/env python3
"""會考倒數題庫附圖總產生器。用法:python3 fig_all.py [id ...](無參數=全部)"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyArrow, Rectangle, Circle as MCircle
import numpy as np
import os, sys

PF = FontProperties(fname='/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc')
OUT = os.path.join(os.path.dirname(__file__), 'figs')
os.makedirs(OUT, exist_ok=True)
INK, RED, BLUE, GREY = '#333333', '#d0342c', '#2a5fb4', '#999999'
FIGS = {}

def fig(qid):
    def deco(fn):
        FIGS[qid] = fn
        return fn
    return deco

def new_ax(w=6.0, h=4.2, equal=True):
    f, ax = plt.subplots(figsize=(w, h), dpi=200)
    if equal:
        ax.set_aspect('equal')
    ax.axis('off')
    return f, ax

def save(f, qid):
    f.savefig(os.path.join(OUT, f'q{qid}.png'), bbox_inches='tight', pad_inches=0.15, facecolor='white')
    plt.close(f)
    print('saved', qid)

def dot(ax, x, y, label, dx=0.12, dy=0.12, color=INK, fs=13):
    ax.plot([x], [y], 'o', ms=4, color=color)
    ax.text(x + dx, y + dy, label, fontsize=fs, color=color, fontproperties=PF)

def txt(ax, x, y, s, color=INK, fs=13, **kw):
    ax.text(x, y, s, fontsize=fs, color=color, fontproperties=PF, **kw)

def circle(ax, cx, cy, r, color=INK, lw=1.4):
    th = np.linspace(0, 2 * np.pi, 240)
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color=color, lw=lw)

def arc(ax, cx, cy, r, a0, a1, color=RED, lw=1.4):
    th = np.linspace(np.radians(a0), np.radians(a1), 60)
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color=color, lw=lw)

# ── 三平行線截線(30212 / 30428 / 30718 共用版型)──────────
def parallel_cut(qid, gap_top, gap_bot, left_note, right_top, right_bot):
    f, ax = new_ax()
    total = gap_top + gap_bot
    ys = [total, gap_bot, 0.0]
    for y, name in zip(ys, ['l₁', 'l₂', 'l₃']):
        ax.plot([-0.6, 6.0], [y, y], color=INK, lw=1.4)
        ax.annotate('', xy=(5.7, y), xytext=(5.35, y), arrowprops=dict(arrowstyle='->', color=INK, lw=1.2))
        txt(ax, 6.1, y, name, va='center', fs=14)
    for x0, slope, labels, side in [(0.6, 0.35, 'ABC', 'left'), (3.6, 0.55, 'DEF', 'right')]:
        pts = [(x0 + slope * (total - y), y) for y in ys]
        ax.plot([pts[0][0] - 0.35 * slope * total / 3, pts[2][0] + 0.35 * slope * total / 3],
                [total + 0.35, -0.35], color=BLUE, lw=1.4)
        for (x, y), lab in zip(pts, labels):
            dot(ax, x, y, lab, dx=(-0.42 if side == 'left' else 0.16), dy=0.1)
    txt(ax, -0.55, (gap_bot + total) / 2, left_note, color=RED, fs=13)
    txt(ax, 5.0, gap_bot + gap_top * 0.55, right_top, color=RED, fs=13)
    txt(ax, 5.5, gap_bot * 0.45, right_bot, color=RED, fs=14)
    save(f, qid)

@fig(30212)
def f30212():
    parallel_cut(30212, 1.2, 1.8, 'AB:BC = 2:3', 'DE = 4', 'EF = ?')

@fig(30428)
def f30428():
    parallel_cut(30428, 1.14, 1.9, 'AB = 3\nBC = 5', 'DE = 6', 'EF = ?')

@fig(30718)
def f30718():
    parallel_cut(30718, 1.2, 1.8, '2 : 3', '', '2 : 3')

# ── 30218 圓心角與圓周角 ──────────────────────────────────
@fig(30218)
def f30218():
    f, ax = new_ax(5.2, 5.2)
    circle(ax, 0, 0, 1)
    A = (np.cos(np.radians(130)), np.sin(np.radians(130)))
    B = (np.cos(np.radians(50)), np.sin(np.radians(50)))
    P = (0, -1)
    for X in (A, B):
        ax.plot([0, X[0]], [0, X[1]], color=INK, lw=1.3)
        ax.plot([P[0], X[0]], [P[1], X[1]], color=BLUE, lw=1.3)
    arc(ax, 0, 0, 0.25, 50, 130)
    txt(ax, -0.13, 0.33, '80°', color=RED, fs=14)
    arc(ax, P[0], P[1], 0.3, 63, 117)
    txt(ax, P[0] - 0.06, P[1] + 0.38, '?', color=RED, fs=15)
    th = np.linspace(np.radians(50), np.radians(130), 60)
    ax.plot(np.cos(th), np.sin(th), color=RED, lw=3)
    dot(ax, 0, 0, 'O', dx=0.06, dy=-0.2)
    dot(ax, *A, 'A', dx=-0.2, dy=0.06)
    dot(ax, *B, 'B', dx=0.08, dy=0.06)
    dot(ax, *P, 'P', dx=-0.04, dy=-0.26)
    save(f, 30218)

# ── 30225 切線與過圓心割線 ────────────────────────────────
@fig(30225)
def f30225():
    f, ax = new_ax(6.4, 4.0)
    r, po = 2.1, 3.5                     # 6:10 縮放
    circle(ax, 0, 0, r)
    P = (-po, 0)
    A = (r * -0.6, r * 0.8)              # OA⊥PA
    Bfar = (r, 0)
    ax.plot([P[0], Bfar[0]], [0, 0], color=INK, lw=1.3)          # 割線 P–O–B
    ax.plot([P[0], A[0]], [P[1], A[1]], color=BLUE, lw=1.5)      # 切線 PA
    ax.plot([0, A[0]], [0, A[1]], color=INK, lw=1.2)             # 半徑 OA
    # 直角記號(於 A,OA 與 PA 垂直)
    u = np.array(A) / np.linalg.norm(A)
    v = np.array(A) - np.array(P); v = v / np.linalg.norm(v)
    s = 0.22
    corner = np.array(A) - u * s
    ax.plot([corner[0], corner[0] - v[0] * s], [corner[1], corner[1] - v[1] * s], color=INK, lw=1)
    ax.plot([corner[0] - v[0] * s + u[0] * s * 0, A[0] - v[0] * s], [corner[1] - v[1] * s, A[1] - v[1] * s], color=INK, lw=1)
    dot(ax, *P, 'P', dx=-0.3, dy=-0.05)
    dot(ax, 0, 0, 'O', dx=0.02, dy=-0.3)
    dot(ax, *A, 'A', dx=-0.05, dy=0.14)
    dot(ax, *Bfar, 'B', dx=0.1, dy=-0.28)
    txt(ax, -po / 2 - 0.3, -0.35, 'PO = 10', color=RED, fs=13)
    txt(ax, A[0] / 2 - 0.28, A[1] / 2 - 0.08, '6', color=INK, fs=13)   # 貼在半徑 OA 中點旁
    txt(ax, -po * 0.72, r * 0.62, 'PA = ?', color=RED, fs=13)
    save(f, 30225)

# ── 30230 平行線同位角 ────────────────────────────────────
@fig(30230)
def f30230():
    f, ax = new_ax(5.8, 4.0)
    for y, name in [(2.2, 'L1'), (0, 'L2')]:
        ax.plot([-0.5, 5.4], [y, y], color=INK, lw=1.4)
        ax.annotate('', xy=(5.15, y), xytext=(4.8, y), arrowprops=dict(arrowstyle='->', color=INK, lw=1.2))
        txt(ax, 5.5, y, name, va='center', fs=13)
    # 截線
    def x_at(y):
        return 1.2 + 0.8 * y
    ax.plot([x_at(-0.7), x_at(3.0)], [-0.7, 3.0], color=BLUE, lw=1.4)
    for y, lab in [(2.2, '∠α'), (0, '∠β')]:
        x = x_at(y)
        a0 = 0
        a1 = np.degrees(np.arctan2(1, 0.8))
        arc(ax, x, y, 0.45, a0, a1)
        txt(ax, x + 0.55, y + 0.28, lab, color=RED, fs=14)
    save(f, 30230)

# ── 30232 對頂角與鄰角 ────────────────────────────────────
@fig(30232)
def f30232():
    f, ax = new_ax(5.0, 3.8)
    ax.plot([-2.4, 2.4], [-1.1, 1.1], color=INK, lw=1.4)
    ax.plot([-2.4, 2.4], [1.1, -1.1], color=INK, lw=1.4)
    ang = np.degrees(np.arctan2(1.1, 2.4))
    arc(ax, 0, 0, 0.7, -ang, ang)
    txt(ax, 0.82, -0.1, '65°', color=RED, fs=14)
    arc(ax, 0, 0, 0.55, ang, 180 - ang, color=BLUE)
    txt(ax, -0.16, 0.72, '?', color=BLUE, fs=15)
    save(f, 30232)

# ── 30367 直角三角形縮小 1/2 ──────────────────────────────
@fig(30367)
def f30367():
    f, ax = new_ax(6.6, 3.6)
    def tri(x0, sa, sb, la, lb, lc, color=INK):
        ax.plot([x0, x0 + sb, x0, x0], [0, 0, sa, 0], color=color, lw=1.5)
        ax.plot([x0 + sb, x0], [0, sa], color=color, lw=1.5)
        ax.add_patch(Rectangle((x0, 0), 0.18, 0.18, fill=False, ec=color, lw=1))
        txt(ax, x0 - 0.35, sa / 2, la, fs=13)
        txt(ax, x0 + sb / 2 - 0.1, -0.32, lb, fs=13)
        txt(ax, x0 + sb / 2 + 0.18, sa / 2 + 0.14, lc, fs=13)
    tri(0, 2.4, 3.2, 'a', 'b', 'c')
    ax.annotate('', xy=(4.7, 1.1), xytext=(3.9, 1.1), arrowprops=dict(arrowstyle='->', color=GREY, lw=1.4))
    txt(ax, 3.95, 1.35, '×1/2', color=GREY, fs=12)
    tri(5.2, 1.2, 1.6, 'a/2', 'b/2', 'c/2', color=BLUE)
    txt(ax, 5.35, -0.85, '面積 = 原來的?倍', color=RED, fs=13)
    save(f, 30367)

# ── 30414 雙峰分布 ────────────────────────────────────────
@fig(30414)
def f30414():
    f, ax = plt.subplots(figsize=(6.2, 3.8), dpi=200)
    x = np.linspace(0, 100, 300)
    y = 12 * np.exp(-((x - 38) ** 2) / 120) + 10 * np.exp(-((x - 78) ** 2) / 100) + 0.5
    ax.plot(x, y, color=BLUE, lw=2)
    ax.fill_between(x, y, color=BLUE, alpha=0.12)
    for px in (38, 78):
        ax.axvline(px, color=GREY, ls=':', lw=1)
    txt(ax, 33, 13.1, '峰 1', color=RED, fs=12)
    txt(ax, 73, 11.1, '峰 2', color=RED, fs=12)
    ax.set_xlabel('成績(分)', fontproperties=PF, fontsize=11)
    ax.set_ylabel('人數', fontproperties=PF, fontsize=11)
    ax.set_yticks([])
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    save(f, 30414)

# ── 30425 竹竿與樹影 ──────────────────────────────────────
@fig(30425)
def f30425():
    f, ax = new_ax(6.4, 4.6)
    ax.plot([-0.3, 8.6], [0, 0], color=INK, lw=1.6)
    px = 1.6
    ax.plot([px, px], [0, 1.8], color=INK, lw=3)
    ax.plot([px, px - 1.2], [0, 0], color=RED, lw=3)
    ax.plot([px - 1.2, px], [0, 1.8], color=GREY, lw=1, ls='--')
    txt(ax, px + 0.1, 0.85, '180', fs=12)
    txt(ax, px - 1.25, -0.34, '影長 120', color=RED, fs=12)
    tx, th = 7.6, 3.375
    sh = 2.25
    ax.plot([tx, tx], [0, th], color='#2e7d32', lw=4)
    ax.add_patch(MCircle((tx, th), 0.4, color='#66bb6a'))
    ax.plot([tx, tx - sh], [0, 0], color=RED, lw=3)
    ax.plot([tx - sh, tx], [0, th], color=GREY, lw=1, ls='--')
    txt(ax, tx + 0.16, th * 0.5, '高 ?', color=RED, fs=13)
    txt(ax, tx - sh + 0.15, -0.34, '影長 500', color=RED, fs=12)
    txt(ax, 0.1, 3.6, '同一時刻', color=GREY, fs=11)
    ax.set_xlim(-0.5, 9.2)
    ax.set_ylim(-0.7, 4.3)
    save(f, 30425)

# ── 30431 切線與直角三角形 ────────────────────────────────
@fig(30431)
def f30431():
    f, ax = new_ax(6.4, 4.2)
    r = 1.5
    circle(ax, 0, r, r)                      # 圓心在 (0, r),切線為 x 軸
    ax.plot([-2.2, 5.0], [0, 0], color=BLUE, lw=1.5)
    txt(ax, 5.1, 0, 'L', va='center', fs=13)
    P = (0, 0)
    Q = (3.9, 0)                             # 13:5 → PQ=12 → 縮放 0.3 → 3.6;取 3.9 視覺
    O = (0, r)
    ax.plot([O[0], P[0]], [O[1], P[1]], color=INK, lw=1.3)
    ax.plot([O[0], Q[0]], [O[1], Q[1]], color=INK, lw=1.3)
    ax.add_patch(Rectangle((0, 0), 0.2, 0.2, fill=False, ec=INK, lw=1))
    dot(ax, *O, 'O', dx=-0.28, dy=0.05)
    dot(ax, *P, 'P', dx=-0.1, dy=-0.32)
    dot(ax, *Q, 'Q', dx=0.05, dy=-0.32)
    txt(ax, -0.55, r * 0.45, 'OP = 5', color=INK, fs=12)
    txt(ax, Q[0] * 0.52, r * 0.62, 'OQ = 13', color=INK, fs=12)
    txt(ax, Q[0] * 0.45, -0.38, 'PQ = ?', color=RED, fs=13)
    save(f, 30431)

# ── 30436 切線平行弦 ─────────────────────────────────────
@fig(30436)
def f30436():
    f, ax = new_ax(5.4, 5.0)
    circle(ax, 0, 0, 1)
    T = (0, -1)
    A = (np.cos(np.radians(220)), np.sin(np.radians(220)))
    B = (np.cos(np.radians(320)), np.sin(np.radians(320)))
    ax.plot([-1.5, 1.5], [-1, -1], color=BLUE, lw=1.5)           # 切線 L
    txt(ax, 1.6, -1, 'L', va='center', fs=13)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=INK, lw=1.4)       # 弦 AB
    for X in (A, T, B):
        ax.plot([0, X[0]], [0, X[1]], color=GREY, lw=1, ls='--')
    th = np.linspace(np.radians(220), np.radians(270), 40)
    ax.plot(np.cos(th), np.sin(th), color=RED, lw=3)
    th = np.linspace(np.radians(270), np.radians(320), 40)
    ax.plot(np.cos(th), np.sin(th), color='#e59d00', lw=3)
    txt(ax, -0.98, -0.98, '弧AT 50°', color=RED, fs=12)
    txt(ax, 0.5, -0.98, '弧TB ?', color='#e59d00', fs=12)
    dot(ax, 0, 0, 'O', dx=0.06, dy=0.08)
    dot(ax, *A, 'A', dx=-0.26, dy=0.0)
    dot(ax, *B, 'B', dx=0.1, dy=0.0)
    dot(ax, *T, 'T', dx=-0.05, dy=-0.3)
    txt(ax, -0.35, 0.35, 'AB ∥ L', color=GREY, fs=11)
    save(f, 30436)

# ── 30442 兩圓外切 ───────────────────────────────────────
@fig(30442)
def f30442():
    f, ax = new_ax(6.2, 3.6)
    R, r = 2.0, 0.75
    O1, O2 = (0, 0), (R + r, 0)
    circle(ax, *O1, R)
    circle(ax, *O2, r)
    a1 = np.radians(135)
    ax.plot([0, R * np.cos(a1)], [0, R * np.sin(a1)], color=BLUE, lw=1.3)
    txt(ax, 0.45 * R * np.cos(a1) - 0.3, 0.5 * R * np.sin(a1) + 0.05, '8', color=BLUE, fs=14)
    a2 = np.radians(110)
    ax.plot([O2[0], O2[0] + r * np.cos(a2)], [0, r * np.sin(a2)], color=BLUE, lw=1.3)
    txt(ax, O2[0] + r * np.cos(a2) - 0.05, r * np.sin(a2) + 0.12, '3', color=BLUE, fs=14)
    ax.plot([0, O2[0]], [0, 0], color=RED, lw=1.6, ls='--')
    txt(ax, O2[0] / 2 - 0.42, -0.4, '圓心距 ?', color=RED, fs=13)
    dot(ax, *O1, 'O₁', dx=-0.12, dy=0.12)
    dot(ax, *O2, 'O₂', dx=-0.06, dy=0.14)
    save(f, 30442)

# ── 30450 俯角 45° ───────────────────────────────────────
@fig(30450)
def f30450():
    f, ax = new_ax(6.0, 4.2)
    ax.plot([-0.4, 5.4], [0, 0], color=INK, lw=1.6)              # 地面
    ax.plot([0, 0], [0, 3.0], color=INK, lw=3.5)                 # 塔
    top = (0, 3.0)
    Pt = (3.0, 0)
    ax.plot([top[0], Pt[0]], [top[1], Pt[1]], color=BLUE, lw=1.4)
    ax.plot([0, 2.0], [3.0, 3.0], color=GREY, lw=1.1, ls='--')   # 水平線
    arc(ax, 0, 3.0, 0.75, -45, 0)
    txt(ax, 0.85, 2.6, '俯角 45°', color=RED, fs=12)
    txt(ax, -0.75, 1.45, '塔高 20', fs=12)
    txt(ax, 1.25, -0.38, '水平距離 ?', color=RED, fs=13)
    dot(ax, *Pt, '', dx=0, dy=0)
    save(f, 30450)

# ── 30602 大正方形挖小正方形 ─────────────────────────────
@fig(30602)
def f30602():
    f, ax = new_ax(4.8, 4.4)
    a, b = 3.2, 1.3
    ax.add_patch(Rectangle((0, 0), a, a, facecolor='#dfe8f7', edgecolor=INK, lw=1.5))
    ax.add_patch(Rectangle((a - b, a - b), b, b, facecolor='white', edgecolor=INK, lw=1.5))
    txt(ax, a / 2 - 0.1, -0.35, 'a', fs=14)
    txt(ax, -0.32, a / 2 - 0.05, 'a', fs=14)
    txt(ax, a - b / 2 - 0.1, a + 0.14, 'b', fs=14)
    txt(ax, a + 0.12, a - b / 2 - 0.06, 'b', fs=14)
    txt(ax, 0.35, a * 0.42, '剩餘面積 = ?', color=RED, fs=13)
    ax.set_xlim(-0.7, a + 0.8)
    ax.set_ylim(-0.7, a + 0.6)
    save(f, 30602)

# ── 30408 折線圖 ─────────────────────────────────────────
@fig(30408)
def f30408():
    f, ax = plt.subplots(figsize=(6.4, 4.0), dpi=200)
    days = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']
    known = [170, 185, 175, 190, 180]
    ax.plot(range(5), known, '-o', color=BLUE, lw=2, ms=5)
    for i, v in enumerate(known):
        ax.annotate(str(v), (i, v), textcoords='offset points', xytext=(0, 8), ha='center',
                    fontsize=10, color=INK, fontproperties=PF)
    ax.plot([5, 6], [250, 250], 'o', mfc='white', mec=RED, mew=1.6, ms=8)
    for i in (5, 6):
        ax.annotate('?', (i, 250), textcoords='offset points', xytext=(0, 10), ha='center',
                    fontsize=13, color=RED, fontproperties=PF)
    ax.plot([4, 5], [180, 250], ls=':', color='#aaaaaa', lw=1.4)
    ax.plot([5, 6], [250, 250], ls=':', color='#aaaaaa', lw=1.4)
    ax.set_xticks(range(7))
    ax.set_xticklabels(days, fontproperties=PF, fontsize=11)
    ax.set_ylabel('來客數(人)', fontproperties=PF, fontsize=11)
    ax.set_ylim(140, 290)
    ax.grid(axis='y', color='#eeeeee')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    save(f, 30408)


# ══ 批次 B:圓的性質 + 等高線 ══════════════════════════════

@fig(30722)
def f30722():
    f, ax = new_ax(5.2, 5.0)
    circle(ax, 0, 0, 1)
    d, L = 0.6, 0.8
    # 弦 AB(上方水平)
    ax.plot([-L, L], [d, d], color=INK, lw=1.5)
    ax.plot([0, 0], [0, d], color=RED, lw=1.2, ls='--')
    txt(ax, 0.05, d * 0.35, '6', color=RED, fs=13)
    dot(ax, -L, d, 'A', dx=-0.22, dy=0.05)
    dot(ax, L, d, 'B', dx=0.08, dy=0.05)
    # 弦 CD(左下,與 AB 等長)
    phi = np.radians(215)
    n = np.array([np.cos(phi), np.sin(phi)])
    t = np.array([-n[1], n[0]])
    C = d * n + L * t
    D = d * n - L * t
    ax.plot([C[0], D[0]], [C[1], D[1]], color=INK, lw=1.5)
    ax.plot([0, d * n[0]], [0, d * n[1]], color=BLUE, lw=1.2, ls='--')
    txt(ax, d * n[0] * 0.75 - 0.22, d * n[1] * 0.75 - 0.1, '?', color=BLUE, fs=15)
    dot(ax, C[0], C[1], 'C', dx=-0.1, dy=0.1)
    dot(ax, D[0], D[1], 'D', dx=0.02, dy=-0.28)
    dot(ax, 0, 0, 'O', dx=0.08, dy=0.05)
    txt(ax, -1.05, 1.12, 'AB = CD,半徑 10', color=GREY, fs=12)
    save(f, 30722)

@fig(30733)
def f30733():
    f, ax = new_ax(5.2, 5.0)
    circle(ax, 0, 0, 1)
    A = np.array([np.cos(np.radians(155)), np.sin(np.radians(155))])
    B = np.array([np.cos(np.radians(-25)), np.sin(np.radians(-25))])
    P = A + (B - A) * 3 / 11
    ax.plot([A[0], B[0]], [A[1], B[1]], color=INK, lw=1.4)
    # 過 P 的另一弦 CD:方向 dir,與圓交點
    dirv = np.array([np.cos(np.radians(75)), np.sin(np.radians(75))])
    b = 2 * P.dot(dirv)
    c = P.dot(P) - 1
    t1 = (-b + np.sqrt(b * b - 4 * c)) / 2
    t2 = (-b - np.sqrt(b * b - 4 * c)) / 2
    Cpt = P + dirv * t2       # 短側 → C(PC=4)
    Dpt = P + dirv * t1       # 長側 → D(PD=?)
    ax.plot([Cpt[0], Dpt[0]], [Cpt[1], Dpt[1]], color=BLUE, lw=1.4)
    dot(ax, *A, 'A', dx=-0.24, dy=0.05)
    dot(ax, *B, 'B', dx=0.08, dy=-0.1)
    dot(ax, *Cpt, 'C', dx=0.0, dy=-0.28)
    dot(ax, *Dpt, 'D', dx=-0.02, dy=0.1)
    dot(ax, *P, 'P', dx=0.1, dy=-0.05)
    txt(ax, (A[0] + P[0]) / 2 - 0.12, (A[1] + P[1]) / 2 + 0.14, 'PA=3', color=RED, fs=12)
    txt(ax, (B[0] + P[0]) / 2, (B[1] + P[1]) / 2 + 0.1, 'PB=8', color=RED, fs=12)
    txt(ax, (Cpt[0] + P[0]) / 2 + 0.08, (Cpt[1] + P[1]) / 2, 'PC=4', color=BLUE, fs=12)
    txt(ax, (Dpt[0] + P[0]) / 2 + 0.08, (Dpt[1] + P[1]) / 2, 'PD=?', color=BLUE, fs=12)
    save(f, 30733)

@fig(30736)
def f30736():
    f, ax = new_ax(5.4, 5.0)
    circle(ax, 0, 0, 1)
    A, B = (-1, 0), (1, 0)
    th = np.arccos(-0.28)
    C = (np.cos(th), np.sin(th))
    D = ((C[0] + 1) / 2, C[1] / 2)
    E = np.array(D) / np.linalg.norm(D)
    ax.plot([A[0], B[0]], [0, 0], color=INK, lw=1.4)
    ax.plot([B[0], C[0]], [B[1], C[1]], color=BLUE, lw=1.5)
    ax.plot([0, E[0]], [0, E[1]], color=RED, lw=1.4)
    dot(ax, *A, 'A', dx=-0.24, dy=-0.05)
    dot(ax, *B, 'B', dx=0.1, dy=-0.05)
    dot(ax, *C, 'C', dx=-0.12, dy=0.12)
    dot(ax, *D, 'D', dx=0.1, dy=-0.06)
    dot(ax, *E, 'E', dx=0.06, dy=0.1)
    dot(ax, 0, 0, 'O', dx=-0.22, dy=-0.05)
    txt(ax, (B[0] + C[0]) / 2 + 0.1, C[1] / 2 + 0.12, 'BC = 8', color=BLUE, fs=12)
    txt(ax, E[0] * 0.3 - 0.35, E[1] * 0.3 + 0.02, 'OD = ?', color=RED, fs=12)
    txt(ax, -1.02, 1.1, '半徑 5,D 為 BC 中點', color=GREY, fs=12)
    save(f, 30736)

@fig(30739)
def f30739():
    f, ax = new_ax(5.8, 4.0)
    for y, name in [(2.2, 'L₁'), (0, 'L₂')]:
        ax.plot([-0.5, 5.4], [y, y], color=INK, lw=1.4)
        ax.annotate('', xy=(5.15, y), xytext=(4.8, y), arrowprops=dict(arrowstyle='->', color=INK, lw=1.2))
        txt(ax, 5.5, y, name, va='center', fs=13)
    def x_at(y):
        return 1.2 + 0.8 * y
    ax.plot([x_at(-0.7), x_at(3.0)], [-0.7, 3.0], color=BLUE, lw=1.4)
    slope_deg = np.degrees(np.arctan2(1, 0.8))
    arc(ax, x_at(2.2), 2.2, 0.5, 180 + slope_deg, 360)        # L₁ 下方右側
    txt(ax, x_at(2.2) + 0.6, 1.55, '∠1', color=RED, fs=14)
    arc(ax, x_at(0), 0, 0.5, 0, slope_deg, color=BLUE)
    txt(ax, x_at(0) + 0.6, 0.32, '∠2', color=BLUE, fs=14)
    txt(ax, 0.0, 1.0, '∠1 + ∠2 = ?', color=RED, fs=13)
    save(f, 30739)

@fig(30742)
def f30742():
    f, ax = new_ax(6.2, 3.6)
    R, r = 1.75, 0.75            # 7:3
    O2 = (R + r, 0)
    circle(ax, 0, 0, R)
    circle(ax, *O2, r)
    a1 = np.radians(135)
    ax.plot([0, R * np.cos(a1)], [0, R * np.sin(a1)], color=BLUE, lw=1.3)
    txt(ax, 0.45 * R * np.cos(a1) - 0.3, 0.5 * R * np.sin(a1) + 0.05, '7', color=BLUE, fs=14)
    a2 = np.radians(110)
    ax.plot([O2[0], O2[0] + r * np.cos(a2)], [0, r * np.sin(a2)], color=BLUE, lw=1.3)
    txt(ax, O2[0] + r * np.cos(a2) - 0.05, r * np.sin(a2) + 0.12, '3', color=BLUE, fs=14)
    ax.plot([0, O2[0]], [0, 0], color=RED, lw=1.6, ls='--')
    txt(ax, O2[0] / 2 - 0.42, -0.4, '圓心距 ?', color=RED, fs=13)
    dot(ax, 0, 0, 'O₁', dx=-0.12, dy=0.12)
    dot(ax, *O2, 'O₂', dx=-0.06, dy=0.14)
    save(f, 30742)

@fig(50849)
def f50849():
    f, ax = new_ax(5.6, 5.2)
    # 地形:山頂在原點,西陡(等高線密)、東緩(疏),南側有溪谷(V 形往高處凹)
    x = np.linspace(-2.2, 3.4, 400)
    y = np.linspace(-3.0, 2.4, 400)
    X, Y = np.meshgrid(x, y)
    ax_w = np.where(X < 0, 0.7, 1.9)
    Z = np.exp(-(X / ax_w) ** 2 - (Y / 1.5) ** 2)
    Z = Z - 0.28 * np.exp(-(X / 0.35) ** 2) * (Y < 0) * np.clip(-Y / 1.6, 0, 1)
    cs = ax.contour(X, Y, Z, levels=[0.2, 0.35, 0.5, 0.65, 0.8], colors=['#7a5c3e'], linewidths=1.2)
    ax.plot([0], [0.05], marker='^', ms=9, color=INK)
    txt(ax, 0.12, 0.12, '山頂', fs=12)
    txt(ax, -2.05, 0.0, '西', color=BLUE, fs=13)
    txt(ax, 3.05, 0.0, '東', color=BLUE, fs=13)
    txt(ax, 0.35, -2.75, '南(V 形)', color=RED, fs=12)
    ax.annotate('', xy=(2.6, 2.15), xytext=(2.6, 1.55), arrowprops=dict(arrowstyle='->', color=INK, lw=1.3))
    txt(ax, 2.72, 1.8, '北', fs=12)
    save(f, 50849)

# ══ 批次 C:自然(波、光、力學)═══════════════════════════

def wave_fig(qid, note_left, note_right, mark_P=False):
    f, ax = plt.subplots(figsize=(6.6, 3.4), dpi=200)
    ax.axis('off')
    x = np.linspace(0, 10, 400)
    y = np.sin(x * 2 * np.pi / 4)
    ax.plot(x, y, color=BLUE, lw=2)
    ax.axhline(0, color=GREY, lw=0.8, ls=':')
    # 波長標注(兩相鄰波峰 x=1→5)
    ax.annotate('', xy=(5, 1.35), xytext=(1, 1.35), arrowprops=dict(arrowstyle='<->', color=RED, lw=1.4))
    ax.text(2.55, 1.5, '波長 4 m', fontsize=12, color=RED, fontproperties=PF)
    ax.annotate('', xy=(9.9, -1.6), xytext=(8.4, -1.6), arrowprops=dict(arrowstyle='->', color=INK, lw=1.6))
    ax.text(7.9, -1.95, '傳播方向', fontsize=11, color=INK, fontproperties=PF)
    ax.text(0.0, -1.95, note_left, fontsize=12, color=INK, fontproperties=PF)
    ax.text(4.2, -1.95, note_right, fontsize=12, color=INK, fontproperties=PF)
    if mark_P:
        ax.plot([1], [1], 'o', ms=6, color=RED)
        ax.text(0.85, 1.12, 'P', fontsize=13, color=RED, fontproperties=PF)
    ax.set_ylim(-2.2, 1.9)
    save(f, qid)

@fig(40171)
def f40171():
    wave_fig(40171, '週期 2 秒', '', mark_P=True)

@fig(40467)
def f40467():
    wave_fig(40467, '波速 8 m/s', '')

@fig(40455)
def f40455():
    f, ax = plt.subplots(figsize=(6.6, 3.2), dpi=200)
    ax.axis('off')
    x1 = np.linspace(0, 5, 200)
    y1 = 0.9 * np.sin(x1 * 2 * np.pi / 2.4)
    ax.plot(x1, y1, color=BLUE, lw=1.6)
    x2 = np.linspace(5, 10, 200)
    y2 = 0.55 * np.sin((x2 - 5) * 2 * np.pi / 1.5 + np.pi * 0.2)
    ax.plot(x2, y2, color=BLUE, lw=3.6)
    ax.axvline(5, color=GREY, lw=1, ls='--')
    ax.text(1.6, 1.25, '細繩', fontsize=12, color=INK, fontproperties=PF)
    ax.text(7.4, 1.25, '粗繩', fontsize=12, color=INK, fontproperties=PF)
    ax.annotate('', xy=(4.2, -1.45), xytext=(2.7, -1.45), arrowprops=dict(arrowstyle='->', color=INK, lw=1.6))
    ax.text(2.2, -1.8, '傳播方向', fontsize=11, color=INK, fontproperties=PF)
    ax.set_ylim(-2.0, 1.6)
    save(f, 40455)

@fig(40478)
def f40478():
    f, ax = new_ax(5.2, 5.0)
    ax.axhline(0, color=INK, lw=1.6)                       # 界面
    ax.plot([0, 0], [-2.2, 2.2], color=GREY, lw=1, ls='--')  # 法線
    inc = np.radians(45)
    ax.annotate('', xy=(0, 0), xytext=(-2.0 * np.sin(inc), 2.0 * np.cos(inc)),
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.8))
    ref = np.radians(30)
    ax.annotate('', xy=(1.8 * np.sin(ref), -1.8 * np.cos(ref)), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.8))
    arc(ax, 0, 0, 0.8, 90, 135)
    txt(ax, -0.62, 0.92, '45°', color=RED, fs=13)
    arc(ax, 0, 0, 0.8, 270, 300, color=BLUE)
    txt(ax, 0.42, -1.05, '30°', color=BLUE, fs=13)
    txt(ax, -2.3, 1.85, '空氣', fs=13)
    txt(ax, -2.3, -1.0, '玻璃', fs=13)
    ax.set_xlim(-2.5, 2.3)
    ax.set_ylim(-2.3, 2.3)
    save(f, 40478)

@fig(40529)
def f40529():
    f, ax = new_ax(4.6, 4.8)
    ax.plot([-1.6, 1.9], [0, 0], color=INK, lw=1.8)
    ax.add_patch(MCircle((0, 5 * 0.8), 0.22, facecolor='#e59d00', edgecolor=INK))
    ax.annotate('', xy=(0, 2.6), xytext=(0, 3.6), arrowprops=dict(arrowstyle='->', color=GREY, lw=1.4))
    ax.plot([-1.2, 1.2], [0.8, 0.8], color=RED, lw=1, ls='--')
    dot(ax, 0.0, 0.8, '', dx=0, dy=0)
    txt(ax, 1.28, 0.75, '距地 1 m', color=RED, fs=12)
    txt(ax, 1.28, 0.3, '動能 = ?', color=RED, fs=12)
    ax.annotate('', xy=(-1.05, 0), xytext=(-1.05, 4.0), arrowprops=dict(arrowstyle='<->', color=INK, lw=1.2))
    txt(ax, -1.55, 2.0, '5 m', fs=12)
    txt(ax, 0.35, 4.15, '質量 2 kg,自由落下', color=GREY, fs=11)
    ax.set_ylim(-0.5, 4.6)
    save(f, 40529)

def wire_compass(qid, compass_above):
    f, ax = new_ax(6.0, 3.6)
    ax.plot([-2.6, 2.6], [0, 0], color=INK, lw=2.4)
    ax.annotate('', xy=(1.9, 0.22), xytext=(0.7, 0.22), arrowprops=dict(arrowstyle='->', color=RED, lw=1.8))
    txt(ax, 1.0, 0.4, '電流 I', color=RED, fs=13)
    cy = 1.05 if compass_above else -1.05
    ax.add_patch(MCircle((0, cy), 0.5, facecolor='#f4f4f4', edgecolor=INK, lw=1.4))
    ax.plot([0], [cy], 'o', ms=3, color=INK)
    txt(ax, -0.22, cy + 0.62 if compass_above else cy - 0.85, '磁針', fs=12)
    txt(ax, 0.62, cy - 0.08, 'N 極指向?', color=BLUE, fs=13)
    txt(ax, -2.55, 0.35 if compass_above else -0.55, '導線', color=GREY, fs=11)
    ax.set_ylim(-2.0, 2.0)
    save(f, qid)

@fig(40546)
def f40546():
    wire_compass(40546, compass_above=False)

@fig(40794)
def f40794():
    wire_compass(40794, compass_above=True)

@fig(40549)
def f40549():
    f, ax = new_ax(5.6, 3.8)
    for gx in np.linspace(-2.2, 2.2, 6):
        for gy in np.linspace(-1.3, 1.3, 4):
            ax.plot([gx], [gy], marker='x', ms=7, color=GREY, mew=1.4)
    ax.plot([0.6, 0.6], [-1.5, 1.5], color=RED, lw=3)
    ax.annotate('', xy=(1.9, 0), xytext=(0.75, 0), arrowprops=dict(arrowstyle='->', color=BLUE, lw=2))
    txt(ax, 1.35, 0.15, 'v', color=BLUE, fs=14)
    txt(ax, -2.35, 1.62, '均勻磁場(射入紙面)', color=GREY, fs=11)
    txt(ax, 0.15, 1.62, '導線', color=RED, fs=12)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-1.9, 2.0)
    save(f, 40549)

@fig(40556)
def f40556():
    f, ax = new_ax(5.8, 3.8)
    for gy in np.linspace(-1.2, 1.2, 5):
        ax.annotate('', xy=(2.5, gy), xytext=(-2.5, gy), arrowprops=dict(arrowstyle='->', color=GREY, lw=1.1))
    txt(ax, 2.6, 1.1, 'B', color=GREY, fs=13)
    ax.add_patch(Rectangle((-0.8, -0.9), 1.6, 1.8, fill=False, edgecolor=RED, lw=2))
    th = np.linspace(np.radians(35), np.radians(145), 40)
    ax.plot(1.35 * np.cos(th), 1.55 + 0.35 * np.sin(th), color=BLUE, lw=1.6)
    ax.annotate('', xy=(1.35 * np.cos(np.radians(33)), 1.55 + 0.35 * np.sin(np.radians(33))),
                xytext=(1.35 * np.cos(np.radians(45)), 1.55 + 0.35 * np.sin(np.radians(45))),
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.6))
    txt(ax, -0.75, 1.95, '線圈旋轉 90°', color=BLUE, fs=12)
    txt(ax, -0.72, -0.15, '矩形線圈', color=RED, fs=12)
    ax.set_xlim(-2.8, 3.0)
    ax.set_ylim(-1.6, 2.3)
    save(f, 40556)

@fig(40563)
def f40563():
    f, ax = new_ax(4.8, 5.2)
    ax.plot([-1.2, 1.2], [4.6, 4.6], color=INK, lw=2)
    for hx in np.linspace(-1.1, 1.1, 9):
        ax.plot([hx, hx + 0.18], [4.6, 4.78], color=INK, lw=1)
    zz_y = np.linspace(4.6, 3.3, 14)
    zz_x = 0.16 * np.array([0, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 0])
    ax.plot(zz_x, zz_y, color=GREY, lw=1.4)
    ax.add_patch(Rectangle((-0.35, 2.3), 0.7, 1.0, facecolor='#dfe8f7', edgecolor=INK, lw=1.4))
    txt(ax, -0.14, 3.02, 'N', color=RED, fs=13)
    txt(ax, -0.13, 2.42, 'S', color=BLUE, fs=13)
    ax.annotate('', xy=(0.75, 3.35), xytext=(0.75, 2.35), arrowprops=dict(arrowstyle='<->', color=RED, lw=1.6))
    txt(ax, 0.9, 2.75, '上下振動', color=RED, fs=12)
    for cx in np.linspace(-0.45, 0.45, 4):
        e = matplotlib.patches.Ellipse((cx, 1.45), 0.3, 0.75, fill=False, edgecolor=INK, lw=1.3)
        ax.add_patch(e)
    txt(ax, -1.55, 1.4, '線圈\n(固定)', fs=11)
    ax.plot([0.6, 1.5, 1.5, 0.6], [1.45, 1.45, 0.4, 0.4], color=INK, lw=1.2)
    ax.add_patch(Rectangle((0.95, 0.25), 0.5, 0.3, fill=False, edgecolor=INK, lw=1.3))
    txt(ax, 1.02, 0.0, '電阻', fs=11)
    ax.set_xlim(-2.0, 2.1)
    ax.set_ylim(-0.4, 5.0)
    save(f, 40563)

@fig(40708)
def f40708():
    f, ax = new_ax(5.8, 4.0)
    S1, S2 = (-1.2, 0), (1.2, 0)
    for S in (S1, S2):
        for r in (0.5, 1.0, 1.5, 2.0):
            th = np.linspace(0, 2 * np.pi, 160)
            ax.plot(S[0] + r * np.cos(th), S[1] + r * np.sin(th), color=BLUE, lw=0.9, alpha=0.7)
        ax.plot([S[0]], [S[1]], 'o', ms=5, color=INK)
    txt(ax, S1[0] - 0.1, -0.35, 'S₁', fs=12)
    txt(ax, S2[0] - 0.1, -0.35, 'S₂', fs=12)
    # 兩同相波源:中垂線上路徑差 0 → 相長(乙);側邊節線 → 相消(甲)
    txt(ax, -0.6, 1.75, '乙(振動最劇烈)', color='#0a7d38', fs=12)
    ax.plot([0], [1.5], 's', ms=7, color='#0a7d38', mfc='none', mew=1.6)
    txt(ax, 1.85, 1.4, '甲(幾乎靜止)', color=RED, fs=12)
    ax.plot([2.05, 2.05], [1.15, 1.15], 's', ms=7, color=RED, mfc='none', mew=1.6)
    txt(ax, -2.9, -1.9, '兩列頻率相同的水波相遇', color=GREY, fs=11)
    ax.set_xlim(-3.4, 3.6)
    ax.set_ylim(-2.2, 2.3)
    save(f, 40708)

@fig(40762)
def f40762():
    f, ax = new_ax(6.2, 3.4)
    ax.plot([-3.0, 3.2], [0, 0], color=INK, lw=1.6)
    ax.add_patch(Rectangle((-2.0, 0.28), 3.4, 0.65, facecolor='#dfe8f7', edgecolor=INK, lw=1.4))
    ax.add_patch(Rectangle((0.6, 0.28), 1.0, 0.9, facecolor='#f6d6b0', edgecolor=INK, lw=1.4))
    ax.add_patch(MCircle((-1.4, 0.16), 0.16, facecolor='#666666'))
    ax.add_patch(MCircle((0.7, 0.16), 0.16, facecolor='#666666'))
    ax.annotate('', xy=(2.6, 0.6), xytext=(1.75, 0.6), arrowprops=dict(arrowstyle='->', color=RED, lw=2))
    txt(ax, 2.0, 0.78, '卡車突然加速', color=RED, fs=12)
    ax.annotate('', xy=(0.35, 1.35), xytext=(1.05, 1.35), arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.6))
    txt(ax, -0.9, 1.5, '木箱相對車向後滑', color=BLUE, fs=12)
    txt(ax, 0.72, 0.44, '木箱', fs=11)
    ax.set_ylim(-0.5, 2.0)
    save(f, 40762)

@fig(40776)
def f40776():
    f, ax = new_ax(5.4, 4.0)
    ax.plot([-0.3, 4.2], [0, 0], color=INK, lw=1.6)
    ax.plot([0, 3.6], [0, 2.1], color=INK, lw=1.6)
    ax.plot([3.6, 3.6], [0, 2.1], color=INK, lw=1.2)
    ang = np.arctan2(2.1, 3.6)
    cx, cy = 1.7, 1.7 * np.tan(ang)
    w, h = 0.9, 0.55
    t = matplotlib.transforms.Affine2D().rotate_around(cx, cy, ang) + ax.transData
    ax.add_patch(Rectangle((cx - w / 2, cy), w, h, facecolor='#dfe8f7', edgecolor=INK, lw=1.4, transform=t))
    bx = cx - (h / 2 + 0.05) * np.sin(ang) * -1
    ax.annotate('', xy=(cx, cy - 0.9), xytext=(cx, cy + 0.1), arrowprops=dict(arrowstyle='->', color=GREY, lw=1.6))
    txt(ax, cx + 0.08, cy - 0.85, '重力', color=GREY, fs=12)
    txt(ax, cx - 1.3, cy + 1.15, '支撐力 N 方向 = ?', color=RED, fs=13)
    arc(ax, 0, 0, 0.75, 0, np.degrees(ang), color=INK)
    ax.set_ylim(-0.6, 3.2)
    save(f, 40776)

# ══ 批次 D:自然(流程圖、示意圖)═════════════════════════

def box(ax, x, y, w, h, label, fc='#eef3fb', fs=12, color=INK):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=INK, lw=1.3))
    txt(ax, x + w / 2, y + h / 2, label, fs=fs, ha='center', va='center', color=color)

def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.6, style='->'):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle=style, color=color, lw=lw))

@fig(40413)
def f40413():
    f, ax = new_ax(6.6, 4.2)
    box(ax, 1.7, 3.0, 3.0, 0.9, '大氣二氧化碳', fc='#e8eef8')
    box(ax, 0.2, 1.2, 1.9, 0.9, '植物', fc='#e2f2e2')
    box(ax, 2.6, 1.2, 1.9, 0.9, '動物', fc='#fbeadb')
    box(ax, 4.9, 1.2, 1.9, 0.9, '分解者', fc='#f2e6f2')
    arrow(ax, 2.3, 3.0, 1.35, 2.12, style='<->')
    txt(ax, 0.55, 2.55, '光合/呼吸', color=GREY, fs=10)
    arrow(ax, 2.1, 1.65, 2.6, 1.65)
    arrow(ax, 4.5, 1.65, 4.9, 1.65)
    arrow(ax, 5.9, 2.1, 4.3, 3.0)
    txt(ax, 5.3, 2.6, '呼吸作用', color=GREY, fs=10)
    ax.set_xlim(-0.1, 7.0)
    ax.set_ylim(0.7, 4.3)
    save(f, 40413)

@fig(40589)
def f40589():
    f, ax = new_ax(6.4, 3.8)
    ax.add_patch(Rectangle((-3.1, -0.6), 3.1, 0.6, facecolor='#cfe4f7', edgecolor='none'))
    ax.add_patch(Rectangle((0, -0.6), 3.2, 0.6, facecolor='#e8d9bd', edgecolor='none'))
    ax.plot([-3.1, 3.2], [0, 0], color=INK, lw=1.2)
    txt(ax, -2.0, -0.42, '海', color=BLUE, fs=13)
    txt(ax, 1.6, -0.42, '陸地', color='#8a6b34', fs=13)
    ax.add_patch(MCircle((2.6, 2.6), 0.32, facecolor='#f6c344', edgecolor='none'))
    txt(ax, 2.25, 2.0, '白天', color='#b98a1a', fs=11)
    arrow(ax, -1.6, 0.35, 0.9, 0.35, color=RED, lw=2)
    txt(ax, -1.15, 0.5, '海風(風向)', color=RED, fs=12)
    arrow(ax, 1.6, 0.7, 1.6, 2.0, color=GREY, lw=1.6)
    txt(ax, 1.72, 1.35, '空氣受熱上升', color=GREY, fs=10)
    arrow(ax, 1.0, 2.4, -1.5, 2.4, color=GREY, lw=1.2)
    arrow(ax, -2.0, 2.0, -2.0, 0.7, color=GREY, lw=1.2)
    ax.set_xlim(-3.3, 3.5)
    ax.set_ylim(-0.8, 3.1)
    save(f, 40589)

@fig(40625)
def f40625():
    f, ax = new_ax(6.8, 3.6)
    names = ['心臟', '主動脈', '腎動脈', '腎臟', '腎靜脈', '下腔靜脈']
    xs = np.linspace(0, 8.4, 6)
    for x, n in zip(xs, names):
        fc = '#f8dede' if n == '腎臟' else '#eef3fb'
        box(ax, x, 1.0, 1.25, 0.8, n, fc=fc, fs=11)
    for i in range(5):
        arrow(ax, xs[i] + 1.25, 1.4, xs[i + 1], 1.4)
    arrow(ax, xs[5] + 0.6, 1.0, xs[0] + 0.6, 0.35, lw=1.2)
    ax.plot([xs[0] + 0.6, xs[5] + 0.6], [0.35, 0.35], color=INK, lw=1.2)
    arrow(ax, xs[0] + 0.6, 0.35, xs[0] + 0.6, 1.0, lw=1.2)
    txt(ax, xs[3] + 0.1, 2.05, '流經腎臟後,何者濃度明顯下降?', color=RED, fs=12, ha='center')
    ax.set_xlim(-0.3, 10.0)
    ax.set_ylim(0.0, 2.5)
    save(f, 40625)

@fig(40645)
def f40645():
    f, ax = new_ax(6.0, 4.4)
    def male(x, y, filled, label):
        ax.add_patch(Rectangle((x - 0.28, y - 0.28), 0.56, 0.56,
                               facecolor=INK if filled else 'white', edgecolor=INK, lw=1.4))
        txt(ax, x, y - 0.62, label, fs=11, ha='center')
    def female(x, y, filled, label, q=False):
        ax.add_patch(MCircle((x, y), 0.3, facecolor=INK if filled else 'white', edgecolor=INK, lw=1.4))
        if q:
            txt(ax, x - 0.07, y - 0.1, '?', color=RED, fs=14)
        txt(ax, x, y - 0.66, label, fs=11, ha='center')
    male(1.0, 3.4, True, '祖父(色盲)')
    female(2.6, 3.4, False, '祖母(正常)')
    ax.plot([1.3, 2.3], [3.4, 3.4], color=INK, lw=1.2)
    ax.plot([1.8, 1.8], [3.4, 2.75], color=INK, lw=1.2)
    male(1.8, 2.4, False, '父親(正常)')
    female(3.6, 2.4, False, '母親(正常)', q=True)
    ax.plot([2.1, 3.3], [2.4, 2.4], color=INK, lw=1.2)
    ax.plot([2.7, 2.7], [2.4, 1.75], color=INK, lw=1.2)
    male(2.7, 1.4, True, '小明(色盲)')
    txt(ax, 4.4, 3.5, '■ = 色盲', fs=11)
    txt(ax, 4.4, 3.1, '□ ○ = 正常', fs=11)
    txt(ax, 4.4, 2.7, '母親基因型 = ?', color=RED, fs=12)
    ax.set_xlim(0.2, 6.2)
    ax.set_ylim(0.6, 4.1)
    save(f, 40645)

@fig(40704)
def f40704():
    f, ax = new_ax(5.6, 4.2)
    ax.plot([-2.4, 2.6], [0, 0], color=INK, lw=2)               # 桌面
    txt(ax, 1.9, -0.35, '桌面', color=GREY, fs=11)
    ax.add_patch(Rectangle((-0.7, 0.02), 1.4, 1.5, facecolor='#f3e3d3', edgecolor=INK, lw=1.4))
    ax.plot([0.7, 1.05, 1.05, 0.7], [1.2, 1.1, 0.5, 0.4], color=INK, lw=1.3)
    txt(ax, -0.42, 0.7, '熱咖啡', fs=12)
    for wx in (-0.35, 0.05, 0.45):
        xw = np.linspace(0, 0.5, 40)
        ax.plot(wx + 0.08 * np.sin(xw * 12), 1.6 + xw, color=RED, lw=1.2)
    txt(ax, -0.3, 2.35, '對流(空氣上升)', color=RED, fs=11)
    arrow(ax, 0, 0.02, 0, -0.5, color=BLUE, lw=1.8)
    txt(ax, 0.15, -0.55, '傳導(經杯底→桌面)', color=BLUE, fs=11)
    for i, ang in enumerate((160, 180, 200)):
        r0, r1 = 0.85, 1.5
        a = np.radians(ang)
        arrow(ax, -0.7, 0.75, -0.7 + (r1 - r0) * np.cos(a) * 2.2, 0.75 + (r1 - r0) * np.sin(a) * 2.2,
              color='#e59d00', lw=1.2)
    txt(ax, -2.45, 0.95, '輻射', color='#e59d00', fs=11)
    ax.set_xlim(-2.6, 2.8)
    ax.set_ylim(-0.9, 2.7)
    save(f, 40704)

@fig(40834)
def f40834():
    f, ax = new_ax(5.6, 4.6)
    layers = [('0~5 m(最年輕)', '#f2e6c9', 3.4, 4.2),
              ('5~12 m', '#e3d3b0', 2.6, 3.4),
              ('12~20 m', '#d4bd93', 1.8, 2.6),
              ('20 m 以下(最老)', '#c2a877', 0.2, 1.2)]
    for name, fc, y0, y1 in layers:
        ax.add_patch(Rectangle((0, y0), 4.2, y1 - y0, facecolor=fc, edgecolor=INK, lw=1.1))
        txt(ax, 4.35, (y0 + y1) / 2, name, fs=11, va='center')
    ax.add_patch(Rectangle((0, 1.2), 4.2, 0.6, facecolor='#e88a7a', edgecolor=RED, lw=1.6))
    txt(ax, 2.1, 1.5, '約 20 m:比上方更年輕的岩石?', fs=11, ha='center', va='center', color='#7a1408')
    txt(ax, 0.0, 4.45, '地表', color=GREY, fs=11)
    ax.annotate('', xy=(-0.45, 0.4), xytext=(-0.45, 4.2), arrowprops=dict(arrowstyle='->', color=GREY, lw=1.3))
    txt(ax, -0.95, 2.3, '深度', color=GREY, fs=11)
    ax.set_xlim(-1.3, 7.6)
    ax.set_ylim(-0.1, 4.8)
    save(f, 40834)


# ══ 第二輪:模板化圖組 ═════════════════════════════════════

# 直角三角形(直角在 C,A 在右下,B 在左上)
def rt_tri(qid, w, h, bottom, left, hyp, angA):
    f, ax = new_ax(5.2, 4.4)
    C, A, B = (0, 0), (w, 0), (0, h)
    ax.plot([C[0], A[0], B[0], C[0]], [C[1], A[1], B[1], C[1]], color=INK, lw=1.6)
    ax.add_patch(Rectangle((0, 0), 0.22, 0.22, fill=False, ec=INK, lw=1))
    dot(ax, *C, 'C', dx=-0.3, dy=-0.3)
    dot(ax, *A, 'A', dx=0.12, dy=-0.3)
    dot(ax, *B, 'B', dx=-0.3, dy=0.1)
    if bottom:
        txt(ax, w / 2 - 0.3, -0.38, bottom, fs=13)
    if left:
        txt(ax, -0.85, h / 2, left, fs=13)
    if hyp:
        txt(ax, w / 2 + 0.25, h / 2 + 0.15, hyp, fs=13)
    if angA:
        ang = np.degrees(np.arctan2(h, -w) )
        arc(ax, w, 0, 0.6, 180 - np.degrees(np.arctan2(h, w)), 180)
        txt(ax, w - 1.45, 0.3, angA, color=RED, fs=13)
    ax.set_xlim(-1.2, w + 0.7)
    ax.set_ylim(-0.7, h + 0.5)
    save(f, qid)

@fig(30235)
def f30235(): rt_tri(30235, 2.4, 4.15, 'AC = 4', 'BC = 4√3', '', '∠A = ?')
@fig(30237)
def f30237(): rt_tri(30237, 2.4, 4.15, 'AC = 4', '', 'AB = ?', '∠A = 60°')
@fig(30240)
def f30240(): rt_tri(30240, 4.15, 2.4, 'AC = ?', 'BC = 5', '', '∠A = 30°')

# 坐標平面兩點距離
def coord_dist(qid, A, B):
    f, ax = new_ax(5.2, 5.0)
    for gx in range(-1, 6):
        ax.plot([gx, gx], [-1, 7], color='#eeeeee', lw=0.8, zorder=0)
    for gy in range(-1, 8):
        ax.plot([-1, 5], [gy, gy], color='#eeeeee', lw=0.8, zorder=0)
    ax.annotate('', xy=(5.2, 0), xytext=(-1.2, 0), arrowprops=dict(arrowstyle='->', color=INK, lw=1.2))
    ax.annotate('', xy=(0, 7.2), xytext=(0, -1.2), arrowprops=dict(arrowstyle='->', color=INK, lw=1.2))
    txt(ax, 5.05, -0.45, 'x', fs=12)
    txt(ax, 0.15, 7.0, 'y', fs=12)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=RED, lw=1.8)
    ax.plot([A[0], B[0], B[0]], [A[1], A[1], B[1]], color=BLUE, lw=1.2, ls='--')
    dot(ax, *A, f'A({A[0]}, {A[1]})', dx=0.15, dy=-0.55, color=INK)
    dot(ax, *B, f'B({B[0]}, {B[1]})', dx=0.15, dy=0.15, color=INK)
    txt(ax, (A[0] + B[0]) / 2 - 1.35, (A[1] + B[1]) / 2 + 0.35, '距離 = ?', color=RED, fs=13)
    save(f, qid)

@fig(30133)
def f30133(): coord_dist(30133, (0, 0), (3, 4))
@fig(30632)
def f30632(): coord_dist(30632, (0, 0), (3, 4))
@fig(30139)
def f30139(): coord_dist(30139, (1, 2), (4, 6))
@fig(30365)
def f30365(): coord_dist(30365, (1, 2), (4, 6))
@fig(30633)
def f30633(): coord_dist(30633, (1, 2), (4, 6))

# 圓餅圖
def pie_fig(qid, slices, note=''):
    f, ax = plt.subplots(figsize=(4.8, 4.4), dpi=200)
    labels = [s[0] for s in slices]
    vals = [s[1] for s in slices]
    colors = ['#7f9fd4', '#e8b26a', '#8fc98f', '#d48f8f', '#b39ddb'][:len(slices)]
    w, t, at = ax.pie(vals, labels=labels, colors=colors, startangle=90, counterclock=False,
                      autopct=lambda p: f'{p * 3.6:.0f}°' if qid in (30201, 30700) else f'{p:.0f}%',
                      textprops=dict(fontproperties=PF, fontsize=11))
    for a in at:
        a.set_fontproperties(PF)
        a.set_fontsize(10)
    if note:
        ax.set_title(note, fontproperties=PF, fontsize=11, color=GREY)
    save(f, qid)

@fig(30410)
def f30410():
    # C 的百分比不顯示在扇形上,避免把第一步計算洩題
    f, ax = plt.subplots(figsize=(4.8, 4.4), dpi=200)
    w, t = ax.pie([36, 25, 39], labels=['A 36%', 'B 25%', 'C = ?%'],
                  colors=['#7f9fd4', '#e8b26a', '#8fc98f'], startangle=90, counterclock=False,
                  textprops=dict(fontproperties=PF, fontsize=12))
    ax.set_title('500 位民眾的飲料喜好', fontproperties=PF, fontsize=11, color=GREY)
    save(f, 30410)
@fig(30201)
def f30201(): pie_fig(30201, [('珍珠奶茶', 25), ('其他飲料', 75)], '200 人的飲料調查')
@fig(30700)
def f30700(): pie_fig(30700, [('某項目', 20), ('其他', 80)], '圓形圖(某扇形圓心角 72°)')

# 30417 縱軸起點不同的兩張長條圖
@fig(30417)
def f30417():
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 3.4), dpi=200)
    data = [92, 95, 98]
    names = ['甲組', '乙組', '丙組']
    for ax, base, title in [(ax1, 0, '甲圖(縱軸從 0 開始)'), (ax2, 90, '乙圖(縱軸從 90 開始)')]:
        ax.bar(names, data, color='#7f9fd4', width=0.55)
        ax.set_ylim(base, 100)
        ax.set_title(title, fontproperties=PF, fontsize=11)
        ax.set_xticks(range(3))
        ax.set_xticklabels(names, fontproperties=PF, fontsize=10)
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
    f.tight_layout()
    save(f, 30417)

# 折線圖/長條圖模板
def line_fig(qid, xs, ys, xlabel, ylabel, highlight=None):
    f, ax = plt.subplots(figsize=(6.2, 3.6), dpi=200)
    ax.plot(range(len(xs)), ys, '-o', color=BLUE, lw=2, ms=5)
    for i, v in enumerate(ys):
        ax.annotate(str(v), (i, v), textcoords='offset points', xytext=(0, 8), ha='center',
                    fontsize=10, color=INK, fontproperties=PF)
    ax.set_xticks(range(len(xs)))
    ax.set_xticklabels(xs, fontproperties=PF, fontsize=10)
    ax.set_ylabel(ylabel, fontproperties=PF, fontsize=11)
    ax.grid(axis='y', color='#eeeeee')
    ax.set_ylim(min(ys) - 5, max(ys) + 6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    save(f, qid)

@fig(30424)
def f30424(): line_fig(30424, ['2019', '2020', '2021', '2022', '2023'], [35, 32, 28, 25, 22], '', 'PM2.5(μg/m³)')
@fig(30686)
def f30686(): line_fig(30686, ['週一', '週二', '週三', '週四', '週五', '週六', '週日'], [14, 16, 18, 15, 17, 20, 19], '', '氣溫(℃)')

def bar_fig(qid, names, vals, ylabel):
    f, ax = plt.subplots(figsize=(6.2, 3.6), dpi=200)
    ax.bar(names, vals, color='#7f9fd4', width=0.55)
    for i, v in enumerate(vals):
        ax.annotate(str(v), (i, v), textcoords='offset points', xytext=(0, 4), ha='center',
                    fontsize=10, color=INK, fontproperties=PF)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, fontproperties=PF, fontsize=10)
    ax.set_ylabel(ylabel, fontproperties=PF, fontsize=11)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    save(f, qid)

@fig(30692)
def f30692(): bar_fig(30692, ['綠茶', '紅茶', '咖啡', '果汁', '牛奶'], [120, 90, 150, 60, 80], '銷售量(杯)')
@fig(30701)
def f30701(): bar_fig(30701, ['A市', 'B市', 'C市', 'D市'], [25, 20, 28, 22], '年均溫(℃)')

# 30203 莖葉圖
@fig(30203)
def f30203():
    f, ax = new_ax(4.2, 2.6)
    ax.plot([1.1, 1.1], [0.2, 1.8], color=INK, lw=1.4)
    txt(ax, 0.45, 1.95, '莖', fs=13)
    txt(ax, 1.9, 1.95, '葉', fs=13)
    txt(ax, 0.55, 0.9, '7', fs=16)
    txt(ax, 1.5, 0.9, '2   5   8', fs=16)
    ax.plot([0.1, 3.4], [1.75, 1.75], color=GREY, lw=1)
    ax.set_xlim(0, 3.6)
    ax.set_ylim(0, 2.4)
    save(f, 30203)

# 聲音波形比較(甲上乙下)
def wave_pair(qid, a1, f1, a2, f2):
    f, axes = plt.subplots(2, 1, figsize=(6.0, 3.8), dpi=200, sharex=True)
    x = np.linspace(0, 10, 500)
    for ax, amp, freq, name, color in [(axes[0], a1, f1, '甲', BLUE), (axes[1], a2, f2, '乙', '#0a7d38')]:
        ax.plot(x, amp * np.sin(x * freq), color=color, lw=1.8)
        ax.axhline(0, color=GREY, lw=0.7, ls=':')
        ax.text(-0.9, 0, name, fontsize=14, color=color, fontproperties=PF, va='center')
        ax.set_ylim(-1.3, 1.3)
        ax.axis('off')
    axes[1].text(3.6, -1.9, '(橫軸:時間,縱軸:位移)', fontsize=10, color=GREY, fontproperties=PF)
    save(f, qid)

@fig(40456)
def f40456(): wave_pair(40456, 1.0, 2.6, 0.5, 1.3)   # 甲振幅大且頻率高
@fig(40714)
def f40714(): wave_pair(40714, 1.0, 1.3, 0.5, 2.6)   # 甲振幅大頻率低

# 40792 動滑輪
@fig(40792)
def f40792():
    f, ax = new_ax(4.4, 4.8)
    ax.plot([-1.4, 1.4], [4.4, 4.4], color=INK, lw=2)
    for hx in np.linspace(-1.3, 1.3, 10):
        ax.plot([hx, hx + 0.16], [4.4, 4.56], color=INK, lw=1)
    ax.plot([-0.6, -0.6], [4.4, 2.0], color=GREY, lw=1.6)          # 固定端
    ax.plot([0.6, 0.6], [4.4, 2.0], color=GREY, lw=1.6)            # 施力端
    ax.annotate('', xy=(0.6, 3.9), xytext=(0.6, 3.2), arrowprops=dict(arrowstyle='->', color=RED, lw=2))
    txt(ax, 0.75, 3.5, 'F(向上拉)', color=RED, fs=12)
    th = np.linspace(np.pi, 2 * np.pi, 80)
    ax.plot(0.6 * np.cos(th), 2.0 + 0.6 * np.sin(th), color=INK, lw=1.6)
    ax.plot([-0.6, 0.6], [2.0, 2.0], color='white', lw=2.5, zorder=3)
    ax.add_patch(MCircle((0, 2.0), 0.12, color=INK))
    ax.plot([0, 0], [1.4, 0.9], color=GREY, lw=1.6)
    ax.plot([0, 0], [2.0, 1.4], color=GREY, lw=0)   # 佔位
    ax.add_patch(Rectangle((-0.5, 0.1), 1.0, 0.8, facecolor='#dfe8f7', edgecolor=INK, lw=1.4))
    txt(ax, -0.35, 0.4, '100 N', fs=12)
    ax.plot([0, 0], [0.9, 1.42], color=GREY, lw=1.6)
    txt(ax, -1.85, 2.0, '動滑輪', color=GREY, fs=11)
    txt(ax, -0.5, 4.65, '(等速上升 2 m)', color=GREY, fs=10)
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-0.2, 4.9)
    save(f, 40792)

# 30720 平面鏡測電線桿
@fig(30720)
def f30720():
    f, ax = new_ax(6.6, 4.0)
    ax.plot([-0.6, 8.2], [0, 0], color=INK, lw=1.6)
    ax.plot([0, 0], [0, 1.6], color=INK, lw=2.5)                     # 人
    ax.add_patch(MCircle((0, 1.75), 0.16, fill=False, ec=INK, lw=1.4))
    M = (1.5, 0)
    ax.plot([M[0] - 0.28, M[0] + 0.28], [0.02, 0.02], color=BLUE, lw=3)
    txt(ax, M[0] - 0.25, -0.4, '鏡子', color=BLUE, fs=11)
    px = 1.5 + 6.0
    ph = 1.6 / 1.5 * 6.0
    ax.plot([px, px], [0, ph], color=INK, lw=3.5)
    txt(ax, px + 0.15, ph / 2, '高 ?', color=RED, fs=13)
    ax.plot([0, M[0]], [1.6, 0.02], color=GREY, lw=1, ls='--')
    ax.plot([M[0], px], [0.02, ph], color=GREY, lw=1, ls='--')
    txt(ax, 0.15, -0.4, '1.5 m', fs=11)
    txt(ax, 4.3, -0.4, '6 m', fs=11)
    txt(ax, -0.75, 0.8, '眼高\n1.6 m', fs=10)
    ax.set_ylim(-0.8, ph + 0.4)
    save(f, 30720)

# 40482 平行玻璃磚
@fig(40482)
def f40482():
    f, ax = new_ax(5.4, 4.4)
    ax.add_patch(Rectangle((-2.4, -0.7), 4.8, 1.4, facecolor='#e7eef8', edgecolor=INK, lw=1.3))
    txt(ax, 1.7, 0.0, '玻璃磚', fs=12)
    txt(ax, -2.3, 1.6, '空氣', color=GREY, fs=11)
    txt(ax, -2.3, -1.55, '空氣', color=GREY, fs=11)
    ax.annotate('', xy=(-0.8, 0.7), xytext=(-2.0, 1.9), arrowprops=dict(arrowstyle='->', color=RED, lw=1.8))
    txt(ax, -2.35, 2.0, '入射光', color=RED, fs=11)
    ax.plot([-0.8, -0.15], [0.7, -0.7], color=RED, lw=1.6, ls='-')
    ax.annotate('', xy=(0.9, -1.9), xytext=(-0.15, -0.7), arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.8))
    txt(ax, 0.6, -1.75, '出射光與入射光的關係?', color=BLUE, fs=11)
    ax.plot([-0.8, -0.8], [1.3, 0.1], color=GREY, lw=0.9, ls=':')
    ax.plot([-0.15, -0.15], [-0.1, -1.3], color=GREY, lw=0.9, ls=':')
    ax.set_xlim(-2.6, 3.4)
    ax.set_ylim(-2.2, 2.3)
    save(f, 40482)

# 圓:單弦與弦心距
def chord_dist(qid, p1, p2, chord_text, dist_text, note, foot=''):
    f, ax = new_ax(5.0, 4.8)
    circle(ax, 0, 0, 1)
    d, L = 0.55, np.sqrt(1 - 0.55 ** 2)
    ax.plot([-L, L], [d, d], color=INK, lw=1.6)
    ax.plot([0, 0], [0, d], color=RED, lw=1.2, ls='--')
    dot(ax, -L, d, p1, dx=-0.24, dy=0.06)
    dot(ax, L, d, p2, dx=0.08, dy=0.06)
    dot(ax, 0, 0, 'O', dx=0.06, dy=-0.22)
    if foot:
        dot(ax, 0, d, foot, dx=0.07, dy=0.09)
    txt(ax, 0.07, d * 0.45, dist_text, color=RED, fs=12)
    txt(ax, -0.42, d + 0.16, chord_text, fs=12)
    if note:
        txt(ax, -1.05, -1.25, note, color=GREY, fs=12)
    save(f, qid)

@fig(30216)
def f30216(): chord_dist(30216, 'A', 'B', 'AB = 16', '?', '半徑 10')
@fig(30219)
def f30219(): chord_dist(30219, 'P', 'Q', 'PQ = ?', '3', '半徑 5')
@fig(30227)
def f30227(): chord_dist(30227, 'C', 'D', 'CD = 10', '?', '直徑 AB = 26')
@fig(30430)
def f30430(): chord_dist(30430, 'A', 'B', 'AB = 16', 'OM = ?', '半徑 10', foot='M')
@fig(30438)
def f30438(): chord_dist(30438, 'A', 'B', '弦 = 12', '?', '直徑 20')
@fig(30721)
def f30721(): chord_dist(30721, 'A', 'B', 'AB = 8', '?', '半徑 5')
@fig(30723)
def f30723(): chord_dist(30723, 'P', 'Q', 'PQ = ?', '2.5', '直徑 13')
@fig(30440)
def f30440(): chord_dist(30440, 'A', 'B', 'AB = ?', 'OM = 3', '半徑 5,M 為 AB 中點', foot='M')

# 圓:兩弦與弦心距
def two_chords(qid, top_text, top_d, bot_text, bot_d, note):
    f, ax = new_ax(5.0, 4.8)
    circle(ax, 0, 0, 1)
    for d, text, dtext, sgn in [(0.5, top_text, top_d, 1), (0.68, bot_text, bot_d, -1)]:
        L = np.sqrt(1 - d ** 2)
        y = sgn * d
        ax.plot([-L, L], [y, y], color=INK, lw=1.5)
        ax.plot([0, 0], [0, y], color=RED if sgn > 0 else BLUE, lw=1.2, ls='--')
        txt(ax, 0.07, y * 0.5 - 0.04, dtext, color=RED if sgn > 0 else BLUE, fs=11)
        txt(ax, -0.45, y + (0.13 if sgn > 0 else -0.24), text, fs=12)
    dot(ax, 0, 0, 'O', dx=0.08, dy=-0.05)
    txt(ax, -1.05, -1.3, note, color=GREY, fs=12)
    save(f, qid)

@fig(30224)
def f30224(): two_chords(30224, 'AB', '4', 'CD', '5', '半徑 6,AB、CD 長度關係?')
@fig(30437)
def f30437(): two_chords(30437, 'AB', '6', 'CD', '8', '半徑 10,AB 與 CD 的長度差?')
@fig(30441)
def f30441(): two_chords(30441, 'AB = 10', '?', 'CD = 24', '?', '半徑 13,兩弦到圓心的距離差?')

# 圓:兩弦相交
def chords_cross(qid, pname, la, lb, lc, ld, t1):
    f, ax = new_ax(5.2, 5.0)
    circle(ax, 0, 0, 1)
    A = np.array([np.cos(np.radians(155)), np.sin(np.radians(155))])
    B = np.array([np.cos(np.radians(-25)), np.sin(np.radians(-25))])
    P = A + (B - A) * t1
    ax.plot([A[0], B[0]], [A[1], B[1]], color=INK, lw=1.4)
    dirv = np.array([np.cos(np.radians(75)), np.sin(np.radians(75))])
    b = 2 * P.dot(dirv)
    c = P.dot(P) - 1
    tpos = (-b + np.sqrt(b * b - 4 * c)) / 2
    tneg = (-b - np.sqrt(b * b - 4 * c)) / 2
    Cpt = P + dirv * tneg
    Dpt = P + dirv * tpos
    ax.plot([Cpt[0], Dpt[0]], [Cpt[1], Dpt[1]], color=BLUE, lw=1.4)
    dot(ax, *A, 'A', dx=-0.24, dy=0.05)
    dot(ax, *B, 'B', dx=0.08, dy=-0.1)
    dot(ax, *Cpt, 'C', dx=0.0, dy=-0.28)
    dot(ax, *Dpt, 'D', dx=-0.02, dy=0.1)
    dot(ax, *P, pname, dx=0.12, dy=-0.02)
    txt(ax, (A[0] + P[0]) / 2 - 0.1, (A[1] + P[1]) / 2 + 0.14, la, color=RED, fs=12)
    txt(ax, (B[0] + P[0]) / 2, (B[1] + P[1]) / 2 + 0.1, lb, color=RED, fs=12)
    txt(ax, (Cpt[0] + P[0]) / 2 + 0.08, (Cpt[1] + P[1]) / 2, lc, color=BLUE, fs=12)
    txt(ax, (Dpt[0] + P[0]) / 2 + 0.08, (Dpt[1] + P[1]) / 2, ld, color=BLUE, fs=12)
    save(f, qid)

@fig(30226)
def f30226(): chords_cross(30226, 'P', 'AP=3', 'PB=8', 'CP=4', 'PD=?', 3 / 11)
@fig(30434)
def f30434(): chords_cross(30434, 'E', 'AE=3', 'EB=12', 'CE=4', 'ED=?', 3 / 15)
@fig(30435)
def f30435(): chords_cross(30435, 'P', 'AP=6', 'PB=4', 'CP=3', 'PD=?', 6 / 10)

# 圓:切線長(P 外部一點)
def tangent_len(qid, tname, po_text, r_text, pa_text):
    f, ax = new_ax(6.2, 3.8)
    r, po = 1.5, 3.2
    circle(ax, 0, 0, r)
    P = (-po, 0)
    T = np.array([r * -r / po, r * np.sqrt(1 - (r / po) ** 2)])
    ax.plot([P[0], 0], [0, 0], color=GREY, lw=1.2, ls='--')
    ax.plot([P[0], T[0]], [P[1], T[1]], color=BLUE, lw=1.6)
    ax.plot([0, T[0]], [0, T[1]], color=INK, lw=1.2)
    dot(ax, *P, 'P', dx=-0.28, dy=-0.05)
    dot(ax, 0, 0, 'O', dx=0.08, dy=-0.24)
    dot(ax, *T, tname, dx=-0.03, dy=0.14)
    txt(ax, -po / 2 - 0.35, -0.35, po_text, fs=12)
    txt(ax, T[0] / 2 + 0.1, T[1] / 2 - 0.1, r_text, fs=12)
    txt(ax, (P[0] + T[0]) / 2 - 0.35, (P[1] + T[1]) / 2 + 0.22, pa_text, color=RED, fs=13)
    save(f, qid)

@fig(30433)
def f30433(): tangent_len(30433, 'A', 'PO = 13', '5', 'PA = ?')
@fig(30726)
def f30726(): tangent_len(30726, 'T', 'PO = 13', '5', 'PT = ?')
@fig(30728)
def f30728(): tangent_len(30728, 'T', 'PO = ?', '5', 'PT = 12')

# 30727 兩切線
@fig(30727)
def f30727():
    f, ax = new_ax(6.2, 4.2)
    r, po = 1.4, 3.0
    circle(ax, 0, 0, r)
    P = (-po, 0)
    k = r / po
    for sgn, name in [(1, 'A'), (-1, 'B')]:
        T = np.array([r * -k, sgn * r * np.sqrt(1 - k * k)])
        ax.plot([P[0], T[0]], [P[1], T[1]], color=BLUE, lw=1.6)
        ax.plot([0, T[0]], [0, T[1]], color=INK, lw=1.2)
        dot(ax, *T, name, dx=-0.02, dy=0.14 * sgn if sgn > 0 else -0.3)
    ax.plot([P[0], 0], [0, 0], color=GREY, lw=1.2, ls='--')
    dot(ax, *P, 'P', dx=-0.28, dy=-0.05)
    dot(ax, 0, 0, 'O', dx=0.1, dy=-0.05)
    txt(ax, -po / 2 - 0.4, 0.12, 'PO = 10', fs=12)
    txt(ax, -po * 0.55, 0.95, 'PA = 8', color=RED, fs=12)
    txt(ax, 0.35, 0.7, '半徑 = ?', color=RED, fs=12)
    save(f, 30727)

# 30731 兩圓外離
@fig(30731)
def f30731():
    f, ax = new_ax(6.6, 3.2)
    r1, r2, dd = 1.25, 0.75, 3.0
    circle(ax, 0, 0, r1)
    circle(ax, dd, 0, r2)
    ax.plot([0, dd], [0, 0], color=RED, lw=1.4, ls='--')
    dot(ax, 0, 0, 'O', dx=-0.05, dy=0.12)
    dot(ax, dd, 0, "O'", dx=-0.05, dy=0.12)
    a1 = np.radians(120)
    ax.plot([0, r1 * np.cos(a1)], [0, r1 * np.sin(a1)], color=BLUE, lw=1.2)
    txt(ax, r1 * 0.5 * np.cos(a1) - 0.3, r1 * 0.5 * np.sin(a1), '5', color=BLUE, fs=13)
    a2 = np.radians(60)
    ax.plot([dd, dd + r2 * np.cos(a2)], [0, r2 * np.sin(a2)], color=BLUE, lw=1.2)
    txt(ax, dd + r2 * 0.6 * np.cos(a2) + 0.07, r2 * 0.6 * np.sin(a2) + 0.08, '3', color=BLUE, fs=13)
    txt(ax, dd / 2 - 0.55, -0.4, "OO' = 12", color=RED, fs=13)
    txt(ax, dd / 2 - 0.9, -1.35, '兩圓外離,公切線共幾條?', color=GREY, fs=12)
    ax.set_ylim(-1.7, 1.6)
    save(f, 30731)

# 30732 直徑上的圓周角
@fig(30732)
def f30732():
    f, ax = new_ax(5.2, 4.6)
    circle(ax, 0, 0, 1)
    A, B = (-1, 0), (1, 0)
    th = np.arccos(0.28)
    C = (np.cos(th), np.sin(th))
    ax.plot([A[0], B[0]], [0, 0], color=INK, lw=1.5)
    ax.plot([A[0], C[0]], [A[1], C[1]], color=BLUE, lw=1.5)
    ax.plot([B[0], C[0]], [B[1], C[1]], color=BLUE, lw=1.5)
    dot(ax, *A, 'A', dx=-0.24, dy=-0.05)
    dot(ax, *B, 'B', dx=0.1, dy=-0.05)
    dot(ax, *C, 'C', dx=0.02, dy=0.13)
    dot(ax, 0, 0, 'O', dx=-0.06, dy=-0.26)
    txt(ax, -0.25, -0.28, '直徑 AB = 10', fs=12)
    txt(ax, (B[0] + C[0]) / 2 + 0.1, C[1] / 2, 'BC = 6', color=BLUE, fs=12)
    txt(ax, (A[0] + C[0]) / 2 - 0.55, C[1] / 2 + 0.1, 'AC = ?', color=RED, fs=13)
    save(f, 30732)

# 30735 圓心角 60° 與弦
@fig(30735)
def f30735():
    f, ax = new_ax(5.2, 4.8)
    circle(ax, 0, 0, 1)
    A = (np.cos(np.radians(120)), np.sin(np.radians(120)))
    B = (np.cos(np.radians(60)), np.sin(np.radians(60)))
    Cpt = (np.cos(np.radians(-60)), np.sin(np.radians(-60)))
    for X in (A, B):
        ax.plot([0, X[0]], [0, X[1]], color=INK, lw=1.3)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=BLUE, lw=1.6)
    arc(ax, 0, 0, 0.3, 60, 120)
    txt(ax, -0.16, 0.4, '60°', color=RED, fs=13)
    dot(ax, *A, 'A', dx=-0.22, dy=0.08)
    dot(ax, *B, 'B', dx=0.08, dy=0.08)
    dot(ax, *Cpt, 'C', dx=0.08, dy=-0.24)
    dot(ax, 0, 0, 'O', dx=0.02, dy=-0.26)
    txt(ax, -0.42, 0.98, 'AB = 6 公尺', color=BLUE, fs=12)
    txt(ax, -1.1, -1.3, '噴水池直徑 = ?', color=RED, fs=13)
    save(f, 30735)

# 50311 等高線同心圈
@fig(50311)
def f50311():
    f, ax = new_ax(5.0, 4.6)
    for i, rr in enumerate([2.1, 1.7, 1.3, 0.9, 0.5]):
        th = np.linspace(0, 2 * np.pi, 120)
        wob = 1 + 0.06 * np.sin(3 * th + i)
        ax.plot(rr * wob * np.cos(th), 0.85 * rr * wob * np.sin(th), color='#7a5c3e', lw=1.2)
    txt(ax, 1.55, -1.75, '最外圈 200 m', color=BLUE, fs=12)
    txt(ax, -0.5, 0.0, '最內圈 = ?', color=RED, fs=13)
    ax.plot([0], [0.02], marker='^', ms=8, color=INK)
    txt(ax, -1.0, 2.15, '等高線間距 20 m,共 5 條', color=GREY, fs=11)
    save(f, 50311)

# 50596 V 形等高線
@fig(50596)
def f50596():
    f, ax = new_ax(5.2, 4.2)
    # V 字尖端(曲線頂點)朝上 = 朝向高處
    for i, (yy, label) in enumerate([(0.0, '120 m'), (0.7, '140 m'), (1.4, '160 m')]):
        xx = np.linspace(-2.2, 2.2, 200)
        vy = yy + 0.3 + 0.9 * np.exp(-(xx / 0.55) ** 2)
        ax.plot(xx, vy, color='#7a5c3e', lw=1.3)
        txt(ax, 2.3, yy + 0.25, label, fs=11, color='#7a5c3e')
    ax.annotate('', xy=(0, 3.4), xytext=(0, 2.75), arrowprops=dict(arrowstyle='->', color=INK, lw=1.3))
    txt(ax, 0.14, 3.05, '高處', fs=12)
    txt(ax, -2.15, 3.3, 'V 字尖端朝向高處', color=RED, fs=12)
    ax.set_xlim(-2.4, 3.3)
    ax.set_ylim(0.4, 3.7)
    save(f, 50596)

if __name__ == '__main__':
    ids = [int(a) for a in sys.argv[1:]] or sorted(FIGS)
    for qid in ids:
        FIGS[qid]()
