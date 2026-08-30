import time

users = {
    "张三": "123456",
    "李四": "888888",
    "王五": "abc123"
}

username = input("请输入用户名: ")
passwd = input("请输入密码: ")

with open("log.txt", "a+", encoding="utf-8") as f:
    if username not in users:
        print(f"{username}不存在")
        f.write(f"{username}不存在, 时间{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    elif passwd != users.get(username):
        print(f"{passwd}不正确")
        f.write(f"{passwd}不正确, 时间{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    elif passwd == users.get(username):
        print(f"{username}登录成功")
        f.write(f"{username}登录成功, 时间{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
