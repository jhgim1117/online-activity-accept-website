from flask import render_template, session, abort

def teacher_get():
    if not 'teacher' in session:
        return abort(403)
    return render_template('/teacher/index.html')

