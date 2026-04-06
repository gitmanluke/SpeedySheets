#data: the CLI interface will send any queries to this module
# example "show me the average price of keyboards in 2026"

#controls: The service will convert this query to a valid prompt
# the prompt will be specifically designed for the LLM to create a SQL representation
# of the query
# the service will send this prompt to the LLM interface

#status: invalid row, invalid column, unable to update data ?

import sqlite3
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
            if answer == "generation unavailable":
                return None
            return answer
        else:
            print("invalid query")
            return None

    def send_to_LLM(self, schemaManager, question) -> str:
        prompt = self._llm.create_prompt(self.schemaManager.schema, question)
        response = self._llm.natural_language_to_sql(prompt)
        print(response)
        if (self.database_validator.valid_query(response)):
            self.cursor.execute(response)
            answer = str(self.cursor.fetchall())
            print(answer)
            return answer
        else:
            print("invalid query")
            return None
            # todo: spin back to the LLM again, and get a new prompt maybe it will be good

