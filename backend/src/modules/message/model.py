from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
from src.modules.user.model import UserResponse

# ----------------Message Type -----------------------
class MessageTypeBase(BaseModel):
    message_type_name: Optional[str] = None
    message_type_description: Optional[str] = None
    
class MessageTypeResponse(MessageTypeBase):
    message_type_id: int
    
    class Config:
        from_attributes = True
        
class MessageTypeUpdate(BaseModel):
    message_type_name: Optional[str] = None
    message_type_description: Optional[str] = None

# ------------------ Message ------------------
class MessageBase(BaseModel):
    message_text: str
    message_type_id: Optional[int] = None
    reply_to_id: Optional[uuid.UUID] = None


class MessageCreate(MessageBase):
    room_chat_id: uuid.UUID
    user_id: uuid.UUID
    

    
class MessageResponse(MessageBase):
    message_id: uuid.UUID
    room_chat_id: uuid.UUID
    user_id: uuid.UUID
    reply_to: Optional["MessageResponse"] = None
    created_at: datetime
    user: Optional["UserResponse"] = None
    class Config:
        from_attributes = True
        
class FastAnswerQuestion(BaseModel):
    room_id: uuid.UUID
    user_id: uuid.UUID
    answer: str