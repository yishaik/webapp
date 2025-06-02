from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(unique=True, index=True)

    prompts: List["Prompt"] = Relationship(back_populates="user")


class Prompt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", nullable=True, index=True)
    base_prompt: str = Field(sa_column_kwargs={"type": "Text"}) # Using Text for potentially long prompts
    timestamp: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"default": datetime.utcnow})

    user: Optional[User] = Relationship(back_populates="prompts")
    questionnaire_responses: List["QuestionnaireResponse"] = Relationship(back_populates="prompt")
    model_outputs: List["ModelOutput"] = Relationship(back_populates="prompt")


class QuestionnaireResponse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    prompt_id: int = Field(foreign_key="prompt.id", index=True)
    question: str = Field(sa_column_kwargs={"type": "Text"})
    answer: str = Field(sa_column_kwargs={"type": "Text"})

    prompt: "Prompt" = Relationship(back_populates="questionnaire_responses")


class ModelOutput(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    prompt_id: int = Field(foreign_key="prompt.id", index=True)
    model_name: str
    # optimized_prompt: str = Field(sa_column_kwargs={"type": "Text"}) # This field was in the old pydantic model but not in the new requirements
    output: str = Field(sa_column_kwargs={"type": "Text"})
    timestamp: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"default": datetime.utcnow})

    prompt: "Prompt" = Relationship(back_populates="model_outputs")