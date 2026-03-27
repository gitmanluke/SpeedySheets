# data: takes in a number of .csv files
# controls: send data to schema manager
# status: valid or invalid data

import pandas

data_paths = ["/Users/luke/Desktop/school/EC530/SpeedySheets/Example Data - Well formatted.csv"]


class dataLoader():
    def __init__(self):
        self.schemaManager = schemaManager()
        self.data_paths = data_paths
        print("schema manager set")

    def send_to_manager(self, data_paths):
        for path in data_paths:
            print(path)
            data = pandas.read_csv(path)
            print(data)
            self.schemaManager.add_table(data)
