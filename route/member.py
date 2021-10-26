from flask import render_template, request
from lib import db
import bcrypt

def login_get():
    return render_template('user/login.html')

def login_post():
    id, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    hashed_pw = db.db_execute('SELECT pw FROM user WHERE nickname=?', (id,))[0]['pw']
    if bcrypt.checkpw(plain_pw.encode('utf-8'),hashed_pw.encode('utf-8')):
        return '<script>alert("성공");</script>'
    else:
        return '<script>alert("실패");</script>'
    return render_template('user/login.html')

def signup_get():
    return render_template('user/signup.html')

def signup_post():
    nickname, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    name = request.form["name"]
    generation = request.form["generation"]
    num = request.form["num"]
    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.user_insert(name, num, generation, nickname, hashed_pw)
    return render_template('user/signup.html')
