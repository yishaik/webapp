from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None


# Forward references for nested Read schemas
# These will be fully defined later in the file.
class QuestionnaireResponseRead(BaseModel):
    id: int
    prompt_id: int
    question: str
    answer: str

    class Config:
        from_attributes = True

class ModelOutputRead(BaseModel):
    id: int
    prompt_id: int
    model_name: str
    output: str
    timestamp: datetime

    class Config:
        from_attributes = True


# Prompt Schemas
class PromptBase(BaseModel):
    base_prompt: str

class PromptCreate(PromptBase):
    user_id: Optional[int] = None

class PromptRead(PromptBase):
    id: int
    user_id: Optional[int] = None
    timestamp: datetime
    questionnaire_responses: List[QuestionnaireResponseRead] = []
    model_outputs: List[ModelOutputRead] = []

    class Config:
        from_attributes = True

class PromptUpdate(BaseModel):
    base_prompt: Optional[str] = None
    user_id: Optional[int] = None


# QuestionnaireResponse Schemas
class QuestionnaireResponseBase(BaseModel):
    question: str
    answer: str

class QuestionnaireResponseCreate(QuestionnaireResponseBase):
    prompt_id: int # Required when creating a response

# QuestionnaireResponseRead is defined above for PromptRead to use

class QuestionnaireResponseUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    # prompt_id: Optional[int] = None # Decided to remove this, less common to update parent ID


# ModelOutput Schemas
class ModelOutputBase(BaseModel):
    model_name: str
    output: str

class ModelOutputCreate(ModelOutputBase):
    prompt_id: int # Required when creating an output

# ModelOutputRead is defined above for PromptRead to use

class ModelOutputUpdate(BaseModel):
    model_name: Optional[str] = None
    output: Optional[str] = None
    # prompt_id: Optional[int] = None # Decided to remove this


# Pydantic v1 style update_forward_refs if needed, though direct definition order is preferred.
# For Pydantic v2, this is often not needed if types are correctly hinted (e.g. using strings for forward refs)
# and models are in the same module.
# If UserRead needed to be in PromptRead and was defined later, we'd do:
# PromptRead.update_forward_refs()
# UserRead.update_forward_refs()
# etc. for all models that might have forward references.
# Given the order of definition, explicit update_forward_refs might not be strictly necessary here,
# but it's good practice if there's any doubt or for more complex dependency graphs.

# It's generally better to define dependent models first or use string type hints ('ClassName')
# and then call Model.update_forward_refs() on the models that use them.
# The above structure defines QuestionnaireResponseRead and ModelOutputRead before PromptRead,
# so direct type hinting works.

# No explicit update_forward_refs calls needed due to definition order.


# Request Schemas for new endpoints
class QuestionnaireResponseCreateNoPromptId(QuestionnaireResponseBase): # For use in SubmitQuestionnaireRequest
    pass

class ModelOutputCreateNoPromptId(ModelOutputBase): # For use in creating model output without prompt_id in body
    pass

class SubmitQuestionnaireRequest(BaseModel):
    base_prompt: str
    user_id: Optional[int] = None
    responses: List[QuestionnaireResponseCreateNoPromptId]
