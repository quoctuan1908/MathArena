from sqlalchemy import Column,Integer,ForeignKey, DateTime,func
from src.database.core import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Storage(Base):
    __tablename__ = "storages"

    storage_id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4, nullable=False)
    room_chat_id = Column(UUID(as_uuid=True), ForeignKey("room_chats.room_chat_id"))
    space_remain = Column(Integer)
    total_space = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())    
    
    room_chat = relationship("RoomChat", back_populates="storage",uselist=False)
    medias = relationship("Media", back_populates="storage")