from flask import render_template, request, redirect, session
from lib import db
import bcrypt
import datetime

def login_get():
    status=0
    if 'signup' in request.args.to_dict():
        status=1
    elif 'no_id' in request.args.to_dict():
        status=2
    elif 'wrong' in request.args.to_dict():
        status=3
    return render_template('user/login.html', status=status)

def login_post():
    id, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    id_list = db.db_execute("SELECT id FROM user WHERE nickname=?", (id,))
    if not len(id_list):
        return redirect('/login?no_id=1')
    hashed_pw = db.db_execute('SELECT pw FROM user WHERE nickname=?', (id,))[0]['pw']
    if bcrypt.checkpw(plain_pw.encode('utf-8'),hashed_pw.encode('utf-8')):
        session['user_id'] = id_list[0]['id']
        return redirect('/')
    else:
        return redirect('/login?wrong=1')

def signup_get():
    return render_template('user/signup.html')

def signup_post():
    nickname, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    name = request.form["name"]
    generation = request.form["generation"]
    num = request.form["num"]
    now = datetime.datetime.now()
    
    # 빈칸 거르기
    if not (nickname and plain_pw and name and generation and num):
        print("오류")
        return "오류"
    
    # 기수 거르기
    able_generation = [now.year-1985, now.year-1984, now.year-1983]
    if generation in able_generation:
        print("gen: yes")
        pass
    else:
        print("gen: no")
        pass #경고 메시지
    
    #닉네임 거르기
    
    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.user_insert(name, num, generation, nickname, hashed_pw)
    return redirect('/login?signup=1')