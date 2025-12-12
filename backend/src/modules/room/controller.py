from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from src.database.core import get_db
from . import model, service
from src.modules.auth.jwt import get_current_user

room_controller = APIRouter(prefix="/rooms", tags=["Rooms"], dependencies=[Depends(get_current_user)])


# ------------------- RoomType ------------------- #
@room_controller.post("/types", response_model=model.RoomTypeResponse, status_code=status.HTTP_201_CREATED)
def create_room_type(room_type: model.RoomTypeCreate, db: Session = Depends(get_db)):
    return service.create_room_type(db, room_type)


@room_controller.get("/types", response_model=List[model.RoomTypeResponse])
def list_room_types(db: Session = Depends(get_db)):
    return service.get_room_types(db)


@room_controller.get("/types/{room_type_id}", response_model=model.RoomTypeResponse)
def get_room_type(room_type_id: int, db: Session = Depends(get_db)):
    return service.get_room_type_by_id(db, room_type_id)

@room_controller.put("/types/{room_type_id}", response_model=model.RoomTypeResponse)
def update_room_type(room_type_id: int, update_data: model.RoomTypeUpdate, db: Session = Depends(get_db)):
    return service.update_room_type(db, room_type_id, update_data)


@room_controller.delete("/types/{room_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_type(room_type_id: int, db: Session = Depends(get_db)):
    service.delete_room_type(db, room_type_id)
    return {"message": "RoomType deleted successfully"}


# ------------------- RoomChat ------------------- #
@room_controller.post("/chats", response_model=model.RoomChatResponse, status_code=status.HTTP_201_CREATED)
def create_room_chat(room_chat: model.RoomChatCreate, db: Session = Depends(get_db)):
    return service.create_room_chat(db, room_chat)


@room_controller.get("/chats", response_model=List[model.RoomChatResponse])
def list_room_chats(db: Session = Depends(get_db)):
    return service.get_room_chats(db)

@room_controller.get("/chats/central", response_model=model.RoomChatResponse)
def get_room_chat_central(db: Session = Depends(get_db)):
    return service.get_room_chat_central(db)

@room_controller.get("/chats/name/{room_chat_name}", response_model=model.RoomChatResponse)
def get_room_chat_by_name(room_chat_name: str, db: Session = Depends(get_db)):
    return service.get_room_chat_by_name(db, room_chat_name)

@room_controller.get("/quiz/", response_model=List[model.RoomChatResponse])
def get_room_quiz(db: Session = Depends(get_db)):
    return service.get_room_quiz(db)

@room_controller.get("/chats/{room_chat_id}", response_model=model.RoomChatResponse)
def get_room_chat_by_id(room_chat_id: UUID, db: Session = Depends(get_db)):
    return service.get_room_chat_by_id(db, room_chat_id)


@room_controller.put("/chats/{room_chat_id}", response_model=model.RoomChatResponse)
def update_room_chat(room_chat_id: UUID, update_data: model.RoomChatUpdate, db: Session = Depends(get_db)):
    return service.update_room_chat(db, room_chat_id, update_data)


@room_controller.delete("/chats/{room_chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_chat(room_chat_id: UUID, db: Session = Depends(get_db)):
    service.delete_room_chat(db, room_chat_id)
    return {"message": "RoomChat deleted successfully"}
