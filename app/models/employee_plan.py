# file: app/models/employee_plan.py

from sqlmodel import SQLModel, Field

class EmployeePlan(SQLModel, table=True):
    """
    Link table for many-to-many relationship:
    One Employee ⇔ Many Plans
    One Plan ⇔ Many Employees
    """
    employee_id: int = Field(
        foreign_key="employee.employee_id",
        primary_key=True
    )
    plan_id: int = Field(
        foreign_key="plan.plan_id",
        primary_key=True
    )
