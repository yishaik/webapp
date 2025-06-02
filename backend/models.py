from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)

    prompts: List["Prompt"] = Relationship(back_populates="user")

class Prompt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", nullable=True)
    base_prompt: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="prompts")
    questionnaire_responses: List["QuestionnaireResponse"] = Relationship(back_populates="prompt")
    model_outputs: List["ModelOutput"] = Relationship(back_populates="prompt")

class QuestionnaireResponse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompt_id: int = Field(foreign_key="prompt.id")
    question: str
    answer: str

    prompt: Prompt = Relationship(back_populates="questionnaire_responses")

class ModelOutput(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompt_id: int = Field(foreign_key="prompt.id")
    model_name: str
    output: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    prompt: Prompt = Relationship(back_populates="model_outputs")
