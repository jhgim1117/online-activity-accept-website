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

##use example 1: print(db_execute("SELECT * FROM user"))
## 2: db_execute("INSERT ~")

##for learning query of sqlite: google "sqlite query"

# db_execute("CREATE TABLE user(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, num INT NOT NULL, generation INT NOT NULL, nickname TEXT NOT NULL, pw TEXT NOT NULL)")

print(db_execute("SELECT * FROM user WHERE rowid = 0"))