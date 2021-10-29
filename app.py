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

@app.route("/member/<path:act>", methods=['GET', 'POST'])
def member_act(act = None):
    if request.method == 'GET':
        return member.treat_member(act, True)
    elif request.method == 'POST':
        return member.treat_member(act, False)

@app.route('/admin')
def admin_site():
    return admin.admin_get()

@app.route("/admin/<path:act>", methods=['GET', 'POST'])
def admin_act(act = None):
    if request.method == 'GET':
        return admin.treat_admin(act, True)
    elif request.method == 'POST':
        return admin.treat_admin(act, False)

if __name__ == '__main__':
    app.run(debug=True)