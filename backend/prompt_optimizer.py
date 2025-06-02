from typing import List
from . import schemas # Assuming schemas.py contains QuestionnaireResponseRead

def optimize_prompt(
    base_prompt: str,
    questionnaire_answers: List[schemas.QuestionnaireResponseRead],
    target_model: str  # Placeholder for now
) -> str:
    """
    Optimizes a base prompt using questionnaire answers and generic strategies.
    """
    optimized_prompt = base_prompt

    # Incorporate insights from questionnaire answers
    # This is a simplified example; more sophisticated NLP could be used here.
    for qa in questionnaire_answers:
        # Example: If a question was about length, and answer specified it.
        if "length" in qa.question.lower() and qa.answer:
            optimized_prompt += f"\nEnsure the response has a length of approximately: {qa.answer}."
        # Example: If a question was about target audience.
        elif "audience" in qa.question.lower() and qa.answer:
            optimized_prompt += f"\nThe target audience is: {qa.answer}."
        # Example: If question was about programming language
        elif "programming language" in qa.question.lower() and qa.answer and qa.answer.lower() not in ["any", "none", "n/a", "not specific"]:
             optimized_prompt += f"\nThe preferred programming language is {qa.answer}."
        # Generic: add other answers as context if not directly actionable as a specific instruction
        elif qa.answer and qa.answer.lower() not in ["none", "n/a", "not sure"]:
             optimized_prompt += f"\nConsider also: {qa.question} - {qa.answer}."


    # Apply generic optimization strategies
    # Strategy 1: Role-playing (simple version)
    # More advanced: could try to infer domain from prompt/answers.
    # For now, a generic expert role if not otherwise specified by user.
    if "act as" not in base_prompt.lower():
        # Check if any answer already implies a role
        role_implied = any("role of" in qa.answer.lower() or "act as" in qa.answer.lower() for qa in questionnaire_answers)
        if not role_implied:
            optimized_prompt += "\nAct as an expert in the relevant domain."

    # Strategy 2: Requesting step-by-step thinking (if not already implied)
    if "step-by-step" not in base_prompt.lower() and "step by step" not in base_prompt.lower():
        optimized_prompt += "\nThink step by step to ensure a comprehensive and accurate response."

    # Strategy 3: Adding clarity/conciseness request
    if "clear and concise" not in base_prompt.lower():
        optimized_prompt += "\nEnsure your response is clear, concise, and directly addresses the query."

    # Placeholder for target_model specific optimizations - not used yet
    # if target_model == "some_specific_model":
    #    optimized_prompt += "\n[Specific instruction for some_specific_model]"

    return optimized_prompt.strip()

# Example usage:
# if __name__ == "__main__":
#     class QARead(schemas.SQLModel): # Mock for testing
#         question: str
#         answer: str
#
#     sample_base_prompt = "Explain photosynthesis."
#     sample_answers = [
#         QARead(question="What is the target audience for this explanation (e.g., beginner, intermediate, expert)?", answer="beginner"),
#         QARead(question="Are there any specific constraints or requirements for the output (e.g., tone, style, format)?", answer="casual tone")
#     ]
#     optimized = optimize_prompt(sample_base_prompt, sample_answers, "gpt-4")
#     print(optimized)
#
#     sample_base_prompt_2 = "Write Python code to sort a list of numbers."
#     sample_answers_2 = [
#        QARead(question="What programming language are you focusing on for the code generation (if any specific)?", answer="Python"),
#        QARead(question="Are there any specific libraries or frameworks to be used or avoided?", answer="No specific libraries"),
#     ]
#     optimized_2 = optimize_prompt(sample_base_prompt_2, sample_answers_2, "gpt-4")
#     print(optimized_2)
