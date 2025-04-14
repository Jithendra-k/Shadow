def check_security_flags(agent_level, query):
    sensitive_phrases = {
        "facility x-17": 4,
        "omega echo": 5,
        "eclipse protocol": 5,
        "the whispering gate": 5
    }

    warnings = []
    for phrase, required_level in sensitive_phrases.items():
        if phrase in query.lower():
            if agent_level < required_level:
                warnings.append(f"[SECURITY FLAG] Unauthorized access attempt to '{phrase.upper()}' (Requires Level {required_level})")

    return "\\n".join(warnings) if warnings else ""
