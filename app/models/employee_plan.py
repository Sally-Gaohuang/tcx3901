from sqlmodel import SQLModel, Field, Relationship

class EmployeePlan(SQLModel, table=True):
    employee_id: int = Field(foreign_key="employee.id", primary_key=True)
    plan_id: int = Field(foreign_key="plan.id", primary_key=True)
