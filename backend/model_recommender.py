from typing import List
import schemas

def recommend_models(
    base_prompt: str,
    questionnaire_answers: List[schemas.QuestionnaireResponseCreate] # Changed type here
) -> List[str]:
    """
    Recommends models based on keywords in the base prompt.
    Questionnaire answers are available for more complex future logic.
    """
    recommendations = set()
    prompt_lower = base_prompt.lower()
    
    # Combine questionnaire answers into text for analysis
    # Ensure questionnaire_answers is not None before iterating
    answers_text = ""
    if questionnaire_answers:
        answers_text = " ".join([qa.answer.lower() for qa in questionnaire_answers if qa.answer])

    # Rule 1: Creative writing
    creative_keywords = ["creative writing", "story", "poem", "write a novel", "screenplay", "creative", "narrative"]
    if any(keyword in prompt_lower for keyword in creative_keywords) or any(keyword in answers_text for keyword in creative_keywords):
        recommendations.add("Claude Opus 4")
        recommendations.add("GPT-4.1")

    # Rule 2: Summary, short, quick answer
    summary_keywords = ["summary", "summarize", "short answer", "quick answer", "tldr", "concise explanation", "brief"]
    if any(keyword in prompt_lower for keyword in summary_keywords) or any(keyword in answers_text for keyword in summary_keywords):
        recommendations.add("Claude Sonnet 4")
        recommendations.add("GPT-4.1 Mini")
        recommendations.add("Gemini 2.5 Flash")
        recommendations.add("Grok-3 Mini")

    # Rule 3: Code, programming, script
    code_keywords = ["code", "python", "javascript", "java", "c++", "script", "program", "develop", "algorithm", "function"]
    if any(keyword in prompt_lower for keyword in code_keywords) or any(keyword in answers_text for keyword in code_keywords):
        recommendations.add("Claude Opus 4")
        recommendations.add("GPT-4.1")
        recommendations.add("Grok-3")

    # Rule 4: Explanation, definition
    explanation_keywords = ["explain", "define", "what is", "describe", "how does", "how to"]
    if any(keyword in prompt_lower for keyword in explanation_keywords):
        recommendations.add("GPT-4.1")
        recommendations.add("Claude Opus 4")
        recommendations.add("Claude Sonnet 4")

    # Incorporate questionnaire answers for more specific recommendations
    for qa in questionnaire_answers:
        if "format" in qa.question.lower() and qa.answer and "json" in qa.answer.lower():
            recommendations.add("GPT-4.1")
            recommendations.add("Claude Opus 4")
        elif "tone" in qa.question.lower() and qa.answer and "formal" in qa.answer.lower():
            recommendations.add("Claude Opus 4")
        elif "audience" in qa.question.lower() and qa.answer and "beginner" in qa.answer.lower():
            recommendations.add("Claude Sonnet 4")
            recommendations.add("GPT-4.1 Mini")
        elif "length" in qa.question.lower() and qa.answer and any(word in qa.answer.lower() for word in ["detailed", "comprehensive", "long"]):
            recommendations.add("Claude Opus 4")
            recommendations.add("GPT-4.1")

    # Default/fallback models if no specific recommendations were triggered
    if not recommendations:
        recommendations.add("GPT-4.1 Mini")
        recommendations.add("Claude Sonnet 4")
        recommendations.add("Gemini 2.5 Pro")

    # Convert to list and limit to reasonable number
    final_recommendations = list(recommendations)
    
    # Prioritize based on general effectiveness
    priority_order = ["Claude Opus 4", "GPT-4.1", "Claude Sonnet 4", "Grok-3", "GPT-4.1 Mini", 
                     "Gemini 2.5 Pro", "Gemini 2.5 Flash", "Grok-3 Mini"]
    
    final_recommendations.sort(key=lambda x: priority_order.index(x) if x in priority_order else 99)
    
    # Return top 3-4 recommendations
    return final_recommendations[:4]


# Compatibility function for backward compatibility with master branch signature
def recommend_models_legacy(initial_prompt: str, questionnaire_answers: List[str]) -> List[str]:
    """Legacy function signature for backward compatibility"""
    # Convert string answers to QuestionnaireResponseRead objects
    qa_objects = []
    for i, answer in enumerate(questionnaire_answers): # This function might need adjustment or removal if not used
        # This conversion is problematic as QuestionnaireResponseCreate doesn't have id/prompt_id
        # For now, assuming this legacy function will be updated or removed separately
        # as the main recommend_models function is now aligned with QuestionnaireResponseCreate
        qa_objects.append(schemas.QuestionnaireResponseCreate(
            question=f"Question {i+1}", # Simplified
            answer=answer
        ))
    # The recursive call here is to the updated recommend_models, which now expects List[QuestionnaireResponseCreate]
    return recommend_models(initial_prompt, qa_objects)
