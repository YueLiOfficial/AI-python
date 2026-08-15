import pymysql

class DeviceRepo:
    '''封装数据库操作'''

    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost', 
            port=3306,
            user='root',
            password='root123456',
            database='factory_db',
            charset='utf8mb4'
        )

        self.cursor = self.conn.cursor()

    def add_device(self, code: str, name: str, type_: str):
        '''新增设备'''
        sql = "INSERT INTO devices (code, name, type) VALUE (%s, %s, %s)"

        self.cursor.execute(sql, (code, name, type_))
        self.conn.commit()

        print(f"已添加{name}")

    def find_by_code(self, code: str):
        '''按照编号查找设备'''
        sql = "SELECT * FROM devices WHERE code = %s"

        self.cursor.execute(sql, (code,))
        return self.cursor.fetchone()

    def list_all(self):
        '''列出全部设备'''
        sql = "SELECT * FROM devices"

        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def set_status(self, code: str, status: bool):
        '''启停设备，True表示启动，False表示停止'''
        sql = "UPDATE devices SET status = %s WHERE code = %s"

        self.cursor.execute(sql, (status, code))

        self.conn.commit()

        print(f"设备{code}的状态已更新")

    def close(self):
        '''关闭连接'''
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    repo = DeviceRepo()

    repo.add_device('E-104', '压力变送器', '传感器')
    print(repo.find_by_code('E-101'))
    repo.set_status('E104', False)
    for d in repo.list_all():
        print(d)

    repo.close()