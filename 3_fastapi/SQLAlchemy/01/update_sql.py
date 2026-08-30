from database import SessionLocal
from models import Department, Employee

# 修改单个
def update_employee_data():
    with SessionLocal() as session:
        try:
            emp = session.query(Employee).filter(Employee.ename == "王五").first()
            if emp:
                print(f"修改前, {emp.ename}的工资是{emp.salary}")
                emp.salary += 2000
                print(f"修改后，{emp.ename}的工资是{emp.salary}")
                session.commit() # 提交更新
        except Exception as e:
            session.rollback()
            print(f"修改失败: {e}")

# 修改多个
def update_employee_data_many():
    with SessionLocal() as session:
        try:
            employees = session.query(Employee).filter(Employee.did == 9).all()
            for emp in employees:
                print(f"修改前, {emp.ename}的工资是{emp.salary}")
                emp.salary += 2000
                print(f"修改后，{emp.ename}的工资是{emp.salary}")
            # 所有数据修改完成后提交一次commit, 不需要每次修改都提交
            session.commit() # 提交更新
        except Exception as e:
            session.rollback()
            print(f"修改失败: {e}")

if __name__ == "__main__":
    update_employee_data_many()