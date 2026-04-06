# data: takes in a number of .csv files
# controls: send data to schema manager
# status: valid or invalid data

import pandas
from schemaManager.schemaManager import schemaManager

# data_paths = ["/Users/luke/Desktop/school/EC530/SpeedySheets/Example Data - Well formatted.csv"]


class dataLoader():
    def __init__(self, schemaManager):
        self.schemaManager = schemaManager
        print("schema manager set")

    def send_to_manager(self, data_path, database_path, table_name):
        print(f"Sending {data_path} to manager")
        print(f"Database path: {database_path}")
        print(f"Table name: {table_name}")
        data = pandas.read_csv(data_path)
        self.schemaManager.add_table(database_path, data, table_name)
