from flask import render_template, session, request, abort
from lib import db
import random

def show_admin_site():
    if not 'admin' in session:
        return abort(403)
    return render_template('/admin/index.html')

def token_post():
    if not 'admin' in session:
        return abort(403)
    generation, num = request.form["generation"], request.form["num"]
    token = random.randint(100000, 999999)
    db.db_execute("INSERT INTO token (generation, num, token) VALUES (?, ?, ?)", (generation, num, token))
    return render_template('/admin/token.html')

def token_get():
    if not 'admin' in session:
        return abort(403)
    return render_template('/admin/token.html')

token_list_in_db = db.db_execute("SELECT * FROM token")
def show_token_list():
    if not 'admin' in session:
        return abort(403)
    return render_template(
        'admin/token_list.html',
        user_token_list = token_list_in_db
    )

user_list_in_db = db.db_execute("SELECT * FROM user")

def show_user_list():
    if not 'admin' in session:
        return abort(403)
    return render_template(
        'admin/user_list.html',
        user_list = user_list_in_db
    )