from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.database.core import Base 
import uuid
from sqlalchemy.dialects.postgresql import UUID

class QuestionType(Base):
    __tablename__ = "question_types"

    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    questions = relationship("Question", back_populates="question_type")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    questions = relationship("Question", back_populates="subject")


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,nullable=False)
    question_text = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    score = Column(Integer, default=0)

    question_type_id = Column(Integer, ForeignKey("question_types.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    question_type = relationship("QuestionType", back_populates="questions")
    subject = relationship("Subject", back_populates="questions")
    creator = relationship("User", back_populates="questions")
