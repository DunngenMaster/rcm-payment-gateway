from fastapi import APIRouter, HTTPException, Depends, status, Header
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.models import CodeExchangeRequest
from app.api.handlers import AuthHandler
from app.core.constants import (
    AUTH_ROUTER_PREFIX,
    AUTH_ROUTER_TAG,
    AUTH_START_ROUTE,
    AUTH_EXCHANGE_ROUTE,
    HTTP_STATUS_INTERNAL_SERVER_ERROR,
)
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.db.models import User, Merchant

auth_handler = AuthHandler()
router = APIRouter(prefix=AUTH_ROUTER_PREFIX, tags=[AUTH_ROUTER_TAG])


class RegisterRequest(BaseModel):
    email: str
    password: str
    merchant_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.get(AUTH_START_ROUTE)
async def start_auth():
    auth_url = await auth_handler.start_auth()
    return { "success": True, "auth_url": auth_url }


@router.post(AUTH_EXCHANGE_ROUTE)
async def exchange_code(payload: CodeExchangeRequest):
    try:
        return await auth_handler.exchange_code(payload)
    except Exception as e:
        raise HTTPException(status_code=HTTP_STATUS_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/status")
async def check_status():
    return await auth_handler.check_connection()


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    merchant = Merchant(
        clover_merchant_id=f"temp_{request.email}",
        clover_access_token=b"",
        merchant_name=request.merchant_name
    )
    db.add(merchant)
    db.flush()
    
    user = User(
        email=request.email,
        password_hash=hash_password(request.password),
        merchant_id=merchant.merchant_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token({"user_id": str(user.user_id), "merchant_id": str(merchant.merchant_id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"user_id": str(user.user_id), "merchant_id": str(user.merchant_id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization scheme")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")
    
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return {
        "user_id": str(user.user_id),
        "email": user.email,
        "merchant_id": str(user.merchant_id),
        "merchant_name": user.merchant.merchant_name
    }
