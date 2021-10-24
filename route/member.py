from flask import render_template
def login_get():
    return render_template('user/login.html')