from sqlalchemy import Column, String,ForeignKey, DateTime,func, Integer
from src.database.core import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class MediaType(Base):
    __tablename__ = "media_types"

    media_type_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    media_type_name = Column(String(50), nullable=False)
    media_type_description = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())   
    
    medias = relationship("Media", back_populates="media_type")


class Media(Base):
    __tablename__ = "medias"

    media_id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    storage_id = Column(UUID(as_uuid=True),ForeignKey("storages.storage_id"),nullable=False)
    media_type_id = Column(Integer,ForeignKey("media_types.media_type_id"),nullable=False)
    media_name = Column(String(50), unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())       
    
    user = relationship("User", back_populates="medias")
    storage = relationship("Storage", back_populates="medias")
    media_type = relationship("MediaType", back_populates="medias")