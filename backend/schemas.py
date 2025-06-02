from sqlmodel import SQLModel
from typing import List, Optional
from datetime import datetime

# Re-using User model from models.py for UserRead, as it includes the ID.
# For UserCreate, we define a specific schema.
class UserCreate(SQLModel):
    username: str

class UserRead(SQLModel):
    id: int
    username: str

# Re-using Prompt model from models.py for some read operations.
# PromptCreate will not include server-set fields like id, timestamp, user_id (if taken from auth)
class PromptCreate(SQLModel):
    base_prompt: str
    # user_id will be set in the endpoint logic, not part of this creation schema directly by client usually
    # or if it's for an admin/specific use case, it might be included.
    # For now, assuming user_id is handled by the request context (e.g. current logged-in user)
    # If a user_id needs to be explicitly passed during creation by API, add:
    # user_id: Optional[int] = None

class PromptRead(SQLModel):
    id: int
    user_id: Optional[int]
    base_prompt: str
    timestamp: datetime

# Re-using QuestionnaireResponse model for read.
class QuestionnaireResponseCreate(SQLModel):
    question: str
    answer: str
    # prompt_id will likely be set based on the context of the request.

class QuestionnaireResponseRead(SQLModel):
    id: int
    prompt_id: int
    question: str
    answer: str

# Re-using ModelOutput model for read.
class ModelOutputCreate(SQLModel):
    model_name: str
    output: str
    # prompt_id will be set based on context.

class ModelOutputRead(SQLModel):
    id: int
    prompt_id: int
    model_name: str
    output: str
    timestamp: datetime

# Schemas for nested data (ReadWithDetails)
# These need to refer to the *Read schemas* of the related models, not the table models directly
# if we want to control the output shape precisely (e.g. exclude certain fields from related objects).
# However, SQLModel's default behavior when using relationship attributes often serializes
# the defined model fields, which can be sufficient.

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
    responses: List[QuestionnaireResponseCreate] # Re-using the existing create schema for individual Q&A

# --- Schemas for Prompt Optimization ---
class OptimizePromptRequest(SQLModel):
    prompt_id: int
    target_model: str # For future model-specific optimizations

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
    model_name: str # User-friendly model name, e.g., "Claude Opus 4"

class ModelResponseResponse(SQLModel):
    prompt_id: int
    model_name: str # User-friendly model name
    output: str
    # Potentially also include the optimized_prompt used, for transparency
    optimized_prompt_used: Optional[str] = None

# To make the schemas usable with FastAPI's response_model, need to ensure they have Config.from_attributes = True
# For SQLModel classes that are NOT table models, this is not strictly necessary for pydantic v2+
# but can be good practice if issues arise.
# For SQLModel classes that ARE table models (from models.py), this is handled by SQLModel itself.

# Let's ensure from_attributes (orm_mode) is enabled for our *Read schemas if they are not table models.
# SQLModel automatically enables it for table models.
# For non-table SQLModel schemas, it's also generally enabled by default in Pydantic v2 style.

# The UserRead, PromptRead, etc., if directly derived from SQLModel without table=True,
# will work fine. If we were using Pydantic's BaseModel, we'd add:
# class Config:
# from_attributes = True

# For clarity and to be explicit, especially if we derive from a base SQLModel that isn't a table model
# and want to load data from ORM objects:
# SQLModel (and Pydantic v2+) generally handles from_attributes well by default.
# The re-declarations below are not strictly necessary.
# class UserRead(UserRead):
#     pass
#
# class PromptRead(PromptRead):
#     pass
#
# class QuestionnaireResponseRead(QuestionnaireResponseRead):
#     pass
#
# class ModelOutputRead(ModelOutputRead):
#     pass
#
# class PromptReadWithDetails(PromptReadWithDetails): # This inherits from PromptRead
#     pass
