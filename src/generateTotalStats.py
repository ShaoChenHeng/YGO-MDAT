import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from utils.dynamicStats import *
from matplotlib import rcParams
import pandas as pd
from tabulate import tabulate
from matplotlib.ticker import MultipleLocator

rcParams['font.family'] = 'sans-serif'
rcParams['axes.unicode_minus'] = False
rcParams['font.sans-serif'] = ['LXGW WenKai']


def rate_calc(numerator, denominator):
    if denominator <= 0:
        return 0
    return (numerator / denominator) * 100

def individual_show_plot_analysis(total_stats):
    stats = total_stats['interval_stats']
    seasons = [s['season_num'] for s in stats]
    min_season = min(seasons)
    max_season = max(seasons)

    # 创建3行1列的子图布局
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 18))
    plt.subplots_adjust(
        hspace=0.8,
        top = 0.95,
        bottom=0.08
    )  # 调整子图间距

    # 第一行：核心胜率趋势
    ax1.plot(seasons, [s['win_rate'] for s in stats],
            marker='o', label='对局胜率', color='#ff6188')
    ax1.plot(seasons, [s['coin_win_rate'] for s in stats],
            marker='s', label='硬币胜率', color='#78dce8')

    ax1.vlines(x=18, ymin=35, ymax=89,
               colors='#898cb6', linewidth=1.5,
               linestyle=':', alpha=0.8)
    ax1.text(18.2, 88, '珠泪环境',
             rotation=0, va='top',
             color='#898cb6', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax1.vlines(x=21, ymin=35, ymax=89,
               colors='#ff90ab', linewidth=1.5,
               linestyle=':', alpha=0.8)
    ax1.text(21.2, 88, '皮尔莉环境',
             rotation=0, va='top',
             color='#ff90ab', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax1.vlines(x=23, ymin=35, ymax=89,
               colors='#d59156', linewidth=1.5,
               linestyle=':', alpha=0.8)
    ax1.text(23.2, 88, '百花齐放环境',
             rotation=0, va='top',
             color='#d59156', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax1.vlines(x=26, ymin=35, ymax=89,
               colors='purple', linewidth=1.5,
               linestyle=':', alpha=0.8)
    ax1.text(26.2, 88, '蛇眼环境',
             rotation=0, va='top',
             color='purple', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax1.vlines(x=31, ymin=35, ymax=89,
               colors='#957cc2', linewidth=1.5,
               linestyle=':', alpha=0.8)
    ax1.text(31.2, 88, '尤贝尔环境',
             rotation=0, va='top',
             color='#957cc2', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax1.vlines(x=34, ymin=35, ymax=89,
              colors='red', linewidth=1.5,
              linestyle=':', alpha=0.8)
    ax1.text(34.2, 88, '天杯龙环境',
            rotation=0, va='top',
            color='red', fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))


    ax1.vlines(x=38, ymin=35, ymax=89,
              colors='#577482', linewidth=1.5,
              linestyle=':', alpha=0.8)
    ax1.text(38.2, 88, '圣刻蛇环境',
            rotation=0, va='top',
            color='#577482', fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax1.vlines(x=40, ymin=35, ymax=89,
              colors='#9bd8f1', linewidth=1.5,
              linestyle=':', alpha=0.8)
    ax1.text(40.2, 88, '白龙环境',
            rotation=0, va='top',
            color='#9bd8f1', fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax1.hlines(y=50, xmin=min_season, xmax=max_season,
               colors='red', linestyles='--', alpha=0.7, zorder=0)
    ax1.set_title('核心胜率趋势', fontsize=12, pad=10)
    ax1.set_ylabel('百分比 (%)')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')

    # 第二行：先后手表现
    ax2.plot(seasons, [s['first_move_rate'] for s in stats],
            marker='^', label='先手率', color='#bda4ea')
    ax2.plot(seasons, [s['first_move_win_rate'] for s in stats],
            marker='d', label='先手胜率', color='#ffd866')
    ax2.plot(seasons, [s['second_move_win_rate'] for s in stats],
            marker='*', label='后手胜率', color='#a9dc76')
    ax2.hlines(y=50, xmin=min_season, xmax=max_season,
               colors='red', linestyles='--', alpha=0.7, zorder=0)
    ax2.set_title('先后手表现', fontsize=12, pad=10)
    ax2.set_ylabel('百分比 (%)')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper left')

    # 第三行：硬币关联胜率
    ax3.plot(seasons, [s['win_coin_win_rate'] for s in stats],
            marker='p', label='赢硬币胜率', color='#fc9867')
    ax3.plot(seasons, [s['lose_coin_win_rate'] for s in stats],
            marker='H', label='输硬币胜率', color='#2b9692')
    ax3.hlines(y=50, xmin=min_season, xmax=max_season,
               colors='red', linestyles='--', alpha=0.7, zorder=0)
    ax3.set_title('硬币胜负关联胜率', fontsize=12, pad=10)
    ax3.set_xlabel('赛季编号', labelpad=10)
    ax3.set_ylabel('百分比 (%)')
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='upper left')

    # 统一设置公共属性
    for ax in [ax1, ax2, ax3]:
        ax.set_ylim(35, 90)
        ax.set_xticks(seasons)
        ax.xaxis.set_tick_params(rotation=0)

        # y轴次要刻度配置
        ax.yaxis.set_minor_locator(MultipleLocator(5))

        ax.grid(which='minor', alpha=0.2, linestyle=':')

    # 保持原有主网格线设置
    ax.grid(True, alpha=0.3, which='major')

    plt.tight_layout()
    plt.savefig('season_trends.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

def generate_season_stats_table(interval_stats):
    # 创建DataFrame
    df = pd.DataFrame(interval_stats)

    # 设置赛季编号为索引
    df.set_index('season_num', inplace=True)

    # 定义要显示的列及其中文名称
    columns_map = {
        'total_matches': '总对局数',
        'wins': '胜场数',
        'win_rate': '胜率(%)',
        'coin_wins': '硬币胜场',
        'coin_win_rate': '硬币胜率(%)',
        'first_moves': '先手次数',
        'first_move_rate': '先手率(%)',
        'first_move_wins': '先手胜场',
        'first_move_win_rate': '先手胜率(%)',
        'second_move_wins': '后手胜场',
        'second_move_win_rate': '后手胜率(%)',
        'win_coin_wins': '赢硬币胜场',
        'win_coin_win_rate': '赢硬币胜率(%)',
        'lose_coin_wins': '输硬币胜场',
        'lose_coin_win_rate': '输硬币胜率(%)'
    }


    # 筛选并重命名列
    df = df[list(columns_map.keys())].rename(columns=columns_map)

    # 格式化输出
    print(tabulate(df, headers='keys', tablefmt='grid', floatfmt=".2f", showindex=True))

    # 可选：保存到CSV文件
    df.to_csv('season_stats.csv', encoding='utf-8-sig')

    return df

def generate_individual_season_stats_table(interval_stats):
        # 准备表头和数据
    headers = [
        "赛季", "总对局", "胜率%", "硬币胜率%",
        "先手率%", "先手胜率%", "后手胜率%",
        "赢硬币胜率%", "输硬币胜率%"
    ]

    # 构建数据行
    table_data = []

    for stats in interval_stats:
        row = [
            stats['season_num'],
            stats['total_matches'],
            f"{stats['win_rate']:.1f}",
            f"{stats['coin_win_rate']:.1f}",
            f"{stats['first_move_rate']:.1f}",
            f"{stats['first_move_win_rate']:.1f}",
            f"{stats['second_move_win_rate']:.1f}",
            f"{stats['win_coin_win_rate']:.1f}",
            f"{stats['lose_coin_win_rate']:.1f}"
        ]
        table_data.append(row)

    # 生成表格（使用网格样式）
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def strek_chart(streak_coin_win, streak_coin_lose):
    # 合并数据并转为 DataFrame
    df_win = pd.DataFrame({"连续次数": streak_coin_win, "类型": "连续正"})
    df_lose = pd.DataFrame({"连续次数": streak_coin_lose, "类型": "连续负"})
    df = pd.concat([df_win, df_lose])

    plt.figure(figsize=(10, 6))
    ax = sns.countplot(
        data=df,
        x="连续次数",
        hue="类型",
        palette={"连续正": "#a9dc76", "连续负": "#ff6188"},
        alpha=0.8,
    )

    # 计算 y 轴最大值（取最大出现次数 + 1）
    max_count = max(
        max(pd.Series(streak_coin_win).value_counts()),
        max(pd.Series(streak_coin_lose).value_counts()),
    )
    y_max = max_count + 1  # 稍微留一点空间

    # 设置 y 轴刻度（每 1 个单位一个刻度）
    plt.yticks(range(0, y_max, 5))  # 0, 1, 2, ..., y_max

    # 添加网格线（水平方向）
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.title("连续正/负数字出现次数对比")
    plt.xlabel("连续次数")
    plt.ylabel("出现次数")
    plt.legend()
    plt.show()

# 赛季独立胜率变化
def individual_season_stats():
    stats_dir = Path("~/yugioh-data/data/stats").expanduser()
    sorted_files = sorted(
        stats_dir.glob("s*_stats.json"),
        key=lambda x: int(x.stem.split("_")[0][1:])  # 提取s后的数字
    )
    interval_stats = []

    for json_file in sorted_files:
        # 从文件名解析赛季编号（如s39）
        season_name = json_file.stem.split('_')[0]  # 获取s39
        season_num = int(season_name[1:])  # 提取纯数字39
        print(season_num)
        # 读取数据
        with open(json_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)

            total_matches = stats['total_matches']
            win_rate = stats['win_rate']
            coin_win_rate = stats['coin_win_rate']
            first_move_rate = stats['first_move_rate']
            first_move_win_rate = stats['first_move_win_rate']
            second_move_win_rate = stats['second_move_win_rate']
            win_coin_win_rate = stats['win_coin_win_rate']
            lose_coin_win_rate = stats['lose_coin_win_rate']

            interval_stats.append({
                'season_num':season_num,
                'total_matches': total_matches,
                'win_rate': win_rate,
                'coin_win_rate': coin_win_rate,
                'first_move_rate': first_move_rate,
                'first_move_win_rate': first_move_win_rate,
                'second_move_win_rate': second_move_win_rate,
                'win_coin_win_rate': win_coin_win_rate,
                'lose_coin_win_rate': lose_coin_win_rate,
            })

    total_stats = {'interval_stats':interval_stats}
    # individual_show_plot_analysis(total_stats)
    generate_individual_season_stats_table(
        total_stats['interval_stats']
    )


def accumulate_season_stats():
    stats_dir = Path("~/yugioh-data/data/stats").expanduser()
    sorted_files = sorted(
        stats_dir.glob("s*_stats.json"),
        key=lambda x: int(x.stem.split("_")[0][1:])  # 提取s后的数字
    )

    wins = 0
    coin_wins = 0
    total_matches = 0
    first_moves = 0
    first_move_wins = 0
    second_move_wins = 0
    win_coin_wins = 0
    lose_coin_wins = 0

    streak_coin_win = []
    streak_coin_lose = []

    interval_stats = []

    for json_file in sorted_files:
        # 从文件名解析赛季编号（如s39）
        season_name = json_file.stem.split('_')[0]  # 获取s39
        season_num = int(season_name[1:])  # 提取纯数字39

        # 读取数据
        with open(json_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)

            wins += stats['wins']
            coin_wins += stats['coin_wins']
            total_matches += stats['total_matches']
            first_moves += stats['first_moves']
            first_move_wins += stats['first_move_wins']
            second_move_wins += stats['second_move_wins']
            win_coin_wins += stats['win_coin_wins']
            lose_coin_wins += stats['lose_coin_wins']

            streak_coin_win.extend(
                stats['coin_streaks']['streak_list']['win']
            )
            streak_coin_lose.extend(
                stats['coin_streaks']['streak_list']['lose']
            )

            win_rate = rate_calc(wins, total_matches)                    # 胜率
            coin_win_rate = rate_calc(coin_wins, total_matches)          # 硬币胜率
            first_move_rate = rate_calc(first_moves, total_matches)      # 先手率
            first_move_win_rate = rate_calc(first_move_wins, first_moves)# 先手胜率
            second_move_win_rate = rate_calc(second_move_wins,           # 后手胜率
                                             (total_matches - first_moves))
            win_coin_win_rate = rate_calc(win_coin_wins, coin_wins)      # 赢硬币胜率

            lose_coin_win_rate = rate_calc(lose_coin_wins,               # 输硬币胜率
                                           (total_matches - coin_wins))

            accumulate_stats = {
                'season_num':season_num,
                'total_matches': total_matches,
                'coin_wins': coin_wins,
                'wins': wins,
                'first_moves':first_moves,
                'total_matches': total_matches,
                'first_moves':first_moves,
                'first_move_wins':first_move_wins,
                'second_move_wins': second_move_wins,
                'win_coin_wins': win_coin_wins,
                'lose_coin_wins': lose_coin_wins,
                'win_rate': round(win_rate, 2),
                'coin_win_rate': round(coin_win_rate, 2),
                'first_move_rate': round(first_move_rate, 2),
                'first_move_win_rate': round(first_move_win_rate, 2),
                'second_move_win_rate': round(second_move_win_rate, 2),
                'win_coin_win_rate': round(win_coin_win_rate, 2),
                'lose_coin_win_rate': round(lose_coin_win_rate, 2),
            }
            # print(accumulate_stats)
            interval_stats.append(accumulate_stats)
    total_stats = {'interval_stats':interval_stats}

    # 生成所有赛季累积的各种胜率
    show_plot_analysis(total_stats)
    #strek_chart(streak_coin_win, streak_coin_lose)

        # 赛季表格
        # stats_table = generate_season_stats_table(
        #     total_stats['interval_stats']
        # )



if __name__ == "__main__":
    #accumulate_season_stats()
    individual_season_stats()
