import pytest
from backend.questionnaire import generate_questions

def test_generate_questions_short_prompt():
    prompt = "Short one."
    questions = generate_questions(prompt)
    assert "The prompt is quite short. Could you specify the desired length or verbosity of the response?" in questions

def test_generate_questions_code_keywords():
    prompt = "Write python code for a function."
    questions = generate_questions(prompt)
    assert "What programming language are you focusing on for the code generation (if any specific)?" in questions
    assert "Are there any specific libraries or frameworks to be used or avoided?" in questions

def test_generate_questions_explanation_keywords():
    prompt = "Explain black holes to me."
    questions = generate_questions(prompt)
    assert "What is the target audience for this explanation (e.g., beginner, intermediate, expert)?" in questions

def test_generate_questions_comparison_keywords():
    prompt = "Compare SQL and NoSQL databases."
    questions = generate_questions(prompt)
    assert "What are the key aspects or criteria you want to focus on for the comparison/contrast?" in questions

def test_generate_questions_generic_fallback_if_few_specific():
    prompt = "A very generic and neutral prompt that doesn't trigger other rules."
    # This prompt is longer than 10 words, so it won't trigger the short prompt question by default.
    # It also doesn't contain specific keywords for code, explanation, or comparison.
    questions = generate_questions(prompt)
    # Depending on the internal logic of generate_questions, it might hit the "if len(questions) < 2"
    # or the "if not questions" fallback.
    assert len(questions) > 0
    if len(questions) < 2: # This condition in test might be tricky due to generate_questions internal logic
         assert "Are there any specific constraints or requirements for the output (e.g., tone, style, format)?" in questions
    else: # If it already generated 2 or more (e.g. from the "if not questions" block)
        # Check if the generic fallback (if not questions) was hit
        assert any("primary goal or objective" in q for q in questions) or \
               any("specific format or structure" in q for q in questions) or \
               "Are there any specific constraints or requirements for the output (e.g., tone, style, format)?" in questions


def test_generate_questions_always_returns_questions():
    prompt = "alskdjfhalskdjfhalksdjfh" # Gibberish, long enough
    questions = generate_questions(prompt)
    assert len(questions) > 0
    # Should hit the "if not questions:" fallback in generate_questions
    assert "What is the primary goal or objective of this prompt?" in questions
    assert "Is there a specific format or structure you expect for the response?" in questions


def test_generate_questions_max_five():
    # Construct a prompt that could trigger many rules
    prompt = "Explain python code to compare a short story. Define it."
    questions = generate_questions(prompt)
    assert len(questions) <= 5

def test_generate_questions_empty_prompt():
    prompt = ""
    questions = generate_questions(prompt)
    # Should still ask for clarification
    assert "The prompt is quite short. Could you specify the desired length or verbosity of the response?" in questions
    assert len(questions) > 0

def test_generate_questions_long_prompt_no_keywords():
    prompt = "This is a fairly long sentence that does not contain any of the specific keywords like code or explain or compare and it should result in some generic questions."
    questions = generate_questions(prompt)
    # Expecting fallback questions
    assert len(questions) > 0
    assert any("primary goal or objective" in q for q in questions) or \
           any("specific format or structure" in q for q in questions) or \
           "Are there any specific constraints or requirements for the output (e.g., tone, style, format)?" in questions

# Example of a prompt that might trigger multiple specific questions
def test_generate_questions_multiple_keywords():
    prompt = "Can you explain how to code a Python script that compares two text files?"
    questions = generate_questions(prompt)
    assert "What programming language are you focusing on for the code generation (if any specific)?" in questions
    assert "Are there any specific libraries or frameworks to be used or avoided?" in questions
    assert "What is the target audience for this explanation (e.g., beginner, intermediate, expert)?" in questions
    # It might also trigger comparison, but the question limit is 5.
    # The exact set depends on the order of checks in generate_questions.
    assert len(questions) <= 5
    assert len(questions) >= 3 # Expecting at least 3 specific questions here
