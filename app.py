from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
from lib import db
from route import member, admin
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
def user_list_show():
    return admin.show_user_list()

@app.route("/signout", methods=['POST'])
def signout():
    session.pop('user_id', None)
    session.pop('admin', None)
    return redirect("/")


@app.route("/configdata", methods=['GET','POST']) #회워 정보 수정페이지
def configdata():
    if request.method=="POST":
        return member.configdata_post()

    else:
        pass

@app.route("/configdata/update", methods=['GET','POST']) #회원 정보 수정 실시
def configdata_update():
    if request.method=="POST":
        return member.db_config_update()

    else:
        pass

@app.route('/admin')
def admin_site():
    return admin.show_admin_site()

@app.route("/admin/token", methods=['GET', 'POST'])
def issue_token():
    if request.method == 'GET':
        return admin.token_get()
    elif request.method == 'POST':
        return admin.token_post()

@app.route("/admin/token/DELETE", methods=['POST'])
def token_delete():
     return admin.token_delete()
    
@app.route('/admin/token/LIST')
def token_list():
    return admin.show_token_list()

if __name__ == '__main__':
    app.run(debug=True)