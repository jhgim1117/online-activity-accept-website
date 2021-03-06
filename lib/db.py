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

def show_table_info(table):
    print(db_execute("SELECT * FROM " + table))

##use example 1: print(db_execute("SELECT * FROM student"))
## 2: db_execute("INSERT ~")

##for learning query of sqlite: google "sqlite query"

if __name__ == '__main__':
    
    db_execute("CREATE TABLE IF NOT EXISTS student(student_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, num INTEGER NOT NULL, generation INTEGER NOT NULL, nickname TEXT NOT NULL, pw TEXT NOT NULL)")
    db_execute("DROP TABLE apply")
    db_execute("CREATE TABLE IF NOT EXISTS apply(req_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, datetime DATETIME NOT NULL, req_student INTEGER NOT NULL, req_date DATE NOT NULL, req_start_time TIME NOT NULL, req_end_time TIME NOT NULL, place INTEGER NOT NULL, reason TEXT NOT NULL, num INTEGER NOT NULL, name TEXT NOT NULL)")
    db_execute("DROP TABLE confirmed_apply")
    db_execute("CREATE TABLE IF NOT EXISTS confirmed_apply(confirm_id INTEGER PRIMARY KEY AUTOINCREMENT, req_id INTEGER NOT NULL, allowed INTEGER)")
    db_execute("CREATE TABLE IF NOT EXISTS student_token(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, generation INTEGER NOT NULL, num INTEGER NOT NULL, token INTEGER NOT NULL)")
    db_execute("CREATE TABLE IF NOT EXISTS admin(admin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL)")
    db_execute("CREATE TABLE IF NOT EXISTS teacher(teacher_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, nickname TEXT NOT NULL, pw TEXT NOT NULL)")
    db_execute("CREATE TABLE IF NOT EXISTS teacher_token(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, token INTEGER NOT NULL)")
    check_table_info("confirmed_apply")