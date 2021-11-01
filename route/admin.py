from flask import render_template, session, request, abort, redirect, flash
from lib import db
import random

def admin_get():
    if not 'admin' in session:
        return abort(403)
    return render_template('/admin/index.html')

def student_list_get():
    student_list_in_db = db.db_execute("SELECT * FROM student")
    print(student_list_in_db)
    return render_template(
        'admin/student/list.html',
        student_list = student_list_in_db
    )

def student_token_post():
    generation, num = request.form["generation"], request.form["num"]
    student_token = random.randint(100000, 999999)
    if not db.db_execute("SELECT * FROM student_token WHERE num=? AND generation=?", (num, generation)):
        db.db_execute("INSERT INTO student_token (generation, num, token) VALUES (?, ?, ?)", (generation, num, student_token))
    else:
        flash('이미 토큰이 발급되어있습니다.')
    return render_template('/admin/student/token.html')

def student_token_list_get():
    student_token_list_in_db = db.db_execute("SELECT * FROM student_token")
    return render_template(
        'admin/student/token_list.html',
        student_token_list = student_token_list_in_db
    )

def student_token_delete():
    id = request.form['id']
    db.db_execute("DELETE FROM student_token WHERE id=?", (id, ))
    return redirect('/admin/student/token/list')

def student_delete():
    id = request.form['id']
    db.db_execute("DELETE FROM student WHERE id=?", (id, ))
    return redirect("/admin/student/list")

def teacher_token_get():
    return render_template('/admin/teacher/token.html')

def teacher_token_post():
    name, subject = request.form["name"], request.form["subject"]
    token = random.randint(100000, 999999)
    if not db.db_execute("SELECT * FROM teacher_token WHERE name=? AND subject=?", (name, subject)):
        db.db_execute("INSERT INTO teacher_token (name, token) VALUES (?, ?)", (name, token))

def treat_admin(act, is_get):
    if not 'admin' in session:
        return abort(403)
    path_list = act.split('/')
    if path_list[0] == 'student':
        if path_list[1] == 'list':
            if is_get:
                return student_list_get()
            else:
                return abort(405)
        if path_list[1] == 'delete':
            if not is_get:
                return student_delete()
            else:
                return abort(405)
        if path_list[1] == 'token':
            if len(path_list) ==2:
                if is_get:
                    return render_template('/admin/student/token.html')
                else:
                    return student_token_post()
            if path_list[2] == 'delete':
                if is_get:
                    return abort(405)
                else:
                    return student_token_delete()
            if path_list[2] == 'list':
                if is_get:
                    return student_token_list_get()
                else:
                    return abort(405)
        return abort(404)