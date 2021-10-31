from flask import Flask, render_template, request, session, abort
from lib import db
from route import member, admin, apply
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

@app.route('/admin', methods=['GET'])
def admin_site():
    return admin.admin_get()

@app.route("/admin/<path:act>", methods=['GET', 'POST'])
def admin_act(act = None):
    if request.method == 'GET':
        return admin.treat_admin(act, True)
    elif request.method == 'POST':
        return admin.treat_admin(act, False)

@app.route('/apply', methods=['GET', 'POST'])
def apply_page():
    if not 'user_id' in session:
        abort(403)
    if request.method == 'GET':
        return apply.apply_get()
    else:
        return apply.apply_post()

if __name__ == '__main__':
    app.run(debug=True)