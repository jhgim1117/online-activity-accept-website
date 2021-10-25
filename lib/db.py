import sqlite3
def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def db_execute(exec, v=()):
    conn = sqlite3.connect('db/main.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(exec, v)
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

def check_table_info(tbl_name):
    table_info = db_execute("PRAGMA table_info(" + tbl_name + ")")
    for column_info in table_info:
        print(f"column name : {column_info['name']}")
        print(f"type of data : {column_info['type']}")
        print('------------------')

##use example 1: print(db_execute("SELECT * FROM user"))
## 2: db_execute("INSERT ~")

##for learning query of sqlite: google "sqlite query"

# create table
# db_execute("CREATE TABLE user(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, num INTEGER NOT NULL, generation INTEGER NOT NULL, nickname TEXT NOT NULL, pw TEXT NOT NULL)")

# check db info
check_table_info('user')
# print(len(db_execute("PRAGMA table_info(user)")))