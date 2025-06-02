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
class OptimizePromptRequest(SQLModel): # Modified as per task
    base_prompt: str
    questionnaire_responses: Optional[List[QuestionnaireResponseCreate]] = []
    target_model: Optional[str] = None

class OptimizedPromptResponse(SQLModel):
    optimized_prompt: str

# --- Schemas for Model Recommendation ---
class RecommendModelsByIdRequest(SQLModel): # Renamed from RecommendModelsRequest
    prompt_id: int

class ModelRecommendationDirectRequest(SQLModel): # New schema as per task
    base_prompt: str
    questionnaire_responses: Optional[List[QuestionnaireResponseCreate]] = []

class RecommendedModelsResponse(SQLModel):
    models: List[str]

# --- Schemas for Model Interaction / Response Endpoint ---
# Existing ModelResponseRequest & ModelResponseResponse might be for a different flow or deprecated by ModelInteraction
class OldModelResponseRequest(SQLModel): # Renamed to avoid confusion if new one is ModelResponseRequest
    prompt_id: int
    model_name: str

class OldModelResponseResponse(SQLModel): # Renamed
    prompt_id: int
    model_name: str
    output: str
    optimized_prompt_used: Optional[str] = None

# New Schemas for Unified Model Interaction Endpoint
class ModelInteractionRequest(SQLModel):
    prompt_id: Optional[int] = None
    base_prompt: Optional[str] = None
    questionnaire_responses: Optional[List[QuestionnaireResponseCreate]] = []
    model_name: str
    optimized_prompt_override: Optional[str] = None

class ModelInteractionResponse(SQLModel):
    model_name: str
    output: str
    prompt_id: Optional[int] = None
    optimized_prompt_used: Optional[str] = None # Added to match old response, seems useful
