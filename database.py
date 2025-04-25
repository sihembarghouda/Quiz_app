from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL de connexion à PostgreSQL
# Le problème est ici dans la chaîne de connexion
URL_DATABASE = 'postgresql://postgres:0000@localhost:5432/quizApp'

# Créer un moteur pour la base de données
engine = create_engine(URL_DATABASE)

# Créer une session locale pour interagir avec la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()