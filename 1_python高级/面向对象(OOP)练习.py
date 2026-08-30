class Employee:
    def __init__(self, name, employee_id, base_salary):
        self.__name = name
        self.__id = employee_id
        self.__base_salary = base_salary

    def get_details(self):
        return f"员工{self.__name}的id是{self.__id}, 工资是{self.calculate_salary()}"

    def calculate_salary(self):
        return self.__base_salary

    @property
    def id(self):
        return self.__id

class Manager(Employee):
    def __init__(self, name, employee_id, base_salary, bonus):
        super().__init__(name, employee_id, base_salary)
        self.__bonus = bonus

    def calculate_salary(self):
        return super().calculate_salary() + self.__bonus

class Developer(Employee):
    def __init__(self, name, employee_id, base_salary, project_count):
        super().__init__(name, employee_id, base_salary)
        self.__project_count = project_count

    def calculate_salary(self):
        return super().calculate_salary() + self.__project_count * 100

class Intern(Employee):
    def __init__(self, name, employee_id, base_salary, mentor):
        super().__init__(name, employee_id, base_salary)
        self.__mentor = mentor

    def calculate_salary(self):
        return 2000

class Company:
    def __init__(self):
        self.__employee_list = []

    def add_employee(self, e: Employee):
        self.__employee_list.append(e)

    def remove_employee(self, employee_id):
        for e in self.__employee_list:
            if e.id == employee_id:
                self.__employee_list.remove(e)
                break

    def get_total_salary(self):
        return sum(e.calculate_salary() for e in self.__employee_list)
    
    def list_all_employees(self):
        for e in self.__employee_list:
            print(e.get_details())


# tel_book = {"张三": "13000000001", "李四": "13000000002"}

# def save_contacts(contacts, filename):
#     with open(filename, "a", encoding="utf-8") as f:
#         for name, tel in tel_book.items():
#             f.write(f"{name}: {tel}\n")

# def load_contacts(filename):
#     tel_book2 = {}
#     with open(filename, "r", encoding="utf-8") as f:
#         lines = f.readlines()

#         for line in lines:
#             name, tel = line.strip().split(":")
#             tel_book2[name] = tel

#     return tel_book2

class Student:
    school_name = "第一中学"
    student_count = 0

    def __init__(self, name, age, class_name):
        self.__name = name
        self.__age = age
        self.__class_name = class_name

        Student.student_count += 1

    def introduce(self):
        print(f"{self.__name}的年龄是{self.__age}, 班级是{self.__class_name}")

    def have_birthday(self):
        print("生日快乐")
        self.__age += 1

    @classmethod
    def change_school(cls, new_name):
        cls.school_name = new_name

    @classmethod
    def get_student_count(cls):
        return cls.student_count

    @staticmethod
    def is_valid_age(age):
        if 6 <= age <= 18:
            print("年龄在6-18岁之间")
        else:
            print("年龄不在6-18岁之间")

class Goods:
    def __init__(self, title, price):
        self.__title = title
        self.__price = price

    @property
    def title(self):
        return self.__title

    @property
    def price(self):
        return self.__price

    def __str__(self):
        return self.__title

    # 打印列表时对列表内部每个对象使用
    def __repr__(self):
        return self.__title

class ShoppingCart:
    store_name = "百货大楼"
    total_carts = 0

    def __init__(self, owner: str, items: list[Goods], total_price = 0):
        self.__owner = owner
        self.__items = []
        self.__total_price = 0

        ShoppingCart.total_carts += 1

    def add_item(self, item_name, price):
        self.__items.append(Goods(item_name, price))
        self.__total_price += price

    def remove_item(self, item_name):
        for item in self.__items:
            if item_name == item.title:
                price = item.price
                self.__total_price -= price
                self.__items.remove(item)
                break

    def show_cart(self):
        print(f"商品有:{self.__items}总价为{self.__total_price}")

    @classmethod
    def set_store_name(cls, new_name):
        cls.store_name = new_name

    @classmethod
    def show_total_carts(cls):
        print(f"创建了{cls.total_carts}个购物车")

    @staticmethod
    def calculate_discount(price, discount_rate):
        return price * discount_rate

cart1 = ShoppingCart("张三", None, 0)
cart2 = ShoppingCart("李四", None, 0)

cart1.add_item("苹果", 5)
cart1.add_item("香蕉", 6)
cart1.add_item("牛奶", 10)

cart2.add_item("电脑", 5000)
cart2.add_item("鼠标", 100)
cart2.add_item("键盘", 300)
cart2.add_item("耳机", 200)

cart1.show_cart()
    