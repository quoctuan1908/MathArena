from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
from datetime import datetime, timezone
from . import model
from src.entities import RoomType, RoomChat
import uuid
from src.modules.user_room.service import create_user_room
from src.modules.user_room.model import UserRoomCreate

# ------------------- RoomType Service ------------------- #
def create_room_type(db: Session, room_type: model.RoomTypeCreate) -> RoomType:
    new_room_type = RoomType(
        room_type_name=room_type.room_type_name,
        room_type_description=room_type.room_type_description,
    )
    db.add(new_room_type)
    db.commit()
    db.refresh(new_room_type)
    return new_room_type


def get_room_types(db: Session):
    excluded_ids = [1]
    return db.query(RoomType).filter(~RoomType.room_type_id.in_(excluded_ids)).all()

def get_room_type_by_id(db: Session, room_type_id: int):
    room_type = db.query(RoomType).filter(RoomType.room_type_id == room_type_id).first()
    if not room_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RoomType not found")
    return room_type


def update_room_type(db: Session, room_type_id: int, update_data: model.RoomTypeUpdate):
    room_type = get_room_type_by_id(db, room_type_id)
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(room_type, field, value)
    room_type.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(room_type)
    return room_type


def delete_room_type(db: Session, room_type_id: int):
    room_type = get_room_type_by_id(db, room_type_id)
    db.delete(room_type)
    db.commit()
    return {"message": "RoomType deleted successfully"}


# ------------------- RoomChat Service ------------------- #
def create_room_chat(db: Session, room_chat: model.RoomChatCreate) -> RoomChat:
    room_type = db.query(RoomType).filter(RoomType.room_type_id == room_chat.room_type_id).first()
    if not room_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid room_type_id")

    new_room_chat = RoomChat(
        room_name=room_chat.room_name,
        room_capacity=room_chat.room_capacity,
        room_type_id=room_chat.room_type_id,
        room_password=room_chat.room_password
    )
    db.add(new_room_chat)
    db.commit()
    db.refresh(new_room_chat)
    
    new_user_room = create_user_room(db, UserRoomCreate(
        user_id=room_chat.host_id,
        user_room_role_id=1,
        room_chat_id=new_room_chat.room_chat_id
    ))

    db.add(new_user_room)
    db.commit()
    db.refresh(new_user_room)
    
    return new_room_chat


def get_room_chats(db: Session):
    return db.query(RoomChat).all()


def get_room_chat_by_id(db: Session, room_chat_id: UUID):
    room_chat = db.query(RoomChat).filter(RoomChat.room_chat_id == room_chat_id).first()
    if not room_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RoomChat not found")
    return room_chat

def get_room_chat_by_name(db: Session, room_chat_name: str):
    room_chat = db.query(RoomChat).filter(RoomChat.room_name == room_chat_name).first()
    if not room_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RoomChat not found")
    return room_chat

def get_room_chat_central(db: Session):
    room_chat = db.query(RoomChat).filter(RoomChat.room_type_id == 1).first()
    if not room_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RoomChat not found")
    return room_chat

def get_room_quiz(db: Session):
    room_quizs = (
        db.query(RoomChat)
        .join(RoomChat.room_type)
        .filter(RoomType.room_type_name.ilike("%Quiz%"))
        .all()
    )
    if not room_quizs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="RoomQuiz not found"
        )
    return room_quizs

def update_room_chat(db: Session, room_chat_id: UUID, update_data: model.RoomChatUpdate):
    room_chat = get_room_chat_by_id(db, room_chat_id)
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(room_chat, field, value)
    room_chat.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(room_chat)
    return room_chat


def delete_room_chat(db: Session, room_chat_id: UUID):
    room_chat = get_room_chat_by_id(db, room_chat_id)
    db.delete(room_chat)
    db.commit()
    return {"message": "RoomChat deleted successfully"}
