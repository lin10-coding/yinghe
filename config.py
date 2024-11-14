import pymysql

NOW_PLAYER_ID = -1
# 建立连接
CONNECTION = pymysql.connect(host='81.70.22.101',
                             user='root',
                             password='yabdylm',
                             database='swordCome',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)