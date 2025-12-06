# file: api/services/coverage_service.py
from sqlmodel import Session, select
from app.database.database import engine
from app.models import PolicyCategory, PlanTier
# from api.database.database import SessionLocal

def get_category_limits(plan_id: int):
    with Session(engine) as session:
        tiers = session.exec(
            select(PlanTier).where(PlanTier.plan_id == plan_id)
        ).all()

        result = []
        for t in tiers:
            category = session.get(PolicyCategory, t.category_id)
            result.append({
                "category": category.category_name,
                "sum_insured": t.sum_insured
            })
        return result
