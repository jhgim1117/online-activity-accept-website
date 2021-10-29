from flask import render_template, session, request, abort, redirect
from lib import db
import random

def admin_get():
    if not 'admin' in session:
        return abort(403)
    return render_template('/admin/index.html')

def user_list_get():
    user_list_in_db = db.db_execute("SELECT * FROM user")
    return render_template(
        'admin/user_list.html',
        user_list = user_list_in_db
    )

def token_get():
    if not 'admin' in session:
        return abort(403)
    return render_template('/admin/token.html')

def token_post():
    if not 'admin' in session:
        return abort(403)
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
    return redirect("/admin/user")

def treat_admin(act, is_get):
    print(act)
    if not 'admin' in session:
        return abort(403)
    if act == "user/list":
        if is_get:
            return user_list_get()
        else:
            abort(405)
    elif act == "user/delete":
        if not is_get:
            return user_delete()
        else:
            abort(405)
    elif act == "token":
        if is_get:
            return token_get()
        else:
            return token_post()
    elif act == "token/delete":
        if is_get:
            abort(405)
        else:
            return token_delete()
    elif act == "token/list":
        if is_get:
            return token_list_get()
        else:
            abort(405)
    abort(404)
