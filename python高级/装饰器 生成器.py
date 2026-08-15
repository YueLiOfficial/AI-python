import time
from functools import wraps

class Device:
    def __init__(self, name, status = "待机"):
        self.name = name
        self.status = status
        self._run_time = 0

    def timer(func):
        @wraps(func)
        def run_time(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            print(f"{func.__name__}耗时{time.time() - start_time:.2f}s")
            return result

        return run_time

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

def print_num(n):
    for i in range(n  +1):
        if i % 2 == 0:
            yield i

for i in print_num(10):
    print(i, end=' ')