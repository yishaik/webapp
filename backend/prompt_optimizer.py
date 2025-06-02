from typing import List, Optional
import schemas # Assuming schemas.py contains QuestionnaireResponseCreate

def optimize_prompt(
    base_prompt: str,
    questionnaire_answers: Optional[List[schemas.QuestionnaireResponseCreate]],
    target_model: Optional[str] = None
) -> str:
    """
    Optimizes a base prompt using questionnaire answers and generic strategies.
    """
    optimized_prompt_parts = [base_prompt]
    role_set = False

    if questionnaire_answers:
        for qa in questionnaire_answers:
            question_lower = qa.question.lower()
            answer_lower = qa.answer.lower()

            if not qa.answer or answer_lower in ["none", "n/a", "not sure", "any"]:
                continue

            # Strategy: Role-Playing based on answers
            if ("expert" in answer_lower or "role" in answer_lower or "act as" in answer_lower) and not role_set:
                # Attempt to extract a specific domain if possible, otherwise generic expert
                # This is a simple extraction, could be improved with NLP
                domain = ""
                if "expert in" in answer_lower:
                    try:
                        domain = answer_lower.split("expert in")[1].split(".")[0].split(",")[0].strip()
                    except IndexError:
                        domain = "the relevant field"
                elif "role of" in answer_lower:
                    try:
                        domain = answer_lower.split("role of")[1].split(".")[0].split(",")[0].strip()
                    except IndexError:
                        domain = "the specified role"

                if domain:
                    optimized_prompt_parts.insert(0, f"You are an expert in {domain}.")
                else:
                    optimized_prompt_parts.insert(0, "You are an expert in the relevant domain.")
                role_set = True

            # Strategy: Output Format based on answers
            elif "format" in question_lower:
                if "json" in answer_lower:
                    optimized_prompt_parts.append("Please provide the output in JSON format.")
                elif "markdown" in answer_lower:
                    optimized_prompt_parts.append("Please provide the output in Markdown format.")
                elif "xml" in answer_lower:
                    optimized_prompt_parts.append("Please provide the output in XML format.")
                elif "list" in answer_lower:
                    optimized_prompt_parts.append("Please provide the output as a list.")

            # Other general context additions from questionnaire
            elif "length" in question_lower:
                optimized_prompt_parts.append(f"Ensure the response has a length of approximately: {qa.answer}.")
            elif "audience" in question_lower:
                optimized_prompt_parts.append(f"The target audience is: {qa.answer}.")
            elif "programming language" in question_lower and qa.answer.lower() not in ["any", "none", "n/a", "not specific"]:
                 optimized_prompt_parts.append(f"The preferred programming language is {qa.answer}.")
            elif "tone" in question_lower or "style" in question_lower:
                optimized_prompt_parts.append(f"Use a {qa.answer} tone/style.")
            # Generic catch-all for other answers
            else:
                 optimized_prompt_parts.append(f"Consider also: {qa.question} - {qa.answer}.")

    # Default Role-Playing if not set by answers
    if not role_set and "act as" not in base_prompt.lower():
        optimized_prompt_parts.append("Act as an expert in the relevant domain.")

    # Step-by-Step for complexity (simple check)
    if ("plan" in base_prompt.lower() or "steps" in base_prompt.lower() or "complex" in base_prompt.lower()) \
       and "step by step" not in base_prompt.lower() and "step-by-step" not in base_prompt.lower():
        optimized_prompt_parts.append("Think step by step.")

    # Generic clarity/conciseness if not already present
    if "clear and concise" not in base_prompt.lower():
        optimized_prompt_parts.append("Ensure your response is clear, concise, and directly addresses the query.")

    # Target model specific optimizations (placeholder)
    if target_model:
        if "gpt-4" in target_model.lower():
            optimized_prompt_parts.append("Leverage advanced reasoning capabilities for GPT-4.")
        elif "claude" in target_model.lower():
            optimized_prompt_parts.append("Be thorough and analytical in your response, as expected for Claude models.")
        elif "gemini" in target_model.lower():
            optimized_prompt_parts.append("Utilize Gemini's multimodal understanding if applicable.")
        elif "grok" in target_model.lower():
            optimized_prompt_parts.append("Provide a unique and insightful perspective characteristic of Grok.")


    # Join parts with newline, but ensure base_prompt is first if role was prepended
    if optimized_prompt_parts[0].startswith("You are an expert"):
        role_prepend = optimized_prompt_parts.pop(0)
        final_prompt = role_prepend + "\n" + "\n".join(p for p in optimized_prompt_parts if p.strip())
    else:
        final_prompt = "\n".join(p for p in optimized_prompt_parts if p.strip())

    return final_prompt.strip()


# Legacy function compatibility (might need removal or update if QuestionnaireResponseRead is very different)
# For now, this will likely fail if QuestionnaireResponseCreate is not directly usable in place of QuestionnaireResponseRead
# by the old logic that was here, or if the old function was expecting specific fields from Read.
# The new optimize_prompt function is designed to work with QuestionnaireResponseCreate.
def optimize_prompt_legacy(initial_prompt: str, questionnaire_answers: List[str], target_model: str) -> str:
    """Legacy function signature. Converts basic string answers to schema for the main optimizer."""
    qa_objects: List[schemas.QuestionnaireResponseCreate] = []
    for i, answer_text in enumerate(questionnaire_answers):
        qa_objects.append(schemas.QuestionnaireResponseCreate(
            question=f"Legacy Question {i+1}", # Placeholder question
            answer=answer_text
        ))
    return optimize_prompt(initial_prompt, qa_objects, target_model)
