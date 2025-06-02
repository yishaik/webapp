from sqlmodel import SQLModel
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserCreate(SQLModel):
    username: str

class UserRead(SQLModel):
    id: int
    username: str

# Prompt Schemas
class PromptCreate(SQLModel):
    base_prompt: str

class PromptRead(SQLModel):
    id: int
    user_id: Optional[int]
    base_prompt: str
    timestamp: datetime

# QuestionnaireResponse Schemas
class QuestionnaireResponseCreate(SQLModel):
    question: str
    answer: str

class QuestionnaireResponseRead(SQLModel):
    id: int
    prompt_id: int
    question: str
    answer: str

# ModelOutput Schemas
class ModelOutputCreate(SQLModel):
    model_name: str
    output: str

class ModelOutputRead(SQLModel):
    id: int
    prompt_id: int
    model_name: str
    output: str
    timestamp: datetime

# Schemas for nested data (ReadWithDetails)
class PromptReadWithDetails(PromptRead):
    questionnaire_responses: List[QuestionnaireResponseRead] = []
    model_outputs: List[ModelOutputRead] = []

# --- Schemas for Questionnaire Generation ---
class InitialPromptRequest(SQLModel):
    base_prompt: str

class GeneratedQuestionnaire(SQLModel):
    questions: List[str]

# --- Schemas for Questionnaire Submission ---
class SubmitQuestionnaireRequest(SQLModel):
    base_prompt: str
    responses: List[QuestionnaireResponseCreate]

# --- Schemas for Prompt Optimization ---
class OptimizePromptRequest(SQLModel):
    prompt_id: int
    target_model: str

class OptimizedPromptResponse(SQLModel):
    optimized_prompt: str

# --- Schemas for Model Recommendation ---
class RecommendModelsRequest(SQLModel):
    prompt_id: int

class RecommendedModelsResponse(SQLModel):
    models: List[str]

# --- Schemas for Model Response Endpoint ---
class ModelResponseRequest(SQLModel):
    prompt_id: int
    model_name: str

class ModelResponseResponse(SQLModel):
    prompt_id: int
    model_name: str
    output: str
    optimized_prompt_used: Optional[str] = None
