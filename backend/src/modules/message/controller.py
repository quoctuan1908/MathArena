from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from src.database.core import get_db
from src.entities import User, UserInfo, UserRole, UserStatistic, LevelType
from . import model, service
from typing import List
from src.modules.auth.jwt import get_current_user

message_controller = APIRouter(prefix="/messages", tags=["users"], dependencies=[Depends(get_current_user)])


@message_controller.get("/types", response_model=List[model.MessageTypeResponse])
def get_all_message_types(db: Session = Depends(get_db)):
    return service.get_all_message_types(db)

@message_controller.get("/types/{message_type_id}", response_model=model.MessageTypeResponse)
def get_message_type_by_id(message_type_id: int,db: Session = Depends(get_db)):
    message_type = service.get_message_type_by_id(db, message_type_id)
    if not message_type:
        raise HTTPException(status_code=404, detail="Message type not found")
    return message_type


@message_controller.put("/types/{message_type_id}", response_model=model.MessageTypeResponse)
def update_message_type(message_type_id: int,update_data: model.MessageTypeUpdate,db: Session = Depends(get_db)):
    updated = service.update_message_type(db, message_type_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Message type not found")
    return updated

@message_controller.post("/types", response_model=model.MessageTypeResponse, status_code=status.HTTP_201_CREATED)
def create_message_type(type_data: model.MessageTypeBase,db: Session = Depends(get_db)):
    return service.create_message_type(db, type_data)

@message_controller.delete("/types/{message_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message_type(message_type_id: int,db: Session = Depends(get_db)):
    success = service.delete_message_type(db, message_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message type not found")
    return None

@message_controller.get("/room/{room_chat_id}", response_model=List[model.MessageResponse])
def get_messages_by_room_chat_id(room_chat_id: UUID,skip: int = 0,limit: int = 20,db: Session = Depends(get_db)):
    return service.get_messages_by_room_chat_id(db, room_chat_id, skip, limit)


@message_controller.post("/", response_model=model.MessageResponse)
def create_message(message_data: model.MessageCreate, db: Session = Depends(get_db)):
    return service.create_message(db, message_data)


@message_controller.get("/{message_id}", response_model=model.MessageResponse)
def get_message_by_id(message_id: UUID, db: Session = Depends(get_db)):
    return service.get_message_by_id(db, message_id)

@message_controller.delete("/{message_id}")
def delete_message(message_id: UUID,db: Session = Depends(get_db)): 
    return service.delete_message(db, message_id)


