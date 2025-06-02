import pytest
from backend.model_recommender import recommend_models
from backend.schemas import QuestionnaireResponseRead # Assuming this is the schema used

# Helper to create mock QuestionnaireResponseRead objects for tests
def create_qr_read(question: str, answer: str, id: int = 1, prompt_id: int = 1) -> QuestionnaireResponseRead:
    return QuestionnaireResponseRead(id=id, prompt_id=prompt_id, question=question, answer=answer)

def test_recommend_models_creative_writing():
    prompt = "Write a short story about a space adventure."
    answers = []
    recommendations = recommend_models(prompt, answers)
    assert "Claude Opus 4" in recommendations
    assert "GPT-4.1" in recommendations

def test_recommend_models_summary_short_answer():
    prompt = "Summarize this document quickly."
    answers = []
    recommendations = recommend_models(prompt, answers)
    assert "Claude Sonnet 4" in recommendations
    assert "GPT-4.1 Mini" in recommendations
    assert "Gemini 2.5 Flash" in recommendations
    assert "Grok-3 Mini" in recommendations

def test_recommend_models_code_programming():
    prompt = "Develop a python script for data analysis."
    answers = []
    recommendations = recommend_models(prompt, answers)
    assert "Claude Opus 4" in recommendations
    assert "GPT-4.1" in recommendations
    assert "Grok-3" in recommendations

def test_recommend_models_explanation_detailed():
    prompt = "Explain the theory of relativity in detail."
    answers = []
    recommendations = recommend_models(prompt, answers)
    assert "GPT-4.1" in recommendations
    assert "Claude Opus 4" in recommendations
    assert "Claude Sonnet 4" in recommendations # Also good for explanations

def test_recommend_models_default_fallback():
    prompt = "What's the weather like today?" # No strong keywords
    answers = []
    recommendations = recommend_models(prompt, answers)
    assert "GPT-4.1 Mini" in recommendations
    assert "Claude Sonnet 4" in recommendations
    assert "GPT-4.1" in recommendations # General purpose fallback

def test_recommend_models_with_questionnaire_answers_json_format():
    prompt = "Parse this data."
    answers = [create_qr_read("Desired output format?", "JSON format please")]
    recommendations = recommend_models(prompt, answers)
    # Check if models good for JSON are added/prioritized
    assert "GPT-4.1" in recommendations
    assert "Claude Opus 4" in recommendations

def test_recommend_models_with_questionnaire_answers_formal_tone():
    prompt = "Write a business proposal."
    answers = [create_qr_read("What is the desired tone?", "Very formal and professional")]
    recommendations = recommend_models(prompt, answers)
    assert "Claude Opus 4" in recommendations # Known for formal tone

def test_recommend_models_uniqueness_of_recommendations():
    # Prompt that could trigger multiple rules leading to same model
    prompt = "Explain how to code a creative story summary in python."
    answers = []
    recommendations = recommend_models(prompt, answers)
    # Ensure each recommended model appears only once
    assert len(recommendations) == len(set(recommendations))
    # Check some expected models (exact list depends on internal set logic)
    assert "Claude Opus 4" in recommendations
    assert "GPT-4.1" in recommendations

def test_recommend_models_empty_prompt():
    prompt = ""
    answers = []
    recommendations = recommend_models(prompt, answers)
    # Should still return default/fallback recommendations
    assert "GPT-4.1 Mini" in recommendations
    assert "Claude Sonnet 4" in recommendations
    assert "GPT-4.1" in recommendations

def test_recommend_models_no_answers():
    prompt = "Tell me a joke." # Generic enough
    answers = [] # No answers provided
    recommendations = recommend_models(prompt, answers)
    # Should rely solely on prompt content, likely hitting fallback
    assert len(recommendations) > 0
    assert "GPT-4.1 Mini" in recommendations # Part of fallback
    assert "Claude Sonnet 4" in recommendations # Part of fallback
    assert "GPT-4.1" in recommendations # Part of fallback
