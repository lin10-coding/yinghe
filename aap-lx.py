from datetime import datetime, timedelta
from flask import url_for
from flask import Flask, request, jsonify, render_template
import json
import os

from statistic import calculate_totals, read_records_from_json

app = Flask(__name__)

# 确保数据文件存在
DATA_FILE = 'billing.json'
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:  # 指定编码为utf-8
        json.dump([], f, ensure_ascii=False)  # 确保非ASCII字符被正确处理

@app.route("/")
def index():
    return render_template('home.html')
@app.route("/statistics.html")
def statistics():
    return render_template('statistics.html')
@app.route("/basic-accounting.html")
def basicaccounting():
    return render_template('basic-accounting.html')
@app.route("/view-records.html")
def viewrecords():
    return render_template('view-records.html')
@app.route("/index_read.html")
def read0():
    return render_template('index_read.html')

@app.route('/billing/loadData', methods=['POST'])
def add_Data():
    print("Received POST request", request.json)  # 打印请求数据以确认接收

    data = request.json
    # 确保所有必要的字段都存在
    if not all(key in data for key in ['date', 'price', 'category']):
        return jsonify({'error': 'Missing required fields'}), 400

    with open(DATA_FILE, 'r+', encoding='utf-8') as f:
        transactions = json.load(f)
        new_transaction = {
            'date': data['date'],
            'price': data['price'],
            'category': data['category'],
            'note': data.get('note', '')  # 备注是可选的
        }
        transactions.append(new_transaction)

        # 将文件指针移动到文件开头
        f.seek(0)
        # 写入更新后的交易列表
        json.dump(transactions, f, ensure_ascii=False)
        # 如果数据比文件原来的大小小，则截断文件
        f.truncate()

    return jsonify({'redirect': url_for('index', _external=True)}), 201  # 确保使用 _external=True