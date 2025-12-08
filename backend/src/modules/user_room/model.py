from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
from src.modules.room.model import RoomChatResponse

#------------------------- UserRoomRole -----------------------------#

class UserRoonRoleBase(BaseModel):
    user_room_role_name: Optional[str] = None
    user_room_role_description: Optional[str] = None
    
    
class UserRoonRoleCreate(UserRoonRoleBase):
    user_room_role_name: str
    
    
class UserRoomRoleUpdate(BaseModel):
    user_room_role_name: Optional[str] = None
    user_room_role_description: Optional[str] = None    
    
    
class UserRoonRoleResponse(UserRoonRoleBase):
    user_room_role_id: int
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
#------------------------- UserRoom -----------------------------#

class UserRoomBase(BaseModel):
    room_chat_id: uuid.UUID
    user_id: uuid.UUID
    user_room_role_id: int
    
class UserRoomCreate(UserRoomBase):
    pass    
        
class UserRoomResponse(UserRoomBase):
    created_at: datetime
    room_chats: Optional[RoomChatResponse] = None
    
    class Config:
        from_attributes = True
        
class UserRoomUpdate(BaseModel):
    user_room_role_id: Optional[int] = None

    class Config:
        from_attributes = True