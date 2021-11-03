from flask import Flask, render_template, request, session, abort
from lib import db
from route import student, admin, apply, teacher
app = Flask(__name__)
app.secret_key = 'asdfasdfadf'
@app.route("/")
def index():
    print(session)
    name=''
    if 'student_id' in session or 'teacher_id' in session:
        if 'student_id' in session:
            student_id=session['student_id']
            name = db.db_execute('SELECT name FROM student WHERE id=?', (student_id,))[0]['name']
        else:
            teacher_id = session['teacher_id']
            name = db.db_execute('SELECT name FROM teacher WHERE teacher_id=?', (teacher_id, ))[0]['name']
    return render_template('index.html', name=name)

@app.route("/student/<path:act>", methods=['GET', 'POST'])
def student_act(act = None):
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

@app.route('/apply', methods=['GET', 'POST'])
def apply_page():
    if not 'student_id' in session:
        abort(403)
    if request.method == 'GET':
        return apply.apply_get()
    else:
        return apply.apply_post()

@app.route("/teacher", methods=['GET'])
def teacher_site():
    return teacher.teacher_get()

@app.route("/teacher/<path:act>", methods=['GET', 'POST'])
def teacher_act(act = None):
    if request.method == 'GET':
        return teacher.treat_teacher(act, True)
    elif request.method == 'POST':
        return teacher.treat_teacher(act, False)

if __name__ == '__main__':
    app.run(debug=True)