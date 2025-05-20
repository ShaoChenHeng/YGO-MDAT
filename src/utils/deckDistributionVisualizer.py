import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

class DeckDistributionVisualizer:
    def __init__(self, deck_data, season_num=None, figsize=(10, 8)):
        rcParams['font.sans-serif'] = ['LXGW WenKai']

        self.decks = list(deck_data.keys())
        self.counts = list(deck_data.values())
        self.season_num = season_num

        self.fig, self.ax = plt.subplots(figsize=figsize)
        self._create_pie_chart()

    def _create_pie_chart(self):
        # 按值从大到小排序（保持原始顺序需先排序）
        sorted_pairs = sorted(zip(self.counts, self.decks), reverse=True)
        sorted_counts = [pair[0] for pair in sorted_pairs]
        sorted_decks = [pair[1] for pair in sorted_pairs]

        # 设置顺时针参数
        explode = [0.1] + [0]*(len(sorted_counts)-1)  # 突出最大值
        start_angle = 90  # 最大值从12点开始

        # 绘制饼图（关键参数调整）
        wedges, texts, autotexts = self.ax.pie(
            sorted_counts,
            explode=explode,
            labels=sorted_decks,  # 临时标签用于调试
            colors=plt.cm.Paired.colors,
            startangle=start_angle,
            autopct=lambda p: f'{p:.1f}%',
            pctdistance=0.75,
            counterclock=False  # 强制顺时针
        )

        # 修正图例顺序
        self.ax.legend(
            wedges,
            [f'{d} ({c}次)' for d, c in zip(sorted_decks, sorted_counts)],
            title="卡组分布",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        # 设置样式
        self.ax.axis('equal')  # 正圆形
        self.ax.set_title(
            f's{self.season_num}赛季天梯环境TOP10分布',
            fontsize=14,
            pad=20
        )


        # 调整百分比标签样式
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)

    def show(self):
        plt.tight_layout()
        plt.show()

    def save(self, filename):
        plt.tight_layout()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

