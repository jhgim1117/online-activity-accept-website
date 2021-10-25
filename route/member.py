from flask import render_template, request
def login_get():
    return render_template('user/login.html')

def login_post():
    id, pw = request.form["ID"], request.form["password"] #로그인할 때 아이디, 비번 get
    
    print(id)
    print(pw)
    
    return render_template('user/login.html')

def signup_get():
    pass

def signup_post():
    
    print("100")