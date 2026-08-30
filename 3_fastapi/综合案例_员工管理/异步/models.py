from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

class Base(DeclarativeBase):
    pass

class Department(Base):
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    employee = relationship(
        argument="Employee",
        back_populates="department",
        lazy="selectin"
    )


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(nullable=False)
    department_id: Mapped[int | None] = mapped_column(ForeignKey("department.id", ondelete="SET NULL", onupdate="CASCADE"))

    department = relationship(
        argument="Department",
        back_populates="employee",
        lazy="joined"
    )