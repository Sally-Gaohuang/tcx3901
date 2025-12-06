# file: api/routers/insurer.py

from fastapi import APIRouter, Depends, HTTPException
from app.auth.auth_service import get_current_user
from app.services.insurer_service import (
    get_required_categories,
    submit_bid,
    update_bid
)

router = APIRouter()

def verify_insurer(current_user):
    if current_user.role != "insurer":
        raise HTTPException(status_code=403, detail="Insurer access only")

# GET /insurer/categories
@router.get("/categories")
def categories(current_user = Depends(get_current_user)):
    verify_insurer(current_user)
    return get_required_categories()

# POST /insurer/bid
@router.post("/bid")
def new_bid(
    category_id: int,
    round_id: int,
    premium: float,
    current_user = Depends(get_current_user)
):
    verify_insurer(current_user)
    return submit_bid(current_user.user_id, category_id, round_id, premium)

# PUT /insurer/bid/{bid_id}
@router.put("/bid/{bid_id}")
def modify_bid(
    bid_id: int,
    premium: float,
    current_user = Depends(get_current_user)
):
    verify_insurer(current_user)
    return update_bid(bid_id, premium)
