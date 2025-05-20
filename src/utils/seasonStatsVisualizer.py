import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

class SeasonStatsVisualizer:
    def __init__(self, stats, season_num=18):
        plt.rcParams['font.sans-serif'] = ['LXGW WenKai']
        self.stats = stats
        self.season_num = season_num
        self.mid_stats = stats['middle_stats'][0] if stats['middle_stats'] else None
        self.fig = plt.figure(figsize=(12, 8), dpi=120)
        self.gs = GridSpec(3, 2, figure=self.fig, height_ratios=[0.8, 2, 0.7])

        self.create_main_table()
        self.create_comparison_chart()
        self.create_test_table()
        self.create_mid_test_table()


    def create_main_table(self):
        ax = self.fig.add_subplot(self.gs[0, :])
        ax.axis('off')

        # 主数据表格
        columns = [
            '进度','总对局数', '先手次数', '硬币胜场', '胜率', '硬币胜率',
            '先手率', '先手胜率', '后手胜率', '赢硬币胜率', '输硬币胜率'
        ]

        # 构建行数据
        full_season_row = [
            '全赛季',
            self.stats['total_matches'],
            self.stats['first_moves'],
            self.stats['coin_wins'],
            f"{self.stats['win_rate']}%",
            f"{self.stats['coin_win_rate']}%",
            f"{self.stats['first_move_rate']}%",
            f"{self.stats['first_move_win_rate']}%",
            f"{self.stats['second_move_win_rate']}%",
            f"{self.stats['win_coin_win_rate']}%",
            f"{self.stats['lose_coin_win_rate']}%"
        ]

        mid_season_row = [
            '中期',
            self.mid_stats.get('total_matches', ''),
            self.mid_stats.get('first_moves', ''),
            self.mid_stats.get('coin_wins', ''),
            self._fmt_rate(self.mid_stats, 'win_rate'),
            self._fmt_rate(self.mid_stats, 'coin_win_rate'),
            self._fmt_rate(self.mid_stats, 'first_move_rate'),
            self._fmt_rate(self.mid_stats, 'first_move_win_rate'),
            self._fmt_rate(self.mid_stats, 'second_move_win_rate'),
            self._fmt_rate(self.mid_stats, 'win_coin_win_rate'),
            self._fmt_rate(self.mid_stats, 'lose_coin_win_rate')
        ] if self.mid_stats else None

        cell_text = [mid_season_row]
        cell_text.append(full_season_row)

        table = ax.table(
            cellText=cell_text,
            colLabels=columns,
            loc='upper center',
            cellLoc='center',
            colColours=['#f0f0f0']*len(columns),
            bbox=[0, 0, 1, 1]
        )
        ax.set_title(f's{self.season_num}赛季数据', fontsize=12)

    def create_comparison_chart(self):
        ax = self.fig.add_subplot(self.gs[1, :])
        ax.margins(y=0.05)
        labels = ['胜率', '硬币胜率', '先手率', '先手胜率', '后手胜率', '赢硬币胜率', '输硬币胜率']
        full_season = [
            self.stats['win_rate'],
            self.stats['coin_win_rate'],
            self.stats['first_move_rate'],
            self.stats['first_move_win_rate'],
            self.stats['second_move_win_rate'],
            self.stats['win_coin_win_rate'],
            self.stats['lose_coin_win_rate'],
        ]

        y_max = max(full_season) + 5
        ax.set_ylim(0, y_max * 1.3)  # 增加15%的空间


        if self.mid_stats:
            mid = [
                self.mid_stats['win_rate'],
                self.mid_stats['coin_win_rate'],
                self.mid_stats['first_move_rate'],
                self.mid_stats['first_move_win_rate'],
                self.mid_stats['second_move_win_rate'],
                self.mid_stats['win_coin_win_rate'],
                self.mid_stats['lose_coin_win_rate'],
            ]

            x = np.arange(len(labels))
            bars_mid = ax.bar(x - 0.2, mid, 0.4, label='中期', color='#a9dc76')
            bars_full = ax.bar(x + 0.2, full_season, 0.4, label='全赛季', color='#78dce8')

            # 在柱子上方添加数值标签
            for bar in bars_mid:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontsize=8)

                for bar in bars_full:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.1f}%',
                            ha='center', va='bottom', fontsize=8)

            ax.set_xticks(x)


        ax.set_xticklabels(labels, rotation=0)
        ax.set_title(f's{self.season_num}赛季数据对比', fontsize=12, pad=10)  # 添加标题
        ax.set_ylabel('百分比 (%)')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        ax.yaxis.set_major_locator(plt.MultipleLocator(15))  # 每15%一个主刻度


    def create_test_table(self):
        ax = self.fig.add_subplot(self.gs[2, 1])
        ax.axis('off')

        # 创建检验结果表格
        columns = ['检验类型', '统计量', 'P值', '结论']
        cell_text = [
            ['卡方检验',
             f"{self.stats['coin_fairness_test']['chi2_statistic']:.6f}",
             f"{self.stats['coin_fairness_test']['p_value']:.6f}",
             '符合公平' if self.stats['coin_fairness_test']['is_fair'] else '可能不公平'],
            ['二项检验',
             '-',
             f"{self.stats['binom_test']:.6f}",
             '符合公平' if self.stats['binom_test'] > 0.05 else '可能不公平']
        ]

        table = ax.table(cellText=cell_text,
                        colLabels=columns,
                        loc='upper center',
                        cellLoc='center',
                        colColours=['#f0f0f0']*len(columns),
                        colWidths=[0.25, 0.25, 0.25, 0.25])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        ax.set_title(f's{self.season_num}全赛季硬币公平性检验', fontsize=12)

    def create_mid_test_table(self):
        if not self.mid_stats:
            return

        ax = self.fig.add_subplot(self.gs[2, 0])
        ax.axis('off')

        # 创建中期检验结果表格
        columns = ['检验类型', '统计量', 'P值', '结论']
        cell_text = [
            ['卡方检验',
             f"{self.mid_stats['coin_fairness_test']['chi2_statistic']:.6f}",
             f"{self.mid_stats['coin_fairness_test']['p_value']:.6f}",
             '符合公平' if self.mid_stats['coin_fairness_test']['is_fair'] else '可能不公平'],
            ['二项检验',
             '-',
             f"{self.mid_stats['binom_test']:.6f}",
             '符合公平' if self.mid_stats['binom_test'] > 0.05 else '可能不公平']
        ]

        table = ax.table(cellText=cell_text,
                        colLabels=columns,
                        loc='upper center',
                        cellLoc='center',
                        colColours=['#f0f0f0']*len(columns),
                        colWidths=[0.25, 0.25, 0.25, 0.25])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        ax.set_title(f's{self.season_num}中期硬币公平性检验', fontsize=12)

    def _fmt_rate(self, data, key):
        return f"{data.get(key, '')}%" if data else ''

    def show(self):
        plt.tight_layout(pad=1.0, h_pad=1.0, w_pad=1.0)
        plt.show()

    def save(self, filename):
        plt.tight_layout(pad=1.0, h_pad=1.0, w_pad=1.0)
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

