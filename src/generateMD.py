from pathlib import Path
import re

def generate_season_markdown(chart_dir, md_dir):
    # 展开用户目录并转换为Path对象
    chart_dir = Path(chart_dir).expanduser()
    md_dir = Path(md_dir).expanduser()

    relative_chart_path = Path("../chart")

    # 遍历所有赛季目录（s开头的文件夹）
    for season_dir in chart_dir.glob("s[0-9]*"):
        if not season_dir.is_dir():
            continue

        # 提取赛季编号（例如s39中的39）
        season_num = re.search(r"s(\d+)$", season_dir.name).group(1)
        md_filename = md_dir / f"s{season_num}.md"

        # 定义需要的图片文件列表
        image_files = [
            "top10_decks.png",
            "season_stats.png",
            "deck_stats.png",
            "dynamic_stats.png",
            "streak.png",
        ]

        # 生成Markdown内容
        md_content = f"# 赛季 {season_num} 数据分析报告\n\n"


        for img in image_files:
            img_relative_path = relative_chart_path / f"s{season_num}" / img
            md_content += (
                f"## {img.split('.')[0].replace('_', ' ').title()}\n"
                f"![{img}]({img_relative_path.as_posix()})\n\n"
            )

        # 写入文件
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Generated: {md_filename}")

if __name__ == "__main__":
    chart_dir="~/yugioh-data/data/chart"
    md_dir = "~/yugioh-data/data/MD"
    generate_season_markdown(chart_dir, md_dir)
