def extract_info(agent_level, query):
    return {
        "level": int(agent_level),
        "query": query.lower().strip(),
    }
