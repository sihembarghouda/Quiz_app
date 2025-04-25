# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from schemas import QuestionBase, ChoiceBase

app = FastAPI()

# Créer les tables dans la base de données PostgreSQL
models.Base.metadata.create_all(bind=engine)

# Fonction pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Point de terminaison pour ajouter une question
@app.post('/questions/')
def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()

    return {"message": "Question added successfully!"}

# Point de terminaison pour obtenir une question par ID
@app.get('/questions/{question_id}')
def read_questions(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question not found")
    return result

# Point de terminaison pour obtenir les choix associés à une question
@app.get('/choices/{question_id}')
def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choices not found")
    return result

@app.get("/")
def read_root():
    return {"Hello": "World"}