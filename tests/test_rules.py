from app.rule_engine import apply_rules

def test_basic_match():
    query_data = {"level": 1, "query": "protocol red mist"}
    assert "game-like sequence" in apply_rules(query_data).lower()

def test_insufficient_level_flag():
    query_data = {"level": 2, "query": "Facility X-17"}
    response = apply_rules(query_data)
    assert "[SECURITY FLAG]" in response

def test_denied_query():
    query_data = {"level": 1, "query": "project eclipse"}
    response = apply_rules(query_data)
    assert "access denied" in response.lower()

def test_case_insensitive_trigger():
    query_data = {"level": 1, "query": "Disguise Strategies"}
    assert "layered concealment" in apply_rules(query_data).lower()
