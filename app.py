from flask import Flask, render_template, request, session
from lib import db
from route import member
from route.admin import user_list
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

@app.route("/admin/user_list")
def user_list():
    return user_list.show_user_list()

@app.route("/configdata", methods=['get','POST'])
def configdata():
    if 'user_id' in session:
        return render_template('configdata.html')

@app.route("/admin/token")
def token():
    return token.issue_token()

if __name__ == '__main__':
    app.run(debug=True)