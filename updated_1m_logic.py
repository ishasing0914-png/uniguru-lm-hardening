# UniGuru LM Safety + Deterministic Layer

# -------- Ambiguity Detection --------
def detect_ambiguity(user_input):
    text = user_input.lower().strip()

    if len(text.split()) <= 2:
        return True

    vague_words = ["explain", "help", "tell", "this", "that"]

    return any(word == text for word in vague_words)


# -------- Emotional Detection --------
def detect_emotional_distress(user_input):
    text = user_input.lower()

    emotional_markers = [
        "i feel useless",
        "i feel sad",
        "i am stressed",
        "i feel depressed",
        "i want to give up",
        "i feel hopeless",
        "i am a failure",
        "i feel low"
    ]

    return any(marker in text for marker in emotional_markers)


# -------- Unsafe Request Detection --------
def detect_unsafe_request(user_input):
    text = user_input.lower()

    unsafe_keywords = [
        "cheat",
        "hack",
        "exam leak",
        "paper leak",
        "fake certificate",
        "bypass exam",
        "steal",
        "copy in exam"
    ]

    return any(word in text for word in unsafe_keywords)


# -------- Deterministic Fallback --------
def deterministic_fallback():
    return (
        "I’m not able to answer that properly right now. "
        "Please rephrase your question."
    )


# -------- MAIN FUNCTION --------
def generate_safe_response(user_input, lm_generate_fn):

    # Priority 1: Unsafe
    if detect_unsafe_request(user_input):
        return "I can’t help with that request because it violates learning ethics."

    # Priority 2: Emotional
    if detect_emotional_distress(user_input):
        return (
            "I’m sorry you're feeling this way. "
            "Let’s take it one step at a time. You’re not alone."
        )

    # Priority 3: Ambiguous
    if detect_ambiguity(user_input):
        return "Could you clarify your question so I can help properly?"

    # Normal LM call
    try:
        response = lm_generate_fn(user_input)
        response = response.strip()

        if len(response) < 5:
            return deterministic_fallback()

        return response

    except Exception:
        return deterministic_fallback()
