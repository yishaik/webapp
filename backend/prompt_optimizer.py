import random

# Basic keyword extraction (very naive)
def extract_keywords(text: str, num_keywords: int = 3) -> list[str]:
    """Extracts simple keywords by splitting the text and picking common words, avoiding very short ones."""
    words = [word.lower().strip(",.?!") for word in text.split() if len(word) > 3]
    if not words:
        return []
    # This is a placeholder for a more sophisticated keyword extraction
    # For now, just return some of the longer words if available
    # Sort by length (desc) then alphabetically (asc) for deterministic output
    return sorted(list(set(words)), key=lambda w: (-len(w), w))[:num_keywords]

def get_domain_from_keywords(keywords: list[str]) -> str:
    """Attempts to guess a domain from keywords - very simplistic."""
    if not keywords:
        return "the relevant field"
    # Simple example: if 'code' or 'python' is a keyword, suggest 'software development'
    if any(k in ["code", "python", "javascript", "java", "programming"] for k in keywords):
        return "software development"
    if any(k in ["medical", "health", "doctor"] for k in keywords):
        return "medicine"
    if any(k in ["legal", "law", "contract"] for k in keywords):
        return "law"
    # Fallback to a generic domain based on the first keyword
    return f"the field of {keywords[0]}"


def optimize_prompt(initial_prompt: str, questionnaire_answers: list[str], target_model: str) -> str:
    """
    Applies generic optimization strategies to the initial_prompt.
    Uses questionnaire_answers to potentially extract keywords or understand user intent.
    target_model is not heavily used yet.
    """
    optimized_prompt = initial_prompt

    # Combine answers into a single string for keyword extraction
    answers_text = " ".join(questionnaire_answers)
    full_text_for_keywords = initial_prompt + " " + answers_text
    keywords = extract_keywords(full_text_for_keywords, num_keywords=7) # Increased to 7
    domain = get_domain_from_keywords(keywords) # Domain will be based on these 7 keywords

    strategies = []

    # Strategy 1: Act as an expert
    strategies.append(f"Act as an expert in {domain}.")

    # Strategy 2: Think step-by-step (if not already implied)
    if "step-by-step" not in optimized_prompt.lower() and "step by step" not in optimized_prompt.lower():
        strategies.append("Think step-by-step to ensure a comprehensive answer.")

    # Strategy 3: Output format (example: markdown, could be influenced by answers)
    # For example, if an answer mentions "report" or "document"
    if any(ans_kw in answers_text.lower() for ans_kw in ["report", "document", "formatted"]):
        strategies.append("Present the final output in a clear, well-structured markdown format.")
    elif any(kw in initial_prompt.lower() for kw in ["code", "script", "python", "function", "generate"]) and "markdown" not in optimized_prompt.lower():
         strategies.append("If generating code, present it in a markdown code block with the appropriate language tag.")


    # Strategy 4: Desired length (example, could be more specific based on answers)
    # This is a placeholder, as actual length control is complex.
    # We can look for keywords in answers like "short", "detailed", "summary"
    if "short" in answers_text.lower() or "brief" in answers_text.lower() or "summary" in answers_text.lower():
        strategies.append("Keep the response concise and to the point.")
    elif "detailed" in answers_text.lower() or "comprehensive" in answers_text.lower() or "in-depth" in answers_text.lower():
        strategies.append("Provide a detailed and comprehensive response.")


    # Apply a subset of strategies (e.g., 1 or 2 randomly, or based on some logic)
    # For now, let's add all applicable ones, prepended to the prompt.

    # Shuffle to make the order a bit random, but "Act as expert" usually good at start
    # random.shuffle(strategies)

    final_applied_strategies = []
    if f"Act as an expert in {domain}." in strategies:
        final_applied_strategies.append(f"Act as an expert in {domain}.")
        strategies.remove(f"Act as an expert in {domain}.")

    # Add other strategies, up to 2 more for now to avoid overly long prepended instructions
    random.shuffle(strategies)
    final_applied_strategies.extend(strategies[:2])


    if final_applied_strategies:
        prefix = " ".join(final_applied_strategies)
        optimized_prompt = f"{prefix}\n\nOriginal prompt: \"{optimized_prompt}\""

    # A very simple use of target_model (can be expanded significantly)
    if "gpt-4" in target_model.lower() and "complex" in answers_text.lower():
        optimized_prompt += "\nLeverage advanced reasoning capabilities for this complex task."
    elif "claude" in target_model.lower() and "creative" in answers_text.lower():
        optimized_prompt += "\nFeel free to be creative and explore novel approaches."

    return optimized_prompt
