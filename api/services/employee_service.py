# file: api/services/employee_service.py
from sqlmodel import Session, select
from api.database.database import engine
from api.models import (
    User, Employee, Plan, PlanTier,
    PolicyCategory, BiddingRound, Bid
)

def get_employee_coverage(username: str):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == username)
        ).first()
        if not user:
            return {"error": "User not found"}

        employee = session.exec(
            select(Employee).where(Employee.user_id == user.user_id)
        ).first()
        if not employee:
            return {"error": "Not an employee"}

        plan = session.get(Plan, employee.plan_id)
        if not plan:
            return {"error": "No plan assigned"}

        tiers = session.exec(
            select(PlanTier).where(PlanTier.plan_id == plan.plan_id)
        ).all()

        coverage = []
        for tier in tiers:
            category = session.get(PolicyCategory, tier.category_id)
            coverage.append({
                "category": category.category_name,
                "sum_insured": tier.sum_insured
            })

        return {
            "employee_name": employee.name,
            "employee_code": employee.employee_code,
            "assigned_plan": plan.plan_name,
            "insurer_id": plan.insurer_id,
            "coverage": coverage
        }


def get_ward_class_and_limits(username: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            return {"error": "User not found"}

        employee = session.exec(
            select(Employee).where(Employee.user_id == user.user_id)
        ).first()
        plan = session.get(Plan, employee.plan_id)

        tiers = session.exec(
            select(PlanTier).where(PlanTier.plan_id == plan.plan_id)
        ).all()

        results = []
        for t in tiers:
            category = session.get(PolicyCategory, t.category_id)
            results.append({
                "category": category.category_name,
                "limit": t.sum_insured
            })

        return results
