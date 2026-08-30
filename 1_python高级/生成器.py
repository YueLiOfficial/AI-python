# 生成器就是一种特殊的迭代器
# 生成器通过yield自动实现迭代器法则

# 用生成器实现遍历Person对象的属性
class Person:
    def __init__(self, name: str, age: int, gender: str, addr: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.addr = addr

        self.__attrs = [name, age, gender, addr]

    def __iter__(self):
        yield from self.__attrs

p1 = Person("张三", 18, "男", "杭州")

# for item in p1:
    # print(item)

# 用生成器实现斐波那契数列
def fibo(total):
    pre = 1
    cur = 1
    for i in range(total):
        if i < 2:
            yield 1
        else:
            value = pre + cur
            pre = cur
            cur = value

            yield value

f1 = fibo(10)
# for i in f1:
#     print(i)

# 生成器表达式: (表达式 for i in 可迭代对象), 得到的结果是一个生成器对象
nums = [10, 20, 30, 40]
nums1 = (n * 2 for n in nums)
for i in nums1:
    print(i)