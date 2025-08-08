import sqlite3

#CREATE A CONNECTION TO THE SQLITE DATABASE
connection = sqlite3.connect("personaltaskmanager.db")

''' CREATING AN OBJECT FOR CURSOR(CONTROL STRUCTURE) TO BRIDGE THE CONNECTION BETWEEN PYTHON APP AND SQLITE
THIS CURSOR ONLY HELPS IN EXECUTING THE QUERIES , FETCHING RESULTS AND ITERATE THROUGH DATASETS '''
cursor = connection.cursor()

#LIST OF TABLES IN A DATABASE
''' cursor.execute(""" SELECT name FROM sqlite_master WHERE type = "table" """)
tables = cursor.fetchall()
print("Current tables in the database:", tables) '''


#CREATE A TABLE FOR STORING THE LEGITIMATE USERS IN THE DATABASE
cursor.execute(""" CREATE TABLE IF NOT EXISTS users
               (username TEXT NOT NULL UNIQUE PRIMARY KEY,
                password TEXT NOT NULL,
                name TEXT)""")

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

''' cursor.execute(""" DROP TABLE task""") '''
#CREATE THE DATABASE TO STORE THE TASKS

cursor.execute(""" CREATE TABLE IF NOT EXISTS task 
               (taskid INTEGER PRIMARY KEY AUTOINCREMENT,
                taskname TEXT NOT NULL,
               description TEXT,
                due_date DATE,
               priority TEXT,
               category TEXT,
               remainder TEXT,
                username TEXT NOT NULL,
                FOREIGN KEY(username) REFERENCES users(username))""")

cursor.execute("SELECT * FROM task")
rows = cursor.fetchall()
for row in rows:
    print(row)


connection.commit()

connection.close()

