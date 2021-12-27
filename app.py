from flask import Flask, render_template, request, session, abort
from lib import db
from route import student, admin, teacher, announce
app = Flask(__name__)
app.secret_key = 'asdfasdfadf'
@app.route("/")
def index():
    nickname = ''
    if 'user_id' in session:
        user_id=session['user_id']
        nickname = db.db_execute('SELECT nickname FROM user WHERE id=?', (user_id,))[0]['nickname']
    return render_template('index.html', nickname=nickname)

@app.route("/student", methods = ['GET'])
def student_site():
    if 'teacher_id' in session:
        return abort(403)
    return student.student_get()

@app.route("/student/<path:act>", methods=['GET', 'POST'])
def student_act(act = None):
    if 'teacher_id' in session:
        abort(403)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return student.treat_student(act, True)
    elif request.method == 'POST':
        return student.treat_student(act, False)

@app.route('/admin', methods=['GET'])
def admin_site():
    return admin.admin_get()

@app.route("/admin/<path:act>", methods=['GET', 'POST'])
def admin_act(act = None):
    if request.method == 'GET':
        return admin.treat_admin(act, True)
    elif request.method == 'POST':
        return admin.treat_admin(act, False)

@app.route("/teacher", methods=['GET'])
def teacher_site():
    if 'student_id' in session:
        abort(403)
    return teacher.teacher_get()

@app.route("/teacher/<path:act>", methods=['GET', 'POST'])
def teacher_act(act = None):
    if 'student_id' in session:
        return abort(403)
    if request.method == 'GET':
        return teacher.treat_teacher(act, True)
    elif request.method == 'POST':
        
        return teacher.treat_teacher(act, False)

@app.route("/announce", methods=['GET'])
def announce_get():
    return announce.announce_board()

@app.route("/signout", methods=['GET', 'POST'])
def signout():
    if request.method == 'GET':
        return member.signout_get()
    else:
        return member.signout_post()


if __name__ == '__main__':
    app.run(debug=True)  