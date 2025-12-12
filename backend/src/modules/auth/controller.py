from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy.orm import Session
from uuid import UUID
from src.database.core import get_db
from . import model, services

auth_controller = APIRouter(prefix="/auth", tags=["auth"])

@auth_controller.post("/login", response_model=model.LoginResponse)
def login_user(login_data: model.Login, response: Response, db: Session = Depends(get_db)):
    db_login = services.login_user(db, login_data, response)
    if not db_login:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Authentication")
    
    return db_login


