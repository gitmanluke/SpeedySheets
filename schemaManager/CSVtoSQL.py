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

class schemaManager():
    def __init__():
        pass

    def add_table(data):
        print("table added to db")

