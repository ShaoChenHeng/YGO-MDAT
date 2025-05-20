import matplotlib.pyplot as plt
from matplotlib import rcParams

class StreakVisualizer:
    def __init__(self, win_streaks, lose_streaks, season_num, figsize=(12, 6)):
        rcParams['font.sans-serif'] = ['LXGW WenKai']

        self.win_streaks = win_streaks
        self.lose_streaks = lose_streaks
        self.season_num = season_num

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=figsize)
        self._configure_figure()
        self._plot_streaks()

    def _configure_figure(self):
        self.fig.suptitle(f's{self.season_num}赛季硬币连续情况', fontsize=16)
        plt.tight_layout()

    def _plot_streaks(self):
        self._plot_single_streak(
            self.ax1,
            self.win_streaks,
            '#a9dc76',
            '硬币连续胜',
            '连胜长度'
        )

        self._plot_single_streak(
            self.ax2,
            self.lose_streaks,
            '#ff6188',
            '硬币连续负',  # 修正原代码中的标题错误
            '连负长度'
        )

    def _plot_single_streak(self, ax, data, color, title, ylabel):
        ax.bar(range(1, len(data)+1), data, color=color, alpha=0.7)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xticks(range(1, len(data)+1))  # 修正原代码的刻度偏移问题
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    def show(self):
        plt.show()

    def save(self, filename):
        self.fig.savefig(filename)
        plt.close()
