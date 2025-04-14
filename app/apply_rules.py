import json
from pathlib import Path
from app.security_flags import check_security_flags

RULE_PATH = Path(__file__).parent / "knowledge_base/classified_rules.json"

def apply_rules(query_data):
    rules = json.loads(RULE_PATH.read_text())
    level = query_data["level"]
    q = query_data["query"]

    # Check for security flags first
    flag_warning = check_security_flags(level, q)

    for rule in rules:
        if rule["level"] <= level:
            if rule["trigger"] in q:
                return f"{flag_warning}\\n{rule['response']}" if flag_warning else rule["response"]
            if q.strip() == rule["trigger"]:
                return f"{flag_warning}\\n{rule['response']}" if flag_warning else rule["response"]

    return f"{flag_warning}\\nAccess denied. Query unrecognized or beyond clearance." if flag_warning else "Access denied. Query unrecognized or beyond clearance."