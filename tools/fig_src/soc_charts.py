from fig_all import *   # plt, np, PF, fig, new_ax, save, txt, dot, circle, arc, INK/RED/BLUE/GREY

LBLUE = '#8fb3e0'
MONTHS = list(range(1, 13))


def style_ticks(ax, fs=12):
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontproperties(PF)
        lab.set_fontsize(fs)


def climo_ax(ax, T, R, tlim=(-10, 40), rlim=(0, 400), title=None, tstep=10, rstep=100):
    """月雨量長條(右軸)+月均溫折線(左軸)。"""
    ax2 = ax.twinx()
    ax2.bar(MONTHS, R, color=LBLUE, edgecolor=BLUE, lw=1.0, width=0.7, zorder=1)
    ax2.set_ylim(*rlim)
    ax2.set_yticks(np.arange(rlim[0], rlim[1] + 1, rstep))
    ax.set_zorder(ax2.get_zorder() + 1)
    ax.patch.set_visible(False)
    ax.plot(MONTHS, T, color=RED, lw=2.0, marker='o', ms=4, zorder=3)
    ax.set_ylim(*tlim)
    ax.set_yticks(np.arange(tlim[0], tlim[1] + 1, tstep))
    ax.set_xlim(0.4, 12.6)
    ax.set_xticks(MONTHS)
    ax.set_xlabel('月', fontproperties=PF, fontsize=12)
    ax.set_ylabel('月均溫(°C)', fontproperties=PF, fontsize=12, color=RED)
    ax2.set_ylabel('月雨量(mm)', fontproperties=PF, fontsize=12, color=BLUE)
    style_ticks(ax); style_ticks(ax2)
    if title:
        ax.set_title(title, fontproperties=PF, fontsize=13)
    return ax2


def climo(qid, T, R, **kw):
    f, ax = plt.subplots(figsize=(6, 4), dpi=200)
    climo_ax(ax, T, R, **kw)
    save(f, qid)


# ───────────────────────── 氣候圖 ─────────────────────────
@fig(50980)
def f50980():
    climo(50980, [26.5, 27.1, 27.5, 27.9, 28.3, 28.3, 27.9, 27.8, 27.6, 27.4, 26.9, 26.5],
          [240, 165, 185, 180, 170, 160, 160, 175, 170, 195, 255, 290], tlim=(0, 40))


@fig(50981)
def f50981():
    climo(50981, [14, 17, 21, 26, 32, 34, 35, 35, 32, 27, 20, 15],
          [12, 8, 22, 25, 5, 0, 0, 0, 0, 1, 6, 12], tlim=(0, 40))


@fig(50982)
def f50982():
    climo(50982, [8, 9, 11, 14, 18, 22, 25, 25, 22, 17, 12, 9],
          [80, 75, 70, 65, 45, 20, 15, 30, 70, 110, 110, 95], tlim=(0, 40), rlim=(0, 200), rstep=50)


@fig(50983)
def f50983():
    climo(50983, [24.5, 24.8, 23, 20, 16.5, 14, 13, 13.5, 15, 17.5, 20.5, 22.5],
          [15, 15, 20, 40, 110, 170, 150, 120, 80, 50, 25, 15], tlim=(0, 40), rlim=(0, 200), rstep=50)


@fig(50984)
def f50984():
    climo(50984, [24, 25, 27, 28.5, 30, 29, 27.5, 27, 27.5, 28.5, 27.5, 25.5],
          [1, 0, 0, 1, 15, 520, 840, 530, 310, 60, 15, 3], tlim=(0, 40), rlim=(0, 900), rstep=300)


@fig(50985)
def f50985():
    # 高雄 1991–2020 月平均(中央氣象署)
    climo(50985, [19.7, 20.7, 23.0, 25.7, 27.8, 28.9, 29.4, 28.9, 28.5, 26.9, 24.5, 21.2],
          [19, 18, 32, 68, 202, 416, 377, 512, 225, 53, 26, 19], tlim=(0, 40), rlim=(0, 600))


@fig(50986)
def f50986():
    f, axs = plt.subplots(1, 2, figsize=(6.6, 3.6), dpi=200, sharey=True)
    # 甲=基隆、乙=高雄,1991–2020 月平均雨量(中央氣象署)
    data = [('甲城市', [328, 350, 274, 211, 284, 290, 120, 211, 390, 378, 397, 357]),
            ('乙城市', [19, 18, 32, 68, 202, 416, 377, 512, 225, 53, 26, 19])]
    for ax, (name, R) in zip(axs, data):
        ax.bar(MONTHS, R, color=LBLUE, edgecolor=BLUE, lw=1.0, width=0.7)
        ax.set_title(name, fontproperties=PF, fontsize=13)
        ax.set_xticks([1, 3, 5, 7, 9, 11])
        ax.set_xlim(0.4, 12.6)
        ax.set_ylim(0, 600)
        ax.set_xlabel('月', fontproperties=PF, fontsize=12)
        style_ticks(ax)
    axs[0].set_ylabel('月雨量(mm)', fontproperties=PF, fontsize=12)
    f.tight_layout()
    save(f, 50986)


@fig(50987)
def f50987():
    climo(50987, [24.5, 23.5, 21.5, 18, 14.5, 11.5, 11, 12.5, 14.5, 17.5, 20.5, 23],
          [120, 120, 140, 120, 90, 60, 65, 70, 80, 125, 120, 115], tlim=(0, 40), rlim=(0, 200), rstep=50)


@fig(50988)
def f50988():
    f, ax = plt.subplots(figsize=(6, 4), dpi=200)
    A = [5, 5, 7, 9, 13, 16, 18, 18, 15, 12, 8, 6]
    B = [-7, -6, -1, 6, 13, 17, 19, 17, 11, 5, -1, -5]
    ax.plot(MONTHS, A, color=INK, lw=2.0, marker='o', ms=4)
    ax.plot(MONTHS, B, color=INK, lw=2.0, ls='--', marker='s', ms=4)
    ax.axhline(0, color=GREY, lw=1.0)
    txt(ax, 12.2, 6, '甲地', va='center', fs=13)
    txt(ax, 12.2, -5, '乙地', va='center', fs=13)
    ax.set_xlim(0.5, 13.3)
    ax.set_xticks(MONTHS)
    ax.set_ylim(-10, 25)
    ax.set_xlabel('月', fontproperties=PF, fontsize=12)
    ax.set_ylabel('月均溫(°C)', fontproperties=PF, fontsize=12)
    style_ticks(ax)
    save(f, 50988)


@fig(50989)
def f50989():
    climo(50989, [-39, -35, -22, -7, 6, 15, 19, 15, 6, -8, -28, -38],
          [8, 6, 5, 8, 15, 30, 40, 35, 25, 15, 12, 10], tlim=(-40, 30), rlim=(0, 140),
          tstep=10, rstep=20)


@fig(50990)
def f50990():
    climo(50990, [14.0, 14.0, 13.9, 14.0, 14.0, 14.0, 14.0, 14.3, 14.3, 14.0, 13.9, 14.0],
          [115, 130, 155, 175, 125, 50, 20, 25, 80, 130, 110, 100], tlim=(0, 40), rlim=(0, 200), rstep=50)


@fig(50991)
def f50991():
    climo(50991, [25, 28, 31, 32, 31, 29, 27, 26, 27, 28, 27, 25],
          [0, 0, 3, 15, 55, 135, 220, 260, 170, 50, 3, 0], tlim=(0, 40), rlim=(0, 400))


@fig(50992)
def f50992():
    # 臺北 1991–2020 月平均(中央氣象署)
    climo(50992, [16.4, 16.9, 18.8, 22.3, 25.6, 28.2, 29.9, 29.5, 27.7, 24.6, 21.9, 18.2],
          [94, 129, 158, 151, 245, 355, 214, 337, 337, 163, 89, 97], tlim=(0, 40), rlim=(0, 400))


# ───────────────────────── 人口 ─────────────────────────
AGE_LABELS = ['0', '10', '20', '30', '40', '50', '60', '70', '80']


def pyramid_ax(ax, m, fm, title=None, xmax=None):
    m, fm = np.array(m, float), np.array(fm, float)
    tot = (m.sum() + fm.sum()) / 100.0   # 換算成占總人口 %
    m, fm = m / tot, fm / tot
    y = np.arange(len(m))
    ax.barh(y, -m, height=0.85, color=LBLUE, edgecolor=BLUE, lw=0.8)
    ax.barh(y, fm, height=0.85, color='#f2b8b4', edgecolor=RED, lw=0.8)
    xmax = xmax or np.ceil(max(m.max(), fm.max()))
    ax.set_xlim(-xmax * 1.05, xmax * 1.05)
    ticks = np.linspace(-xmax, xmax, 5)
    ax.set_xticks(ticks)
    ax.set_xticklabels([f'{abs(t):g}' for t in ticks])
    ax.set_yticks(np.arange(0, len(m), 2) - 0.5)
    ax.set_yticklabels(AGE_LABELS[:len(np.arange(0, len(m), 2))])
    ax.set_ylim(-0.6, len(m) - 0.4)
    ax.axvline(0, color=INK, lw=1.0)
    ax.text(0.02, 1.01, '男', color=BLUE, fontsize=13, fontproperties=PF, transform=ax.transAxes, va='bottom')
    ax.text(0.98, 1.01, '女', color=RED, fontsize=13, fontproperties=PF, transform=ax.transAxes, va='bottom', ha='right')
    ax.set_xlabel('占總人口(%)', fontproperties=PF, fontsize=12)
    style_ticks(ax)
    if title:
        ax.set_title(title, fontproperties=PF, fontsize=13)


def pyramid(qid, m, fm, xmax=None):
    f, ax = plt.subplots(figsize=(5.4, 4), dpi=200)
    pyramid_ax(ax, m, fm, xmax=xmax)
    ax.set_ylabel('年齡(歲)', fontproperties=PF, fontsize=12)
    save(f, qid)


# 5 歲一組,0–4 … 80+(17 組),數值為「占總人口 %」
EXPANSIVE_M = [8.0, 7.0, 6.1, 5.3, 4.5, 3.8, 3.2, 2.7, 2.2, 1.8, 1.4, 1.1, 0.8, 0.6, 0.4, 0.25, 0.15]
EXPANSIVE_F = [7.7, 6.8, 6.0, 5.2, 4.5, 3.8, 3.2, 2.7, 2.2, 1.8, 1.5, 1.2, 0.9, 0.7, 0.5, 0.3, 0.2]
CONSTR_M = [1.8, 2.0, 2.2, 2.4, 2.8, 3.0, 3.2, 3.4, 3.6, 3.7, 3.6, 3.4, 3.1, 2.7, 2.1, 1.5, 1.4]
CONSTR_F = [1.7, 1.9, 2.1, 2.3, 2.7, 2.9, 3.1, 3.3, 3.5, 3.6, 3.6, 3.5, 3.3, 3.0, 2.5, 2.0, 2.3]


@fig(50993)
def f50993():
    pyramid(50993, EXPANSIVE_M, EXPANSIVE_F, xmax=10)


@fig(50994)
def f50994():
    pyramid(50994, CONSTR_M, CONSTR_F, xmax=5)


@fig(50995)
def f50995():
    f, ax = plt.subplots(figsize=(5.6, 4), dpi=200)
    vals = [20, 60, 20]
    labs = ['0~14 歲\n20%', '15~64 歲\n60%', '65 歲以上\n20%']
    cols = [LBLUE, '#e6e6e6', '#f2b8b4']
    wedges, _ = ax.pie(vals, colors=cols, startangle=90, counterclock=False,
                       wedgeprops=dict(edgecolor=INK, lw=1.2))
    for w, s in zip(wedges, labs):
        a = np.radians((w.theta1 + w.theta2) / 2)
        txt(ax, 0.6 * np.cos(a), 0.6 * np.sin(a), s, ha='center', va='center', fs=13)
    ax.set_title('某國(虛構)年齡結構', fontproperties=PF, fontsize=13)
    ax.set_aspect('equal')
    save(f, 50995)


@fig(50996)
def f50996():
    m = [2.6, 2.5, 2.6, 2.9, 5.2, 7.2, 6.6, 5.0, 3.6, 2.9, 2.4, 1.9, 1.4, 1.0, 0.7, 0.4, 0.3]
    fm = [2.5, 2.4, 2.5, 2.8, 4.9, 6.8, 6.2, 4.7, 3.4, 2.8, 2.4, 2.0, 1.5, 1.1, 0.8, 0.5, 0.4]
    pyramid(50996, m, fm, xmax=8)


@fig(50997)
def f50997():
    f, ax = plt.subplots(figsize=(6.2, 4), dpi=200)
    years = [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025]
    vals = [5.8, 7.4, 8.9, 10.3, 12.1, 14.8, 17.6, 21.0]
    ax.bar(range(len(years)), vals, color=LBLUE, edgecolor=BLUE, lw=1.0, width=0.65)
    for i, v in enumerate(vals):
        txt(ax, i, v + 0.4, f'{v}', ha='center', fs=12)
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels([str(y) for y in years])
    ax.set_ylim(0, 25)
    ax.set_ylabel('65 歲以上人口占比(%)', fontproperties=PF, fontsize=12)
    ax.set_xlabel('年', fontproperties=PF, fontsize=12)
    ax.set_title('某國(虛構)老年人口比例', fontproperties=PF, fontsize=13)
    style_ticks(ax, 11)
    save(f, 50997)


@fig(50998)
def f50998():
    f, ax = plt.subplots(figsize=(6.2, 4), dpi=200)
    names = ['亞洲', '甲', '歐洲', '乙', '北美洲', '大洋洲']
    vals = [58, 19, 9, 8, 5, 1]   # 聯合國 WPP 推估,2024~2026 年約略值
    ax.bar(range(6), vals, color=LBLUE, edgecolor=BLUE, lw=1.0, width=0.65)
    for i, v in enumerate(vals):
        txt(ax, i, v + 1, f'{v}', ha='center', fs=12)
    ax.set_xticks(range(6))
    ax.set_xticklabels(names)
    ax.set_ylim(0, 68)
    ax.set_ylabel('占世界人口(%)', fontproperties=PF, fontsize=12)
    ax.set_title('世界各洲人口占比(約略值)', fontproperties=PF, fontsize=13)
    style_ticks(ax, 12)
    save(f, 50998)


# 51001:甲(幼年多)、乙(老年多)兩國扶養比都約 60
DEP_A_M = [6.0, 5.4, 5.0, 4.7, 4.3, 3.8, 3.4, 3.0, 2.6, 2.2, 1.9, 1.5, 1.1, 0.6, 0.35, 0.2, 0.15]
DEP_A_F = [5.8, 5.2, 4.8, 4.6, 4.3, 3.8, 3.4, 3.0, 2.6, 2.3, 2.0, 1.6, 1.2, 0.7, 0.4, 0.25, 0.2]
DEP_B_M = [2.0, 2.0, 2.1, 2.5, 2.8, 3.0, 3.2, 3.3, 3.4, 3.4, 3.3, 3.2, 3.0, 3.0, 2.8, 2.5, 2.4]
DEP_B_F = [1.9, 1.9, 2.0, 2.4, 2.7, 2.9, 3.1, 3.2, 3.3, 3.3, 3.3, 3.3, 3.2, 3.2, 3.0, 2.9, 3.8]


@fig(50999)
def f50999():
    f, axs = plt.subplots(1, 2, figsize=(6.8, 3.9), dpi=200)
    pyramid_ax(axs[0], DEP_A_M, DEP_A_F, title='甲國', xmax=8)
    pyramid_ax(axs[1], DEP_B_M, DEP_B_F, title='乙國', xmax=5)
    axs[0].set_ylabel('年齡(歲)', fontproperties=PF, fontsize=12)
    f.tight_layout()
    save(f, 50999)


def transition(qid, years, birth, death, bounds, labels):
    f, ax = plt.subplots(figsize=(6.4, 4), dpi=200)
    ax.plot(years, birth, color=RED, lw=2.0, label='出生率')
    ax.plot(years, death, color=BLUE, lw=2.0, ls='--', label='死亡率')
    for b in bounds[1:-1]:
        ax.axvline(b, color=GREY, lw=1.2, ls=':')
    for (a, b), lab in zip(zip(bounds[:-1], bounds[1:]), labels):
        txt(ax, (a + b) / 2, 47, lab, ha='center', fs=14)
    ax.set_xlim(bounds[0], bounds[-1])
    ax.set_ylim(0, 52)
    ax.set_xlabel('年', fontproperties=PF, fontsize=12)
    ax.set_ylabel('‰', fontproperties=PF, fontsize=12)
    leg = ax.legend(prop=PF, fontsize=12, loc='center right', frameon=False)
    for t in leg.get_texts():
        t.set_fontsize(12)
    style_ticks(ax)
    save(f, qid)


@fig(51000)
def f51000():
    years = [1900, 1920, 1940, 1950, 1960, 1980, 2000, 2020]
    birth = [40, 40, 40, 39, 36, 25, 15, 12]
    death = [33, 30, 22, 14, 10, 8, 7, 8]
    transition(51000, years, birth, death, [1900, 1935, 1975, 2020], ['甲', '乙', '丙'])


@fig(51001)
def f51001():
    years = [1900, 1925, 1950, 1975, 2000, 2010, 2020, 2030]
    birth = [42, 41, 34, 20, 11, 9, 7, 6]
    death = [32, 22, 13, 8, 7, 8, 10, 12]
    transition(51001, years, birth, death, [1900, 1930, 1960, 2000, 2030], ['甲', '乙', '丙', '丁'])


# ───────────────────────── 統計圖 ─────────────────────────
def stacked3(ax, names, data, legend, fmt='{:g}'):
    data = np.array(data, float)
    cols = ['#cfe3c2', LBLUE, '#f2b8b4']
    bottom = np.zeros(len(names))
    for i in range(3):
        ax.bar(range(len(names)), data[:, i], bottom=bottom, color=cols[i], edgecolor=INK, lw=1.0,
               width=0.6, label=legend[i])
        for j, v in enumerate(data[:, i]):
            if v >= 6:
                txt(ax, j, bottom[j] + v / 2, fmt.format(v), ha='center', va='center', fs=12)
        bottom += data[:, i]
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names)
    ax.set_ylim(0, 100)
    ax.set_xlim(-0.6, len(names) - 0.4)
    style_ticks(ax)


@fig(51002)
def f51002():
    f, ax = plt.subplots(figsize=(6.4, 4), dpi=200)
    stacked3(ax, ['甲國', '乙國', '丙國', '丁國'],
             [[42, 22, 36], [3, 22, 75], [65, 10, 25], [18, 33, 49]],
             ['第一級產業', '第二級產業', '第三級產業'])
    ax.set_ylabel('就業人口比例(%)', fontproperties=PF, fontsize=12)
    ax.set_xlim(-0.6, 5.2)
    leg = ax.legend(prop=PF, loc='center right', frameon=False)
    for t in leg.get_texts():
        t.set_fontsize(12)
    save(f, 51002)


@fig(51003)
def f51003():
    f, ax = plt.subplots(figsize=(6.4, 4), dpi=200)
    # 行政院主計總處(農業統計年報 112 年表 1 轉載):1960、1986、2020 年
    stacked3(ax, ['1960 年', '1986 年', '2020 年'],
             [[28.2, 26.4, 45.4], [5.4, 46.0, 48.6], [1.6, 39.0, 59.4]],
             ['農業', '工業', '服務業'], fmt='{:.1f}')
    ax.set_ylabel('占國內生產毛額(%)', fontproperties=PF, fontsize=12)
    ax.set_xlim(-0.6, 3.9)
    leg = ax.legend(prop=PF, loc='center right', frameon=False)
    for t in leg.get_texts():
        t.set_fontsize(12)
    ax.set_title('臺灣產業結構(約略值)', fontproperties=PF, fontsize=13)
    save(f, 51003)


@fig(51004)
def f51004():
    f, ax = plt.subplots(figsize=(6, 4), dpi=200)
    vals = [40, 40, 10, 6, 4]
    labs = ['燃煤 40%', '燃氣 40%', '再生能源 10%', '核能 6%', '其他 4%']
    cols = ['#bbbbbb', '#e6e6e6', '#cfe3c2', LBLUE, '#f2b8b4']
    wedges, _ = ax.pie(vals, colors=cols, startangle=90, counterclock=False,
                       wedgeprops=dict(edgecolor=INK, lw=1.2))
    pos = [(0.45, 0.1, 'center'), (-0.45, -0.25, 'center'), (-0.95, 0.75, 'right'),
           (-0.45, 1.12, 'right'), (0.2, 1.12, 'left')]
    for w, s, (x, y, ha) in zip(wedges, labs, pos):
        txt(ax, x, y, s, ha=ha, va='center', fs=12)
    ax.set_title('某國(虛構)發電結構', fontproperties=PF, fontsize=13)
    ax.set_aspect('equal')
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.35, 1.35)
    save(f, 51004)


@fig(51005)
def f51005():
    f, ax = plt.subplots(figsize=(6.4, 4), dpi=200)
    names = ['甲國', '乙國', '丙國', '丁國']
    ex = [120, 70, 150, 60]
    im = [80, 140, 40, 50]
    x = np.arange(4)
    ax.bar(x - 0.19, ex, width=0.36, color=LBLUE, edgecolor=BLUE, lw=1.0, label='出口值')
    ax.bar(x + 0.19, im, width=0.36, color='#f2b8b4', edgecolor=RED, lw=1.0, label='進口值')
    for i in range(4):
        txt(ax, i - 0.19, ex[i] + 3, str(ex[i]), ha='center', fs=11)
        txt(ax, i + 0.19, im[i] + 3, str(im[i]), ha='center', fs=11)
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylim(0, 180)
    ax.set_ylabel('貿易值(億美元)', fontproperties=PF, fontsize=12)
    ax.set_title('某國(虛構)與四個貿易夥伴的貿易', fontproperties=PF, fontsize=13)
    leg = ax.legend(prop=PF, loc='upper right', frameon=False, ncol=2)
    for t in leg.get_texts():
        t.set_fontsize(12)
    style_ticks(ax)
    save(f, 51005)


@fig(51006)
def f51006():
    f, axs = plt.subplots(1, 2, figsize=(6.8, 3.8), dpi=200)
    names = ['甲', '乙', '丙', '丁']
    tot = [1000, 800, 300, 400]
    per = [2, 16, 10, 1]
    for ax, vals, ttl, yl, top in [(axs[0], tot, '二氧化碳總排放量', '百萬公噸', 1200),
                                   (axs[1], per, '每人平均排放量', '公噸／人', 20)]:
        ax.bar(range(4), vals, color=LBLUE, edgecolor=BLUE, lw=1.0, width=0.6)
        for i, v in enumerate(vals):
            txt(ax, i, v + top * 0.02, str(v), ha='center', fs=12)
        ax.set_xticks(range(4)); ax.set_xticklabels(names)
        ax.set_ylim(0, top)
        ax.set_yticks(np.linspace(0, top, 5))
        ax.set_title(ttl, fontproperties=PF, fontsize=13)
        ax.set_ylabel(yl, fontproperties=PF, fontsize=12)
        style_ticks(ax, 11)
    f.suptitle('四國(虛構)排放資料', fontproperties=PF, fontsize=13, y=1.0)
    f.tight_layout()
    save(f, 51006)


@fig(51007)
def f51007():
    f, ax = plt.subplots(figsize=(6.2, 4), dpi=200)
    names = ['稻米', '蔬菜', '水果', '肉類', '小麥', '玉米']
    vals = [110, 85, 80, 65, 1, 2]
    ax.bar(range(6), vals, color=LBLUE, edgecolor=BLUE, lw=1.0, width=0.6)
    for i, v in enumerate(vals):
        txt(ax, i, v + 2, str(v), ha='center', fs=12)
    ax.axhline(100, color=GREY, lw=1.2, ls='--')
    ax.set_xticks(range(6)); ax.set_xticklabels(names)
    ax.set_ylim(0, 125)
    ax.set_ylabel('自給率(%)', fontproperties=PF, fontsize=12)
    ax.set_title('某國(虛構)各類糧食自給率', fontproperties=PF, fontsize=13)
    style_ticks(ax)
    save(f, 51007)


@fig(51008)
def f51008():
    f, ax = plt.subplots(figsize=(6.4, 4), dpi=200)
    names = ['1980 年', '2020 年']
    data = np.array([[30, 45, 5, 20], [3, 7, 60, 30]], float)
    legend = ['農產品', '紡織、成衣、鞋類', '電子與資訊產品', '其他']
    cols = ['#cfe3c2', '#f2b8b4', LBLUE, '#e6e6e6']
    bottom = np.zeros(2)
    for i in range(4):
        ax.bar(range(2), data[:, i], bottom=bottom, color=cols[i], edgecolor=INK, lw=1.0,
               width=0.5, label=legend[i])
        for j, v in enumerate(data[:, i]):
            if v >= 5:
                txt(ax, j, bottom[j] + v / 2, f'{v:g}', ha='center', va='center', fs=12)
        bottom += data[:, i]
    ax.set_xticks(range(2)); ax.set_xticklabels(names)
    ax.set_xlim(-0.5, 3.0)
    ax.set_ylim(0, 100)
    ax.set_ylabel('占出口總值(%)', fontproperties=PF, fontsize=12)
    ax.set_title('某國(虛構)出口商品結構', fontproperties=PF, fontsize=13)
    leg = ax.legend(prop=PF, loc='center right', frameon=False)
    for t in leg.get_texts():
        t.set_fontsize(12)
    style_ticks(ax)
    save(f, 51008)


@fig(51009)
def f51009():
    f, ax = plt.subplots(figsize=(6.2, 4), dpi=200)
    yrs = [2010, 2015, 2020, 2025]
    vals = [4, 7, 10, 20]
    ax.plot(yrs, vals, color=BLUE, lw=2.0, marker='o', ms=5)
    for x, v in zip(yrs, vals):
        txt(ax, x - 0.4, v + 1.2, f'{v}%', ha='right', fs=12)
    ax.plot([2030], [30], marker='*', ms=13, color=RED)
    txt(ax, 2030, 32.5, '2030 年目標 30%', ha='center', fs=12, color=RED)
    ax.set_xlim(2008, 2033)
    ax.set_xticks([2010, 2015, 2020, 2025, 2030])
    ax.set_ylim(0, 40)
    ax.set_ylabel('再生能源發電占比(%)', fontproperties=PF, fontsize=12)
    ax.set_xlabel('年', fontproperties=PF, fontsize=12)
    ax.set_title('某國(虛構)再生能源發電占比', fontproperties=PF, fontsize=13)
    style_ticks(ax)
    save(f, 51009)


# ───────────────────────── 經濟圖 ─────────────────────────
def sd_axes(ax, xmax=10, ymax=10):
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_linewidth(1.4); ax.spines['bottom'].set_linewidth(1.4)
    ax.set_xlabel('數量', fontproperties=PF, fontsize=12, loc='right')
    ax.set_ylabel('價格', fontproperties=PF, fontsize=12, loc='top')


X0 = 1.5   # 供需線整體右移,避免平移後被座標軸切掉


def line(ax, x0, y0, x1, y1, lab, color=INK, ls='-', dx=0.15, dy=0.0):
    x0, x1 = x0 + X0, x1 + X0
    ax.plot([x0, x1], [y0, y1], color=color, lw=2.0, ls=ls)
    txt(ax, x1 + dx, y1 + dy, lab, color=color, fs=13, va='center')


def shift_arrow(ax, x0, y0, x1, y1, color=RED):
    ax.annotate('', xy=(x1 + X0, y1), xytext=(x0 + X0, y0),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.8))


def D(ax, k=0, lab='D', **kw):   # 需求線:由左上到右下,k 為水平平移
    line(ax, 1 + k, 9, 8 + k, 2, lab, **kw)


def S(ax, k=0, lab='S', **kw):   # 供給線:由左下到右上
    line(ax, 1 + k, 2, 8 + k, 9, lab, dy=0.1, **kw)


@fig(51010)
def f51010():
    f, ax = plt.subplots(figsize=(5.4, 4), dpi=200)
    sd_axes(ax, 12.5, 10.5)
    S(ax)
    D(ax, 0, 'D₁')
    D(ax, 2, 'D₂', color=RED, ls='--')
    shift_arrow(ax, 4.3, 4.6, 5.9, 4.6)
    save(f, 51010)


@fig(51011)
def f51011():
    f, ax = plt.subplots(figsize=(5.4, 4), dpi=200)
    sd_axes(ax, 12.5, 10.5)
    D(ax)
    S(ax, 0, 'S₁')
    S(ax, -1.4, 'S₂', color=RED, ls='--')
    shift_arrow(ax, 6.0, 7.0, 4.6, 7.0)
    save(f, 51011)


def four_panels(qid, order):
    """order:四個面板(甲乙丙丁)各自的移動種類:'D+','D-','S+','S-'。"""
    f, axs = plt.subplots(2, 2, figsize=(6.2, 4.8), dpi=200)
    for ax, kind, name in zip(axs.flat, order, ['甲', '乙', '丙', '丁']):
        sd_axes(ax, 13, 10.5)
        ax.set_xlabel('數量', fontproperties=PF, fontsize=11, loc='right')
        ax.set_ylabel('價格', fontproperties=PF, fontsize=11, loc='top')
        if kind[0] == 'D':
            S(ax)
            D(ax, 0, 'D₁')
            k = 1.6 if kind[1] == '+' else -1.4
            D(ax, k, 'D₂', color=RED, ls='--')
            shift_arrow(ax, 4.5, 5.5, 4.5 + 0.8 * k, 5.5)
        else:
            D(ax)
            S(ax, 0, 'S₁')
            k = 1.6 if kind[1] == '+' else -1.4
            S(ax, k, 'S₂', color=RED, ls='--')
            shift_arrow(ax, 5.0, 6.5, 5.0 + 0.8 * k, 6.5)
        ax.set_title(name, fontproperties=PF, fontsize=13)
    f.tight_layout()
    save(f, qid)


@fig(51012)
def f51012():
    four_panels(51012, ['D+', 'S+', 'D-', 'S-'])


@fig(51013)
def f51013():
    f, ax = plt.subplots(figsize=(5.6, 4.2), dpi=200)
    sd_axes(ax, 12.5, 10.5)
    D(ax)
    S(ax)
    # 均衡點 E (4.5, 5.5);候選新均衡點
    pts = {'E': (4.5, 5.5), '甲': (3.3, 6.7), '乙': (5.7, 4.3), '丙': (5.7, 6.7), '丁': (3.3, 4.3)}
    for k, (x, y) in pts.items():
        x += X0
        ax.plot([x], [y], 'o', ms=6, color=RED if k != 'E' else INK, zorder=5)
        dx = {'E': 0.25, '甲': -0.7, '乙': -0.75, '丙': 0.25, '丁': 0.25}[k]
        dy = {'E': 0.0, '甲': 0.1, '乙': -0.45, '丙': 0.1, '丁': -0.45}[k]
        txt(ax, x + dx, y + dy, k, fs=13, va='center')
    save(f, 51013)


@fig(51014)
def f51014():
    f, ax = plt.subplots(figsize=(5.6, 4.2), dpi=200)
    sd_axes(ax, 13.5, 11)
    D(ax, 0, 'D₁')
    S(ax, 0, 'S₁')
    D(ax, 1.4, 'D₂', color=RED, ls='--')
    S(ax, -1.4, 'S₂', color=RED, ls='--')
    # E1 = (4.5, 5.5);E2:D2 與 S2 交點 (4.5, 6.9)
    for (x, y, lab) in [(4.5, 5.5, 'E₁'), (4.5, 6.9, 'E₂')]:
        x += X0
        ax.plot([x], [y], 'o', ms=6, color=INK, zorder=5)
        txt(ax, x + 0.3, y, lab, fs=13, va='center')
    save(f, 51014)


def idx_axes(ax, years, ylim, ylabel):
    ax.set_xticks(years)
    ax.set_xlim(years[0] - 0.5, years[-1] + 0.5)
    ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel, fontproperties=PF, fontsize=12)
    ax.set_xlabel('年', fontproperties=PF, fontsize=12)
    style_ticks(ax)


@fig(51015)
def f51015():
    f, ax = plt.subplots(figsize=(6.2, 4), dpi=200)
    yrs = list(range(2019, 2025))
    cpi = [100, 101, 103, 108, 112, 114]
    ax.plot(yrs, cpi, color=RED, lw=2.0, marker='o', ms=5)
    for x, v in zip(yrs, cpi):
        txt(ax, x, v + 0.8, str(v), ha='center', fs=12)
    idx_axes(ax, yrs, (96, 118), '消費者物價指數')
    ax.set_title('某國(虛構)消費者物價指數(2019 年=100)', fontproperties=PF, fontsize=13)
    save(f, 51015)


@fig(51016)
def f51016():
    f, ax = plt.subplots(figsize=(6.4, 4.2), dpi=200)
    yrs = list(range(2019, 2025))
    cpi = [100, 101, 103, 108, 112, 114]
    wage = [100, 102, 105, 107, 112, 116]
    ax.plot(yrs, wage, color=BLUE, lw=2.0, marker='s', ms=5, label='平均名目薪資指數')
    ax.plot(yrs, cpi, color=RED, lw=2.0, ls='--', marker='o', ms=5, label='消費者物價指數')
    for x, w, c in zip(yrs, wage, cpi):
        if w == c:
            txt(ax, x, w + 1.0, str(w), ha='center', fs=11, color=INK)
            continue
        txt(ax, x, w + (1.0 if w > c else -2.0), str(w), ha='center', fs=11, color=BLUE)
        txt(ax, x, c + (1.0 if c > w else -2.0), str(c), ha='center', fs=11, color=RED)
    idx_axes(ax, yrs, (94, 120), '指數(2019 年=100)')
    leg = ax.legend(prop=PF, loc='upper left', frameon=False)
    for t in leg.get_texts():
        t.set_fontsize(12)
    ax.set_title('某國(虛構)薪資與物價', fontproperties=PF, fontsize=13)
    save(f, 51016)


@fig(51017)
def f51017():
    f, ax = plt.subplots(figsize=(6.2, 4), dpi=200)
    yrs = list(range(2006, 2013))
    u = [3.9, 3.9, 4.1, 5.9, 5.2, 4.4, 4.2]
    ax.plot(yrs, u, color=BLUE, lw=2.0, marker='o', ms=5)
    for x, v in zip(yrs, u):
        txt(ax, x - (0.22 if x == 2008 else 0), v + 0.15, f'{v}', ha='center', fs=12)
    idx_axes(ax, yrs, (3, 6.6), '失業率(%)')
    ax.set_title('某國(虛構)失業率', fontproperties=PF, fontsize=13)
    save(f, 51017)


@fig(51018)
def f51018():
    f, ax = plt.subplots(figsize=(5.8, 4.2), dpi=200)
    p = np.array([10, 20, 30, 40, 50])
    qd = 600 - 10 * p
    qs = 10 * p
    ax.plot(qd, p, color=INK, lw=2.0, marker='o', ms=4)
    ax.plot(qs, p, color=BLUE, lw=2.0, marker='o', ms=4)
    txt(ax, qd[-1] - 10, 52, '需求', fs=13, ha='center')
    txt(ax, qs[-1] + 10, 52, '供給', fs=13, ha='center', color=BLUE)
    ax.set_xlim(0, 600); ax.set_ylim(0, 60)
    ax.set_xticks([0, 100, 200, 300, 400, 500, 600])
    ax.set_yticks([0, 10, 20, 30, 40, 50, 60])
    ax.grid(color='#dddddd', lw=0.8)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_xlabel('數量(個)', fontproperties=PF, fontsize=12)
    ax.set_ylabel('價格(元)', fontproperties=PF, fontsize=12)
    style_ticks(ax, 11)
    save(f, 51018)


@fig(51019)
def f51019():
    f, ax = plt.subplots(figsize=(6.2, 4), dpi=200)
    months = ['1月', '3月', '5月', '7月', '9月', '11月']
    rate = [32.0, 31.4, 30.6, 29.8, 28.9, 28.2]
    ax.plot(range(6), rate, color=BLUE, lw=2.0, marker='o', ms=5)
    for i, v in enumerate(rate):
        txt(ax, i, v + 0.25, f'{v}', ha='center', fs=12)
    ax.set_xticks(range(6)); ax.set_xticklabels(months)
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(27, 33)
    ax.set_ylabel('1 美元可兌換新臺幣(元)', fontproperties=PF, fontsize=12)
    ax.set_title('某年新臺幣兌美元匯率(虛構)', fontproperties=PF, fontsize=13)
    style_ticks(ax)
    save(f, 51019)
