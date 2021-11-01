from flask import render_template, request, redirect, session, flash, abort
from lib import db
import bcrypt
import datetime

def login_post():
    id, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    id_list = db.db_execute("SELECT id FROM student WHERE nickname=?", (id,))
    if not len(id_list):
        flash("id가 존재하지 않습니다.")
        return redirect('/student/login')
    student_id = id_list[0]['id']
    hashed_pw = db.db_execute('SELECT pw FROM student WHERE nickname=?', (id,))[0]['pw']
    if bcrypt.checkpw(plain_pw.encode('utf-8'),hashed_pw.encode('utf-8')):
        if len(db.db_execute('SELECT * FROM admin WHERE student_id=?', (student_id,))):
            session['admin'] = True
        session['student_id'] = student_id
        return redirect('/')
    else:
        flash('pw가 일치하지 않습니다.')
        return redirect('/student/login')

def signup_post():
    nickname, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    name = request.form["name"]
    generation = request.form["generation"]
    num = request.form["num"]
    token = request.form['token']
    now = datetime.datetime.now()

    # 빈칸 거르기
    if not (nickname and plain_pw and name and generation and num and token):
        flash('입력되지 않은 데이터가 있습니다.')
        return redirect('/student/signup')
    
    able_generation = [now.year-1985, now.year-1984, now.year-1983]
    if not int(generation) in able_generation:
        flash('기수 입력이 잘못되었습니다.')
        return redirect('/student/signup')

    if len(name) < 2 or len(name) > 10:
        flash('이름 길이가 범위에서 벗어났습니다.')
        return redirect('/student/signup')
        
    str_num = str(num)
    if (int(str_num[0]) not in range(1, 4)) or (int(str_num[1]) not in range(1, 6)) or (int(str_num[2:]) not in range(1, 25)):
        flash('학번 입력이 잘못되었습니다.')
        return redirect('/student/signup')

    id_list = db.db_execute("SELECT id FROM student WHERE nickname=?", (nickname,))
    if len(id_list):
        flash('이미 존재하는 id입니다.')
        return redirect('/student/signup')
    
    token_list = db.db_execute("SELECT token FROM student_token WHERE num=? AND generation=?", (num, generation))
    if len(token_list):
        if int(token) != int(token_list[0]['token']):
            flash('토큰이 일치하지 않습니다.')
            return redirect('/student/signup')
    else:
        flash('토큰이 등록되어있지 않습니다.')
        return redirect('/student/signup')
    db.db_execute('DELETE FROM student_token WHERE num=? AND generation=?', (num, generation))

    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.db_execute("insert into student (name, num, generation, nickname, pw) values (?, ?, ?, ?, ?);", (name, num, generation, nickname, hashed_pw))
    flash('회원가입되었습니다. 로그인해주시기 바랍니다.')
    return redirect('/student/login')
    
def config_get():
    student_id=session['student_id']
        #이름 학번 기수 아이디 가져오기
    student_data = db.db_execute('SELECT nicknamem, name, num, generation FROM student WHERE id=?', (student_id,))[0]

    if 'student_id' in session: #로그인 상태일때만
        return render_template('student/config.html', nickname=student_data['nickname'], name=student_data['name'], num=student_data['num'], generation=student_data['generation'])

def config_post():
    student_id=session['student_id']

    name = request.form["name"]
    num = int(request.form["num"])
    generation = int(request.form["generation"])
    Id = request.form["ID"]
    present_pw = request.form["now password"] #사용자가 작성한 기존 비번
    new_pw = request.form["new password"] #바꿀 비번
    renew_pw = request.form["renew password"] #바꿀 비번 확인
    
    hashed_pw = db.db_execute('SELECT pw FROM student WHERE id=?', (student_id,))[0]['pw'] #DB 상의 기존 비번 들고오기
    if new_pw == renew_pw: #비번 확인
        if bcrypt.checkpw(present_pw.encode('utf-8'),hashed_pw.encode('utf-8')): #DB 기존 비번과 입력한 비번이 일치하면 DB업데이트 
            hashed_pw = bcrypt.hashpw(new_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.db_execute("UPDATE student SET name=?, num=?, generation=?, nickname=?, pw=? WHERE id=?", (name, num, generation, Id, hashed_pw, student_id))
            flash("성공적으로 변경되었습니다!")
            return redirect("/student/config")
        else:
            flash("기존 비밀번호가 일치하지 않습니다!")
            return redirect("/student/config")
    else:
        flash("새 비밀번호와 다시 확인 비밀번호가 다릅니다!")
        return redirect("/student/config")

def treat_student(act, is_get):  
    if act == "login":
        if 'student_id' in session:
            flash("이미 로그인된 상태입니다.")
            return redirect('/')
        if is_get:
            return render_template('student/login.html')
        else:
            return login_post()
    elif act == "signup":
        if 'student_id' in session:
            flash("이미 로그인된 상태입니다.")
            return redirect('/')
        if is_get:
            return render_template('student/signup.html')
        else:
            return signup_post()
    elif act == "config":
        if is_get:
            return config_get()
        else:
            return config_post()
    elif act == "signout":
        if not is_get:
            session.pop('student_id', None)
            session.pop('admin', None)
            return redirect("/")
        else:
            return abort(405)
    return abort(404)