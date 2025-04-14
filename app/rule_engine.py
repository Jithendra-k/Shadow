import json
from pathlib import Path

RULE_PATH = Path(__file__).parent / "knowledge_base/classified_rules.json"

def apply_rules(query_data):
    rules = json.loads(RULE_PATH.read_text())
    level = query_data["level"]
    q = query_data["query"]

    for rule in rules:
        if rule["level"] == level and rule["trigger"] in q:
            return rule["response"]
    return "Access denied. Query unrecognized or beyond clearance."
