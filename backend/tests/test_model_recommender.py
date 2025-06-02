import pytest
from backend.model_recommender import recommend_models, extract_keywords_for_recommender, AVAILABLE_MODELS

def test_extract_keywords_for_recommender_basic():
    text = "Write a long creative story about a robot in Python code."
    # Deterministic keyword list with num_keywords=5:
    # creative (8), python (6), about (5), robot (5), story (5)
    expected_keywords = ['creative', 'python', 'about', 'robot', 'story']
    keywords = extract_keywords_for_recommender(text, 5)
    assert keywords == expected_keywords

def test_recommend_models_creative_writing():
    prompt = "Write a poem about the sea."
    answers = ["expressive", "metaphorical language"]
    recommendations = recommend_models(prompt, answers)
    assert "opus" in recommendations or "gpt-4" in recommendations
    assert len(recommendations) >= 1 and len(recommendations) <= 3

def test_recommend_models_coding_task():
    prompt = "Generate a JavaScript function for API call."
    answers = ["needs to be efficient", "handle errors"]
    recommendations = recommend_models(prompt, answers)
    assert "opus" in recommendations or "grok-1" in recommendations or "gpt-4" in recommendations
    assert len(recommendations) >= 1 and len(recommendations) <= 3

def test_recommend_models_quick_summary():
    prompt = "Summarize this text quickly."
    answers = ["bullet points", "short and concise"]
    recommendations = recommend_models(prompt, answers)
    assert "haiku" in recommendations or "gemini-flash" in recommendations or "gpt-3.5" in recommendations
    assert len(recommendations) >= 1 and len(recommendations) <= 3

def test_recommend_models_general_purpose():
    prompt = "What's the weather like today?"
    answers = []
    recommendations = recommend_models(prompt, answers)
    # Expect balanced models
    assert "sonnet" in recommendations or "gemini-pro" in recommendations
    assert len(recommendations) >= 1 and len(recommendations) <= 3

def test_recommend_models_specific_model_mentioned_claude():
    prompt = "I want to use Claude to write an article."
    answers = ["long form content"]
    recommendations = recommend_models(prompt, answers)
    assert "opus" in recommendations
    assert "sonnet" in recommendations

def test_recommend_models_specific_model_mentioned_gpt():
    prompt = "Can GPT help me with this math problem?"
    answers = ["step by step solution"]
    recommendations = recommend_models(prompt, answers)
    assert "gpt-4" in recommendations
    assert "gpt-3.5" in recommendations

def test_recommend_models_no_clear_keywords():
    prompt = "Hello there."
    answers = ["general conversation"]
    recommendations = recommend_models(prompt, answers)
    # Should default to general purpose models
    assert "sonnet" in recommendations or "gemini-pro" in recommendations
    assert len(recommendations) >= 1 and len(recommendations) <= 3

def test_recommend_models_multiple_categories_hits_coding_and_creative():
    # Test that it can hit multiple rules but still limits output
    prompt = "Write a creative python script for a game."
    answers = ["needs to be complex", "story driven game"]
    recommendations = recommend_models(prompt, answers)
    # Expect models good for both coding and creative/complex tasks
    assert "opus" in recommendations or "gpt-4" in recommendations
    # It might also suggest grok due to coding
    # Check total number of recommendations
    assert len(recommendations) <= 3

def test_recommend_models_all_recommended_are_valid_keys():
    prompt = "Tell me something interesting."
    answers = ["surprise me!"]
    recommendations = recommend_models(prompt, answers)
    for model_key in recommendations:
        assert model_key in AVAILABLE_MODELS

def test_recommend_models_empty_prompt_and_answers():
    prompt = ""
    answers = []
    recommendations = recommend_models(prompt, answers)
    assert "sonnet" in recommendations or "gemini-pro" in recommendations # General purpose
    assert len(recommendations) >= 1 and len(recommendations) <= 3

def test_recommend_max_limit():
    # Prompt designed to hit many rules
    prompt = "Create a complex python script for a creative story generation using Claude model, make it quick."
    answers = ["detailed code", "summarize the story too"]
    recommendations = recommend_models(prompt, answers)
    assert len(recommendations) <= 3
