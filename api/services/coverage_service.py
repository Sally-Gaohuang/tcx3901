# file: api/services/coverage_service.py
from sqlmodel import Session, select
from api.database.database import engine
from api.models import PolicyCategory, PlanTier

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
