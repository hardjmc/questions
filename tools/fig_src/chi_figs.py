from fig_all import *   # plt, np, PF, fig, new_ax, save, txt, dot, circle, arc, INK/RED/BLUE/GREY
from matplotlib.patches import FancyBboxPatch, Rectangle, Wedge, Polygon

FS = 15
LIGHT = '#dfe8f6'
PINK = '#f8dedc'


def P(size):
    p = PF.copy()
    p.set_size(size)
    return p


def style(ax, fs=14):
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontproperties(P(fs))
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(1.3)


def chart(w=6.4, h=4.0):
    f, ax = plt.subplots(figsize=(w, h), dpi=200)
    return f, ax


def title(ax, s, fs=16, y=1.04):
    ax.set_title(s, fontproperties=P(fs), color=INK, y=y)


def box(ax, x, y, w, h, s, fs=FS, fc='white', ec=INK, lw=1.5, color=INK, r=0.08, **kw):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                                fc=fc, ec=ec, lw=lw))
    ax.text(x, y, s, fontproperties=P(fs), color=color, ha='center', va='center', **kw)


def arrow(ax, p, q, color=INK, lw=1.6):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=16))


def t(ax, x, y, s, fs=FS, color=INK, **kw):
    ax.text(x, y, s, fontproperties=P(fs), color=color, **kw)


def vtext(ax, x, y, s, fs=FS, color=INK, gap=1.0, **kw):
    """直排文字:由 (x, y) 往下排。gap 為字距(資料座標)。"""
    for i, ch in enumerate(s):
        if ch == ' ':
            continue
        ax.text(x, y - i * gap, ch, fontproperties=P(fs), color=color, ha='center', va='center', **kw)


def canvas(w, h, xlim, ylim):
    f, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis('off')
    return f, ax


# 11000 每週課外閱讀時間
@fig(11000)
def f11000():
    f, ax = chart()
    cats = ['未滿1', '1～3', '3～5', '5以上']
    vals = [45, 80, 50, 25]
    ax.bar(cats, vals, color=BLUE, width=0.6)
    for i, v in enumerate(vals):
        t(ax, i, v + 2, f'{v}人', fs=14, ha='center', va='bottom')
    ax.set_ylim(0, 95)
    ax.set_ylabel('人數', fontproperties=P(14))
    ax.set_xlabel('每週閱讀時間（小時）', fontproperties=P(14))
    title(ax, '九年級學生每週課外閱讀時間（共200人）')
    style(ax)
    save(f, 11000)


# 11001 紙本書與電子書借閱量
@fig(11001)
def f11001():
    f, ax = chart()
    yrs = [2021, 2022, 2023, 2024, 2025]
    paper = [52, 48, 45, 41, 38]
    ebook = [8, 14, 21, 29, 36]
    ax.plot(yrs, paper, '-o', color=BLUE, lw=2, ms=6)
    ax.plot(yrs, ebook, '--s', color=RED, lw=2, ms=6)
    for x, a, b in zip(yrs, paper, ebook):
        t(ax, x, a + 2.2, str(a), fs=13, ha='center', color=BLUE)
        t(ax, x, b - 5.2, str(b), fs=13, ha='center', color=RED)
    t(ax, 2025.15, 38, '紙本書', fs=14, color=BLUE, va='center')
    t(ax, 2025.15, 32, '電子書', fs=14, color=RED, va='center')
    ax.set_xlim(2020.6, 2025.9); ax.set_ylim(0, 60)
    ax.set_xticks(yrs); ax.set_xticklabels([str(y) for y in yrs])
    ax.set_ylabel('借閱量（萬冊）', fontproperties=P(14))
    title(ax, '青禾鎮圖書館借閱量')
    style(ax)
    save(f, 11001)


# 11002 畢業旅行投票圓餅圖
@fig(11002)
def f11002():
    f, ax = plt.subplots(figsize=(6.4, 4.0), dpi=200)
    vals = [12, 9, 6, 3]
    labs = ['山林步道\n12票', '海邊\n9票', '主題樂園\n6票', '博物館\n3票']
    cols = ['#9db7e0', '#f2b8b3', '#c9d9a8', '#e6d3a3']
    ws, _ = ax.pie(vals, colors=cols, startangle=90, counterclock=False,
                   wedgeprops=dict(edgecolor='white', linewidth=2))
    for w, s in zip(ws, labs):
        a = np.radians((w.theta1 + w.theta2) / 2)
        r = 0.62 if w.theta2 - w.theta1 > 40 else 1.28
        ax.text(r * np.cos(a), r * np.sin(a), s, fontproperties=P(14), ha='center', va='center', color=INK)
    ax.set_aspect('equal')
    ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.1, 1.6)
    ax.set_title('畢業旅行地點投票（全班30人，每人一票）', fontproperties=P(15), y=1.02)
    save(f, 11002)


# 11003 二手書交換市集海報
@fig(11003)
def f11003():
    f, ax = canvas(6.0, 4.2, (0, 10), (0, 7))
    ax.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 6.4, boxstyle='round,pad=0,rounding_size=0.3',
                                fc='#fffaf0', ec=INK, lw=1.8))
    t(ax, 5, 6.0, '社區二手書交換市集', fs=21, ha='center', va='center', weight='bold')
    rows = [('日期', '12月6日'), ('時間', '上午 9:00～12:00'), ('地點', '社區活動中心一樓'),
            ('規則', '每帶1本書，可換1張兌換券')]
    for i, (k, v) in enumerate(rows):
        y = 4.75 - i * 0.95
        box(ax, 1.6, y, 1.5, 0.7, k, fs=15, fc=LIGHT, ec=BLUE, lw=1.3)
        t(ax, 2.7, y, v, fs=16, va='center')
    t(ax, 5, 0.85, '名額有限，請先報名！', fs=17, color=RED, ha='center', va='center')
    save(f, 11003)


# 11004 場地借用流程
@fig(11004)
def f11004():
    f, ax = canvas(6.8, 4.0, (0, 13.6), (0, 8))
    t(ax, 6.8, 7.5, '學生借用場地申請流程', fs=17, ha='center', va='center')
    t(ax, 6.8, 6.75, '※申請表須於使用日3天前送出', fs=14, ha='center', va='center', color=RED)
    y1 = 5.4
    xs = [1.8, 5.9, 10.6]
    for x, s in zip(xs, ['填寫申請表', '導師簽名', '學務處審核']):
        box(ax, x, y1, 3.2, 1.0, s, fs=15)
    arrow(ax, (3.4, y1), (4.3, y1)); arrow(ax, (7.5, y1), (9.0, y1))
    # 通過
    box(ax, 10.6, 2.9, 3.6, 1.0, '領取鑰匙使用場地', fs=14, fc=LIGHT, ec=BLUE)
    arrow(ax, (10.6, y1 - 0.5), (10.6, 3.4), color=BLUE)
    t(ax, 10.8, 4.15, '通過', fs=14, color=BLUE, va='center')
    box(ax, 10.6, 0.9, 4.6, 1.0, '活動結束當天歸還鑰匙', fs=14)
    arrow(ax, (10.6, 2.4), (10.6, 1.4))
    # 未通過
    box(ax, 5.9, 2.9, 3.6, 1.0, '依審核意見修改', fs=14, fc=PINK, ec=RED)
    arrow(ax, (9.3, y1 - 0.5), (7.7, 3.4), color=RED)
    t(ax, 6.5, 4.15, '未通過', fs=14, color=RED, va='center')
    arrow(ax, (5.9, 3.4), (5.9, y1 - 0.5), color=RED)
    t(ax, 5.7, 4.15, '重新送簽', fs=13, color=RED, ha='right', va='center')
    save(f, 11004)


# 11005 作家沈青大事記
@fig(11005)
def f11005():
    f, ax = canvas(6.8, 3.6, (0, 13.6), (0, 7.2))
    t(ax, 6.8, 6.7, '作家沈青大事記', fs=17, ha='center', va='center')
    ax.plot([0.5, 13.1], [3.6, 3.6], color=INK, lw=2)
    ev = [(1952, '出生於\n海邊漁村'), (1975, '發表第一篇\n散文〈潮聲〉'), (1983, '出版散文集\n《海的手》'),
          (1990, '移居山城'), (1998, '出版散文集\n《霧裡的山》'), (2010, '獲頒\n文學獎')]
    xs = np.linspace(1.3, 12.3, len(ev))
    for i, (x, (y, s)) in enumerate(zip(xs, ev)):
        ax.plot([x], [3.6], 'o', ms=8, color=BLUE)
        t(ax, x, 3.6 + (0.55 if i % 2 == 0 else -0.55), str(y), fs=14, ha='center',
          va='bottom' if i % 2 == 0 else 'top', color=BLUE)
        if i % 2 == 0:
            t(ax, x, 1.75, s, fs=14, ha='center', va='center', linespacing=1.3)
        else:
            t(ax, x, 5.45, s, fs=14, ha='center', va='center', linespacing=1.3)
    save(f, 11005)


def table_fig(qid, header, rows, colw, title_s=None, w=6.6, h=3.6, fs=15, hfs=15, rowh=1.0, first_bold=False):
    tot = sum(colw)
    n = len(rows) + 1
    top = n * rowh + (1.0 if title_s else 0.2)
    f, ax = canvas(w, h, (-0.1, tot + 0.1), (-0.1, top))
    if title_s:
        t(ax, tot / 2, n * rowh + 0.5, title_s, fs=16, ha='center', va='center')
    xs = np.concatenate([[0], np.cumsum(colw)])
    for r in range(n):
        y0 = (n - 1 - r) * rowh
        if r == 0:
            ax.add_patch(Rectangle((0, y0), tot, rowh, fc=LIGHT, ec='none'))
        cells = header if r == 0 else rows[r - 1]
        for c, s in enumerate(cells):
            t(ax, (xs[c] + xs[c + 1]) / 2, y0 + rowh / 2, s, fs=hfs if r == 0 else fs, ha='center', va='center')
    for r in range(n + 1):
        ax.plot([0, tot], [r * rowh, r * rowh], color=INK, lw=1.4 if r in (0, n, n - 1) else 1.0)
    for x in xs:
        ax.plot([x, x], [0, n * rowh], color=INK, lw=1.2)
    save(f, qid)


# 11006 三款保溫瓶比較
@fig(11006)
def f11006():
    table_fig(11006, ['款式', '容量', '保溫時間', '重量', '價格'],
              [['甲', '500毫升', '12小時', '380公克', '690元'],
               ['乙', '750毫升', '24小時', '520公克', '890元'],
               ['丙', '600毫升', '24小時', '410公克', '790元']],
              [1.2, 2.2, 2.2, 2.2, 1.8], title_s='三款保溫瓶規格比較', h=3.4)


# 11007 午餐剩食原因
@fig(11007)
def f11007():
    f, ax = chart(6.6, 3.8)
    cats = ['不喜歡菜色', '份量太多', '用餐時間太短', '身體不舒服'][::-1]
    vals = [66, 48, 42, 6][::-1]
    ax.barh(cats, vals, color=BLUE, height=0.55)
    for i, v in enumerate(vals):
        t(ax, v + 1.5, i, f'{v}人', fs=14, va='center')
    ax.set_xlim(0, 80)
    ax.set_xlabel('人數', fontproperties=P(14))
    title(ax, '午餐剩食原因調查（受訪120人，可複選）', fs=15)
    style(ax, 14)
    save(f, 11007)


# 11008 竹 心智圖
@fig(11008)
def f11008():
    f, ax = canvas(6.8, 4.0, (0, 13.6), (0, 8))
    c = (6.8, 4.0)
    nodes = [((3.0, 6.5), '外形', '中空、有節'), ((10.6, 6.5), '用途', '建材、竹筍可食'),
             ((3.0, 1.5), '象徵', '虛心、氣節'), ((10.6, 1.5), '詩句', '寧可食無肉，\n不可居無竹')]
    for (x, y), k, v in nodes:
        ax.plot([c[0], x], [c[1], y], color=GREY, lw=1.6, zorder=0)
    ax.add_patch(plt.Circle(c, 0.95, fc=PINK, ec=RED, lw=1.8))
    t(ax, c[0], c[1], '竹', fs=24, ha='center', va='center', color=RED)
    for (x, y), k, v in nodes:
        h = 2.3 if '\n' in v else 1.9
        ax.add_patch(FancyBboxPatch((x - 2.2, y - h / 2), 4.4, h, boxstyle='round,pad=0,rounding_size=0.15',
                                    fc='white', ec=BLUE, lw=1.5, zorder=2))
        t(ax, x, y + h / 2 - 0.42, k, fs=15, ha='center', va='center', color=BLUE, zorder=3)
        t(ax, x, y - 0.3 if '\n' in v else y - 0.25, v, fs=15, ha='center', va='center', linespacing=1.25, zorder=3)
    save(f, 11008)


# 11009 校外教學行程表
@fig(11009)
def f11009():
    table_fig(11009, ['時間', '行程'],
              [['08:00', '校門口集合出發'], ['09:30', '抵達科學館，分組參觀'], ['11:30', '午餐（請自備）'],
               ['12:30', '搭車前往植物園'], ['13:00', '植物園導覽（至15:00）'], ['16:30', '返抵學校']],
              [2.0, 5.6], title_s='校外教學行程表', w=5.6, h=4.2, rowh=0.8)


# 11010 信封(直式)
@fig(11010)
def f11010():
    f, ax = canvas(6.4, 4.4, (0, 12.8), (0, 8.8))
    ax.add_patch(Rectangle((4.4, 0.3), 4.0, 8.2, fc='#fffdf6', ec=INK, lw=1.8))
    # 郵票
    ax.add_patch(Rectangle((4.65, 6.95), 0.95, 1.25, fc='white', ec=GREY, lw=1.2, ls='--'))
    t(ax, 5.12, 7.57, '郵票', fs=12, ha='center', va='center', color=GREY)
    # 右:收件人地址
    vtext(ax, 7.85, 8.0, '臺北市青禾路三段一○八號', fs=13, gap=0.6)
    # 中:收件人
    vtext(ax, 6.4, 6.9, '林正雄', fs=21, gap=0.95)
    vtext(ax, 6.4, 3.85, '先生', fs=16, gap=0.75)
    vtext(ax, 6.4, 2.05, '收啟', fs=16, gap=0.75)
    # 左:寄件人
    vtext(ax, 4.85, 6.3, '臺中市和平路十二號', fs=12, gap=0.5)
    vtext(ax, 4.85, 1.75, '林', fs=12, gap=0.5)
    vtext(ax, 4.85, 1.25, '謹緘', fs=12, gap=0.45)
    # 說明文字
    t(ax, 9.0, 6.0, '←收信人地址', fs=14, va='center', color=BLUE)
    t(ax, 9.0, 3.0, '←收信人姓名\n  稱謂、啟封詞', fs=14, va='center', color=BLUE, linespacing=1.3)
    t(ax, 3.8, 4.0, '寄信人地址\n與緘封詞→', fs=14, va='center', ha='right', color=BLUE, linespacing=1.3)
    save(f, 11010)


# 11011 公布欄 師長喜訊
@fig(11011)
def f11011():
    f, ax = canvas(6.4, 3.6, (0, 12.8), (0, 7.2))
    ax.add_patch(FancyBboxPatch((0.3, 0.3), 12.2, 6.6, boxstyle='round,pad=0,rounding_size=0.3',
                                fc='#f3efe2', ec='#8a6d3b', lw=3))
    t(ax, 6.4, 5.9, '本週師長喜訊', fs=19, ha='center', va='center', color=RED)
    items = ['一、王老師喜獲麟兒', '二、李主任的父親八十大壽', '三、張老師的先生新開設診所']
    for i, s in enumerate(items):
        t(ax, 1.4, 4.4 - i * 1.35, s, fs=17, va='center')
    save(f, 11011)


# 11012 給老師的信
@fig(11012)
def f11012():
    f, ax = canvas(6.4, 4.2, (0, 12.8), (0, 8.4))
    ax.add_patch(Rectangle((0.3, 0.2), 12.2, 8.0, fc='#fffdf6', ec=INK, lw=1.5))
    t(ax, 0.9, 7.4, '陳老師 道鑒：', fs=16, va='center')
    t(ax, 1.6, 6.3, '謝謝您上週推薦的《小王子》，我已讀完，', fs=15, va='center')
    t(ax, 0.9, 5.45, '收穫很多，也更明白「看不見的才重要」。', fs=15, va='center')
    t(ax, 1.6, 4.4, '祝', fs=16, va='center')
    t(ax, 0.9, 3.5, '學安', fs=16, va='center')
    t(ax, 7.4, 2.3, '學生 李小華 敬上', fs=16, va='center')
    t(ax, 8.6, 1.1, '十一月二十日', fs=15, va='center')
    for s, (x, y) in [('甲', (5.0, 7.4)), ('乙', (3.0, 3.5)), ('丙', (11.7, 2.3)), ('丁', (12.0, 1.1))]:
        ax.add_patch(plt.Circle((x, y), 0.36, fc='white', ec=BLUE, lw=1.4))
        t(ax, x, y, s, fs=13, ha='center', va='center', color=BLUE)
    save(f, 11012)


# 11013 圖書館公告
@fig(11013)
def f11013():
    f, ax = canvas(6.6, 3.8, (0, 13.2), (0, 7.6))
    ax.add_patch(Rectangle((0.2, 0.2), 12.8, 7.2, fc='white', ec=INK, lw=1.8))
    t(ax, 6.6, 6.75, '圖書館公告', fs=19, ha='center', va='center')
    t(ax, 0.7, 5.6, '主旨：本館12月進行館藏盤點，暫停開放。', fs=15, va='center')
    t(ax, 0.7, 4.4, '一、閉館期間：12月8日至12月12日。', fs=15, va='center')
    t(ax, 0.7, 3.2, '二、到期日在閉館期間的書，還書期限', fs=15, va='center')
    t(ax, 1.95, 2.35, '延至12月15日。', fs=15, va='center')
    t(ax, 0.7, 1.15, '三、閉館期間，還書箱照常開放。', fs=15, va='center')
    save(f, 11013)


# 11014 各年級手機使用時間
@fig(11014)
def f11014():
    f, ax = chart()
    g = np.arange(3)
    wd = [1.5, 2.0, 2.5]; we = [3.5, 4.0, 3.0]
    ax.bar(g - 0.18, wd, 0.36, color=BLUE, label='平日')
    ax.bar(g + 0.18, we, 0.36, color='#f2a7a1', edgecolor=RED, lw=1.2, label='假日')
    for x, a, b in zip(g, wd, we):
        t(ax, x - 0.18, a + 0.08, f'{a}', fs=13, ha='center', va='bottom')
        t(ax, x + 0.18, b + 0.08, f'{b}', fs=13, ha='center', va='bottom')
    ax.set_xticks(g); ax.set_xticklabels(['七年級', '八年級', '九年級'])
    ax.set_ylim(0, 5); ax.set_ylabel('小時', fontproperties=P(14))
    ax.legend(prop=P(13), frameon=False, loc='upper right', ncol=2)
    title(ax, '各年級平均每日使用手機時間')
    style(ax)
    save(f, 11014)


# 11015 冰淇淋銷量與溺水事件
@fig(11015)
def f11015():
    f, ax = chart(6.8, 4.0)
    m = np.arange(1, 13)
    ice = [2, 2, 3, 5, 8, 12, 15, 14, 9, 5, 3, 2]
    dr = [0, 0, 1, 2, 4, 7, 9, 8, 4, 1, 0, 0]
    ax.bar(m, ice, color='#b9cbe8', width=0.6, label='冰淇淋銷量')
    ax.set_ylim(0, 18); ax.set_xticks(m); ax.set_xticklabels([str(i) for i in m])
    ax.set_ylabel('冰淇淋銷量（千支）', fontproperties=P(13), color=BLUE)
    ax.set_xlabel('月份', fontproperties=P(13))
    ax2 = ax.twinx()
    ax2.plot(m, dr, '-o', color=RED, lw=2, ms=5)
    ax2.set_ylim(0, 12)
    ax2.set_ylabel('溺水事件（件）', fontproperties=P(13), color=RED)
    for lab in ax2.get_yticklabels():
        lab.set_fontproperties(P(13))
    ax2.spines['top'].set_visible(False)
    title(ax, '某縣市各月冰淇淋銷量與溺水事件數', fs=15)
    style(ax, 13)
    ax.spines['right'].set_visible(True)
    save(f, 11015)


# 11016 再生紙流程
@fig(11016)
def f11016():
    f, ax = canvas(6.8, 3.4, (0, 13.6), (0, 6.8))
    t(ax, 6.8, 6.3, '再生紙製造流程（示意）', fs=17, ha='center', va='center')
    top = ['回收廢紙', '分類', '打漿\n（加水攪碎）', '除墨']
    bot = ['抄紙', '乾燥', '再生紙']
    xs = [1.6, 4.9, 8.4, 11.9]
    for x, s in zip(xs, top):
        box(ax, x, 4.4, 2.6, 1.3, s, fs=15, linespacing=1.2)
    for a, b in zip(xs[:-1], xs[1:]):
        arrow(ax, (a + 1.3, 4.4), (b - 1.3, 4.4))
    bx = [11.9, 8.4, 4.9]
    for x, s in zip(bx, bot):
        box(ax, x, 1.4, 2.6, 1.1, s, fs=15, fc=LIGHT if s == '再生紙' else 'white',
            ec=BLUE if s == '再生紙' else INK)
    arrow(ax, (11.9, 3.75), (11.9, 1.95))
    arrow(ax, (10.6, 1.4), (9.7, 1.4)); arrow(ax, (7.1, 1.4), (6.2, 1.4))
    save(f, 11016)


# 11017 說明文段落架構
@fig(11017)
def f11017():
    f, ax = canvas(6.8, 4.0, (0, 13.6), (0, 8))
    t(ax, 6.8, 7.55, '〈城市裡的綠屋頂〉段落架構', fs=16, ha='center', va='center')
    box(ax, 6.8, 6.3, 7.4, 1.0, '第一段：說明什麼是綠屋頂', fs=15, fc=LIGHT, ec=BLUE)
    mids = [('第二段\n降低室內溫度', 2.4), ('第三段\n減緩暴雨積水', 6.8), ('第四段\n提供生物棲地', 11.2)]
    for s, x in mids:
        box(ax, x, 3.9, 3.8, 1.5, s, fs=15, linespacing=1.3)
        arrow(ax, (6.8 if x == 6.8 else (5.0 if x < 6.8 else 8.6), 5.8), (x, 4.65))
        arrow(ax, (x, 3.15), (6.8 if x == 6.8 else (5.0 if x < 6.8 else 8.6), 2.0))
    box(ax, 6.8, 1.5, 7.4, 1.0, '第五段：總結並呼籲推廣', fs=15, fc=LIGHT, ec=BLUE)
    save(f, 11017)


# 11018 最受歡迎社團調查
@fig(11018)
def f11018():
    f, ax = chart()
    cats = ['熱舞社', '籃球社', '書法社', '其他']
    vals = [32, 5, 2, 1]
    ax.bar(cats, vals, color=BLUE, width=0.55)
    for i, v in enumerate(vals):
        t(ax, i, v + 0.6, f'{v}票', fs=14, ha='center', va='bottom')
    ax.set_ylim(0, 40); ax.set_ylabel('票數', fontproperties=P(14))
    title(ax, '全校最受歡迎社團調查', fs=16, y=1.1)
    t(ax, 1.5, 41.5, '調查對象：熱舞社社員40人', fs=14, ha='center', color=INK)
    style(ax)
    save(f, 11018)


# 11019 讀書會選書
@fig(11019)
def f11019():
    table_fig(11019, ['書名', '得票', '頁數', '館藏'],
              [['《星河旅人》', '12', '320', '8本'], ['《島嶼的風》', '10', '220', '4本'],
               ['《晚安，鯨魚》', '8', '180', '6本'], ['《祖母的菜園》', '5', '150', '7本']],
              [4.2, 1.6, 1.6, 1.6], title_s='讀書會候選書目', w=6.0, h=3.8)


# 11020 園遊會海報
@fig(11020)
def f11020():
    f, ax = canvas(6.0, 4.0, (0, 10), (0, 6.7))
    ax.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 6.1, boxstyle='round,pad=0,rounding_size=0.3',
                                fc='#fff6f5', ec=RED, lw=2))
    t(ax, 5, 5.6, '校慶園遊會', fs=22, ha='center', va='center', color=RED, weight='bold')
    rows = [('日期', '12月14日'), ('時間', '上午9:00～下午3:00'), ('地點', '學校操場'),
            ('園遊券', '每張100元，各攤位通用')]
    for i, (k, v) in enumerate(rows):
        y = 4.35 - i * 1.0
        box(ax, 1.65, y, 1.7, 0.72, k, fs=15, fc='white', ec=RED, lw=1.2)
        t(ax, 2.85, y, v, fs=16, va='center')
    save(f, 11020)


# 11021 動物睡眠時間
@fig(11021)
def f11021():
    f, ax = chart(6.4, 3.8)
    cats = ['無尾熊', '貓', '狗', '人', '長頸鹿'][::-1]
    vals = [20, 14, 11, 7, 2][::-1]
    ax.barh(cats, vals, color=BLUE, height=0.55)
    for i, v in enumerate(vals):
        t(ax, v + 0.3, i, f'{v}小時', fs=14, va='center')
    ax.set_xlim(0, 25); ax.set_xticks([0, 5, 10, 15, 20, 25])
    title(ax, '幾種動物每天的平均睡眠時間（示意）', fs=15)
    style(ax, 14)
    save(f, 11021)


# 11022 上學方式圓餅圖
@fig(11022)
def f11022():
    f, ax = plt.subplots(figsize=(6.4, 4.0), dpi=200)
    vals = [35, 25, 20, 15, 5]
    labs = ['步行\n35%', '騎腳踏車\n25%', '搭公車\n20%', '家長接送\n15%', '其他 5%']
    cols = ['#9db7e0', '#f2b8b3', '#c9d9a8', '#e6d3a3', '#d9d9d9']
    ws, _ = ax.pie(vals, colors=cols, startangle=90, counterclock=False,
                   wedgeprops=dict(edgecolor='white', linewidth=2))
    for w, s in zip(ws, labs):
        a = np.radians((w.theta1 + w.theta2) / 2)
        r = 0.63 if w.theta2 - w.theta1 > 30 else 1.3
        ax.text(r * np.cos(a), r * np.sin(a), s, fontproperties=P(14), ha='center', va='center')
    ax.set_aspect('equal'); ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.1, 1.6)
    ax.set_title('我們班同學上學的方式（全班40人）', fontproperties=P(15), y=1.02)
    save(f, 11022)


# 11023 步道與遊客人數
@fig(11023)
def f11023():
    f, ax = chart(6.8, 4.0)
    m = np.arange(1, 13)
    y24 = [3, 3, 4, 4, 5, 5, 6, 6, 5, 4, 4, 3]
    y25 = [3, 3, 4, 4, 5, 5, 9, 10, 9, 8, 8, 7]
    ax.plot(m, y25, '-s', color=BLUE, lw=3, ms=8, label='2025年', zorder=2)
    ax.plot(m, y24, '--o', color='#777777', lw=1.6, ms=4.5, label='2024年', zorder=3)
    ax.axvline(6.5, color=RED, ls=':', lw=1.6)
    t(ax, 6.65, 11.2, '2025年7月 新步道開放', fs=13, color=RED, va='center')
    ax.set_xticks(m); ax.set_xticklabels([str(i) for i in m])
    ax.set_ylim(0, 12); ax.set_xlabel('月份', fontproperties=P(13))
    ax.set_ylabel('遊客人數（千人）', fontproperties=P(13))
    ax.legend(prop=P(13), frameon=False, loc='upper left')
    title(ax, '山城鎮各月遊客人數', fs=15)
    style(ax, 13)
    save(f, 11023)


# 11024 人物關係圖
@fig(11024)
def f11024():
    f, ax = canvas(6.4, 4.0, (0, 12.8), (0, 8))
    t(ax, 6.4, 7.5, '小說《木頭會說話》人物關係圖', fs=16, ha='center', va='center')
    pos = {'阿蘭（姊）': (2.4, 5.4), '阿樹（弟）': (2.4, 1.4), '老木匠（父）': (10.4, 1.4), '阿德（子）': (10.4, 5.4)}
    edges = [('阿蘭（姊）', '阿樹（弟）', '姊弟'), ('阿樹（弟）', '老木匠（父）', '師徒'),
             ('老木匠（父）', '阿德（子）', '父子'), ('阿德（子）', '阿蘭（姊）', '同班同學')]
    for a, b, s in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.plot([x1, x2], [y1, y2], color=GREY, lw=1.8, zorder=0)
        t(ax, (x1 + x2) / 2, (y1 + y2) / 2, s, fs=15, ha='center', va='center', color=RED,
          bbox=dict(fc='white', ec='none', pad=2))
    for k, (x, y) in pos.items():
        box(ax, x, y, 3.4, 1.1, k, fs=16, fc=LIGHT, ec=BLUE)
    save(f, 11024)


# 11025 喜帖
@fig(11025)
def f11025():
    f, ax = canvas(6.4, 4.0, (0, 12.8), (0, 8))
    ax.add_patch(Rectangle((0.3, 0.3), 12.2, 7.4, fc='#fff1f0', ec=RED, lw=2.2))
    lines = ['謹詹於民國一一六年一月九日', '為長男 志明 與 林府千金 雅婷',
             '舉行結婚典禮 敬備喜筵', '恭候  光臨']
    for i, s in enumerate(lines):
        t(ax, 1.0, 6.7 - i * 1.05, s, fs=16, va='center', color='#7a1f1a')
    t(ax, 8.4, 2.45, '陳國華 謹訂', fs=16, va='center', color='#7a1f1a')
    t(ax, 1.0, 1.1, '席設：青禾飯店二樓（中午十二時入席）', fs=14, va='center', color='#7a1f1a')
    save(f, 11025)


# 11026 書信用語表
@fig(11026)
def f11026():
    table_fig(11026, ['收信人', '提稱語', '結尾敬辭'],
              [['祖父母', '膝下', '敬請 福安'], ['老師', '道鑒', '敬請 教安'],
               ['同學', '大鑒', '祝 學安'], ['弟弟', '如晤', '敬請 福安']],
              [2.4, 2.4, 3.2], title_s='小芳的書信用語表', w=5.6, h=3.8)


# 11027 春聯
@fig(11027)
def f11027():
    f, ax = canvas(6.0, 4.4, (0, 12), (0, 8.8))
    # 門
    ax.add_patch(Rectangle((3.6, 0.2), 4.8, 6.6, fc='#e9dcc6', ec=INK, lw=1.6))
    ax.plot([6.0, 6.0], [0.2, 6.8], color=INK, lw=1.4)
    for x in (5.6, 6.4):
        ax.add_patch(plt.Circle((x, 3.4), 0.15, fc=INK))
    # 橫批
    ax.add_patch(Rectangle((3.9, 7.0), 4.2, 1.2, fc='#f6c9c5', ec=RED, lw=1.6))
    t(ax, 6.0, 7.6, '?', fs=22, ha='center', va='center', color=RED)
    # 右聯(面對大門的右側)、左聯
    for x, s in [(9.4, '春回大地千山秀'), (2.6, '日暖神州萬物榮')]:
        ax.add_patch(Rectangle((x - 0.6, 0.4), 1.2, 6.4, fc='#f6c9c5', ec=RED, lw=1.6))
        vtext(ax, x, 6.25, s, fs=17, gap=0.86)
    save(f, 11027)


# 11028 颱風構造示意
@fig(11028)
def f11028():
    f, ax = canvas(6.6, 4.2, (-5.6, 7.6), (-4.2, 4.2))
    th = np.linspace(0, 1.25 * np.pi, 200)
    for k in range(3):
        r = 1.1 + 2.3 * th / (1.25 * np.pi)
        a = k * 2 * np.pi / 3 - th
        ax.plot(r * np.cos(a), r * np.sin(a), color=BLUE, lw=2.4, alpha=0.75)
    ax.add_patch(plt.Circle((0, 0), 0.95, fc='#c7d6ee', ec=INK, lw=2.2))
    ax.add_patch(plt.Circle((0, 0), 0.45, fc='white', ec=INK, lw=1.4))
    # 旋轉方向箭頭(逆時針)
    ax.annotate('', xy=(-3.3, 1.6), xytext=(-2.4, 3.0),
                arrowprops=dict(arrowstyle='-|>', color=RED, lw=2, mutation_scale=18,
                                connectionstyle='arc3,rad=0.25'))
    t(ax, -5.5, 3.6, '北半球：逆時針旋轉', fs=14, color=RED, va='center')
    # 標註
    for (x0, y0), (x1, y1), s in [((0.25, 0.1), (4.3, 2.9), '颱風眼：風小、少雲'),
                                   ((0.85, -0.3), (4.3, 0.6), '眼牆：風雨最強'),
                                   ((2.6, -1.4), (4.3, -2.0), '螺旋雨帶：\n外圍陣雨')]:
        ax.plot([x0, x1 - 0.1], [y0, y1], color=INK, lw=1.2)
        t(ax, x1, y1, s, fs=14, va='center', linespacing=1.2,
          bbox=dict(fc='white', ec='none', pad=1))
    save(f, 11028)


# 11029 茶的發酵程度
@fig(11029)
def f11029():
    f, ax = canvas(6.8, 3.0, (0, 13.6), (0, 6))
    t(ax, 6.8, 5.5, '臺灣常見茶類的發酵程度', fs=17, ha='center', va='center')
    ax.annotate('', xy=(13.2, 3.2), xytext=(0.4, 3.2),
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=2, mutation_scale=18))
    t(ax, 0.4, 4.2, '發酵程度 低', fs=13, va='center', color=GREY)
    t(ax, 13.2, 4.2, '高', fs=13, va='center', ha='right', color=GREY)
    teas = [('綠茶', '不發酵'), ('包種茶', '輕發酵'), ('凍頂\n烏龍茶', '中發酵'), ('東方\n美人茶', '重發酵'),
            ('紅茶', '全發酵')]
    xs = np.linspace(1.3, 12.0, 5)
    for x, (n, d) in zip(xs, teas):
        ax.plot([x], [3.2], 'o', ms=10, color=BLUE)
        t(ax, x, 1.6, n, fs=15, ha='center', va='center', linespacing=1.15)
        t(ax, x, 0.35, d, fs=13, ha='center', va='center', color=BLUE)
    save(f, 11029)


# 11030 蜜蜂搖擺舞
@fig(11030)
def f11030():
    f, ax = canvas(6.8, 3.8, (0, 13.6), (0, 7.6))
    # 左:蜂巢外(俯視)
    t(ax, 3.3, 7.15, '蜂巢外（由上往下看）', fs=14, ha='center', va='center')
    hive = (3.3, 1.2)
    ax.add_patch(plt.Circle(hive, 0.45, fc='#f2d48a', ec=INK, lw=1.4))
    t(ax, 3.3, 0.35, '蜂巢', fs=13, ha='center', va='center')
    ax.add_patch(plt.Circle((3.3, 6.1), 0.42, fc='#ffd75e', ec=RED, lw=1.4))
    t(ax, 3.85, 6.1, '太陽', fs=13, va='center', color=RED)
    ax.plot([3.3, 3.3], [1.7, 5.6], color=RED, ls='--', lw=1.4)
    a = np.radians(60)
    fx, fy = 3.3 + 3.1 * np.sin(a), 1.2 + 3.1 * np.cos(a)
    arrow(ax, (3.3 + 0.45 * np.sin(a), 1.2 + 0.45 * np.cos(a)), (fx - 0.3 * np.sin(a), fy - 0.3 * np.cos(a)), color=BLUE)
    t(ax, fx - 0.2, fy + 0.45, '食物', fs=14, color=BLUE, va='center', ha='center')
    arc(ax, 3.3, 1.2, 1.4, 30, 90, color=INK)
    t(ax, 3.75, 2.95, '60°', fs=13, va='center')
    ax.plot([6.8, 6.8], [0.3, 7.3], color=GREY, lw=1.2, ls=':')
    # 右:巢片上(垂直)
    t(ax, 10.2, 7.15, '巢片上（垂直）的搖擺舞', fs=14, ha='center', va='center')
    ax.add_patch(Rectangle((7.6, 0.4), 5.2, 6.1, fc='#fbf1d4', ec=INK, lw=1.4))
    c = (10.2, 2.0)
    ax.plot([10.2, 10.2], [2.0, 5.9], color=RED, ls='--', lw=1.4)
    t(ax, 10.35, 6.15, '正上方', fs=13, color=RED, va='center')
    arrow(ax, c, (10.2 + 2.6 * np.sin(a), 2.0 + 2.6 * np.cos(a)), color=BLUE, lw=2.2)
    arc(ax, 10.2, 2.0, 1.3, 30, 90, color=INK)
    t(ax, 10.6, 3.65, '60°', fs=13, va='center')
    t(ax, 10.2, 1.0, '搖擺前進方向', fs=13, ha='center', va='center', color=BLUE)
    save(f, 11030)


# 11031 植物園導覽圖
@fig(11031)
def f11031():
    f, ax = canvas(6.4, 4.2, (0, 12.8), (0, 8.4))
    ax.add_patch(Rectangle((0.4, 0.6), 10.0, 7.4, fc='#f2f7ec', ec=INK, lw=1.8))
    box(ax, 5.4, 6.7, 3.0, 1.1, '溫室', fs=15, fc='white')
    ax.add_patch(plt.matplotlib.patches.Ellipse((5.4, 4.2), 3.2, 1.8, fc='#cfe0f5', ec=BLUE, lw=1.5))
    t(ax, 5.4, 4.2, '荷花池', fs=15, ha='center', va='center')
    box(ax, 1.9, 4.2, 2.2, 1.2, '香草園', fs=15, fc='white')
    box(ax, 8.9, 4.2, 2.2, 1.2, '蕨類區', fs=15, fc='white')
    box(ax, 8.9, 6.9, 2.2, 1.0, '咖啡屋', fs=15, fc='white')
    ax.plot([4.6, 6.2], [0.6, 0.6], color='white', lw=4)
    t(ax, 5.4, 0.25, '入口', fs=15, ha='center', va='center', color=RED)
    ax.plot([5.4, 5.4], [0.8, 3.2], color=GREY, lw=2, ls=':')
    # 指北針
    arrow(ax, (11.7, 5.4), (11.7, 7.3))
    t(ax, 11.7, 7.8, '北', fs=15, ha='center', va='center')
    save(f, 11031)


# 11032 停水公告
@fig(11032)
def f11032():
    f, ax = canvas(6.4, 3.8, (0, 12.8), (0, 7.6))
    ax.add_patch(Rectangle((0.2, 0.2), 12.4, 7.2, fc='white', ec=BLUE, lw=2))
    t(ax, 6.4, 6.65, '停水公告', fs=20, ha='center', va='center', color=BLUE)
    t(ax, 0.7, 5.45, '因自來水管線工程，下列地區將暫停供水：', fs=15, va='center')
    t(ax, 0.7, 4.2, '停水時間：12月5日晚上10點', fs=16, va='center')
    t(ax, 3.1, 3.3, '至12月6日上午6點', fs=16, va='center')
    t(ax, 0.7, 2.1, '停水範圍：和平里、光明里', fs=16, va='center')
    t(ax, 0.7, 0.95, '請民眾事先儲水備用。', fs=15, va='center', color=RED)
    save(f, 11032)


# 11033 複習方法與記憶保留率
@fig(11033)
def f11033():
    f, ax = chart()
    cats = ['只讀一遍', '畫重點', '自我測驗', '教給別人']
    vals = [20, 25, 55, 60]
    ax.bar(cats, vals, color=BLUE, width=0.55)
    for i, v in enumerate(vals):
        t(ax, i, v + 1.2, f'{v}%', fs=14, ha='center', va='bottom')
    ax.set_ylim(0, 72); ax.set_ylabel('一週後記得的比例', fontproperties=P(13))
    title(ax, '不同複習方法一週後的記憶保留率（示意）', fs=15)
    style(ax)
    save(f, 11033)


# 11034 老街大事記
@fig(11034)
def f11034():
    f, ax = canvas(6.8, 3.6, (0, 13.6), (0, 7.2))
    t(ax, 6.8, 6.75, '青禾老街大事記', fs=17, ha='center', va='center')
    ax.plot([0.5, 13.1], [3.6, 3.6], color=INK, lw=2)
    ev = [(1920, '興建老街\n市場'), (1960, '鐵路設站，\n老街繁榮'), (1985, '新公路開通，\n商家外移'),
          (2008, '居民整修\n老屋'), (2015, '開辦文化節，\n遊客回流')]
    xs = np.linspace(1.4, 12.2, len(ev))
    for i, (x, (y, s)) in enumerate(zip(xs, ev)):
        ax.plot([x], [3.6], 'o', ms=8, color=BLUE)
        up = i % 2 == 0
        t(ax, x, 3.6 + (0.5 if up else -0.5), str(y), fs=14, ha='center', va='bottom' if up else 'top', color=BLUE)
        t(ax, x, 1.75 if up else 5.45, s, fs=14, ha='center', va='center', linespacing=1.3)
    save(f, 11034)


# 11035 延長午休意見調查
@fig(11035)
def f11035():
    f, ax = chart(6.8, 3.8)
    grades = ['九年級', '八年級', '七年級']
    data = np.array([[10, 25, 40, 25], [20, 35, 30, 15], [30, 40, 20, 10]])
    labs = ['非常同意', '同意', '不同意', '非常不同意']
    cols = ['#2a5fb4', '#9db7e0', '#f2b8b3', '#d0342c']
    tcol = ['white', INK, INK, 'white']
    left = np.zeros(3)
    for j in range(4):
        ax.barh(grades, data[:, j], left=left, color=cols[j], height=0.6, label=labs[j], edgecolor='white')
        for i in range(3):
            t(ax, left[i] + data[i, j] / 2, i, f'{data[i, j]}%', fs=13, ha='center', va='center', color=tcol[j])
        left += data[:, j]
    ax.set_xlim(0, 100); ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.legend(prop=P(13), frameon=False, ncol=4, loc='upper center', bbox_to_anchor=(0.45, 1.2),
              handlelength=1.0, columnspacing=0.8)
    title(ax, '「延長午休」意見調查（各年級各200人）', fs=15, y=1.2)
    style(ax, 14)
    save(f, 11035)


# 11036 合作社海報(標題空白)
@fig(11036)
def f11036():
    f, ax = canvas(6.0, 4.0, (0, 10), (0, 6.7))
    ax.add_patch(FancyBboxPatch((0.3, 0.3), 9.4, 6.1, boxstyle='round,pad=0,rounding_size=0.3',
                                fc='#f1f8ee', ec='#4c8c4a', lw=2))
    box(ax, 5, 5.5, 6.0, 1.0, '【  ？  】', fs=19, fc='white', ec='#4c8c4a')
    items = ['自備杯子，飲料店折5元', '自助餐提供環保碗借用', '集滿10點，換棉布購物袋']
    for i, s in enumerate(items):
        y = 4.0 - i * 1.15
        ax.plot([1.3], [y], 'o', ms=8, color='#4c8c4a')
        t(ax, 1.8, y, s, fs=17, va='center')
    t(ax, 9.3, 0.7, '學校合作社', fs=13, ha='right', va='center', color=GREY)
    save(f, 11036)


# 11037 公車時刻表
@fig(11037)
def f11037():
    table_fig(11037, ['路線', '青禾車站發車時間', '到博物館車程'],
              [['1號', '8:00、8:30、9:00、9:30', '40分鐘'], ['7號', '8:15、8:45、9:15、9:45', '25分鐘']],
              [1.4, 5.0, 2.6], title_s='往博物館公車時刻表', w=6.6, h=2.8, rowh=1.1, fs=15)


# 11038 截斷縱軸的長條圖
@fig(11038)
def f11038():
    f, ax = chart(5.6, 4.0)
    ax.bar(['甲班', '乙班'], [92, 95], color=BLUE, width=0.5)
    ax.set_ylim(90, 96); ax.set_yticks([90, 91, 92, 93, 94, 95, 96])
    ax.set_ylabel('平均分數', fontproperties=P(14))
    title(ax, '兩班國文段考平均分數')
    style(ax)
    save(f, 11038)


# 11039 最主要資訊來源
@fig(11039)
def f11039():
    f, ax = chart(6.6, 4.0)
    cats = ['電視', '網路影音', '社群媒體', '報紙']
    a = [40, 25, 20, 15]; b = [20, 45, 25, 10]
    x = np.arange(4)
    ax.bar(x - 0.19, a, 0.38, color='#c9c9c9', edgecolor=GREY, label='2020年')
    ax.bar(x + 0.19, b, 0.38, color=BLUE, label='2025年')
    for i in range(4):
        t(ax, x[i] - 0.19, a[i] + 0.8, f'{a[i]}%', fs=12.5, ha='center', va='bottom')
        t(ax, x[i] + 0.19, b[i] + 0.8, f'{b[i]}%', fs=12.5, ha='center', va='bottom')
    ax.set_xticks(x); ax.set_xticklabels(cats)
    ax.set_ylim(0, 55); ax.set_ylabel('百分比', fontproperties=P(13))
    ax.legend(prop=P(13), frameon=False, loc='upper right')
    title(ax, '學生「最主要資訊來源」調查', fs=15)
    style(ax)
    save(f, 11039)
