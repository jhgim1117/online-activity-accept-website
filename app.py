from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
from lib import db
from route import member
app = Flask(__name__)
app.secret_key = 'asdfasdfadf'
@app.route("/")
def index():
    nickname = ''
    if 'user_id' in session:
        user_id=session['user_id']
        nickname = db.db_execute('SELECT nickname FROM user WHERE id=?', (user_id,))[0]['nickname']
    return render_template('index.html', nickname=nickname)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return member.login_get()
    else:
        return member.login_post()

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return member.signup_get()
    else:
        return member.signup_post()

@app.route("/signout", methods=['POST'])
def signout():
    session.pop('user_id', None)
    return redirect("/")

@app.route("/configdata", methods=['get','POST'])
def configdata():
    user_id=session['user_id']
    #이름 학번 기수 아이디 가져오기
    nickname = db.db_execute('SELECT nickname FROM user WHERE id=?', (user_id,))[0]['nickname']
    name = db.db_execute('SELECT nickname FROM user WHERE id=?', (user_id,))[0]['name']
    num = db.db_execute('SELECT nickname FROM user WHERE id=?', (user_id,))[0]['num']
    generation = db.db_execute('SELECT nickname FROM user WHERE id=?', (user_id,))[0]['generation']

    if 'user_id' in session: #로그인 상태일때만
        return render_template('configdata.html', nickname=nickname, name=name, num=num, generation=generation)



if __name__ == '__main__':
    app.run(debug=True)