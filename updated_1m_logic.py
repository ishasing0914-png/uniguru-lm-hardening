# updated_lm_logic.py
# Purpose: Deterministic safety + robustness layer for UniGuru LM

def detect_ambiguity(user_input):
    ambiguous_phrases = [
        "explain this",
        "tell me everything",
        "do it",
        "help me",
        "what about this"
    ]
    return user_input.lower().strip() in ambiguous_phrases


def detect_emotional_distress(user_input):
    emotional_markers = [
        "i feel useless",
        "i am lost",
        "i want to quit",
        "i can't do this",
        "i feel hopeless"
    ]
    return any(marker in user_input.lower() for marker in emotional_markers)


def detect_unsafe_request(user_input):
    unsafe_keywords = [
        "cheat",
        "hack",
        "illegal",
        "bypass",
        "fake certificate"
    ]
    return any(word in user_input.lower() for word in unsafe_keywords)


def deterministic_fallback(reason):
    return f"[SAFE_FALLBACK] Unable to proceed due to: {reason}"


def generate_safe_response(user_input, lm_generate_fn):
    """
    Central LM entry point.
    This MUST be used instead of calling the LM directly.
    """

    # 1️⃣ Ambiguity handling
    if detect_ambiguity(user_input):
        return "Could you please clarify your question so I can help you better?"

    # 2️⃣ Emotional safety handling
    if detect_emotional_distress(user_input):
        return (
            "I’m really sorry you’re feeling this way. "
            "You’re not alone, and it’s okay to pause. "
            "If you’d like, we can take this one small step at a time."
        )

    # 3️⃣ Unsafe request handling
    if detect_unsafe_request(user_input):
        return (
            "I can’t help with that request because it goes against "
            "learning and ethical guidelines."
        )

    # 4️⃣ Normal LM execution
    try:
        response = lm_generate_fn(user_input)

        # 5️⃣ Silent failure protection
        if response is None or len(response.strip()) < 5:
            return deterministic_fallback("Low-quality or empty response")

        return response

    except Exception as e:
        return deterministic_fallback(str(e))
