#data: the CLI interface will send any queries to this module
# example "show me the average price of keyboards in 2026"

#controls: The service will convert this query to a valid prompt
# the prompt will be specifically designed for the LLM to create a SQL representation
# of the query
# the service will send this prompt to the LLM interface

#status: invalid row, invalid column, unable to update data ?
