from app.agent_levels import greet_agent
from app.query_parser import extract_info
from app.rule_engine import apply_rules
from app.response_generator import generate_response
from rich import print

def main():
    print("[bold cyan]Welcome to the RAW Simulation Interface[/bold cyan]")
    agent_level = input("Enter agent level (1-5): ").strip()
    query = input("Enter classified query: ").strip()

    greeting = greet_agent(agent_level)
    print(greeting)

    query_data = extract_info(agent_level, query)
    rule_output = apply_rules(query_data)
    response = generate_response(query_data, rule_output)

    print(f"\n[bold green]RESPONSE:[/bold green] {response}")

if __name__ == "__main__":
    main()
