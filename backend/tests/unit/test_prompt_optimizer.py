import pytest
from backend.prompt_optimizer import optimize_prompt
from backend.schemas import QuestionnaireResponseRead # Assuming this is the schema used

# Helper to create mock QuestionnaireResponseRead objects for tests
def create_qr_read(question: str, answer: str, id: int = 1, prompt_id: int = 1) -> QuestionnaireResponseRead:
    # The actual schema might require id, prompt_id. We provide defaults.
    # If QuestionnaireResponseRead is a SQLModel table model, it might behave differently.
    # Based on schemas.py, it's a SQLModel class not inheriting from table=True, so direct instantiation is fine.
    return QuestionnaireResponseRead(id=id, prompt_id=prompt_id, question=question, answer=answer)

def test_optimize_prompt_basic_concatenation():
    base_prompt = "Translate this to French."
    answers = [
        create_qr_read(question="Target audience?", answer="Adult"),
        create_qr_read(question="Desired tone?", answer="Formal")
    ]
    target_model = "test_model"
    optimized = optimize_prompt(base_prompt, answers, target_model)

    assert base_prompt in optimized
    assert "Target audience is: Adult." in optimized
    assert "Consider also: Desired tone? - Formal." in optimized # Generic fallback for this answer

def test_optimize_prompt_adds_role_playing():
    base_prompt = "Explain dark matter."
    answers = []
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    assert "Act as an expert in the relevant domain." in optimized

def test_optimize_prompt_does_not_add_role_if_present_in_base():
    base_prompt = "Act as a historian and explain the French Revolution."
    answers = []
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    # Count occurrences to ensure it's not added again
    assert optimized.lower().count("act as") == 1

def test_optimize_prompt_does_not_add_role_if_implied_in_answers():
    base_prompt = "Explain the French Revolution."
    answers = [create_qr_read("Any specific perspective?", "Yes, act as a historian.")]
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    # The answer itself will be appended, which includes "act as"
    assert "act as a historian" in optimized.lower()
    # Check that the generic "Act as an expert" is not added additionally
    assert "Act as an expert in the relevant domain." not in optimized or optimized.lower().count("act as an expert") == 0


def test_optimize_prompt_adds_step_by_step():
    base_prompt = "Solve this complex problem."
    answers = []
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    assert "Think step by step" in optimized

def test_optimize_prompt_does_not_add_step_by_step_if_present():
    base_prompt = "Solve this complex problem. Think step-by-step."
    answers = []
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    assert optimized.lower().count("step-by-step") == 1 or optimized.lower().count("step by step") == 1


def test_optimize_prompt_adds_clarity_conciseness():
    base_prompt = "Describe your product."
    answers = []
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    assert "Ensure your response is clear, concise" in optimized

def test_optimize_prompt_does_not_add_clarity_if_present():
    base_prompt = "Describe your product. Ensure your response is clear and concise."
    answers = []
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    assert optimized.lower().count("clear and concise") == 1

def test_optimize_prompt_handles_specific_answer_keywords():
    base_prompt = "Write code."
    answers = [
        create_qr_read(question="What is the desired length?", answer="Approx 100 lines"),
        create_qr_read(question="Target audience?", answer="Expert developers"),
        create_qr_read(question="What programming language?", answer="Python")
    ]
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    assert "Ensure the response has a length of approximately: Approx 100 lines." in optimized
    assert "The target audience is: Expert developers." in optimized
    assert "The preferred programming language is Python." in optimized

def test_optimize_prompt_ignores_irrelevant_answers_for_specific_keywords():
    base_prompt = "Summarize this document."
    answers = [
        create_qr_read(question="What programming language?", answer="None"),
        create_qr_read(question="Desired length?", answer="N/A")
    ]
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    assert "programming language" not in optimized
    # "N/A" for length might be appended by generic "Consider also" if that logic is hit
    # The current optimizer adds "Consider also: Desired length? - N/A."
    # This can be refined in the optimizer if "N/A" type answers should be fully ignored.
    assert "Consider also: Desired length? - N/A" in optimized
    assert "Ensure the response has a length of approximately: N/A" not in optimized


def test_optimize_prompt_empty_answers():
    base_prompt = "This is a test."
    answers = []
    optimized = optimize_prompt(base_prompt, answers, "test_model")
    assert base_prompt in optimized
    assert "Act as an expert" in optimized
    assert "Think step by step" in optimized
    assert "clear, concise" in optimized

def test_optimize_prompt_target_model_placeholder():
    # Currently, target_model does not change logic, so this is a basic check.
    base_prompt = "Test."
    answers = []
    optimized_generic = optimize_prompt(base_prompt, answers, "generic_model")
    optimized_specific = optimize_prompt(base_prompt, answers, "some_specific_model")
    # Expect them to be the same as no specific logic for 'some_specific_model' exists.
    assert optimized_generic == optimized_specific
