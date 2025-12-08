from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select,func
from typing import List, Optional
from uuid import UUID

from src.entities import QuestionType, Subject, Question
from . import model


# ==============================
# QuestionType Service
# ==============================

def get_all_question_types(db: Session) -> List[QuestionType]:
    return db.query(QuestionType).all()

def get_question_type_by_id(db: Session, question_type_id: int) -> Optional[QuestionType]:
    return db.query(QuestionType).filter(QuestionType.id == question_type_id).first()


def create_question_type(db: Session, type_data: model.QuestionTypeCreate) -> QuestionType:
    question_type = QuestionType(**type_data.model_dump())
    db.add(question_type)
    db.commit()
    db.refresh(question_type)
    return question_type


def update_question_type(db: Session, question_type_id: int, update_data: model.QuestionTypeUpdate) -> Optional[QuestionType]:
    question_type = db.query(QuestionType).filter(QuestionType.id == question_type_id).first()
    if not question_type:
        return None

    update_fields = update_data.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(question_type, key, value)

    db.commit()
    db.refresh(question_type)
    return question_type


def delete_question_type(db: Session, question_type_id: int) -> bool:
    question_type = db.query(QuestionType).filter(QuestionType.id == question_type_id).first()
    if not question_type:
        return False
    db.delete(question_type)
    db.commit()
    return True


# ==============================
# Subject Service
# ==============================

def get_all_subjects(db: Session) -> List[Subject]:
    return db.query(Subject).all()


def get_subject_by_id(db: Session, subject_id: int) -> Optional[Subject]:
    return db.query(Subject).filter(Subject.id == subject_id).first()


def create_subject(db: Session, subject_data: model.SubjectCreate) -> Subject:
    subject = Subject(**subject_data.model_dump())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


def update_subject(db: Session, subject_id: int, update_data: model.SubjectUpdate) -> Optional[Subject]:
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        return None

    update_fields = update_data.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(subject, key, value)

    db.commit()
    db.refresh(subject)
    return subject


def delete_subject(db: Session, subject_id: int) -> bool:
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        return False
    db.delete(subject)
    db.commit()
    return True


# ==============================
# Question Service
# ==============================

def get_all_questions(db: Session) -> List[Question]:
    return (
        db.query(Question)
        .options(
            joinedload(Question.question_type),
            joinedload(Question.subject)
        )
        .all()
    )

def get_questions_by_creator_id(db: Session, creator_id: UUID, skip: int = 0, limit: int = 10): 
    return (
        db.query(Question)
        .options(
            joinedload(Question.question_type),
            joinedload(Question.subject)
        )
        .filter(Question.creator_id == creator_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_question_by_id(db: Session, question_id: UUID) -> Optional[Question]:
    return (
        db.query(Question)
        .options(
            joinedload(Question.question_type),
            joinedload(Question.subject)
        )
        .filter(Question.id == question_id)
        .first()
    )

def get_random_questions(db: Session) -> List[Question]:
    return db.query(Question).order_by(func.random()).limit(10).all()

def create_question(db: Session, question_data: model.QuestionCreate) -> Question:
    question = Question(**question_data.model_dump())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def update_question(db: Session, question_id: UUID, update_data: model.QuestionUpdate) -> Optional[Question]:
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return None

    update_fields = update_data.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(question, key, value)

    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question_id: UUID) -> bool:
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return False
    db.delete(question)
    db.commit()
    return True
