from fastapi import APIRouter, Depends, HTTPException, status,Response, Request
from sqlalchemy.orm import Session
from uuid import UUID
from src.database.core import get_db
from . import model, services, jwt

auth_controller = APIRouter(prefix="/auth", tags=["auth"])

@auth_controller.post("/refresh")
def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = jwt.decode(refresh_token, jwt.SECRET_KEY, algorithms=[jwt.ALGORITHM])
    user_id = payload.get("sub")

    new_access_token = jwt.create_access_token({"sub": user_id})
    return {"token": new_access_token}

@auth_controller.post("/login", response_model=model.LoginResponse)
def login_user(login_data: model.Login, response: Response, db: Session = Depends(get_db)):
    db_login = services.login_user(db, login_data, response)
    if not db_login:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Authentication")
    
    return db_login


