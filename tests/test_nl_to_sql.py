from LLMInterface.nl_to_sql import LLM_adapter


def test_prompt_creation():
    adapter = LLM_adapter()
    schema = {
    "players": ["name", "age", "goals"],
    "teams":   ["id", "name", "city"],
    "matches": ["id", "home_team", "away_team", "date"]
    }
    question = "who are the top 5 players by most number of goals"
    prompt = adapter.create_prompt(schema,question)
    response = adapter.natural_language_to_sql(prompt)

    print(response)
