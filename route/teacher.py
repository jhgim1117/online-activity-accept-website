from flask import render_template, session, abort, request, flash, redirect
from lib import db
import bcrypt
import datetime

now = datetime.datetime.today()
today = str(now.year)+'-'+'0'*(2-len(str(now.month)))+str(now.month)+'-'+'0'*(2-len(str(now.day)))+str(now.day)

place = {1:"체력단련장", 2:"정보체육 연구실", 3:"정보R&E실", 4:"입학 사정관실", 5:"진로진학상담실",\
        6:"멀티미디어실", 7:"서버실", 8:"교장실", 9:"행정실", 10:"숙직실",\
        11:"관리실", 12:"행정실장실", 13:"1층진자실", 14:"악기보관실", 15:"음악실", \
        16:"연습실1", 17:"연습실2", 18:"R&E 1", 19:"R&E 2", 20:"R&E 3", \
        21:"R&E 4", 22:"R&E 5", 23:"R&E 6", 78:"R&E 7", 79:"R&E 8", 80:"문서고", 81:"역사관",\

        24:"3-3", 25:"3-4", 26:"2-1", 27:"1학년실", 82:"방송실",\
        28:"회의실", 29:"교무실", 30:"생물연구실", 31:"생물R&E실", 32:"생물실험실",\
        33:"전자현미경실", 34:"생장실", 35:"화학실험실", 36:"화학R&E실", 37:"화학연구실",\

        38:"2-5", 39:"2-4", 40:"2-3", 41:"세미나실", 42:"학생회실",\
        43:"2-2", 44:"진학실", 45:"3층진자실", 46:"2학년실", 47:"지구과학연구실",\
        48:"지구과학R&E실", 49:"지구과학실험실", 50:"국어사회연구실", 51:"물리실험실", 52:"물리R&E실",\
        53:"물리연구실",\

        54:"1-5", 55:"1-4", 56:"1-3", 57:"세미나실", 58:"사진동아리방",\
        59:"1-2", 60:"1-1", 61:"보건실", 62:"소강당", 63:"수학연구실2",\
        64:"영어과 사무실", 65:"영어전용교실", 66:"외국어과연구실", 67:"수학3실", 68:"수학2실",\
        69:"수학1실", 70:"수학연구실1",\
        
        71:"다용도실", 72:"도서관", 73:"3학년학습실", 74:"컴퓨터실", 75:"3-1",\
        76:"3학년실", 77:"3-2", -1:"기숙사"}

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
    if not((int(str_homeroom[0]) in range(1, 4) and int(str_homeroom[1]) in range(1, 6)) or str_homeroom == '00'):
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

def config_get():
    teacher_id = session['teacher_id']
    teacher_data = db.db_execute("SELECT * FROM teacher WHERE teacher_id=?", (teacher_id, ))[0]
    if 'teacher_id' in session:
        return render_template(
            '/teacher/config.html',
            name = teacher_data['name'],
            ID = teacher_data['nickname']
        )

def config_post():
    teacher_id = session['teacher_id']
    name = request.form['name']
    nickname = request.form['ID']
    new_pw = request.form["newPW"] #바꿀 비번
    renew_pw = request.form["renewPW"] #바꿀 비번 확인
    present_pw = request.form['nowPW']
    hashed_pw = db.db_execute('SELECT pw FROM teacher WHERE teacher_id=?', (teacher_id,))[0]['pw'] #DB 상의 기존 비번 들고오기
    if not (nickname  and name):
        flash('입력되지 않은 데이터가 있습니다.')
        return redirect('/teacher/config')
    if len(name) < 2 or len(name) > 10:
        flash('이름 길이가 범위에서 벗어났습니다.')
        return redirect('/teacher/config')
    if not new_pw:
        new_pw = present_pw
        renew_pw = present_pw        

    if new_pw == renew_pw: #비번 확인
        if bcrypt.checkpw(present_pw.encode('utf-8'),hashed_pw.encode('utf-8')): #DB 기존 비번과 입력한 비번이 일치하면 DB업데이트 
            hashed_pw = bcrypt.hashpw(new_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.db_execute("UPDATE teacher SET name=?, nickname=?, pw=? WHERE teacher_id=?", (name, nickname, hashed_pw, teacher_id, ))
            flash("성공적으로 변경되었습니다!")
            return redirect("/teacher/config")
        else:
            flash("기존 비밀번호가 일치하지 않습니다!")
            return redirect("/teacher/config")
    else:
        flash("새 비밀번호와 다시 확인 비밀번호가 다릅니다!")
        return redirect("/teacher/config")

def apply_index():
    teacher_id = session['teacher_id']
    teacher_info = db.db_execute("SELECT * FROM teacher WHERE teacher_id=?", (teacher_id, ))[0]
    name = teacher_info['name']
    homeroom = teacher_info['homeroom']
    subject_id = teacher_info['subject_id']
    dayduty = session['dayduty']
    return render_template(
        '/teacher/apply/index.html',
        name = name,
        homeroom = homeroom,
        subject_id = subject_id,
        dayduty = dayduty
    )

def apply_homeroom():
    global today, place
    teacher_id = session['teacher_id']
    teacher_info = db.db_execute("SELECT * FROM teacher WHERE teacher_id=?", (teacher_id, ))[0]
    name = teacher_info['name']
    homeroom = db.db_execute('SELECT homeroom FROM teacher WHERE teacher_id=?', (teacher_id, ))[0]['homeroom']
    req_ids = [list(i.values())[0] for i in db.db_execute("SELECT req_id FROM apply WHERE num/100=? EXCEPT SELECT req_id FROM confirmed_apply", (homeroom, ))]
    apply_list = list()
    for req_id in req_ids:
        apply = db.db_execute("SELECT * FROM apply WHERE req_id=? AND req_date>=?", (req_id, today, ))
        if len(apply):
            apply_list.append(apply[0])
    return render_template(
        '/teacher/apply/list.html',
        apply_list = apply_list,
        act = 'homeroom',
        name = name,
        place = place
    )

def apply_RnE(): #rne table에 있는 student_id랑 student table id 랑 안 맞음 -> db 초기화하면 괜찮아짐
    global today, place
    teacher_id = session['teacher_id']
    teacher_info = db.db_execute("SELECT * FROM teacher WHERE teacher_id=?", (teacher_id, ))[0]
    name = teacher_info['name']
    subject_id = db.db_execute('SELECT subject_id FROM teacher WHERE teacher_id=?', (session['teacher_id'], ))[0]['subject_id']
    student_ids = [list(i.values())[0] for i in db.db_execute("SELECT user_id FROM rne WHERE rne_id=?", (subject_id, ))]
    req_ids = list()
    for student_id in student_ids:
        req_ids_raw = db.db_execute("SELECT req_id FROM apply WHERE req_student=? AND req_date>=? EXCEPT SELECT req_id FROM confirmed_apply", (student_id, today, ))
        for req_id_raw in req_ids_raw:
            req_ids.append(req_id_raw['req_id'])
    apply_list = list()
    for req_id in req_ids:
        apply = db.db_execute("SELECT * FROM apply WHERE req_id=?", (req_id, ))
        apply_list.append(apply[0])
    return render_template(
        '/teacher/apply/list.html',
        apply_list = apply_list,
        act = 'RnE',
        name = name,
        place = place
    )

def apply_dayduty():
    global today, place
    teacher_id = session['teacher_id']
    teacher_info = db.db_execute("SELECT * FROM teacher WHERE teacher_id=?", (teacher_id, ))[0]
    name = teacher_info['name']
    req_ids = [list(i.values())[0] for i in db.db_execute("SELECT req_id FROM apply WHERE req_date>=? EXCEPT SELECT req_id FROM confirmed_apply", (today, ))]
    apply_list = list()
    for req_id in req_ids:
        apply = db.db_execute("SELECT * FROM apply WHERE req_id=?", (req_id, ))
        apply_list.append(apply[0])
    return render_template(
        '/teacher/apply/list.html',
        apply_list = apply_list,
        act = 'dayduty',
        name = name,
        place = place
    )

def apply_allow():
    allow_id = request.form['req_id']
    allowed = 1
    db.db_execute("INSERT INTO confirmed_apply (req_id, allowed) VALUES (?, ?)", (allow_id, allowed, ))

def apply_reject():
    reject_id = request.form['req_id']
    allowed = 0
    db.db_execute("INSERT INTO confirmed_apply (req_id, allowed) VALUES (?, ?)", (reject_id, allowed, ))

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
    elif act == "config":
        if 'teacher_id' in session:
            if is_get:
                return config_get()
            else:
                return config_post()
        else:
            flash('로그인 후 이용해주시길 바랍니다.')
            return redirect('/teacher/login')
    elif path_list[0] == 'apply':
        if 'teacher_id' in session:
            if len(path_list) == 1:
                if is_get:
                    return apply_index()
                else:
                    return abort(405)
            elif path_list[1] == 'homeroom':
                if len(path_list) == 2:
                    if is_get:
                        return apply_homeroom()
                    else:
                        return abort(405)
                elif path_list[2] == 'allow':
                    apply_allow()
                    return redirect('/teacher/apply/homeroom')
                elif path_list[2] == 'reject':
                    apply_reject()
                    return redirect('/teacher/apply/homeroom')
            elif path_list[1] == 'RnE':
                if len(path_list) == 2:
                    if is_get:
                        return apply_RnE()
                    else:
                        return abort(405)
                elif path_list[2] == 'allow':
                    apply_allow()
                    return redirect('/teacher/apply/RnE')
                elif path_list[2] == 'reject':
                    apply_reject()
                    return redirect('/teacher/apply/RnE')
            elif path_list[1] == 'dayduty':
                if len(path_list) == 2:
                    return apply_dayduty()
                elif path_list[2] == 'allow':
                    apply_allow()
                    return redirect('/teacher/apply/dayduty')
                elif path_list[2] == 'reject':
                    apply_reject()
                    return redirect('/teacher/apply/dayduty')
        else:
            flash('로그인 후 이용해주시길 바랍니다.')
            return redirect('/teacher/login')