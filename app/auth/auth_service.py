# file: app/auth/auth_service.py

from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.database.database import engine
from app.models.models import User   # make sure this path is correct

# -----------------------------
# JWT CONFIGURATION
# -----------------------------
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_THIS"   # move to .env later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# -----------------------------
# PASSWORD HASHING
# -----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed):
    return pwd_context.verify(plain_password, hashed)

def hash_password(password):
    return pwd_context.hash(password)

# -----------------------------
# TOKEN CREATION
# -----------------------------
def create_access_token(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

# -----------------------------
# OAuth2 Authentication Scheme
# -----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# -----------------------------
# VALIDATE USER CREDENTIALS
# -----------------------------
def authenticate_user(username: str, password: str):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == username)
        ).first()

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

# -----------------------------
# GET CURRENT USER
# -----------------------------
def get_current_user(token: str = oauth2_scheme):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.username == username)
            ).first()

            if user is None:
                raise HTTPException(status_code=401, detail="User not found")

            return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
