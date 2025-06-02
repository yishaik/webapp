from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

SQLITE_DATABASE_URL = "sqlite:///./prompts.db"

engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    
    prompts = relationship("Prompt", back_populates="user")

class Prompt(Base):
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    base_prompt = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="prompts")
    questionnaire_responses = relationship("QuestionnaireResponse", back_populates="prompt")
    model_outputs = relationship("ModelOutput", back_populates="prompt")

class QuestionnaireResponse(Base):
    __tablename__ = "questionnaire_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    question = Column(Text)
    answer = Column(Text)
    
    prompt = relationship("Prompt", back_populates="questionnaire_responses")

class ModelOutput(Base):
    __tablename__ = "model_outputs"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"))
    model_name = Column(String)
    optimized_prompt = Column(Text)
    output = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    prompt = relationship("Prompt", back_populates="model_outputs")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)