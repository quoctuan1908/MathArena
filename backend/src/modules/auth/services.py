from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
import bcrypt
from uuid import UUID
from src.entities import User
from . import model
from src.modules.user.service import verify_password,get_user_by_username
from .jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
import datetime


def login_user(db: Session, login_data: model.Login) -> model.LoginResponse:
    
    # Tìm user theo username
    user = get_user_by_username(db, login_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Kiểm tra password
    if not verify_password(login_data.password, user.password_hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password 2")


    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires,
    )
    
    return {
        "token": access_token,
        "user": user,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


