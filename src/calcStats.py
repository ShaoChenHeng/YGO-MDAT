import json
import os
import numpy as np
from collections import defaultdict
from pathlib import Path
from scipy.stats import chisquare, binomtest

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_, np.integer, np.floating)):
            return obj.item()
        return super().default(obj)

def rate_calc(numerator, denominator):
    if denominator <= 0:
        return 0
    return (numerator / denominator) * 100

# 卡方拟合度检验
def chisquare_calc(coin_wins, total_matches):
    observed_coin = [coin_wins, total_matches - coin_wins]  # [正面次数, 反面次数]
    expected_coin = [total_matches * 0.5, total_matches * 0.5]  # 期望值
    chi2, p_value = chisquare(observed_coin, f_exp=expected_coin)

    coin_fairness_test = {
        'chi2_statistic': chi2,
        'p_value': p_value,
        'is_fair': p_value > 0.05  # 如果p>0.05则认为硬币公平
    }

    return coin_fairness_test

# 二项检验
def binomtest_calc(coin_wins, total_matches):
    result = binomtest(coin_wins, total_matches, p=0.5)
    return result.pvalue

def analyze_match_data(json_file):
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        matches = json.load(f)

    # Initialize counters
    total_matches = len(matches)
    wins = 0
    coin_wins = 0
    first_moves = 0
    first_move_wins = 0
    second_move_wins = 0
    win_coin_wins = 0
    lose_coin_wins = 0

    # 连续硬币统计
    current_coin_streak = 0  # 当前连续次数
    last_coin_result = None  # 上一次硬币结果
    streak_type = matches[0]['match_res']  # 当前连续类型 ('win'或'lose')

    # 连续3次及以上统计
    streak_occurrences = {'win': 0, 'lose': 0}  # 发生次数
    max_streaks = {'win': 0, 'lose': 0}         # 最大连续次数
    streak_list = {'win':[], 'lose':[]}

    # Count deck matchups
    deck_matchups = defaultdict(lambda: {'wins': 0, 'total': 0})
    deck_counts = defaultdict(int)

    my_deck_stats = defaultdict(lambda: {
        'total': 0,
        'wins': 0,
        'coin_wins': 0,
    })

    # 每隔20场对各种概率统计一次
    interval_stats = []
    current_count = 0

    # 赛季中期统计
    middle_stats = []

    # Process each match
    for match in matches:

        my_deck = match['my_deck']
        current_coin = match['coin_res']  # 'win'或'lose'
        win_or_lose = match['match_res']
        current_count += 1

        my_deck_stats[my_deck]['total'] += 1

        # 胜率 & 卡组胜率
        if win_or_lose == 'win':
            my_deck_stats[my_deck]['wins'] += 1
            wins += 1

        # 赢硬币次数 & 赢/输硬币 赢次数
        if current_coin == 'win':
            coin_wins += 1
            my_deck_stats[my_deck]['coin_wins'] += 1
            if win_or_lose == 'win':
                win_coin_wins += 1
        else:
            if win_or_lose == 'win':
                lose_coin_wins += 1

        # 连续硬币统计逻辑
        if current_coin == last_coin_result:
            current_coin_streak += 1
        else:
            # 记录上一个连续序列
            if current_coin_streak >= 3:
                streak_occurrences[streak_type] += 1
                streak_list[streak_type].append(current_coin_streak)
                if current_coin_streak > max_streaks[streak_type]:
                    max_streaks[streak_type] = current_coin_streak
            current_coin_streak = 1
            streak_type = current_coin
        last_coin_result = current_coin

        # 先手胜率
        if match['first_move'] == 'first':
            first_moves += 1
            if win_or_lose == 'win':
                first_move_wins += 1
        else:
            if win_or_lose == 'win':
                second_move_wins += 1

        # Track deck matchups (optional)
        # 对 对手卡组胜率
        deck_matchups[match['op_deck']]['total'] += 1
        if win_or_lose == 'win':
            deck_matchups[match['op_deck']]['wins'] += 1

        deck_counts[match['op_deck']] += 1

        # 记录每20场统计
        if current_count % 20 == 0:
            win_rate = rate_calc(wins, current_count)
            coin_win_rate = rate_calc(coin_wins, current_count)
            first_move_rate = rate_calc(first_moves, current_count)
            first_move_win_rate = rate_calc(first_move_wins, first_moves)
            second_move_win_rate = rate_calc(second_move_wins,
                                             current_count - first_moves)
            win_coin_win_rate = rate_calc(win_coin_wins, coin_wins)
            lose_coin_win_rate = rate_calc(lose_coin_wins, current_count - coin_wins)

            interval_stats.append({
                'total_matches': current_count,
                'coin_win_rate': round(coin_win_rate, 2),
                'win_rate': round(win_rate, 2),
                'first_move_rate': round(first_move_rate, 2),
                'first_move_win_rate': round(first_move_win_rate, 2),
                'second_move_win_rate': round(second_move_win_rate, 2),
                'win_coin_win_rate': round(win_coin_win_rate, 2),
                'lose_coin_win_rate': round(lose_coin_win_rate, 2)
            })

        # 赛季中期统计
        if current_count == total_matches // 2:
            win_rate = rate_calc(wins, current_count)
            coin_win_rate = rate_calc(coin_wins, current_count)
            first_move_rate = rate_calc(first_moves, current_count)
            first_move_win_rate = rate_calc(first_move_wins, first_moves)
            second_move_win_rate = rate_calc(second_move_wins,
                                             current_count - first_moves)
            win_coin_win_rate = rate_calc(win_coin_wins, coin_wins)
            lose_coin_win_rate = rate_calc(lose_coin_wins, current_count - coin_wins)
            coin_fairness_test = chisquare_calc(coin_wins, current_count)
            binom_test =  binomtest_calc(coin_wins, current_count)

            middle_stats.append({
                'total_matches': current_count,
                'wins': wins,
                'coin_wins': coin_wins,
                'first_moves':first_moves,
                'first_move_wins': first_move_wins,
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
                'coin_fairness_test' : coin_fairness_test,
                'binom_test' : binom_test
            })

    # 处理最后一个连续序列
    if current_coin_streak >= 3:
        streak_occurrences[streak_type] += 1
        streak_list[streak_type].append(current_coin_streak)
        if current_coin_streak > max_streaks[streak_type]:
            max_streaks[streak_type] = current_coin_streak

    # 前十对手卡组（按出现次数排序）
    top_10_decks = sorted(
        deck_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    # 结果统计
    win_rate = rate_calc(wins, total_matches)                    # 胜率
    coin_win_rate = rate_calc(coin_wins, total_matches)          # 硬币胜率
    first_move_rate = rate_calc(first_moves, total_matches)      # 先手率
    first_move_win_rate = rate_calc(first_move_wins, first_moves)# 先手胜率
    second_move_win_rate = rate_calc(second_move_wins,           # 后手胜率
                                     (total_matches - first_moves))
    win_coin_win_rate = rate_calc(win_coin_wins, coin_wins)      # 赢硬币胜率
    lose_coin_win_rate = rate_calc(lose_coin_wins,               # 输硬币胜率
                                   (total_matches - coin_wins))
    coin_fairness_test = chisquare_calc(coin_wins, total_matches)
    binom_test =  binomtest_calc(coin_wins, current_count)

    my_deck_results = {}
    for deck, stats in my_deck_stats.items():
        total = stats['total']
        my_deck_results[deck] = {
            'total': total,
            'wins': stats['wins'],
            'win_rate': round(rate_calc(stats['wins'], total), 2),
            'coin_wins': stats['coin_wins'],
            'coin_win_rate': round(rate_calc(stats['coin_wins'], total), 2)
        }

    results = {
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
        'coin_fairness_test' : coin_fairness_test,
        'binom_test' : binom_test,
        'top_10_decks': dict(top_10_decks),
        'my_decks': my_deck_results,
        'coin_streaks': {
            'win_occurrences': streak_occurrences['win'],
            'lose_occurrences': streak_occurrences['lose'],
            'max_win_streak': max_streaks['win'],
            'max_lose_streak': max_streaks['lose'],
            'streak_list' : streak_list
        },
        'middle_stats' : middle_stats,
        'interval_stats': interval_stats
    }

    return results

# 数据处理
num = 36

def save_stats(output_path, stats_file):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stats_file, f, ensure_ascii=False, indent=2, cls=CustomEncoder)


json_dir = os.path.expanduser("~/yugioh-data/data/json")
json_file = os.path.join(json_dir, f"s{num}.json")
stats_dir = os.path.expanduser("~/yugioh-data/data/stats")
os.makedirs(json_dir, exist_ok=True)

for i in range(18, 42):
    json_file = os.path.join(json_dir, f"s{i}.json")
    stats_file = os.path.join(stats_dir, f"s{i}_stats.json")
    if not os.path.exists(json_file):
        print(f"{json_file}.json 不存在，跳过该文件。")
        continue
    stats = analyze_match_data(json_file)
    save_stats(stats_file, stats)
    print(f"s{i}处理完毕")
