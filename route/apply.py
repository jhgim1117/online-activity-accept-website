from flask import render_template, session, request, flash, redirect
from lib import db
import datetime

def apply_get():
    return render_template('/student/apply/index.html')

def apply_post():
    req_student = session['student_id']
    req_date = request.form['req_date']
    req_start_time = request.form['req_start_time']
    req_end_time = request.form['req_end_time']
    place = request.form['place']
    reason = request.form['reason']
    teacher = request.form['teacher']

    # 빈칸 거르기
    if not (req_date and req_start_time and req_end_time and place and reason and teacher):
        flash('입력되지 않은 데이터가 있습니다.')
    req_date = datetime.date.fromisoformat(req_date)
    formatted_req_start_time = datetime.time.fromisoformat(req_start_time)
    formatted_req_end_time = datetime.time.fromisoformat(req_end_time)
    if formatted_req_start_time >= formatted_req_end_time:
        flash('활동 시간이 올바르지 않습니다.')
        return redirect('/apply')
    db.db_execute("insert into apply (datetime, req_student, req_date, req_start_time, req_end_time, place, reason, teacher_id) values ((SELECT datetime('now', '+9 hours')), ?, ?, ?, ?, ?, ?, ?);", (req_student, req_date, req_start_time, req_end_time, place, reason, teacher))
    return ''