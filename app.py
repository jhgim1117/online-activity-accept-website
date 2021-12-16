from flask import Flask, render_template, request, session, abort
from lib import db
from route import student, admin, teacher
app = Flask(__name__)
app.secret_key = 'asdfasdfadf'
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/student", methods = ['GET'])
def student_site():
    if 'teacher_id' in session:
        return abort(403)
    return student.student_get()

@app.route("/student/<path:act>", methods=['GET', 'POST'])
def student_act(act = None):
    if 'teacher_id' in session:
        abort(403)
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

if __name__ == '__main__':
    app.run(debug=True)