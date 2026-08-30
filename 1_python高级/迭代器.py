# 迭代器法则：
# 1. 能够被iter()接受：实现__iter__魔法方法
# 2. 能够被next()一步一步取值：实现__next__魔法方法

# 实现方法一
# region

# class Person:
#     def __init__(self, name: str, age: int, gender: str, addr: str):
#         self.name = name
#         self.age = age
#         self.gender = gender
#         self.addr = addr

#     # 可迭代对象调用iter()返回一个迭代器
#     def __iter__(self):
#         return PersonIterator(self)

# class PersonIterator:
#     def __init__(self, p: Person):
#         self.p = p
#         # 记录当前遍历的位置
#         self.index = 0
#         # 要遍历的内容
#         self.attrs = [p.name, p.age, p.gender, p.addr]

#     # 迭代器调用iter()返回迭代器自身
#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.index >= len(self.attrs):
#             raise StopIteration

#         value = self.attrs[self.index]
#         self.index += 1

#         return value

# p1 = Person("张三", 18, "男", "杭州")

# for i in p1:
#     print(i)

# endregion


# 实现方法二
# region

# 将Person实例对象既当成可迭代对象，也当成迭代器
class Person:
    def __init__(self, name: str, age: int, gender: str, addr: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.addr = addr

        self.__index = 0
        self.__attrs = [name, age, gender, addr]

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index >= len(self.__attrs):
            raise StopIteration

        value = self.__attrs[self.__index]
        self.__index += 1

        return value

p1 = Person("张三", 18, "男", "杭州")

for i in p1:
    print(i)

# endregion
