from flask import render_template, request
from lib import db

def login_get():
    return render_template('user/login.html')

def login_post():
    id, pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    
    print(id)
    print(pw)
    
    return render_template('user/login.html')

def signup_get():
    return render_template('user/signup.html')

def signup_post():
    nickname, pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    name = request.form["name"]
    generation = request.form["generation"]
    num = request.form["num"]
    print(name, num, generation, nickname, pw)
    db.user_insert(name, num, generation, nickname, pw)
    return render_template('user/signup.html')