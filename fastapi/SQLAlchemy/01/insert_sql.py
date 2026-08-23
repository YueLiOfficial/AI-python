from database import SessionLocal
from models import Department, Employee
from datetime import date

'''
    添加操作：
        (1) 创建会话session
        (2) 实例化对象
        (3) 调用session.add(单条数据)或者session.add_all([多条数据])
        (4) 调用session.commit()提交事务
        (5) 调用session.refresh(对象)获取数据库中最新的数据
'''
def insert_department_data():
    new_dept = Department(dname = "安保部", description = "负责公司安保工作")

    with SessionLocal() as session:
        try:
            session.add(new_dept)
            session.commit()
            session.refresh(new_dept)

            print(f"添加了部门: {new_dept.dname}, 部门ID是: {new_dept.did}, 部门职责是: {new_dept.description}")
        except Exception as e:
            session.rollback()
            print(f"添加失败: {e}")

def insert_employee_data():
    # 员工1
    emp1 = Employee(
        ename = "张三",
        salary = 15000,
        birthday = date(1995, 5, 1),
        gender = "男",
        tel = "13100000020",
        email = "zhangsan@aiguigu.com",
        hiredate = date(2003, 1, 1),
        did = 9
    )

    # 员工2：同部门的另一个员工
    emp2 = Employee(
        ename="李四",
        salary = 15000,
        birthday = date(1996,6,1),
        gender = "男",
        tel = "18396587546",
        email = "lisi@atguigu.com",
        work_place="北京,深圳",
        hiredate=date(2023, 1, 1),
        did=9
    )

    # 员工3：其他部门的另一个员工
    emp3 = Employee(
        ename="王五",
        salary = 15000,
        birthday = date(1996,6,1),
        gender = "男",
        tel = "18396587545",
        email = "wangwu@atguigu.com",
        work_place="北京,深圳",
        hiredate=date(2023, 1, 1),
        did=1
    )
    with SessionLocal() as session:
        try:
            session.add_all([emp1, emp2, emp3])
            session.commit()

            for emp in [emp1, emp2, emp3]:
                session.refresh(emp)

            print(f"新增员工1: ID={emp1.eid}, 姓名={emp1.ename}, 所属部门={emp1.did}")
            print(f"新增员工2: ID={emp2.eid}, 姓名={emp2.ename}, 所属部门={emp2.did}")
            print(f"新增员工3: ID={emp3.eid}, 姓名={emp3.ename}, 所属部门={emp3.did}")
        except Exception as e:
            session.rollback()
            print(f"添加失败: {e}")

if __name__ == "__main__":
    insert_department_data()