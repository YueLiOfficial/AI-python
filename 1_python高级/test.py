from datetime import datetime

class TodoList():
    total_tasks = 0
    total_complete_tasks = 0

    def __init__(self, owner, task_type):
        self.__owner = owner
        self.__task_type = task_type
        self.__tasks = []
        self.__created_time = datetime.now()

    def add_task(self, task_name):
        self.__tasks.append({"task": task_name, "completed": False})
        TodoList.total_tasks += 1

    def complete_task(self, task_name):
        for task in self.__tasks:
            if task["task"] == task_name:
                if not task["completed"]:
                    task["completed"] = True
                    TodoList.total_complete_tasks += 1
                    return True

        return False

    def show_tasks(self, show_all=True):
        if show_all:
            for task in self.__tasks:
                print(task)
        else:
            for task in self.__tasks:
                if task["completed"] == False:
                    print(task)

    def delete_task(self, task_name):
        for task in self.__tasks:
            if task["task"] == task_name:
                # 如果删除的是已完成的任务
                if task["completed"] == True:
                    TodoList.total_complete_tasks -= 1

                self.__tasks.remove(task)
                TodoList.total_tasks -= 1
                return True

        return False

    def get_progress(self):
        if not self.__tasks:
            return "0%"
        
        count = 0
        for task in self.__tasks:
            if task["completed"] == True:
                count += 1

        return f"{count / len(self.__tasks) * 100}%"

    @classmethod
    def get_total_tasks(cls):
        return cls.total_tasks

    @classmethod
    def get_total_progress(cls):
        return f"{cls.total_complete_tasks / cls.total_tasks * 100}%"


class Vehicle:
    def __init__(self, base_rate, rent_days):
        self._base_rate = base_rate
        self._rent_days = rent_days

    def calculate_cost(self):
        return self._base_rate * self._rent_days

    def set_rent_days(self, days):
        self._rent_days = days

class Car(Vehicle):
    def calculate_cost(self):
        return super().calculate_cost() + self._rent_days * 50

class Truck(Vehicle):
    def calculate_cost(self, km):
        return super().calculate_cost() + km * 5

class Fighter:
    def __init__(self, strength):
        self.__strength = strength

    def attack(self):
        print("物理攻击")

    def get_power(self):
        return self.__strength

    @property
    def strength(self):
        return self.__strength

class Mage:
    def __init__(self, intelligence):
        self.__intelligence = intelligence

    def cast_spell(self):
        print("火球术")

    def get_power(self):
        return self.__intelligence

    @property
    def intelligence(self):
        return self.__intelligence

class Healer:
    def __init__(self, wisdom):
        self.__wisdom = wisdom

    def heal(self):
        print("治疗术")

    def get_power(self):
        return self.__wisdom

    @property
    def wisdom(self):
        return self.__wisdom

class Paladin(Fighter, Healer):
    def __init__(self, strength, wisdom):
        Fighter.__init__(self, strength)
        Healer.__init__(self, wisdom)

    def get_power(self):
        return self.strength * 0.6 + self.wisdom * 0.4

    def holy_light(self):
        print("圣光普照")

class Spellblade(Fighter, Mage):
    def __init__(self, strength, intelligence):
        Fighter.__init__(self, strength)
        Mage.__init__(self, intelligence)

    def get_power(self):
        return self.strength * 0.5 + self.intelligence * 0.5

    def attack(self):
        Mage.cast_spell(self)
        Fighter.attack(self)

def show_power(character):
    print(character.get_power())


# count = 0
# total_score = 0
# while True:
#     try:
#         score = input("请输入分数: ")

#         if score == "结束":
#             break

#         score = int(score)

#         count += 1
#     except ValueError:
#         print("输入的数为非整数")
#     else:
#         total_score += score
#     finally:
#         print(f"当前已输入{count}个有效成绩")

# print(total_score / count)


# numbers = [23, 45, 67, 89, 12, 34, 56, 78, 90, 21]

# while True:
#     try:
#         index_str = input("请输入索引: ")

#         if index_str == "退出":
#             break

#         index = int(index_str)
#         if index < 0 or index > 9:
#             raise IndexError("索引超出范围, 有效范围是0-9")
#     except ValueError:
#         print("请输入整数索引")
#     except IndexError as e:
#         print(e)
#     else:
#         print(numbers[index])
#     finally:
#         print("索引访问尝试完成")



