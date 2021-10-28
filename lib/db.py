import sqlite3
import bcrypt
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

def user_update(name, num, generation, nickname, plain_pw):
    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_execute("UPDATE user SET name=?, num=?, generation=?, nickname=?, pw=? WHERE id=?", (name, num, generation, nickname, hashed_pw, id))

def token_insert(generation, num, token):
    db_execute("INSERT INTO token (generation, num, token) VALUES (?, ?, ?)", (generation, num, token))

def show_db_info(table):
    print(db_execute("SELECT * FROM " + table))
##use example 1: print(db_execute("SELECT * FROM user"))
## 2: db_execute("INSERT ~")

##for learning query of sqlite: google "sqlite query"

if __name__ == '__main__':
    
    # create table
    # db_execute("CREATE TABLE user(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, num INTEGER NOT NULL, generation INTEGER NOT NULL, nickname TEXT NOT NULL, pw TEXT NOT NULL)")
    # db_execute("CREATE TABLE request(req_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, datetime DATETIME NOT NULL, req_user INTEGER NOT NULL, req_date DATE NOT NULL, req_start_time TIME NOT NULL, req_end_time TIME NOT NULL, place TEXT NOT NULL, reason TEXT NOT NULL, teacher_id INTEGER NOT NULL)")
    # db_execute("CREATE TABLE token(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, generation INTEGER NOT NULL, num INTEGER NOT NULL, token INTEGER NOT NULL)")
    # check db info
    # check_table_info('user')
    # print(db_execute("SELECT * FROM user"))
    # check_table_info('token')
    # db_execute('UPDATE user SET pw="minjae@@2" WHERE id=10')
    # user_update('이시환', 2114, 37, 'lhs0831', '123456789', 7)
    show_db_info('token')