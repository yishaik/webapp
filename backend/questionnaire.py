import re
from typing import List

# Simple keyword-based question generation logic
def generate_questions(base_prompt: str) -> List[str]:
    questions = []
    prompt_lower = base_prompt.lower()

    # Strategy 1: Length-based question
    if len(base_prompt.split()) < 10:  # Arbitrary short length
        questions.append("The prompt is quite short. Could you specify the desired length or verbosity of the response?")

    # Strategy 2: Keyword "code" or language names
    code_keywords = ["code", "python", "javascript", "java", "c++", "script", "program"]
    if any(keyword in prompt_lower for keyword in code_keywords):
        questions.append("What programming language are you focusing on for the code generation (if any specific)?")
        questions.append("Are there any specific libraries or frameworks to be used or avoided?")

    # Strategy 3: Keyword "explain" or "define"
    explanation_keywords = ["explain", "define", "what is", "describe"]
    if any(keyword in prompt_lower for keyword in explanation_keywords):
        questions.append("What is the target audience for this explanation (e.g., beginner, intermediate, expert)?")

    # Strategy 4: Keyword "compare" or "contrast"
    comparison_keywords = ["compare", "contrast", "difference between"]
    if any(keyword in prompt_lower for keyword in comparison_keywords):
        questions.append("What are the key aspects or criteria you want to focus on for the comparison/contrast?")

    # Strategy 5: Content type specific questions
    if "email" in prompt_lower:
        questions.append("What is the purpose of this email (e.g., inquiry, marketing, follow-up)?")
    if "story" in prompt_lower or "narrative" in prompt_lower:
        questions.append("What is the main genre of the story (e.g., fantasy, sci-fi, romance)?")
    if "marketing" in prompt_lower or "advertisement" in prompt_lower:
        questions.append("What is the product or service being marketed?")

    # Strategy 6: Generic fallback questions if not too many specific ones already
    if len(questions) < 2:  # Add generic if we don't have many questions yet
        questions.append("Are there any specific constraints or requirements for the output (e.g., tone, style, format)?")

    if not questions:  # Ensure at least one question is always asked
        questions.append("What is the primary goal or objective of this prompt?")
        questions.append("Is there a specific format or structure you expect for the response?")

    # Limit to 3-5 questions as per requirement
    return questions[:5]
