from flask import render_template, request
from lib import db
import bcrypt

def login_get():
    return render_template('user/login.html')

def login_post():
    id, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    return render_template('user/login.html')

def signup_get():
    return render_template('user/signup.html')

def signup_post():
    nickname, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    name = request.form["name"]
    generation = request.form["generation"]
    num = request.form["num"]
    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(hashed_pw)
    db.user_insert(name, num, generation, nickname, hashed_pw)
    return render_template('user/signup.html')
