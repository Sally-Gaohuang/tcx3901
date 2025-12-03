from sqlmodel import Session, select
from database import engine
from api.models import User, Plan, PolicyCategory

from api.models.models import (
    User, Employee, PolicyCategory, Plan, PlanTier,
    BiddingRound, Bid
)


def seed_data():
    with Session(engine) as session:

        # ---- USERS ----
        admin = User(username="admin", password_hash="admin123", role="admin")
        insurer_aia = User(username="aia", password_hash="aia123", role="insurer")
        insurer_singlife = User(username="singlife", password_hash="sing123", role="insurer")
        emp1_user = User(username="emp001", password_hash="emp001pass", role="employee")

        session.add(admin)
        session.add(insurer_aia)
        session.add(insurer_singlife)
        session.add(emp1_user)
        session.commit()

        # ---- EMPLOYEES ----
        emp1 = Employee(
            user_id=emp1_user.user_id,
            employee_code="EE001",
            name="Sally Employee",
            department="HR",
            age=35,
            gender="Female"
        )
        session.add(emp1)
        session.commit()

        # ---- POLICY CATEGORIES (GTL, GCI, GHS, GPA, FWMI) ----
        categories = [
            PolicyCategory(category_name="GTL"),
            PolicyCategory(category_name="GCI"),
            PolicyCategory(category_name="GHS"),
            PolicyCategory(category_name="GPA"),
            PolicyCategory(category_name="FWMI")
        ]
        session.add_all(categories)
        session.commit()

        # Fetch categories
        cat_gtl = session.exec(select(PolicyCategory).where(PolicyCategory.category_name == "GTL")).first()
        cat_gci = session.exec(select(PolicyCategory).where(PolicyCategory.category_name == "GCI")).first()
        cat_ghs = session.exec(select(PolicyCategory).where(PolicyCategory.category_name == "GHS")).first()
        cat_gpa = session.exec(select(PolicyCategory).where(PolicyCategory.category_name == "GPA")).first()
        cat_fwmi = session.exec(select(PolicyCategory).where(PolicyCategory.category_name == "FWMI")).first()

        # ---- PLANS (Plan 1 and Plan 2 from AIA & Singlife) ----
        plan1 = Plan(plan_name="Plan A - AIA", insurer_id=insurer_aia.user_id)
        plan2 = Plan(plan_name="Plan B - Singlife", insurer_id=insurer_singlife.user_id)

        session.add_all([plan1, plan2])
        session.commit()

        # ---- PLAN TIERS ----
        tiers = [
            PlanTier(plan_id=plan1.plan_id, category_id=cat_gtl.category_id, sum_insured=30000),
            PlanTier(plan_id=plan1.plan_id, category_id=cat_gci.category_id, sum_insured=10000),
            PlanTier(plan_id=plan1.plan_id, category_id=cat_ghs.category_id, sum_insured=70000),
            PlanTier(plan_id=plan1.plan_id, category_id=cat_gpa.category_id, sum_insured=5000),
            PlanTier(plan_id=plan1.plan_id, category_id=cat_fwmi.category_id, sum_insured=60000),

            PlanTier(plan_id=plan2.plan_id, category_id=cat_gtl.category_id, sum_insured=25000),
            PlanTier(plan_id=plan2.plan_id, category_id=cat_gci.category_id, sum_insured=8000),
            PlanTier(plan_id=plan2.plan_id, category_id=cat_ghs.category_id, sum_insured=50000),
            PlanTier(plan_id=plan2.plan_id, category_id=cat_gpa.category_id, sum_insured=3000),
            PlanTier(plan_id=plan2.plan_id, category_id=cat_fwmi.category_id, sum_insured=65000)
        ]
        session.add_all(tiers)
        session.commit()

        # ---- ASSIGN EMPLOYEE TO AIA PLAN ----
        emp1.plan_id = plan1.plan_id
        session.add(emp1)
        session.commit()

        # ---- BIDDING ROUND ----
        round_2025 = BiddingRound(
            round_name="2025 Renewal Round 1",
            start_date="2025-01-10",
            end_date="2025-01-20"
        )
        session.add(round_2025)
        session.commit()

        # ---- BIDS (AIA & Singlife give premiums) ----
        bids = [
            Bid(round_id=round_2025.round_id, insurer_id=insurer_aia.user_id, category_id=cat_gtl.category_id, premium=12.50),
            Bid(round_id=round_2025.round_id, insurer_id=insurer_aia.user_id, category_id=cat_gci.category_id, premium=18.00),
            Bid(round_id=round_2025.round_id, insurer_id=insurer_aia.user_id, category_id=cat_ghs.category_id, premium=42.00),

            Bid(round_id=round_2025.round_id, insurer_id=insurer_singlife.user_id, category_id=cat_gtl.category_id, premium=11.00),
            Bid(round_id=round_2025.round_id, insurer_id=insurer_singlife.user_id, category_id=cat_gci.category_id, premium=19.00),
            Bid(round_id=round_2025.round_id, insurer_id=insurer_singlife.user_id, category_id=cat_ghs.category_id, premium=36.00),
        ]
        session.add_all(bids)
        session.commit()

        print("Seed data inserted successfully!")


if __name__ == "__main__":
    seed_data()
