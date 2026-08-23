from database import SessionLocal
from models import Department, Employee, Job
from sqlalchemy import text, and_, or_, func
from datetime import date

# 使用sql原生语句查询
def read_data_by_sql():
    with SessionLocal() as session:
        try:
            result = session.execute(
                text("SELECT * FROM t_employee WHERE gender = '女'")
            )

            rows = result.fetchall()

            for row in rows:
                print(row)

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

# 根据主键查询
def read_data_by_primary_key():
    with SessionLocal() as session:
        try:
            # 查询id = 1的部门, 返回的是部门对象
            dept = session.get(Department, 1)

            print(dept)

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

# 根据单个条件查询
def read_data_by_filter():
    with SessionLocal() as session:
        try:
            results = session.query(Employee).filter(Employee.did ==1).all()

            for res in results:
                print(res.ename, res.did)

        except Exception as e:
            print(f"查询失败: {e}")

# 根据多个条件查询
def read_data_and_or():
    with SessionLocal() as session:
        try:
            # 薪资[10000,15000]且部门编号为1的员工（and_）
            results = session.query(Employee).filter(and_(Employee.salary.between(10000, 15000), Employee.did == 1)).all()

            print(f"符合薪资[10000, 15000]且部门编号为1的员工")
            for res in results:
                print(res.ename, res.salary, res.did)

            # 属于2号部门或薪资高于20000的员工（or_）
            results = session.query(Employee).filter(or_(Employee.did == 2, Employee.salary > 20000)).all()

            print(f"符合属于2号部门或薪资高于20000的员工")
            for res in results:
                print(res.ename, res.salary, res.did)

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

# 去重
def read_data_distinct():
    # 查询所有有员工的部门编号（去重）
    with SessionLocal() as session:
        try:
            # distinct()需要放在.all()前边
            results = session.query(Employee.did).distinct().all()

            print(f"部门编号: {results}")

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

# 分组查询

'''
相当于：
    SELECT did AS "部门ID", 
    MAX(salary) AS "最高薪资", 
    AVG(salary) AS "平均薪资" 
    FROM t_employee GROUP BY did;
'''
def read_data_group_by():
    with SessionLocal() as session:
        try:
            # 按照员工部门id分组，查询每个部门的最高薪资和平均薪资
            results = session.query(Employee.did.label("部门id"),
                                    func.max(Employee.salary).label("最高薪资"),
                                    func.avg(Employee.salary).label("平均薪资")
                                    ).group_by(Employee.did)

            col_names = [col["name"] for col in results.column_descriptions]
            
            print(col_names)
            for res in results:
                print(res)

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

def read_data_subquery():
    with SessionLocal() as session:
        try:
             # 步骤1：定义子查询：查询最高薪资值
            sub_result = session.query(func.max(Employee.salary).label("max_salary")).subquery()
            # 步骤2：主查询  ，子查询对象.c.字段名
            result = session.query(Employee).filter(Employee.salary == sub_result.c.max_salary).first()

            print(result.ename, result.salary)

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

# 查询部门和孙洪亮一样的员工
def read_data_subquery2():
    with SessionLocal() as session:
        try:
            sub_result = session.query(Employee.did).filter(Employee.ename == "孙洪亮").subquery()

            results = session.query(Employee).filter(Employee.did == sub_result.c.did).all()

            for res in results:
                print(f"{res.ename}, {res.did}")

        except Exception as e:
            session.rollback()
            print(f"查询失败: {e}")

if __name__ == "__main__":
    read_data_subquery2()