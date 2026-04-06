from queryService.handleQuery import handleQuery
from schemaManager.schemaManager import schemaManager

data_path = "data/database.db"
schemaManager = schemaManager(data_path)

def test_sql_execution():
    query_handler = handleQuery(schemaManager)
    ''' testing passing in an invalid column name '''
    SQL = "Select * FROM first_name"
    output = query_handler.execute_SQL(SQL)
    assert output == None
    ''' testing a vali query '''
    SQL = "Select * FROM people WHERE first_name = 'Bob' "
    output = query_handler.execute_SQL(SQL)
    assert output != None
    