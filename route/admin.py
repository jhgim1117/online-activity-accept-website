from flask import render_template, session, request, abort, redirect, flash
from lib import db
import random

def admin_get():
    if not 'admin' in session:
        return abort(403)
    return render_template('/admin/index.html')

def student_list_get():
    student_list_in_db = db.db_execute("SELECT * FROM student")
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

def teacher_token_post():
    name = request.form["name"]
    subject_id = request.form['subject']
    token = random.randint(100000, 999999)
    if not db.db_execute("SELECT * FROM teacher_token WHERE name=? AND subject_id=?", (name, subject_id)):
        db.db_execute("INSERT INTO teacher_token (name, token, subject_id) VALUES (?, ?, ?)", (name, token, subject_id))
    else:
        flash("이미 토큰이 발급되어있습니다.")
    return redirect('/admin/teacher/token')

def teacher_token_list():
    teacher_token_list_in_db = db.db_execute("SELECT * FROM teacher_token")
    return render_template(
        'admin/teacher/token_list.html',
        teacher_token_list = teacher_token_list_in_db
    )

def teacher_token_delete():
    id = request.form['id']
    db.db_execute("DELETE FROM teacher_token WHERE id=?", (id, ))
    return redirect('/admin/teacher/token/list')

def teacher_delete():
    id = request.form['id']
    db.db_execute("DELETE FROM teacher WHERE teacher_id=?", (id, ))
    return redirect('/admin/teacher/list')

def teacher_list():
    teacher_list_in_db = db.db_execute("SELECT * FROM teacher")
    return render_template(
        'admin/teacher/list.html',
        teacher_list = teacher_list_in_db
    )

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
    elif path_list[0] == 'teacher':
        if path_list[1] == 'list':
            if is_get:
                return teacher_list()
        if path_list[1] == 'delete':
            if is_get:
                return abort(405)
            else:
                return teacher_delete()
        if path_list[1] == 'token':
            if len(path_list) == 2:
                if is_get:
                    return render_template('/admin/teacher/token.html')
                else:
                    return teacher_token_post()
            elif path_list[2] == 'list':
                if is_get:
                    return teacher_token_list()
                else:
                    abort(405)
            elif path_list[2] == 'delete':
                if is_get:
                    return abort(405)
                else:
                    return teacher_token_delete()
        elif path_list[1] == list:
            if is_get:
                return teacher_list()
            else:
                return abort(405)
        elif path_list[1] == 'delete':
            if is_get:
                return abort(405)
            else:
                return teacher_delete()
    return abort(404)
