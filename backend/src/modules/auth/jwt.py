import jwt
from datetime import datetime, timedelta,timezone
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY =  os.getenv('JWT_SECRET_KEY')
ALGORITHM =  os.getenv('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES =  int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
