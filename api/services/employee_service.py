from sqlmodel import Session, select
from api.database.database import engine

from api.models import (
    User, Employee, Plan, PlanTier,
    PolicyCategory
)


# -------------------------------------------------
# 1. Get full employee insurance coverage
# -------------------------------------------------
def get_employee_coverage(username: str):
    with Session(engine) as session:

        # 1. Find user
        user = session.exec(
            select(User).where(User.username == username)
        ).first()
        if not user:
            return {"error": "User not found"}

        # 2. Find employee record
        employee = session.exec(
            select(Employee).where(Employee.user_id == user.user_id)
        ).first()
        if not employee:
            return {"error": "Not an employee"}

        # 3. Load assigned plan
        plan = session.get(Plan, employee.plan_id)
        if not plan:
            return {"error": "No plan assigned"}

        # 4. Load plan tiers (GTL, GCI, GPA, GHS, etc.)
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


# -------------------------------------------------
# 2. Get ward class + limits (GHS only)
# -------------------------------------------------
def get_ward_class_and_limits(username: str):
    with Session(engine) as session:

        # 1. Find user
        user = session.exec(
            select(User).where(User.username == username)
        ).first()
        if not user:
            return {"error": "User not found"}

        # 2. Find employee
        employee = session.exec(
            select(Employee).where(Employee.user_id == user.user_id)
        ).first()
        if not employee:
            return {"error": "Not an employee"}

        # 3. Load plan
        plan = session.get(Plan, employee.plan_id)
        if not plan:
            return {"error": "No plan assigned"}

        # 4. Load only GHS category
        ghs_category = session.exec(
            select(PolicyCategory).where(PolicyCategory.category_name == "GHS")
        ).first()
        if not ghs_category:
            return {"error": "No GHS category defined"}

        tier = session.exec(
            select(PlanTier)
            .where(PlanTier.plan_id == plan.plan_id)
            .where(PlanTier.category_id == ghs_category.category_id)
        ).first()

        if not tier:
            return {"error": "No hospitalisation coverage (GHS) for this plan"}

        return {
            "ward_class": "B1/B2/A (depends on your model)",  # update as needed
            "annual_limit": tier.sum_insured,
            "category": "GHS – Hospitalisation Plan"
        }


# # file: api/services/employee_service.py
# from sqlmodel import Session, select
# from api.database.database import engine
# # from api.database.database import SessionLocal

# from api.models import (
#     User, Employee, Plan, PlanTier,
#     PolicyCategory, BiddingRound, Bid
# )

# def get_employee_coverage(username: str):
#     with Session(engine) as session:
#         user = session.exec(
#             select(User).where(User.username == username)
#         ).first()
#         if not user:
#             return {"error": "User not found"}

#         employee = session.exec(
#             select(Employee).where(Employee.user_id == user.user_id)
#         ).first()
#         if not employee:
#             return {"error": "Not an employee"}

#         plan = session.get(Plan, employee.plan_id)
#         if not plan:
#             return {"error": "No plan assigned"}

#         tiers = session.exec(
#             select(PlanTier).where(PlanTier.plan_id == plan.plan_id)
#         ).all()

#         coverage = []
#         for tier in tiers:
#             category = session.get(PolicyCategory, tier.category_id)
#             coverage.append({
#                 "category": category.category_name,
#                 "sum_insured": tier.sum_insured
#             })

#         return {
#             "employee_name": employee.name,
#             "employee_code": employee.employee_code,
#             "assigned_plan": plan.plan_name,
#             "insurer_id": plan.insurer_id,
#             "coverage": coverage
#         }


# def get_ward_class_and_limits(username: str):
#     with Session(engine) as session:
#         user = session.exec(select(User).where(User.username == username)).first()
#         if not user:
#             return {"error": "User not found"}

#         employee = session.exec(
#             select(Employee).where(Employee.user_id == user.user_id)
#         ).first()
#         plan = session.get(Plan, employee.plan_id)

#         tiers = session.exec(
#             select(PlanTier).where(PlanTier.plan_id == plan.plan_id)
#         ).all()

#         results = []
#         for t in tiers:
#             category = session.get(PolicyCategory, t.category_id)
#             results.append({
#                 "category": category.category_name,
#                 "limit": t.sum_insured
#             })

#         return results
# file: api/services/employee_service.py