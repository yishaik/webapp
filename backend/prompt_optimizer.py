from typing import List
import schemas

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
        # Example: If question was about tone/style
        elif "tone" in qa.question.lower() or "style" in qa.question.lower() and qa.answer:
            optimized_prompt += f"\nUse a {qa.answer} tone/style."
        # Generic: add other answers as context if not directly actionable as a specific instruction
        elif qa.answer and qa.answer.lower() not in ["none", "n/a", "not sure"]:
             optimized_prompt += f"\nConsider also: {qa.question} - {qa.answer}."

    # Apply generic optimization strategies
    # Strategy 1: Role-playing (simple version)
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

    # Placeholder for target_model specific optimizations
    if "gpt-4" in target_model.lower():
        optimized_prompt += "\nLeverage advanced reasoning capabilities."
    elif "claude" in target_model.lower():
        optimized_prompt += "\nBe thorough and analytical in your response."

    return optimized_prompt.strip()


# Compatibility function for backward compatibility with master branch signature
def optimize_prompt_legacy(initial_prompt: str, questionnaire_answers: List[str], target_model: str) -> str:
    """Legacy function signature for backward compatibility"""
    # Convert string answers to QuestionnaireResponseRead objects
    qa_objects = []
    for i, answer in enumerate(questionnaire_answers):
        qa_objects.append(schemas.QuestionnaireResponseRead(
            id=i,
            prompt_id=0,
            question=f"Question {i+1}",
            answer=answer
        ))
    return optimize_prompt(initial_prompt, qa_objects, target_model)
