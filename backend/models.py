from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    
    prompts = relationship("Prompt", back_populates="user")

class Prompt(Base):
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    base_prompt = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="prompts")
    questionnaire_responses = relationship("QuestionnaireResponse", back_populates="prompt")
    model_outputs = relationship("ModelOutput", back_populates="prompt")

class QuestionnaireResponse(Base):
    __tablename__ = "questionnaire_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), index=True)
    question = Column(Text)
    answer = Column(Text)
    
    prompt = relationship("Prompt", back_populates="questionnaire_responses")

class ModelOutput(Base):
    __tablename__ = "model_outputs"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), index=True)
    model_name = Column(String)
    output = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    prompt = relationship("Prompt", back_populates="model_outputs")

# Pydantic models for API responses
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class PromptBase(BaseModel):
    base_prompt: str

class PromptCreate(PromptBase):
    user_id: Optional[int] = None

class PromptResponse(PromptBase):
    id: int
    user_id: Optional[int]
    timestamp: datetime

    class Config:
        from_attributes = True

class QuestionnaireSubmission(BaseModel):
    prompt: str
    answers: List[str]

class RecommendModelsRequest(BaseModel):
    initial_prompt: str
    questionnaire_answers: List[str]