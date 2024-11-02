
import json
import os
from datetime import datetime

# 从 JSON 文件读取记录
def read_records_from_json(file_path='billing.json'):
    try:
        # 获取当前文件的目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建 JSON 文件的完整路径
        full_path = os.path.join(base_dir, file_path)
        with open(full_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        data = []
    return data

# 计算收支统计
def calculate_totals(records, date_filter=None, category_filter=None):
    total_income = 0.0
    total_expense = 0.0

    # 处理日期过滤参数的格式
    if date_filter:
        if isinstance(date_filter, tuple) and len(date_filter) == 2:
            start_date_str, end_date_str = date_filter
            # 解析过滤参数中的日期字符串
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        elif isinstance(date_filter, str):
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d')
        else:
            start_date = end_date = None

    for record in records:
        # 日期筛选
        record_date = datetime.strptime(record['date'], '%Y年%m月%d日')
        date_match = True
        if date_filter:
            if isinstance(date_filter, tuple) and start_date and end_date:
                # 时间范围过滤
                date_match = start_date <= record_date <= end_date
            elif isinstance(date_filter, str):
                date_match = record_date == filter_date

        # 类别筛选
        category_match = True
        if category_filter:
            category_match = record['category'] == category_filter

        # 检查是否匹配所有条件
        if date_match and category_match:
            # 计算总收入和支出
            price = float(record['price'])  # 确保金额转换为浮点数
            if price > 0:
                total_income += price
            else:
                total_expense += price  # 支出为负数

    # 返回统计结果
    return {
        "total_income": total_income,
        "total_expense": abs(total_expense),
        "net_income": total_income + total_expense
    }

# 测试数据读取
if __name__ == "__main__":
    records = read_records_from_json("billing.json")
    print("Records from JSON file:", records)