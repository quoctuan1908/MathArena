from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
import uuid
from sqlalchemy import desc
from src.entities import Message, MessageType
from . import model
from typing import List

def create_message(db: Session, message_data: model.MessageCreate) -> Message: 
    try:
        print(message_data)
        if message_data.reply_to_id:
            replied_msg = db.query(Message).filter(Message.message_id == message_data.reply_to_id).first()
            if not replied_msg:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Replied message not found")
        
        new_message = Message(
            message_id=uuid.uuid4(),
            user_id=message_data.user_id,
            room_chat_id=message_data.room_chat_id,
            message_text=message_data.message_text,
            message_type_id=message_data.message_type_id,
            reply_to_id=message_data.reply_to_id
        )
        
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message
    except Exception:
        db.rollback()
        raise

def get_message_by_id(db: Session, message_id: uuid.UUID) -> Message:
    """Truy vấn tin nhắn và tải EAGERLY thông tin User liên quan."""
    message = (
        db.query(Message)
        .options(joinedload(Message.user))
        .filter(Message.message_id == message_id)
        .first()
    )
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message


def delete_message(db: Session, message_id: uuid.UUID):
    message = get_message_by_id(db, message_id)
    db.delete(message)
    db.commit()
    return {"message": "Message deleted successfully"}


def get_messages_by_room_chat_id(db: Session,room_chat_id: uuid.UUID,skip: int = 0,limit: int = 20) -> List[Message]:
    """Lấy 20 tin nhắn gần nhất và tải EAGERLY thông tin User liên quan."""
    messages = (
        db.query(Message)
        .filter(Message.room_chat_id == room_chat_id)
        .options(joinedload(Message.user)) 
        .order_by(desc(Message.created_at)) 
        .offset(skip)
        .limit(limit)
        .all()
    )
    return list(reversed(messages))

def create_message_type(db: Session, type_data: model.MessageTypeBase):
    new_type = MessageType(
        message_type_name=type_data.message_type_name,
        message_type_description=type_data.message_type_description,
    )
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


def get_all_message_types(db: Session):
    return db.query(MessageType).all()


def get_message_type_by_id(db: Session, message_type_id: int):
    return db.query(MessageType).filter(MessageType.message_type_id == message_type_id).first()


def update_message_type(db: Session, message_type_id: int, update_data: model.MessageTypeUpdate):
    message_type = db.query(MessageType).filter(MessageType.message_type_id == message_type_id).first()
    if not message_type:
        return None

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(message_type, field, value)

    db.commit()
    db.refresh(message_type)
    return message_type


def delete_message_type(db: Session, message_type_id: int):
    message_type = db.query(MessageType).filter(MessageType.message_type_id == message_type_id).first()
    if not message_type:
        return False

    db.delete(message_type)
    db.commit()
    return True