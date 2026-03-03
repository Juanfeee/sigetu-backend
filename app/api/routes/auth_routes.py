from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import AuthResponse, LoginRequest, LogoutResponse, RefreshTokenRequest, TokenRefreshResponse, UserCreate
from app.db.session import get_db
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/register", response_model=AuthResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(
        db=db,
        full_name=user_data.full_name,
        email=user_data.email,
        password=user_data.password,
        programa_academico=user_data.programa_academico,
    )


@router.post("/login", response_model=AuthResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(
        db=db,
        email=login_data.email,
        password=login_data.password,
    )


@router.post("/refresh", response_model=TokenRefreshResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    return auth_service.refresh(
        db=db,
        refresh_token=payload.refresh_token,
    )


@router.post("/logout", response_model=LogoutResponse)
def logout(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    return auth_service.logout(
        db=db,
        refresh_token=payload.refresh_token,
    )