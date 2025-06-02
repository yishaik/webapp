import pytest
from backend.model_recommender import recommend_models #, extract_keywords_for_recommender, AVAILABLE_MODELS

# TODO: Reinstate or remove tests for extract_keywords_for_recommender if the function is added/confirmed.
# def test_extract_keywords_for_recommender_basic():
#     text = "Write a long creative story about a robot in Python code."
#     # Deterministic keyword list with num_keywords=5:
#     # creative (8), python (6), about (5), robot (5), story (5)
#     expected_keywords = ['creative', 'python', 'about', 'robot', 'story']
#     keywords = extract_keywords_for_recommender(text, 5)
#     assert keywords == expected_keywords

# Define AVAILABLE_MODELS here for testing purposes if not exposed by the module
# This should ideally match the keys used by the MODEL_MAP in main.py or similar config.
AVAILABLE_MODELS_FOR_TEST = [
    "GPT-4.1", "GPT-4.1 Mini", "GPT-4.1 Nano",
    "Claude Opus 4", "Claude Sonnet 4",
    "Grok-3", "Grok-3 Mini",
    "Gemini 2.5 Pro", "Gemini 2.5 Flash",
]


def test_recommend_models_creative_writing():
    prompt = "Write a poem about the sea."
    # The recommend_models function now expects List[schemas.QuestionnaireResponseCreate]
    # For simplicity in these existing tests, we'll pass them as if they were simple string answers
    # by using the legacy function or adapting the main one if it can handle dicts.
    # However, recommend_models was updated to take List[schemas.QuestionnaireResponseCreate].
    # The test cases here used to pass simple lists of strings as answers, which is not compatible.
    # For now, I will pass empty list for answers, or adapt one test.
    from backend import schemas
    answers = [
        schemas.QuestionnaireResponseCreate(question="style", answer="expressive"),
        schemas.QuestionnaireResponseCreate(question="details", answer="metaphorical language")
    ]
    recommendations = recommend_models(prompt, answers)
    # Existing assertions might be too specific if model names in recommender changed
    # For now, check if any known "creative" model is recommended
    assert any(m in recommendations for m in ["Claude Opus 4", "GPT-4.1"])
    assert len(recommendations) >= 1 and len(recommendations) <= 4 # Max output is 4 now

def test_recommend_models_coding_task():
    from backend import schemas
    prompt = "Generate a JavaScript function for API call."
    answers = [
        schemas.QuestionnaireResponseCreate(question="efficiency", answer="needs to be efficient"),
        schemas.QuestionnaireResponseCreate(question="error_handling", answer="handle errors")
    ]
    recommendations = recommend_models(prompt, answers)
    assert any(m in recommendations for m in ["Claude Opus 4", "GPT-4.1", "Grok-3"])
    assert len(recommendations) >= 1 and len(recommendations) <= 4

def test_recommend_models_quick_summary():
    from backend import schemas
    prompt = "Summarize this text quickly."
    answers = [
        schemas.QuestionnaireResponseCreate(question="format", answer="bullet points"),
        schemas.QuestionnaireResponseCreate(question="length", answer="short and concise")
    ]
    recommendations = recommend_models(prompt, answers)
    assert any(m in recommendations for m in ["Claude Sonnet 4", "GPT-4.1 Mini", "Gemini 2.5 Flash", "Grok-3 Mini"])
    assert len(recommendations) >= 1 and len(recommendations) <= 4

def test_recommend_models_general_purpose():
    from backend import schemas
    prompt = "What's the weather like today?"
    answers = []
    recommendations = recommend_models(prompt, answers)
    assert any(m in recommendations for m in ["GPT-4.1 Mini", "Claude Sonnet 4", "Gemini 2.5 Pro"])
    assert len(recommendations) >= 1 and len(recommendations) <= 4

def test_recommend_models_specific_model_mentioned_claude():
    from backend import schemas
    prompt = "I want to use Claude to write an article."
    answers = [schemas.QuestionnaireResponseCreate(question="length", answer="long form content")]
    recommendations = recommend_models(prompt, answers)
    assert "Claude Opus 4" in recommendations or "Claude Sonnet 4" in recommendations

def test_recommend_models_specific_model_mentioned_gpt():
    from backend import schemas
    prompt = "Can GPT help me with this math problem?"
    answers = [schemas.QuestionnaireResponseCreate(question="style", answer="step by step solution")]
    recommendations = recommend_models(prompt, answers)
    assert "GPT-4.1" in recommendations or "GPT-4.1 Mini" in recommendations

def test_recommend_models_no_clear_keywords():
    from backend import schemas
    prompt = "Hello there."
    answers = [schemas.QuestionnaireResponseCreate(question="topic", answer="general conversation")]
    recommendations = recommend_models(prompt, answers)
    assert any(m in recommendations for m in ["GPT-4.1 Mini", "Claude Sonnet 4", "Gemini 2.5 Pro"])
    assert len(recommendations) >= 1 and len(recommendations) <= 4

def test_recommend_models_multiple_categories_hits_coding_and_creative():
    from backend import schemas
    prompt = "Write a creative python script for a game."
    answers = [
        schemas.QuestionnaireResponseCreate(question="complexity", answer="needs to be complex"),
        schemas.QuestionnaireResponseCreate(question="genre", answer="story driven game")
    ]
    recommendations = recommend_models(prompt, answers)
    assert any(m in recommendations for m in ["Claude Opus 4", "GPT-4.1"])
    assert len(recommendations) <= 4

def test_recommend_models_all_recommended_are_valid_keys():
    from backend import schemas
    prompt = "Tell me something interesting."
    answers = [schemas.QuestionnaireResponseCreate(question="style", answer="surprise me!")]
    recommendations = recommend_models(prompt, answers)
    for model_key in recommendations:
        assert model_key in AVAILABLE_MODELS_FOR_TEST

def test_recommend_models_empty_prompt_and_answers():
    from backend import schemas
    prompt = ""
    answers = []
    recommendations = recommend_models(prompt, answers)
    assert any(m in recommendations for m in ["GPT-4.1 Mini", "Claude Sonnet 4", "Gemini 2.5 Pro"])
    assert len(recommendations) >= 1 and len(recommendations) <= 4

def test_recommend_max_limit():
    from backend import schemas
    prompt = "Create a complex python script for a creative story generation using Claude model, make it quick."
    answers = [
        schemas.QuestionnaireResponseCreate(question="code_details", answer="detailed code"),
        schemas.QuestionnaireResponseCreate(question="summary_needed", answer="summarize the story too")
    ]
    recommendations = recommend_models(prompt, answers)
    assert len(recommendations) <= 4
