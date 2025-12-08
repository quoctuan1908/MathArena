from pydantic import BaseModel, EmailStr
from typing import Optional,List
from datetime import date
import uuid
from datetime import datetime

# ------------------ User Info ------------------
class UserInfoBase(BaseModel):
    name: Optional[str] = None
    birthday: Optional[date] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInfoCreate(UserInfoBase):
    pass


class UserInfoResponse(UserInfoBase):
    user_id: uuid.UUID

    class Config:
        from_attributes = True  


# ------------------ User Role ------------------
class UserRoleBase(BaseModel):
    user_role_name: str
    user_role_description: Optional[str] = None

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleResponse(UserRoleBase):
    user_role_id: int

    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    user_role_name: Optional[str] = None
    user_role_description: Optional[str] = None

# ----------------Level Type -----------------------
class LevelTypeBase(BaseModel):
    level_name: Optional[str] = None
    level_description: Optional[str] = None
    
class LevelTypeResponse(LevelTypeBase):
    level_id: int
    
    class Config:
        from_attributes = True
        
class LevelTypeUpdate(BaseModel):
    level_name: Optional[str] = None
    level_description: Optional[str] = None


# ---------------------User Statistic----------------------
class UserStatisticBase(BaseModel):
    level_id: int
    problem_solved: int = 0
    score: int = 0

class UserStatisticCreate(UserStatisticBase):
    pass

class UserStatisticResponse(UserStatisticBase):
    user_id: uuid.UUID
    
    created_at: datetime
    
    class Config:
        from_attributes = True
    

# ------------------ User ------------------
class UserBase(BaseModel):
    username: str
    is_enabled: Optional[bool] = True


class UserCreate(UserBase):
    password_hashed: str  
    user_info: Optional[UserInfoCreate] = None
    user_statistic: Optional[UserStatisticCreate] = None
    user_role_id: int = None


class UserUpdate(UserBase):
    user_role_id: Optional[int] = None
    user_statistic: Optional[UserStatisticCreate] = None
    user_info: Optional[UserInfoCreate] = None

class StatUpdate(BaseModel):
    added_score: int
    added_solved: int

class UserPasswordUpdate(BaseModel):
    current_password_hashed: str
    password_hashed: str

class UserResponse(UserBase):
    id: uuid.UUID
    user_role_id: int
    user_role: Optional[UserRoleResponse] = None
    user_info: Optional[UserInfoResponse] = None
    user_statistic: Optional[UserStatisticResponse] = None
    
    created_at: datetime
    class Config:
        from_attributes = True

class SystemStats(BaseModel):
    total_users: int
    total_rooms: int
    total_messages: int
    total_questions: int
    average_users_per_room: float
    total_score: int
    average_user_score: float  # rename từ avg_score_per_user
    active_users: Optional[int] = None
    last_update: Optional[str] = None

    class Config:
        from_attributes = True


# ==============================
# NGƯỜI DÙNG (USER STATS)
# ==============================

class UserStats(BaseModel):
    user_id: uuid.UUID
    username: str
    total_score: int
    level: Optional[str] = None
    problem_solved: Optional[int] = None

    class Config:
        from_attributes = True


# ==============================
# PHÒNG (ROOM STATS)
# ==============================

class RoomUserStat(BaseModel):
    user_id: uuid.UUID
    username: str
    score: int
    messages_sent: int

    class Config:
        from_attributes = True


class RoomStats(BaseModel):
    room_chat_id: uuid.UUID
    room_name: str
    total_users: int
    total_messages: int
    total_score: int
    top_users: List[RoomUserStat] = []
    created_at: datetime

    class Config:
        from_attributes = True