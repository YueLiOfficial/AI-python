from database import SessionLocal
from models import Department, Employee, Job

'''
(1) 内连接: session.query(A表, B表).join(A表或B表, 关联条件).all()

    - query(A表, B表)：等价于联合查询的`select A表.*, B表.*`
    - join(A表或B表, 关联条件) ：等价于 `A表 inner join B表 on 关联条件`, 此时join()中写A或B表都一样
'''
def inner_join_demo():
    with SessionLocal() as session:
        try:
            results = session.query(Employee, Department).join(Employee, Employee.did == Department.did).all()

            for emp, dept in results:
                print(emp.ename, dept.dname)
        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

'''
(2) 左连接: session.query(A表, B表).outerjoin(B表, 关联条件).all 
            等价于
            A表 LEFT JOIN B表 ON 关联条件
'''
def left_join_demo():
    with SessionLocal() as session:
        try:
            results = session.query(Employee, Department).outerjoin(Department, Employee.did == Department.did).all()

            for emp, dept in results:
                print(emp.ename, dept.dname if dept else None)

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

'''
(3) 右连接: session.query(A表, B表).join(B表, 关联条件, isouter=True).all()
            等价于
            B表 RIGHT JOIN A表 ON 关联条件

            session.query(A表, B表).select_from(A表).outerjoin(B表, 关联条件).all()
            等价于
            B表 RIGHT JOIN A表 ON 关联条件
'''
def right_join_demo():
    with SessionLocal() as session:
        try:
            results = session.query(Employee, Department).join(Department, Employee.did == Department.did, isouter=True).all()

            for emp, dept in results:
                print(emp.ename, dept.dname if dept else None)

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

def right_join_demo2():
    with SessionLocal() as session:
        try:
            results = session.query(Employee, Department).select_from(Employee).outerjoin(Department, Employee.did == Department.did).all()

            for emp, dept in results:
                print(emp.ename, dept.dname if dept else None)

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

'''
(4) union: 左连接查询A表所有 union 右连接查询B表所有
            左连接查询A表所有 union 左连接查询B表所有
            ...
'''

def read_data_full_join():
    with SessionLocal() as session:
        try:
            # 左连接查询Employee所有内容 union 右连接查询Department所有内容
            results = session.query(Employee, Department).outerjoin(Department, Employee.did == Department.did)\
                        .union(
                            session.query(Employee, Department).select_from(Department).outerjoin(Employee, Employee.did == Department.did)
                        ).all()

            for emp, dept in results:
                print(emp.ename if emp else None, dept.dname if dept else None)

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

if __name__ == "__main__":
    read_data_full_join()