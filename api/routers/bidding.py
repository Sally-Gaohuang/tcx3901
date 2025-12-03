# file: api/routers/bidding.py

from fastapi import APIRouter, Depends
from api.auth.auth_service import get_current_user
from api.services.bidding_service import (
    get_bids_for_round,
    compare_bids
)

router = APIRouter()

@router.get("/round/{round_id}/bids")
def bids_for_round(round_id: int, current_user = Depends(get_current_user)):
    return get_bids_for_round(round_id)

@router.get("/round/{round_id}/compare")
def bidding_comparison(round_id: int, current_user = Depends(get_current_user)):
    return compare_bids(round_id)
