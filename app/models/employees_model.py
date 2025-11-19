from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    DECIMAL,
    Enum,
    text,
    MetaData
)
from sqlalchemy.orm import declarative_base

sdnet_metadata = MetaData()
SDNetBase = declarative_base(metadata=sdnet_metadata)


class Employee(SDNetBase):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)

    fullname = Column(String(100), nullable=False)
    mobile = Column(String(20), nullable=False, unique=True)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)

    city = Column(String(50), nullable=True)
    village = Column(String(50), nullable=True)
    street = Column(String(100), nullable=True)
    building = Column(String(50), nullable=True)
    floor = Column(String(10), nullable=True)

    type = Column(
        Enum("home", "work", "other", name="employee_address_type"),
        nullable=False,
        server_default="home"
    )

    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    def __repr__(self):
        return f"<Employee id={self.id} username='{self.username}'>"
    

class EmployeeSalary(SDNetBase):
    __tablename__ = "employee_salary"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Employee username (no FK)
    employee_username = Column(String(100), nullable=False)

    # Salary month (stored as YYYY-MM-01)
    salary_month = Column(Date, nullable=False)

    # Salary details
    base_salary = Column(DECIMAL(12, 2), nullable=True)
    payment = Column(DECIMAL(12, 2), nullable=True)
    bonus = Column(DECIMAL(12, 2), nullable=True)
    deductions = Column(DECIMAL(12, 2), nullable=True)

    # Final salary
    net_salary = Column(DECIMAL(12, 2), nullable=False)

    # Currency enum
    currency = Column(
        Enum("USD", "LBP", name="salary_currency"),
        nullable=False,
        server_default="LBP"
    )

    # Payment method enum
    payment_method = Column(
        Enum("cash", "card", "bank", "other", name="salary_payment_method"),
        nullable=False,
        server_default="cash"
    )

    # Notes
    notes = Column(String(255), nullable=True)

    # Audit timestamps
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )
