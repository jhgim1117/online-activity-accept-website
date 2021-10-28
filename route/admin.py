from flask import render_template, session
from lib import db
import random

admin_ID = 'admin'
def check_admin():
    user_id = session['user_id']
    ID = db.db_execute("SELECT nickname FROM user WHERE id=?", (user_id, ))[0]['nickname']
    print(ID)
    if ID == admin_ID:
        return True
    else:
        return False

def show_admin_site():
    if check_admin():
        return render_template('/admin/index.html')
    else:
        return render_template('/admin/not_admin.html')

def token_post():
    if check_admin():
        generation, num = request.form["generation"], request.form["num"]
        token = random.randint(100000, 999999)
        db_execute("INSERT INTO token (generation, num, token) VALUES (?, ?, ?)", (generation, num, token))
        return render_template('/admin/token.html')
    else:
        return render_template('/admin/not_admin.html')

def token_get():
    if check_admin():
        return render_template('/admin/token.html')
    else:
        return render_template('/admin/not_admin.html')

token_list_in_db = db.db_execute("SELECT * FROM token")
def show_token_list():
    if check_admin():
        return render_template(
            'admin/token_list.html',
            user_token_list = token_list_in_db
        )
    else:
        return render_template('/admin/not_admin.html')

user_list_in_db = db.db_execute("SELECT * FROM user")

def show_user_list():
    if check_admin():
        return render_template(
            'admin/user_list.html',
            user_list = user_list_in_db
        )
    else:
        return render_template('/admin/not_admin.html')
