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
        self.table_names = []
        try:
            with sqlite3.connect("data/database.db") as self.conn: #opens connection with existing database or creates new one if not found
                self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as e:
            print("Failed to open database:", e)

    def add_table(self, data, name):
        # takes in a pandas dataframe
        if isinstance(data, pandas.DataFrame):
            self.table_names.append(name)
            print(data)
            print(data.dtypes.get("last_name"))

            create_table = "CREATE TABLE IF NOT EXISTS " + name + " (id INTEGER PRIMARY KEY AUTOINCREMENT, "

            num_columns = data.columns.size # data.columns is a pandas.index object, get its length with '.size'
            num_loops = 0
            for column in data.columns:
                num_loops+=1
                if str(data.dtypes.get(column)) == "str":
                    data_type = "TEXT"
                elif str (data.dtypes.get(column)) == "int64":
                    data_type = "INTEGER"
                create_table = create_table + column + " " + data_type
                if num_loops != num_columns:
                    create_table += ","
            create_table += ");"
            print(create_table)
            self.cursor.execute(create_table)
            self.conn.commit()
            print("table created")


    def view_tables(self):
        for name in self.table_names:
            view_table = "PRAGMA table_info(" + name + ")"
            table = self.cursor.execute(view_table).fetchall()
            if table:
                print(f"Table {name} exists")
            else:
                print(f"Table {name} does not exist")
     
        
