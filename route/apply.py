from flask import render_template, session, request, flash, redirect
from lib import db

def apply_get():
    return render_template('/apply/index.html')

def apply_post():
    req_user = session['user_id']
    req_date = request.form['req_date']
    req_start_time = request.form['req_start_time']
    req_end_time = request.form['req_end_time']
    place = request.form['place']
    reason = request.form['reason']
    teacher = request.form['teacher']

    # 빈칸 거르기
    if not (req_date and req_start_time and req_end_time and place and reason and teacher):
        flash('입력되지 않은 데이터가 있습니다.')
        return redirect('/apply')
    print(type(req_date), req_start_time, req_end_time, place, reason, teacher)
    

    return render_template('')