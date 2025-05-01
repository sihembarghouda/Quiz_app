# 🧠 FastAPI Quiz Game with PostgreSQL

Une application backend pour un jeu de quiz, construite avec **FastAPI**, **SQLAlchemy**, et **PostgreSQL**.

---

## 📌 Introduction

Ce projet montre comment développer une API REST avec FastAPI et PostgreSQL pour un jeu de quiz.  
Fonctionnalités :
- Ajouter des questions avec plusieurs choix.
- Récupérer une question et ses choix associés.

---

## 📁 Structure du Projet

```
quiz-app/
│
├── main.py              # Application FastAPI principale
├── models.py            # Modèles SQLAlchemy
├── database.py          # Connexion à la base de données
├── requirements.txt     # Dépendances Python
└── README.md            # Documentation du projet
```

---

## ⚙️ Installation & Configuration

### 1. Créer un environnement virtuel

```bash
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install fastapi sqlalchemy psycopg2-binary uvicorn
```

> Optionnel : pour sauvegarder les dépendances :
```bash
pip freeze > requirements.txt
```

---

## 🛠 Configuration de PostgreSQL

Assurez-vous que PostgreSQL est installé et en cours d’exécution.

Créer une base de données `quizApp` :

```sql
CREATE DATABASE quizApp;
```

Mettre à jour la chaîne de connexion dans `database.py` :

```python
URL_DATABASE = 'postgresql://USERNAME:PASSWORD@localhost:5432/quizApp'
```

---

## 🚀 Lancer l'application

```bash
uvicorn main:app --reload
```

Swagger UI : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧱 Modèles SQLAlchemy

### `models.py`

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)

class Choices(Base):
    __tablename__ = 'choices'
    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
```

---

## 📦 API Endpoints

### ➕ Ajouter une question

`POST /questions/`

Exemple JSON :

```json
{
  "question_text": "What is the best Python Framework",
  "choices": [
    { "choice_text": "FastAPI", "is_correct": true },
    { "choice_text": "Flask", "is_correct": false },
    { "choice_text": "Django", "is_correct": false }
  ]
}
```

### 🔍 Récupérer une question

`GET /questions/{question_id}`

### 🔍 Récupérer les choix d'une question

`GET /choices/{question_id}`

---

## 🛠 Code principal `main.py` (résumé)

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post('/questions/')
def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        db.add(db_choice)
    db.commit()
    return {"message": "Question created successfully"}

@app.get('/questions/{question_id}')
def read_questions(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Question not found!')
    return result

@app.get('/choices/{question_id}')
def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Choices not found!')
    return result
```

---

## 🧪 Tester votre API

Utilisez :
- Swagger UI ([http://localhost:8000/docs](http://localhost:8000/docs))
- Postman
- Curl

---

## 🧠 Technologies utilisées

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

---

## 📄 Licence

Ce projet est sous licence **MIT**.

---

## 🙌 Remerciements

Merci à la communauté FastAPI et SQLAlchemy pour leurs ressources et documentation de qualité.
