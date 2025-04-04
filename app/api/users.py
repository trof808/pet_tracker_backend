from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import timedelta
# from app.database import get_db
from app.database import SessionDep
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.services.user import create_user, get_user_by_email
from app.auth.security import (
    create_access_token,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
import bcrypt

router = APIRouter()


@router.post("/sign_up", response_model=UserResponse)
def sign_up(user: UserCreate, session: SessionDep):
    db_user = get_user_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(session, user=user)


@router.post("/sign_in")
def sign_in(response: Response, user: UserCreate, session: SessionDep):
    existing_user = session.query(User).filter(User.email == user.email).first()

    if not existing_user or not bcrypt.checkpw(
        user.password.encode("utf-8"), existing_user.hashed_password.encode("utf-8")
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Создание JWT токена
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "id": existing_user.id,
            "sub": existing_user.email,
            # "role": existing_user.role,
        },
        # expires_delta=access_token_expires,
    )

    # Установка токена в httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"access_token": access_token, "token_type": "bearer"}


def get_user(user_id: int, session: SessionDep) -> User:
    """
    Получение пользователя по ID
    """
    db_user = session.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user
