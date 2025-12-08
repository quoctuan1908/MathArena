from pydantic import BaseModel
from src.modules.user.model import UserResponse


class Login(BaseModel):
    username: str
    password: str
    remember_me: bool = False
    
class LoginResponse(BaseModel):
    user: UserResponse
    token: str
    expires_in: int
    
