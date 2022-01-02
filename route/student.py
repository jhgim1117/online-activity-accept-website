from flask import render_template, request, redirect, session, flash, abort
from lib import db
import bcrypt
import datetime

def student_get():
    name=''
    if 'student_id' in session:
        if 'student_id' in session:
            student_id=session['student_id']
            name = db.db_execute('SELECT name FROM student WHERE student_id=?', (student_id,))[0]['name']
    return render_template('student/index.html', name=name, session=session)

def login_post():
    id, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    id_list = db.db_execute("SELECT student_id FROM student WHERE nickname=?", (id,))
    if not len(id_list):
        flash("id가 존재하지 않습니다.")
        return redirect('/student/login')
    student_id = id_list[0]['student_id']
    hashed_pw = db.db_execute('SELECT pw FROM student WHERE nickname=?', (id,))[0]['pw']
    if bcrypt.checkpw(plain_pw.encode('utf-8'),hashed_pw.encode('utf-8')):
        if len(db.db_execute('SELECT * FROM admin WHERE student_id=?', (student_id,))):
            session['admin'] = True
        session['student_id'] = student_id
        return redirect('/student')
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
    rne = request.form["rne"]

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

    id_list = db.db_execute("SELECT student_id FROM student WHERE nickname=?", (nickname,))
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
    db.db_execute("insert into student (name, num, generation, nickname, pw) values (?, ?, ?, ?, ?)", (name, num, generation, nickname, hashed_pw))
    db.db_execute("insert into rne (rne_id) values (?)", (int(rne), ))
    flash('회원가입되었습니다. 로그인해주시기 바랍니다.')
    return redirect('/student/login')
    
def config_get():
    student_id=session['student_id']
        #이름 학번 기수 아이디 가져오기
    student_data = db.db_execute('SELECT nickname, name, num, generation FROM student WHERE student_id=?', (student_id,))[0]

    if 'student_id' in session: #로그인 상태일때만
        return render_template('student/config.html', nickname=student_data['nickname'], name=student_data['name'], num=student_data['num'], generation=student_data['generation'])

def config_post():
    student_id=session['student_id']

    name = request.form["name"]
    num = int(request.form["num"])
    generation = int(request.form["generation"])
    nickname = request.form["ID"]
    present_pw = request.form["now password"] #사용자가 작성한 기존 비번
    new_pw = request.form["new password"] #바꿀 비번
    renew_pw = request.form["renew password"] #바꿀 비번 확인
    now = datetime.datetime.now()

    hashed_pw = db.db_execute('SELECT pw FROM student WHERE student_id=?', (student_id,))[0]['pw'] #DB 상의 기존 비번 들고오기
    if not (nickname  and name and generation and num):
        flash('입력되지 않은 데이터가 있습니다.')
        return redirect('/student/config')
    
    able_generation = [now.year-1985, now.year-1984, now.year-1983]
    if not int(generation) in able_generation:
        flash('기수 입력이 잘못되었습니다.')
        return redirect('/student/config')

    if len(name) < 2 or len(name) > 10:
        flash('이름 길이가 범위에서 벗어났습니다.')
        return redirect('/student/config')
        
    str_num = str(num)
    if (int(str_num[0]) not in range(1, 4)) or (int(str_num[1]) not in range(1, 6)) or (int(str_num[2:]) not in range(1, 25)):
        flash('학번 입력이 잘못되었습니다.')
        return redirect('/student/comfig')

    id_list = db.db_execute("SELECT student_id FROM student WHERE nickname=?", (nickname,))
    if len(id_list):
        if db.db_execute("SELECT nickname FROM student WHERE student_id=?", (student_id, ))[0]['nickname'] != nickname:
            flash('이미 존재하는 ID 입니다.')
            return redirect('/student/config')

    if not new_pw:
        new_pw = present_pw
        renew_pw = present_pw        

    if new_pw == renew_pw: #비번 확인
        if bcrypt.checkpw(present_pw.encode('utf-8'),hashed_pw.encode('utf-8')): #DB 기존 비번과 입력한 비번이 일치하면 DB업데이트 
            hashed_pw = bcrypt.hashpw(new_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.db_execute("UPDATE student SET name=?, num=?, generation=?, nickname=?, pw=? WHERE student_id=?", (name, num, generation, nickname, hashed_pw, student_id))
            flash("성공적으로 변경되었습니다!")
            return redirect("/student/config")
        else:
            flash("기존 비밀번호가 일치하지 않습니다!")
            return redirect("/student/config")
    else:
        flash("비밀번호가 일치하지 않습니다")
        return redirect("/student/config")

def apply_get():
    student_id = session['student_id']
    student_info = db.db_execute("SELECT * FROM student WHERE student_id=?", (student_id, ))[0]
    name = student_info['name']
    return render_template('/student/apply/index.html', name=name)

def apply_post():
    student_id = session['student_id']
    student_info = db.db_execute("SELECT * FROM student WHERE student_id=?", (student_id, ))[0]
    name = student_info['name']
    req_student = session['student_id']
    req_date = request.form['req_date']
    req_start_time = request.form['req_start_time']
    req_end_time = request.form['req_end_time']
    place = request.form['place']
    reason = request.form['reason']
    num = db.db_execute("SELECT num FROM student WHERE student_id=?", (req_student, ))[0]['num']
    name = db.db_execute("SELECT name FROM student WHERE student_id=?", (req_student, ))[0]['name']

    # 빈칸 거르기
    if not (req_date and req_start_time and req_end_time and place and reason):
        flash('입력되지 않은 데이터가 있습니다.')
    req_date = datetime.date.fromisoformat(req_date)
    formatted_req_start_time = datetime.time.fromisoformat(req_start_time)
    formatted_req_end_time = datetime.time.fromisoformat(req_end_time)
    if formatted_req_start_time >= formatted_req_end_time:
        flash('활동 시간이 올바르지 않습니다.')
        return redirect('/student/apply')
    db.db_execute("INSERT INTO apply (datetime, req_student, req_date, req_start_time, req_end_time, place, reason, num, name) values ((SELECT datetime('now', '+9 hours')), ?, ?, ?, ?, ?, ?, ?, ?);", (req_student, req_date, req_start_time, req_end_time, place, reason, num, name))
    flash('활승 신청이 완료되었습니다.')
    return redirect("/student/apply")

def choice_place():
    one_floor = {1:"체력단련장", 2:"정보체육 연구실", 3:"정보R&E실", 4:"입학 사정관실", 5:"진로진학상담실",\
            6:"멀티미디어실", 7:"서버실", 8:"교장실", 9:"행정실", 10:"숙직실",\
            11:"관리실", 12:"행정실장실", 13:"1층진자실", 14:"악기보관실", 15:"음악실", \
            16:"연습실1", 17:"연습실2", 18:"R&E 1", 19:"R&E 2", 20:"R&E 3", \
            21:"R&E 4", 22:"R&E 5", 23:"R&E 6"}

    two_floor = {24:"3-3", 25:"3-4", 26:"2-1", 27:"1학년실", 26:"방송실",\
            28:"회의실", 29:"교무실", 30:"생물연구실", 31:"생물R&E실", 32:"생물실험실",\
            33:"전자현미경실", 34:"생장실", 35:"화학실험실", 36:"화학R&E실", 37:"화학연구실"}

    three_floor = {38:"2-5", 39:"2-4", 40:"2-3", 41:"세미나실", 42:"학생회실",\
            43:"2-2", 44:"진학실", 45:"3층진자실", 46:"2학년실", 47:"지구과학연구실",\
            48:"지구과학R&E실", 49:"지구과학실험실", 50:"국어사회연구실", 51:"물리실험실", 52:"물리R&E실",\
            53:"물리연구실"}

    four_floor = {54:"1-5", 55:"1-4", 56:"1-3", 57:"세미나실", 58:"사진동아리방",\
            59:"1-2", 60:"1-1", 61:"보건실", 62:"소강당", 63:"수학연구실2",\
            64:"영어과 사무실", 65:"영어전용교실", 66:"외국어과연구실", 67:"수학3실", 68:"수학2실",\
            69:"수학1실", 70:"수학연구실1"}
            
    tamgu = {71:"다용도실", 72:"도서관", 73:"3학년학습실", 74:"컴퓨터실", 75:"3-1",\
            76:"3학년실", 77:"3-2"}

def treat_student(act, is_get):  
    if act == "login":
        if 'student_id' in session:
            flash("이미 로그인된 상태입니다.")
            return redirect('/student')
        if is_get:
            return render_template('student/login.html')
        else:
            return login_post()
    elif act == "signup":
        if 'student_id' in session:
            flash("이미 로그인된 상태입니다.")
            return redirect('/student')
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
            return redirect("/student")
        else:
            return abort(405)
    elif act == "apply":
        if is_get:
            return apply_get()
        else:
            return apply_post()
    return abort(404)

