import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='root123456',
    database='factory_db',
    charset='utf8mb4'
)

# 创建游标
cursor = conn.cursor()

# 建表
sql = (
    "CREATE TABLE IF NOT EXISTS devices (" \
    "id INT PRIMARY KEY AUTO_INCREMENT," \
    "code VARCHAR(20) NOT NULL UNIQUE," \
    "name VARCHAR(20) NOT NULL," \
    "type VARCHAR(20)," \
    "install_date DATE," \
    "status BOOL DEFAULT TRUE)"
)

cursor.execute(sql)

sql = "CREATE TABLE IF NOT EXISTS alarms (" \
"id INT PRIMARY KEY AUTO_INCREMENT," \
"device_id INT NOT NULL," \
"temp DECIMAL(5,1)," \
"happened DATETIME)"

cursor.execute(sql)

# 插入数据  
# sql = (
#     "INSERT INTO devices (code, name, type, install_date)" \
#     "VALUE (%s, %s, %s, %s)"
# )

# data = [
#     ('E-101', '主轴电机', '电机', "2026-08-11"),
#     ('E-102', '冷却水泵', '水泵', '2026-08-12'),
#     ('E-103', '空压机', '空压机', '2026-08-13')
# ]

# cursor.executemany(sql, data)

# 增删改需要commit
# conn.commit()

sql = "INSERT INTO alarms (device_id, temp, happened) VALUE (%s, %s, %s)"

data = [
    (1, 88.5, '2026-08-13 8:25:06'),
    (1, 97.8, '2026-08-13 8:25:06'),
    (2, 80.3, '2026-08-13 8:25:06'),
    (2, 88.0, '2026-08-13 8:25:06'),
    (2, 93.1, '2026-08-13 8:25:06')
]

cursor.executemany(sql, data)

conn.commit()

#查
sql = "SELECT * FROM devices"

cursor.execute(sql)

rows = cursor.fetchall()

for row in rows:
    print(row)

sql = "SELECT device_id, AVG(temp) FROM alarms GROUP BY device_id"

cursor.execute(sql)

rows = cursor.fetchall()

for type_, avg_temp in rows:
    print(f"{type_}, {avg_temp:.2f}")


cursor.close()
conn.close()