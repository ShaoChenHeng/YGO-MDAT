import os
import json
from pathlib import Path
from utils.deckDistributionVisualizer import DeckDistributionVisualizer
from utils.deckStatsVisualizer import DeckStatsVisualizer
from utils.seasonStatsVisualizer import SeasonStatsVisualizer
from utils.streakVisualizer import StreakVisualizer
from utils.dynamicStats import *

def show_streak(season_num, win_data, lose_data):
    visualizer = StreakVisualizer(
        win_streaks=win_data,
        lose_streaks=lose_data,
        season_num=season_num
    )
    visualizer.show()

def save_streak(season_num, win_data, lose_data, filename):
    visualizer = StreakVisualizer(
        win_streaks=win_data,
        lose_streaks=lose_data,
        season_num=season_num
    )
    visualizer.save(filename)

def show_deck_stats(stats, num):
    visualizer = DeckStatsVisualizer(stats, num)
    visualizer.show()

def save_deck_stats(stats, num, filename):
    visualizer = DeckStatsVisualizer(stats, num)
    visualizer.save(filename)

def show_top10_deck(deck_data, season_num):
    visualizer = DeckDistributionVisualizer(
        deck_data,
        season_num
    )
    visualizer.show()

def save_top10_deck(deck_data, season_num, filename, figsize=(14, 10)):
    visualizer = DeckDistributionVisualizer(
        deck_data,
        season_num,
        figsize=figsize
    )
    visualizer.save(filename)

def show_season_stats(stats, season_num):
    visualizer = SeasonStatsVisualizer(stats, season_num)
    visualizer.show()

def save_season_stats(stats, season_num, filename):
    visualizer = SeasonStatsVisualizer(stats, season_num)
    visualizer.save(filename)

if __name__ == "__main__":
    stats_dir = Path("~/yugioh-data/data/stats").expanduser()
    chart_base = Path("~/yugioh-data/data/chart").expanduser()
    for json_file in stats_dir.glob("s*_stats.json"):
        # 从文件名解析赛季编号（如s39）
        season_name = json_file.stem.split('_')[0]  # 获取s39
        season_num = int(season_name[1:])  # 提取纯数字39

        # 创建赛季图表目录
        season_chart_dir = chart_base / season_name
        season_chart_dir.mkdir(parents=True, exist_ok=True)

        # 读取数据
        with open(json_file, 'r', encoding='utf-8') as f:
            stats = json.load(f)

        # 准备数据
        win_data = stats['coin_streaks']['streak_list']['win']
        lose_data = stats['coin_streaks']['streak_list']['lose']
        deck_stats = stats['my_decks']
        top_10_decks = stats['top_10_decks']

        # 生成并保存所有图表
        save_streak(
            season_num,
            win_data,
            lose_data,
            str(season_chart_dir / "streak.png")
        )
        save_deck_stats(
            deck_stats,
            season_num,
            str(season_chart_dir / "deck_stats.png")
        )
        save_top10_deck(
            top_10_decks,
            season_num,
            str(season_chart_dir / "top10_decks.png")
        )
        save_season_stats(
            stats,
            season_num,
            str(season_chart_dir / "season_stats.png")
        )
        save_plot_analysis(
            stats,
            str(season_chart_dir / "dynamic_stats.png")
        )
        print(f"赛季{season_num}图表处理完毕")
