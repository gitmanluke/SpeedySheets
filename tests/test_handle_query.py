from queryService.handleQuery import handleQuery
from schemaManager.schemaManager import schemaManager

data_path = "data/database.db"
schemaManager = schemaManager()
schemaManager.set_database(data_path)

def test_sql_execution():
    query_handler = handleQuery(schemaManager)
    ''' testing passing in an invalid column name '''
    SQL = "SELECT * FROM first_name"
    output = query_handler.execute_SQL(SQL)
    assert output == None
    ''' testing a valid query '''
    SQL = "SELECT * FROM orders WHERE Name = 'Luke'"
    output = query_handler.execute_SQL(SQL)
    assert output != None
    