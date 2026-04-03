#data: recieves a formatted prompt from the queryService.
# outputs a SQL SELECT statement that will represent what the user asked for

#controls: call the claude API using the inputted prompt, and collects the output
import anthropic
from schemaManager.schemaManager import schemaManager

class LLM_adapter():
    def __init__(self):
        self.client = anthropic.Anthropic()

    def create_prompt(self, schema: str, question: str) -> str:
        prompt = f"""You are an AI assistant tasked with converting natural language
        requests into SQL code. 
        The database schema contains the following tables and columns {schema}
        An example of an input you will recieve would be a
        question such as 'which players have over 5 goals?' and the SQL you produce
        for this question will be 'SELECT player FROM players WHERE goals > 5'. 
        1. Generate a SQL query that accurately answers the user's question. 
        2. Ensure the SQL is compatible with SQLite syntax. 
        3. Provide a short comment explaining what the query does. 
        Output Format: - SQL Query - Explanation
        Guidelines:
        > only generate SQL for read only queries, no writes should be allowed
        User Query: {question}
        """
        return prompt


    def natural_language_to_sql(self, prompt: str) -> str:
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text