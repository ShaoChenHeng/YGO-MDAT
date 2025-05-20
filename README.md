# YGO-MDAT - 游戏王大师决斗数据分析工具

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

YuGiOh Master Duel Analytics Tool 是为《游戏王：大师决斗》玩家设计的专业数据分析系统。旨在验证该游戏的平衡机制。

## 🎮 核心功能
### 样例文件
统计了一份3000场对局的游戏记录，包含赛季18-41数据。

### 数据处理管道
- Excel/XLSX → JSON 格式转换（赛季18-41数据）
- 自动化数据清洗（处理异常值/统一卡组命名）
- 智能硬币结果推断（基于"让先/被让先"备注）

### 高级统计分析
- 赛季核心指标计算（胜率/先手率/硬币胜率）
- 卡组专属表现分析（使用次数/胜率/硬币操控）
- 连胜模式检测（3+连胜自动识别与统计）

### 可视化报告
- 自动生成赛季Markdown报告（含图表嵌入）
- TOP10卡组分布饼图
- 动态胜率趋势折线图
- 硬币公平性统计检验（卡方/二项式检验）

### 全面统计
- 跨赛季累计数据聚合
- 环境变迁趋势分析
- 核心指标历史波动跟踪

## 📂 项目结构
```
YGO-MDAT/
├── data/
│   ├── json/         # 清洗后的比赛记录
│   ├── stats/        # 计算的统计数据
│   ├── xlsx/         # 原始比赛记录表
│   └── chart/        # 生成的图表文件
├── docs/
│   └── total_stats.md # 累计统计报告
├── src/
│   ├── calcStats.py          # 核心统计计算
│   ├── drawStats.py          # 可视化模块
│   ├── generateMD.py         # Markdown生成
│   ├── generateTotalStats.py # 总体数据图表生成
│   ├── xlsxToJson.py         # 数据转换
|   ├── printStatsJson.py     # 即使查看数据工具
│   └── utils/                # 可视化工具类
└── README.md
```

## 🚀 快速开始

### 环境需求
```bash
Python 3.10+
pip install -r requirements.txt
```
requirements.txt:
```
pandas>=1.5.0
matplotlib>=3.6.0
seaborn>=0.12.0
scipy>=1.9.0
openpyxl>=3.0.0
tabulate>=0.9.0
```
