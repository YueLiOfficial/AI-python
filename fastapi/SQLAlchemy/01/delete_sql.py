from database import SessionLocal
from models import Department, Employee

# 删除员工
def delete_employee_data():
    with SessionLocal() as session:
        try:
            emp = session.query(Employee).filter(Employee.ename == "王五").first()
            if emp:
                session.delete(emp)
                session.commit()
                print(f"已删除员工{emp.ename}")
        except Exception as e:
            session.rollback()
            print(f"删除失败: {e}")

# 删除部门
def delete_department_data():
    with SessionLocal() as session:
        try:
            dept = session.query(Department).filter(Department.dname == "安保部").first()
            if dept:
                session.delete(dept)
                session.commit()
                print(f"已删除部门{dept.dname}")
        except Exception as e:
            session.rollback()
            print(f"删除失败: {e}")

if __name__ == "__main__":
    delete_department_data()