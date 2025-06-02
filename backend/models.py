from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class PromptBase(BaseModel):
    base_prompt: str

class PromptCreate(PromptBase):
    user_id: int

class Prompt(PromptBase):
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class QuestionnaireResponseBase(BaseModel):
    question: str
    answer: str

class QuestionnaireResponseCreate(QuestionnaireResponseBase):
    prompt_id: int

class QuestionnaireResponse(QuestionnaireResponseBase):
    id: int
    prompt_id: int
    
    class Config:
        from_attributes = True

class ModelOutputBase(BaseModel):
    model_name: str
    optimized_prompt: str
    output: str

class ModelOutputCreate(ModelOutputBase):
    prompt_id: int

class ModelOutput(ModelOutputBase):
    id: int
    prompt_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class PromptOptimizationRequest(BaseModel):
    base_prompt: str
    questionnaire_responses: List[QuestionnaireResponseBase]
    selected_models: List[str]

class OptimizedPromptResponse(BaseModel):
    model_name: str
    optimized_prompt: str
    output: Optional[str] = None