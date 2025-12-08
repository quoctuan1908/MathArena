from sqlalchemy import Column, String, ForeignKey, Boolean, Date, DateTime,func, Integer
from src.database.core import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class UserInfo(Base):
    __tablename__ = "user_infos"

    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    name = Column(String(100), default="Unknown Person")
    birthday = Column(Date, nullable=True)
    address = Column(String, nullable=True)
    phone = Column(String(10), nullable=True)
    email = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="user_info",uselist=False)

class UserRole(Base):
    __tablename__ = "user_roles"

    user_role_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    user_role_name = Column(String(50), unique=True, nullable=False)
    user_role_description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    users = relationship("User", back_populates="user_role")


class LevelType(Base):
    __tablename__ = "level_types"

    level_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    level_name = Column(String(50), unique=True, nullable=False)
    level_description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_statistics = relationship("UserStatistic", back_populates="level_type", cascade="all, delete-orphan")


class UserStatistic(Base):
    __tablename__ = "user_statistics"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    level_id = Column(Integer, ForeignKey("level_types.level_id", ondelete="SET NULL"))
    problem_solved = Column(Integer, default=0)
    score = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="user_statistic", uselist=False)
    level_type = relationship("LevelType", back_populates="user_statistics")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_role_id = Column(Integer, ForeignKey("user_roles.user_role_id"))
    username = Column(String(30), unique=True, nullable=False)
    password_hashed = Column(String, nullable=False)
    is_enabled = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_info = relationship("UserInfo", back_populates="user", uselist=False, cascade="all, delete-orphan")
    user_statistic = relationship("UserStatistic", back_populates="user", uselist=False, cascade="all, delete-orphan")
    user_role = relationship("UserRole", back_populates="users")

    user_rooms = relationship("UserRoom", back_populates="users")
    messages = relationship("Message", back_populates="user")
    medias = relationship("Media", back_populates="user")
    questions = relationship("Question", back_populates="creator")