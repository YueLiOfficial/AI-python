import time
from functools import wraps

# 函数装饰器
class Device:
    def __init__(self, name, status = "待机"):
        self.name = name
        self.status = status
        self._run_time = 0

    def timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result =  func(*args, **kwargs)
            print(f"{func.__name__}耗时{time.time() - start_time:.2f}s")
            return result

        return wrapper

    @timer
    def start(self):
        if self.status == "开启":
            print(f"{self.name}已在运行")
            return

        self.status = "开启"
        time.sleep(1)
        print(f"{self.name}已启动")

dev = Device("dev1")
dev.start()

# 函数装饰器
def say_hello(func):
    def wrapper(*args, **kwargs):
        print(f"你好，我要开始计算了")
        return func(*args, **kwargs)

    return wrapper

@say_hello
def add(x, y):
    res = x + y
    print(f"{x}和{y}进行计算的值是{res}")
    return res

add(10, 20)

# 带参数的函数装饰器
def say_hello(msg):
    def outer(func):
        def wrapper(*args, **kwargs):
            print(f"你好，我要开始进行{msg}计算了")
            return func(*args, **kwargs)
        return wrapper
    return outer

@say_hello('加法')
def add(x, y):
    res = x + y
    print(f"{x}和{y}进行计算的值是{res}")
    return res

add(10, 20)

# 类装饰器
class SayHello:
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print("你好，我要开始计算了")
            return func(*args, **kwargs)
        return wrapper

@SayHello()
def add(x, y):
    res = x + y
    print(f"{x}和{y}进行计算的值是{res}")
    return res

add(20, 20)

# 带参数的类装饰器
class SayHello:
    def __init__(self, msg):
        self.msg = msg

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f"你好，我要开始进行{self.msg}计算了")
            return func(*args, **kwargs)
        return wrapper

@SayHello('加法')
def add(x, y):
    res = x + y
    print(f"{x}和{y}进行计算的值是{res}")
    return res

add(20, 20)


# 迭代器
# def print_num(n):
#     for i in range(n  +1):
#         if i % 2 == 0:
#             yield i

# for i in print_num(10):
#     print(i, end=' ')
