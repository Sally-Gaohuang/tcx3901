# file: api/routers/coverage.py

from fastapi import APIRouter
from api.services.coverage_service import get_category_limits

router = APIRouter()

# GET /coverage/plan/{plan_id}
@router.get("/plan/{plan_id}")
def category_limits(plan_id: int):
    return get_category_limits(plan_id)
