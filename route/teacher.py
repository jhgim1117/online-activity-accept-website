from flask import render_template, session, abort, request

def teacher_get():
    if not 'teacher' in session:
        return abort(403)
    return render_template('/teacher/index.html')

def signup_post():
    name = request.form['name']
    nickname = request.form['nickname']
    plain_pw = request.form['pw']
    token = request.form['token']

    if not(name and nickname and plain_pw and token):
        flash('입력되지 않은 정보가 있습니다.')
        return redirect('/teacher/signup')
    
    if len(name) < 2 or len(name) > 10:
        flash('이름 길이가 범위에서 벗어났습니다.')
        return redirect('/teacher/signup') 
    
    id_list = db.db_execute("SELECT id FROM teacher WHERE nickname=?", (nickname,))
    if len(id_list):
        flash('이미 존재하는 id입니다.')
        return redirect('/teacher/signup')
    
    token_list = db.db_execute("SELECT token FROM token WHERE name=?", (name, ))
    if len(token_list):
        if int(token) != int(token_list[0]['token']):
            flash('토큰이 일치하지 않습니다.')
            return redirect('/teacher/signup')
    else:
        flash('토큰이 등록되어있지 않습니다.')
        return redirect('/teacher/signup')
    db.db_execute('DELETE FROM teacher_token WHERE name=?', (name, ))

    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.db_execute("INERT INTO teacher (name, nickname, pw) values (?, ?, ?);", (name, nickname, hashed_pw))
    flash('회원가입되었습니다. 로그인해주시기 바랍니다.')
    return redirect('/teacher/login')

def login_post():
    id, plain_pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    id_list = db.db_execute("SELECT teacher_id FROM teacher WHERE nickname=?", (id,))
    if not len(id_list):
        flash("id가 존재하지 않습니다.")
        return redirect('/teacher/login')
    teacher_id = id_list[0]['id']
    hashed_pw = db.db_execute('SELECT pw FROM teacher WHERE nickname=?', (id,))[0]['pw']
    if bcrypt.checkpw(plain_pw.encode('utf-8'),hashed_pw.encode('utf-8')):
        
        session['teacher'] = True
        session['teacher_id'] = teacher_id
        return redirect('/')
    else:
        flash('pw가 일치하지 않습니다.')
        return redirect('/teacher/login')