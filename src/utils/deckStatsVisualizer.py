import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

class DeckStatsVisualizer:
    def __init__(self, stats_data, season_num=None, figsize=(14, 8)):
        rcParams['font.sans-serif'] = ['LXGW WenKai']

        self.decks = list(stats_data.keys())
        self.data = stats_data
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self._setup_chart(season_num)

    def _setup_chart(self, season_num):
        # 主标题
        title = "卡组使用统计" + (f" (赛季 {season_num})" if season_num else "")
        self.fig.suptitle(title, fontsize=16)

        # 绘制四组数据

        self._plot_bars()
        self._add_labels()
        self._style_axes()
        self.add_avg_line()

    def add_avg_line(self, yvalue=50, color='#FF4500'):  # 改为更醒目的橙红色
        """添加基准参考线"""
        self.ax2.axhline(yvalue, color=color, linestyle='--', alpha=0.5, lw=1.5)

        # 在右侧添加标签
        x_max = self.ax2.get_xlim()[1]  # 获取X轴最大值
        self.ax2.text(x_max + 0.2,  # X轴最右侧偏移
                    yvalue,
                    f' {yvalue}% 基准线',
                    color=color,
                    va='center',
                    ha='right',  # 右对齐
                    fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    def _plot_bars(self):
        # X轴位置
        x = np.arange(len(self.decks))
        bar_width = 0.18  # 调小宽度适应四个柱状图

        # 主柱状图（使用次数）
        self.ax.bar(x - 0.27, [d['total'] for d in self.data.values()],
                   width=bar_width, label='总对局', color='#78dce8')

        # 次级柱状图（胜利次数）
        self.ax.bar(x - 0.09, [d['wins'] for d in self.data.values()],
                   width=bar_width, label='胜利次数', color='#a9dc76')

        # 双Y轴柱状图（胜率）
        self.ax2 = self.ax.twinx()
        self.ax2.bar(x + 0.09, [d['win_rate'] for d in self.data.values()],
                     width=bar_width, label='总胜率',
                     color='#ffd866',
                     alpha=0.9,
                     edgecolor='#817c6e',
                     hatch='/',
                     )
        self.ax2.bar(x + 0.27, [d['coin_win_rate'] for d in self.data.values()],
                     width=bar_width, label='硬币胜率',
                     color='#FF6B6B',
                     alpha=0.9,
                     edgecolor='#817c6e',
                     hatch='/'
                     )

    def _add_labels(self):
        # 添加所有柱状图数值标签
        for i, deck in enumerate(self.decks):
            # 主Y轴标签
            self.ax.text(i - 0.27, self.data[deck]['total'] + 1,
                         self.data[deck]['total'], ha='center', fontsize=9)
            self.ax.text(i - 0.09, self.data[deck]['wins'] + 1,
                         self.data[deck]['wins'], ha='center', fontsize=9)

            # 次Y轴标签
            self.ax2.text(i + 0.09, self.data[deck]['win_rate'] + 1.5,
                          f"{self.data[deck]['win_rate']}%",
                          ha='center',
                          fontsize=9,
                          color='#4d4d4d')  # 深灰色

            self.ax2.text(i + 0.27, self.data[deck]['coin_win_rate'] + 1.5,
                          f"{self.data[deck]['coin_win_rate']}%",
                          ha='center',
                          fontsize=9,
                          color='#4d4d4d')

    def _style_axes(self):
        # 主Y轴范围调整
        max_total = max(d['total'] for d in self.data.values())
        self.ax.set_ylim(0, max_total * 1.15)  # 留出标签空间

        # 次Y轴保持0-100范围
        self.ax2.set_ylim(0, 100)

        # 主Y轴设置
        self.ax.set_ylabel('对局次数', fontsize=12)
        self.ax.set_xticks(np.arange(len(self.decks)))
        self.ax.set_xticklabels(self.decks,
                                rotation=0,
                                ha='right',
                                fontsize=12)

        self.ax.grid(axis='y', linestyle='--', alpha=0.7)

        # 双Y轴设置
        self.ax2.set_ylabel('胜率 (%)', fontsize=12)
        self.ax2.set_ylim(0, 100)

        # 合并图例
        lines, labels = self.ax.get_legend_handles_labels()
        lines2, labels2 = self.ax2.get_legend_handles_labels()
        self.ax.legend(lines + lines2, labels + labels2, loc='upper left')

    def show(self):
        plt.tight_layout()
        plt.show()

    def save(self, filename):
        plt.tight_layout()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
