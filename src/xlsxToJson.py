import pandas as pd
import json
import os
from pathlib import Path

def clean_remark(value):
    if pd.isna(value):
        return ""
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return value.strip()
    else:
        return value

class MatchDataReader:
    """对战数据读取器"""

    COLUMN_MAPPING = {
        '己方牌组': 'my_deck',
        '对手牌组': 'op_deck',
        '先后手': 'first_move',
        '胜负': 'match_res'
    }

    def __init__(self, input_path):
        self.input_path = Path(input_path).expanduser()
        self.df = None
        self.records = []

    def _clean_data(self):
        """数据清洗"""
        self.df['备注'] = self.df['备注'].apply(clean_remark)
        self.df['先后手'] = self.df['先后手'].map({'先': 'first', '后': 'second'})
        self.df['胜负'] = self.df['胜负'].map({'胜': 'win', '负': 'lose'})

    def _infer_coin_result(self, row):
        """硬币结果推断逻辑"""
        notes = row['备注']
        if "让先" == notes:
            return "win"
        elif "被让先" == notes:
            return "lose"
        else:
            return "win" if row['先后手'] == "first" else "lose"

    def process(self):
        """主处理流程"""
        self.df = pd.read_excel(self.input_path)
        self._clean_data()
        self.df['coin_res'] = self.df.apply(self._infer_coin_result, axis=1)

        self.records =(
             self.df.rename(columns=self.COLUMN_MAPPING)
            .assign(notes=self.df['备注'], coin_res=self.df['coin_res'])
            [list(self.COLUMN_MAPPING.values()) + ['coin_res', 'notes']]
            .to_dict('records'))

        return self

    def save_json(self, output_path):
        """保存结果"""
        with Path(output_path).open('w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
        return self

# 使用示例
if __name__ == "__main__":
    xlsx_dir = os.path.expanduser("~/yugioh-data/data/xlsx/")
    json_dir = os.path.expanduser("~/yugioh-data/data/json")

    # Make sure the json directory exists
    os.makedirs(json_dir, exist_ok=True)
    for i in range(18, 42):
        xlsx_file = os.path.join(xlsx_dir, f"s{i}.xlsx")
        json_file = os.path.join(json_dir, f"s{i}.json")
        if not os.path.exists(xlsx_file):
            print(f"{xlsx_file}.xlsx 不存在，跳过该文件。")
            continue
        processor = MatchDataReader(xlsx_file)
        processor.process().save_json(json_file)
        print(f"s{i}处理完毕")
