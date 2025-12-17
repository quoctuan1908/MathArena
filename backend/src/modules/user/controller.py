from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.core import get_db
from src.entities import User
from . import model, service
from src.modules.auth.jwt import get_current_user

user_controller = APIRouter(prefix="/users", tags=["users"])

# ================================
# USER ROLE MANAGEMENT
# ================================
@user_controller.post("/roles", response_model=model.UserRoleResponse, status_code=status.HTTP_201_CREATED)
def create_user_role(role_data: model.UserRoleCreate, db: Session = Depends(get_db)):
    return service.create_user_role(db, role_data)

@user_controller.get("/roles", response_model=list[model.UserRoleResponse])
def list_user_roles(db: Session = Depends(get_db)):
    return service.get_all_user_roles(db)

@user_controller.put("/roles/{role_id}", response_model=model.UserRoleResponse)
def update_user_role(role_id: int, role_data: model.UserRoleUpdate, db: Session = Depends(get_db)):
    db_role = service.update_user_role(db, role_id, role_data)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return db_role

@user_controller.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_role(role_id: int, db: Session = Depends(get_db)):
    success = service.delete_user_role(db, role_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return {"message": "Role deleted"}

# ================================
# SYSTEM-WIDE STATISTICS (tĩnh — nên đặt TRƯỚC /{user_id})
# ================================
@user_controller.get("/system", response_model=model.SystemStats)
def system_stats(db: Session = Depends(get_db)):
    return service.get_system_statistics(db)

@user_controller.get("/user/{user_id}", response_model=model.UserStats)
def user_stats(user_id: str, db: Session = Depends(get_db)):
    return service.get_user_statistics(db, user_id)

@user_controller.get("/room/{room_chat_id}", response_model=model.RoomStats)
def room_stats(room_chat_id: str, db: Session = Depends(get_db)):
    return service.get_room_statistics(db, room_chat_id)

# ================================
# USER CRUD
# ================================
@user_controller.post("/", response_model=model.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: model.UserCreate, db: Session = Depends(get_db)):
    db_user = service.create_user(db, user_data)
    return db_user

@user_controller.get("/", response_model=list[model.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return service.get_all_users(db)

@user_controller.get("/{user_id}", response_model=model.UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@user_controller.put("/{user_id}", response_model=model.UserResponse)
def update_user(user_id: UUID, user_data: model.UserUpdate, db: Session = Depends(get_db)):
    db_user = service.update_user(db, user_id, user_data)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@user_controller.put("/{user_id}/password", response_model=model.UserResponse)
def update_user_password(user_id: UUID, password_data: model.UserPasswordUpdate, db: Session = Depends(get_db)):
    db_user = service.update_user_password(db, user_id, password_data)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid current password or user not found")
    return db_user

@user_controller.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    success = service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted"}

# ================================
# USER STATISTICS
# ================================
@user_controller.get("/stat/{user_id}", response_model=model.UserStatisticResponse)
def get_user_statistic(user_id: UUID, db: Session = Depends(get_db)):
    db_user = service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user.user_statistic

@user_controller.patch("/stat/{user_id}", response_model=model.UserResponse)
def update_user_statistic(user_id: UUID, user_data: model.StatUpdate, db: Session = Depends(get_db)):
    db_user = service.update_user_stat(db, user_id, user_data)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

# ================================
# USER INFO
# ================================
@user_controller.get("/info/{user_id}", response_model=model.UserInfoResponse)
def get_user_info(user_id: UUID, db: Session = Depends(get_db)):
    db_user = service.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user.user_info
