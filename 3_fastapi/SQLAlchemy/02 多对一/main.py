from database import SessionLocal
from models import Department, Employee, Job

def read_data_all_emp():
    with SessionLocal() as session:
        try:
            employees = session.query(Employee).all()

            for emp in employees:
                print(emp.ename, emp.department.dname if emp.department else None, emp.job.jname if emp.job else None)
        except Exception as e:
            print(f"查询失败: {e}")

def read_data_all_dept():
    with SessionLocal() as session:
        try:
            depts = session.query(Department).all()

            for dept in depts:
                emps = dept.employees
                print(dept.dname, [emp.ename for emp in emps])
                
        except Exception as e:
            print(f"查询失败: {e}")

def read_data_all_job():
    with SessionLocal() as session:
        try:
            jobs = session.query(Job).all()

            for job in jobs:
                emps = job.employees
                print(job.jname, [emp.ename for emp in emps])
        except Exception as e:
            print(f"查询失败: {e}")


if __name__ == "__main__":
    read_data_all_job()