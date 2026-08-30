import asyncio, time

# 多个任务同步执行
# async def work(n, t):
#     print(f"任务{n}开始")
#     print(f"任务{n}执行中")
#     await asyncio.sleep(t)
#     print(f"任务{n}结束")

#     return f"任务{n}返回值"

# async def main():
#     print("任务main开始")

#     start = time.time()

#     # 得到三个协程对象
#     coroutine1 = work(1, 2)
#     coroutine2 = work(2, 2)
#     coroutine3 = work(3, 2)

#     # 等待coroutine1完成
#     res1 = await coroutine1
#     print(res1)

#     # 等待coroutine1完成后再等待coroutine2完成
#     res2 = await coroutine2
#     print(res2)

#     # 等待coroutine2完成后再等待coroutine3完成
#     res3 = await coroutine3
#     print(res3)

#     print(f"任务main结束, time = {time.time() - start}")

#     return f"任务main返回值"

# res = asyncio.run(main())
# print(res)


# 多个任务异步执行
# async def work(n, t):
#     print(f"任务{n}开始")
#     print(f"任务{n}执行中")
#     await asyncio.sleep(t)
#     print(f"任务{n}结束")

#     return f"任务{n}返回值"

# async def main():
#     print(f"任务main开始")

#     start = time.time()

#     # # asyncio.create_task()能够将协程对象包装成可被事件循环调度的任务，并注册到事件循环中
#     # task1 = asyncio.create_task(work(1, 2))
#     # task2 = asyncio.create_task(work(2, 2))
#     # task3 = asyncio.create_task(work(3, 2))

    

#     # # 等待task1执行完毕
#     # res1 = await task1
#     # print(res1)

#     # # 等待task1执行完毕后，再等待task2执行完毕
#     # res2 = await task2
#     # print(res2)

#     # # 等待task2执行完毕后，再等待task3执行完毕
#     # res3 = await task3
#     # print(res3)

#     # 也可以使用asyncio.gather()一次性将多个协程对象打包并丢给事件循环，并且等待所有的协程执行完毕后能够一次性拿到所有的返回值
#     res = await asyncio.gather(work(1, 2), work(2, 2), work(3, 2))
#     print(res)

#     print(f"任务main结束, time = {time.time() - start}")

#     return f"任务main返回值"

# res = asyncio.run(main())
# print(res)

# 使用独立线程隔离需要执行传统阻塞的代码
def old_task(name):
    print(f"任务{name}开始运行")
    for i in range(5):
        print(f"任务{name}执行第{i}次")
        time.sleep(1)
    print(f"任务{name}执行完毕")

async def main():
    print("任务main开始执行")

    task1 = asyncio.to_thread(old_task, "task1")
    task2 = asyncio.to_thread(old_task, "task2")

    await asyncio.gather(*[task1, task2])

    print("任务main执行完毕")

asyncio.run(main())