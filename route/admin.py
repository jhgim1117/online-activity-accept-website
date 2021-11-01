from flask import render_template, session, request, abort, redirect, flash
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
    return render_template('/admin/token.html')

def token_post():
    generation, num = request.form["generation"], request.form["num"]
    token = random.randint(100000, 999999)
    if not db.db_execute("SELECT * FROM token WHERE num=? AND generation=?", (num, generation, )):
        db.db_execute("INSERT INTO token (generation, num, token) VALUES (?, ?, ?)", (generation, num, token))
    else:
        flash('이미 토큰이 발급되어있습니다.')
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

def teacher_token_get():
    return render_template('/admin/token_teacher.html')

def teacher_token_post():
    name = request.form["name"]
    token = random.randint(100000, 999999)
    if not db.db_execute("SELECT * FROM teacher_token WHERE name=?", (name, )):
        db.db_execute("INSERT INTO teacher_token (name, token) VALUES (?, ?)", (name, token))
    else:
        flash("이미 토큰이 발급되어있습니다.")
    return redirect('/admin/token/teacher')

def treat_admin(act, is_get):
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
        elif path_list[1] == 'teacher':
            if is_get:
                return teacher_token_get()
            else:
                return teacher_token_post()
            
    abort(404)
