from flask import render_template, request, redirect, session, flash
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

def configdata_post():
    user_id=session['user_id']
        #이름 학번 기수 아이디 가져오기
    nickname = db.db_execute('SELECT nickname FROM user WHERE id=?', (user_id,))[0]['nickname']
    name = db.db_execute('SELECT name FROM user WHERE id=?', (user_id,))[0]['name']
    num = db.db_execute('SELECT num FROM user WHERE id=?', (user_id,))[0]['num']
    generation = db.db_execute('SELECT generation FROM user WHERE id=?', (user_id,))[0]['generation']

    if 'user_id' in session: #로그인 상태일때만
        return render_template('user/configdata.html', nickname=nickname, name=name, num=num, generation=generation)

def db_config_update():
    user_id=session['user_id']

    name = request.form["name"]
    num = request.form["num"]
    generation = request.form["generation"]
    Id = request.form["ID"]
    present_pw = request.form["now password"] #사용자가 작성한 기존 비번
    new_pw = request.form["new password"] #바꿀 비번
    renew_pw = request.form["renew password"] #바꿀 비번 확인
    
    hashed_pw = db.db_execute('SELECT pw FROM user WHERE nickname=?', (user_id,))[0]['pw'] #DB 상의 기존 비번 들고오기
    if new_pw == renew_pw: #비번 확인
        if bcrypt.checkpw(present_pw.encode('utf-8'),hashed_pw.encode('utf-8')): #DB 기존 비번과 입력한 비번이 일치하면 DB업데이트 
            db.user_update(name, num, generation, Id, new_pw)
            flash("성공적으로 변경되었습니다!")
            return render_template("index.html")
        else:
            flash("기존 비밀번호가 일치하지 않습니다!")
            return render_template("configdata.html")
    else:
        flash("새 비밀번호와 다시 확인 비밀번호가 다릅니다!")
        return render_template("configdata.html")
    
    db.user_insert()
