from typing import List
from . import schemas # Assuming schemas.py contains QuestionnaireResponseRead

def recommend_models(
    base_prompt: str,
    questionnaire_answers: List[schemas.QuestionnaireResponseRead] # For potential future use
) -> List[str]:
    """
    Recommends models based on keywords in the base prompt.
    Questionnaire answers are available for more complex future logic.
    """
    recommendations = set() # Use a set to avoid duplicate recommendations initially
    prompt_lower = base_prompt.lower()

    # Rule 1: Creative writing
    creative_keywords = ["creative writing", "story", "poem", "write a novel", "screenplay"]
    if any(keyword in prompt_lower for keyword in creative_keywords):
        recommendations.add("Claude Opus 4")
        recommendations.add("GPT-4.1")

    # Rule 2: Summary, short, quick answer
    summary_keywords = ["summary", "summarize", "short answer", "quick answer", "tldr", "concise explanation"]
    if any(keyword in prompt_lower for keyword in summary_keywords):
        recommendations.add("Claude Sonnet 4")
        recommendations.add("GPT-4.1 Mini")
        recommendations.add("Gemini 2.5 Flash")
        recommendations.add("Grok-3 Mini")

    # Rule 3: Code, programming, script
    code_keywords = ["code", "python", "javascript", "java", "c++", "script", "program", "develop"]
    if any(keyword in prompt_lower for keyword in code_keywords):
        recommendations.add("Claude Opus 4") # Often good for complex coding
        recommendations.add("GPT-4.1")
        recommendations.add("Grok-3")

    # Rule 4: Explanation, definition (might overlap with summary, but can be more detailed)
    explanation_keywords = ["explain", "define", "what is", "describe detail", "how does"]
    if any(keyword in prompt_lower for keyword in explanation_keywords):
        recommendations.add("GPT-4.1")
        recommendations.add("Claude Opus 4") # Good for detailed explanations
        recommendations.add("Claude Sonnet 4")


    # Incorporate questionnaire answers if they provide strong signals
    # For example, if user specified a desired output format that one model handles better.
    # This is a placeholder for more advanced logic.
    for qa in questionnaire_answers:
        if "format" in qa.question.lower() and "json" in qa.answer.lower():
            # If JSON output specifically requested, some models are better.
            recommendations.add("GPT-4.1") # Often reliable for structured output
            recommendations.add("Claude Opus 4")
        if "tone" in qa.question.lower() and "formal" in qa.answer.lower():
            recommendations.add("Claude Opus 4")


    # Default/fallback models if no specific recommendations were triggered
    if not recommendations:
        recommendations.add("GPT-4.1 Mini")
        recommendations.add("Claude Sonnet 4")
        # Add a general purpose one too
        recommendations.add("GPT-4.1")

    return list(recommendations)


# Example usage:
# if __name__ == "__main__":
#     class QARead(schemas.SQLModel): # Mock for testing
#         question: str
#         answer: str
#
#     prompt1 = "Tell me a creative story about a dragon."
#     ans1: List[QARead] = []
#     print(f"Recommendations for '{prompt1}': {recommend_models(prompt1, ans1)}")
#
#     prompt2 = "Summarize this article about quantum physics quickly."
#     ans2: List[QARead] = []
#     print(f"Recommendations for '{prompt2}': {recommend_models(prompt2, ans2)}")
#
#     prompt3 = "Write a python script to parse a CSV file."
#     ans3: List[QARead] = [QARead(question="Any specific python version?", answer="Python 3.9")]
#     print(f"Recommendations for '{prompt3}': {recommend_models(prompt3, ans3)}")
#
#     prompt4 = "What are the implications of AI on society?"
#     ans4: List[QARead] = []
#     print(f"Recommendations for '{prompt4}': {recommend_models(prompt4, ans4)}")
