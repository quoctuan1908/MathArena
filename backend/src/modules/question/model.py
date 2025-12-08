from pydantic import BaseModel, EmailStr
from typing import Optional,List
from datetime import datetime
from uuid import UUID 


class MathRequest(BaseModel):
    text: str


class QuestionTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class QuestionTypeCreate(QuestionTypeBase):
    pass


class QuestionTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class QuestionTypeResponse(QuestionTypeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class SubjectResponse(SubjectBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        

class QuestionBase(BaseModel):
    question_text: str
    answer: Optional[str] = None
    score: Optional[int] = 0
    question_type_id: int
    subject_id: int
    creator_id: UUID


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    answer: Optional[str] = None
    score: Optional[int] = None
    question_type_id: Optional[int] = None
    subject_id: Optional[int] = None
    creator_id: Optional[UUID] = None


class QuestionResponse(QuestionBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Optional nested info
    question_type: Optional[QuestionTypeResponse] = None
    subject: Optional[SubjectResponse] = None

    class Config:
        from_attributes = True

class QuestionListResponse(BaseModel):
    items: List[QuestionResponse]
    total: int