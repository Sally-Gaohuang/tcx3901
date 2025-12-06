# file: api/services/admin_service.py
from sqlmodel import Session, select, func
from app.database.database import engine
# from api.database.database import SessionLocal
from app.models import (
    User, Employee, Plan, PlanTier,
    PolicyCategory, Bid
)

MIN_FWMI_AMOUNT = 15000   # Example MOM requirement

# ---------------------------
# Employee CRUD
# ---------------------------

def create_employee(data: dict):
    with Session(engine) as session:
        employee = Employee(**data)
        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee


def update_employee(emp_id: int, data: dict):
    with Session(engine) as session:
        employee = session.get(Employee, emp_id)
        if not employee:
            return {"error": "Employee not found"}

        for key, value in data.items():
            setattr(employee, key, value)

        session.add(employee)
        session.commit()
        session.refresh(employee)
        return employee


def deactivate_employee(emp_id: int):
    with Session(engine) as session:
        employee = session.get(Employee, emp_id)
        if not employee:
            return {"error": "Employee not found"}

        employee.active = False
        session.commit()
        return {"message": "Employee deactivated"}


# ---------------------------
# Automatic plan assignment
# ---------------------------

def assign_plan_based_on_designation(employee: Employee):
    with Session(engine) as session:
        designation = employee.department   # example logic
        tier = session.exec(
            select(PlanTier).where(PlanTier.plan_id == employee.plan_id)
        ).first()
        return tier


# ---------------------------
# FWMI Compliance
# ---------------------------

def get_fwmi_non_compliant():
    with Session(engine) as session:
        result = session.exec(
            select(Employee, PlanTier)
            .join(Plan, Plan.plan_id == Employee.plan_id)
            .join(PlanTier, PlanTier.plan_id == Plan.plan_id)
            .join(PolicyCategory, PolicyCategory.category_id == PlanTier.category_id)
            .where(
                PolicyCategory.category_name == "FWMI",
                PlanTier.sum_insured < MIN_FWMI_AMOUNT
            )
        ).all()

        return [
            {
                "employee_id": emp.employee_id,
                "employee_name": emp.name,
                "coverage": tier.sum_insured
            }
            for emp, tier in result
        ]


# ---------------------------
# Coverage Reports
# ---------------------------

def generate_coverage_report():
    with Session(engine) as session:
        report = session.exec(
            select(
                PolicyCategory.category_name,
                func.count(PlanTier.tier_id)
            )
            .join(PlanTier, PlanTier.category_id == PolicyCategory.category_id)
            .group_by(PolicyCategory.category_name)
        ).all()

        return [{"category": c, "count": cnt} for c, cnt in report]
