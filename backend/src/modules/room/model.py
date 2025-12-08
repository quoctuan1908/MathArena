from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
#------------------------- RoonType -----------------------------#

class RoomTypeBase(BaseModel):
    room_type_name: Optional[str] = None
    room_type_description: Optional[str] = None
    
class RoomTypeCreate(RoomTypeBase):
    room_type_name: str
    
    class Config:
        from_attributes = True   
    
class RoomTypeResponse(RoomTypeBase):
    room_type_id: int
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
class RoomTypeUpdate(RoomTypeBase):
    pass

#------------------------- RoonChat -----------------------------#
class RoomChatBase(BaseModel):
    room_name: Optional[str] = None
    room_capacity: Optional[int] = 1
    room_type_id: int
    room_password: Optional[int] = None
    
class RoomChatCreate(RoomChatBase):
    room_type_id: int
    host_id: uuid.UUID

class RoomChatUpdate(BaseModel):
    room_name: Optional[str] = None
    room_capacity: Optional[int] = None
    room_password: Optional[int] = None
    room_type_id: Optional[int] = None    

class RoomChatResponse(RoomChatBase):
    room_chat_id: uuid.UUID
    room_type_id: int
    room_type: Optional[RoomTypeResponse] = None

    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True