from flask import Flask, render_template, request, session
from route import member
app = Flask(__name__)
app.secret_key = 'asdfasdfadf'
@app.route("/")
def index():
    user_id =''
    if 'user_id' in session:
        user_id=session['user_id']
    return render_template('index.html', user_id=user_id)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return member.login_get()
    else:
        return member.login_post()

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return member.signup_get()
    else:
        return member.signup_post()

if __name__ == '__main__':
    app.run(debug=True)