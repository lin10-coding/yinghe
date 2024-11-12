from flask import Flask, render_template, request
import pymysql
app = Flask(__name__)

# 数据库连接参数
host = '81.70.22.101'  # 数据库服务器地址
user = 'root'  # 数据库用户名
password = 'yabdylm'  # 数据库密码
database = 'swordCome'  # 数据库名

# 建立连接
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=database,
                             charset='utf8mb4',  # 指定字符集
                             cursorclass=pymysql.cursors.DictCursor)  # 使用字典游标

@app.route('/')
def index():
    return render_template("login.html")


@app.route('/create_character', methods=['GET', 'POST'])
def create_character():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        attributes = {
            '根骨': request.form.get('root_bone'),
            '魅力': request.form.get('charm'),
            '家境': request.form.get('family_back_ground'),
            '悟性': request.form.get('insight'),
            '机缘': request.form.get('fate'),
            '体魄': request.form.get('physique')
        }
        talent = request.form.get('talent')
        legacy = request.form.get('inheritance')
        return player_name


if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0',debug=True)
