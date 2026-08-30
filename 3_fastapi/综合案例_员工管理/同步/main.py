from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from database import SessionLocal
from models import Department, Employee
from sqlalchemy.exc import IntegrityError

app = FastAPI(title="企业员工管理系统")

class DepartmentCreate(BaseModel):
    name: str

class DepartmentResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class EmployeeCreate(BaseModel):
    name: str
    age: int
    department_id: int | None = None

class EmployeeResponse(BaseModel):
    id: int
    name: str
    age: int
    department_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


@app.get("/")
def root():
    return f"Welcome!"

@app.post("/department/add", response_model=DepartmentResponse)
def add_department(dept: DepartmentCreate):
    new_department = Department(**dept.model_dump())

    with SessionLocal() as session:
        try:
            session.add(new_department)
            session.commit()
            session.refresh(new_department)
            return new_department
        except IntegrityError:
            session.rollback()

            raise HTTPException(
                status_code=400,
                detail="部门已存在"
            )
        except Exception as e:
            session.rollback()

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

@app.post("/employee/add", response_model=EmployeeResponse)
def add_employee(emp: EmployeeCreate):
    new_emp = Employee(**emp.model_dump())

    with SessionLocal() as session:
        try:
            session.add(new_emp)
            session.commit()
            session.refresh(new_emp)
            return new_emp
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400,
                detail="员工已存在、或指定的部门不存在"
            )
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

@app.get("/department/get", response_model=DepartmentResponse)
def get_department_by_id(did: int):
    with SessionLocal() as session:
        result = session.get(Department, did)
        if result is None:
            raise HTTPException(
                status_code=404,
                detail="部门不存在"
            )
        return result


@app.get("/department/all", response_model=list[DepartmentResponse])
def get_department_all():
    with SessionLocal() as session:
        results = session.query(Department).all()
        return results


@app.get("/employee/all", response_model=list[EmployeeResponse])
def get_employee_all():
    with SessionLocal() as session:
        results = session.query(Employee).all()
        return results


@app.put("/department/update")
def update_department(did: int, new_name: str):
    with SessionLocal() as session:
        try:
            dept = session.query(Department).filter(Department.id == did).first()
            if dept is None:
                raise HTTPException(
                    status_code=404,
                    detail="部门不存在"
                )
            
            dept.name = new_name
            session.commit()
            return {"result": "success", "content":f"将部门ID为{did}的部门修改为{new_name}"}

        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400,
                detail="部门名称已存在"
            )
        except HTTPException:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

@app.delete("/department/del")
def del_department(did: int):
    with SessionLocal() as session:
        try:
            dept = session.query(Department).filter(Department.id == did).first()
            if dept is None:
                raise HTTPException(
                    status_code=404,
                    detail="部门不存在"
                )
            session.delete(dept)
            session.commit()
            return {"result": "success", "content": f"删除了部门ID为{did}的部门"}
        except HTTPException:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )