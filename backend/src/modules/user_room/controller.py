from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from src.database.core import get_db
from . import model, service
from typing import List

user_room_controller = APIRouter(prefix="/user_rooms", tags=["user-rooms"])


# ------------------------ User Room Role -----------------------#

@user_room_controller.post("/roles", response_model=model.UserRoonRoleResponse)
def create_user_room_role(role_data: model.UserRoonRoleCreate, db: Session = Depends(get_db)):
    return service.create_user_room_role(db, role_data)


@user_room_controller.get("/roles", response_model=list[model.UserRoonRoleResponse])
def get_user_room_roles(db: Session = Depends(get_db)):
    return service.get_user_room_roles(db)


@user_room_controller.get("/roles/{role_id}", response_model=model.UserRoonRoleResponse)
def get_user_room_role(role_id: int, db: Session = Depends(get_db)):
    return service.get_user_room_role_by_id(db, role_id)


@user_room_controller.put("/roles/{role_id}", response_model=model.UserRoonRoleResponse)
def update_user_room_role(role_id: int, role_data: model.UserRoomRoleUpdate, db: Session = Depends(get_db)):
    updated_role = service.update_user_room_role(db, role_id, role_data)
    if not updated_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserRoomRole not found")
    return updated_role


@user_room_controller.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_room_role(role_id: int, db: Session = Depends(get_db)):
    service.delete_user_room_role(db, role_id)
    return None

# ------------------------ User Room -----------------------#

@user_room_controller.post("/", response_model=model.UserRoomResponse)
def create_user_room(user_room_data: model.UserRoomCreate, db: Session = Depends(get_db)):
    return service.create_user_room(db, user_room_data)



@user_room_controller.get("/user/{user_id}", response_model=List[model.UserRoomResponse])
def get_user_room_by_user_id(user_id: UUID, db: Session = Depends(get_db)):
    return service.get_user_room_by_user_id(db, user_id)


@user_room_controller.get("/{room_chat_id}/{user_id}", response_model=model.UserRoomResponse)
def get_user_room(room_chat_id: UUID, user_id: UUID, db: Session = Depends(get_db)):
    return service.get_user_room(db, room_chat_id, user_id)

@user_room_controller.delete("/{room_chat_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_room(room_chat_id: UUID, user_id: UUID, db: Session = Depends(get_db)):
    service.delete_user_room(db, room_chat_id, user_id)
    return None

@user_room_controller.put("/{room_chat_id}/{user_id}", response_model=model.UserRoomResponse)
def update_user_room(
    room_chat_id: UUID,
    user_id: UUID,
    update_data: model.UserRoomUpdate,
    db: Session = Depends(get_db)
):
    return service.update_user_room(db, room_chat_id, user_id, update_data)


