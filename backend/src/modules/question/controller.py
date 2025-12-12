# src/modules/auth/controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database.core import get_db
from src.entities import User, UserInfo, UserRole,Question
from . import model, service
from uuid import UUID
from src.machine_learning import model_service

question_controller = APIRouter(prefix="/questions", tags=["questions"])




# @question_controller.post("/generate")
# def generate_math(req: model.MathRequest):
#     result = model_service.generate_output(input_text=req.text)
#     print(result)
#     return result

@question_controller.get("/types", response_model=List[model.QuestionTypeResponse])
def get_all_question_types(db: Session = Depends(get_db)):
    return service.get_all_question_types(db)

@question_controller.get("/types/{question_type_id}", response_model=model.QuestionTypeResponse)
def get_question_type_by_id(question_type_id: int, db: Session = Depends(get_db)):
    question_type = service.get_question_type_by_id(db, question_type_id)
    if not question_type:
        raise HTTPException(status_code=404, detail="Question type not found")
    return question_type

@question_controller.post("/types", response_model=model.QuestionTypeResponse, status_code=status.HTTP_201_CREATED)
def create_question_type(type_data: model.QuestionTypeCreate, db: Session = Depends(get_db)):
    return service.create_question_type(db, type_data)

@question_controller.put("/types/{question_type_id}", response_model=model.QuestionTypeResponse)
def update_question_type(question_type_id: int, update_data: model.QuestionTypeUpdate, db: Session = Depends(get_db)):
    updated = service.update_question_type(db, question_type_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Question type not found")
    return updated

@question_controller.delete("/types/{question_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question_type(question_type_id: int, db: Session = Depends(get_db)):
    success = service.delete_question_type(db, question_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question type not found")
    return None

@question_controller.get("/subjects", response_model=List[model.SubjectResponse])
def get_all_subjects(db: Session = Depends(get_db)):
    return service.get_all_subjects(db)

@question_controller.get("/subjects/{subject_id}", response_model=model.SubjectResponse)
def get_subject_by_id(subject_id: int, db: Session = Depends(get_db)):
    subject = service.get_subject_by_id(db, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@question_controller.post("/subjects/", response_model=model.SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(subject_data: model.SubjectCreate, db: Session = Depends(get_db)):
    return service.create_subject(db, subject_data)

@question_controller.put("/subjects/{subject_id}", response_model=model.SubjectResponse)
def update_subject(subject_id: int, update_data: model.SubjectUpdate, db: Session = Depends(get_db)):
    updated = service.update_subject(db, subject_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Subject not found")
    return updated

@question_controller.delete("/subjects/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    success = service.delete_subject(db, subject_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subject not found")
    return None

@question_controller.get("/", response_model=List[model.QuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return service.get_all_questions(db)


@question_controller.get("/random", response_model=model.QuestionResponse)
def get_random_quesion(db: Session = Depends(get_db)):
    return service.get_random_question(db)


@question_controller.get("/creator/{creator_id}", response_model=model.QuestionListResponse)
def get_questions_by_creator_id(
    creator_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    questions = service.get_questions_by_creator_id(db, creator_id, skip=skip, limit=limit)
    total = (
        db.query(Question)
        .filter(Question.creator_id == creator_id)
        .count()
    )

    return {
        "items": questions,
        "total": total
    }


@question_controller.get("/{question_id}", response_model=model.QuestionResponse)
def get_question_by_id(question_id: UUID, db: Session = Depends(get_db)):
    question = service.get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@question_controller.post("/", response_model=model.QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(question_data: model.QuestionCreate, db: Session = Depends(get_db)):
    return service.create_question(db, question_data)

@question_controller.put("/{question_id}", response_model=model.QuestionResponse)
def update_question(question_id: UUID, update_data: model.QuestionUpdate, db: Session = Depends(get_db)):
    updated = service.update_question(db, question_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated

@question_controller.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: UUID, db: Session = Depends(get_db)):
    success = service.delete_question(db, question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return None