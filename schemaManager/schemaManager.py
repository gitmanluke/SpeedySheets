#data: takes in well formatted (for now) data in the form of a csv file.
# output will be a .SQL file with the table data and the INSERT statement will probably be stored somewhere else.

#controls: Each of the cells in the top row becomes a SQL column, use the CREATE TABLE keyword for this operation.
# dont need to execute the creation but it can save the info in a file
#
# each of the rows will be an entry, Example: 
# INSERT INTO students (first_name, last_name, age, major)
# VALUES 
# ('Alice', 'Johnson', 20, 'Computer Science'),
# ('Bob', 'Smith', 22, 'Mathematics'),
# ('Charlie', 'Brown', 19, 'Physics');
# values can be a list of size of number of entries and we will do 
# one INSERT until the list is empty

#status: later figure this out, mostly will be for data that is not well formatted
import sqlite3
import pandas

class schemaManager():
    def __init__(self):
        self.schema = {}
        self.table_names = []
        self.database_path = None
        self.conn = None
        self.cursor = None

    def set_database(self, database_path):
        self.database_path = database_path
        print(f"PATH: {database_path}")
        try:
            self.conn = sqlite3.connect(database_path)
            self.cursor = self.conn.cursor()
            print(f"Schema Manager connected to database at '{database_path}'")
        except sqlite3.OperationalError as e:
            print("Failed to open database:", e)

    # def check(data) -> :
    #     checks if the incoming data structure matches a table currently in the db 
    #     i = 0
    #     for name in self.table_names:
    #         view_table = "PRAGMA table_info(" + name + ")"
    #         table = self.cursor.execute(view_table).fetchall()
    #         if table[i+1][1] == data.columns[i]
    #             i += 1
    #             continue

    # def append_table(self,data):

    def add_table(self, data_path, data, name):
        try:
            self.conn = sqlite3.connect(data_path)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            print("Failed to open database when adding table:", e)
        # takes in a pandas dataframe
        if isinstance(data, pandas.DataFrame):
            self.table_names.append(name)
            print(data)

            create_table = f"CREATE TABLE IF NOT EXISTS {name} (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            populate_table = f"INSERT INTO {name} ("

            num_columns = data.columns.size # data.columns is a pandas.index object, get its length with '.size'
            num_loops = 0
            values = []
            for column in data.columns:
                num_loops+=1
                populate_table += column
                if str(data.dtypes.get(column)) == "str":
                    data_type = "TEXT"
                elif str (data.dtypes.get(column)) == "int64":
                    data_type = "INTEGER"
                create_table = create_table + column + " " + data_type
                values.append(column)
                if num_loops != num_columns:
                    create_table += ","
                    populate_table += ","
            create_table += ");"
            print(create_table)
            self.cursor.execute(create_table)
            self.conn.commit()
            self.schema[name] = values
            print("table created")
            num_entries = data.index.size
            populate_table += ') VALUES '
            num_loops = 0
            for index in data.index: # this will loopthe number of times that entries in the table
                row = data.loc[index].to_list() # row is a list
                row = "','".join(str(item) for item in row)
                populate_table += f" ('{row}')"
                num_loops += 1
                if num_loops != num_entries:
                    populate_table += ","
            print(populate_table)
            self.cursor.execute(populate_table)
            self.conn.commit()            

    def view_tables(self):
        for name in self.table_names:
            view_table = "PRAGMA table_info(" + name + ")"
            table = self.cursor.execute(view_table).fetchall()
            if table:
                print(f"Table {name} exists: {table}")
                print(f"column 1 {table[1][1]}")
     
        
