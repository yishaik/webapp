import random

def generate_questions(prompt: str) -> list[str]:
    """
    Generates 3-5 simple, context-aware questions based on the input prompt.
    """
    questions = [
        "What is the desired length of the output?",
        "What is the target audience for this content?",
        "Are there any specific keywords or phrases that must be included?",
        "What is the overall tone or style you're aiming for (e.g., formal, informal, humorous)?",
    ]

    prompt_lower = prompt.lower()

    if "code" in prompt_lower or "script" in prompt_lower or "program" in prompt_lower:
        questions.append("Which programming language are you referring to (e.g., Python, JavaScript)?")
    if "email" in prompt_lower:
        questions.append("What is the purpose of this email (e.g., inquiry, marketing, follow-up)?")
        questions.append("Who is the recipient of this email?")
    if "story" in prompt_lower or "narrative" in prompt_lower:
        questions.append("What is the main genre of the story (e.g., fantasy, sci-fi, romance)?")
        questions.append("Are there any specific characters or settings to focus on?")
    if "marketing" in prompt_lower or "advertisement" in prompt_lower:
        questions.append("What is the product or service being marketed?")
        questions.append("What is the key message you want to convey?")
    if "blog" in prompt_lower or "article" in prompt_lower:
        questions.append("What is the main topic or title of the blog post/article?")
        questions.append("Is there a specific call to action you want to include?")

    # Select 3 to 5 questions randomly, ensuring a mix of general and context-specific ones.
    # Prioritize context-specific questions if available.

    context_specific_questions = []
    general_questions = [
        "What is the desired length of the output?",
        "What is the target audience for this content?",
        "Are there any specific keywords or phrases that must be included?",
        "What is the overall tone or style you're aiming for (e.g., formal, informal, humorous)?",
    ]

    if "code" in prompt_lower or "script" in prompt_lower or "program" in prompt_lower:
        context_specific_questions.append("Which programming language are you referring to (e.g., Python, JavaScript)?")
    if "email" in prompt_lower:
        context_specific_questions.append("What is the purpose of this email (e.g., inquiry, marketing, follow-up)?")
        context_specific_questions.append("Who is the recipient of this email?")
    if "story" in prompt_lower or "narrative" in prompt_lower:
        context_specific_questions.append("What is the main genre of the story (e.g., fantasy, sci-fi, romance)?")
        context_specific_questions.append("Are there any specific characters or settings to focus on?")
    if "marketing" in prompt_lower or "advertisement" in prompt_lower:
        context_specific_questions.append("What is the product or service being marketed?")
        context_specific_questions.append("What is the key message you want to convey?")
    if "blog" in prompt_lower or "article" in prompt_lower:
        context_specific_questions.append("What is the main topic or title of the blog post/article?")
        context_specific_questions.append("Is there a specific call to action you want to include?")

    # If prompt is short, add specific questions for that condition.
    # These will be added to the pool of context_specific_questions.
    if len(prompt_lower.split()) < 10:
        if not prompt.strip(): # Empty prompt
            context_specific_questions.append("Could you provide more details about the desired output?") # Prioritize this
        else: # Short but not empty
            context_specific_questions.append("Could you provide more details about the desired output?")
        context_specific_questions.append("What is the primary goal you want to achieve with this prompt?")

    # Deduplicate all collected context_specific_questions, preserving some order if possible (set loses it)
    # A simple way for now:
    unique_context_qs = []
    for q in context_specific_questions:
        if q not in unique_context_qs:
            unique_context_qs.append(q)
    context_specific_questions = unique_context_qs

    # For empty prompts, ensure "Could you provide more details..." is first if present
    if not prompt.strip() and "Could you provide more details about the desired output?" in context_specific_questions:
        context_specific_questions.pop(context_specific_questions.index("Could you provide more details about the desired output?"))
        context_specific_questions.insert(0, "Could you provide more details about the desired output?")

    final_questions = []
    random_target_count = random.randint(3, 5) # Determine total questions needed first

    # Add up to 3 context-specific questions if available (increased from 2)
    num_context_to_take = min(len(context_specific_questions), 3)

    # Prioritize key thematic questions if their themes were triggered
    prioritized_context_qs = []
    if "story" in prompt_lower:
        q_genre = "What is the main genre of the story (e.g., fantasy, sci-fi, romance)?"
        if q_genre in context_specific_questions:
            prioritized_context_qs.append(q_genre)
    if "blog" in prompt_lower:
        q_topic = "What is the main topic or title of the blog post/article?"
        if q_topic in context_specific_questions:
            # Add only if not already added (e.g. if story and blog are same, avoid similar q twice from priority)
            if q_topic not in prioritized_context_qs:
                prioritized_context_qs.append(q_topic)

    # Take up to 2 prioritized questions (e.g. one for story, one for blog if both themes hit)
    final_chosen_context_qs = prioritized_context_qs[:2]

    # Create a list of remaining context questions (not prioritized, and not already selected)
    remaining_context_pool = [q for q in context_specific_questions if q not in final_chosen_context_qs]
    random.shuffle(remaining_context_pool)

    # Fill the rest of num_context_to_take slots from the remaining pool
    num_slots_left_for_context = num_context_to_take - len(final_chosen_context_qs)
    if num_slots_left_for_context > 0:
        final_chosen_context_qs.extend(remaining_context_pool[:num_slots_left_for_context])

    final_questions.extend(final_chosen_context_qs)

    # Add remaining general questions to make up random_target_count
    remaining_slots = max(0, random_target_count - len(final_questions))
    random.shuffle(general_questions)
    final_questions.extend(general_questions[:remaining_slots])

    # Ensure we have at least 3 questions, even if no context-specific ones were added and general were few.
    while len(final_questions) < 3 and general_questions:
        q = general_questions.pop(0)
        if q not in final_questions: # ensure no duplicates if initial pool was small
             final_questions.append(q)

    # Fallback if somehow still not enough questions (shouldn't happen with current logic)
    if not final_questions:
        final_questions = [
            "What is the desired length of the output?",
            "What is the target audience for this content?",
            "Are there any specific keywords or phrases that must be included?",
        ]

    return list(set(final_questions))[:5] # Ensure unique questions and max 5
