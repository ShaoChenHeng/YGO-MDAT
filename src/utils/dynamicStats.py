import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
from abc import ABC, abstractmethod

class BasePlotter(ABC):
    """图表绘制基类"""
    def __init__(self, stats_data, colors, markers):
        self.stats = stats_data
        self.colors = colors
        self.markers = markers
        self.x = [i['total_matches'] for i in self.stats['interval_stats']]


        # 配置中文字体
        plt.rcParams['font.sans-serif'] = ['LXGW WenKai']

    def showx(self):
        print(self.x)

    @abstractmethod
    def _get_plot_data(self):
        """子类需实现的数据提取方法"""
        pass

    @abstractmethod
    def _setup_axes(self, ax):
        """子类需实现的坐标轴设置"""
        pass

    def _add_baseline(self, ax):
        """添加基准线"""
        ax.axhline(y=50, color='red', linestyle='--', alpha=0.7, linewidth=1)

    def _set_dynamic_ylim(self, ax, data_series):
        """动态设置Y轴范围"""
        all_values = sum(data_series, [])  # 展开多维列表
        safe_min = min(min(all_values), 50)
        safe_max = max(max(all_values), 50)
        ax.set_ylim(
            max(safe_min-10, 0),
            min(safe_max+10, 100)
        )

    def plot(self, ax):
        """主绘制方法"""
        plot_data = self._get_plot_data()

        # 绘制各条折线
        for (label, data), color, marker in zip(plot_data, self.colors, self.markers):
            ax.plot(self.x, data, marker=marker, color=color, label=label)

        # 配置坐标轴
        self._setup_axes(ax)
        self._add_baseline(ax)

        # 设置动态范围
        self._set_dynamic_ylim(ax, [d[1] for d in plot_data])

        ax.grid(True, alpha=0.3)
        ax.legend()

class CoreStatsPlotter(BasePlotter):
    """核心统计图表"""
    def _get_plot_data(self):
        return [
            ('对局胜率', [i['win_rate'] for i in self.stats['interval_stats']]),
            ('硬币胜率', [i['coin_win_rate'] for i in self.stats['interval_stats']])
        ]

    def _setup_axes(self, ax):
        ax.set_title('核心胜率趋势')
        ax.set_ylabel('百分比 (%)')

class MoveStatsPlotter(BasePlotter):
    """先后手统计图表"""
    def _get_plot_data(self):
        return [
            ('先手率', [i['first_move_rate'] for i in self.stats['interval_stats']]),
            ('先手胜率', [i['first_move_win_rate'] for i in self.stats['interval_stats']]),
            ('后手胜率', [i['second_move_win_rate'] for i in self.stats['interval_stats']])
        ]

    def _setup_axes(self, ax):
        ax.set_title('先后手表现')
        ax.set_ylabel('百分比 (%)')

class CoinStatsPlotter(BasePlotter):
    """硬币关联统计图表"""
    def _get_plot_data(self):
        return [
            ('赢硬币胜率', [i['win_coin_win_rate'] for i in self.stats['interval_stats']]),
            ('输硬币胜率', [i['lose_coin_win_rate'] for i in self.stats['interval_stats']])
        ]

    def _setup_axes(self, ax):
        ax.set_title('硬币胜负关联胜率')
        ax.set_xlabel('对局数')
        ax.set_ylabel('百分比 (%)')

def show_plot_analysis(stats):
    # 初始化图表
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(3, 1, height_ratios=[1, 1, 1])

    # 配置各图表参数
    chart_configs = [
        (CoreStatsPlotter, {'colors': ['#ff6188', '#78dce8'], 'markers': ['o', 's']}),
        (MoveStatsPlotter, {'colors': ['#bda4ea', '#ffd866', '#a9dc76'], 'markers': ['^', '*', 'x']}),
        (CoinStatsPlotter, {'colors': ['#fc9867', '#2b9692'], 'markers': ['D', 'v']})
    ]

    # 逐个绘制子图
    for idx, (plotter_cls, style) in enumerate(chart_configs):
        ax = fig.add_subplot(gs[idx])
        plotter = plotter_cls(stats, **style)
        plotter.plot(ax)

    plt.tight_layout()
    plt.show()

def save_plot_analysis(stats, filename):
    # 初始化图表
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(3, 1, height_ratios=[1, 1, 1])

    # 配置各图表参数
    chart_configs = [
        (CoreStatsPlotter, {'colors': ['#ff6188', '#78dce8'], 'markers': ['o', 's']}),
        (MoveStatsPlotter, {'colors': ['#bda4ea', '#ffd866', '#a9dc76'], 'markers': ['^', '*', 'x']}),
        (CoinStatsPlotter, {'colors': ['#fc9867', '#2b9692'], 'markers': ['D', 'v']})
    ]

    # 逐个绘制子图
    for idx, (plotter_cls, style) in enumerate(chart_configs):
        ax = fig.add_subplot(gs[idx])
        plotter = plotter_cls(stats, **style)
        plotter.plot(ax)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
