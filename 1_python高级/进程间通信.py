# 使用Queue实现进程间通信
# from multiprocessing import Process, Queue
# import time

# # 进程1：向队列中放数据
# def task1(q:Queue):
#     for i in range(10):
#         print(f"task1向队列中添加{i}")
#         q.put(i)
#         time.sleep(1)

# # 进程2：从队列中取数据
# def task2(q:Queue):
#     for i in range(10):
#         data = q.get()
#         print(f"task2从队列中取出{data}")
#         time.sleep(1)

# if __name__ == "__main__":
#     q = Queue()

#     p1 = Process(target=task1, args=(q,))
#     p2 = Process(target=task2, args=(q,))

#     p1.start()
#     p2.start()

#     p1.join()
#     p2.join()


# 使用Pipe实现进程间通信（双向）
from multiprocessing import Process, Pipe
import time

# 进程1：向pipe中放数字，取字母
def task1(con1):
    for i in range(10):
        con1.send(i)
        letter = con1.recv()
        print(f"task1向进程中放入{i}, 取出了{letter}")
        time.sleep(1)
    
# 进程1：向pipe中放字母，取数字
def task2(con2):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for i in letters:
        con2.send(i)
        num = con2.recv()
        print(f"task2向进程中放入{i}, 取出了{num}")
        time.sleep(1)

if __name__ == "__main__":
    con1, con2 = Pipe()

    p1 = Process(target=task1, args=(con1,))
    p2 = Process(target=task2, args=(con2,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()