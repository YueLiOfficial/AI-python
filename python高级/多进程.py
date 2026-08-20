# from multiprocessing import Process, current_process
# import os
# import time

# def speak(a, b, msg):
#     for i in range(10):
#         print(f"speak进程--{msg}--{a}--{b}--{current_process().name}执行第{i}次, 进程pid = {os.getpid()}, 父进程pid = {os.getppid()}")
#         time.sleep(1)

# def study():
#     for i in range(15):
#         print(f"study进程{current_process().name}执行第{i}次, 进程pid = {os.getpid()}, 父进程pid = {os.getppid()}")
#         time.sleep(1)

# if __name__ == "__main__":
#     print(f"父进程开始, pid = {os.getpid()}")
#     p1 = Process(target=speak, name="说话进程", args=(1, 2), kwargs={"msg": "test"})
#     p2 = Process(target=study)

#     p1.start()
#     p2.start()

#     print("父进程结束")

# 继承Process类创建子进程
from multiprocessing import Process, current_process
import os, time
class SpeakProcess(Process):
    def __init__(self, a, b, msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.a = a
        self.b = b
        self.msg = msg

    def run(self):
        for i in range(10):
            print(f"speak进程--{self.msg}--{self.a}--{self.b}--{current_process().name}, pid = {os.getpid()}执行第{i}次")
            time.sleep(1)

class StudyProcess(Process):
    def run(self):
        for i in range(10):
            print(f"study进程 pid = {os.getpid()}执行第{i}次")
            time.sleep(1)

if __name__ == "__main__":
    p1 = SpeakProcess(1, 2, "test", name = "speak")
    p2 = StudyProcess()

    p1.start()
    p2.start()

    p1.join()
    p2.join()


# 进程锁 Lock
# from multiprocessing import Process, Lock, RLock
# import time

# def speak(lock):
#     for i in range(10):
#         lock.acquire()
#         lock.acquire()
#         print("你", end='')
#         print("好", end='')
#         print("啊")
#         lock.release()
#         lock.release()
#         time.sleep(1)

# def study(lock):
#     try:
#         for i in range(10):
#             # with.lock开始之前自动获取锁：lock.acquire()
#             # with.lock结束后自动释放锁：lock.release()
#             with lock:
#                 print("A", end='')
#                 print("B", end='')
#                 print("C")
#             time.sleep(1)
#     # 使用termiante()让操作系统强制终止进程不会执行finally
#     finally:
#         print("finally中的逻辑")

# if __name__ == "__main__":
#     print('主进程开始执行')
#     lock = RLock()

#     p1 = Process(target=speak, args=(lock,))
#     p2 = Process(target=study, args=(lock,))

#     p1.start()
#     p2.start()

#     time.sleep(3)
#     print("准备强制终止p2进程")
#     p2.terminate() # 向操作系统申请强制终止p2进程

#     p2.join() # 让主进程等p2执行完毕后再继续执行

#     print(f"p2的状态{p2.is_alive()}")

#     p1.join() # 让主进程等p1执行完毕后再继续执行

#     print('主进程执行完毕')
