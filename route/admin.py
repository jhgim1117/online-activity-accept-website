from os import path
from flask import render_template, session, request, abort, redirect
from lib import db
import random

def admin_get():
    return render_template('/admin/index.html')

def user_list_get():
    user_list_in_db = db.db_execute("SELECT * FROM user")
    return render_template(
        'admin/user_list.html',
        user_list = user_list_in_db
    )

def token_get():
    return render_template('/admin/token.html')

def token_post():
    generation, num = request.form["generation"], request.form["num"]
    token = random.randint(100000, 999999)
    db.db_execute("INSERT INTO token (generation, num, token) VALUES (?, ?, ?)", (generation, num, token))
    return render_template('/admin/token.html')

def token_list_get():
    token_list_in_db = db.db_execute("SELECT * FROM token")
    return render_template(
        'admin/token_list.html',
        user_token_list = token_list_in_db
    )

def token_delete():
    id = request.form['id']
    db.db_execute("DELETE FROM token WHERE id=?", (id, ))
    return redirect('/admin/token/list')

def user_delete():
    id = request.form['id']
    db.db_execute("DELETE FROM user WHERE id=?", (id, ))
    return redirect("/admin/user/list")

def treat_admin(act, is_get):
    print(act)
    if not 'admin' in session:
        return abort(403)
    path_list = act.split('/')
    if path_list[0] == 'user':
        if path_list[1] == 'list':
            if is_get:
                return user_list_get()
            else:
                abort(405)
        if path_list[1] == 'delete':
            if not is_get:
                return user_delete()
            else:
                abort(405)
    elif path_list[0] == 'token':
        if len(path_list)==1:
            if is_get:
                return token_get()
            else:
                return token_post()
        elif path_list[1] == 'delete':
            if is_get:
                abort(405)
            else:
                return token_delete()
        elif path_list[1] == 'list':
            if is_get:
                return token_list_get()
            else:
                abort(405)
    abort(404)
