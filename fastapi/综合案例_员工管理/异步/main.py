from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, HTTPException
from database import SessionLocal
from models import Department, Employee
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

app = FastAPI(title="企业员工管理系统")

class DepartmentCreate(BaseModel):
    name: str

class EmployeeCreate(BaseModel):
    name: str
    age: int
    department_id: int | None = None

class DepartmentResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class EmployeeResponse(BaseModel):
    id: int
    name: str
    age: int
    department_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

@app.get("/")
async def root():
    return "Welcome"

@app.post("/department/add", response_model = DepartmentResponse)
async def add_department(dept: DepartmentCreate):
    new_dept = Department(**dept.model_dump())

    async with SessionLocal() as session:
        try:
            session.add(new_dept)
            await session.commit()
            await session.refresh(new_dept)
            return new_dept
        except IntegrityError:
            await session.rollback()    
            raise HTTPException(
                status_code=400,
                detail="部门已存在"
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

@app.post("/employee/add", response_model = EmployeeResponse)
async def add_employee(emp: EmployeeCreate):
    new_emp = Employee(**emp.model_dump())

    async with SessionLocal() as session:
        try:
            session.add(new_emp)
            await session.commit()
            await session.refresh(new_emp)
            return new_emp
        except IntegrityError:
            await session.rollback()    
            raise HTTPException(
                status_code=400,
                detail="员工已存在或指定的部门不存在"
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

@app.get("/department/get", response_model=DepartmentResponse)
async def get_department_by_id(did: int):
    async with SessionLocal() as session:
        dept = await session.get(Department, did)
        if dept is None:
            raise HTTPException(
                status_code=404,
                detail="部门不存在"
            )
        
        return dept

@app.get("/department/all", response_model=list[DepartmentResponse])
async def get_department_all():
    async with SessionLocal() as session:
        results = await session.execute(select(Department))
        depts = results.scalars().all()
        return depts

@app.get("/employee/all", response_model=list[EmployeeResponse])
async def get_employee_all():
    async with SessionLocal() as session:
        result = await session.execute(select(Employee))
        emps = result.scalars().all()
        return emps

@app.put("/department/update")
async def update_department(did: int, new_name: str):
    async with SessionLocal() as session:
        try:
            result = await session.execute(select(Department).where(Department.id == did))
            dept = result.scalar_one_or_none()
            if dept is None:
                raise HTTPException(
                    status_code=404,
                    detail="部门不存在"
                )
            dept.name = new_name
            await session.commit()
            return {"result": "success", "content": f"将部门ID为{did}的部门改为{new_name}"}
        except HTTPException:
            await session.rollback()
            raise
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail="部门已存在"
            )
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

@app.delete("/department/del")
async def del_department(did: int):
    async with SessionLocal() as session:
        try:
            result = await session.execute(select(Department).where(Department.id == did))
            dept = result.scalar_one_or_none()
            if dept is None:
                raise HTTPException(
                    status_code=404,
                    detail="部门不存在"
                )
            await session.delete(dept)
            await session.commit()
            return {"result": "success", "content": f"已删除部门ID为{did}的部门"}
        except HTTPException:
            await session.rollback()
            raise
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )