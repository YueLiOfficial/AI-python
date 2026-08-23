from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Enum, Numeric, ForeignKey, CHAR
from sqlalchemy.dialects.mysql import SET
from datetime import date
from decimal import Decimal

class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "t_department"

    did: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dname: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(200))

    def __str__(self):
        return f"{self.did}, {self.dname}, {self.description}"

class Employee(Base):
    __tablename__ = "t_employee"

    eid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ename: Mapped[str] = mapped_column(String(20), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)
    commission_pct: Mapped[Decimal | None] = mapped_column(Numeric(3, 2))
    birthday: Mapped[date] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(Enum("男", "女"), default="男", nullable=False)
    tel: Mapped[str] = mapped_column(CHAR(11), nullable=False)
    email: Mapped[str] = mapped_column(String(32), nullable=False)
    address: Mapped[str | None] = mapped_column(String(150))
    work_place: Mapped[str] = mapped_column(SET("北京", "深圳", "上海", "武汉", "成都", "西安"), default="北京", nullable=False)
    hiredate: Mapped[date] = mapped_column(nullable=False)
    job_id: Mapped[int | None] = mapped_column(ForeignKey("t_job.jid", ondelete="SET NULL", onupdate="CASCADE"))
    mid: Mapped[int | None] = mapped_column(ForeignKey("t_employee.eid", ondelete="SET NULL", onupdate="CASCADE"))
    did:Mapped[int | None] = mapped_column(ForeignKey("t_department.did", ondelete="SET NULL", onupdate="CASCADE"))

class Job(Base):
    __tablename__ = "t_job"

    jid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    jname: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(200))