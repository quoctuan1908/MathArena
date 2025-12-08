from sqlalchemy import Column, String, Integer,ForeignKey, DateTime,func
from src.database.core import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class RoomType(Base):
    __tablename__ = "room_types"

    room_type_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    room_type_name = Column(String(50), nullable=False)
    room_type_description = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    room_chats = relationship("RoomChat", back_populates="room_type")


class RoomChat(Base):
    __tablename__ = "room_chats"

    room_chat_id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    room_name = Column(String(30),default="No Name")
    room_capacity = Column(Integer, nullable=True)
    room_type_id = Column(Integer, ForeignKey("room_types.room_type_id"))
    room_password = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())       
    
    room_type = relationship("RoomType", back_populates="room_chats")
    user_rooms = relationship("UserRoom", back_populates="room_chats")
    messages = relationship("Message", back_populates="room_chat")
    storage = relationship("Storage", back_populates="room_chat",uselist=False,cascade="all, delete-orphan",single_parent=True)