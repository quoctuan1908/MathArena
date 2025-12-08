from sqlalchemy import Column, String, ForeignKey, DateTime,func,Integer
from src.database.core import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class UserRoomRole(Base):
    __tablename__ = "user_room_roles"

    user_room_role_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    user_room_role_name = Column(String(50), unique=True, nullable=False)
    user_room_role_description = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())    
    
    user_rooms = relationship("UserRoom", back_populates="user_room_role")


class UserRoom(Base):
    __tablename__ = "user_rooms"

    room_chat_id = Column(UUID(as_uuid=True), ForeignKey("room_chats.room_chat_id", ondelete="CASCADE"),primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    user_room_role_id = Column(Integer, ForeignKey("user_room_roles.user_room_role_id", ondelete="CASCADE"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())    
    
    users = relationship("User", back_populates="user_rooms")
    room_chats = relationship("RoomChat", back_populates="user_rooms")
    user_room_role = relationship("UserRoomRole", back_populates="user_rooms")