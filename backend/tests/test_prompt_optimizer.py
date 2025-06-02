import pytest
from backend.prompt_optimizer import optimize_prompt #, extract_keywords, get_domain_from_keywords
from backend import schemas # For creating QuestionnaireResponseCreate objects

# TODO: Reinstate or remove tests for extract_keywords and get_domain_from_keywords if those functions are added/confirmed.
# def test_extract_keywords_simple():
#     text = "This is a simple test sentence for keyword extraction."
#     keywords = extract_keywords(text, 4)
#     assert "extraction" in keywords
#     assert "sentence" in keywords
#     assert "keyword" in keywords
#     assert "simple" in keywords

# def test_extract_keywords_empty_text():
#     text = ""
#     keywords = extract_keywords(text)
#     assert keywords == []

# def test_extract_keywords_no_long_words():
#     text = "a of the to is"
#     keywords = extract_keywords(text)
#     assert keywords == []

# def test_get_domain_from_keywords_coding():
#     keywords = ["python", "script", "algorithm"]
#     domain = get_domain_from_keywords(keywords)
#     assert domain == "software development"

# def test_get_domain_from_keywords_medical():
#     keywords = ["health", "patient", "treatment"]
#     domain = get_domain_from_keywords(keywords)
#     assert domain == "medicine"

# def test_get_domain_from_keywords_generic():
#     keywords = ["document", "summary", "report"]
#     domain = get_domain_from_keywords(keywords)
#     assert domain == "the field of document"

# def test_get_domain_from_keywords_empty():
#     keywords = []
#     domain = get_domain_from_keywords(keywords)
#     assert domain == "the relevant field"

def test_optimize_prompt_basic():
    initial_prompt = "Write a poem about nature."
    answers = [
        schemas.QuestionnaireResponseCreate(question="length", answer="short"),
        schemas.QuestionnaireResponseCreate(question="audience", answer="for children")
    ]
    target_model = "gpt-3.5" # In new optimizer, this is "gpt-4.1-nano" or similar
    optimized = optimize_prompt(initial_prompt, answers, target_model)

    assert "You are an expert" in optimized # Default role-playing
    assert initial_prompt in optimized
    assert "Ensure the response has a length of approximately: short" in optimized
    assert "The target audience is: for children" in optimized
    assert "Leverage advanced reasoning capabilities for GPT-4." not in optimized # Check specific model optimization

def test_optimize_prompt_coding_task_and_format():
    initial_prompt = "Generate a python function to sort a list."
    answers = [
        schemas.QuestionnaireResponseCreate(question="details", answer="list of numbers"),
        schemas.QuestionnaireResponseCreate(question="algorithm", answer="efficient algorithm"),
        schemas.QuestionnaireResponseCreate(question="complexity", answer="complex task"),
        schemas.QuestionnaireResponseCreate(question="output format", answer="JSON output with explanation")
    ]
    target_model = "gpt-4.1" # Matches "gpt-4" in optimizer logic
    optimized = optimize_prompt(initial_prompt, answers, target_model)

    assert "You are an expert in the relevant domain." in optimized # Generic role if not specified by answers
    assert initial_prompt in optimized
    assert "Please provide the output in JSON format." in optimized
    assert "Leverage advanced reasoning capabilities for GPT-4." in optimized
    assert "Think step by step." in optimized # Due to "complex"

def test_optimize_prompt_step_by_step_from_prompt():
    initial_prompt = "Explain photosynthesis step by step."
    answers = [
        schemas.QuestionnaireResponseCreate(question="audience", answer="for high school students")
    ]
    target_model = "claude-sonnet-4" # Matches "claude"
    optimized = optimize_prompt(initial_prompt, answers, target_model)

    # "Think step by step." might not be added again if already in prompt.
    # The current logic in optimizer checks for "step by step" in base_prompt.
    assert initial_prompt in optimized # Original prompt should be there
    assert optimized.count("Think step by step.") == 1 # Ensure not duplicated
    assert "Be thorough and analytical in your response, as expected for Claude models." in optimized

def test_optimize_prompt_no_answers():
    initial_prompt = "What is the capital of France?"
    answers = []
    target_model = "gemini-2.5-flash" # Matches "gemini"
    optimized = optimize_prompt(initial_prompt, answers, target_model)

    assert "You are an expert" in optimized
    assert initial_prompt in optimized
    assert "Utilize Gemini's multimodal understanding if applicable." in optimized

def test_optimize_prompt_role_from_answers():
    initial_prompt = "Create a new character for a fantasy story."
    answers = [
        schemas.QuestionnaireResponseCreate(question="role", answer="Act as an expert storyteller specialized in mythology.")
    ]
    target_model = "claude-opus-4"
    optimized = optimize_prompt(initial_prompt, answers, target_model)

    # Role from answers should take precedence and be specific.
    assert "You are an expert in storyteller specialized in mythology." in optimized
    assert "Act as an expert in the relevant domain." not in optimized or optimized.count("You are an expert") == 1


def test_optimize_prompt_no_strategies_if_already_present_in_base():
    initial_prompt = "You are an expert in history. Think step by step. Write a detailed essay about the Roman Empire. Output in markdown."
    answers = [
        schemas.QuestionnaireResponseCreate(question="style", answer="Ensure it is comprehensive")
    ]
    target_model = "gpt-4.1"

    optimized = optimize_prompt(initial_prompt, answers, target_model)

    # Check that "You are an expert" is not added again if similar phrase already there.
    assert optimized.count("You are an expert") == 1
    # Check that "Think step by step" is not added again.
    assert optimized.count("Think step by step.") == 1
    # Markdown might be added again if not perfectly matched by the answer format check (question needs to be "format")
    # For this test, let's assume the "Output in markdown" in prompt is enough.
    # The answer "Ensure it is comprehensive" does not trigger format rule.
    assert "Please provide the output in Markdown format." not in optimized # Because no answer triggered it
    assert initial_prompt in optimized
    assert "Use a Ensure it is comprehensive tone/style." in optimized # From the answer
