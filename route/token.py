from flask import render_template, request, redirect
from lib import db
import random



def token_post():
    generation, num = request.form["generation"], request.form["num"]
    token = random.randint(100000, 999999)
    db.db_execute("INSERT INTO token (generation, num, token) VALUES (?, ?, ?)", (generation, num, token))
    return render_template('/admin/token.html')
    
def token_get():
    return render_template('/admin/token.html')

def show_token_list():
    return render_template(
        '/admin/token_list.html',
        token_list = db.db_execute("SELECT * FROM token")
    )