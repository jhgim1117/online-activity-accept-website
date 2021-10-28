from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
from lib import db
from route import member, user_list, token
app = Flask(__name__)
app.secret_key = 'asdfasdfadf'

@app.route("/") ##main page
def index():
    nickname = ''
    if 'user_id' in session:
        user_id=session['user_id']
        nickname = db.db_execute('SELECT nickname FROM user WHERE id=?', (user_id,))[0]['nickname']
    return render_template('index.html', nickname=nickname)

@app.route("/login", methods=['GET', 'POST']) ##login page
def login():
    if request.method == 'GET':
        return member.login_get()
    else:
        return member.login_post()

@app.route("/signup", methods=['GET', 'POST']) ##signup page
def signup():
    if request.method == 'GET':
        return member.signup_get()
    else:
        return member.signup_post()

@app.route("/signout", methods=['POST']) ##signout page
def signout():
    session.pop('user_id', None)
    return redirect("/")

@app.route("/configdata", methods=['GET','POST'])
def configdata():
    if request.method == 'POST':
        user_id=session['user_id']
        #이름 학번 기수 아이디 가져오기
        nickname = db.db_execute('SELECT nickname FROM user WHERE id=?', (user_id,))[0]['nickname']
        name = db.db_execute('SELECT name FROM user WHERE id=?', (user_id,))[0]['name']
        num = db.db_execute('SELECT num FROM user WHERE id=?', (user_id,))[0]['num']
        generation = db.db_execute('SELECT generation FROM user WHERE id=?', (user_id,))[0]['generation']

        if 'user_id' in session: #로그인 상태일때만
            return render_template('user/configdata.html', nickname=nickname, name=name, num=num, generation=generation)
            
    else:
        pass

@app.route("/admin") ##admin/user list
def admin():
    return render_template('admin/index.html')

@app.route("/admin/user_list") ##admin/user list
def user_list_show():
    return user_list.show_user_list()

@app.route("/admin/token", methods=['GET', 'POST'])
def issue_token():
    if request.method == 'GET':
        return token.token_get()
    else:
        return token.token_post()

if __name__ == '__main__':
    app.run(debug=True)