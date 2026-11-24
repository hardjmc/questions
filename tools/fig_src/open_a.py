from fig_all import *


def axes_style(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_linewidth(1.3)
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontproperties(PF); lab.set_fontsize(12)


@fig(39010)
def f39010():
    f, ax = plt.subplots(figsize=(6, 3.6), dpi=200)
    ax.plot([0, 8], [120, 0], color=BLUE, lw=2)
    ax.set_xlim(0, 10); ax.set_ylim(0, 150)
    ax.set_xticks(range(0, 11, 2)); ax.set_yticks([0, 40, 80, 120])
    ax.grid(True, color='#dddddd', lw=0.8)
    dot(ax, 0, 120, '(0, 120)', dx=0.25, dy=4, color=INK)
    dot(ax, 8, 0, '(8, 0)', dx=0.2, dy=6, color=INK)
    ax.set_xlabel('x(分鐘)', fontproperties=PF, fontsize=12, loc='right')
    txt(ax, 0.2, 140, 'y(公升)', fs=12)
    axes_style(ax)
    save(f, 39010)


@fig(39011)
def f39011():
    f, ax = plt.subplots(figsize=(6, 3.6), dpi=200)
    ax.plot([0, 60], [0, 4], color=BLUE, lw=2)
    ax.plot([20, 40], [0, 4], color=RED, lw=2)
    ax.set_xlim(0, 70); ax.set_ylim(0, 4.8)
    ax.set_xticks(range(0, 71, 10)); ax.set_yticks(range(0, 5))
    ax.grid(True, color='#dddddd', lw=0.8)
    dot(ax, 60, 4, '(60, 4)', dx=1, dy=0.12)
    dot(ax, 40, 4, '(40, 4)', dx=-11, dy=0.15)
    dot(ax, 20, 0, '(20, 0)', dx=-12, dy=0.15)
    txt(ax, 46, 2.3, '哥哥', color=BLUE, fs=13)
    txt(ax, 33, 3.3, '弟弟', color=RED, fs=13)
    ax.set_xlabel('x(分鐘)', fontproperties=PF, fontsize=12, loc='right')
    txt(ax, 1, 4.6, 'y(公里)', fs=12)
    axes_style(ax)
    save(f, 39011)


@fig(39018)
def f39018():
    f, ax = plt.subplots(figsize=(6, 3.6), dpi=200)
    cnt = [6, 12, 10, 8, 4]
    for i, c in enumerate(cnt):
        ax.bar(i * 10 + 5, c, width=10, color='#cfe0f5', edgecolor=BLUE, lw=1.4)
    ax.set_xlim(0, 55); ax.set_ylim(0, 14)
    ax.set_xticks(range(0, 51, 10)); ax.set_yticks(range(0, 15, 2))
    ax.grid(True, axis='y', color='#dddddd', lw=0.8); ax.set_axisbelow(True)
    ax.set_xlabel('通勤時間(分鐘)', fontproperties=PF, fontsize=12, loc='right')
    ax.set_ylabel('人數(人)', fontproperties=PF, fontsize=12, loc='top')
    axes_style(ax)
    save(f, 39018)


@fig(39020)
def f39020():
    f, ax = plt.subplots(figsize=(6, 3.6), dpi=200)
    xs = [60, 80, 100, 120, 140, 160]; ys = [0, 10, 30, 64, 90, 100]
    ax.plot(xs, ys, color=BLUE, lw=2, marker='o', ms=5)
    for x, y in zip(xs[1:], ys[1:]):
        txt(ax, x - 9, y + 3, f'{y}%', fs=12)
    ax.set_xlim(55, 165); ax.set_ylim(0, 112)
    ax.set_xticks(xs); ax.set_yticks(range(0, 101, 20))
    ax.set_yticklabels([f'{v}%' for v in range(0, 101, 20)])
    ax.grid(True, color='#dddddd', lw=0.8)
    ax.set_xlabel('跳繩次數(次)', fontproperties=PF, fontsize=12, loc='right')
    ax.set_ylabel('累積相對次數', fontproperties=PF, fontsize=12, loc='top')
    axes_style(ax)
    save(f, 39020)


@fig(39024)
def f39024():
    f, ax = new_ax(6, 3.6)
    x = np.linspace(-4, 4, 200)
    ax.plot(x, -x ** 2 / 4 + 4, color=INK, lw=2)
    ax.plot([-5.2, 5.4], [0, 0], color=INK, lw=1.3)
    ax.plot([0, 0], [-0.3, 5.0], color=INK, lw=1.3)
    ax.annotate('', xy=(5.6, 0), xytext=(5.2, 0), arrowprops=dict(arrowstyle='->', color=INK, lw=1.3))
    ax.annotate('', xy=(0, 5.2), xytext=(0, 4.9), arrowprops=dict(arrowstyle='->', color=INK, lw=1.3))
    txt(ax, 5.7, -0.1, 'x', fs=13); txt(ax, 0.15, 5.1, 'y', fs=13)
    txt(ax, 0.15, -0.45, 'O', fs=13)
    # 寬 8
    ax.annotate('', xy=(-4, -0.9), xytext=(4, -0.9), arrowprops=dict(arrowstyle='<->', color=RED, lw=1.3))
    txt(ax, -0.5, -1.45, '8 公尺', color=RED, fs=12)
    # 高 4
    ax.plot([0.0, -5.0], [4, 4], color=GREY, lw=1, ls='--')
    ax.annotate('', xy=(-4.8, 0), xytext=(-4.8, 4), arrowprops=dict(arrowstyle='<->', color=RED, lw=1.3))
    txt(ax, -6.6, 1.9, '4 公尺', color=RED, fs=12)
    txt(ax, -4.35, -0.55, '−4', fs=12); txt(ax, 3.85, -0.55, '4', fs=12)
    ax.set_xlim(-6.8, 6.2); ax.set_ylim(-1.7, 5.5)
    save(f, 39024)


@fig(39026)
def f39026():
    f, ax = plt.subplots(figsize=(6, 3.2), dpi=200)
    data = {'甲班': (40, 58, 70, 82, 96, 2), '乙班': (30, 62, 74, 80, 92, 1)}
    for name, (mn, q1, md, q3, mx, y) in data.items():
        ax.plot([mn, q1], [y, y], color=INK, lw=1.5); ax.plot([q3, mx], [y, y], color=INK, lw=1.5)
        ax.plot([mn, mn], [y - .15, y + .15], color=INK, lw=1.5); ax.plot([mx, mx], [y - .15, y + .15], color=INK, lw=1.5)
        ax.add_patch(Rectangle((q1, y - .3), q3 - q1, .6, fc='white', ec=BLUE, lw=1.6, zorder=3))
        ax.plot([md, md], [y - .3, y + .3], color=RED, lw=1.8, zorder=4)
    ax.set_yticks([1, 2]); ax.set_yticklabels(['乙班', '甲班'])
    ax.set_xlim(25, 100); ax.set_ylim(0.4, 2.6)
    ax.set_xticks(range(30, 101, 10)); ax.set_xticks(range(25, 101, 2), minor=True)
    ax.grid(True, axis='x', which='major', color='#dddddd', lw=0.8)
    ax.set_xlabel('成績(分)', fontproperties=PF, fontsize=12, loc='right')
    axes_style(ax); ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    save(f, 39026)
