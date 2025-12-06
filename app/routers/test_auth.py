# file: api/routers/test_auth.py

from fastapi import APIRouter, Depends
from app.auth.auth_service import get_current_user

router = APIRouter()

@router.get("/check")
def check_auth(current_user = Depends(get_current_user)):
    """
    Test endpoint to verify JWT token works.
    Returns logged-in user's username and role.
    """
    return {
        "authenticated": True,
        "user": current_user.username,
        "role": current_user.role
    }
