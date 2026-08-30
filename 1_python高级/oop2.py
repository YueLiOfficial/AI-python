class Devices:
    total = 0
    
    def __init__(self, name, status = "待机"):
        self.name = name
        self.status = status
        self._run_time = 0
        Devices.total += 1

    def start(self):
        if self.status == "开启":
            print(f"设备{self.name}正在运行")
            return

        self.status = "开启"
        print(f"设备{self.name}已开启")

    def stop(self):
        self.status = "待机"
        print(f"设备{self.name}已停止")

    @classmethod
    def create_from_dict(cls, data):
        return cls(data["name"], data.get("status", "待机"))

    @staticmethod
    def is_valid_name(name):
        return bool(name) and len(name) <= 20

    @property
    def run_time(self):
        return self._run_time

    @run_time.setter
    def run_time(self, val):
        if val < 0:
            raise ValueError("run_time 不能小于0")

        self._run_time = val

    def __str__(self):
        return f"设备{self.name}的运行状态是{self.status}, 运行时长是{self.run_time}s"

class Motor(Devices):
    def __init__(self, name, kw_power):
        super().__init__(name)
        self.kw_power = kw_power

    def start(self):
        super().start()
        print(f" →{self.name} 功率{self.kw_power}已开启")

    def __str__(self):
        return super().__str__() + f", 功率是{self.kw_power}"

class Pump(Devices):
    def __init__(self, name, flow_rate):
        super().__init__(name)
        self.flow_rate = flow_rate


def find_device(devices, name):
    for d in devices:
        if d.name == name:
            return d

    return None

devices = []
devices.append(Motor("电机", 15))
devices.append(Pump("水泵", 30))
devices.append(Devices.create_from_dict({"name": "空压机", "status": "故障"}))

for d in devices:
    d.start()
    print(d)

print(f"设备总数：{Devices.total}")
print(f"{Devices.is_valid_name('冷却水泵')}")

dev = find_device(devices, "水泵")
if dev:
    print(dev)
