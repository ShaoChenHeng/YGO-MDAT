import os
import json
num = 18
output_dir = os.path.expanduser("~/yugioh-data/data/stats")
json_file = os.path.join(output_dir, f"s{num}_stats.json")

# 检查文件是否存在
if not os.path.exists(json_file):
    print(f"文件 {json_file} 不存在！")
else:
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        stats = json.load(f)

# Print the results
print(f"\n====== s"+str(num)+"赛季情况 ======")
print(f"总对局数: {stats['total_matches']}")
print(f"先手数: {stats['first_moves']}")
print(f"硬币正面: {stats['coin_wins']}")
print(f"胜率: {stats['win_rate']}%")
print(f"硬币胜率: {stats['coin_win_rate']}%")
print(f"先手率: {stats['first_move_rate']}%")
print(f"先手胜率: {stats['first_move_win_rate']}%")
print(f"后手胜率: {stats['second_move_win_rate']}%")
print(f"赢硬币胜率: {stats['win_coin_win_rate']}%")
print(f"输硬币胜率: {stats['lose_coin_win_rate']}%")
print("\n=== 我的卡组统计 ===")

for deck, data in stats['my_decks'].items():
    print(f"\n卡组: {deck}")
    print(f"使用次数: {data['total']}")
    print(f"胜利次数: {data['wins']}")
    print(f"胜率: {data['win_rate']}%")
    print(f"赢硬币次数: {data['coin_wins']}")
    print(f"硬币胜率: {data['coin_win_rate']}%")

print(f"\n=== s"+str(num)+"赛季天梯环境TOP10 ===")
for deck, count in stats['top_10_decks'].items():
    print(f"- {deck}: {count}次")

# 打印新增的连续硬币统计
print("\n=== 连续硬币统计 ===")
print(f"连续3+次硬币胜出现次数: {stats['coin_streaks']['win_occurrences']}")
print(f"连续3+次硬币负出现次数: {stats['coin_streaks']['lose_occurrences']}")
print(f"最大连续硬币胜次数: {stats['coin_streaks']['max_win_streak']}")
print(f"最大连续硬币负次数: {stats['coin_streaks']['max_lose_streak']}")
print("硬币连续胜:")
for i in stats['coin_streaks']['streak_list']['win']:
    print(i, end=' ')

print("\n硬币连续负:")
for i in stats['coin_streaks']['streak_list']['lose']:
    print(i, end=' ')

print("\n=== 硬币公平性检验 ===")
print("\n* 卡方检验 *")
print(f"卡方统计量: {stats['coin_fairness_test']['chi2_statistic']:.6f}")
print(f"P值: {stats['coin_fairness_test']['p_value']:.6f}")
if stats['coin_fairness_test']['is_fair']:
    print("结论: 硬币结果符合公平分布 (p > 0.05)")
else:
    print("结论: 硬币结果可能不公平 (p ≤ 0.05)")
print("\n* 二项检验 *")
pvalue = stats['binom_test']
print(f"P值: {pvalue:.6f}")
if pvalue > 0.05:
    print("结论: 硬币结果符合公平分布 (p > 0.05)")
else:
    print("结论: 硬币结果可能不公平 (p ≤ 0.05)")

print("\n=== 赛季中期统计 ===")
print(f"截至第{stats['total_matches'] // 2}场")
interval = stats['middle_stats'][0]
print(f"\n对局数: {interval['total_matches']}")
print(f"先手数: {interval['first_moves']}")
print(f"硬币正面: {interval['coin_wins']}")
print(f"胜率: {interval['win_rate']}%")
print(f"硬币胜率: {interval['coin_win_rate']}%")
print(f"先手率: {interval['first_move_rate']}%")
print(f"先手胜率: {interval['first_move_win_rate']}%")
print(f"后手胜率: {interval['second_move_win_rate']}%")
print(f"赢硬币胜率: {interval['win_coin_win_rate']}%")
print(f"输硬币胜率: {interval['lose_coin_win_rate']}%")

print("\n**中期硬币公平性检验**")
print("\n* 卡方检验  *")
print(f"卡方统计量: {interval['coin_fairness_test']['chi2_statistic']:.6f}")
print(f"P值: {interval['coin_fairness_test']['p_value']:.6f}")
if interval['coin_fairness_test']['is_fair']:
    print("结论: 硬币结果符合公平分布 (p > 0.05)")
else:
    print("结论: 硬币结果可能不公平 (p ≤ 0.05)")

print("\n* 二项检验 *")
pvalue = interval['binom_test']
print(f"P值: {pvalue:.6f}")
if pvalue > 0.05:
    print("结论: 硬币结果符合公平分布 (p > 0.05)")
else:
    print("结论: 硬币结果可能不公平 (p ≤ 0.05)")

print("\n=== 每20场统计 ===")
for interval in stats['interval_stats']:
    print(f"\n对局数: {interval['total_matches']}")
    print(f"硬币胜率: {interval['coin_win_rate']}%")
    print(f"对局胜率: {interval['win_rate']}%")
    print(f"先手率: {interval['first_move_rate']}%")
    print(f"先手胜率: {interval['first_move_win_rate']}%")
    print(f"后手胜率: {interval['second_move_win_rate']}%")
    print(f"赢硬币胜率: {interval['win_coin_win_rate']}%")
    print(f"输硬币胜率: {interval['lose_coin_win_rate']}%")

print("==============================")
