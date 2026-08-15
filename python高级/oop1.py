import time

class Devices:
    def __init__(self, name, status = "关闭"):
         self.name = name
         self.status = status
         self.run_time = 0

    def start(self):
        if self.status == "开启":
            print(f"设备{self.name}已在运行")
        else:
            self.status = "开启"
            print(f"设备{self.name}已开启")
            self.start_time = time.time()

    def stop(self):
        if self.status == "关闭":
            print(f"设备{self.status}未开启，无法关闭")
            return
        
        self.status = "关闭"
        print(f"设备{self.name}已关闭")

        self.stop_time = time.time()
        self.run_time = self.stop_time - self.start_time

    def __str__(self):
        return f"设备{self.name}的状态是{self.status}, 设备运行时间是{self.run_time:.2f}s"

    def __eq__(self, other):
        return self.name == other.name

dev1 = Devices("dev1", "关闭")

dev2 = Devices("dev1", "关闭")

print(dev1 == dev2)
