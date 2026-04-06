#data: the CLI interface will send any queries to this module
# example "show me the average price of keyboards in 2026"

#controls: The service will convert this query to a valid prompt
# the prompt will be specifically designed for the LLM to create a SQL representation
# of the query
# the service will send this prompt to the LLM interface

#status: invalid row, invalid column, unable to update data ?

import sqlite3
import re
from queryService.DBvalidator import DBvalidator
from schemaManager.schemaManager import schemaManager
from LLMInterface.nl_to_sql import LLM_adapter

class handleQuery():
    def __init__(self, schemaManager):
        self.database_path = schemaManager.database_path
        self.database_validator = DBvalidator(self.database_path)
        self.schemaManager = schemaManager
        self._llm = LLM_adapter()
        try:
            with sqlite3.connect(self.database_path) as self.conn: #opens connection with existing database or creates new one if not found
                print(f"Query handler connected to database at '{self.database_path}'")
                self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            print("Failed to open database:", e)


    def execute_SQL(self, user_command) -> str:
        if (self.database_validator.valid_query(user_command)):
            self.cursor.execute(user_command)
            answer = str(self.cursor.fetchall())
            return answer
        else:
            print("invalid query")
            return None

    def _extract_sql_from_response(self, response: str):
        if not isinstance(response, str):
            return None
        match = re.search(r"```sql\s*(.*?)\s*```", response, flags=re.IGNORECASE | re.DOTALL)
        if not match:
            return None
        sql_query = match.group(1).strip()
        if not sql_query:
            return None
        return sql_query

    def send_to_LLM(self, question) -> str:
        schema = self.schemaManager.get_schema()
        prompt = self._llm.create_prompt(schema, question)
        response = self._llm.natural_language_to_sql(prompt)
        if response == "generation unavailable":
            return None
        sql_query = self._extract_sql_from_response(response)
        if not sql_query:
            print("invalid query")
            return None
        print(sql_query)
        answer = self.execute_SQL(sql_query)
        return answer

