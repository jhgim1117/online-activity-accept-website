from flask import render_template, session, request, abort, redirect
from lib import db
import random

def show_admin_site():
    if not 'admin' in session:
        return abort(403)
    return render_template('/admin/index.html')

def show_user_list():
    user_list_in_db = db.db_execute("SELECT * FROM user")
    if not 'admin' in session:
        return abort(403)
    return render_template(
        'admin/user_list.html',
        user_list = user_list_in_db
    )

def user_delete():
    id = request.form['id']
    db.db_execute("DELETE FROM user WHERE id=?", (id, ))
    return redirect("/admin/user")

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

def show_token_list():
    token_list_in_db = db.db_execute("SELECT * FROM token")
    if not 'admin' in session:
        return abort(403)
    return render_template(
        'admin/token_list.html',
        user_token_list = token_list_in_db
    )

def token_delete():
    id = request.form['id']
    db.db_execute("DELETE FROM token WHERE id=?", (id, ))
    return redirect('/admin/token/list')