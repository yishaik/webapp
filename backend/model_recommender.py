# A predefined list of available models.
# This could eventually come from a config file or an API call.
AVAILABLE_MODELS = {
    "opus": "Claude 3 Opus",
    "sonnet": "Claude 3 Sonnet",
    "haiku": "Claude 3 Haiku",
    "gpt-4": "OpenAI GPT-4 Turbo",
    "gpt-3.5": "OpenAI GPT-3.5 Turbo",
    "gemini-pro": "Google Gemini Pro",
    "gemini-flash": "Google Gemini Flash",
    "grok-1": "xAI Grok-1",
}

# Simple keyword extraction (can be shared or improved)
def extract_keywords_for_recommender(text: str, num_keywords: int = 5) -> list[str]:
    words = [word.lower().strip(",.?!") for word in text.split() if len(word) > 3]
    if not words:
        return []
    # More sophisticated keyword extraction would be beneficial here
    # Sort by length (desc) then alphabetically (asc) for deterministic output
    return sorted(list(set(words)), key=lambda w: (-len(w), w))[:num_keywords]

def recommend_models(initial_prompt: str, questionnaire_answers: list[str]) -> list[str]:
    """
    Recommends 1-2 suitable models based on simple rule-based logic
    applied to the initial prompt and questionnaire answers.
    Returns a list of model identifiers (keys from AVAILABLE_MODELS).
    """
    recommendations = set()
    text_corpus = initial_prompt.lower() + " " + " ".join(q.lower() for q in questionnaire_answers)
    keywords = extract_keywords_for_recommender(text_corpus, num_keywords=7) # Increased to 7

    # Rule 1: Creative Writing / Complex Tasks
    if any(kw in keywords for kw in ["creative", "story", "poem", "novel", "complex", "research", "strategy"]):
        recommendations.add("opus") # Claude 3 Opus
        recommendations.add("gpt-4")  # GPT-4 Turbo

    # Rule 2: Coding / Technical Prompts
    if any(kw in keywords for kw in ["code", "script", "python", "javascript", "java", "debug", "algorithm", "technical"]):
        recommendations.add("opus") # Opus is good for coding
        recommendations.add("grok-1") # Grok for coding
        recommendations.add("gpt-4")

    # Rule 3: Quick Summary / Short Tasks / Fast Response
    if any(kw in keywords for kw in ["summary", "summarize", "quick", "fast", "short", "translate", "classification"]):
        recommendations.add("haiku") # Claude 3 Haiku
        recommendations.add("gemini-flash") # Gemini Flash
        recommendations.add("gpt-3.5")

    # Rule 4: General Purpose / Balanced
    if not recommendations or len(recommendations) < 2 : # If no specific rules hit, or need more
        recommendations.add("sonnet") # Claude 3 Sonnet (balanced)
        recommendations.add("gemini-pro") # Gemini Pro (balanced)

    # Rule 5: If prompt mentions specific model types or providers
    if "claude" in text_corpus:
        recommendations.add("opus")
        recommendations.add("sonnet")
    if "gpt" in text_corpus or "openai" in text_corpus:
        recommendations.add("gpt-4")
        recommendations.add("gpt-3.5")
    if "gemini" in text_corpus or "google" in text_corpus:
        recommendations.add("gemini-pro")
        recommendations.add("gemini-flash")
    if "grok" in text_corpus or "xai" in text_corpus:
        recommendations.add("grok-1")

    # Ensure we don't recommend too many, prioritize based on rule strength or a default.
    # For now, if many are added, just take a slice. Max 2-3 suggestions.

    final_recommendations = list(recommendations)

    # Prioritize models if many are selected. This is a very basic prioritization.
    priority_order = ["opus", "gpt-4", "grok-1", "sonnet", "gemini-pro", "haiku", "gemini-flash", "gpt-3.5"]

    # Sort current recommendations by this priority
    final_recommendations.sort(key=lambda x: priority_order.index(x) if x in priority_order else 99)

    # If a specific model family was mentioned in the prompt, prioritize/filter for it
    mentioned_family = None
    if "claude" in text_corpus: mentioned_family = "claude"
    elif "gpt" in text_corpus or "openai" in text_corpus: mentioned_family = "gpt"
    elif "gemini" in text_corpus or "google" in text_corpus: mentioned_family = "gemini"
    elif "grok" in text_corpus or "xai" in text_corpus: mentioned_family = "grok"

    if mentioned_family:
        filtered_by_family = []
        for model_key in final_recommendations:
            # This is a simplification; actual family matching would be more robust
            if mentioned_family == "gpt" and ("gpt-4" == model_key or "gpt-3.5" == model_key):
                filtered_by_family.append(model_key)
            elif mentioned_family == "claude" and ("opus" == model_key or "sonnet" == model_key or "haiku" == model_key):
                filtered_by_family.append(model_key)
            elif mentioned_family == "gemini" and ("gemini-pro" == model_key or "gemini-flash" == model_key):
                filtered_by_family.append(model_key)
            elif mentioned_family == "grok" and ("grok-1" == model_key):
                filtered_by_family.append(model_key)

        if filtered_by_family: # If we have models from the mentioned family
            final_recommendations = filtered_by_family

    # Return top 1-2, or up to 3 if diverse categories were hit.
    # The slicing logic from before:
    if len(final_recommendations) > 2 and not any(kw in keywords for kw in ["creative", "code", "technical"]): # if not very specific, limit more
        return final_recommendations[:2]

    return final_recommendations[:3] # Max 3 recommendations


# Example Usage (for testing)
if __name__ == '__main__':
    prompt1 = "Write a short story about a dragon."
    answers1 = ["fantasy genre", "about 500 words", "for young adults"]
    print(f"Prompt: {prompt1}\nAnswers: {answers1}\nRecommended: {recommend_models(prompt1, answers1)}\n")

    prompt2 = "Generate a python script to parse a CSV file."
    answers2 = ["the csv has 3 columns", "output should be json", "handle potential errors"]
    print(f"Prompt: {prompt2}\nAnswers: {answers2}\nRecommended: {recommend_models(prompt2, answers2)}\n")

    prompt3 = "Summarize this article about climate change quickly."
    answers3 = ["main points only", "for a general audience", "very short summary"]
    print(f"Prompt: {prompt3}\nAnswers: {answers3}\nRecommended: {recommend_models(prompt3, answers3)}\n")

    prompt4 = "What's the capital of France?"
    answers4 = []
    print(f"Prompt: {prompt4}\nAnswers: {answers4}\nRecommended: {recommend_models(prompt4, answers4)}\n")

    prompt5 = "I need a creative tagline for my new coffee shop. It's called 'The Daily Grind' and it's very modern."
    answers5 = ["target audience is young professionals", "tagline should be catchy"]
    print(f"Prompt: {prompt5}\nAnswers: {answers5}\nRecommended: {recommend_models(prompt5, answers5)}\n")
