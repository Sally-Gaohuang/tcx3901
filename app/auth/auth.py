# file: app/auth/auth.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user,
)

# Create router for auth endpoints
router = APIRouter()

# ---------------------------
# LOGIN ENDPOINT
# ---------------------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "user_id": user.user_id
    }


# ---------------------------
# CURRENT USER
# ---------------------------
@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "role": current_user.role,
        "user_id": current_user.user_id
    }
