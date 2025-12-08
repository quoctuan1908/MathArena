from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime
from . import model
from src.entities import UserRoomRole, UserRoom, RoomChat
import uuid
from typing import List


# ------------------------ User Room Role-----------------------#

def create_user_room_role(db: Session, data: model.UserRoonRoleCreate) -> UserRoomRole:
    new_role = UserRoomRole(
        user_room_role_name=data.user_room_role_name,
        user_room_role_description=data.user_room_role_description
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def get_user_room_roles(db: Session):
    return db.query(UserRoomRole).all()


def get_user_room_role_by_id(db: Session, role_id: UUID):
    role = db.query(UserRoomRole).filter(UserRoomRole.user_room_role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserRoomRole not found")
    return role


def update_user_room_role(db: Session, role_id: UUID, role_data: model.UserRoomRoleUpdate):
    db_user_room_role = db.query(UserRoomRole).filter(UserRoomRole.user_room_role_id == role_id).first()
    if not db_user_room_role:
        return None
    for key, value in role_data.model_dump(exclude_unset=True).items():
        setattr(db_user_room_role, key, value)
    db.commit()
    db.refresh(db_user_room_role)
    return db_user_room_role

def delete_user_room_role(db: Session, role_id: UUID):
    role = get_user_room_role_by_id(db, role_id)
    db.delete(role)
    db.commit()
    return {"message": "UserRoomRole deleted successfully"}

# ------------------------ User Room -----------------------#

def create_user_room(db: Session, user_room_data: model.UserRoomCreate) -> UserRoom:
    # 1. Lấy thông tin phòng
    room = db.query(RoomChat).filter(RoomChat.room_chat_id == user_room_data.room_chat_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Phòng không tồn tại")

    # 2. Kiểm tra capacity
    # Nếu room_capacity là null → không giới hạn
    if room.room_capacity is not None:
        if room.room_capacity <= 0:
            raise HTTPException(status_code=400, detail="Phòng đã đầy")
        # Giảm capacity đi 1
        room.room_capacity -= 1
        db.add(room)

    # 3. Tạo user_room
    new_user_room = UserRoom(
        room_chat_id=user_room_data.room_chat_id,
        user_id=user_room_data.user_id,
        user_room_role_id=user_room_data.user_room_role_id
    )
    db.add(new_user_room)
    db.commit()
    db.refresh(new_user_room)

    return new_user_room

def get_user_rooms(db: Session):
    return db.query(UserRoom).all()


def get_user_room(db: Session, room_chat_id: UUID, user_id: UUID) -> UserRoom:
    user_room = (
        db.query(UserRoom)
        .filter(UserRoom.room_chat_id == room_chat_id, UserRoom.user_id == user_id)
        .first()
    )
    if not user_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserRoom not found for room_chat_id={room_chat_id}, user_id={user_id}",
        )
    return user_room

def get_user_room_by_user_id(db: Session, user_id: UUID) -> List[UserRoom]:
    user_rooms = (db.query(UserRoom).filter(UserRoom.user_id == user_id))
    if not user_rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"UserRoom not found for user_id={user_id}",
        )
    return user_rooms        

def update_user_room(
    db: Session, room_chat_id: UUID, user_id: UUID, update_data: model.UserRoomUpdate) -> UserRoom:
    user_room = get_user_room(db, room_chat_id, user_id)

    if update_data.user_room_role_id is not None:
        user_room.user_room_role_id = update_data.user_room_role_id

    db.commit()
    db.refresh(user_room)
    return user_room


def delete_user_room(db: Session, room_chat_id: UUID, user_id: UUID):
    # Lấy UserRoom
    user_room = get_user_room(db, room_chat_id, user_id)
    if not user_room:
        raise HTTPException(status_code=404, detail="UserRoom không tồn tại")

    # Lấy phòng
    room = db.query(RoomChat).filter(RoomChat.room_chat_id == room_chat_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Phòng không tồn tại")

    # Xóa UserRoom
    db.delete(user_room)

    # Nếu phòng có giới hạn, tăng capacity lên 1
    if room.room_capacity is not None:
        room.room_capacity += 1
        db.add(room)

    db.commit()
    return {"message": "UserRoom deleted successfully"}