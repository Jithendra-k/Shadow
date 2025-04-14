def greet_agent(level):
    greetings = {
        "1": "Salute, Shadow Cadet.",
        "2": "Bonjour, Sentinel.",
        "3": "Eyes open, Phantom.",
        "4": "In the wind, Commander.",
        "5": "The unseen hand moves, Whisper.",
    }
    return greetings.get(level, "Unknown clearance level. Report anomaly.")
