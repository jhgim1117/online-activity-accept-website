from flask import render_template, request, redirect, session
from lib import db
import bcrypt
import datetime

def login_get():
    status=0
    if 'state' in request.args.to_dict():
        status=int(request.args.to_dict()['state'])
    return render_template('user/login.html', status=status)

def login_post():
    id, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    id_list = db.db_execute("SELECT id FROM user WHERE nickname=?", (id,))
    if not len(id_list):
        return redirect('/login?state=2')
    hashed_pw = db.db_execute('SELECT pw FROM user WHERE nickname=?', (id,))[0]['pw']
    if bcrypt.checkpw(plain_pw.encode('utf-8'),hashed_pw.encode('utf-8')):
        session['user_id'] = id_list[0]['id']
        return redirect('/')
    else:
        return redirect('/login?state=3')

def signup_get():
    status=0
    if 'state' in request.args.to_dict():
        status=int(request.args.to_dict()['state'])
    return render_template('user/signup.html', status=status)

def signup_post():
    nickname, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    name = request.form["name"]
    generation = request.form["generation"]
    num = request.form["num"]
    now = datetime.datetime.now()
    
    if not (nickname and plain_pw and name and generation and num):
        return redirect('/signup?state=1')
    
    able_generation = [now.year-1985, now.year-1984, now.year-1983]
    if not int(generation) in able_generation:
        return redirect('/signup?state=2')
    
    if len(name) < 2 or len(name) > 10:
        return redirect('/signup?state=3')
        
    str_num = str(num)
    if (int(str_num[0]) not in range(1, 4)) or (int(str_num[1]) not in range(1, 6)) or (int(str_num[2:]) not in range(1, 25)):
        return redirect('/signup?state=4')

    id_list = db.db_execute("SELECT id FROM user WHERE nickname=?", (nickname,))
    if len(id_list):
        return redirect('/signup?state=5')

    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.user_insert(name, num, generation, nickname, hashed_pw)
    return redirect('/login?state=1')
