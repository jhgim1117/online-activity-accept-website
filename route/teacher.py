from flask import render_template, session, abort, request, flash, redirect
from lib import db
import bcrypt

def teacher_get():
    name=''
    if 'teacher_id' in session:
        if 'teacher_id' in session:
            teacher_id=session['teacher_id']
            name = db.db_execute('SELECT name FROM teacher WHERE teacher_id=?', (teacher_id,))[0]['name']
    return render_template('teacher/index.html', name=name)

def signup_post():
    name = request.form['name']
    nickname = request.form['nickname']
    plain_pw = request.form['PW']
    token = request.form['token']
    subject_id = request.form['subject']
    homeroom = request.form['homeroom']

    if not(name and nickname and plain_pw and token and homeroom):
        flash('입력되지 않은 정보가 있습니다.')
        return redirect('/teacher/signup')
    
    if len(name) < 2 or len(name) > 10:
        flash('이름 길이가 범위에서 벗어났습니다.')
        return redirect('/teacher/signup') 
    
    id_list = db.db_execute("SELECT teacher_id FROM teacher WHERE nickname=?", (nickname,))
    if len(id_list):
        flash('이미 존재하는 id입니다.')
        return redirect('/teacher/signup')
    
    str_homeroom = str(homeroom)
    if not((int(str_homeroom[0]) in range(1, 4) and int(str_homeroom[1]) in range(1, 6)) or homeroom == 0):
        flash('학반 정보를 안내에 따라 정확히 입력해주세요.')
        return redirect('/teacher/signup')

    token_list = db.db_execute("SELECT token FROM teacher_token WHERE name=? AND subject_id=?", (name, subject_id))
    if len(token_list):
        if int(token) != int(token_list[0]['token']):
            flash('토큰이 일치하지 않습니다.')
            return redirect('/teacher/signup')
    else:
        flash('토큰이 등록되어있지 않습니다.')
        return redirect('/teacher/signup')
    db.db_execute('DELETE FROM teacher_token WHERE name=?', (name, ))

    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.db_execute("INSERT INTO teacher (name, nickname, pw, subject_id, homeroom) values (?, ?, ?, ?, ?);", (name, nickname, hashed_pw, subject_id, homeroom))
    flash('회원가입되었습니다. 로그인해주시기 바랍니다.')
    return redirect('/teacher/login')

def login_post():
    id, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    try:
        dayduty = bool(request.form['dayduty'])
    except:
        dayduty = False
    id_list = db.db_execute("SELECT teacher_id FROM teacher WHERE nickname=?", (id,))
    if not len(id_list):
        flash("id가 존재하지 않습니다.")
        return redirect('/teacher/login')
    teacher_id = id_list[0]['teacher_id']
    hashed_pw = db.db_execute('SELECT pw FROM teacher WHERE nickname=?', (id,))[0]['pw']
    if bcrypt.checkpw(plain_pw.encode('utf-8'),hashed_pw.encode('utf-8')):
        
        session['teacher'] = True
        session['teacher_id'] = teacher_id
        session['dayduty'] = dayduty
        return redirect('/teacher')
    else:
        flash('pw가 일치하지 않습니다.')
        return redirect('/teacher/login')

def apply_index():
    teacher_id = session['teacher_id']
    teacher_info = db.db_execute("SELECT * FROM teacher WHERE teacher_id=?", (teacher_id, ))[0]
    homeroom = teacher_info['homeroom']
    subject_id = teacher_info['subject_id']
    dayduty = session['dayduty']
    return render_template(
        'teacher/apply/index.html',
        homeroom = homeroom,
        subject_id = subject_id,
        dayduty = dayduty
    )

def apply_homeroom():
    homeroom = db.db_execute('SELECT homeroom FROM teacher WHERE teacher_id=?', (session['teacher_id'], ))[0]['homeroom']
    apply_list = db.db_execute("SELECT * FROM apply WHERE num/100=?", (int(homeroom), ))
    print(apply_list)
    return render_template(
        'teacher/apply/list.html',
        apply = apply_list
    )

def apply_RnE():
    subject_id = db.db_execute('SELECT subject_id FROM teacher WHERE teacher_id=?', (session['teacher_id'], ))[0]['subject_id']
    user_ids = db.db_execute("SELECT user_id FROM rne WHERE rne_id=?", (subject_id, ))
    user_id_list = [list(i.values())[0] for i in user_ids]
    print(user_id_list)

def treat_teacher(act, is_get):
    path_list = act.split('/')
    if act == 'login':
        if 'teacher_id' in session:
            flash('이미 로그인 된 상태입니다.')
            return redirect('/teacher')
        if is_get:
            return render_template('/teacher/login.html')
        else:
            return login_post()
    elif act == 'signup':
        if 'teacher_id' in session:
            flash('이미 로그인 된 상태입니다.')
            return redirect('/teacher')
        if is_get:
            return render_template('/teacher/signup.html')
        else:
            return signup_post()
    elif act == "signout":
        if not is_get:
            session.pop('teacher_id', None)
            session.pop('admin', None)
            return redirect("/teacher")
        else:
            return abort(405)
    elif path_list[0] == 'apply':
        if len(path_list) == 1:
            return apply_index()
        elif path_list[1] == 'homeroom':
            return apply_homeroom()
        elif path_list[1] == 'RnE':
            apply_RnE()
        elif path_list[1] == 'dayduty':
            return render_template(
                '/teacher/apply/list.html',
                apply = db.db_execute("SELECT * FROM apply")
            )