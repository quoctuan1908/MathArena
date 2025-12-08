from sqlalchemy import Column, String, Integer,ForeignKey, DateTime,func
from src.database.core import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class MessageType(Base):
    __tablename__ = "message_types"

    message_type_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    message_type_name = Column(String(50), nullable=False)
    message_type_description = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())       
    
    messages = relationship("Message", back_populates="message_type")


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    room_chat_id = Column(UUID(as_uuid=True), ForeignKey("room_chats.room_chat_id"),nullable=False)
    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    message_type_id = Column(Integer, ForeignKey("message_types.message_type_id"))
    message_text = Column(String)
    reply_to_id = Column(UUID(as_uuid=True), ForeignKey("messages.message_id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())   
    
    room_chat = relationship("RoomChat", back_populates="messages")
    user = relationship("User", back_populates="messages")
    message_type = relationship("MessageType", back_populates="messages")
    reply_to = relationship("Message", remote_side=[message_id], backref="replies")
    
    
    