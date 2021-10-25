from flask import Flask, render_template, request
from route import member
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return member.login_get()
    else:
        return member.login_post()

if __name__ == '__main__':
    app.run(debug=True)