from schemaManager.schemaManager import schemaManager
import pandas as pd

def test_add_table():
    ''' this unit test will add a fake table to the db and verify it has been added '''
    people_df = pd.DataFrame({
    "first_name": ["Alice", "Bob"],
    "last_name": ["Johnson", "Smith"],
    "age": [20, 22]
    })
    soccer_df = pd.DataFrame({
    "player": ["messi", "ronaldo"],
    "age": ["38", "41"],
    "goals": [900, 965]
    })
    fake_df = 1
    test_manager = schemaManager()
    # add 2 tables that have pandas df
    test_manager.add_table(people_df,"people")
    test_manager.add_table(soccer_df,"players")
    # add table that doesnt have data
    test_manager.add_table(fake_df,"DOES NOT EXIST")
    test_manager.view_tables()
