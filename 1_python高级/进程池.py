from concurrent.futures import ProcessPoolExecutor, as_completed
import time, os

# def work(n: int):
#     print(f"work正在执行{n}, pid = {os.getpid()}")
#     time.sleep(1)

# if __name__ == "__main__":
#     executor = ProcessPoolExecutor(3)

#     for i in range(10):
#         executor.submit(work, i)

#     executor.shutdown(wait=True)

# def squre(n):
#     time.sleep(1)
#     return n * n


# if __name__ == "__main__":
#     with ProcessPoolExecutor(3) as executor:
#         # results = []
#         # for i in range(1, 11):
#         #     result = executor.submit(squre, i)
#         #     results.append(result)

#         results = [executor.submit(squre, i) for i in range(1, 11)]

#         for res in results:
#             print(res.result())


def work(i):
    if i == 1:
        time.sleep(15)
    elif i ==2:
        time.sleep(10)
    else:
        time.sleep(1)

    return f"我是任务{i}的结果"


if __name__ == "__main__":
    with ProcessPoolExecutor(3) as executor:
        # 提交10个任务
        futures = [executor.submit(work, index) for index in range(1, 10)]

        results = []

        for f in as_completed(futures):
            results.append(f.result())

        print(results)
